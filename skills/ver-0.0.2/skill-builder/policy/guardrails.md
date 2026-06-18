# === G1-G8 GUARDRAILS ENFORCEMENT — skill-builder ver-0.0.3 ===
# [TỪ DESIGN §2.3, BA §2.1 FR-17..FR-19, HANDBOOK §6.4]
# Detailed enforcement contract for each guardrail. Enforced by validator + agent runtime.

guardrails_version: "0.0.3"
severity_levels:
  MUST: "Block build, log error, halt"
  SHOULD: "Log warning, allow build to continue"
  INFO: "Always show, no enforcement"

# === G1: Engineer-Critic Stance ===
G1_engineer_critic:
  severity: "MUST"
  short: "Audit design before build. Quyền sửa phi logic."
  detailed:
    description: "Builder PHẢI audit design.md trước Phase 3. Có quyền flag phi logic, missing sections, hoặc contradictions."
    applies_to: "Phase 1 PREPARE + Phase 2 CLARIFY"
    actions:
      - "Read design.md §1-§12 fully"
      - "Cross-check design.md §9 Open Questions with todo.md [CẦN LÀM RÕ] markers"
      - "Flag missing required sections (12 sections per quality-matrix L0-01)"
      - "Verify zone count = 9 per design.md §3"
      - "If confidence < 70% → HALT + emit [CẦN LÀM RÕ: <missing>]"
    enforcement_tool: "skill-builder self-check (Phase 1 audit) + user confirmation gate"
  reference: "design.md §2.3 G1, ba-report.md FR-02, SPEC.md §7 engineer_critic_stance"

# === G2: Phase Discipline ===
G2_phase_discipline:
  severity: "MUST"
  short: "Chia BUILD theo Phase todo.md. Mark-as-done từng phase."
  detailed:
    description: "Builder PHẢI execute PH1→PH2→PH3→PH4→PH5 in order. No skip, no reorder without explicit user approval."
    applies_to: "All 5 phases"
    actions:
      - "Mark phase [x] only after Gate 1/2/3 confirmation"
      - "Track phase progress in Workflow Progress Tracker Checklist"
      - "If any phase skipped → G2 violation = quality-gate FAIL"
    enforcement_tool: "validate_skill.py check_phase_discipline (planned) + user gate at IP-2/4/6"
  reference: "design.md §2.3 G2, ba-report.md FR-18, SPEC.md §5 AH3, todo.md §7.2 DAG Order Enforcement"

# === G3: Log-Notify-Stop ===
G3_log_notify_stop:
  severity: "MUST"
  short: "Lỗi hệ thống → Log → Notify → DỪNG NGAY."
  detailed:
    description: "On any system error, Builder PHẢI log to build-log.md, notify user, STOP all tasks immediately."
    applies_to: "All phases (esp. PH3 BUILD)"
    actions:
      - "Append error to .skill-context/{target_skill}/build-log.md with format [SYSTEM_ERROR] + ISO8601 timestamp"
      - "Use AskUserQuestion or equivalent to notify developer"
      - "STOP all tasks; do NOT continue past the error point"
      - "If error is recoverable: surface to user with proposed fix → wait for approval"
    enforcement_tool: "validate_skill.py check_error_handling + manual review"
  reference: "design.md §2.3 G3, ba-report.md §5 S-06, SPEC.md §5 AH6"

# === G4: Source Grounding ===
G4_source_grounding:
  severity: "MUST"
  short: "Nội dung 100% từ design/todo/resources. Không ảo giác."
  detailed:
    description: "Builder PHẢI derive 100% output from design.md, todo.md, resources/*. KHÔNG hallucinate facts or files."
    applies_to: "Phase 3 BUILD (all file creation)"
    actions:
      - "Every file MUST cite at least one [TỪ DESIGN §N], [TỪ BA §N], [TỪ HANDBOOK §N], or [GỢI Ý BỔ SUNG] trace tag"
      - "No file creation outside design.md §3 Zone Mapping"
      - "No invented file names, paths, or filenames"
    enforcement_tool: "validate_skill.py check_file_mapping + check_trace_tags"
  reference: "design.md §2.3 G4, ba-report.md FR-04, FR-17, SPEC.md §5 AH1, AH2"

