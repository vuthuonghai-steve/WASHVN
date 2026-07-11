#!/usr/bin/env python3
"""Matcher classifier — char-set -> exact_or|regex + footgun warning.

Primitive only: I/O + rule eval. No business logic.
[TỬ TODO #T4.1] [TỬ DESIGN §3 scripts/, §8 R1]
Source rules: data/matcher-char-rules.yaml (or inline fallback).
"""
import json
import re
import sys

EXACT_CHARS = re.compile(r"^[a-zA-Z0-9 \-,|]+$")


def classify(matcher: str) -> dict:
    """Return {mode, warning} for a matcher string."""
    if matcher is None or matcher == "":
        return {"mode": "empty", "warning": "empty matcher"}
    # footgun: literal '.' forces regex
    warning = None
    if "." in matcher:
        warning = "matcher contains '.' -> forced REGEX mode (not exact). Verify intent."
    mode = "regex" if not EXACT_CHARS.match(matcher) else "exact_or"
    return {"mode": mode, "warning": warning}


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: matcher_classifier.py <matcher>", file=sys.stderr)
        return 2
    result = classify(sys.argv[1])
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
