#!/usr/bin/env python3
"""Validate Suite Integrity — Phase 0 version.

Dynamic path resolution — works from any working directory.

Checks:
  1. Structural checks (directories and boot files exist).
  2. 7-Zone skeleton (knowledge/, scripts/, templates/, data/, loop/, assets/).
  3. Frontmatter validity (YAML structure, required keys per AGENTS.md §10).
  4. Registry consistency (matching skills-registry.json, orphan detection).

Exit codes:
  0 = all checks pass
  1 = structural checks fail (missing dirs/files/zones)
  2 = schema validity fail (yaml parse error or missing required keys)
  3 = registry consistency fail (skills-registry.json mismatch with filesystem)
"""

import os
import sys
import json
import re
from datetime import datetime, timezone

try:
    import yaml
except ImportError:
    print("Error: pyyaml package is required. Install it via 'pip install pyyaml'.", file=sys.stderr)
    sys.exit(1)

ZONE_DIRS = ["knowledge", "scripts", "templates", "data", "loop", "assets"]
REQUIRED_FM_FIELDS = {
    "name": str,
    "description": str,
    "version": str,
    "suite": str,
    "tags": list,
    "when_to_use": str,
}

def resolve_repo_root():
    """Resolve repo root from script location.
    Script at:  WASHVN/.claude/scripts/validate_suite_integrity.py
    Root is:    WASHVN/
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(script_dir, "..", ".."))


def gen_escalation_report(errors, warnings, registry_path, output_dir):
    """Generate escalation_report.yaml on failure (eval v1 đề xuất 4)."""
    report = {
        "triggered_at": datetime.now(timezone.utc).isoformat(),
        "escalation_depth": 1,
        "pipeline_phase": "phase-0-validate-suite-integrity",
        "failure_summary": f"{len(errors)} error(s), {warnings} warning(s)",
        "errors": errors,
        "registry_path": registry_path,
        "action_required": "Fix errors above and re-run validate_suite_integrity.py",
        "recommended_recovery": "manual inspection",
    }
    report_path = os.path.join(output_dir, "escalation_report.yaml")
    try:
        os.makedirs(output_dir, exist_ok=True)
        with open(report_path, "w", encoding="utf-8") as f:
            yaml.dump(report, f, default_flow_style=False, allow_unicode=True)
        print(f"  → Escalation report: {report_path}", file=sys.stderr)
    except Exception as e:
        print(f"  → Warning: Could not write escalation report: {e}", file=sys.stderr)


def check_7zone(skill_dir, name):
    """Check that all 6 sub-zone directories exist."""
    missing = []
    for zone in ZONE_DIRS:
        if not os.path.isdir(os.path.join(skill_dir, zone)):
            missing.append(zone)
    return missing


def parse_frontmatter(content, name):
    """Parse YAML frontmatter from SKILL.md content.
    Returns (frontmatter_dict|None, error_msg|None).
    Handles BOM, embedded --- markers.
    """
    raw = content
    bom = "\ufeff"
    if raw.startswith(bom):
        raw = raw[len(bom):]

    raw = raw.strip()
    if not raw:
        return None, None  # stub

    if not raw.startswith("---"):
        return None, "Missing frontmatter start marker '---'"

    parts = raw.split("---")
    if len(parts) < 3:
        return None, "Missing frontmatter end marker '---'"

    fm_str = parts[1]
    try:
        fm = yaml.safe_load(fm_str)
    except Exception as e:
        return None, f"Failed to parse YAML frontmatter: {e}"

    if not isinstance(fm, dict):
        return None, "Frontmatter is not a YAML dictionary"

    return fm, None


def validate_frontmatter(fm, name, skill_dir):
    """Validate frontmatter fields against AGENTS.md §10 quality gates.
    Returns list of error dicts.
    """
    errors = []

    dir_name = os.path.basename(skill_dir)

    # Check all required fields exist and have correct type
    for field, expected_type in REQUIRED_FM_FIELDS.items():
        val = fm.get(field)
        if field == "tags":
            if not val:
                errors.append({"skill": name, "type": "schema", "detail": f"Missing required field '{field}'"})
                continue
            if not isinstance(val, list):
                errors.append({"skill": name, "type": "schema", "detail": f"Field '{field}' must be a list, got {type(val).__name__}"})
                continue
            continue
        if field == "version":
            if not val:
                errors.append({"skill": name, "type": "schema", "detail": "Missing required field 'version'"})
                continue
            if not isinstance(val, str):
                errors.append({"skill": name, "type": "schema", "detail": f"Field 'version' must be a string, got {type(val).__name__} ('{val}')"})
                continue
            if not re.match(r"^\d+\.\d+\.\d+$", val):
                errors.append({"skill": name, "type": "schema", "detail": f"Version '{val}' is not valid semantic version (expected x.y.z)"})
                continue
            continue
        if not val:
            errors.append({"skill": name, "type": "schema", "detail": f"Missing required field '{field}'"})
            continue

    # Name matches registry name
    fm_name = fm.get("name")
    if fm_name != name:
        errors.append({"skill": name, "type": "schema", "detail": f"Frontmatter name '{fm_name}' != registry name '{name}'"})

    # Name matches directory name
    if fm_name != dir_name:
        errors.append({"skill": name, "type": "schema", "detail": f"Frontmatter name '{fm_name}' != directory name '{dir_name}'"})

    # Suite must be WASHVN
    fm_suite = fm.get("suite")
    if fm_suite != "WASHVN":
        errors.append({"skill": name, "type": "schema", "detail": f"Invalid suite '{fm_suite}' (expected 'WASHVN')"})

    return errors


def walk_skill_dirs(repo_root):
    """Fallback directory walk when skills-registry.json is missing."""
    ver3 = os.path.join(repo_root, "raw", "ver-3")
    if not os.path.isdir(ver3):
        return []
    results = []
    exclude = {"_shared", "roadmaps"}
    for entry in sorted(os.listdir(ver3)):
        if entry in exclude:
            continue
        if os.path.isdir(os.path.join(ver3, entry)):
            results.append({
                "name": entry,
                "src_path": os.path.join("raw", "ver-3", entry),
                "boot_file": "SKILL.md",
            })
    return results


def main():
    repo_root = resolve_repo_root()
    errors = []
    warnings = []
    escalation_dir = os.path.join(repo_root, ".skill-context", "_state-archive")

    registry_path = os.path.join(repo_root, "skills-registry.json")

    # --- Load skills list ---
    skills = []
    registry_mode = True

    if not os.path.exists(registry_path):
        print(f"Warning: skills-registry.json not found at {registry_path}", file=sys.stderr)
        print("Info: Falling back to directory walk of raw/ver-3/", file=sys.stderr)
        skills = walk_skill_dirs(repo_root)
        registry_mode = False
        if not skills:
            errors.append({"skill": None, "type": "structural", "detail": "No skills found via fallback — raw/ver-3/ is empty or missing"})
            gen_escalation_report(errors, len(warnings), registry_path, escalation_dir)
            print(f"FAIL: {len(errors)} error(s), 0 valid (warnings: {len(warnings)})", file=sys.stderr)
            sys.exit(1)
    else:
        try:
            with open(registry_path, "r", encoding="utf-8") as f:
                registry = json.load(f)
        except Exception as e:
            errors.append({"skill": None, "type": "registry", "detail": f"Failed to parse skills-registry.json: {e}"})
            gen_escalation_report(errors, len(warnings), registry_path, escalation_dir)
            print(f"FAIL: {len(errors)} error(s), 0 valid (warnings: {len(warnings)})", file=sys.stderr)
            sys.exit(3)

        # Validate workspace_paths (dynamic check)
        ws = registry.get("workspace_paths", {})
        source_dir = ws.get("source_dir", "")
        if source_dir:
            sd_abs = os.path.join(repo_root, source_dir)
            if not os.path.isdir(sd_abs):
                warnings.append(f"workspace_paths.source_dir '{source_dir}' not found at {sd_abs}")
                print(f"  Warning: workspace_paths.source_dir '{source_dir}' → not found", file=sys.stderr)

        skills = registry.get("skills", [])
        if not skills:
            errors.append({"skill": None, "type": "registry", "detail": "skills array is empty in skills-registry.json"})
            gen_escalation_report(errors, len(warnings), registry_path, escalation_dir)
            print(f"FAIL: {len(errors)} error(s), 0 valid (warnings: {len(warnings)})", file=sys.stderr)
            sys.exit(1)

    total_skills = len(skills)
    valid_count = 0

    # --- Validate each skill ---
    for skill in skills:
        name = skill.get("name")
        src_path_rel = skill.get("src_path")
        boot_file = skill.get("boot_file", "SKILL.md")

        if not name or not src_path_rel:
            errors.append({"skill": name or "unknown", "type": "registry", "detail": f"Invalid entry (missing name or src_path): {skill}"})
            continue

        skill_dir = os.path.join(repo_root, src_path_rel)

        # 1. Directory exists
        if not os.path.isdir(skill_dir):
            errors.append({"skill": name, "type": "structural", "detail": f"Skill directory not found at {skill_dir}"})
            continue

        # 2. Boot file exists
        boot_path = os.path.join(skill_dir, boot_file)
        if not os.path.isfile(boot_path):
            errors.append({"skill": name, "type": "structural", "detail": f"Boot file '{boot_file}' not found at {boot_path}"})
            continue

        # 3. 7-Zone skeleton check
        missing_zones = check_7zone(skill_dir, name)
        if missing_zones:
            errors.append({"skill": name, "type": "structural", "detail": f"Missing 7-Zone directories: {', '.join(missing_zones)}"})

        # 4. Read and parse frontmatter
        with open(boot_path, "r", encoding="utf-8") as f:
            content = f.read()

        fm, fm_err = parse_frontmatter(content, name)
        if fm_err:
            errors.append({"skill": name, "type": "schema", "detail": fm_err})
            continue
        if fm is None:
            continue  # stub — counted as not valid but not an error

        # 5. Validate frontmatter fields
        fm_errors = validate_frontmatter(fm, name, skill_dir)
        if fm_errors:
            errors.extend(fm_errors)
            continue

        valid_count += 1

    # --- Orphan detection (only in registry mode) ---
    if registry_mode:
        ver3 = os.path.join(repo_root, "raw", "ver-3")
        if os.path.isdir(ver3):
            registered = set()
            for s in skills:
                sp = s.get("src_path", "")
                if sp.startswith("raw/ver-3/"):
                    registered.add(sp[len("raw/ver-3/"):])
                elif sp:
                    registered.add(sp)
            exclude = {"_shared", "roadmaps"}
            for entry in sorted(os.listdir(ver3)):
                if entry in exclude:
                    continue
                if entry not in registered and os.path.isdir(os.path.join(ver3, entry)):
                    warnings.append(f"Orphan skill directory '{entry}' — not in skills-registry.json")
                    print(f"  Warning: Skill dir '{entry}' exists but is not registered", file=sys.stderr)

    # --- Summary ---
    if errors:
        print(f"FAIL: {len(errors)} error(s), {valid_count}/{total_skills} valid, {len(warnings)} warning(s)", file=sys.stderr)
        gen_escalation_report(errors, len(warnings), registry_path, escalation_dir)
        has_structural = any(e["type"] == "structural" for e in errors)
        has_schema = any(e["type"] == "schema" for e in errors)
        if has_structural:
            sys.exit(1)
        elif has_schema:
            sys.exit(2)
        else:
            sys.exit(3)
    else:
        print(f"OK: {valid_count}/{total_skills} skills valid ({len(warnings)} warning(s))")
        sys.exit(0)


if __name__ == "__main__":
    main()
