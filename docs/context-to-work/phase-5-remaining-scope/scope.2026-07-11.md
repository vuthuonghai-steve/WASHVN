# Phase 5 BA Pipeline — Scope Analysis: Remaining Work

**Date**: 2026-07-11
**Status**: Complete — Document Only (per context-before-fix pattern)
**Skill**: context-before-fix v1.0.0
**Inputs**:
- `docs/plans/plan-checklist.2026-07-07.md` (§10)
- `Temps/spec/roadmaps/05-skill-build-ba-pipeline.md`
- `Temps/spec/architects/` (P0, P3, P4, P5, shared)
- `docs/context-to-work/phase-5-audit/phase5-ba-pipeline-test-report.2026-07-11.md`
- Filesystem audit: `.claude/`, `skills/ver-3/`, `.skill-context/`

---

## §1: Problem Summary

Phase 5 (BA Skills Pipeline) hiện tại `in_progress` với **9/15 tasks** hoàn thành và **7/9 AC** mechanical PASS. Tuy nhiên, có **nhiều vấn đề tiềm ẩn** không được phản ánh trong plan-checklist:

1. **aggregate-quality-gatekeeper không tồn tại** — Phase 3 đã decompose nó thành 3 agents riêng, nhưng Phase 5 vẫn tham chiếu nó như monolithic → impedance mismatch blocking Tasks 3/6/9 và AC-8
2. **ba-pipeline-runner chưa được test end-to-end sạch** — A artifacts tồn tại nhưng là direct writes, không qua agent → AC-9 là false positive
3. **DRC resolver global fail** — 13 skills fail, trong đó 3 BA skills thiếu registry entries
4. **8 tasks bị missing khỏi checklist** — sync gaps, validator bugs, quality gates chưa verify
5. **2 bug reports** trên ba-pipeline-runner cần resolve
6. **`production-quality-gatekeeper` không có trong `skills/ver-3/`** — không deploy được cho AC-8

---

## §2: Entry Point

| Field | Value |
|:------|:------|
| **Primary spec** | `Temps/spec/roadmaps/05-skill-build-ba-pipeline.md` (642 lines) |
| **Tracking doc** | `docs/plans/plan-checklist.2026-07-07.md` §10 (lines 527-619) |
| **Audit report** | `docs/context-to-work/phase-5-audit/phase5-ba-pipeline-test-report.2026-07-11.md` |
| **Agent architecture** | `docs/context-to-work/phase-3/agent-architecture.md` (decomposition) |
| **Bug reports** | `docs/bugs/hooks/ba-pipeline-runner-state-write-conflict.md` |
| | `docs/bugs/hooks/state-ledger-schema-mismatch-runner-vs-hook.md` |
| **State schema** | `Temps/spec/architects/P0-context-bus-and-state/state-yaml-protocol.md` |
| **Fallback matrix** | `Temps/spec/architects/P5-fallback-and-escalation/fallback-matrix-full.md` |
| **Quality gates** | `Temps/spec/architects/shared/quality-gates-reference.md` |
| **Context bus** | `Temps/spec/architects/P0-context-bus-and-state/context-bus-schema.md` |
| **Artifact registry** | `skills/ver-3/_shared/artifact_registry.yaml` |
| **Next phase blockers** | `docs/context-to-work/next-phase-analysis/scope.2026-07-10.md` (line 383) |

---

## §3: Scope Definition

```yaml
in_scope:
  - Tất cả tasks còn lại của Phase 5 theo plan-checklist (Tasks 3, 6, 9, 11, 14, 15)
  - Missing items từ roadmap spec không có trong checklist (M1-M8)
  - Hidden/implicit requirements từ architect specs (H1-H7)
  - Blockers cần resolve trước khi Phase 5 đạt DONE (C1-C4)
  - Dependencies: aggregate-quality-gatekeeper, ba-pipeline-runner, DRC resolver, _state.yaml
  - File sync status (.claude/skills/ vs skills/ver-3/)

out_of_scope:
  - Fix code hoặc implementation (chỉ document)
  - Phase 6+ design decisions
  - Pre-existing bugs không liên quan Phase 5 (e.g. DRC fail trên pre-Phase-5 skills)
  - Re-write roadmap spec (đã có ver-3 với decomposed names)

confidence: 90%
# Cao vì đã có filesystem audit + 2 agent cross-reference + audit report
```

---

## §4: Current Status Baseline (Verified)

### Checklist Tasks

