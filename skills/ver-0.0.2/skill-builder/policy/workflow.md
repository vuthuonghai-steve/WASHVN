# === 5-PHASE WORKFLOW — skill-builder ver-0.0.3 ===
# [TỪ DESIGN §2.2, BA §2.1 FR-01..FR-10, HANDBOOK §1.3]
# Detailed execution contract for each phase. Read at Phase boundaries.

workflow:
  version: "0.0.3"
  phases: 5
  execution_mode: "strict_order_no_skip"

phase_1_prepare:
  name: "PREPARE & Evaluate"
  duration_estimate: "10% of total build time"
  gate: "→ PH2 (continue to clarify)"
  inputs:
    - ".skill-context/{target_skill}/design.md (REQUIRED)"
    - ".skill-context/{target_skill}/todo.md (REQUIRED)"
    - ".skill-context/{target_skill}/resources/* (WHEN listed in design §3)"
    - ".skill-context/{target_skill}/data/* (WHEN listed in design §3)"
    - "policy/skill-builder.yaml (Tier 1, L1 guardrails)"
    - "data/builder-knowledge-sources.yaml (Tier 1, knowledge scan)"
  actions:
    - "Load policy/skill-builder.yaml — extract G1-G8 guardrails"
    - "Scan data/builder-knowledge-sources.yaml — determine Tier 1/2/3 routing"
    - "Read design.md §3 Zone Mapping — build file checklist (Critical vs Supportive)"
    - "Read todo.md §2 Phase Breakdown — confirm DAG order"
    - "Audit design.md for phi logic (G1 Engineer-Critic stance)"
    - "Classify inputs: Critical (design.md, todo.md, resources/*, data/*) vs Supportive (loop/*, domain-handbook.md)"
    - "Emit inventory summary to user; AWAIT explicit confirmation (Gate 1)"
  exit_criteria:
    - "All required upstream artifacts loaded"
    - "Zone count matches design.md §3 file count"
    - "User confirmed scope"
  on_failure: "HALT + emit [CẦN LÀM RÕ: <missing artifact>]"

phase_2_clarify:
  name: "CLARIFY (Closing the Loop)"
  duration_estimate: "5% of total build time"
  gate: "⏸️ Gate: User clarification (max 5 questions)"
  inputs:
    - "todo.md from Phase 1"
    - "design.md §9 Open Questions (cross-reference)"
  actions:
    - "Scan todo.md for [CẦN LÀM RÕ] markers"
    - "Cross-check with design.md §9 Open Questions"
    - "Collect max 5 clarification items, each with: context + question + expected answer"
    - "Emit consolidated clarification list to user"
    - "Record user answers into design.md §Clarifications (append-only)"
    - "Re-audit todo.md — if [CẦN LÀM RÕ] remains → HALT"
  exit_criteria:
    - "Zero unresolved [CẦN LÀM RÕ] in todo.md"
    - "All 5 questions answered (or user explicitly marked 'proceed with assumption')"
  on_failure: "HALT + emit clarification list"

phase_3_build:
  name: "BUILD (Phase-Driven)"
  duration_estimate: "70% of total build time"
  gate: "→ PH4 (validator + checklist)"
  inputs:
    - "All outputs from PH1, PH2"
    - "knowledge/architect.md (Tier 2, builder-specific guardrails)"
    - "knowledge/build-guidelines.md (Tier 2, format selection)"
    - "knowledge/anthropic-skill-standards.md (Tier 2, SKILL.md contract)"
    - "knowledge/skill-builder-script-boundary-policy.md (Tier 2, scripts deterministic boundary)"
    - "knowledge/builder-token-budget.md (Tier 2, L0/L1/L2/L3 budgets)"
    - "examples/build-exemplars.md (Tier 2, concrete build references)"
  actions:
    - "Execute todo.md §2 Phase Breakdown task by task in DAG order"
    - "For each task:"
    - "  1. Read cited source (design.md §N, resources/X, etc.)"
    - "  2. Compute target file content (markdown/YAML/python per format rules)"
    - "  3. Verify zone contract (G7): file in design.md §3 Zone Mapping"
    - "  4. Write file to {runtime_dest}/{target_skill}/{path}"
    - "  5. Append to build-log.md: 'Task #N -> Output: {file} -> Source: {design.md §M / resources/X}' with [TỪ TODO #N] trace tag"
    - "  6. Apply double-pass refinement to detect information loss"
    - "Micro-skill handling (if SCS >= 3.0):"
    - "  - For each micro-skill, also build {runtime_dest}/{target_skill}-{micro-name}/"
    - "  - Generate scripts/orchestrate.py in main meta-skill using SSP"
  exit_criteria:
    - "All files in design.md §3 Zone Mapping created"
    - "All Critical resources have Resource Usage Matrix row"
    - "SKILL.md token count <= 400 (Q3 strict) or 700 (hard cap)"
    - "Zero placeholders in production code (TODO, FIXME, mock, pass # implement later)"
    - "All trace tags present in first 200 tokens of every content file"
  on_failure: "Log-Notify-Stop (G3) on system error"

