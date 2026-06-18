---
artifact_type: "todo"
skill_name: "skill-builder"
version: "0.0.3-target"
generated_by: "skill-planner (Stage 2)"
generated_at: "2026-06-18"
stage: "planner"
status: "in_progress"
lifecycle: "planning"
scs: 3.1                            # from quality-matrix 0.97 + 9 zones + 18 files
design_md_path: ".skill-context/skill-builder/design.md"
quality_matrix_path: ".skill-context/skill-builder/quality-matrix.yaml"
handoff_to: "skill-builder-agent (Stage 3 — builds ver-0.0.3)"
---

# skill-builder — Implementation Plan (todo.md) for ver-0.0.3

> **Stage 2 (Planner) output.** Decompose `.skill-context/skill-builder/design.md` (12 sections, 9 zones, 18 files, SCS=3.1) into DAG-ordered executable tasks for Stage 3 (`skill-builder-agent`). Mọi task mang trace tag về `design.md §N` hoặc upstream artifact.
>
> **Quality gate upstream**: 98.2% PASS (161/161 MUST), 7/7 contradictions resolved, 7/10 KG closed, 9 zones, 0 placeholders, trace_tag_coverage=1.0.
>
> **DAG depth**: 10 phases. **Critical path**: T0.1 → T1.1 → T2.1 → T5.1 → T8.1 → T9.1 → T9.2 (7 tasks, ~14h est.).

---

## 1. Pre-requisites

| # | Artifact / Knowledge | Tier | Mục đích | Trace | Status |
|---|----------------------|------|----------|-------|--------|
| 1 | `design.md` (Stage 1 output, 12 sections, 18 files, 9 zones) | Architectural | Source-of-truth: zone mapping, sections, risks, open questions, progressive disclosure | [TỪ DESIGN §1-§12] | READY |
| 2 | `quality-matrix.yaml` (Stage 1.5, 98.2% PASS, 161/161 MUST) | Quality gate | SCS=3.1, severity tags, 9 scoring categories, MUST-filter for blocking checks | [TỪ QUALITY §1-§2] | READY |
| 3 | `ba-report.md` (Stage -1, 19 FR + 10 NFR + 10 KG + 7C + 4 RI) | Domain | Functional/non-functional requirements, MoSCoW, 7 contradictions | [TỪ BA §2-§6, §8.2-§8.3] | READY |
| 4 | `domain-handbook.md` (Stage 0.5, 10 sections, 70+ citations) | Domain | Glossary, FR/NFR distilled, existing code patterns, KG-1..KG-10 with actions | [TỪ HANDBOOK §1-§10] | READY |
| 5 | Source runtime: `skills/ver-0.0.2/skill-builder/` (10 files) | Runtime source | Sync source cho runtime target `.claude/skills/skill-builder/` | [TỪ CLAUDE.md §3] | READY (verified by Glob) |
| 6 | Runtime target: `.claude/skills/skill-builder/` (10 files, byte-identical to ver-0.0.2) | Runtime target | Destination cho `cp -r` sync sau khi build xong | [TỪ CLAUDE.md §3] | READY |
| 7 | Sibling reference: `skills/ver-0.0.2/skill-architect/` (knowledge/script-boundary-policy.md, knowledge/knowledge-boot-sequence.md) | Sibling pattern | Template/pattern reuse cho KG-1, KG-2 | [TỪ HANDBOOK §5.4, DESIGN §11] | READY |
| 8 | `skills-registry.json` (line 168 `src_path`) | Routing | Cần update `raw/ver-3/skill-builder` → `skills/ver-0.0.2/skill-builder` (R4 mitigation) | [TỪ BA §8.3 RI-1, DESIGN §8 R4] | READY (will mutate in T9.3) |
| 9 | `workspce_tree.md` (Stage 3 row, line 34) | Routing | Cần sync path với registry (R4 + RI-2) | [TỪ BA §8.3 RI-2, DESIGN §8 R4] | READY (will mutate in T9.3) |
| 10 | `validate_skill.py` source code (725 lines, 11 check methods) | Runtime validator | Refactor target (R1: extract `_parse_zone_mapping` helper; R2: try/except isolation) | [TỪ DESIGN §2.5, HANDBOOK §5.3] | READY |

**Tổng pre-requisites**: 10/10 READY — không có resource gap, không cần Phase 0 Resource Preparation riêng cho upstream. Phase 0 dưới đây cover carry-over R1, R3, R4.

---

## 2. Phase Breakdown (DAG-ordered)

> **DAG rationale**: Knowledge → Policy (L1 extraction from SKILL.md) → Data (knowledge-sources registry) → Loop (checklist v2.0.0 depends on guardrails) → Scripts (validator refactor depends on policy) → Examples (concrete builds reference knowledge) → Templates (scaffold for delivery) → Core SKILL.md (refactor AFTER all zones ready — L0 anchor only, refs policy) → Verification (sandbox + sync).
>
> **Critical path** (longest dependency chain): T0.1 → T1.1 → T2.1 → T5.1 → T8.1 → T9.1 → T9.2 = 7 tasks ≈ 14h.

### Phase 0: Carry-over Risk Mitigation (R1, R2, R3, R4, C1, C2)

| # | Task ID | Description | Priority | Est. | Deps | Trace | Output | Status |
|---|---------|-------------|----------|------|------|-------|--------|--------|
| 1 | T0.1 | **R1+R2** Refactor `validate_skill.py`: extract `_parse_zone_mapping(design_path)` helper dùng section-number pattern `^## 3\.\s+` (khớp `## 3. Zone Mapping`, `## 3 Zone Mapping`, `## 3. Zones`); share với `check_todo_cross_reference` (lines 349-361); wrap mỗi recursive sub-skill call trong `report()` (lines 619-648) bằng try/except IOError → log warning + continue | Critical | 3h | — | [TỪ DESIGN §2.5, BA §1.2 P5+P8, HANDBOOK §10.3.1, R-01/R-02 in quality-matrix] | `scripts/validate_skill.py` (refactored) | pending |
| 2 | T0.2 | **R3** Extract G1-G8 guardrails + must/must_not + placeholder threshold + token budget từ SKILL.md body → `policy/skill-builder.yaml` (L1 working policy, per KG-5); giữ SKILL.md ≤ 400 tokens L0 anchor only | Critical | 2h | T0.1 | [TỪ DESIGN §2.3 + §3 policy zone + §8 R3, BA §1.2 P2+P6, HANDBOOK §7.4, KG-5] | `policy/skill-builder.yaml` (skeleton — full content in T2.1) | pending |
| 3 | T0.3 | **R4** Update `skills-registry.json` line 168: `src_path: "raw/ver-3/skill-builder"` → `"skills/ver-0.0.2/skill-builder"` (canonical per CLAUDE.md); sync `workspce_tree.md` Stage 3 row line 34 | Critical | 0.5h | — | [TỪ DESIGN §8 R4, BA §8.3 RI-1+RI-2, CLAUDE.md §3] | `skills-registry.json` + `workspce_tree.md` (mutated) | pending |
| 4 | T0.4 | **C1+C2** Bump SKILL.md frontmatter `version: 0.0.1` → `0.0.3`; unify placeholder threshold to `<5 PASS / 5-9 WARNING / >= 10 FAIL` ở SKILL.md line 30, build-checklist.yaml C1, SPEC.md §4 | Critical | 1h | — | [TỪ DESIGN §8 R5+R6, §9 Q5+Q8, BA §8.2 C1+C2] | `SKILL.md` (version bump; threshold edit in T8.1) | pending |

