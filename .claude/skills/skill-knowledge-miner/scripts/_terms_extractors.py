"""
_terms_extractors.py — Priority-based glossary extractors for mine_for_terms.py

Split from mine_for_terms.py during barrel refactor.
Contains extraction priorities A through E:
  A: knowledge/*.md for Glossary/Thuật ngữ sections
  B: .claude/agents/*.md and SKILL.md for tags/keywords
  C: Temps/spec/** for definition blocks
  D: _shared/knowledge/*.md for domain terms
  E: exploration.md §1 pain points, §3 assessments
"""

import os
import re
from skill_miner_common import read_file_safely


# ---------------------------------------------------------------------------
# Priority 1: Parse knowledge/*.md for Glossary / Thuật ngữ sections
# ---------------------------------------------------------------------------
RE_GLOSSARY_HEADING = re.compile(r'^##\s+(?:Glossary|Thuật ngữ)\s*$', re.IGNORECASE)
RE_TABLE_ROW = re.compile(r'^\|\s*(\*\*[^*]+\*\*|\S[^|]+)\s*\|\s*(.+?)\s*\|')
RE_BULLET_TERM = re.compile(r'^[\s]*[-*]\s+\*{0,2}([^*\n]+?)\*{0,2}\s*[—–:-]+\s*(.+)')
RE_PIPE_TERM = re.compile(r'^\|\s*\*\*([^*]+)\*\*\s*\|\s*(.+)$', re.IGNORECASE)


def extract_from_knowledge(workspace, logger):
    """Priority A: knowledge/*.md files -> Glossary/Thuật ngữ sections"""
    terms = []
    seen_files = set()

    for pattern_base in [os.path.join(workspace, 'skills', 'ver-3'),
                         os.path.join(workspace, '.claude', 'skills')]:
        if not os.path.isdir(pattern_base):
            continue
        for root, dirs, files in os.walk(pattern_base):
            if 'knowledge' not in root.split(os.sep):
                continue
            for fname in files:
                if not fname.endswith('.md'):
                    continue
                fpath = os.path.join(root, fname)
                if fpath in seen_files:
                    continue
                seen_files.add(fpath)
                extracted = _parse_glossary_file(fpath, "knowledge", logger)
                terms.extend(extracted)
                if extracted and logger.verbose:
                    logger.debug(f"  [P1] {fpath}: {len(extracted)} terms")

    return terms


def _parse_glossary_file(fpath, source_label, logger=None):
    """Parse a single markdown file for glossary terms"""
    terms = []
    content = read_file_safely(fpath, logger)
    if content is None:
        return terms

    in_glossary_section = False
    for line in content.split('\n'):
        if RE_GLOSSARY_HEADING.match(line.strip()):
            in_glossary_section = True
            continue
        if in_glossary_section:
            if line.startswith('#') and not line.startswith('##'):
                in_glossary_section = False
                continue
            # Try table row: | **term** | definition |
            m = RE_PIPE_TERM.match(line.strip())
            if m:
                term = m.group(1).strip()
                defn = m.group(2).strip()
                if term and defn:
                    terms.append((term, defn))
                    continue
            # Try bullet: - **term**: definition
            m = RE_BULLET_TERM.match(line.strip())
            if m:
                term = m.group(1).strip().strip('*').strip()
                defn = m.group(2).strip()
                if term and defn:
                    terms.append((term, defn))

    # If no glossary section found, try scanning whole file for term patterns
    if not terms:
        for line in content.split('\n'):
            m = RE_BULLET_TERM.match(line.strip())
            if m:
                term = m.group(1).strip().strip('*').strip()
                defn = m.group(2).strip()
                if term and defn:
                    terms.append((term, defn))

    return terms


# ---------------------------------------------------------------------------
# Priority 2: Parse .claude/agents/*.md and SKILL.md for tags/keywords
# ---------------------------------------------------------------------------
def extract_from_claude_agents(workspace, logger):
    """Priority B: .claude/agents/*.md -> Terminology sections + tags"""
    terms = []
    agent_dir = os.path.join(workspace, '.claude', 'agents')
    if os.path.isdir(agent_dir):
        for fname in os.listdir(agent_dir):
            if not fname.endswith('.md'):
                continue
            fpath = os.path.join(agent_dir, fname)
            terms.extend(_parse_terminology_section(fpath, logger))

    # Also scan .claude/skills/*/SKILL.md
    skills_dir = os.path.join(workspace, '.claude', 'skills')
    if os.path.isdir(skills_dir):
        for skill_name in os.listdir(skills_dir):
            skill_md = os.path.join(skills_dir, skill_name, 'SKILL.md')
            if os.path.isfile(skill_md):
                terms.extend(_parse_frontmatter_tags(skill_md, logger))
                terms.extend(_parse_terminology_section(skill_md, logger))

    return terms