| # | Task | Checklist Status | Actual Status (Filesystem) | Evidence |
|---|------|:----------------:|:--------------------------:|:---------|
| 1 | Build ba-elicitor | ✅ Done | ✅ Done | 14 files at `.claude/skills/ba-elicitor/` + `skills/ver-3/ba-elicitor/` |
| 2 | Run local validator ba-elicitor | ✅ Done | ✅ Done (3/8 false negatives) | `validate_outputs.py` exists, test report §2.1 |
| **3** | **Gatekeeper audit ba-elicitor** | **❌ Pending** | **🔴 BLOCKED** | aggregate-quality-gatekeeper không tồn tại (xem §4a) |
| 4 | Test invoke ba-elicitor | ✅ Done | ✅ Done | elicitation-report.md 9,913 bytes, test report AC-6 |
| 5 | Build ba-analyst | ✅ Done | ✅ Done | 12 files, validate_metrics.py 8/8 PASS |
| **6** | **Gatekeeper audit ba-analyst** | **❌ Pending** | **🔴 BLOCKED** | Same blocker as Task 3 |
| 7 | Test ba-analyst | ✅ Done | ✅ Done | analysis-report.md exists, test report §2.2 |
| 8 | Build ba-synthesizer | ✅ Done | ✅ Done | 14 files, check_congruence.py 8/8 PASS |
| **9** | **Gatekeeper audit ba-synthesizer** | **❌ Pending** | **🔴 BLOCKED** | Same blocker as Task 3 |
| 10 | Test ba-synthesizer | ✅ Done | ✅ Done | business-analysis.md 5,126 bytes, test report §2.3 |
| **11** | **Pipeline via ba-pipeline-runner** | **❌ Pending** | **⚠️ AT_RISK** | Agent tồn tại; artifacts là direct writes, không qua agent; 2 bug reports |
| 12 | Deploy 3 skills | ✅ Done | ✅ Done | `.claude/skills/ba-{elicitor,analyst,synthesizer}/` |
| 13 | Update skills-registry.json | ✅ Done | ✅ Done | 3 BA entries at lines 224-296 |
| **14** | **Update _state.yaml** | **❌ Pending** | **❌ Not done** | Chỉ 1 line `status: active`; spec expects ~19 fields |
| **15** | **Full AC-1→9** | **❌ Pending** | **⚠️ Partial (7/9)** | AC-8 manual, AC-5 cross-cutting |

### Acceptance Criteria

| AC | Checklist | Actual | Detail |
|:---|:---------:|:------:|:-------|
| AC-1: 3 skills deployed | ✅ | ✅ PASS | `test -f .claude/skills/ba-*/SKILL.md` |
| AC-2: Frontmatter 10 fields | ✅ | ✅ PASS | All 3 parse valid YAML |
| AC-3: SKILL.md ≤ 700 tokens | ✅ | ✅ PASS | All 3 under 800 words |
| AC-4: ≥4 7-Zones populate | ✅ | ✅ PASS | Each has 5-6 zones |
| AC-5: DRC files parse + ref schemas | ✅ | ⚠️ Cross-cutting | Phase-5 passes; global DRC resolver fails (13 skills) |
| AC-6: Mock invoke ba-elicitor | ✅ | ✅ PASS | 9,913 bytes |
| AC-7: Mock full BA pipeline | ✅ | ✅ PASS | 5,126 bytes |
| **AC-8: Gatekeeper ≥70%** | **❌** | **⏸️ MANUAL** | **Blocked by aggregate-quality-gatekeeper** |
| **AC-9: Pipeline chain** | **✅** | **⚠️ FALSE POSITIVE** | Artifacts exist but NOT produced by ba-pipeline-runner agent |

### Deliverables — All 20 files ✅ (per filesystem audit)

All deliverables for ba-elicitor (8), ba-analyst (6), ba-synthesizer (6) checked off and file-verified.

---

## §4a: Blockers & Critical Issues (4 Items)

### C1 — aggregate-quality-gatekeeper Impedance Mismatch 🔴 CRITICAL

**Source**: Phase 3 decomposition (`agent-architecture.md` lines 646-651)
**Affects**: Tasks 3, 6, 9; AC-8
**Status**: UNRESOLVED

| Entity | Status | Description |
|:-------|:------:|:------------|
| `aggregate-quality-gatekeeper` (monolithic) | ❌ Not found | Không tồn tại agent/skill nào với tên này |
| `quality-scorer` agent | ✅ EXISTS | `.claude/agents/quality-scorer.md` — nhưng eval report là **NEEDS_FIX** |
| `design-validator` agent | ✅ EXISTS | `.claude/agents/design-validator.md` |
| `drift-detector` agent | ✅ EXISTS | `.claude/agents/drift-detector.md` |
| `production-quality-gatekeeper` skill | ⚠️ Legacy only | Chỉ ở `skills/ver-0.0.x/`, **không có trong `skills/ver-3/`** |

**quality-scorer NEEDS_FIX (3 blocker items)** — từ post-deploy eval report:
1. Hook format sai — `pre-tool-use` dùng exit code thay vì stdout JSON permissionDecision format
2. `{skill}` placeholder trong regex literal — không resolve được tại runtime
3. `justification` field không nằm trong bất kỳ schema nào — sẽ fail validation

**Ambiguity cần resolve**: Phase 5 roadmap spec references `aggregate-quality-gatekeeper` 6 lần. Phase 3 architecture decomposed nó thành 3 agents. Quyết định:
- Option A: Invoke `quality-scorer` agent (đủ cho META scoring)?
- Option B: Invoke `design-validator` + `quality-scorer` sequential?
- Option C: Sửa `quality-scorer` eval failures trước, rồi invoke?

### C2 — ba-pipeline-runner Agent Chưa Clean Test 🔴 CRITICAL

**Source**: Audit report §5 — "user-auth artifacts exist but were NOT produced by ba-pipeline-runner agent; they were direct writes"
**Affects**: Task 11, AC-9
**Status**: Doc bugs pending

**2 bug reports cần fix trước khi clean test**:
| Bug | File | Impact |
|:----|:-----|:-------|
| State write conflict | `docs/bugs/hooks/ba-pipeline-runner-state-write-conflict.md` | Pipeline runner không write được state |
| Schema mismatch | `docs/bugs/hooks/state-ledger-schema-mismatch-runner-vs-hook.md` | Ledger schema không match giữa runner vs hook |