**Phase 0 totals**: 4 tasks, 6.5h, 4 Critical. Unblocks all downstream phases.

### Phase 1: Knowledge Zone (5 create + 1 update + 1 optional = 7 files)

| # | Task ID | Description | Priority | Est. | Deps | Trace | Output | Status |
|---|---------|-------------|----------|------|------|-------|--------|--------|
| 5 | T1.1 | **KG-1** Author `knowledge/builder-knowledge-boot-sequence.md` — Boot v2: scan `data/builder-knowledge-sources.yaml` → Tier 1 (always: SKILL.md + policy/ + data/ + loop/) → Tier 2 (per phase, load_when conditions) → Tier 3 (on-demand: Mermaid + fidelity + migration) | Critical | 3h | T0.1 | [TỪ DESIGN §3 knowledge/, §7 Tier 1-3, BA §6 KG-1, FR-01] | `knowledge/builder-knowledge-boot-sequence.md` | pending |
| 6 | T1.2 | **KG-2** Author `knowledge/skill-builder-script-boundary-policy.md` — `scripts/` zone của TARGET skill chỉ IO deterministic (read files, write logs, parse YAML/JSON/MD, count placeholders, run CLI subcommands); MUST NOT generate prompt templates, make zone/file decisions, embed business logic, call LLM API | Critical | 2h | T0.1 | [TỪ DESIGN §2.5 + §3, BA §6 KG-2, FR-17, FR-18] | `knowledge/skill-builder-script-boundary-policy.md` | pending |
| 7 | T1.3 | **KG-8** Author `knowledge/builder-token-budget.md` — concrete numbers per zone: L0 SKILL.md ≤400 target / ≤700 hard cap; L1 policy/ ≤1200; L2 knowledge/ ≤2500/file; L3 examples/ ≤1500/file; split action khi vượt | Critical | 1.5h | T0.1 | [TỚI DESIGN §3, BA §6 KG-8, NFR-03] | `knowledge/builder-token-budget.md` | pending |
| 8 | T1.4 | Refactor `knowledge/architect.md` — update 10 Builder-specific guardrails (G1-G10) thành phiên bản 0.0.3: add reference đến `policy/skill-builder.yaml` cho G1-G8 (L1 split); bổ sung guard cho `_parse_zone_mapping` section-number pattern (R1 close-out) | High | 2h | T0.2 | [TỪ DESIGN §3 knowledge/architect.md, HANDBOOK §6.4, BA §1.1 S1] | `knowledge/architect.md` (refactored) | pending |
| 9 | T1.5 | Refactor `knowledge/build-guidelines.md` — update 4-Layer Knowledge Separation section để reference `policy/skill-builder.yaml` (L1) + `data/builder-knowledge-sources.yaml` (Tier 1 boot); add Format Selection table cho YAML/Markdown/XML choices | High | 1.5h | T0.2 | [TỪ DESIGN §3, BA §1.1 S6, HANDBOOK §6.1] | `knowledge/build-guidelines.md` (refactored) | pending |
| 10 | T1.6 | Refactor `knowledge/anthropic-skill-standards.md` — add §10 về Cognitive Agentic Skill Paradigm (L0/L1/L2/L3) reference implementation trong skill-builder 0.0.3 (dogfooding); update §1 frontmatter example với `disable-model-invocation: true` rationale | High | 1.5h | — | [TỪ DESIGN §3, BA §1.2 P9, HANDBOOK §7.4] | `knowledge/anthropic-skill-standards.md` (refactored) | pending |
| 11 | T1.7 | **KG-3** [OPTIONAL] Author `knowledge/build-visualization-guidelines.md` — Mermaid syntax cho build-log.md sequence diagram, folder structure mindmap, workflow flowchart (defer P2 acceptable — `file_required: false` per design §3) | Medium | 2h | T1.1 | [TỪ DESIGN §3 (optional), BA §6 KG-3, HANDBOOK §6.6] | `knowledge/build-visualization-guidelines.md` | pending |

**Phase 1 totals**: 7 tasks, 13.5h, 3 Critical + 3 High + 1 Medium. Foundation cho policy/ + scripts/ + loop/.

### Phase 2: Policy Zone (1 file — L1 extraction from SKILL.md)

| # | Task ID | Description | Priority | Est. | Deps | Trace | Output | Status |
|---|---------|-------------|----------|------|------|-------|--------|--------|
| 12 | T2.1 | **KG-5** Author full `policy/skill-builder.yaml` (extension từ T0.2 skeleton) — content: `guardrails:` block (G1-G8 với rationale + severity MUST/MUST_NOT), `must:` + `must_not:` priority_order, `placeholder_threshold: {pass: "<5", warning: "5-9", fail: ">=10"}` (C2 unified), `token_budget:` per zone (L0/L1/L2/L3), `zone_contract:` spec (G7 strict, files_only_in_design_section_3), `output_contract:` DRC template, `progressive_disclosure:` tier routing | Critical | 4h | T0.1, T0.2, T1.3 | [TỪ DESIGN §2.3 + §3 policy zone + §7 Tier 1, BA §6 KG-5, R-03, RES-02] | `policy/skill-builder.yaml` (complete) | pending |

**Phase 2 totals**: 1 task, 4h, Critical. L1 working policy — consumed by SKILL.md (T8.1) and scripts (T5.1).

