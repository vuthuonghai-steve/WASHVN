#!/usr/bin/env python3
"""
init_context.py — Deterministic IO bootstrap for .skill-context/{target_skill}/

Creates directory structure and extracts _shared.zip if missing.
NO template content generation.

Usage:
    python init_context.py <skill-name>

Example:
    python init_context.py my-api-analyzer
"""

import sys
import re
import subprocess
from pathlib import Path


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

KEBAB_CASE_PATTERN = re.compile(r"^[a-z][a-z0-9]*(-[a-z0-9]+)*$")
MAX_WALK_UP_LEVELS = 10

# ---------------------------------------------------------------------------
# Shared bootstrap: auto-extract _shared.zip if missing
# ---------------------------------------------------------------------------

def ensure_shared_bundled(script_dir: Path) -> Path:
    """Check if ../_shared/ exists. If not, auto-extract from references/_shared.zip.

    Returns path to _shared/ directory.
    Raises RuntimeError if extraction fails.
    """
    skill_root = script_dir.parent  # skill-architect/
    shared_dir = skill_root.parent / "_shared"  # ../_shared/

    if shared_dir.is_dir():
        return shared_dir

    # _shared missing — try bundled zip
    zip_path = skill_root / "references" / "_shared.zip"
    if not zip_path.is_file():
        raise RuntimeError(
            f"_shared/ not found at {shared_dir} and bundled zip not found at {zip_path}. "
            "Ensure the skill package includes references/_shared.zip or install _shared/ separately."
        )

    # Extract to skill_root's parent (where _shared/ should live)
    extract_target = skill_root.parent
    print(f"  [BOOT] _shared/ missing. Extracting {zip_path} -> {extract_target}", file=sys.stderr)
    try:
        result = subprocess.run(
            ["unzip", "-q", "-o", str(zip_path), "-d", str(extract_target)],
            capture_output=True,
            text=True,
            check=True,
        )
    except subprocess.CalledProcessError as e:
        raise RuntimeError(
            f"Failed to extract {zip_path}: {e.stderr or e.stdout}"
        ) from e
    except FileNotFoundError:
        # unzip not available — fallback to Python zipfile
        import zipfile
        with zipfile.ZipFile(zip_path, "r") as zf:
            zf.extractall(path=extract_target)

    if not shared_dir.is_dir():
        raise RuntimeError(
            f"Extraction succeeded but {shared_dir} still missing. "
            "Check zip contents."
        )

    print(f"  [BOOT] _shared/ extracted successfully.", file=sys.stderr)
    return shared_dir



# ---------------------------------------------------------------------------
# Functions
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



def main() -> int:
    import argparse
    parser = argparse.ArgumentParser(description="Initialize .skill-context/{target_skill}/ directory structure")
    parser.add_argument("skill_name", help="Skill name in kebab-case (e.g., my-api-analyzer)")
    parser.add_argument("--project-root", default=None, help="Project root path (default: auto-detect)")
    parser.add_argument("--context-dir", default=None, help="Context directory path (default: {project-root}/.skill-context/{target_skill})")
    parser.add_argument("--skills-root", default=None, help="Skills root path (default: parent of skill-architect)")
    args = parser.parse_args()
    
    skill_name = args.skill_name

    if not validate_skill_name(skill_name):
        print(f"Error: '{skill_name}' is not valid kebab-case.")
        print("  Use lowercase letters, numbers, and hyphens only.")
        print("  Example: my-api-analyzer, error-handler, sequence-diagram")
        return 1

    # --- Bootstrap _shared/ if missing ---
    script_dir = Path(__file__).resolve().parent  # Define early for ensure_shared_bundled
    try:
        ensure_shared_bundled(script_dir)
    except RuntimeError as e:
        print(f"[BOOT WARNING] {e}", file=sys.stderr)

    # --- Detect project root (supports --project-root override) ---
    if args.project_root:
        project_root = Path(args.project_root)
    else:
        project_root = find_project_root(Path.cwd())
        if project_root is None:
            print("Error: Could not find .claude/ directory.")
            print("  Run this script from within the project directory.")
            return 1

    print(f"Project root: {project_root}")

    # --- Resolve paths (supports --context-dir and --skills-root overrides) ---
    if args.context_dir:
        context_root = Path(args.context_dir).parent
        skill_context_dir = Path(args.context_dir)
    else:
        context_root = project_root / ".skill-context"
        skill_context_dir = context_root / skill_name
    resources_dir = skill_context_dir / "resources"

    # --- Create directories ---
    context_root.mkdir(exist_ok=True)
    skill_context_dir.mkdir(exist_ok=True)
    resources_dir.mkdir(exist_ok=True)

    print(f"\nContext directory: {skill_context_dir}")
    print(f"Resources dir: {resources_dir}")
    print("-" * 50)

    return 0


if __name__ == "__main__":
    sys.exit(main())
