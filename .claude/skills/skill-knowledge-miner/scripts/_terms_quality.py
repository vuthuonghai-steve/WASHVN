"""
_terms_quality.py — Deduplication & quality filtering for mine_for_terms.py

Split from mine_for_terms.py during barrel refactor.
"""

import re


def deduplicate(terms):
    """Deduplicate by term (case-insensitive), prefer longer definition"""
    seen = {}
    for term, defn in terms:
        key = term.lower().strip()
        if key not in seen or len(defn) > len(seen[key]):
            seen[key] = defn.strip()
    return [{"term": k, "definition": v} for k, v in seen.items()]


def quality_filter(entries, min_term_len=3):
    """Remove entries with empty/placeholder definitions"""
    filtered = []
    placeholder_patterns = re.compile(r'todo|fixme|placeholder|\.\.\.|^\s*$', re.IGNORECASE)
    for entry in entries:
        term = entry.get("term", "")
        defn = entry.get("definition", "")
        if len(term) < min_term_len:
            continue
        if not defn or placeholder_patterns.search(defn):
            continue
        filtered.append(entry)
    return filtered
