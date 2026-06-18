---
# [TỪ DESIGN §2.5 R1+R2, BA §1.2 P5+P8, HANDBOOK §10.3 §10.3.1, quality-matrix RES-07]
# ver-0.0.3 refactor:
#   - Extract _parse_zone_mapping helper using section-number pattern `^## 3\.\s+`
#   - Share between check_file_mapping and check_todo_cross_reference (R1 close-out)
#   - Wrap recursive sub-skill calls in report() with try/except IOError (R2 close-out)
#   - Add --zone-mapping-version CLI flag (Q2 RESOLVED, non-breaking)
#   - Preserve all 5 existing flags: --path, --design, --todo, --log, --strict-context
# skill_schema_version: "3.1.0"
---
import os
import sys
import re
import json
import uuid
from datetime import datetime
from typing import List, Dict, Set, Optional


# === ZONE MAPPING PARSER (R1 close-out) ===
# Section-number pattern `^## 3\.\s+` matches heading variations:
#   - "## 3. Zone Mapping"
#   - "## 3 Zone Mapping"
#   - "## 3. Zones"
#   - "## 3. ZoneMapping"
# No longer brittle to literal string match (R1 fix).
_ZONE_SECTION_PATTERN = re.compile(r"^##\s+3\.\s+", re.MULTILINE)
_NEXT_SECTION_PATTERN = re.compile(r"^##\s+\d+\.\s+", re.MULTILINE)
_BACKTICK_PATH_PATTERN = re.compile(r"`([^`]+)`")


def _parse_zone_mapping(design_path: str, version: int = 2) -> List[Dict[str, str]]:
    """
    Parse §3 Zone Mapping from design.md.

    Args:
        design_path: Absolute path to design.md
        version: 1 (legacy literal match) or 2 (section-number pattern, default)

    Returns:
        List of {"path": str, "tier": str} dicts. Empty list if §3 not found.

    Used by check_file_mapping and check_todo_cross_reference to eliminate
    duplicate parsing logic. R1 close-out: pattern is robust to heading variations.
    """
    if not os.path.exists(design_path):
        return []

    with open(design_path, "r", encoding="utf-8") as f:
        content = f.read()

    if version == 1:
        # Legacy: literal "## 3. Zone Mapping" string match (kept for backward compat)
        section_marker = "## 3. Zone Mapping"
        idx = content.find(section_marker)
        if idx == -1:
            return []
        start = idx + len(section_marker)
        # Find next "## " heading
        next_match = re.search(r"^##\s+", content[start:], re.MULTILINE)
        end = start + next_match.start() if next_match else len(content)
    else:
        # v2 (default): section-number pattern
        section_match = _ZONE_SECTION_PATTERN.search(content)
        if not section_match:
            return []
        start = section_match.end()
        next_section = _NEXT_SECTION_PATTERN.search(content, start)
        end = next_section.start() if next_section else len(content)

    section_content = content[start:end]
    files = _BACKTICK_PATH_PATTERN.findall(section_content)
    result = []
    for f in files:
        if "/" in f or "." in f or f.startswith("SKILL"):
            result.append({"path": os.path.normpath(f), "tier": "design_spec"})
    return result


def _extract_zone_files(design_path: str, version: int = 2) -> Set[str]:
    """Convenience wrapper: return just the file paths from _parse_zone_mapping."""
    return {entry["path"] for entry in _parse_zone_mapping(design_path, version=version)}