### Phase 3: Data Zone (1 file)

| # | Task ID | Description | Priority | Est. | Deps | Trace | Output | Status |
|---|---------|-------------|----------|------|------|-------|--------|--------|
| 13 | T3.1 | **KG-6** Author `data/builder-knowledge-sources.yaml` — registry 5-7 entries KS-01..KS-07: id, path, tier (1/2/3), priority (P0/P1/P2), load_condition (always / per_phase / on_demand), description; cover all files in `knowledge/`, `policy/`, `loop/`, `templates/`, `data/` zones | High | 2h | T1.1, T2.1 | [TỪ DESIGN §3 data zone + §7 Tier 1, BA §6 KG-6, HANDBOOK §10.3 #4] | `data/builder-knowledge-sources.yaml` | pending |

**Phase 3 totals**: 1 task, 2h, High. Boot config consumed by T1.1 boot sequence and T8.1 SKILL.md routing.

### Phase 4: Loop Zone (3 files — machine-readable + human-readable + template refactor)

| # | Task ID | Description | Priority | Est. | Deps | Trace | Output | Status |
|---|---------|-------------|----------|------|------|-------|--------|--------|
| 14 | T4.1 | **UPDATE** `loop/build-checklist.yaml` v2.0.0 — bump `version: 1.0.0` → `2.0.0`; add `tier_knowledge_parity:` section (Q5 resolution — checks KG-1..KG-10 coverage); unify placeholder threshold to `<5 / 5-9 / >=10` (C2); add `zone_contract_strictness: true` check (G7); add `token_budget_enforcement:` block (NFR-03) | Critical | 3h | T2.1, T3.1 | [TỪ DESIGN §3 loop zone, §9 Q5, BA §8.2 C2, RES-02] | `loop/build-checklist.yaml` (v2.0.0) | pending |
| 15 | T4.2 | Refactor `loop/build-checklist.md` — human-readable mirror của T4.1 YAML; add §11 "Tier Knowledge Parity" + §12 "Token Budget Enforcement" + §13 "Zone Contract Strictness" | High | 1.5h | T4.1 | [TỪ DESIGN §3, BA §1.1 S5] | `loop/build-checklist.md` (refactored) | pending |
| 16 | T4.3 | **UPDATE** `loop/build-log.md.template` v2 — refactor với `execution_trace:` array (Task → Output → Source files per G5), `quality_metrics:` block (NFR-03, NFR-04, NFR-05), `feedback:` array (R12 idempotency — add ISO8601 `execution_id` UUID + timestamp normalization note) | Critical | 2h | T4.1 | [TỪ DESIGN §3 loop zone, BA FR-05, R-12, S5] | `loop/build-log.md.template` (v2) | pending |

**Phase 4 totals**: 3 tasks, 6.5h, 2 Critical + 1 High. Quality gate infrastructure.

### Phase 5: Scripts Zone (1 file — R1/R2 refactor + extension)

| # | Task ID | Description | Priority | Est. | Deps | Trace | Output | Status |
|---|---------|-------------|----------|------|------|-------|--------|--------|
| 17 | T5.1 | **R1+R2** Author/refactor `scripts/validate_skill.py` — final pass sau T0.1: integrate `_parse_zone_mapping` helper vào cả `check_file_mapping` (lines 150-165) + `check_todo_cross_reference` (lines 349-361); ensure try/except IOError wrap around recursive sub-skill calls in `report()` (lines 619-648); add `--zone-mapping-version` CLI flag (Q2 resolution — backward-compat preserved + new flag for explicit pattern selection); preserve all 4 existing flags (`--path`, `--design`, `--todo`, `--log`, `--strict-context`) | Critical | 3h | T0.1, T4.1 | [TỪ DESIGN §2.5 + §3 scripts zone, BA §1.2 P5+P8, RES-07, §9 Q2] | `scripts/validate_skill.py` (refactored + tested) | pending |

**Phase 5 totals**: 1 task, 3h, Critical. Deterministic IO only — no cognitive logic per KG-2.

### Phase 6: Examples Zone (1 required + 1 optional = 2 files)

| # | Task ID | Description | Priority | Est. | Deps | Trace | Output | Status |
|---|---------|-------------|----------|------|------|-------|--------|--------|
| 18 | T6.1 | **KG-4** Author `examples/build-exemplars.md` — ≥2 concrete builds: (a) **leaf skill** example (5 files: SKILL.md + knowledge/concept.md + scripts/process.py + loop/checklist.yaml + data/sources.yaml); (b) **meta-skill** example (3 sub-skills + `scripts/orchestrate.py` với SSP protocol); mỗi example có zone mapping table + build-log excerpt | Critical | 3h | T1.1, T5.1 | [TỪ DESIGN §3 examples zone, BA §6 KG-4, FR-12, FR-15] | `examples/build-exemplars.md` | pending |
| 19 | T6.2 | **KG-9** [OPTIONAL] Author `examples/fidelity-checks.md` — 3 case studies fidelity 1:1: (a) 50→50 (PASS), (b) 50→20 (WARN), (c) 50→5 (FAIL); mỗi case có source line count + target line count + ratio + verdict (`file_required: false` per design §3) | Medium | 2h | T6.1 | [TỪ DESIGN §3 (optional), BA §6 KG-9, FR-14, NFR-04] | `examples/fidelity-checks.md` | pending |

**Phase 6 totals**: 2 tasks, 5h, 1 Critical + 1 Medium. Tier 2 concrete evidence cho abstract mapping.

### Phase 7: Templates Zone (1 file)

| # | Task ID | Description | Priority | Est. | Deps | Trace | Output | Status |
|---|---------|-------------|----------|------|------|-------|--------|--------|
| 20 | T7.1 | **KG-7** Author `templates/build-log.md.template` — full target_skill build scaffold với 3 mandatory sections per FR-05: (1) `## Resource Inventory` (liệt kê design.md, todo.md, resources/*, data/*), (2) `## Resource Usage Matrix` (matrix critical-resource → evidence line), (3) `## Validation Result` (validator exit code + checklist pass/fail + threshold counts) | High | 2h | T4.3 | [TỪ DESIGN §3 templates zone, BA §6 KG-7, FR-05, S5] | `templates/build-log.md.template` | pending |

**Phase 7 totals**: 1 task, 2h, High. Delivery scaffold consumed by PH5 of future builds.

### Phase 8: Core Zone (SKILL.md refactor — L0 anchor only)

| # | Task ID | Description | Priority | Est. | Deps | Trace | Output | Status |
|---|---------|-------------|----------|------|------|-------|--------|--------|
| 21 | T8.1 | **C1+C2+R3** Refactor `SKILL.md` ver-0.0.3 — frontmatter: `name: skill-builder`, `description` (third-person, ≤1024 chars), `version: 0.0.3`, `suite: WASHVN`, `tags`, `when_to_use`, `disable-model-invocation: true` (Q1 resolved — keep consistent với sibling); body: persona (Senior Implementation Engineer) + 5-Phase workflow summary (PH1-PH5 one-liner each) + L0 anchor routing map to `policy/skill-builder.yaml` (G1-G8) + `data/builder-knowledge-sources.yaml` (Tier 1) + `loop/build-checklist.yaml` v2.0.0; L0 strict ≤400 tokens; line 30 placeholder threshold → `>= 10` (C2 unified); include Workflow Progress Tracker Checklist (FR-11) cho 5 phases | Critical | 4h | T0.2, T0.4, T1.1, T2.1, T3.1, T4.1 | [TỪ DESIGN §3 Core zone + §7 Tier 1 + §9 Q1+Q3+Q8, §8 R3+R5+R6, BA §1.2 P1+P6+P7+P9, FR-07, FR-11, NFR-03, RES-01, RES-05] | `SKILL.md` (v0.0.3 refactored) | pending |
| 22 | T8.2 | **MIGRATION** Author `docs/MIGRATION-0.0.2-to-0.0.3.md` — breaking changes guide: (a) zone additions (5 → 9 zones), (b) policy/ extraction (G1-G8 moved from SKILL.md body to policy/skill-builder.yaml), (c) threshold unification (placeholder >=10 everywhere), (d) version sync (SKILL.md 0.0.1 → 0.0.3, SPEC.md 3.0.0 → 3.1.0), (e) validator regex refactor (literal → section-number pattern), (f) routing update (registry src_path), (g) knowledge parity (3/10 → 7/10) | High | 1.5h | T0.1, T0.3, T2.1, T8.1 | [TỪ DESIGN §3 references zone, §10.1 versioning, BA §6 KG-10, R-10, RES-01..RES-08] | `docs/MIGRATION-0.0.2-to-0.0.3.md` | pending |

**Phase 8 totals**: 2 tasks, 5.5h, 1 Critical + 1 High. L0 anchor + migration narrative.

### Phase 9: Verification (sandbox + sync + registry)

| # | Task ID | Description | Priority | Est. | Deps | Trace | Output | Status |
|---|---------|-------------|----------|------|------|-------|--------|--------|
| 23 | T9.1 | Run `scripts/validate_skill.py` self-test trên skill-builder 0.0.3 → expect Exit Code 0; chạy 11 check methods: structure, SKILL.md constraints, PD links, file mapping (section-number pattern), placeholder density (<5 PASS per C2), error handling, context coverage, fidelity, todo cross-ref, trace tags (4 standard + 4 legacy forbidden), format compliance | Critical | 0.5h | T0.1, T5.1, T8.1 | [TỪ DESIGN §3 scripts zone, §6 Interaction #5, FR-06, NFR-02, NFR-04, NFR-06, RES-07] | validator exit log | pending |
| 24 | T9.2 | Run `loop/build-checklist.yaml` v2.0.0 (T4.1) → expect all MUST checks PASS; verify 35 checks across 9 categories (per `skill-architect/loop/design-checklist.yaml` parity) | Critical | 0.5h | T4.1, T8.1 | [TỪ DESIGN §3 loop zone, §6 Interaction #5, NFR-06, RES-02] | checklist result | pending |
| 25 | T9.3 | Sync runtime: `cp -r skills/ver-0.0.2/skill-builder/* .claude/skills/skill-builder/`; verify file count = 18 (10 original + 8 new) | Critical | 0.5h | T8.1, T0.3 | [TỪ DESIGN §10 dependencies, CLAUDE.md §3, RI-3 in HANDBOOK §7.5] | runtime sync | pending |
| 26 | T9.4 | Update `skills-registry.json` entry: `version: 0.0.3` (was 0.0.2), `updated_at: 2026-06-18`, `src_path: skills/ver-0.0.2/skill-builder` (R4 + T0.3); append `output_contract:` DRC block per Q-Ext resolution; ensure `tags: [build, plan2build, pipeline-stage-3]` | High | 0.5h | T0.3, T8.1 | [TỪ DESIGN §10 dependencies, BA §8.3 RI-1, RES-03] | `skills-registry.json` (mutated) | pending |
| 27 | T9.5 | Update `workspce_tree.md` Stage 3 row: `raw/ver-3/skill-builder/` → `skills/ver-0.0.2/skill-builder/` (T0.3 sync); add note re ver-0.0.3 upgrade (T8.1) | High | 0.25h | T0.3, T8.1 | [TỪ DESIGN §10 dependencies, BA §8.3 RI-2] | `workspce_tree.md` (mutated) | pending |

**Phase 9 totals**: 5 tasks, 2.25h, 3 Critical + 2 High. Final delivery gate.

---

### Phase Summary

| Phase | Tasks | Critical | High | Medium | Est. Hours | Cumulative |
|-------|-------|----------|------|--------|------------|------------|
| 0 — Carry-over Risks | 4 | 4 | 0 | 0 | 6.5 | 6.5 |
| 1 — Knowledge | 7 | 3 | 3 | 1 | 13.5 | 20.0 |
| 2 — Policy | 1 | 1 | 0 | 0 | 4.0 | 24.0 |
| 3 — Data | 1 | 0 | 1 | 0 | 2.0 | 26.0 |
| 4 — Loop | 3 | 2 | 1 | 0 | 6.5 | 32.5 |
| 5 — Scripts | 1 | 1 | 0 | 0 | 3.0 | 35.5 |
| 6 — Examples | 2 | 1 | 0 | 1 | 5.0 | 40.5 |
| 7 — Templates | 1 | 0 | 1 | 0 | 2.0 | 42.5 |
| 8 — Core | 2 | 1 | 1 | 0 | 5.5 | 48.0 |
| 9 — Verification | 5 | 3 | 2 | 0 | 2.25 | 50.25 |
| **TOTAL** | **27** | **16** | **9** | **2** | **50.25h** | — |

**Critical path** (7 tasks, ~14h):
T0.1 (R1+R2 validator refactor, 3h) → T1.1 (KG-1 boot sequence, 3h) → T2.1 (KG-5 policy.yaml, 4h) → T5.1 (validator final, 3h) → T8.1 (SKILL.md refactor, 4h) → T9.1 (validator self-test, 0.5h) → T9.2 (checklist v2.0.0, 0.5h)

**Optional zone** (T1.7 + T6.2): 2 tasks = 4h — defer acceptable (per design §3 `file_required: false`).

---

## 3. Knowledge & Resources Needed

### 3.1 Source Artifacts (read-only inputs — already READY per §1)
- `.skill-context/skill-builder/design.md` — 12 sections, 18 files, 9 zones
- `.skill-context/skill-builder/quality-matrix.yaml` — 98.2% PASS, 161/161 MUST
- `.skill-context/skill-builder/ba-report.md` — 19 FR + 10 NFR + 10 KG + 7C + 4 RI
- `.skill-context/skill-builder/domain-handbook.md` — 10 sections, 70+ citations

### 3.2 Source Code (read-only references)
- `skills/ver-0.0.2/skill-builder/scripts/validate_skill.py` — 725 lines, 11 check methods
- `skills/ver-0.0.2/skill-builder/loop/build-checklist.yaml` — current v1.0.0 (to bump v2.0.0)
- `skills/ver-0.0.2/skill-builder/loop/build-log.md.template` — current (to refactor)
- `skills/ver-0.0.2/skill-builder/SKILL.md` — current v0.0.1 (to refactor v0.0.3)
- `skills/ver-0.0.2/skill-builder/SPEC.md` — current spec_version 3.0.0 (to sync 3.1.0)

### 3.3 Sibling Patterns (read-only references)
- `skills/ver-0.0.2/skill-architect/knowledge/knowledge-boot-sequence.md` — template for T1.1
- `skills/ver-0.0.2/skill-architect/knowledge/script-boundary-policy.md` — template for T1.2
- `skills/ver-0.0.2/skill-architect/data/knowledge-sources.yaml` — template for T3.1
- `skills/ver-0.0.2/skill-architect/loop/design-checklist.yaml` — parity structure for T4.1

### 3.4 Runtime Targets (write outputs)
- `skills/ver-0.0.2/skill-builder/SKILL.md` (refactor v0.0.3)
- `skills/ver-0.0.2/skill-builder/knowledge/` (5 existing + 3 new = 7 files)
- `skills/ver-0.0.2/skill-builder/policy/skill-builder.yaml` (new)
- `skills/ver-0.0.2/skill-builder/data/builder-knowledge-sources.yaml` (new)
- `skills/ver-0.0.2/skill-builder/templates/build-log.md.template` (new)
- `skills/ver-0.0.2/skill-builder/examples/` (1 required + 1 optional = 2 files)
- `skills/ver-0.0.2/skill-builder/loop/` (3 files: yaml v2.0.0, md mirror, log template v2)
- `skills/ver-0.0.2/skill-builder/scripts/validate_skill.py` (refactored)
- `skills/ver-0.0.2/skill-builder/docs/MIGRATION-0.0.2-to-0.0.3.md` (new)
- `.claude/skills/skill-builder/` (synced from `skills/ver-0.0.2/`)

### 3.5 Routing Targets (mutate)
- `skills-registry.json` line 168 + entry metadata (T0.3 + T9.4)
- `workspce_tree.md` Stage 3 row line 34 (T0.3 + T9.5)

### 3.6 Validators / Tools
- `scripts/validate_skill.py` (T0.1 + T5.1 — produced/refactored by this plan)
- `loop/build-checklist.yaml` v2.0.0 (T4.1 — produced by this plan)
- Python 3.8-3.14 stdlib only (NFR-10, no new deps)
- Optional: tiktoken for token budget checks (NFR-03)

### 3.7 Sync Command (T9.3)
```bash
cp -r skills/ver-0.0.2/skill-builder/* .claude/skills/skill-builder/
```

---

## 4. Definition of Done

- [ ] **18 zone files** (10 existing refactored + 8 new) created/updated per `design.md §3 Zone Mapping` — all in `skills/ver-0.0.2/skill-builder/`
- [ ] **R1 closed**: `validate_skill.py` has `_parse_zone_mapping(design_path)` helper using `^## 3\.\s+` pattern; shared between `check_file_mapping` + `check_todo_cross_reference`
- [ ] **R2 closed**: `validate_skill.py` `report()` recursive sub-skill calls wrapped in try/except IOError with graceful skip
- [ ] **R3 closed**: `policy/skill-builder.yaml` exists with G1-G8 guardrails + must/must_not + threshold + token budget + zone contract (full content per T2.1)
- [ ] **R4 closed**: `skills-registry.json` line 168 `src_path: skills/ver-0.0.2/skill-builder`; `workspce_tree.md` Stage 3 row synced
- [ ] **C1 closed**: SKILL.md frontmatter `version: 0.0.3`; SPEC.md `spec_version: 3.1.0` (if exists, sync)
- [ ] **C2 closed**: Placeholder threshold unified to `<5 PASS / 5-9 WARNING / >= 10 FAIL` in SKILL.md line 30 + build-checklist.yaml v2.0.0 + policy/skill-builder.yaml + SPEC.md
- [ ] **SKILL.md ≤ 400 tokens** (L0 strict per Q3 resolution) or ≤ 700 (L0 hard cap)
- [ ] **9 zones** present: Core + Knowledge(7) + Scripts(1) + Policy(1) + Templates(1) + Data(1) + Loop(3) + Examples(2: 1 req + 1 opt) + References(1) + Assets (skipped)
- [ ] **Zero placeholders** in any code/scripts (per FR-17, FR-19, NFR-04)
- [ ] **100% trace tag coverage** — every file header has `[TỪ DESIGN §N]`, `[TỪ BA §N]`, `[TỪ HANDBOOK §N]`, or `[GỢI Ý BỔ SUNG]`
- [ ] **Validator passes** (T9.1): `validate_skill.py` self-test → Exit Code 0, all 11 checks PASS
- [ ] **Checklist passes** (T9.2): `loop/build-checklist.yaml` v2.0.0 → all MUST checks PASS
- [ ] **Runtime synced** (T9.3): `.claude/skills/skill-builder/` has 18 files (10 original replaced + 8 new)
- [ ] **Registry updated** (T9.4): `skills-registry.json` skill-builder entry has `version: 0.0.3` + canonical `src_path` + DRC output_contract block
- [ ] **Routing synced** (T9.5): `workspce_tree.md` Stage 3 row reflects canonical path
- [ ] **Migration doc** (T8.2): `docs/MIGRATION-0.0.2-to-0.0.3.md` documents all 7 breaking changes (C1-C7)
- [ ] **Backward-compat preserved** (Q2): all 4 existing CLI flags (`--path`, `--design`, `--todo`, `--log`, `--strict-context`) functional; new `--zone-mapping-version` flag added (optional, non-breaking)
- [ ] **No new Python dependencies** (NFR-10): stdlib only

---

## 5. Notes — Resolved Open Questions

| # | Question | Resolution | Trace |
|---|----------|------------|-------|
| Q1 | `disable-model-invocation: true` — auto-trigger trong autopilot workflows? | **RESOLVED** — giữ `true` cho consistency với sibling `skill-architect`; document trong SKILL.md §12 "When NOT to Use" rằng Builder chỉ chạy manual HOẶC qua parent orchestrator explicit call. Auto-trigger deferred tới ver-0.0.4 nếu Steve muốn thay đổi | [TỪ BA §7.2 Q1, DESIGN §9 Q1, Q-Ext in DESIGN §9] |
| Q2 | `validate_skill.py` CLI backward-compat? | **RESOLVED** — preserve tất cả 5 flags hiện tại (`--path`, `--design`, `--todo`, `--log`, `--strict-context`); NEW flag `--zone-mapping-version` (optional, non-breaking) để explicit chọn pattern version (e.g., `1` cho literal "## 3. Zone Mapping", `2` cho section-number pattern `^## 3\.\s+`). Default = v2 (section-number) | [TỪ BA §7.2 Q2, DESIGN §9 Q2, R-11] |
| Q3 | SKILL.md 0.0.3 self-target token budget: 400 (strict) hay 700 (validator cap)? | **RESOLVED** — **400 tokens strict** (per BA recommendation + Q3 §9 RESOLVED in design); 700 là hard cap. R3 mitigation extract G1-G8 sang `policy/skill-builder.yaml` để đảm bảo SKILL.md body L0 anchor only | [TỪ BA §7.2 Q3, DESIGN §9 Q3 RESOLVED, §8 R3, BA Appendix B Q3, BA §1.2 P6] |
| Q4 | `policy/` zone format: YAML hay Markdown? | **RESOLVED** — **YAML** (`policy/skill-builder.yaml`) — phù hợp constraint/policy semantics với structured guardrails + threshold + token budget; sibling architect dùng MD cho `policy/*.md` nhưng builder's policy content là G1-G8 + threshold + token budget = structured data → YAML tốt hơn | [TỪ BA §7.2 Q4, DESIGN §9 Q4 RESOLVED, §3 policy zone, HANDBOOK §6.1] |
| Q5 | Bump `loop/build-checklist.yaml` v1.0.0 → 2.0.0? | **RESOLVED** — **YES, bump 2.0.0** với `tier_knowledge_parity` section mới (KG-9 closure); breaking change document trong `docs/MIGRATION-0.0.2-to-0.0.3.md` (KG-10) | [TỪ BA §7.2 Q5, DESIGN §9 Q5 RESOLVED, T4.1] |
| Q6 | NFR-01 build-time p95 benchmark placement (Stage 4 hay Stage 1.5)? | **RESOLVED** — placement ở Stage 4 (sandbox-tester) vì cần controlled environment; Stage 1.5 chỉ document NFR-01 trong §10 Metadata handoff (đã làm) | [TỪ BA Appendix B Q6, DESIGN §9 Q6 RESOLVED] |
| Q7 | NFR-09 idempotency feasibility với timestamps? | **RESOLVED** — set timestamps in build-log.md as ISO8601 with `execution_id` UUID; idempotency check normalize timestamps before diff; add to Stage 4 acceptance criteria (R12 mitigation in T4.3) | [TỪ BA Appendix B Q7, DESIGN §9 Q7 RESOLVED, R-12] |
| Q8 | SPEC.md `spec_version: 3.0.0` semantic (skill vs spec layer)? | **RESOLVED** — spec_version đại diện cho SPEC layer (semver riêng); skill version sync 0.0.1 → 0.0.3 riêng; bump SPEC.md `spec_version: 3.0.0` → `3.1.0` để phản ánh additions (zones, R1 refactor) | [TỪ BA Appendix B Q8, DESIGN §9 Q8 RESOLVED, T0.4, RES-01] |
| Q-Ext | 3 deferred knowledge gaps (KG-3, KG-8, KG-9) timeline? | **RESOLVED** — KG-8 promoted P2 → **P0** (token budget gate is blocker for R3) → schedule trong T1.3; KG-3 + KG-9 defer tới ver-0.0.4 P2 (optional `file_required: false` per design §3) | [TỪ BA §7.3, DESIGN §9 Q-Ext, §11 knowledge requirements] |

**Open `[CẦN LÀM RÕ]` items remaining**: **0** (all 9 questions resolved at this stage)

**Carried-forward risks** (from design §8, surface to Stage 3 Builder):
- R11 (sandbox validation not implemented) — defer `validate_skill.py --sandbox` flag tới ver-0.0.4
- R12 (idempotency benchmark) — T4.3 + T9.2 mitigation in this plan; full benchmark in Stage 4

---

## 6. Output Contract (DRC-compliant)

```yaml
output_contract:
  output_type: "Type 1 (Monolithic Stage)"
  target_context_variable: "target_skill"
  target_variable: "target_skill"
  destination: ".skill-context/skill-builder/todo.md"
  format: "markdown"
  schema: "raw/ver-3/_shared/schemas/todo.schema.yaml"
  handoff_to: "skill-builder-agent (Stage 3) — same skill, builds ver-0.0.3"
  next_stage_hint: "skill-builder-agent"
  confidence: 0.92
  status: in_progress
  lifecycle_transition: "designed → planning-completed"
  deliverables:
    - file_id: "execution_plan"
      path_template: ".skill-context/skill-builder/todo.md"
      format: "markdown"
      required_sections:
        - "§1 Pre-requisites"
        - "§2 Phase Breakdown"
        - "§3 Knowledge & Resources"
        - "§4 Definition of Done"
        - "§5 Notes"
        - "§6 Output Contract"
        - "§7 Builder Feedback Integration"
      required_drc_block: true
      required_trace_tags:
        - "[TỪ DESIGN §N]"
        - "[GỢI Ý BỔ SUNG]"
        - "[TỪ AUDIT TÀI NGUYÊN]"
        - "[CẦN LÀM RÕ]"
  handoff_artifacts:
    - ".skill-context/skill-builder/design.md"
    - ".skill-context/skill-builder/quality-matrix.yaml"
    - ".skill-context/skill-builder/ba-report.md"
    - ".skill-context/skill-builder/domain-handbook.md"
    - ".skill-context/skill-builder/todo.md"
  downstream_consumers:
    - stage: 3
      agent: "skill-builder-agent"
      consumes: ["design.md", "todo.md", "quality-matrix.yaml"]
      produces:
        - "skills/ver-0.0.2/skill-builder/SKILL.md (v0.0.3 refactored)"
        - "skills/ver-0.0.2/skill-builder/knowledge/ (7 files)"
        - "skills/ver-0.0.2/skill-builder/policy/skill-builder.yaml (new)"
        - "skills/ver-0.0.2/skill-builder/scripts/validate_skill.py (refactored)"
        - "skills/ver-0.0.2/skill-builder/templates/build-log.md.template (new)"
        - "skills/ver-0.0.2/skill-builder/data/builder-knowledge-sources.yaml (new)"
        - "skills/ver-0.0.2/skill-builder/loop/ (3 files: yaml v2.0.0 + md + log v2)"
        - "skills/ver-0.0.2/skill-builder/examples/ (1 req + 1 opt)"
        - "skills/ver-0.0.2/skill-builder/docs/MIGRATION-0.0.2-to-0.0.3.md (new)"
        - ".claude/skills/skill-builder/ (synced runtime)"
        - "skills-registry.json (line 168 + entry updated)"
        - "workspce_tree.md (Stage 3 row synced)"
```

---

## 7. Builder Feedback Integration

> Constraints and audit hooks cho Stage 3 (`skill-builder-agent`) khi thực thi todo này.

### 7.1 Mandatory Constraints

- **G1 — Engineer-Critic Stance** (per DESIGN §2.3, HANDBOOK §6.4): Builder MUST audit `design.md` cho phi logic + zone coherence TRƯỚC khi execute T0.1. Nếu confidence < 70% halt + emit `[CẦN LÀM RÕ]`. Mỗi phase gate check trước khi proceed.
- **G4 — Source Grounding** (per DESIGN §2.3, FR-04): Mọi T1.*, T2.1, T3.1, T4.*, T5.1, T6.*, T7.1, T8.* file PHẢI cite ít nhất một `[TỪ DESIGN §N]`, `[TỪ BA §N]`, `[TỪ HANDBOOK §N]`, hoặc `[GỢI Ý BỔ SUNG]` trong header comment.
- **G7 — Zone Contract Block** (per DESIGN §2.3, FR-03 + FR-17): Tất cả file creation PHẢI nằm trong `design.md §3` `Files cần tạo` column. KHÔNG tạo `README.md`, `LICENSE`, `Makefile`, hay bất kỳ file nào ngoài §3 — sẽ trigger `check_file_mapping` FAIL.
- **Script Boundary** (per DESIGN §2.5, KG-2, FR-17/18): `validate_skill.py` (T0.1 + T5.1) chỉ IO deterministic — KHÔNG cognitive logic, KHÔNG generate prompt templates, KHÔNG make zone decisions, KHÔNG LLM API calls.
- **L1 Separation** (per DESIGN §3 policy zone, R3, KG-5): `policy/skill-builder.yaml` (T2.1) chứa toàn bộ G1-G8 + must/must_not + threshold + token budget + zone contract. SKILL.md (T8.1) chỉ L0 anchor ≤400 tokens, tham chiếu `policy/skill-builder.yaml` cho guardrails.
- **Threshold Unification** (per DESIGN §8 R5 + §9 Q5 RESOLVED, C2): Tất cả 4 chỗ (SKILL.md line 30, build-checklist.yaml, policy/skill-builder.yaml, SPEC.md) PHẢI dùng `<5 PASS / 5-9 WARNING / >= 10 FAIL` — KHÔNG có giá trị khác.
- **Zero Placeholder** (per FR-17, FR-19, NFR-04): KHÔNG `TODO`, `pass`, `mock()`, `...`, `[MISSING_DOMAIN_DATA]` trong bất kỳ production code/script. Validator sẽ FAIL.
- **Backward-compat** (per Q2 RESOLVED, T5.1): Tất cả 5 existing CLI flags (`--path`, `--design`, `--todo`, `--log`, `--strict-context`) PHẢI functional. NEW `--zone-mapping-version` flag optional.
- **Runtime Sync Gate** (per DESIGN §10, T9.3): KHÔNG declare "built" cho đến khi `.claude/skills/skill-builder/` có đủ 18 files (10 replaced + 8 new). T9.3 là binary gate.
- **Determinism** (per NFR-02, NFR-09): Validator exit code PHẢI deterministic (0/1, không random). build-log.md timestamps PHẢI ISO8601 + `execution_id` UUID để idempotency check normalize.

### 7.2 DAG Order Enforcement

- **Phase 0** (T0.1-T0.4) MUST complete trước Phase 1 — validator regex refactor + threshold unblock knowledge authors dùng helper mới.
- **Phase 1** (T1.1-T1.7) MUST complete trước Phase 2 — policy.yaml cần knowledge content để extract G1-G8 chính xác.
- **Phase 2** (T2.1) MUST complete trước Phase 4 + Phase 8 — policy.yaml consumed by build-checklist.yaml (T4.1) và SKILL.md (T8.1).
- **Phase 5** (T5.1) MUST complete sau Phase 0 + Phase 4 — validator final pass tích hợp helper + dùng policy.yaml thresholds.
- **Phase 8** (T8.1 SKILL.md) MUST complete CUỐI CÙNG trong zone creation — refactor L0 anchor dựa trên policy.yaml + data sources + loop v2.0.0.
- **Phase 9** (T9.1-T9.5) MUST complete sau tất cả zones — verification gate.
- **Skip/reorder** phases = quality-gate FAIL (per FR-18, G2 must_not).

### 7.3 Optional Tasks (Defer Acceptable)

- **T1.7** `knowledge/build-visualization-guidelines.md` (KG-3, Mermaid standards) — `file_required: false` per design §3
- **T6.2** `examples/fidelity-checks.md` (KG-9, 3 case studies) — `file_required: false` per design §3

Nếu defer → document trong `docs/MIGRATION-0.0.2-to-0.0.3.md` (T8.2) §"Deferred to ver-0.0.4" + add to ver-0.0.4 backlog.

### 7.4 Audit Hooks cho Stage 4 (Tester)

- NFR-01 (build time p95): measure 100 invocations, assert p95 ≤ 90s (1-5 files) / ≤ 180s (6-15 files)
- NFR-02 (validator determinism): 100 runs trên cùng input, assert exit code = 0
- NFR-05 (context coverage): chạy `--strict-context`, assert 100% critical resources covered
- NFR-09 (idempotency 3-run diff): 3 consecutive runs, diff modulo timestamps, assert byte-identical
- NFR-10 (cross-platform): CI matrix trên Python 3.8, 3.11, 3.14

---

## 8. Plan Metadata

| Field | Value |
|-------|-------|
| **Planner agent** | skill-planner (Stage 2) |
| **Generated at** | 2026-06-18 |
| **Skill name** | skill-builder |
| **Skill version (target)** | 0.0.3 |
| **Skill version (current)** | 0.0.2 |
| **SCS (Skill Complexity Score)** | 3.1 (from quality-matrix 0.97 + 9 zones + 18 files — exceeds 3.0 threshold, but design is monolithic not micro-skill split per Stage 1 decision) |
| **DAG depth** | 10 phases (0-9) |
| **Total tasks** | 27 (25 required + 2 optional) |
| **Critical path length** | 7 tasks (T0.1 → T1.1 → T2.1 → T5.1 → T8.1 → T9.1 → T9.2) ≈ 14h |
| **Total estimated hours** | 50.25h (46.25h required + 4h optional) |
| **Critical-severity tasks** | 16 (59%) |
| **Confidence (self-assessed)** | 0.92 |
| **Open clarifications** | 0 (all 9 questions resolved: Q1-Q8 + Q-Ext) |
| **Required micro-skill sub-plans** | 0 (SCS=3.1 but design is monolithic; no Recursive Physical Micro-skills split per DESIGN §10 + Stage 1.5 decision) |
| **Suggested next stage** | `skill-builder-agent` (Stage 3) — awaits explicit user confirmation |
| **Quality gate** | 98.2% PASS (161/161 MUST) per upstream `quality-matrix.yaml` |
| **Routing update required** | YES — `skills-registry.json` + `workspce_tree.md` (T0.3, T9.4, T9.5) |
| **Runtime sync required** | YES — `cp -r skills/ver-0.0.2/skill-builder/* .claude/skills/skill-builder/` (T9.3) |

### Top 3 Risks (carry-forward từ DESIGN §8)

1. **R3** (SKILL.md vượt 700 tokens) — closed bởi T0.2 + T2.1 (L1 extraction) + T8.1 (L0 strict 400 tokens)
2. **R4** (routing mismatch registry src_path) — closed bởi T0.3 + T9.4
3. **R1** (validator regex brittleness) — closed bởi T0.1 + T5.1 (section-number pattern + helper)

### Top 3 `[CẦN LÀM RÕ]` Open (resolved at this stage)

1. Q1 (disable-model-invocation auto-trigger) — RESOLVED: keep `true` for sibling consistency; defer auto-trigger to ver-0.0.4
2. Q2 (CLI backward-compat) — RESOLVED: preserve 5 existing flags; add `--zone-mapping-version` (non-breaking)
3. Q3 (SKILL.md 0.0.3 token budget) — RESOLVED: 400 tokens strict per BA recommendation

### Verification

- Validator self-test (T9.1): expect Exit 0
- Checklist v2.0.0 (T9.2): expect all MUST checks PASS
- Runtime sync (T9.3): 18 files present in `.claude/skills/skill-builder/`
- Registry update (T9.4): `skills-registry.json` reflects ver-0.0.3 + canonical path
- Routing sync (T9.5): `workspce_tree.md` Stage 3 row canonical

---

## 9. Handoff Note to Stage 3 (skill-builder-agent)

> This `todo.md` is the Stage 2 artifact for **skill-builder ver-0.0.3** self-application (dogfooding). Stage 3 (`skill-builder-agent`) consumes `design.md` + `todo.md` + `quality-matrix.yaml` để execute 27 tasks trong 10 phases.
>
> **Critical reminders for Builder**:
>
> 1. **Self-application**: Builder is building ITSELF (skill-builder 0.0.2 → 0.0.3). Honor G1 (engineer-critic stance) — audit design.md for phi logic BEFORE T0.1.
> 2. **DAG order strict**: Do NOT skip/reorder phases. Phase 0 → 1 → 2 → 3 → 4 → 5 → 6 → 7 → 8 → 9. FR-18 violation = quality-gate FAIL.
> 3. **L0 strict**: SKILL.md ≤ 400 tokens (Q3 resolution). Use `policy/skill-builder.yaml` cho G1-G8 guardrails. T8.1 cannot exceed budget.
> 4. **Zone contract**: Tất cả 18 files PHẢI match `design.md §3` exactly — không thêm, không bớt (trừ 2 optional T1.7 + T6.2 có thể defer nhưng phải document).
> 5. **R1 refactor**: `_parse_zone_mapping` helper với `^## 3\.\s+` pattern. Share giữa `check_file_mapping` + `check_todo_cross_reference`. Wrap recursive sub-skill calls in try/except.
> 6. **R3 extraction**: Toàn bộ G1-G8 + must/must_not + threshold + token budget từ SKILL.md body sang `policy/skill-builder.yaml` (T2.1).
> 7. **C2 threshold**: `<5 PASS / 5-9 WARNING / >= 10 FAIL` ở TẤT CẢ 4 chỗ — SKILL.md line 30, build-checklist.yaml v2.0.0, policy/skill-builder.yaml, SPEC.md.
> 8. **C1 version**: SKILL.md frontmatter `version: 0.0.3`; SPEC.md `spec_version: 3.1.0`.
> 9. **Q1 auto-trigger**: Keep `disable-model-invocation: true` — document manual-only behavior in SKILL.md §12.
> 10. **Runtime gate**: T9.3 sync là binary gate — không declare "built" cho đến khi `.claude/skills/skill-builder/` có đủ 18 files.
>
> **No need to re-validate upstream artifacts** — 98.2% PASS, 0 placeholders, trace_tag_coverage=1.0, 7/7 contradictions resolved, 7/10 KG closed (3 deferred optional).
>
> **Do NOT trigger Stage 4** (sandbox-tester) or Stage 5 (indexer) automatically. Parent session decides.
