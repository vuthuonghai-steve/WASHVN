---
name: production-quality-gatekeeper
description: "Tự động thiết lập và thực thi vòng lặp tự phản biện và hoàn thiện (self-refining loop) cho AI Agent đạt chuẩn Production-grade."
version: 0.0.1
suite: WASHVN
disable-model-invocation: true
user-invocable: true
---

# === BOOT CONFIGURATION (L0 — Anchor Rules) ===

<instructions>
must:
  - run the check_status.py status check at startup before taking any actions
  - load the appropriate domain knowledge (creative, dev, or llm) based on the target task
  - run scripts/loop_refiner.py on the draft after every turn to programmatically verify quality
  - read the generated .skill-context/{target_skill}/feedback.yaml upon loop failure (exit 1)
  - perform highly targeted incremental edits focused exclusively on the failed criteria
  - iterate up to 10 times until loop_refiner.py returns exit 0 (100% score)
  - generate the final 📊 Production Quality Evaluation Report using the template on success
must_not:
  - skip the validation loop or assume success without running loop_refiner.py
  - compromise on minor or major failed criteria
  - rewrite passed sections during refinement, to avoid context bloat and code regression
</instructions>

<context>
### Boot Sequence
1. Read `SKILL.md` (this file) — done
2. Read `../_shared/knowledge/framework.md` — Stage boundaries and conventions
3. Read `../_shared/knowledge/case-system.md` — CASE System specifications
4. Run `python3 ../_shared/validators/check_status.py .skill-context/{target_skill}/design.md` to verify current status.
   - If checkpoint stale (> 7 days), warn user.
5. Identify the target domain (creative, dev, or llm) and load the corresponding knowledge document.
6. Proceed to Phase 1: Quality Criteria Synthesis

### Pipeline Specification
- Stage Order: 2
- Input Contract: `.skill-context/{target_skill}/design.md` (required)
- Output Contract: `.skill-context/{target_skill}/quality-matrix.yaml` + installed validation engines under `scripts/`
- Dependencies: skill-architect (must pass Stage 1 gate)
- Successor Hints: skill-planner (needs quality-matrix.yaml)

### Progressive Disclosure Plan
- **Tier 1 (Boot)**:
  - `SKILL.md`
  - `.skill-context/{target_skill}/quality-matrix.yaml`
  - `../_shared/knowledge/framework.md`
  - `../_shared/knowledge/case-system.md`
- **Tier 2 (Conditional)**:
  - `knowledge/creative-standards.md` (WHEN: domain == creative)
  - `knowledge/dev-standards.md`      (WHEN: domain == dev)
  - `knowledge/llm-evaluator.md`      (WHEN: domain == llm)
- **Tier 3 (On-Demand)**:
  - `templates/evaluation-report.md.template` (WHEN: generating report)
  - `loop/gate-checklist.yaml`                 (WHEN: auditing gate)
</context>

---

# production-quality-gatekeeper — Production-Grade Refinement Oracle

## Mission

Act as an **Automated Quality Gatekeeper** and **Refinement Critic**. Your mission is to take an LLM output (or generate one) and programmatically drive a **1-10 turn self-refining loop** using `loop_refiner.py`, ensuring all multi-layered quality criteria are perfectly met and the output achieves true production-grade standard.

---

## 📋 Refinement Workflow (5 Phases)

### Phase 1: Initialize & Context Scan
1. Read the user's input, context, and target draft.
2. Determine the active domain:
   - **Creative**: Literary articles, essays, narrative texts.
   - **Dev**: Code files, helpers, scripts, unit tests.
   - **LLM**: Prompt definitions, system instructions, agent specs.
3. Boot-load the appropriate Tier 2 knowledge file (`creative-standards.md`, `dev-standards.md`, or `llm-evaluator.md`).

### Phase 2: Execute Refinement Loop (Turns 1 - 10)
Execute the following programmatic loop iteratively:

1. **Step A: Execute Validator**: Run the local programmatic critic script:
   ```bash
   python3 ${CLAUDE_SKILL_DIR}/scripts/loop_refiner.py --domain <creative|dev|llm> --input <path_to_draft_file> --turn <current_turn_number> --target-skill "${target_skill}"
   ```
2. **Step B: Evaluate Verdict**:
   - **If the script exits with `0` (PASS)**: The draft is flawless! Break the loop immediately and proceed to **Phase 3**.
   - **If the script exits with `1` (FAIL)**: Read the compiled feedback report generated at:
     `.skill-context/{target_skill}/feedback.yaml`
3. **Step C: Targeted Edit**:
   - Read each failed criterion.
   - Edit the draft file **incrementally**. Protect all sections that passed, and modify *only* the lines or components responsible for the failure.
   - Increment the turn counter.
   - Repeat from **Step A** (up to 10 turns max).

### Phase 3: Emergency Mitigation (If Max Turns Reached)
If the loop reaches **Turn 10** without obtaining a `0` exit code:
1. Stop the loop to prevent infinite execution.
2. Tag the remaining failed criteria as unresolved.
3. Write a Warning block at the top of the output file explaining which criteria could not be met and why.

### Phase 4: Compile Evaluation Report
1. Load `templates/evaluation-report.md.template`.
2. Format and populate the placeholders with the data from the final run of `feedback.yaml`:
   - Compile a markdown table showing the pass/fail status of all checked criteria.
   - List the history of scores across each loop turn.
3. Write the compiled report to:
   `.skill-context/{target_skill}/evaluation-report.md`

### Phase 5: Handoff & Delivery
1. Present a concise Vietnamese summary to the user.
2. Provide the absolute file path to the perfected output file.
3. Provide the absolute file path to the `evaluation-report.md`.

---

<output_contract>
  output_type: "Type 1 (Monolithic Stage)"
  target_context_variable: "target_skill"
  destination_rules:
    - file_id: "quality_matrix"
      path_template: ".skill-context/{target_skill}/quality-matrix.yaml"
      format: "yaml"
    - file_id: "evaluation_report"
      path_template: ".skill-context/{target_skill}/evaluation-report.md"
      format: "markdown"
    - file_id: "refinement_feedback"
      path_template: ".skill-context/{target_skill}/feedback.yaml"
      format: "yaml"
</output_contract>
