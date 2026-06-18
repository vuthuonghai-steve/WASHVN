#!/usr/bin/env python3
"""code_auditor.py — entrypoint for the modular Google Code Review auditor.

Usage:
    python3 code_auditor.py <path-to-py-file> [--target-skill NAME]

Emits .skill-context/{target_skill}/audit-metrics.yaml and prints a human
summary. Exits 0 if no blocking violations, 1 if blocking, 2 on errors.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Allow running this script from the scripts/ directory without installing
sys.path.insert(0, str(Path(__file__).resolve().parent))

from auditor import audit_file_content  # noqa: E402
from auditor.reporting import emit_yaml, human_summary  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Static code auditor producing audit-metrics.yaml",
    )
    parser.add_argument("file_path", help="Path to the Python file to audit")
    parser.add_argument(
        "--target-skill",
        default="production-code-reviewer",
        help="Target skill context directory under .skill-context/",
    )
    args = parser.parse_args()

    result = audit_file_content(args.file_path)

    # Drop error-only results straight to stderr and bail
    if "error" in result and result.get("exit_code") == 2:
        print(f"ERROR: {result['error']}", file=sys.stderr)
        return 2

    output_dir = Path(f".skill-context/{args.target_skill}")
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / "audit-metrics.yaml"
    written = emit_yaml(result, output_file)
    print(f"Metrics written: {written}")
    print(human_summary(result))
    return result["exit_code"]


if __name__ == "__main__":
    sys.exit(main())
