"""
_terms_args.py — CLI argument parsing for mine_for_terms.py

Split from mine_for_terms.py during barrel refactor.
"""

import argparse


def parse_args():
    """Parse CLI arguments for the glossary term extractor."""
    parser = argparse.ArgumentParser(description="Heuristic glossary term extractor")
    parser.add_argument("--target-dir", default=None,
                        help="Output directory for domain-handbook.md context")
    parser.add_argument("--workspace", required=True,
                        help="Root workspace path to scan")
    parser.add_argument("--min-terms", type=int, default=10,
                        help="Minimum glossary terms required (default: 10)")
    parser.add_argument("--verbose", action="store_true",
                        help="Print extraction details")
    parser.add_argument("--dry-run", action="store_true",
                        help="Show what would be extracted without writing")
    parser.add_argument("--exploration", default=None,
                        help="Path to exploration.md for parsing frontmatter context")
    parser.add_argument("--strict", action="store_true",
                        help="Exit code 1 when below min-terms threshold (default: warn only)")
    return parser.parse_args()
