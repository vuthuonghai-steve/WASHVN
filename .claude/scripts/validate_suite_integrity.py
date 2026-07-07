#!/usr/bin/env python3
"""Validate Suite Integrity — Phase 0 version.

Checks:
  1. Structural checks (directories and boot files exist).
  2. Frontmatter validity (YAML structure, required keys).
  3. Registry consistency (matching skills-registry.json).

Exit codes:
  0 = all checks pass
  1 = structural checks fail (missing dirs/files)
  2 = schema validity fail (yaml parse error or missing required keys)
  3 = registry consistency fail (skills-registry.json mismatch with filesystem)
"""

import os
import sys
import json
import re

try:
    import yaml
except ImportError:
    print("Error: pyyaml package is required. Install it using 'pip install pyyaml'.", file=sys.stderr)
    sys.exit(1)

def main():
    # Locate the repository root relative to the script location
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Script is at WASHVN/.claude/scripts/validate_suite_integrity.py
    # Repo root is two levels up: WASHVN/
    repo_root = os.path.abspath(os.path.join(script_dir, "..", ".."))

    registry_path = os.path.join(repo_root, "skills-registry.json")
    if not os.path.exists(registry_path):
        print(f"Error: skills-registry.json not found at {registry_path}", file=sys.stderr)
        sys.exit(1)

    try:
        with open(registry_path, "r", encoding="utf-8") as f:
            registry = json.load(f)
    except Exception as e:
        print(f"Error parsing skills-registry.json: {e}", file=sys.stderr)
        sys.exit(3)

    skills = registry.get("skills", [])
    if not skills:
        print("Warning: No skills registered in skills-registry.json", file=sys.stderr)
        sys.exit(0)

    valid_count = 0
    total_skills = len(skills)

    for skill in skills:
        name = skill.get("name")
        src_path_rel = skill.get("src_path")
        boot_file = skill.get("boot_file", "SKILL.md")

        if not name or not src_path_rel:
            print(f"Error: Invalid skill entry in registry: {skill}", file=sys.stderr)
            sys.exit(3)

        skill_dir = os.path.join(repo_root, src_path_rel)
        
        # 1. Structural checks
        if not os.path.exists(skill_dir) or not os.path.isdir(skill_dir):
            print(f"Structural Error: Skill directory not found for '{name}' at {skill_dir}", file=sys.stderr)
            sys.exit(1)

        boot_file_path = os.path.join(skill_dir, boot_file)
        if not os.path.exists(boot_file_path) or not os.path.isfile(boot_file_path):
            print(f"Structural Error: Boot file '{boot_file}' not found for '{name}' at {boot_file_path}", file=sys.stderr)
            sys.exit(1)

        # Read boot file content
        with open(boot_file_path, "r", encoding="utf-8") as f:
            content = f.read().strip()

        # If file is empty, it is a stub. It is structural ok, but frontmatter is not yet valid.
        # During Phase 0, empty files are expected and allowed. We do not throw Exit 2 for empty files,
        # but we do not count them as valid.
        if not content:
            continue

        # Parse YAML frontmatter
        if not content.startswith("---"):
            print(f"Schema Error: Missing frontmatter start marker '---' in '{name}' boot file", file=sys.stderr)
            sys.exit(2)

        parts = content.split("---")
        if len(parts) < 3:
            print(f"Schema Error: Missing frontmatter end marker '---' in '{name}' boot file", file=sys.stderr)
            sys.exit(2)

        frontmatter_str = parts[1]
        try:
            frontmatter = yaml.safe_load(frontmatter_str)
        except Exception as e:
            print(f"Schema Error: Failed to parse YAML frontmatter for '{name}': {e}", file=sys.stderr)
            sys.exit(2)

        if not isinstance(frontmatter, dict):
            print(f"Schema Error: Frontmatter for '{name}' is not a YAML dictionary", file=sys.stderr)
            sys.exit(2)

        # Validate frontmatter keys
        fm_name = frontmatter.get("name")
        fm_version = frontmatter.get("version")
        fm_suite = frontmatter.get("suite")

        # Name check
        if fm_name != name:
            print(f"Schema Error: Frontmatter name '{fm_name}' does not match registry name '{name}'", file=sys.stderr)
            sys.exit(2)

        # Suite check
        if fm_suite != "WASHVN":
            print(f"Schema Error: Frontmatter suite '{fm_suite}' is invalid for '{name}' (expected 'WASHVN')", file=sys.stderr)
            sys.exit(2)

        # Version check (semver pattern: x.y.z)
        if not fm_version or not re.match(r"^\d+\.\d+\.\d+$", str(fm_version)):
            print(f"Schema Error: Frontmatter version '{fm_version}' for '{name}' is missing or not a valid semantic version", file=sys.stderr)
            sys.exit(2)

        valid_count += 1

    print(f"OK: {valid_count}/{total_skills} skills valid")
    sys.exit(0)

if __name__ == "__main__":
    main()
