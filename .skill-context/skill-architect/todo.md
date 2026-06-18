---
artifact_type: "todo"
skill_name: "skill-architect"
version: "0.0.2"
generated_by: "skill-planner (Stage 2)"
generated_at: "2026-06-18"
stage: "planner"
status: "in_progress"
lifecycle: "planning"
---

# skill-architect — Implementation Plan (todo.md)

> **Stage 2 (Planner) output.** Decomposes `.skill-context/skill-architect/design.md` into DAG-ordered executable tasks for Stage 3 (skill-builder-agent). Every task carries a trace tag back to `design.md §N`, evaluation report, business analysis, or open-question resolution.

---

## 1. Pre-requisites

| # | Artifact / Knowledge | Tier | Mục đích | Trace | Status |
|---|----------------------|------|----------|-------|--------|
| 1 | `design.md` (Stage 1 output) | Architectural | Source of truth for zone mapping, sections, risks, open questions | [TỪ DESIGN §1-§12] | READY (12 sections, 13 zone files) |
| 2 | `quality-matrix.yaml` (Stage 1.5) | Quality gate | SCS, severity tags, scoring rubric | [TỪ QUALITY §1-§3] | READY (95.1% PASS) |
| 3 | `business-analysis.md` (Stage -1) | Domain | FR-01..FR-18, NFR, scope boundary | [TỪ BA §3-§6] | READY (44.5% WARNING — FR-11, FR-17/18 in scope) |
| 4 | `domain-handbook.md` (Stage 0.5) | Domain | Skill-design ontology, meta-prompt patterns | [TỪ HANDBOOK] | READY |
| 5 | `evaluation-report.md` (Turn 2) | Quality | 5 risks (R1-R5), 7 questions (Q1-Q7), gap analysis | [TỪ EVAL §1-§3] | READY (Turn 2 enhanced) |
| 6 | `exploration.md` + `criteria.md` (Stage 0) | Context | Background research, acceptance criteria | [TỪ EXPLORATION] | READY |
| 7 | Source: `skills/ver-0.0.2/skill-architect/` (5 knowledge, 3 policy, 3 scripts, 2 loop, 1 data, 1 template) | Runtime source | Sync source for runtime target | [TỪ CLAUDE.md §3] | READY (partially — 2 knowledge files missing at runtime) |
| 8 | Runtime target: `.claude/skills/skill-architect/` | Runtime target | Destination for sync command | [TỪ CLAUDE.md §3] | PARTIAL (3 of 5 knowledge files present) |

---

## 2. Phase Breakdown (DAG-ordered)

> **DAG order**: Phase 0 (Resource Prep) → Phase 1 (Knowledge) → Phase 2 (Data) → Phase 3 (Loop) → Phase 4 (Scripts) → Phase 5 (Templates) → Phase 6 (Core SKILL.md) → Phase 7 (Policy Updates) → Phase 8 (Verification)
>
> **DAG depth**: 9 phases. Critical path: T0.1 → T1.1 → T3.1 → T4.2 → T6.1 → T8.1 → T8.2 (7 tasks, ~16h est.).

### Phase 0: Resource Preparation

| # | Task ID | Description | Priority | Est. | Deps | Trace | Output | Status |
|---|---------|-------------|----------|------|------|-------|--------|--------|
| 1 | T0.1 | Sync `knowledge/knowledge-boot-sequence.md` from `skills/ver-0.0.2/` → `.claude/skills/skill-architect/knowledge/` | Critical | 0.5h | — | [TỪ DESIGN §11, evaluation-report R3] | runtime knowledge file | pending |
| 2 | T0.2 | Sync `knowledge/script-boundary-policy.md` from `skills/ver-0.0.2/` → `.claude/skills/skill-architect/knowledge/` | Critical | 0.5h | — | [TỪ DESIGN §11, evaluation-report R3] | runtime knowledge file | pending |

### Phase 1: Knowledge Zone (5 files)

| # | Task ID | Description | Priority | Est. | Deps | Trace | Output | Status |
|---|---------|-------------|----------|------|------|-------|--------|--------|
| 3 | T1.1 | Author `knowledge/architect.md` (3 Pillars framework) | Critical | 4h | T0.1, T0.2 | [TỪ DESIGN §3 knowledge/, BA §4.1] | `knowledge/architect.md` | pending |
| 4 | T1.2 | Author `knowledge/knowledge-boot-sequence.md` (boot v2 with scan) | Critical | 3h | T0.1 | [TỪ DESIGN §3, BA FR-11] | `knowledge/knowledge-boot-sequence.md` | pending |
| 5 | T1.3 | Author `knowledge/script-boundary-policy.md` (deterministic boundary policy) | Critical | 2h | T0.2 | [TỪ DESIGN §3, BA FR-17/18] | `knowledge/script-boundary-policy.md` | pending |
| 6 | T1.4 | Author `knowledge/visualization-guidelines.md` (Mermaid standards) | High | 2h | — | [TỪ DESIGN §3, quality-matrix S-05/S-06] | `knowledge/visualization-guidelines.md` | pending |
| 7 | T1.5 | Author `knowledge/design-exemplars.md` (section content spec with exemplars) | High | 3h | T1.1 | [TỪ DESIGN §3, BA §4.2] | `knowledge/design-exemplars.md` | pending |

