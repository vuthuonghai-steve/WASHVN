"""
_antipatterns_patterns.py — Heuristic pattern scanners for find_antipatterns.py

Split from find_antipatterns.py during barrel refactor.
Contains Pattern 1 (must_not sections), Pattern 2 (negative keywords),
Pattern 3 (placeholders), and Pattern 4 (AI-slop / code quality).
"""

import os
import re
from _antipatterns_core import _rule_to_antipattern


# ---------------------------------------------------------------------------
# Pattern 1: Parse must_not sections in skill files
# ---------------------------------------------------------------------------
def scan_must_not_sections(file_contents, logger=None):
    """Pattern 1 — Parse must_not: YAML blocks and must_not: markdown sections"""
    antipatterns = []
    for fpath, content in file_contents.items():
        skill_name = os.path.basename(os.path.dirname(fpath))
        if fpath.endswith('.md') and '.claude/agents' in fpath:
            skill_name = os.path.basename(fpath).replace('.md', '')

        results = _parse_must_not_content(fpath, content, skill_name, logger)
        antipatterns.extend(results)
        if results and logger and logger.verbose:
            logger.debug(f"  [P1] {skill_name}: {len(results)} rules")
    return antipatterns


def _parse_must_not_content(fpath, content, skill_name, logger=None):
    """Extract anti-patterns from must_not sections in a single file's content"""
    results = []

    # Pattern A: YAML frontmatter must_not: list
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            in_must_not = False
            for line in parts[1].split('\n'):
                stripped = line.strip()
                if stripped == 'must_not:' or stripped.startswith('must_not:'):
                    in_must_not = True
                    continue
                if in_must_not:
                    if stripped.startswith('- '):
                        rule = stripped[2:].strip().strip('"').strip("'")
                        if rule and len(rule) > 5:
                            results.append(
                                _rule_to_antipattern(rule, skill_name, "YAML must_not")
                            )
                    elif stripped and not stripped.startswith('-') and not stripped.startswith('#'):
                        in_must_not = False

    # Pattern B: <instructions><must_not> block in markdown body
    must_not_section = re.search(
        r'<instructions>.*?must_not:\s*\n(.*?)(?=</instructions>|must:|\Z)',
        content, re.DOTALL,
    )
    if must_not_section:
        block = must_not_section.group(1)
        for m in re.finditer(r'^\s*-\s+(.+)$', block, re.MULTILINE):
            rule = m.group(1).strip()
            if rule and len(rule) > 5:
                results.append(
                    _rule_to_antipattern(rule, skill_name, "instructions must_not")
                )

    # Pattern C: ## must_not section in body
    for m in re.finditer(r'^##\s+must_not\s*$.*?(?=^##|\Z)',
                         content, re.MULTILINE | re.DOTALL):
        block = m.group(0)
        for bm in re.finditer(r'^\s*[-*]\s+(.+)$', block, re.MULTILINE):
            rule = bm.group(1).strip()
            if rule and len(rule) > 5 and 'must_not' not in rule.lower():
                results.append(
                    _rule_to_antipattern(rule, skill_name, "section must_not")
                )

    return results


# ---------------------------------------------------------------------------
# Pattern 2: Negative keyword scan
# Scope narrowed to .md files only to dramatically reduce false-positives.
# ---------------------------------------------------------------------------
RE_NEGATIVE_KEYWORDS = re.compile(
    r'(không\s+(?:được|nên|có|phải|thể|bao giờ)|'
    r'cấm|tranh|tránh|never|do\s+not|must\s+not|'
    r'anti-pattern|anti_pattern|chống chỉ định|'
    r'should not|shouldn\'t|cannot|can\'t)',
    re.IGNORECASE,
)


