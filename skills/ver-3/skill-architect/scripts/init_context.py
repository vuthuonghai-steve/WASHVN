#!/usr/bin/env python3
"""
init_context.py — Initialize .skill-context/{target_skill}/ for skill-architect ver-3.

Creates context directory, template files (design.md, todo.md, build-log.md),
and DRC contract (data/drc.yaml). Safe-create policy: does NOT overwrite existing files.

Usage:
    python init_context.py <skill-name> [--project-root <path>]

Example:
    python init_context.py my-api-analyzer
"""

import sys
import os
import re
import shutil
from pathlib import Path
from datetime import datetime, timezone


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

KEBAB_CASE_PATTERN = re.compile(r"^[a-z][a-z0-9]*(-[a-z0-9]+)*$")
MAX_WALK_UP_LEVELS = 10

DRC_TEMPLATE_FILENAME = "drc_contract_template.yaml"

TEMPLATE_FILES = {
    "design.md": "design.md.template",
    "todo.md": "todo.md.template",
    "build-log.md": "build-log.md.template",
}

PLACEHOLDERS = {
    "{skill_name}": "",
    "{target_variable}": "target_skill",
    "{date}": "",
    "{generated_at}": "",
    "{author}": "Skill Architect",
}


# ---------------------------------------------------------------------------
# Shared bootstrap: locate _shared/ directory
# ---------------------------------------------------------------------------

def ensure_shared_bundled(script_dir: Path) -> Path:
    """Resolve path to skills/ver-3/_shared/ for ver-3 structure.

    ver-3 has no _shared.zip — always resolves via ../../_shared/
    relative to the script_dir (skills/ver-3/skill-architect/scripts/).

    Returns Path to _shared/ directory. Raises RuntimeError if not found.
    """
    skill_root = script_dir.parent       # skills/ver-3/skill-architect/
    shared_dir = skill_root.parent / "_shared"  # skills/ver-3/_shared/

    if shared_dir.is_dir():
        return shared_dir

    raise RuntimeError(
        f"_shared/ not found at {shared_dir}. "
        "Ensure skills/ver-3/_shared/ exists. "
        "Expected relative path: ../../_shared/ from script location."
    )


# ---------------------------------------------------------------------------
# DRC contract initialization
# ---------------------------------------------------------------------------

def init_drc_contract(shared_dir: Path, data_dir: Path, skill_name: str) -> str:
    """Initialize data/drc.yaml from _shared/templates/drc_contract_template.yaml.

    Performs placeholder substitution for skill_name, suite, and version.

    Returns status string: 'CREATED', 'SKIPPED (already exists)', or
    'FAILED: <reason>'.
    """
    drc_template_path = shared_dir / "templates" / DRC_TEMPLATE_FILENAME
    drc_output_path = data_dir / "drc.yaml"

    if drc_output_path.exists():
        return "SKIPPED (already exists)"

    if not drc_template_path.is_file():
        return f"FAILED: template not found at {drc_template_path}"

    try:
        content = drc_template_path.read_text(encoding="utf-8")
        # Substitute placeholders
        content = content.replace("<skill-name-placeholder>", skill_name)
        content = content.replace("0.0.1", "3.0.0")  # skill_version
        content = content.replace("YYYY-MM-DD", datetime.now(timezone.utc).strftime("%Y-%m-%d"))
        content = content.replace("input_artifact_name", "exploration.md")
        content = content.replace("input_filename.md", "exploration.md")
        content = content.replace("this-skill", "skill-architect")
        content = content.replace("phase-X", "P1-Read")
        content = content.replace("output_artifact_id", "architect_design")
        content = content.replace("output_filename.md", "design.md")
        content = content.replace("criteria.schema.json", "design.schema.yaml")
        content = content.replace("validation_fail", "meta_gate_fail")
        content = content.replace("fallback-escalation", "production-quality-gatekeeper")

        # Set upstream and downstream routing
        lines = content.split("\n")
        new_lines = []
        for line in lines:
            if "upstream_skills: []" in line:
                new_lines.append(line.replace("[]", "[skill-explorer, skill-knowledge-miner]"))
            elif "downstream_skills: []" in line:
                new_lines.append(line.replace("[]", "[production-quality-gatekeeper, skill-planner]"))
            else:
                new_lines.append(line)
        content = "\n".join(new_lines)

        # Replace field_name placeholders
        content = content.replace("field_name_1", "design_md_path")
        content = content.replace("field_name_2", "zone_mapping_complete")

        data_dir.mkdir(parents=True, exist_ok=True)
        drc_output_path.write_text(content, encoding="utf-8")
        return "CREATED"

    except Exception as e:
        return f"FAILED: {e}"


def validate_drc_template(shared_dir: Path) -> bool:
    """Validate that DRC template exists and is readable."""
    template_path = shared_dir / "templates" / DRC_TEMPLATE_FILENAME
    if not template_path.is_file():
        print(f"  WARNING: DRC template not found at {template_path}")
        return False
    return True


# ---------------------------------------------------------------------------
# Context initialization
# ---------------------------------------------------------------------------

def find_project_root(start_dir: Path) -> Path | None:
    """Walk up from start_dir to find the directory containing .claude/."""
    current = start_dir.resolve()
    for _ in range(MAX_WALK_UP_LEVELS):
        if (current / ".claude").is_dir():
            return current
        parent = current.parent
        if parent == current:
            break
        current = parent
    return None


def validate_skill_name(name: str) -> bool:
    """Check that skill name is valid kebab-case."""
    return bool(KEBAB_CASE_PATTERN.match(name))


