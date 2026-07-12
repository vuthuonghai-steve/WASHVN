#!/usr/bin/env python3
"""
find_antipatterns.py — Anti-Pattern Detector (Stage 0.7 Miner)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Barrel module — re-exports all public symbols from sub-modules.

Zero-dependency Python3 script that heuristically detects anti-patterns
(name, symptom, solution) from workspace skill files using single-pass I/O.
Designed for skill-knowledge-miner in the WASHVN Master Skill Suite.

Usage:
    python3 find_antipatterns.py --workspace /path/to/workspace
    python3 find_antipatterns.py --workspace /path --exploration exploration.md
    python3 find_antipatterns.py --dry-run --workspace /path

Exit codes:
    0: anti_patterns >= min_patterns threshold (or threshold not met without --strict)
    1: anti_patterns < min_patterns threshold AND --strict is set
    2: workspace error
"""

import os
import sys
import json

from skill_miner_common import (
    Logger,
    read_file_safely,
    collect_scannable_files,
    write_yaml_safely,
)

from _antipatterns_args import parse_args
from _antipatterns_core import _is_must_not_file, _rule_to_antipattern, deduplicate
from _antipatterns_patterns import (
    RE_NEGATIVE_KEYWORDS,
    RE_TODO,
    scan_must_not_sections,
    scan_negative_keywords,
    scan_placeholders,
    scan_ai_slop,
)
from _antipatterns_exploration import extract_from_exploration

__all__ = [
    # Sub-modules (public API)
    "parse_args",
    "_is_must_not_file",
    "_rule_to_antipattern",
    "deduplicate",
    "RE_NEGATIVE_KEYWORDS",
    "RE_TODO",
    "scan_must_not_sections",
    "scan_negative_keywords",
    "scan_placeholders",
    "scan_ai_slop",
    "extract_from_exploration",
    "main",
    # Re-exports from skill_miner_common (convenience)
    "Logger",
    "read_file_safely",
    "collect_scannable_files",
    "write_yaml_safely",
]


# ---------------------------------------------------------------------------
# Main pipeline — single-pass I/O
# ---------------------------------------------------------------------------
def main():
    args = parse_args()
    logger = Logger("find_antipatterns", verbose=args.verbose)

    workspace = os.path.abspath(args.workspace)
    if not os.path.isdir(workspace):
        logger.error(f"Workspace not found: {workspace}")
        sys.exit(2)

    logger.info(f"Scanning workspace: {workspace}")

    all_patterns = []

    # -------------------------------------------------------------------
    # Single-pass: collect all scannable files once
    # -------------------------------------------------------------------
    scan_dirs = [
        os.path.join(workspace, 'skills', 'ver-3'),
        os.path.join(workspace, '.claude'),
    ]
    # Union of all extensions needed by patterns 1-4
    all_files = collect_scannable_files(
        scan_dirs, ('.py', '.md', '.yaml', '.yml', '.sh', '.ts', '.js'), logger
    )

    logger.info(f"Collected {len(all_files)} files")

    # -------------------------------------------------------------------
    # Single-pass: read each file once, cache by type
    # -------------------------------------------------------------------
    must_not_contents = {}   # Pattern 1
    general_contents = {}    # Patterns 2-4

    for fpath in all_files:
        content = read_file_safely(fpath, logger)
        if content is None:
            continue

        # Pattern 1 — must_not sections (SKILL.md + agent .md)
        if _is_must_not_file(fpath, workspace):
            must_not_contents[fpath] = content

        # Patterns 2-4 — content-based scans
        general_contents[fpath] = content

    logger.info(
        f"Cached {len(general_contents)} files"
        f" ({len(must_not_contents)} for must_not scan)"
    )

    # -------------------------------------------------------------------
    # Pattern 1: must_not sections
    # -------------------------------------------------------------------
    logger.info("Pattern 1: must_not sections...")
    all_patterns.extend(scan_must_not_sections(must_not_contents, logger))

    # -------------------------------------------------------------------
    # Pattern 2: Negative keywords (scope narrowed to .md)
    # -------------------------------------------------------------------
    logger.info("Pattern 2: negative keywords...")
    all_patterns.extend(scan_negative_keywords(general_contents, workspace, logger))

    # -------------------------------------------------------------------
    # Pattern 3: Placeholder detection
    # -------------------------------------------------------------------
    logger.info("Pattern 3: placeholder detection...")
    all_patterns.extend(scan_placeholders(general_contents, workspace, logger))

    # -------------------------------------------------------------------
    # Pattern 4: AI slop / quality (Python files only)
    # -------------------------------------------------------------------
    logger.info("Pattern 4: code quality patterns...")
    all_patterns.extend(scan_ai_slop(general_contents, workspace, logger))

    # -------------------------------------------------------------------
    # Exploration fallback
    # -------------------------------------------------------------------
    if args.exploration:
        logger.info("Exploration fallback...")
        all_patterns.extend(extract_from_exploration(args.exploration, logger))

    # Deduplicate
    unique = deduplicate(all_patterns)
    logger.info(f"Raw: {len(all_patterns)} -> Unique: {len(unique)}")

    # -------------------------------------------------------------------
    # Output YAML
    # -------------------------------------------------------------------
    print(f"# Extracted anti-patterns: {len(unique)}")

    if args.target:
        target = os.path.abspath(args.target)
        os.makedirs(target, exist_ok=True)
        outpath = os.path.join(target, "antipatterns-extracted.yaml")
        write_yaml_safely(outpath, unique, "anti_patterns", logger)
    else:
        # Stdout with safe JSON serialization
        for ap in unique:
            # Strip internal keys (prefixed with _)
            ap_clean = {k: v for k, v in ap.items() if not k.startswith('_')}
            print(f"  - {json.dumps(ap_clean, ensure_ascii=False)}")

    # -------------------------------------------------------------------
    # Exit code: only fail on --strict
    # -------------------------------------------------------------------
    below_threshold = len(unique) < args.min_patterns
    if below_threshold:
        msg = f"Only {len(unique)} anti-patterns found (minimum: {args.min_patterns})"
        if args.strict:
            logger.error(msg)
            sys.exit(1)
        else:
            logger.warn(f"{msg} (pass --strict to fail on this)")
    sys.exit(0)


if __name__ == '__main__':
    main()