phase_4_verify:
  name: "VERIFY (The Gatekeeper)"
  duration_estimate: "10% of total build time"
  gate: "→ PH5 (PASS) or rollback (FAIL)"
  inputs:
    - "All files from PH3"
    - "scripts/validate_skill.py (refactored ver-0.0.3 with section-number parser)"
    - "loop/build-checklist.yaml v2.0.0 (with tier_knowledge_parity section)"
  actions:
    - "Run scripts/validate_skill.py {runtime_dest}/{target_skill}/"
    - "Run with --strict-context flag for full coverage check"
    - "Run loop/build-checklist.yaml v2.0.0 (machine-readable, all MUST checks)"
    - "Apply placeholder density check: <5 PASS / 5-9 WARN / >=10 FAIL (C2 unified)"
    - "Apply token budget recheck: SKILL.md <= 400 target / 700 hard cap"
    - "Apply trace tag audit: every content file has trace tag in first 200 tokens"
    - "Apply zone coverage audit: every design.md §3 file exists in runtime_dest"
  exit_criteria:
    - "Validator exit code = 0 (all 11 checks PASS)"
    - "Build checklist v2.0.0: all MUST checks PASS"
    - "Zero CRITICAL findings from skill-security-reviewer (if security_gate_required)"
  on_failure: "HALT + emit failed check list; do NOT advance to PH5"

phase_5_deliver:
  name: "DELIVER"
  duration_estimate: "5% of total build time"
  gate: "User final-approve → lifecycle: designed → built"
  inputs:
    - "All verified outputs from PH4"
    - "templates/build-log.md.template (3 mandatory sections scaffold)"
  actions:
    - "Finalize build-log.md at .skill-context/{target_skill}/build-log.md"
    - "Mandatory sections: ## Resource Inventory + ## Resource Usage Matrix + ## Validation Result"
    - "Update .skill-context/{target_skill}/_state.yaml: lifecycle: build-completed"
    - "Sync runtime: cp -r skills/ver-0.0.X/{target_skill}/* .claude/skills/{target_skill}/ (if applicable)"
    - "Update skills-registry.json entry: version, src_path, output_contract"
    - "Update workspce_tree.md Stage row with new file count"
    - "Emit final summary to parent session: target_skill, runtime_dest, files_created, build_status, security_status, top 3 risks"
  exit_criteria:
    - "build-log.md has all 3 mandatory sections"
    - "_state.yaml lifecycle: build-completed"
    - "Runtime synced (18+ files in .claude/skills/{target_skill}/)"
    - "Registry + workspce_tree updated"
    - "User explicitly approved final build"
  on_failure: "HALT + notify user with 5-line blocker summary"

# === INTERACTION POINTS (user-confirmation gates) ===
interaction_points:
  - id: "IP-1"
    location: "Boot — Gate-0"
    trigger: "design.md or todo.md missing at .skill-context/{target_skill}/"
    action: "STOP + emit [CẦN LÀM RÕ] + route to Stage 1/2"
  - id: "IP-2"
    location: "PH1 → PH2"
    trigger: "User must confirm scope + zone count"
    action: "Present summary + zone table → wait for explicit Approved"
  - id: "IP-3"
    location: "PH2"
    trigger: "[CẦN LÀM RÕ] found in todo.md"
    action: "Batch max 5 questions → wait for user answers"
  - id: "IP-4"
    location: "PH3 → PH4"
    trigger: "User must confirm build complete before validation"
    action: "Present file list + build-log excerpt → wait for Approved"
  - id: "IP-5"
    location: "PH4"
    trigger: "Validator Exit 1 OR checklist FAIL"
    action: "List failed checks → surgical fix → re-run"
  - id: "IP-6"
    location: "PH5"
    trigger: "User final-approve before lifecycle transition"
    action: "Present build-log.md full → wait for Approved → transition designed → built"
