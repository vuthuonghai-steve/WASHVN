"""
_antipatterns_core.py — Shared helpers & deduplication for find_antipatterns.py

Split from find_antipatterns.py during barrel refactor.
"""

import os
import re


def _is_must_not_file(fpath, workspace):
    """Check if a file should be scanned for must_not sections (SKILL.md or agent .md)"""
    basename = os.path.basename(fpath)
    if basename == 'SKILL.md':
        return True
    rel = os.path.relpath(fpath, workspace)
    if rel.startswith('.claude/agents') and fpath.endswith('.md'):
        return True
    return False


def _rule_to_antipattern(rule, source, pattern_type):
    """Convert a must_not rule to (name, symptom, solution)"""
    name = f"Violation: {rule[:50].strip()}"
    if len(name) > 60:
        name = name[:57] + "..."

    symptom = f"Found in {source}: {rule[:100]}"
    solution = f"Adhere to rule: {rule[:100]}"
    if "không" in rule.lower():
        solution = f"Rewrite to comply: {rule}"

    return {
        "name": name,
        "symptom": symptom,
        "solution": solution,
        "_source": source,
    }


def deduplicate(antipatterns):
    """Deduplicate: fuzzy match on name (normalized)"""
    seen = {}
    for ap in antipatterns:
        key = ap["name"].lower().strip()
        key = re.sub(r'\s+', ' ', key)[:60]
        if key not in seen:
            seen[key] = ap
        else:
            existing = seen[key]
            if len(ap.get("symptom", "")) + len(ap.get("solution", "")) > \
               len(existing.get("symptom", "")) + len(existing.get("solution", "")):
                seen[key] = ap
    return list(seen.values())