**Test results từ các mock features**:
| Feature | Pipeline Status | Issue |
|:--------|:---------------:|:------|
| `user-auth` | completed | Direct writes, không qua agent |
| `mock-search-feature` | completed_with_block | Analyst write bị PreToolUse hook block |
| `mock-cart-feature` | failed | Write gate block ba-analyst zone writes |
| `mock-login-feature` | completed_with_inline_delivery | Artifacts ở dạng text, không persisted |
| `mock-notify-feature` | completed | OK nhưng không verify agent invocation |

### C3 — DRC Resolver Global Failure 🟡 BLOCKER

**Source**: Audit report §3; `drc_resolver.py --all`
**Affects**: AC-5
**Status**: Cross-cutting (13 skills fail)

**Phase 5-specific registry gaps**:
| Missing Entry | Schema Field | Expected Value |
|:-------------|:-------------|:---------------|
| `raw_request` input | artifact_registry.yaml | BA pipeline input artifact |
| `thought_cache` output | artifact_registry.yaml | BA chain intermediate output |
| `input_artifact_name` mapping | DRC cross-ref | BA input resolution |
| `output_artifact_id` mapping | DRC cross-ref | BA output cross-reference |

### C4 — `_state.yaml` Chưa Update 🟡

**Source**: `.skill-context/_state.yaml` — only `status: active` (1 line)
**Affects**: Task 14
**Status**: NOT DONE

**Schema expectation** (từ `state-yaml-protocol.md`): ~19 fields including
`version`, `run_id`, `created_at`, `execution_mode`, `source_skill_ref`, `current_stage`, `status`, `iteration_count`, `max_iterations`, `scs_score`, `branch`, `routing_mode`, `context_bus_ref`, `artifacts`, `fallback_history`, `stage_status`, `micro_skill_tracking`, `escalation`

**Archive**: 2 corrupt state files từ Phase 0, 1 escalation_report.yaml

---

## §4b: Missing Items From Checklist (8 Items — M1→M8)

| # | Missing Item | Source | Severity | Detail |
|---|-------------|--------|----------|--------|
| **M1** | `elicitation_patterns.md` sync (ver-3 → runtime) | Audit §5 | Medium | ver-3 has 3-Layer Architecture + YAML frontmatter; runtime old |
| **M2** | `verify_phase5_artifacts.py` sync | Audit §3 | Low | Already synced ✅ |
| **M3** | Register BA artifacts in `artifact_registry.yaml` | Audit §3, DRC spec | **Medium** | Missing raw_request, thought_cache, I/O mappings (xem C3) |
| **M4** | Fix `validate_outputs.py` false negatives | Audit §5 | Medium | C2 (quoted text), C5 (threshold ≥5), C6 (Mermaid labels) |
| **M5** | BA quality gates (BA-1→4) verification | `quality-gates-reference.md` L10-12 | Medium | 4 BA gates chưa được verify bởi quality-scorer |
| **M6** | Fallback F16-F19 integration test | `fallback-matrix-full.md` L68-71 | Medium | 4 BA-specific fallbacks chưa test |
| **M7** | Context Bus thought-cache registration | `context-bus-schema.md` L67 | Low-Med | thought_cache path chưa có entry riêng trong registry |
| **M8** | Deploy script | Roadmap L38 | Low | Roadmap mentions deploy script nhưng không có; manual cp |

---

## §4c: Hidden Requirements (7 Items — H1→H7)

| # | Requirement | Source | Severity | Detail |
|---|-------------|--------|----------|--------|
| **H1** | Verify ba-pipeline-runner `state_ledger_validation_hook` | `agent-architecture.md` §3-bis | Medium | Hook flag=true cần verified trong agent config |
| **H2** | BA Thought-Cache → Phase 6 consumption contract | `context-bus-schema.md`, `quality-gates-reference.md` | Medium | Phase 6 Builder consumes thought-cache; cần schema alignment |
| **H3** | `artifact_registry.yaml` BA entry expansion (consumed_by) | `artifact_registry.yaml` L112-142 | Medium | `elicitation_report` consumed_by missing `ba-analyst`; `synthesis_report` missing `skill-explorer` |
| **H4** | Pipeline orchestrator ↔ ba-pipeline-runner handoff | `agent-architecture.md`, `Temps/spec/architects/README.md` | Low | By design: BA chain không wire vào orchestrator. Cần verify handoff |
| **H5** | thought-cache.yaml schema file missing | Roadmap D5-1-4, context-bus-schema L67 | Medium | Schema là "inline (per spec P2)" nhưng P2 spec không tồn tại |
| **H6** | karpathy-standards.md incomplete (87/100 dòng) | Phase 4 AC-7 | Low | BA skills reference nó; chưa đạt AC |
| **H7** | Eval v1 downstream: Phase 6 split, hysteresis cap | `critic-response-eval-v1.md` | Low | Không ảnh hưởng trực tiếp Phase 5, nhưng ba-pipeline-runner cần aware |

---

## §4d: Blind Spots Identified (9 Items — BS1→BS9)

> **Source**: Peer review of this document. Các vấn đề tài liệu gốc chưa đề cập hoặc đánh giá sai severity.