### Phase 2: Data Zone

| # | Task ID | Description | Priority | Est. | Deps | Trace | Output | Status |
|---|---------|-------------|----------|------|------|-------|--------|--------|
| 8 | T2.1 | Create `data/knowledge-sources.yaml` (KS-01..KS-05 boot config registry) | High | 2h | — | [TỪ DESIGN §3, BA §6.1] | `data/knowledge-sources.yaml` | pending |

### Phase 3: Loop Zone (machine-readable + human-readable)

| # | Task ID | Description | Priority | Est. | Deps | Trace | Output | Status |
|---|---------|-------------|----------|------|------|-------|--------|--------|
| 9 | T3.1 | Author `loop/design-checklist.yaml` (machine-readable 35 checks) | Critical | 3h | T1.1 | [TỪ DESIGN §3, quality-matrix §1 rubric] | `loop/design-checklist.yaml` | pending |
| 10 | T3.2 | Author `loop/design-checklist.md` (human-readable mirror) | High | 1.5h | T3.1 | [TỪ DESIGN §3, quality-matrix Z-04] | `loop/design-checklist.md` | pending |

### Phase 4: Scripts Zone (3 files — deterministic IO only)

| # | Task ID | Description | Priority | Est. | Deps | Trace | Output | Status |
|---|---------|-------------|----------|------|------|-------|--------|--------|
| 11 | T4.1 | Rewrite `scripts/init_context.py` — strip `FALLBACK_TEMPLATES` dict, keep only deterministic IO (mkdir + zip extract) | Critical | 3h | T1.3 | [TỪ DESIGN §3, evaluation-report R2/Q3, BA FR-17/18] | `scripts/init_context.py` | pending |
| 12 | T4.2 | Create `scripts/validate_design.py` — parse `design.md`, check frontmatter + required sections + zone mapping + trace tag coverage | Critical | 4h | T3.1 | [TỪ DESIGN §3, quality-matrix §1] | `scripts/validate_design.py` | pending |
| 13 | T4.3 | Create `scripts/export-pipeline.py` — extract Mermaid blocks from `design.md` → standalone `.md` files | Medium | 2h | — | [TỪ DESIGN §3, BA §4.3] | `scripts/export-pipeline.py` | pending |

### Phase 5: Templates Zone

| # | Task ID | Description | Priority | Est. | Deps | Trace | Output | Status |
|---|---------|-------------|----------|------|------|-------|--------|--------|
| 14 | T5.1 | Create `templates/design.md.template` — skeleton only (frontmatter + 12 empty section headers, NO pre-populated zone mapping) | High | 1.5h | — | [TỪ DESIGN §3, evaluation-report R5] | `templates/design.md.template` | pending |

### Phase 6: Core Zone (SKILL.md refactor)

| # | Task ID | Description | Priority | Est. | Deps | Trace | Output | Status |
|---|---------|-------------|----------|------|------|-------|--------|--------|
| 15 | T6.1 | Refactor `SKILL.md` — implement Knowledge Boot v2, Tier 1/2/3 routing referencing new knowledge files, §11 output contract, G3 confidence HARD STOP for <70% | Critical | 4h | T1.1-T1.5, T2.1 | [TỪ DESIGN §1-§12, Q1 resolution, BA FR-11] | `SKILL.md` | pending |

### Phase 7: Policy Updates (cross-cutting)

| # | Task ID | Description | Priority | Est. | Deps | Trace | Output | Status |
|---|---------|-------------|----------|------|------|-------|--------|--------|
| 16 | T7.1 | Update `policy/output-spec.md` — add §11 Knowledge Requirements section (Q4 resolution) | High | 1.5h | T6.1 | [TỪ DESIGN §11, Q4 resolution] | `policy/output-spec.md` | pending |
| 17 | T7.2 | Update `policy/workflow.md` — document Knowledge Boot v2 in Phase 0 | Medium | 1h | T6.1 | [GỢI Ý BỔ SUNG: from Turn 2 eval] | `policy/workflow.md` | pending |
| 18 | T7.3 | Update `policy/guardrails.md` — G3: <70% HARD STOP, 70-85% ask + K=8 | Critical | 1h | T6.1 | [TỪ BA FR-11, Q1 resolution] | `policy/guardrails.md` | pending |

