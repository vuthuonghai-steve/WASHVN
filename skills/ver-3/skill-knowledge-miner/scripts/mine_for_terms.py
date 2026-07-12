#!/usr/bin/env python3
"""
mine_for_terms.py — Heuristic Glossary Extractor (Stage 0.7 Miner)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Barrel module — re-exports all public symbols from sub-modules.

Zero-dependency Python3 script that extracts glossary terms (term + definition pairs)
from workspace files using priority-based heuristics. Designed for skill-knowledge-miner
in the WASHVN Master Skill Suite.

Usage:
    python3 mine_for_terms.py --target-dir .skill-context/{name} --workspace /path/to/workspace
    python3 mine_for_terms.py --target-dir .skill-context/{name} --workspace /path --exploration exploration.md
    python3 mine_for_terms.py --dry-run --workspace /path

Exit codes:
    0: glossary >= min_terms threshold (or threshold not met without --strict)
    1: glossary < min_terms threshold AND --strict is set
    2: input/directory error
"""

import os
import sys
import json

from skill_miner_common import Logger, read_file_safely, write_yaml_safely

from _terms_args import parse_args
from _terms_extractors import (
    RE_GLOSSARY_HEADING,
    RE_TABLE_ROW,
    RE_BULLET_TERM,
    RE_PIPE_TERM,
    extract_from_knowledge,
    extract_from_claude_agents,
    extract_from_temps_spec,
    extract_from_shared,
    extract_from_exploration,
)
from _terms_quality import deduplicate, quality_filter

__all__ = [
    # Sub-modules (public API)
    "parse_args",
    "RE_GLOSSARY_HEADING",
    "RE_TABLE_ROW",
    "RE_BULLET_TERM",
    "RE_PIPE_TERM",
    "extract_from_knowledge",
    "extract_from_claude_agents",
    "extract_from_temps_spec",
    "extract_from_shared",
    "extract_from_exploration",
    "deduplicate",
    "quality_filter",
    "main",
    # Re-exports from skill_miner_common (convenience)
    "Logger",
    "read_file_safely",
    "write_yaml_safely",
]


# ---------------------------------------------------------------------------
# Main extraction pipeline
# ---------------------------------------------------------------------------
def main():
    args = parse_args()
    logger = Logger("mine_for_terms", verbose=args.verbose)

    workspace = os.path.abspath(args.workspace)
    if not os.path.isdir(workspace):
        logger.error(f"Workspace not found: {workspace}")
        sys.exit(2)

    logger.info(f"Scanning workspace: {workspace}")

    all_terms = []

    # Priority A
    logger.info("Priority A: knowledge/ dirs...")
    all_terms.extend(extract_from_knowledge(workspace, logger))

    # Priority B
    logger.info("Priority B: .claude/agents/...")
    all_terms.extend(extract_from_claude_agents(workspace, logger))

    # Priority C
    logger.info("Priority C: Temps/spec/...")
    all_terms.extend(extract_from_temps_spec(workspace, logger))

    # Priority D
    logger.info("Priority D: _shared/knowledge/...")
    all_terms.extend(extract_from_shared(workspace, logger))

    # Priority E
    if args.exploration:
        logger.info("Priority E: exploration.md...")
        all_terms.extend(extract_from_exploration(args.exploration, logger))

    # Deduplicate
    unique = deduplicate(all_terms)

    # Quality filter
    clean = quality_filter(unique)

    # Sort alphabetically
    clean.sort(key=lambda x: x["term"].lower())

    logger.info(f"Raw: {len(all_terms)} -> Unique: {len(unique)} -> Clean: {len(clean)}")

    # Output
    if args.dry_run:
        print(f"# DRY RUN: would extract {len(clean)} terms (min required: {args.min_terms})")
        for entry in clean[:5]:
            print(f"#  - {entry['term']}: {entry['definition'][:60]}...")
        if len(clean) > 5:
            print(f"#  ... and {len(clean)-5} more")
    else:
        print(f"# Extracted glossary: {len(clean)} terms")
        if args.target_dir:
            target = os.path.abspath(args.target_dir)
            os.makedirs(target, exist_ok=True)
            outpath = os.path.join(target, "glossary-extracted.yaml")
            write_yaml_safely(outpath, clean, "glossary", logger)
        else:
            # Stdout fallback — safe JSON serialization
            for entry in clean:
                print(f"  - {json.dumps(entry, ensure_ascii=False)}")

    # Exit code: only fail on --strict
    below_threshold = len(clean) < args.min_terms
    if below_threshold:
        msg = f"Only {len(clean)} terms extracted (minimum: {args.min_terms})"
        if args.strict:
            logger.error(msg)
            sys.exit(1)
        else:
            logger.warn(f"{msg} (pass --strict to fail on this)")
    sys.exit(0)


if __name__ == '__main__':
    main()