| # | Blind Spot | Severity | Doc'd Severity | Delta | Description |
|---|-----------|:--------:|:--------------:|:-----:|-------------|
| **BS1** | **quality-scorer eval failures — hidden complexity** | **🔴 P0** | "1 session" | **Underestimated** | 3 blockers ≠ 3 edits. Hook format (`pre-tool-use` exit code) cần rewrite toàn bộ hook logic. `{skill}` regex literal cần rename frontmatter hoặc regex pattern. `justification` field missing schema — add schema trước rồi sửa hook. Actual discrete edits: **5-7 file changes** cross 2-3 components. |
| **BS2** | **_state.yaml chain dependency bị bỏ qua** | **🔴 P0** | "30 min, none" | **Wrong dependency** | `_state.yaml` populate là trách nhiệm của ba-pipeline-runner hooks (per agent-architecture.md). Nếu runner chưa fix bugs (C2), manual update = false positive: Phase 5 "pass" nhưng runner không self-report được. Fix chain: runner bugs → test runner → auto-populate. |
| **BS3** | **Sync direction chưa verify** | **🟡 P1** | No mention | **New finding** | Doc assume `skills/ver-3/` → `.claude/skills/` là one-direction STT. Runtime có thể có hotfix không ported ngược. Cần `diff` check và rule: nếu runtime có delta, sync ver-3 → runtime sẽ **destroy hotfixes**. |
| **BS4** | **Deploy script (M8) underestimated** | **🟡 P1** | Low | **Undervalued** | Deploy script là prerequisite cho autonomous pipeline. AC-9 spirit (pipeline chain) không đạt nếu manual cp là bước cuối. |
| **BS5** | **Regression risk khi fix quality-scorer** | **🟡 P1** | No mention | **New finding** | Existing agents invoke quality-scorer: pipeline-orchestrator, design-validator (indirect). Thay đổi hook format (exit code → stdout JSON) + output schema → có thể **break existing pipelines** ngoài Phase 5. Cần regression test plan trước khi patch. |
| **BS6** | **thought-cache schema (H5) gate priority wrong** | **🟡 P1** | P2 in §9 Q5 | **Mis-prioritized** | Phase 5 outcome artifact (business-analysis.md) không có thought-cache schema = Phase 6 không validate output format. H2 (consumption contract) not enforceable. Nếu Phase 5 DONE yêu cầu output_contract cho Phase 6 → H5 là **P1**. |
| **BS7** | **Corrupt Phase 0 state files — unassessed** | **🟢 P2** | No mention | **New finding** | Line 182 note "2 corrupt state files từ Phase 0" nhưng không trace: BA skills có chain data dependency vào Phase 0 artifacts? Cần git log `.skill-context/_state.yaml` để biết corrupt từ khi nào. |
| **BS8** | **Karpathy standards incomplete (H6) — silent degradation** | **🟢 P2** | Low | **Undervalued** | BA skills reference karpathy-standards.md (87/100 lines). Guideline incomplete → mỗi BA skill interpret khác nhau → **non-uniform quality**. Phase 6 consume → propagate inconsistencies. Compounding risk. |
| **BS9** | **Thiếu "clean test" criteria cho ba-pipeline-runner** | **🟢 P2** | No mention | **New finding** | Task 11 cần AC list riêng: (a) artifacts auto-generated bởi agent? (b) state ledger populated? (c) fallback F16-F19 verified? (d) error propagation stage N→N+1? (e) retry behavior? |

---

## §4e: Decision Tree — Blind Spot Resolution Path

```
BS1 (quality-scorer complexity)
├── Option A: Deep fix — rewrite hook, schema, regex (~1.5 sessions)
│   └── Cần regression test plan (BS5)
└── Option B: Targeted fix — minimal changes, chỉ đủ AC-8 pass (~0.5 session)
    └── Tradeoff: accumulation of tech debt

BS2 (_state.yaml chain) → [Fix runner bugs first → auto-populate]
BS3 (sync direction) → [Diff check → decision rule in §6]
BS4 (deploy script) → [Add to Phase 2 tasks if AC-9 spirit needed]
BS5 (regression) → [Pre-requisite checklist before BS1]
BS6 (thought-cache) → [Resolve Q5: create schema file if Phase 6 contract needed]
BS7 (corrupt state) → [Git log investigation, no execution impact yet]
BS8 (standards) → [Track in Phase 6 readiness, not Phase 5]
BS9 (clean test) → [Define criteria in §10 Phase 2 prerequisites]
```

---

## §5: Impact Analysis

### Direct Impact (if not fixed before Phase 6)

| Issue | Blocks | Risk to Phase 6 |
|:------|:-------|:----------------|
| AC-8 not done | Phase 5 DONE | Phase 6A starts without quality baseline for BA skills → Γ-1 (self-referential blindness) |
| ba-pipeline-runner not tested | Task 11, AC-9 | Phase 6A explorer không nhận được business-analysis.md chất lượng |
| DRC resolver fail | AC-5 | Phase 6A/6B DRC validation cũng fail → Phase 6 AC-5 fail |
| thought-cache not in registry | H3, H5 | Phase 6B builder không tìm thấy thought-cache theo schema → BUILD-6.0/6.1 fail |
| validate_outputs.py false negatives | M4 | Phase 6 sẽ kế thừa validator với false positive rate cao |

| quality-scorer fix complexity (BS1) | AC-8 | 1 session estimate là deficit → actual effort có thể kéo dài Phase 5 completion thêm 0.5-1 session |
| sync direction drift (BS3) | M1, all BA skills | Hotfix trong runtime bị destroy khi sync ver-3 → skill regression không traceable |
| regression risk (BS5) | quality-scorer consumers | Thay đổi hook schema break pipeline-orchestrator, design-validator → multiple Phase failures |
| no clean test criteria (BS9) | AC-9, Task 11 | Task 11 không có pass/fail threshold → completion forever ambiguous |