def resolve_template_content(
    template_name: str, output_name: str, templates_dir: Path
) -> str:
    """Read template file or return fallback content."""
    template_path = templates_dir / template_name
    if template_path.is_file():
        return template_path.read_text(encoding="utf-8")
    print(f"  WARNING: Template '{template_name}' not found, using fallback")
    return f"# {output_name}\n---\nskill_name: {output_name}\n---\n"


def replace_placeholders(content: str, replacements: dict[str, str]) -> str:
    """Replace all placeholders in content."""
    for placeholder, value in replacements.items():
        content = content.replace(placeholder, value)
    return content


def safe_create_file(filepath: Path, content: str) -> str:
    """Create file only if it does not exist. Return status string."""
    if filepath.exists():
        return "SKIPPED (already exists)"
    filepath.parent.mkdir(parents=True, exist_ok=True)
    filepath.write_text(content, encoding="utf-8")
    return "CREATED"


def main() -> int:
    import argparse
    parser = argparse.ArgumentParser(
        description="Initialize .skill-context/{target_skill}/ for skill-architect ver-3"
    )
    parser.add_argument("skill_name", help="Skill name in kebab-case (e.g., my-api-analyzer)")
    parser.add_argument("--project-root", default=None, help="Project root path (default: auto-detect)")
    parser.add_argument("--context-dir", default=None, help="Context directory path (default: {project-root}/.skill-context/{skill-name})")
    args = parser.parse_args()

    skill_name = args.skill_name

    if not validate_skill_name(skill_name):
        print(f"Error: '{skill_name}' is not valid kebab-case.")
        print("  Use lowercase letters, numbers, and hyphens only.")
        return 1

    # --- Bootstrap _shared/ path ---
    script_dir = Path(__file__).resolve().parent
    try:
        shared_dir = ensure_shared_bundled(script_dir)
        print(f"  _shared/ resolved: {shared_dir}")
        drc_template_ok = validate_drc_template(shared_dir)
        print(f"  DRC template found: {drc_template_ok}")
    except RuntimeError as e:
        print(f"[BOOT WARNING] {e}", file=sys.stderr)
        shared_dir = None
        drc_template_ok = False

    # --- Detect project root ---
    if args.project_root:
        project_root = Path(args.project_root)
    else:
        project_root = find_project_root(Path.cwd())
        if project_root is None:
            print("Error: Could not find .claude/ directory.")
            return 1

    print(f"  Project root: {project_root}")

    # --- Resolve context directory ---
    if args.context_dir:
        skill_context_dir = Path(args.context_dir)
        context_root = skill_context_dir.parent
    else:
        context_root = project_root / ".skill-context"
        skill_context_dir = context_root / skill_name

    resources_dir = skill_context_dir / "resources"
    templates_dir = script_dir.parent / "templates"
    data_dir = skill_context_dir / "data"

    # --- Prepare placeholders ---
    now_iso = datetime.now(timezone.utc).isoformat()
    replacements = {
        "{skill_name}": skill_name,
        "{target_variable}": "target_skill",
        "{date}": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "{generated_at}": now_iso,
        "{author}": "Skill Architect",
    }

    # --- Create directories ---
    context_root.mkdir(parents=True, exist_ok=True)
    skill_context_dir.mkdir(exist_ok=True)
    resources_dir.mkdir(exist_ok=True)

    print(f"\n  Context directory: {skill_context_dir}")
    print("-" * 50)

    # --- Create files from templates ---
    results = []
    for output_name, template_name in TEMPLATE_FILES.items():
        raw_content = resolve_template_content(template_name, output_name, templates_dir)
        content = replace_placeholders(raw_content, replacements)
        filepath = skill_context_dir / output_name
        status = safe_create_file(filepath, content)
        results.append((output_name, status))
        print(f"  {output_name:20s} → {status}")

    # --- Initialize DRC contract ---
    if shared_dir and drc_template_ok:
        drc_status = init_drc_contract(shared_dir, data_dir, skill_name)
        results.append(("data/drc.yaml", drc_status))
        print(f"  data/drc.yaml       → {drc_status}")
    else:
        # Fallback: create minimal drc.yaml manually
        data_dir.mkdir(parents=True, exist_ok=True)
        fallback_drc = f"""skill_name: "{skill_name}"
skill_version: "3.0.0"
suite: "WASHVN"
last_updated: "{datetime.now(timezone.utc).strftime('%Y-%m-%d')}"
inputs:
  - name: "exploration.md"
    path_template: ".skill-context/{skill_name}/exploration.md"
    format: "markdown"
    required: true
    consumed_by: "skill-architect"
    downstream_phase: "P1-Read"
outputs:
  - file_id: "architect_design"
    path_template: ".skill-context/{skill_name}/design.md"
    format: "markdown"
    lifecycle_status: "WORM"
    versioning: "semver"
routing:
  upstream_skills: [skill-explorer, skill-knowledge-miner]
  downstream_skills: [production-quality-gatekeeper, skill-planner]
  fallback_targets:
    - trigger: "meta_gate_fail"
      target_skill: "production-quality-gatekeeper"
      target_stage: "validate"
state_persistence:
  context_bus_write: true
  state_yaml_write: true
  fields_to_write: [design_md_path, zone_mapping_complete]
"""
        drc_path = data_dir / "drc.yaml"
        status = safe_create_file(drc_path, fallback_drc)
        results.append(("data/drc.yaml (fallback)", status))
        print(f"  data/drc.yaml       → {status} (fallback, no template)")

    # --- Summary ---
    created_count = sum(1 for _, s in results if s == "CREATED")
    skipped_count = sum(1 for _, s in results if "SKIPPED" in s)
    fail_count = sum(1 for _, s in results if "FAIL" in s)
    print(f"\n  Done: {created_count} created, {skipped_count} skipped, {fail_count} failed")
    print(f"  Resources dir: {resources_dir}")

    return 0 if fail_count == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