def _parse_terminology_section(fpath, logger=None):
    """Parse ## Terminology or ## Thuật ngữ sections"""
    terms = []
    content = read_file_safely(fpath, logger)
    if content is None:
        return terms

    # Look for key: value patterns in frontmatter
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            for line in parts[1].split('\n'):
                kv = re.match(r'^\s*(\w+)\s*:\s*["\']?(.+?)["\']?\s*$', line)
                if kv and kv.group(2).strip():
                    terms.append((kv.group(1), kv.group(2).strip()))

    # Look for **Term**: Definition patterns
    for m in re.finditer(r'\*\*([^*]+)\*\*\s*[:\\-]\s*(.+)', content):
        term = m.group(1).strip()
        defn = m.group(2).strip()
        if term and defn and len(term) > 2:
            terms.append((term, defn))

    return terms


def _parse_frontmatter_tags(fpath, logger=None):
    """Extract tags array from SKILL.md frontmatter"""
    terms = []
    content = read_file_safely(fpath, logger)
    if content is None:
        return terms

    if not content.startswith('---'):
        return terms
    parts = content.split('---', 2)
    if len(parts) < 3:
        return terms

    # Extract tags: ["tag1", "tag2"]
    for line in parts[1].split('\n'):
        tm = re.match(r'^\s*tags\s*:\s*\[(.+)\]', line)
        if tm:
            for tag in tm.group(1).split(','):
                tag = tag.strip().strip('"').strip("'")
                if tag:
                    terms.append((tag, f"Tag from {os.path.basename(fpath)}"))
        # Extract description
        dm = re.match(r'^\s*description\s*:\s*["\']?(.+?)[\"\']?\s*$', line)
        if dm:
            desc = dm.group(1).strip()
            if desc:
                skill_name = os.path.basename(os.path.dirname(fpath))
                terms.append((f"{skill_name}_description", desc))

    return terms


# ---------------------------------------------------------------------------
# Priority 3: Parse Temps/spec/** for definition blocks
# ---------------------------------------------------------------------------
def extract_from_temps_spec(workspace, logger):
    """Priority C: Temps/spec/** -> definition blocks"""
    terms = []
    temps_dir = os.path.join(workspace, 'Temps', 'spec')
    if not os.path.isdir(temps_dir):
        return terms

    for root, dirs, files in os.walk(temps_dir):
        for fname in files:
            if not fname.endswith('.md'):
                continue
            fpath = os.path.join(root, fname)
            content = read_file_safely(fpath, logger)
            if content is None:
                continue

            found = 0
            for m in re.finditer(r'^\s*[-*]\s+\*\*([^*]+)\*\*\s*[—–:\\-]\s*(.+)',
                                 content, re.MULTILINE):
                term = m.group(1).strip()
                defn = m.group(2).strip()
                if term and defn and len(term) > 2:
                    terms.append((term, defn))
                    found += 1

            if found and logger.verbose:
                logger.debug(f"  [P3] {fpath}: {found} terms")

    return terms


# ---------------------------------------------------------------------------
# Priority 4: Parse _shared/knowledge/*.md for domain terms
# ---------------------------------------------------------------------------
def extract_from_shared(workspace, logger):
    """Priority D: _shared/knowledge/*.md"""
    terms = []
    shared_knowledge = os.path.join(workspace, 'skills', 'ver-3', '_shared', 'knowledge')
    if not os.path.isdir(shared_knowledge):
        return terms

    for fname in os.listdir(shared_knowledge):
        if not fname.endswith('.md'):
            continue
        fpath = os.path.join(shared_knowledge, fname)
        extracted = _parse_glossary_file(fpath, "shared", logger)
        terms.extend(extracted)

    return terms


# ---------------------------------------------------------------------------
# Priority 5: Fallback — parse exploration.md §1 pain points, §3 assessments
# ---------------------------------------------------------------------------
def extract_from_exploration(exploration_path, logger):
    """Priority E: exploration.md sections"""
    terms = []
    if not exploration_path or not os.path.isfile(exploration_path):
        return terms

    content = read_file_safely(exploration_path, logger)
    if content is None:
        return terms

    # Parse frontmatter for skill_name, scs_score
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            for line in parts[1].split('\n'):
                kv = re.match(r'^\s*(\w+)\s*:\s*(.+?)\s*$', line)
                if kv:
                    val = kv.group(2).strip().strip('"').strip("'")
                    if val and kv.group(1) in ('skill_name', 'scs_score', 'exploration_summary'):
                        terms.append((kv.group(1), val))

    # Parse §1 pain points for noun phrases
    in_section1 = False
    for line in content.split('\n'):
        if re.match(r'^##\s+1\.', line):
            in_section1 = True
            continue
        if in_section1 and line.startswith('## ') and not line.startswith('###'):
            in_section1 = False
            continue
        if in_section1:
            for m in re.finditer(r'\*\*([^*]+)\*\*', line):
                term = m.group(1).strip()
                if term and len(term) > 3:
                    context = line.strip()[:80]
                    terms.append((term, context))

    return terms