### Indirect Impact

| Issue | Affects | Rationale |
|:------|:--------|:----------|
| aggregate-quality-gatekeeper impedance | Phase 6A quality-scorer | Cùng ambiguity về agent nào chịu trách nhiệm quality audit |
| elicit_patterns.md version drift | All Phase 6 skills using BA | Knowledge inconsistency: 2 versions của cùng 1 doc |
| Fallback F16-F19 untested | Phase 5 resilience | BA pipeline không fallback correct khi thought-cache corrupt |
| _state.yaml not populated | Phase 8, Suite integrity | No Phase 5 completion record cho suite-wide tracking |

---

## §6: Affected Components

### Directly Affected (Phase 5 scope)

```
docs/plans/plan-checklist.2026-07-07.md          ← Cần update tasks 3/6/9 resolution
.skill-context/_state.yaml                        ← Cần populate ~19 fields
skills/ver-3/_shared/artifact_registry.yaml       ← Cần add BA entries (M3, H3)
skills/ver-3/_shared/schemas/                     ← (optional) thought-cache.schema.yaml
.skill-context/ba-*/                              ← Pipeline test artifacts locations
```

### Indirectly Affected (Phase 6 dependency)

```
.claude/agents/quality-scorer.md                  ← Cần fix 3 eval blockers (hook format, regex, field)
.claude/agents/ba-pipeline-runner.md              ← Cần verify state_ledger_validation_hook (H1)
.claude/skills/ba-elicitor/knowledge/elicitation_patterns.md  ← Cần sync ver-3 version
docs/bugs/hooks/ba-pipeline-runner-state-write-conflict.md    ← Cần fix before clean test
.claude/agents/pipeline-orchestrator.md            ← BA handoff interface (H4)
	.claude/agents/*                                  ← BS5: regression affected — all agents invoking quality-scorer
	.skill-context/_state.yaml                        ← BS7: git log corrupt history; BS2: auto-populate via runner
	Temps/spec/architects/P2-*/                       ← BS6: verify P2 spec for thought-cache schema
```

---

## §7: Evidence

```yaml
evidence:
  - file: "docs/plans/plan-checklist.2026-07-07.md"
    lines: 527-619
    finding: "Phase 5 status: in_progress, 9/15 tasks, 7/9 AC"

  - file: "docs/context-to-work/phase-5-audit/phase5-ba-pipeline-test-report.2026-07-11.md"
    lines: 14-23, 126-149
    finding: "7/9 AC mechanical PASS; AC-8 manual; AC-9 artifacts NOT from ba-pipeline-runner"

  - file: "docs/context-to-work/phase-3/agent-architecture.md"
    lines: 646-651
    finding: "aggregate-quality-gatekeeper decomposed → design-validator + quality-scorer + drift-detector"

  - file: "Temps/spec/roadmaps/05-skill-build-ba-pipeline.md"
    lines: 35, 570-573, 591, 597, 603, 631
    finding: "6 references to aggregate-quality-gatekeeper as monolithic entity"

  - file: ".claude/agents/quality-scorer.md"
    finding: "EXISTS; eval report = NEEDS_FIX (3 blocker items)"

  - file: ".skill-context/_state.yaml"
    finding: "1 line: status: active — no Phase 5 data"

  - file: "Temps/spec/architects/P0-context-bus-and-state/state-yaml-protocol.md"
    finding: "Schema expects ~19 fields"

  - file: "skills/ver-3/_shared/artifact_registry.yaml"
    lines: 112-142
    finding: "Missing raw_request, thought_cache, input_artifact_name, output_artifact_id"

  - file: "docs/bugs/hooks/ba-pipeline-runner-state-write-conflict.md"
    finding: "Bug: state write conflict between runner and hooks"

  - file: "Temps/spec/architects/shared/quality-gates-reference.md"
    lines: 10-12, 29
    finding: "BA-1→4 quality gates defined but not integrated into Phase 5 ACs"

  - file: "Temps/spec/architects/P5-fallback-and-escalation/fallback-matrix-full.md"
    lines: 68-71
    finding: "F16-F19 BA-specific fallback scenarios untested"

  - file: "docs/context-to-work/phase-5-remaining-scope/scope.2026-07-11.md"
    lines: 238-284
    finding: "BS1→BS9 blind spots document quality-scorer complexity, sync direction, regression risk"
```

---

## §8: Confidence Assessment