def scan_negative_keywords(file_contents, workspace, logger=None):
    """Pattern 2 — Scan for negative keywords in .md files only."""
    antipatterns = []
    for fpath, content in file_contents.items():
        if not fpath.endswith('.md'):
            continue

        for m in RE_NEGATIVE_KEYWORDS.finditer(content):
            keyword = m.group(0).strip()
            start = max(0, m.start() - 40)
            end = min(len(content), m.end() + 60)
            context = content[start:end].replace('\n', ' ').strip()

            rel_path = os.path.relpath(fpath, workspace)
            antipatterns.append({
                "name": f'Negative keyword: "{keyword}"',
                "symptom": f"Found in {rel_path}: ...{context}...",
                "solution": (
                    f"Review context around '{keyword}' in {rel_path}; "
                    f"ensure this prohibition is intentional and documented"
                ),
                "_source": rel_path,
            })

    return antipatterns


# ---------------------------------------------------------------------------
# Pattern 3: Placeholder detection (TODO/FIXME/HACK/XXX)
# ---------------------------------------------------------------------------
RE_TODO = re.compile(
    r'(?:TODO|FIXME|HACK|XXX|KHÓA|Tạm thời)\s*[:-]?\s*(.*)', re.IGNORECASE
)


def scan_placeholders(file_contents, workspace, logger=None):
    """Pattern 3 — Scan for TODO/FIXME/mock/HACK comments"""
    antipatterns = []
    for fpath, content in file_contents.items():
        rel_path = os.path.relpath(fpath, workspace)
        for m in RE_TODO.finditer(content):
            detail = m.group(1).strip() if m.group(1) else "(no detail)"
            antipatterns.append({
                "name": f"Placeholder: {m.group(0).split(':')[0]}",
                "symptom": f"Found in {rel_path}: \"{detail}\"",
                "solution": (
                    f"Implement or remove the {m.group(0).split(':')[0]} in {rel_path} "
                    f"before production (NFR-9: zero placeholder density)"
                ),
                "_source": rel_path,
            })
            if logger and logger.verbose:
                logger.debug(f"  [P3] {rel_path}: {m.group(0).split(':')[0]}")
    return antipatterns


# ---------------------------------------------------------------------------
# Pattern 4: Generic AI-slop / code quality patterns
# ---------------------------------------------------------------------------
def scan_ai_slop(file_contents, workspace, logger=None):
    """Pattern 4 — Catch generic AI-slop patterns (empty except, pass stubs, type: ignore)"""
    antipatterns = []
    for fpath, content in file_contents.items():
        if not fpath.endswith('.py'):
            continue
        rel_path = os.path.relpath(fpath, workspace)

        # Empty except blocks:  except ...: \n    pass
        for m in re.finditer(r'except\s*.*?:\s*\n\s+pass\s*$', content, re.MULTILINE):
            antipatterns.append({
                "name": "Empty except block",
                "symptom": f"Found in {rel_path}: except ...: pass — suppresses errors silently",
                "solution": "Add specific exception handling or at minimum log the error",
                "_source": rel_path,
            })

        # type: ignore without comment (bare suppress)
        for m in re.finditer(r'#\s*type:\s*ignore\s*$', content, re.MULTILINE):
            line_content = (
                content[:m.start()].split('\n')[-1].strip()
                if m.start() > 0 else ""
            )
            antipatterns.append({
                "name": "Bare type: ignore",
                "symptom": (
                    f"Found in {rel_path}: `{line_content}` "
                    f"with # type: ignore (no explanation)"
                ),
                "solution": "Add comment explaining why type check is suppressed, or fix the type",
                "_source": rel_path,
            })

        # Stub functions: def foo(...): \n    pass
        for m in re.finditer(r'def\s+\w+\s*\(.*?\)\s*:\s*\n\s+pass\s*$',
                             content, re.MULTILINE):
            func_match = re.search(r'def\s+(\w+)', m.group(0))
            func_name = func_match.group(1) if func_match else "unknown"
            antipatterns.append({
                "name": f"Stub function: {func_name}",
                "symptom": f"Found in {rel_path}: {func_name}() contains only 'pass'",
                "solution": "Implement the function body before marking as complete",
                "_source": rel_path,
            })

    return antipatterns
