"""Report emission — YAML/JSON output + human-readable summary."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def emit_yaml(result: dict, dest: Path) -> Path:
    """Write the audit result dict to a YAML file. Uses a small emitter to avoid
    external dependencies (PyYAML is preferred but not required)."""
    try:
        import yaml  # type: ignore
        dest.write_text(
            yaml.safe_dump(result, sort_keys=False, allow_unicode=True),
            encoding="utf-8",
        )
    except ImportError:
        # Fallback to JSON if PyYAML is unavailable
        dest = dest.with_suffix(".json")
        dest.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    return dest


def human_summary(result: dict) -> str:
    """Build the console summary block printed after the YAML."""
    file_path = result.get("file", "?")
    total = result.get("total_lines", 0)
    vcount = result.get("violations_count", 0)
    bcount = result.get("blocking_count", 0)
    verdict = "❌ FAIL (Has Blocking)" if bcount > 0 else "✅ PASS"
    lines = [
        "",
        f"--- AUDITOR ANALYSIS SUMMARY FOR: {file_path} ---",
        f"Total Lines: {total}",
        f"Total Violations: {vcount}",
        f"Blocking Issues: {bcount}",
        f"Verdict: {verdict}",
        "",
    ]
    for v in result.get("violations", []):
        lines.append(f"- [{v['id']}] {v['name']} ({v['severity'].upper()}) at line {v['line']}")
        lines.append(f"  Error: {v['error']}")
        lines.append(f"  Fix: {v['fix_hint']}")
    return "\n".join(lines)