```yaml
overall_confidence: 85%  # Adjusted down: §4d blind spots + uncertainty flags

breakdown:
  checklist_tasks_verification: 95%     # Tasks 1-15 verified via filesystem
  blocker_identification: 90%           # C1-C4 identified + documented
  missing_items_coverage: 88%           # M1-M8 + BS1-BS9 from spec cross-reference (12 → 20 items)
  hidden_requirements_coverage: 90%     # H1-H7 + BS1-BS9 blind spot peer review
  effort_estimation: 65%               # BS1 correction: 5-7 edits → underestimate; BS3 sync unknown
  filesystem_audit_accuracy: 95%       # Parallel agent cross-verification

post_review_adjustments:
  - "overall_confidence lowered to 85% from 90% — peer review uncovered 9 blind spots"
  - "effort_estimation worsened from 70%→65% — BS1 complexity + BS3 sync unknown"
  - "hidden_requirements improved 80%→90% — FS scan achieved via blind spot review"

uncertainty_flags:
  - "C1 resolution (Option A vs B) cần user decision — affecting effort estimate"
  - "H5 (thought-cache schema) uncertain — P2 spec file location không confirmed"
  - "Actual effort để fix quality-scorer needs evaluation (3 blockers → BS1: 5-7 edits)"
  - "BS3 (sync direction) chưa verified — runtime diff = unknown"
  - "BS5 (regression risk) unassessed — fix quality-scorer có thể break existing agents"
  - "BS7 (corrupt state) uninvestigated — phase origin unknown"
  - "BS9 (clean test criteria) undefined — Task 11 pass/fail ambiguous"
```

---

## §9: Open Questions

| # | Question | Priority | Depends On | Status |
|---|----------|----------|------------|--------|
| 1 | aggregate-quality-gatekeeper: invoke quality-scorer alone (A) or design-validator + quality-scorer (B)? | P0 | User decision | **OPEN** |
| 2 | quality-scorer eval failures: fix before AC-8, or bypass? | P0 | User decision | **OPEN** |
| 3 | ba-pipeline-runner bugs (2): fix before Task 11? | P1 | User decision | **OPEN** |
| 4 | DRC resolver skip pre-Phase-5 skills for AC-5, or fix all? | P1 | User decision | **OPEN** |
| 5 | thought-cache schema: create new file or use inline spec? | P2 | None | **OPEN** |
| 6 | BA quality gates (BA-1→4): add to Phase 5 ACs? | P2 | Quality-scorer available | **OPEN** |
| 7 | Fallback F16-F19 test: required for Phase 5 DONE? | P3 | None | **OPEN** |
| 8 | BS1: quality-scorer deep fix vs targeted fix? | P0 | User decision | **OPEN** |
| 9 | BS3: sync direction decision — ver-3 is source or runtime is source? | P1 | Diff results | **OPEN** |
| 10 | BS9: define clean test criteria before Task 11? | P1 | User decision | **OPEN** |

---

## §10: Summary — Remaining Work Prioritization

> **Updated**: BS1→BS9 integrated. Pre-requisite check: BS3 (sync diff) và BS9 (clean test criteria) cần resolve trước Phase 2 execution.

### Phase 1: Blocker Resolution (P0) — 1-2 sessions

| Task | Est. | Depends On | BS Map |
|:-----|:----:|:-----------|:------:|
| Decide C1: quality-scorer vs quality-scorer+design-validator | 15 min | User decision | — |
| Fix quality-scorer 3 eval blockers (hook format, regex, field) | 1-1.5 sessions | User approval | **BS1** (5-7 edits), **BS5** (regression test plan) |
| Fix ba-pipeline-runner 2 bugs | 1 session | User approval | **BS2** (_state.yaml chain dep) |
| Diff check: ver-3 ↔ runtime sync direction | 15 min | None | **BS3** (prerequisite for Phase 2) |

### Phase 2: Task Completion (P1) — 2-3 sessions

| Task | Est. | Depends On | BS Map |
|:-----|:----:|:-----------|:------:|
| Invoke quality-scorer (or equiv) on 3 BA skills ⇒ AC-8 | 1 session | C1 + BS1 resolved | **BS5** regression guard |
| Test ba-pipeline-runner with fresh feature ⇒ Task 11 | 1 session | Bugs fixed + **BS9** criteria defined | **BS9** definition first |
| Update `_state.yaml` per state-yaml-protocol.md ⇒ Task 14 | 30 min | Runner bugs fixed (auto-populate) | **BS2** chain, **BS7** git log verify |
| Register BA artifacts in artifact_registry.yaml ⇒ M3/H3 | 30 min | None | — |
| Sync elicitation_patterns.md ver-3 → runtime ⇒ M1 | 10 min | BS3 diff check done | **BS3** |
| Run full AC-1→9 ⇒ Task 15 | 30 min | All above | — |

### Phase 3: Quality Hardening (P2) — 1 session

| Task | Est. | Depends On |
|:-----|:----:|:-----------|
| Fix validate_outputs.py false negatives ⇒ M4 | 30 min | None |
| Add BA quality gates (BA-1→4) verification ⇒ M5 | 30 min | Quality-scorer fix |
| Add thought-cache.schema.yaml ⇒ H5 | 30 min | None |

### Phase 4: Nice-to-Have (P3) — 1 session

| Task | Est. | Depends On |
|:-----|:----:|:-----------|
| Test fallback F16-F19 in BA failures ⇒ M6 | 1 session | ba-pipeline-runner tested |
| Verify ba-pipeline-runner state_ledger_hook ⇒ H1 | 15 min | None |
| Verify ba ↔ orchestrator handoff ⇒ H4 | 30 min | None |

---

**NO CODE CHANGES MADE** — Context ready for Phase 5 completion sprint.

---

**Document**: `docs/context-to-work/phase-5-remaining-scope/scope.2026-07-11.md`
**Generated by**: context-before-fix v1.0.0
**Language**: Vietnamese
**Version**: 1.0.0

---

## §11: Evidence Reconciliation (Post-Investigation) — 2026-07-11