### Phase 8: Verification (sandbox + sync)

| # | Task ID | Description | Priority | Est. | Deps | Trace | Output | Status |
|---|---------|-------------|----------|------|------|-------|--------|--------|
| 19 | T8.1 | Run `scripts/validate_design.py` against `.skill-context/skill-architect/design.md` → expect Exit 0 | Critical | 0.5h | T4.2, T6.1 | [TỪ DESIGN §3, quality-matrix §2 acceptance] | validation result | pending |
| 20 | T8.2 | Sync runtime: `cp -r skills/ver-0.0.2/skill-architect/* .claude/skills/skill-architect/` | Critical | 0.5h | T0.1, T0.2, T6.1 | [TỪ CLAUDE.md §3] | runtime sync | pending |

**Total tasks: 20 | Critical path: 7 tasks (T0.1 → T1.1 → T3.1 → T4.2 → T6.1 → T8.1 → T8.2) ≈ 16h**

---

## 3. Knowledge & Resources Needed

### 3.1 Source Artifacts (read-only inputs)
- `skills/ver-0.0.2/skill-architect/` — 5 knowledge, 3 policy, 3 scripts, 2 loop, 1 data, 1 template
- `.skill-context/skill-architect/design.md` — 12 sections, 13 zone files
- `.skill-context/skill-architect/quality-matrix.yaml` — 95.1% PASS
- `.skill-context/skill-architect/business-analysis.md` — FR-01..FR-18
- `.skill-context/skill-architect/domain-handbook.md`
- `.skill-context/skill-architect/evaluation-report.md` — Turn 2 enhanced

### 3.2 Runtime Targets (write outputs)
- `.claude/skills/skill-architect/knowledge/` — currently 3 files, needs 2 more
- `.claude/skills/skill-architect/scripts/` — 3 files (init_context.py rewrite + 2 new)
- `.claude/skills/skill-architect/templates/`, `data/`, `loop/`, `policy/`
- `.claude/skills/skill-architect/SKILL.md` — refactor to v2

### 3.3 Validators / Tools
- `scripts/validate_design.py` (T4.2 — produced by this plan)
- Python 3.14.3 stdlib only (no new deps)
- Mermaid CLI optional (for T4.3 export verification)

### 3.4 Sync Command
```bash
cp -r skills/ver-0.0.2/skill-architect/* .claude/skills/skill-architect/
```

---

## 4. Definition of Done

- [ ] All 13 zone files in `design.md §3` created (5 knowledge + 3 scripts + 1 data + 2 loop + 1 template + 1 core)
- [ ] `scripts/init_context.py` has zero `FALLBACK_TEMPLATES` dict (R2 closed)
- [ ] Runtime `.claude/skills/skill-architect/knowledge/` has 5 knowledge files (R3 closed)
- [ ] `data/knowledge-sources.yaml` exists with KS-01..KS-05 entries
- [ ] `policy/output-spec.md` has §11 Knowledge Requirements section (Q4 resolved)
- [ ] `policy/guardrails.md` G3 updated: <70% HARD STOP, 70-85% ask + K=8 (Q1 resolved)
- [ ] `scripts/validate_design.py` returns Exit 0 against `design.md`
- [ ] Zero placeholders in any code file (per FR-17/18)
- [ ] 100% trace tag coverage on assertions (`[TỪ DESIGN §N]` / `[TỪ AUDIT TÀI NGUYÊN]` / `[GỢI Ý BỔ SUNG]` / `[CẦN LÀM RÕ]`)
- [ ] `SKILL.md` ≤ 700 tokens (L0 budget per standards.md)
- [ ] Runtime synced from `skills/ver-0.0.2/` (T8.2 exit 0)
- [ ] All 35 checks in `loop/design-checklist.yaml` pass against `design.md`
- [ ] No new dependencies introduced (Python stdlib only)

---

## 5. Notes — Resolved Open Questions

