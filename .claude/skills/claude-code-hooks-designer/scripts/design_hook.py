#!/usr/bin/env python3
"""Core design engine — event select + matcher classify + handler choose + spec assembly.

Primitive orchestration over other primitives + data files. No embedded domain reasoning.
Validates guardrails: continueOnBlock only Stop/SubagentStop; no PostToolUse block intent.
[TỬ TODO #T4.4] [TỬ DESIGN §3 scripts/, §5 flow, §8 R6]
"""
import json
import subprocess
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent


def _load_yaml(name: str) -> dict:
    # minimal YAML list-of-dicts loader for our data files (no PyYAML dep)
    import re
    text = (SKILL_DIR / "data" / name).read_text(encoding="utf-8")
    events = []
    for m in re.finditer(r"^\s*-\s*name:\s*(\S+)\s*\n((?:\s+[a-z_]+:.*\n?)*)", text, re.M):
        ev = {"name": m.group(1)}
        for fm in re.finditer(r"^\s*([a-z_]+):\s*(.+)$", m.group(2), re.M):
            ev[fm.group(1)] = fm.group(2).strip()
        events.append(ev)
    return events


def validate_continue_on_block(event: str, cob: bool) -> list:
    errs = []
    if cob and event not in ("Stop", "SubagentStop"):
        errs.append(f"continueOnBlock=true INVALID on '{event}' (only Stop/SubagentStop).")
    return errs


def validate_blocking_event(event: str, want_block: bool) -> list:
    errs = []
    if want_block and event != "PreToolUse":
        errs.append(f"blocking hook NOT allowed on '{event}' (only PreToolUse blocks).")
    return errs


def run(matcher: str, event: str, handler_type: str, want_block: bool, cob: bool, if_cond: str) -> dict:
    # delegate classification to matcher_classifier.py
    cls = subprocess.run([sys.executable, str(SKILL_DIR / "scripts" / "matcher_classifier.py"), matcher],
                         capture_output=True, text=True)
    cls_result = json.loads(cls.stdout or '{"mode":"unknown","warning":null}')
    errs = validate_continue_on_block(event, cob) + validate_blocking_event(event, want_block)
    spec = {
        "event": event,
        "matcher": matcher,
        "matcher_mode": cls_result["mode"],
        "footgun_warning": cls_result.get("warning"),
        "handler_type": handler_type,
        "want_block": want_block,
        "continueOnBlock": cob,
        "if_condition": if_cond,
        "errors": errs,
    }
    return spec


def main() -> int:
    if len(sys.argv) < 4:
        print("usage: design_hook.py <matcher> <event> <handler_type> [--block] [--cob] [--if 'cond']", file=sys.stderr)
        return 2
    matcher, event, handler_type = sys.argv[1], sys.argv[2], sys.argv[3]
    want_block = "--block" in sys.argv
    cob = "--cob" in sys.argv
    if_cond = ""
    if "--if" in sys.argv:
        if_cond = sys.argv[sys.argv.index("--if") + 1]
    spec = run(matcher, event, handler_type, want_block, cob, if_cond)
    print(json.dumps(spec, ensure_ascii=False, indent=2))
    return 1 if spec["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