> **Phương pháp**: 5 subagent điều tra song song (READ-ONLY) quét filesystem + eval reports + spec cross-reference. Phát hiện then chốt: **scope doc hiện tại LỖI THỜI** — nhiều "blocker P0" đã được fix trên disk, và một số chẩn đoán sai bản chất. Dưới đây là đối chiếu từng mục.

### §11.1 Bảng Đối Chiếu (Mục → Kết Luận → Bằng Chứng)

| # | Mục trong scope gốc | Kết luận sau điều tra | Bằng chứng |
|:--|:--------------------|:---------------------|:-----------|
| **C1** | aggregate-quality-gatekeeper impedance mismatch 🔴 | **Confirmed** nhưng resolved-by-design | Phase3 decompose (agent-architecture.md L646-651) → design-validator + quality-scorer + drift-detector. Monolithic KHÔNG tồn tại. → Xem Q1. |
| **C2** | ba-pipeline-runner chưa clean test 🔴 | **STALE** — 2 bug ĐÃ FIX trên disk | Ba-pipeline-runner.md L42-46 đã wire `validate-state-ledger.sh` PostToolUse; L192-205 schema đã có 6 fields. 2 bug report vẫn ghi "Open/not applied" = stale. |
| **C3** | DRC resolver 13 fail / 3 BA gaps 🟡 | **Confirmed genuine** | `drc_resolver.py --all` → 13 failures; 3 BA skills thiếu `raw_request`/`thought_cache`/`input_artifact_name`/`output_artifact_id`. See §11.3. |
| **C4** | `_state.yaml` chưa update 🟡 | **Partial** — root ≠ schema scope | Root `_state.yaml` = `status: active` (1 dòng). NHƯNG 19-field schema (state-yaml-protocol.md) dành cho per-run `.skill-context/{skill}/_state_ledger.yaml`, KHÔNG phải root. See BS2. |
| **BS1** | quality-scorer complexity 5-7 edits / 2-3 comp 🔴 | **OVERSTATED / SAI** | Thực tế: **2 edits, 1 file** (quality-scorer.md L11 `hook:`→`hooks:`, L20 `{skill}`→`[^/]+`). Eval report D127 говорит lỗi là `hook:` singular ≠ `hooks:` array — KHÔNG phải "exit code vs stdout JSON" như scope doc L129 ghi. |
| **BS2** | `_state.yaml` chain dep bỏ qua 🔴 | **FALSE-POSITIVE** | Không agent/hook nào populate root `_state.yaml` theo 19-field. Root = global marker. Manual populate = không cần. |
| **BS3** | Sync direction chưa verify 🟡 | **NO DRIFT** | `diff -rq` ba-elicitor/ba-analyst = IDENTICAL. ba-synthesizer: 1 orphan `.claude/skills/ba-synthesizer/ba-synthesizer/` (rác, thiếu nội dung) → xóa. |
| **BS4** | Deploy script (M8) 🟡 | Low — manual cp chấp nhận được | Roadmap L38 mention nhưng không có file. Không block Phase 5. |
| **BS5** | Regression risk fix quality-scorer 🟡 | **OVERSTATED** | Grep toàn repo: KHÔNG agent nào dispatch quality-scorer qua Task. pipeline-orchestrator chỉ gọi `production-quality-gatekeeper`. Không có consumer đọc `quality-matrix.yaml`. |
| **BS6** | thought-cache schema gate priority 🟡 | **Premise sai một phần** | thought_cache schema là **INLINE** trong `elicitation.schema.yaml` L94-113 (KHÔNG thiếu file). P2 spec **TỒN TẠI** (`Temps/spec/architects/P2-context-hydrator/`). Scope doc L209 ghi "P2 không tồn tại" = SAI. |
| **BS7** | Corrupt Phase-0 state unassessed 🟢 | **Không thành lập** | 2 corrupt = `_state-*-corrupt.yaml` (2026-07-07) đã archive. escalation_report.yaml là valid Phase-0 report, không corrupt. BA chain KHÔNG dependency Phase-0. |
| **BS8** | Karpathy standards incomplete 🟢 | Track Phase 6, không block | 87/100 lines — compound risk, không thuộc Phase 5. |
| **BS9** | Thiếu clean-test criteria Task 11 🟢 | **Resolved** — xem §11.2 Q10 | Đã định nghĩa 5 pass/fail criteria có bằng chứng filesystem. |
| **M1** | elicitation_patterns.md drift 🟡 | **FALSE-POSITIVE** | `diff` hai file = IDENTICAL. Không drift. |
| **M3/H3** | artifact_registry BA entries thiếu 🟡 | **Confirmed genuine** | `elicitation_report` consumed_by thiếu `ba-analyst` (L117-119); `synthesis_report` thiếu `skill-explorer` (L138-140). |
| **H1** | state_ledger_validation_hook chưa wired 🟡 | **WIRED nhưng doc stale** | ba-pipeline-runner.md L42-46 đã wire PostToolUse→validate-state-ledger.sh. Roster §2 (agent-architecture L148-160) thiếu flag `state_ledger_validation_hook: true` = stale. |
| **H4** | BA ↔ orchestrator handoff 🟡 | **Intentional non-wiring** | pipeline-orchestrator.md: 0 BA references (grep confirm). Contract schema tồn tại (handoff_manifest) NHƯNG không có manifest file cụ thể BA→Phase6. |
| **H5** | thought-cache.schema.yaml thiếu 🟡 | **INLINE, không thiếu** | See BS6. |
| **AC-9** | Pipeline chain false positive ⚠️ | **Confirmed** — artifacts là direct writes | Audit report L145/L166: user-auth artifacts KHÔNG qua ba-pipeline-runner agent. Vẫn cần 1 clean run (BS9). |