| # | Question | Resolution | Trace |
|---|----------|------------|-------|
| Q1 | Confidence < 70% → STOP (FR-11) vs ask (G3) | **<70% = HARD STOP + block Phase + ask user for domain knowledge**; 70-85% = ask + K=8 samples; ≥85% = proceed | [TỪ BA FR-11, Q1 resolution] |
| Q2 | SCS fast-track for skill-architect | **N/A — monolithic per BA scope_boundary** (single SKILL.md, 7 zones) | [TỪ BA §scope_boundary] |
| Q3 | `init_context.py` strip extent | **Full strip of template-writing + FALLBACK_TEMPLATES dict; keep IO deterministic only (mkdir + zip extract)** | [TỪ HANDBOOK GAP-07, R2] |
| Q4 | Knowledge Requirements §11 vs §2 subsection | **§11 separate section** (per design.md Turn 2 decision — greater visibility for Planner/Builder) | [TỪ DESIGN §11, Q4 resolution] |
| Q5 | Flowchart 3-path coverage | **RESOLVED in design.md §5.2 (D3 flowchart: green-path / yellow-path / red-path)** | [TỪ evaluation-report §1 Turn 2] |
| Q6 | Python vs shell portability for `init_context.py` | **Keep Python 3.14 for `zipfile` logic; document IO split in `script-boundary-policy.md` if needed later** | [GỢI Ý BỔ SUNG] |
| Q7 | 12 missing Gherkin scenarios | **Builder generates 2 critical scenarios at Stage 4; remaining 10 deferred to a future `gherkin-ext` skill** | [GỢI Ý BỔ SUNG] |

### Open `[CẦN LÀM RÕ]` items remaining: 0
All 7 evaluation-report questions resolved at this stage.

---

## 6. Output Contract (DRC-compliant)

```yaml
output_contract:
  output_type: "Type 1 (Monolithic Stage)"
  target_context_variable: "target_skill"
  target_variable: "target_skill"
  destination: ".skill-context/{target_skill}/todo.md"
  format: "markdown"
  schema: "raw/ver-3/_shared/schemas/todo.schema.yaml"
  handoff_to: "skill-builder (Stage 3)"
  next_stage_hint: "skill-builder-agent"
  confidence: 0.92
  status: in_progress
  deliverables:
    - file_id: "execution_plan"
      path_template: ".skill-context/{target_skill}/todo.md"
      format: "markdown"
      required_sections:
        - "§1 Pre-requisites"
        - "§2 Phase Breakdown"
        - "§3 Knowledge & Resources"
        - "§4 Definition of Done"
        - "§5 Notes"
        - "§6 Output Contract"
      required_drc_block: true
      required_trace_tags:
        - "[TỪ DESIGN §N]"
        - "[GỢI Ý BỔ SUNG]"
        - "[TỪ AUDIT TÀI NGUYÊN]"
        - "[CẦN LÀM RÕ]"
  handoff_artifacts:
    - ".skill-context/skill-architect/design.md"
    - ".skill-context/skill-architect/quality-matrix.yaml"
    - ".skill-context/skill-architect/todo.md"
```

---

## 7. Builder Feedback Integration

> Constraints and audit hooks for Stage 3 (skill-builder-agent).

- **G1 — Engineer-Critic Stance**: Builder MUST audit `design.md` for phi logic and zone coherence BEFORE executing T6.1 (`SKILL.md` refactor). If confidence < 70%, halt and notify user.
- **G3 — Confidence Gate**: Per Q1 resolution, if mid-task confidence drops < 70%, HARD STOP — do not proceed to next task. Resume only after user provides domain knowledge.
- **G4 — Source Grounding**: Every T1.*, T4.*, T6.1, T7.* file MUST cite at least one `[TỪ DESIGN §N]`, `[TỪ EVALUATION §N]`, `[TỪ BA §N]`, or `[GỢI Ý BỔ SUNG]` trace tag in its header comment.
- **G10 — Zone Contract Block**: All T1-T5 outputs MUST be enumerated in `design.md §3` `Files cần tạo` column. No file creation outside the zone contract.
- **Determinism Constraint**: All T4.* scripts must be pure-IO (no LLM calls, no network). Business/synthesis logic lives in `knowledge/*.md` (Tier 2 cognitive load).
- **Zero Placeholder**: No `TODO`, `pass`, `mock()`, `...` in any T4.* script. R2 violation = quality-gate FAIL.
- **Runtime Sync**: T8.2 is the gate. No skill is "built" until runtime `.claude/skills/skill-architect/` reflects source.
- **Token Budget**: `SKILL.md` ≤ 700 tokens (L0 anchor). Detailed content in `knowledge/` and `policy/`.

---

## 8. Plan Metadata

| Field | Value |
|-------|-------|
| **Planner agent** | skill-planner (Stage 2) |
| **Generated at** | 2026-06-18 |
| **Skill name** | skill-architect |
| **Skill version** | 0.0.2 |
| **SCS (Skill Complexity Score)** | 2.4 (monolithic — no micro-skill decomposition needed) |
| **DAG depth** | 9 phases |
| **Total tasks** | 20 |
| **Critical path length** | 7 tasks (T0.1 → T1.1 → T3.1 → T4.2 → T6.1 → T8.1 → T8.2) ≈ 16h |
| **Confidence (self-assessed)** | 0.92 |
| **Open clarifications** | 0 (all 7 questions resolved) |
| **Suggested next stage** | `skill-builder-agent` (Stage 3) — awaits explicit user confirmation |