# === G5: Build-Log Mandatory ===
G5_build_log_mandatory:
  severity: "MUST"
  short: "Ghi quyết định, phản biện, file tạo vào build-log.md."
  detailed:
    description: "Builder PHẢI append mỗi decision, file creation, vào build-log.md với format 'Task -> Output -> Source files'."
    applies_to: "Phase 3 BUILD (every file write)"
    actions:
      - "After every file write → append entry to build-log.md"
      - "Format: 'Task #{N} -> Output: {file} -> Source: {design.md §M / resources/X}'"
      - "Include [TỪ TODO #N] trace tag"
      - "Mark critical_tasks_done = true only when all required files logged"
    enforcement_tool: "validate_skill.py check_context_resource_coverage + check_fidelity_heuristics"
  reference: "design.md §2.3 G5, ba-report.md FR-10, SPEC.md §5 AH5"

# === G6: Context Coverage ===
G6_context_coverage:
  severity: "MUST"
  short: "Không bỏ sót file critical; có evidence trong Resource Usage Matrix."
  detailed:
    description: "Builder PHẢI ensure every critical file in design.md, todo.md, resources/*, data/* has usage evidence in build-log.md."
    applies_to: "Phase 5 DELIVER"
    actions:
      - "All Critical resources MUST have row in Resource Usage Matrix"
      - "Uncovered critical resources → E09 error in strict-context mode"
      - "Run validate_skill.py --strict-context for full coverage"
    enforcement_tool: "validate_skill.py check_context_resource_coverage with --strict-context flag"
  reference: "design.md §2.3 G6, ba-report.md NFR-05, SPEC.md §9 DoD, todo.md §4 DoD"

# === G7: Zone Contract Block ===
G7_zone_contract_block:
  severity: "MUST"
  short: "CHỉ tạo file trong design.md §3. Không tự ý thêm."
  detailed:
    description: "Builder PHẢI ONLY create files in design.md §3 Zone Mapping. Hallucinated file paths BLOCK build."
    applies_to: "Phase 3 BUILD (all file writes)"
    actions:
      - "Parse design.md §3 Zone Mapping using section-number pattern `^## 3\\.\\s+`"
      - "Every file write MUST match an entry in §3"
      - "No README.md, LICENSE, Makefile unless listed in §3"
      - "G7 violation → E02 ERROR, halt build, log to build-log.md"
    enforcement_tool: "validate_skill.py check_file_mapping + _parse_zone_mapping helper (R1 refactor)"
  reference: "design.md §2.3 G7, ba-report.md FR-03, FR-17, SPEC.md §5 AH1, todo.md §7.1 G7 Zone Contract Block"

# === G8: Format Compliance ===
G8_format_compliance:
  severity: "MUST"
  short: "Output phải tuân thủ format-standards.md"
  detailed:
    description: "Builder PHẢI tuân thủ 100% format-standards.md: YAML for constraints, XML tags for boundaries, trace tags for all content, token budget enforced."
    applies_to: "All file creation (Phase 3 BUILD)"
    actions:
      - "use_yaml_for: constraints, policies, checklists, output_contracts"
      - "use_xml_tags_for: semantic_boundaries, separating_context_from_instruction"
      - "use_trace_tags_for: all content in knowledge/ and policy/"
      - "follow_token_budget: SKILL.md ≤400 target / 700 hard cap"
      - "yaml_frontmatter_line1: SKILL.md frontmatter MUST start at line 1"
    enforcement_tool: "validate_skill.py check_format_compliance (11 check methods)"
    reject_if:
      - "missing_trace_tags"
      - "missing_xml_boundaries"
      - "missing_yaml_must_must_not"
      - "token_budget_exceeded (>700 tokens for SKILL.md)"
      - "yaml_frontmatter_not_line1"
  reference: "design.md §2.3 G8, ba-report.md FR-04, FR-08, FR-09, NFR-03, NFR-06, SPEC.md §3, §4, §5, §9"