### §11.2 Open Questions — Resolved by Evidence

| # | Câu hỏi | Quyết định (grounded) | Cơ sở |
|:--|:---------|:---------------------|:------|
| **Q1** | aggregate-quality-gatekeeper: invoke quality-scorer alone (A) hay +design-validator (B)? | **Option A** — quality-scorer đơn lẻ | 6 spec refs (roadmap L35/570-573/591/597/603/631) đồng nhất kỳ vọng META-1→3 → ≥70%. design-validator "NOT META scoring" (L6,34) + chỉ validate design.md. drift-detector so sánh design↔todo. |
| **Q2** | Fix quality-scorer trước AC-8? | **KHÔNG bắt buộc** — AC-8 đạt được ngay | NEEDS_FIX chỉ ở hook (không chặn scoring). Capability-auditor PASS. Nên fix targeted (0.5 session) cho hygiene SAU. |
| **Q3** | Fix 2 ba-pipeline-runner bugs trước Task 11? | **ĐÃ FIX rồi** — chỉ update bug-report status | On-disk đã đúng. Stale report = "Open". |
| **Q4** | DRC skip pre-Phase-5 skills? | **Fix BA 4 mappings + registry, ignore 10 pre-Phase-5** | 10 failures do thiếu `output_contract` frontmatter ở pre-Phase-5 skills — out of scope. |
| **Q5** | thought-cache schema: file mới hay inline? | **Giữ inline** — đã có trong elicitation.schema.yaml | Không tạo file mới. P2 spec tồn tại. |
| **Q6** | Add BA-1→4 gates vào Phase 5 ACs? | **Optional** — không bắt buộc AC-8 | quality-scorer đủ cho META. Gates là bonus. |
| **Q7** | Test F16-F19 bắt buộc cho DONE? | **Không** — nice-to-have (Phase 4) | Không block Phase 5. |
| **Q8** | BS1 deep vs targeted fix? | **Targeted** — 2 edits / 0.5 session | Overstated thành 5-7 edits. Thực tế tối thiểu. |
| **Q9** | BS3 sync direction? | **ver-3 là source** (1-way STT) | No runtime hotfix. Xóa orphan `ba-synthesizer/ba-synthesizer/`. |
| **Q10** | BS9 clean-test criteria? | **Định nghĩa 5 criteria** | (a) artifacts by agent? (b) ledger populated? (c) F16-F19? (d) error prop N→N+1? (e) retry behavior? — mỗi cái có pass/fail evidence. |

### §11.3 Genuine Remaining Work (Sau khi loại bỏ stale/false)

**P0 — Bắt buộc trước Phase 5 DONE:**
1. **Run ba-pipeline-runner clean E2E** (BS9 criteria) trên 1 feature mới → chứng minh AC-9 thực sự PASS (hiện là false positive).
2. **Invoke quality-scorer** trên 3 BA skills → AC-8 ≥70% (Option A, Q1/Q2).
3. **Register 4 BA artifacts** trong artifact_registry.yaml (M3/H3: `raw_request`, `thought_cache`, `input_artifact_name`, `output_artifact_id` + consumed_by gaps).
4. **Targeted fix quality-scorer** (2 edits) + update 2 stale bug-reports thành "Resolved".

**P1 — Nên làm:**
5. Xóa orphan `.claude/skills/ba-synthesizer/ba-synthesizer/`.
6. Update agent-architecture §2 roster: add `state_ledger_validation_hook: true` cho ba-pipeline-runner (H1 consistency).
7. Resolve spec conflict 80% (roadmap L36) vs 70% (AC-8/L572/631) → dùng 70%.

**P2/P3 — Nice-to-have:**
8. BA-1→4 gates verify (optional), F16-F19 test, BA→Phase6 handoff manifest (H4 — schema exists, file chưa có).

### §11.4 Revised Confidence

```yaml
overall_confidence: 92%  # Tăng từ 85%: stale/false items đã cleared, remaining work rõ ràng
breakdown:
  stale_items_corrected: 8      # BS1, BS2, BS3, BS5, BS6, BS7, M1, H5 misdiagnosed → corrected
  genuine_blockers: 4           # C3, C4(partial), AC-9, quality-scorer targeted fix
  open_questions_resolved: 10/10
  effort_estimation_accuracy: 90%  # BS1 "5-7 edits" → thực tế 2 edits
```

### §11.5 Recommended Immediate Actions (trước định hình triển khai)

1. **Ghi nhận**: scope doc gốc OVERESTIMATE severity của BS1/BS2/BS3/BS5/BS6/BS7/M1/H5. Thực tế Phase 5 đã gần xong hơn docs nghĩ.
2. **Sửa stale artifacts**: 2 bug-reports (C2) → "Resolved/Applied"; agent-architecture §2 roster H1 flag.
3. **Không manual-populate** `_state.yaml` (BS2 false-positive) — root là global marker.
4. **Triển khai theo §11.3**: P0 items 1-4 là đủ để Phase 5 DONE.

---

**Reconciled by**: 5 parallel investigation subagents (READ-ONLY) — 2026-07-11
**Method**: filesystem audit + eval-report cross-reference + spec reconciliation
**Status**: Scope corrected — ready for implementation shaping
