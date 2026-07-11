#!/usr/bin/env python3
"""Location resolver — 5-location precedence + shadow detection.

Primitive only: I/O + compare. No business logic.
[TỬ TODO #T4.2] [TỬ DESIGN §3 scripts/, §8 R2]
"""
import json
import sys
from pathlib import Path

LOCATIONS = [
    {"priority": 1, "key": "user", "file": "~/.claude/settings.json"},
    {"priority": 2, "key": "project", "file": ".claude/settings.json"},
    {"priority": 3, "key": "local", "file": ".claude/settings.local.json"},
    {"priority": 4, "key": "plugin", "file": "plugin manifest"},
    {"priority": 5, "key": "agent_frontmatter", "file": ".claude/agents/<name>.md"},
]


def precedence_order() -> list:
    return [loc["key"] for loc in sorted(LOCATIONS, key=lambda x: x["priority"])]


def detect_shadow(target_key: str, event: str, matcher: str, existing: dict) -> list:
    """Return warnings for higher-priority locations that define same event+matcher.

    `existing` maps location_key -> {"hooks": {event: [matchers...]}}.
    Policy: WARN only. Never auto-merge (design §9 Q7).
    """
    warnings = []
    target_priority = next(l["priority"] for l in LOCATIONS if l["key"] == target_key)
    for loc in LOCATIONS:
        if loc["priority"] <= target_priority:
            continue
        defined = existing.get(loc["key"], {}).get("hooks", {})
        matchers = defined.get(event, [])
        if matcher in matchers:
            warnings.append(
                f"SHADOW: {loc['key']} (priority {loc['priority']}) already defines "
                f"event={event} matcher={matcher} — will override your write."
            )
    return warnings


def main() -> int:
    if len(sys.argv) < 2:
        print(json.dumps({"precedence": precedence_order()}, ensure_ascii=False))
        return 0
    # argv[1] = path to existing-map json
    existing = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    target_key, event, matcher = sys.argv[2], sys.argv[3], sys.argv[4]
    out = {
        "precedence": precedence_order(),
        "shadow_warnings": detect_shadow(target_key, event, matcher, existing),
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
