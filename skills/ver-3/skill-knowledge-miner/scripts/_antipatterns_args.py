"""
_antipatterns_args.py — CLI argument parsing for find_antipatterns.py

Split from find_antipatterns.py during barrel refactor.
"""

import argparse


def parse_args():
    """Parse CLI arguments for the anti-pattern detector."""
    parser = argparse.ArgumentParser(description="Heuristic anti-pattern detector")
    parser.add_argument("--target", default=None,
                        help="Output directory for domain-handbook.md context")
    parser.add_argument("--workspace", required=True,
                        help="Root workspace path")
    parser.add_argument("--min-patterns", type=int, default=3,
                        help="Minimum anti-patterns required (default: 3)")
    parser.add_argument("--verbose", action="store_true",
                        help="Print detection details")
    parser.add_argument("--exploration", default=None,
                        help="Path to exploration.md for context")
    parser.add_argument("--strict", action="store_true",
                        help="Exit code 1 when below min-patterns threshold (default: warn only)")
    return parser.parse_args()