class SkillValidator:
    """
    Kỹ sư thẩm định chất lượng Agent Skill.
    Đảm bảo tính chính trực giữa thiết kế (design) và thực thi (build).
    """
    def __init__(self, skill_path: str, design_path: str | None = None, log_mode: bool = False, strict_context: bool = False, todo_path: str | None = None, zone_mapping_version: int = 2):
        self.skill_path: str = os.path.abspath(skill_path)
        self.skill_name: str = os.path.basename(self.skill_path.rstrip('/'))
        self.design_path: str | None = os.path.abspath(design_path) if design_path else None
        self.log_mode: bool = log_mode
        self.strict_context: bool = strict_context
        self.todo_path: str | None = os.path.abspath(todo_path) if todo_path else None
        # R1 refactor: zone_mapping_version (1=legacy literal, 2=section-number pattern, default=2)
        self.zone_mapping_version: int = zone_mapping_version
        self.workspace_root: str = self.find_workspace_root()
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.reports: list[str] = []

    def find_workspace_root(self) -> str:
        """
        Return the project workspace root (parent of .skill-context/{target_skill}).
        Strategy:
        1. Walk up from skill_path for .skill-context/{target_skill}, return its parent.
        2. Use design_path parent if provided (common OMC layout).
        3. Fallback to three-level-up from skill_path.
        """
        # Strategy 1: walk up from skill_path — return PARENT of the context dir
        current = self.skill_path
        for _ in range(12):
            marker = os.path.join(current, ".skill-context", self.skill_name)
            if os.path.isdir(marker):
                # marker is .skill-context/{target_skill}, its parent is the project root
                return current
            parent = os.path.dirname(current)
            if parent == current:
                break
            current = parent

        # Strategy 2: design_path ends in .skill-context/{target_skill}/design.md.
        # We need the project root (two levels up).
        if self.design_path and os.path.isabs(self.design_path):
            # design_path: /project/.skill-context/{target_skill}/design.md
            # step 1: parent = /project/.skill-context/{target_skill}
            # step 2: parent = /project/.skill-context  ← NOT what we want
            # step 3: parent = /project                ← project root = .skill-context grandparent
            sc = self.design_path
            for _ in range(5):
                parent = os.path.dirname(sc)
                if os.path.basename(parent) == '.skill-context' or parent == '/':
                    break
                sc = parent
            return os.path.dirname(parent) if os.path.basename(parent) == '.skill-context' else parent

        # Strategy 3: fallback
        return os.path.dirname(os.path.dirname(os.path.dirname(self.skill_path)))

    def log(self, message, level="INFO"):
        prefix = f"[{level}] " if level != "INFO" else ""
        formatted_message = f"{prefix}{message}"
        self.reports.append(formatted_message)
        print(formatted_message)

    def check_structure(self):
        self.log("1. Checking 4 Zones Structural Integrity...")
        # Core zones: SKILL.md + knowledge + loop are mandatory; scripts is optional
        core_zones = ["SKILL.md", "knowledge", "loop"]
        all_zones = core_zones + ["scripts"]
        passed = True
        for zone in all_zones:
            path = os.path.join(self.skill_path, zone)
            if not os.path.exists(path):
                if zone in core_zones:
                    self.errors.append(f"[E01] CRITICAL: Missing mandatory zone: {zone}")
                    passed = False
                else:
                    self.warnings.append(f"[W01] WARNING: Missing optional zone: {zone}")
        return passed

    def check_skill_md_constraints(self):
        skill_md_path = os.path.join(self.skill_path, "SKILL.md")
        if not os.path.exists(skill_md_path): return False
        
        with open(skill_md_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            content = "".join(lines)
        
        self.log(f"2. Analyzing SKILL.md (Lines: {len(lines)})")
        
        if len(lines) > 500:
            self.errors.append(f"[E03] ERROR: SKILL.md exceeds 500 lines limit ({len(lines)})")

        mandatory_keywords = ["Persona", "Workflow", "Guardrails"]
        for kw in mandatory_keywords:
            if kw not in content:
                self.errors.append(f"[E04] ERROR: SKILL.md missing mandatory section keyword: '{kw}'")
        
        return len(self.errors) == 0

    def check_pd_links(self):
        self.log("3. Progressive Disclosure (PD) Integrity Check...")
        skill_md_path = os.path.join(self.skill_path, "SKILL.md")
        if not os.path.exists(skill_md_path): return False
        
        with open(skill_md_path, 'r', encoding='utf-8') as f:
            content = f.read()

        tier2_files = []
        for root, _, files in os.walk(self.skill_path):
            rel_root = os.path.relpath(root, self.skill_path)
            if any(rel_root.startswith(z) for z in ["knowledge", "scripts", "loop"]):
                for file in files:
                    if not file.startswith('.'):
                        rel_path = os.path.normpath(os.path.join(rel_root, file))
                        tier2_files.append(rel_path)

        orphan_count = 0
        for f_path in tier2_files:
            # Pattern: [Label](path) - must use markdown link as per User's request
            regex_path = re.escape(f_path)
            pattern = rf"\[.*\]\(.*{regex_path}.*\)"
            if not re.search(pattern, content):
                self.warnings.append(f"WARNING: Orphan file detected: '{f_path}' is not linked in SKILL.md via Markdown link.")
                self.log(f"   -> Orphan (Missing MD Link): {f_path}", "WARN")
                orphan_count += 1
        
        return orphan_count == 0

    def check_file_mapping(self):
        design_file = self.design_path
        if not design_file:
            return True

        if not os.path.exists(design_file):
            self.errors.append(f"[E06] CRITICAL: Design file not found at {design_file}")
            self.log(f"   -> Design not found: {design_file}", "FAIL")
            return False

        self.log(f"4. File Mapping (Actual vs Design §3) Check...")

        # R1 refactor: use _parse_zone_mapping helper (section-number pattern)
        zone_entries = _parse_zone_mapping(design_file, version=self.zone_mapping_version)
        expected_files: set[str] = {entry["path"] for entry in zone_entries}
        # Ensure SKILL.md is expected
        expected_files.add("SKILL.md")

        actual_files: set[str] = set()
        for root, dirs, files in os.walk(self.skill_path):
            dirs[:] = [d for d in dirs if d != '__pycache__' and not d.startswith('.')]
            rel_root = os.path.relpath(root, self.skill_path)
            for file in files:
                if not file.startswith('.'):
                    rel_path = os.path.normpath(os.path.join(rel_root, file)) if rel_root != "." else file
                    actual_files.add(rel_path)

        missing = expected_files - actual_files
        ignore_extra = {"scripts/validate_skill.py", "loop/build-log.md", "loop/build-checklist.md", "templates/cleaned-prompt.xml.template"}
        extra = actual_files - expected_files - ignore_extra

        if missing:
            for f in missing:
                self.errors.append(f"[E02] ERROR: Missing file from design: {f}")
                self.log(f"   -> Missing: {f}", "FAIL")

        if extra:
            for f in extra:
                self.warnings.append(f"WARNING: Extra file not in design: {f}")
                self.log(f"   -> Extra: {f}", "WARN")

        return len(missing) == 0

    def check_placeholder_density(self):
        self.log("5. Placeholder Density Check...")
        total_placeholders = 0
        for root, _, files in os.walk(self.skill_path):
            for file in files:
                if file.endswith('.md'):
                    path = os.path.join(root, file)
                    with open(path, 'r', encoding='utf-8') as f:
                        total_placeholders += f.read().count("[MISSING_DOMAIN_DATA]")
        
        self.log(f"   -> Total Placeholders: {total_placeholders}")
        if total_placeholders >= 10:
            self.errors.append(f"[E05] FAIL: High Placeholder Density ({total_placeholders}). >10 is unacceptable.")
        elif total_placeholders >= 5:
            self.warnings.append(f"WARNING: Medium Placeholder Density ({total_placeholders}). Progressing to failure.")
        
        return total_placeholders < 10

    def check_error_handling(self):
        """Logic P0: Kiểm tra tính tuân thủ Error STOP policy"""
        # Look for build-log.md in loop/
        log_path = os.path.join(self.skill_path, "loop", "build-log.md")
        if not os.path.exists(log_path):
            return True
            
        self.log("6. Error Handling Policy Check...")
        with open(log_path, 'r', encoding='utf-8') as f:
            log_content = f.read()

        # If system error occurred but build didn't stop (no final status or more files added)
        # This is a simplified check
        if "ERROR" in log_content.upper() and "Log-Notify-Stop" in log_content:
            self.log("   -> System Error detected in log. Verifying STOP stance.", "INFO")
        return True

    def get_context_dir(self):
        """
        Return .skill-context/{target_skill}.
        workspace_root is the project root (where .skill-context/ lives),
        so join workspace_root + .skill-context + skill_name.
        """
        return os.path.join(self.workspace_root, ".skill-context", self.skill_name)

    def collect_context_critical_files(self):
        """
        Critical coverage contract:
        - design.md, todo.md
        - all files under resources/
        - all files under data/
        """
        context_dir = self.get_context_dir()
        critical: list[str] = []
        if not os.path.isdir(context_dir):
            return critical

        for fixed in ("design.md", "todo.md"):
            fixed_path = os.path.join(context_dir, fixed)
            if os.path.isfile(fixed_path):
                critical.append(fixed)

        for rel_root in ("resources", "data"):
            root_dir = os.path.join(context_dir, rel_root)
            if not os.path.isdir(root_dir):
                continue
            for root, _, files in os.walk(root_dir):
                for name in files:
                    if name.startswith("."):
                        continue
                    full = os.path.join(root, name)
                    rel = os.path.relpath(full, context_dir)
                    critical.append(rel.replace("\\", "/"))

        # Stable ordering for deterministic validation output
        return sorted(set(critical))

    def check_context_resource_coverage(self):
        """
        Verify builder actually captured context usage in .skill-context/{target_skill}/build-log.md.
        """
        self.log("7. Context Resource Coverage Check...")
        context_dir = self.get_context_dir()
        if not os.path.isdir(context_dir):
            self.warnings.append(f"WARNING: Context directory not found for coverage check: {context_dir}")
            self.log(f"   -> Missing context dir: {context_dir}", "WARN")
            return True

        build_log = os.path.join(context_dir, "build-log.md")
        if not os.path.isfile(build_log):
            code = "[E07]" if self.strict_context else "[W07]"
            msg = f"{code} {'ERROR' if self.strict_context else 'WARNING'}: Missing context build log required for coverage: {build_log}"
            (self.errors if self.strict_context else self.warnings).append(msg)
            self.log(f"   -> Missing build-log: {build_log}", "FAIL")
            return not self.strict_context

        with open(build_log, "r", encoding="utf-8") as f:
            build_log_content = f.read()

        for section in ("## Resource Inventory", "## Resource Usage Matrix"):
            if section not in build_log_content:
                code = "[E08]" if self.strict_context else "[W08]"
                msg = f"{code} {'ERROR' if self.strict_context else 'WARNING'}: build-log.md missing mandatory section '{section}'"
                (self.errors if self.strict_context else self.warnings).append(msg)
                self.log(f"   -> Missing section: {section}", "FAIL")

        critical_files = self.collect_context_critical_files()
        if not critical_files:
            self.warnings.append(
                "WARNING: No critical context files detected (design/todo/resources/data)."
            )
            self.log("   -> No critical context files detected.", "WARN")
            return len(self.errors) == 0

        uncovered = []
        for rel in critical_files:
            rel_norm = rel.replace("\\", "/")
            full_norm = os.path.join(context_dir, rel).replace("\\", "/")
            if rel_norm not in build_log_content and full_norm not in build_log_content:
                uncovered.append(rel_norm)

        if uncovered:
            for rel in uncovered:
                code = "[E09]" if self.strict_context else "[W09]"
                msg = f"{code} {'ERROR' if self.strict_context else 'WARNING'}: Critical context resource has no usage evidence in build-log.md: {rel}"
                (self.errors if self.strict_context else self.warnings).append(msg)
                self.log(f"   -> Uncovered critical resource: {rel}", "FAIL")
        else:
            self.log(
                f"   -> Coverage OK: {len(critical_files)}/{len(critical_files)} critical resources traced.",
                "INFO",
            )

        return len(uncovered) == 0 if self.strict_context else True

    def check_todo_cross_reference(self):
        if not self.todo_path:
            return True

        if not os.path.exists(self.todo_path):
            self.warnings.append(f"WARNING: todo.md not found at {self.todo_path}, skipping cross-reference")
            return True

        self.log("9. Todo ↔ Design Cross-Reference Check...")

        # R1 refactor: use _parse_zone_mapping helper (shared with check_file_mapping)
        expected_files: set[str] = set()
        if self.design_path and os.path.exists(self.design_path):
            expected_files = _extract_zone_files(self.design_path, version=self.zone_mapping_version)

        with open(self.todo_path, 'r', encoding='utf-8') as f:
            todo_content = f.read()

        task_files = set()
        task_file_patterns = [
            r"(?:→|->)\s*`?([^`\s]+)`?",
            r"file_target:\s*([^\s\n]+)",
        ]
        for pattern in task_file_patterns:
            matches = re.findall(pattern, todo_content)
            for m in matches:
                if m and ("." in m or m.startswith("/")):
                    task_files.add(os.path.normpath(m))

        missing_in_todo = expected_files - task_files
        if missing_in_todo:
            self.warnings.append(
                f"WARNING: Files in design §3 but not covered by todo tasks: {', '.join(missing_in_todo)}"
            )
            self.log(f"   -> Missing in todo: {missing_in_todo}", "WARN")

        self.log(f"   -> §3 files: {len(expected_files)}, Todo tasks: {len(task_files)}, Coverage: {len(task_files & expected_files)}/{len(expected_files)}")
        return True

    def check_fidelity_heuristics(self):
        """
        Check for potential summarization by comparing line counts between sources and targets.
        """
        self.log("8. Fidelity Heuristics Check...")
        context_dir = self.get_context_dir()
        build_log_path = os.path.join(context_dir, "build-log.md")
        if not os.path.isfile(build_log_path):
            return True

        with open(build_log_path, 'r', encoding='utf-8') as f:
            log_content = f.read()

        # Extract Resource Usage Matrix rows (support multi-file sources)
        # Format: | `resources/...` | Target | Notes | OR | Source | Target | Notes |
        # Multi-file case: part-a + part-b → knowledge/claude-code-prompt-patterns.md
        matrix_rows = re.findall(r'\|\s*`([^`]+)`\s*\|\s*Critical\s*\|\s*[^\|]+\|(?:\s*`([^`]+)`\s*\|)?', log_content)
        
        for source_rel, target_rel in matrix_rows:
            if not target_rel: continue
            
            source_path = os.path.join(context_dir, source_rel)
            target_path = os.path.join(self.skill_path, target_rel)
            
            if os.path.isfile(source_path) and os.path.isfile(target_path):
                with open(source_path, 'r', encoding='utf-8') as fs:
                    source_lines = len(fs.readlines())
                with open(target_path, 'r', encoding='utf-8') as ft:
                    target_lines = len(ft.readlines())
                
                # If target is less than 60% of source and source is significant (> 50 lines)
                if source_lines > 50 and target_lines < source_lines * 0.6:
                    self.warnings.append(f"FIDELITY WARNING: '{target_rel}' is significantly shorter than its source '{source_rel}' ({target_lines} vs {source_lines} lines). Potential summarization detected.")
                    self.log(f"   -> Potential summarization: {target_rel} ({target_lines} lines) vs {source_rel} ({source_lines} lines)", "WARN")
                else:
                    self.log(f"   -> Fidelity OK: {target_rel} maintains healthy ratio to {source_rel}.", "INFO")
        
        return True

    def check_trace_tags(self):
        """
        Validate trace tags in todo.md for anti-hallucination enforcement.
        Checks for: [TỪ DESIGN §N], [CẦN LÀM RÕ], [GỢI Ý BỔ SUNG], [TỪ AUDIT TÀI NGUYÊN]
        """
        if not self.todo_path or not os.path.exists(self.todo_path):
            return True

        self.log("10. Trace Tag Validation Check...")

        with open(self.todo_path, 'r', encoding='utf-8') as f:
            todo_content = f.read()

        # Standard trace tags that must be present
        required_tags = {
            r'\[TỪ DESIGN §\d+\]': 'Design trace',
            r'\[CẦN LÀM RÕ\]': 'Clarification needed',
            r'\[GỢI Ý BỔ SUNG\]': 'Suggested addition',
            r'\[TỪ AUDIT TÀI NGUYÊN\]': 'Resource audit trace',
        }

        # Legacy/invalid tags that should NOT appear
        legacy_tags = {
            r'\[GỢI Ý\]': 'Use [GỢI Ý BỔ SUNG] instead',
            r'\[TỪ AUDIT\]': 'Use [TỪ AUDIT TÀI NGUYÊN] instead',
            r'\[TỪ AUDIT CUSTOM\]': 'Invalid tag format',
            r'\[CẦU LÀM RÕ\]': 'Typo - use [CẦN LÀM RÕ]',
        }

        issues = []
        for pattern, name in required_tags.items():
            count = len(re.findall(pattern, todo_content, re.IGNORECASE))
            if count > 0:
                self.log(f"   -> {name}: {count} found")
            else:
                self.warnings.append(f"WARNING: No instances of '{name}' tag found in todo.md")
                issues.append(f"missing_{name}")

        for pattern, fix_suggestion in legacy_tags.items():
            count = len(re.findall(pattern, todo_content, re.IGNORECASE))
            if count > 0:
                self.errors.append(f"ERROR: Found legacy/invalid tag matching '{pattern}' - {fix_suggestion}")
                issues.append(f"legacy_tag")

        if not issues:
            self.log("   -> All trace tags VALID")
        else:
            self.log(f"   -> Trace tag issues: {issues}", "WARN")

        return len([i for i in issues if i.startswith('legacy')]) == 0

    def check_format_compliance(self):
        """
        Validate format standards compliance in built skill.
        Checks: XML tags, YAML blocks, trace tags, token budget.
        """
        self.log("11. Format Standards Compliance Check...")

        skill_md_path = os.path.join(self.skill_path, "SKILL.md")
        if not os.path.exists(skill_md_path):
            self.warnings.append("WARNING: SKILL.md not found, skipping format compliance")
            return True

        with open(skill_md_path, 'r', encoding='utf-8') as f:
            skill_content = f.read()
            skill_lines = skill_content.split('\n')

        # F1: XML tags presence
        required_xml_tags = ['<instructions>', '<context>', '<examples>', '<output_contract>']
        for tag in required_xml_tags:
            if tag in skill_content:
                self.log(f"   -> XML tag {tag}: FOUND")
            else:
                self.warnings.append(f"WARNING: Missing XML tag '{tag}' in SKILL.md")

        # F2: YAML frontmatter at line 1
        if skill_lines[0].strip() == '---':
            self.log("   -> YAML frontmatter at line 1: OK")
        else:
            self.errors.append("ERROR: YAML frontmatter must be at line 1 of SKILL.md")

        # F3: YAML keys in content
        required_yaml_keys = ['must:', 'must_not:', 'priority_order:']
        for key in required_yaml_keys:
            if key in skill_content:
                self.log(f"   -> YAML key '{key}': FOUND")
            else:
                self.warnings.append(f"WARNING: Missing YAML key '{key}' in SKILL.md")

        # F4: Trace tags (if build-log exists in context)
        context_dir = self.get_context_dir()
        build_log_path = os.path.join(context_dir, "build-log.md") if context_dir else None
        if build_log_path and os.path.exists(build_log_path):
            with open(build_log_path, 'r', encoding='utf-8') as f:
                log_content = f.read()

            valid_trace_tags = [
                r'\[TỪ DESIGN §\d+\]',
                r'\[GỢI Ý BỔ SUNG\]',
                r'\[TỪ AUDIT TÀI NGUYÊN\]',
                r'\[CẦN LÀM RÕ\]',
            ]
            for pattern in valid_trace_tags:
                count = len(re.findall(pattern, log_content, re.IGNORECASE))
                if count > 0:
                    self.log(f"   -> Trace tag {pattern}: {count} found")

        # F5: Token budget check (SKILL.md ≤ 400 tokens for L0, warn 500-700, >700 FAIL)
        self.log("   -> Running token count check (CLAUDE.md L0 budget)...")
        token_count = self._count_tokens(skill_content)
        self.log(f"   -> SKILL.md token count: {token_count}")

        if token_count > 700:
            self.errors.append(f"ERROR: SKILL.md exceeds 700 tokens L0 budget ({token_count} tokens). MUST split into policy/ file.")
        elif token_count > 500:
            self.warnings.append(f"WARNING: SKILL.md token count ({token_count}) in warning zone (500-700). Consider splitting.")
        else:
            self.log(f"   -> SKILL.md token count: {token_count} (L0 budget OK: ≤500)")

        # F6: Line count check (legacy check, secondary to token count)
        if len(skill_lines) > 500:
            self.warnings.append(f"WARNING: SKILL.md exceeds 500 lines ({len(skill_lines)} lines) - secondary to token budget")

        # Check knowledge files line count (≤ 200 lines each)
        knowledge_dir = os.path.join(self.skill_path, "knowledge")
        if os.path.exists(knowledge_dir):
            for root, _, files in os.walk(knowledge_dir):
                for file in files:
                    if file.endswith('.md'):
                        file_path = os.path.join(root, file)
                        with open(file_path, 'r', encoding='utf-8') as f:
                            lines = f.readlines()
                            if len(lines) > 200:
                                rel_path = os.path.relpath(file_path, self.skill_path)
                                self.warnings.append(f"WARNING: {rel_path} exceeds 200 lines ({len(lines)} lines)")

        self.log("   -> Format compliance check complete")
        return len([e for e in self.errors if 'format' in e.lower() or 'yaml' in e.lower() or 'xml' in e.lower() or 'token' in e.lower() or '700' in e]) == 0

    def _count_tokens(self, text: str) -> int:
        """
        Count tokens using tiktoken (cl100k_base) for accurate LLM token counting.
        Falls back to character-based estimation if tiktoken unavailable.
        """
        try:
            import tiktoken
            enc = tiktoken.get_encoding("cl100k_base")
            return len(enc.encode(text))
        except ImportError:
            # Fallback: estimate ~4 chars per token for English, ~3.5 for Vietnamese
            # This is rough but better than nothing
            char_count = len(text)
            # Rough estimation: mix of English and Vietnamese
            vietnamese_chars = sum(1 for c in text if '\u00C0' <= c <= '\u1EF3')
            english_chars = sum(1 for c in text if c.isascii())
            other_chars = char_count - vietnamese_chars - english_chars

            # Weight: Vietnamese ~3 chars/token, English ~4 chars/token, Other ~4 chars/token
            estimated_tokens = int(vietnamese_chars / 3) + int(english_chars / 4) + int(other_chars / 4)
            self.log(f"   -> (tiktoken unavailable, using estimation: ~{estimated_tokens} tokens)")
            return estimated_tokens

    def report(self):
        print("\n" + "="*50)
        print("   AGENT SKILL VALIDATION REPORT")
        print(f"   Target: {self.skill_name}")
        print(f"   Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*50)
        
        # Determine if this is a master orchestrator with physical sub-skills
        sub_skills = []
        for entry in os.scandir(self.skill_path):
            if entry.is_dir() and not entry.name.startswith('.') and entry.name != '__pycache__':
                if os.path.exists(os.path.join(entry.path, "SKILL.md")):
                    sub_skills.append(entry)

        # Run checks on this main skill
        self.check_structure()
        self.check_skill_md_constraints()
        self.check_pd_links()
        self.check_file_mapping()
        self.check_placeholder_density()
        self.check_error_handling() 
        self.check_context_resource_coverage()
        self.check_fidelity_heuristics()
        self.check_todo_cross_reference()
        self.check_trace_tags()
        self.check_format_compliance()

        # If sub-skills exist, recursively validate them
        if sub_skills:
            self.log(f"Detected {len(sub_skills)} physical sub-skills inside orchestrator root. Recursively validating:")
            for sub in sub_skills:
                self.log(f"\n---> Sub-skill validation start: {sub.name}", "INFO")
                sub_design = None
                sub_todo = None
                if self.design_path:
                    sub_design_dir = os.path.dirname(self.design_path)
                    sub_design_candidate = os.path.join(sub_design_dir, sub.name, "design.md")
                    if os.path.exists(sub_design_candidate):
                        sub_design = sub_design_candidate
                if self.todo_path:
                    sub_todo_dir = os.path.dirname(self.todo_path)
                    sub_todo_candidate = os.path.join(sub_todo_dir, sub.name, "todo.md")
                    if os.path.exists(sub_todo_candidate):
                        sub_todo = sub_todo_candidate

                # R2 refactor: wrap recursive sub-skill call in try/except IOError
                # to prevent crash when sub-skill is missing SKILL.md or has malformed structure
                try:
                    sub_validator = SkillValidator(
                        sub.path,
                        design_path=sub_design,
                        log_mode=self.log_mode,
                        strict_context=self.strict_context,
                        todo_path=sub_todo,
                        zone_mapping_version=self.zone_mapping_version,
                    )
                    sub_validator.report_nested()
                    self.errors.extend([f"[{sub.name}] {err}" for err in sub_validator.errors])
                    self.warnings.extend([f"[{sub.name}] {warn}" for warn in sub_validator.warnings])
                    self.reports.extend(sub_validator.reports)
                    self.log(f"---> Sub-skill validation end: {sub.name}\n", "INFO")
                except (IOError, OSError) as sub_io_err:
                    # R2: graceful skip with warning, continue with next sub-skill
                    warn_msg = f"Sub-skill '{sub.name}' skipped: {sub_io_err}"
                    self.warnings.append(warn_msg)
                    self.log(f"   -> {warn_msg}", "WARN")
                    continue
                except Exception as sub_err:
                    # Catch-all for unexpected errors (defensive, don't crash the parent)
                    err_msg = f"Sub-skill '{sub.name}' failed validation: {sub_err}"
                    self.errors.append(err_msg)
                    self.log(f"   -> {err_msg}", "FAIL")
                    continue

        print("="*50)

    def report_nested(self):
        """Perform validation but do not print redundant headers or exit the system."""
        self.check_structure()
        self.check_skill_md_constraints()
        self.check_pd_links()
        self.check_file_mapping()
        self.check_placeholder_density()
        self.check_error_handling() 
        self.check_context_resource_coverage()
        self.check_fidelity_heuristics()
        self.check_todo_cross_reference()
        self.check_trace_tags()
        self.check_format_compliance()
        final_status = "PASS" if not self.errors else "FAIL"
        if self.warnings and final_status == "PASS":
            final_status = "PASS (With Warnings)"
            
        print(f"FINAL STATUS: {final_status}")
        
        if self.log_mode:
            self.write_log(final_status)
            
        if self.errors:
            sys.exit(1)
        sys.exit(0)

    def write_log(self, status):
        """Append validation result to build-log.md in .skill-context/{target_skill}/"""
        target_log_path = os.path.join(
            self.workspace_root, ".skill-context", self.skill_name, "build-log.md"
        )

        if not os.path.exists(target_log_path):
            self.log(f"Warning: Build log not found at {target_log_path}", "WARN")
            return

        with open(target_log_path, 'a', encoding='utf-8') as f:
            f.write(f"\n\n## Validation Result ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')})\n")
            f.write(f"- **Final Status**: {status}\n")
            f.write(f"- **Errors**: {len(self.errors)}\n")
            f.write(f"- **Warnings**: {len(self.warnings)}\n")
            if self.errors:
                f.write("### Issues Found:\n")
                for err in self.errors:
                    f.write(f"- [FAILED] {err}\n")
            self.log(f"Results appended to {target_log_path}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="Path to the skill directory")
    parser.add_argument("--design", help="Path to design.md")
    parser.add_argument("--log", action="store_true", help="Append results to build-log.md")
    parser.add_argument(
        "--strict-context",
        action="store_true",
        help="Fail validation if context resource coverage in .skill-context/{target_skill}/build-log.md is incomplete",
    )
    parser.add_argument(
        "--todo",
        default=None,
        help="Path to todo.md for cross-reference validation between todo tasks and design §3 files",
    )
    # Q2 RESOLVED: New optional flag (non-breaking) for explicit zone mapping pattern selection
    parser.add_argument(
        "--zone-mapping-version",
        type=int,
        choices=[1, 2],
        default=2,
        help="Zone mapping parser version: 1=legacy literal '## 3. Zone Mapping' match, 2=section-number pattern '^## 3\\.\\s+' (default, R1 refactor)",
    )
    args = parser.parse_args()

    validator = SkillValidator(
        args.path,
        design_path=args.design,
        log_mode=args.log,
        strict_context=args.strict_context,
        todo_path=args.todo,
        zone_mapping_version=args.zone_mapping_version,
    )
    validator.report()
