# Scope Document — Phase 5: BA Skills Pipeline

**Date**: 2026-07-10
**Status**: Updated (Phase 4 audit incorporated)
**Skill**: context-before-fix v1.0.0
**Source Documents**:
  - `Temps/spec/architects/shared/architecture-overview.md`
  - `Temps/spec/architects/shared/glossary.md`
  - `Temps/spec/architects/shared/quality-gates-reference.md`
  - `Temps/spec/architects/indexes/by-domain.md`
  - `Temps/spec/architects/indexes/by-design.md`
  - `Temps/spec/architects/indexes/by-role.md`
  - `skills/ver-3/roadmaps/index.md`
  - `skills/ver-3/roadmaps/05-skill-build-ba-pipeline.md`
  - `docs/plans/plan-checklist.2026-07-07.md`
  - `docs/context-to-work/phase-4-audit/phase4-audit-report.2026-07-10.md`
  - `skills/ver-0.0.2/ba-elicitor/` (old legacy skill — knowledge asset to mine)
  - `skills/ver-0.0.2/ba-analyst/` (old legacy skill — knowledge asset to mine)
  - `skills/ver-0.0.2/ba-synthesizer/` (old legacy skill — knowledge asset to mine)

---

## §1: Problem Summary

Phase 5 là giai đoạn xây dựng **BA Skills Pipeline** — 3 skills liên hoàn trong Master Skill Suite: `ba-elicitor` → `ba-analyst` → `ba-synthesizer`. Đây là bước đầu tiên trong chuỗi build skill thực tế (Phase 0-4 là foundation). BA pipeline là **upstream bắt buộc** cho Phase 6 (main skill pipeline), vì `business-analysis.md` output từ `ba-synthesizer` là input cho `skill-explorer` Stage 0.

**Mục tiêu cốt lõi:**
1. Build 3 skills với 7-Zone structure (knowledge, scripts, templates, loop, data, assets)
2. Đảm bảo mỗi skill pass quality-scorer ≥70%
3. Deploy skills từ `skills/ver-3/` → `.claude/skills/`
4. Test full pipeline qua `ba-pipeline-runner` agent với 1 mock feature

---

## §2: Entry Point

- **Roadmap spec**: `skills/ver-3/roadmaps/05-skill-build-ba-pipeline.md` (642 dòng)
- **Scope tracking**: `docs/plans/plan-checklist.2026-07-07.md` §10 (Phase 5 section, lines 510-597)
- **Ba-pipeline-runner agent**: `.claude/agents/ba-pipeline-runner.md` (198 dòng — đã deploy)
- **Raw skill directories** (authoring/staging): `skills/ver-3/ba-{elicitor,analyst,synthesizer}/`
  > ⚠️ **Lưu ý**: `skills/ver-3/` là **symlink** → `../skills/ver-3`. Cả 2 đường dẫn trỏ đến cùng một thư mục vật lý tại `skills/ver-3/`. Roadmap spec dùng `skills/ver-3/` làm canonical path cho authoring (xem roadmap dòng 38: "Deploy: move từ skills/ver-3/ → .claude/skills/").
- **Runtime skill directories**: `.claude/skills/ba-{elicitor,analyst,synthesizer}/`
- **Old v0.0.2 skill sources** (knowledge mining targets): `skills/ver-0.0.2/ba-{elicitor,analyst,synthesizer}/` — chứa ~1,330 lines content có thể khai thác cho Phase 5 authoring

---

## §3: Scope Definition

### 3.1 In Scope

```yaml
in_scope:
  # — Content authoring (3 skills) —
  build_ba_elicitor:
    files: ~7 (SKILL.md, knowledge/, templates/ x2, loop/, scripts/, data/)
    z7_zones: [core, knowledge, templates, scripts, loop, data, assets]
  build_ba_analyst:
    files: ~6 (SKILL.md, knowledge/, templates/, loop/, scripts/, data/)
    z7_zones: [core, knowledge, templates, scripts, loop, data, assets]
  build_ba_synthesizer:
    files: ~6 (SKILL.md, knowledge/, templates/, loop/, scripts/, data/)
    z7_zones: [core, knowledge, templates, scripts, loop, data, assets]
  
  # — Quality assurance —
  gatekeeper_audit:
    per_skill: quality-scorer agent audit (META-1→3), fix ≥70%
    sequence: ba-elicitor → fix → ba-analyst → fix → ba-synthesizer → fix
  
  # — Testing —
  mock_test:
    ba_elicitor_test: "I need an e-commerce skill for selling Vietnamese handcrafted goods internationally"
    ba_analyst_test: consume elicitation-report.md, produce analysis-report.md
    ba_synthesizer_test: consume cả 2, produce business-analysis.md
    full_pipeline: qua ba-pipeline-runner agent
  
  # — Deployment —
  deploy_skills:
    move: skills/ver-3/ba-*/ → .claude/skills/ba-*/
    registry: Update skills-registry.json
    state: Update _state.yaml Phase 5 completion
    
  # — Verification —
  run_ac_1_to_9: Mechanical AC verification (9 acceptance criteria)
```

### 3.2 Out of Scope

```yaml
out_of_scope:
  - Không build Phase 6 skills (explorer, miner, architect, gatekeeper)
  - Không build sandbox-tester hoặc indexer (Phase 7)
  - Không integration test xuyên Phase 6/7
  - Không fix architectural defects (Phase 8)
  - Không update hook registry (Phase 2 complete)
  - Không migrate knowleages/ → knowledge/ (deferred)
```

### 3.3 Boundary

```yaml
boundary:
  upstream_dependencies:
    - Phase 3: ba-pipeline-runner agent ✅ deployed
    - Phase 3: quality-scorer agent ✅ deployed (tại .claude/agents/quality-scorer.md)
    - Phase 4: 14 schemas (elicitation, analysis, synthesis) ✅ FULL — 0 stub, AC verified
    - Phase 4: DRC template ✅ tồn tại + parses (skills/ver-3/_shared/templates/drc_contract_template.yaml)
    - Phase 4: skill_skeleton.md ✅ tồn tại + đủ name/suite fields
    - Phase 4: schema_validator.py ✅ validated cơ học (valid→exit 0, broken→exit 1)
    - Phase 4: artifact_lifecycle.py ✅ deployed (SHA-256 drift detection)
    - Phase 4: drc_resolver.py ✅ "Registry consistency check passed."
    - Phase 4: 28 fixtures ✅ (14 valid + 14 broken, real test data)
    - Phase 0: 7-Zone directory scaffold ✅ tồn tại
  
  downstream_dependency:
    - Phase 6A: business-analysis.md là input cho skill-explorer
    - Phase 6A: scs-router reference elicitation-report.md
    
  artifact_zone_confinement:
    - All BA artifacts write đến .skill-context/{feature_name}/ba-{elicitor|analyst|synthesizer}/
    - thought-cache.yaml tại .skill-context/{feature_name}/thought-cache.yaml
    - KHÔNG write vào .claude/skills/, .claude/agents/, .claude/hooks/
```

---

## §4: Impact Analysis

### 4.1 Direct Impact

| Thành phần | Tác động | Mức độ |
|:---|:---|:---:|
| `skills/ver-3/ba-elicitor/` ⚠️ | Author 7 files content (hiện chỉ có .gitkeep) | 🔴 Tạo mới |
| `skills/ver-3/ba-analyst/` ⚠️ | Author 6 files content | 🔴 Tạo mới |
| `skills/ver-3/ba-synthesizer/` ⚠️ | Author 6 files content | 🔴 Tạo mới |
| `.claude/skills/ba-elicitor/SKILL.md` | Sync từ skills/ver-3 (hiện 0 bytes) | 🟡 Overwrite |
| `.claude/skills/ba-analyst/SKILL.md` | Sync từ skills/ver-3 (hiện 0 bytes) | 🟡 Overwrite |
| `.claude/skills/ba-synthesizer/SKILL.md` | Sync từ skills/ver-3 (hiện 0 bytes) | 🟡 Overwrite |
| `skills-registry.json` | Add 3 BA skills entries | 🟢 Update |
| `_state.yaml` (suite) | Record Phase 5 completion | 🟢 Update |
| `.claude/agents/ba-pipeline-runner.md` | Agent ready để orchestrate pipeline | 🟢 Không đổi |

> ⚠️ **Chú thích đường dẫn**: `skills/ver-3/` → `../skills/ver-3` (symlink). Cả 2 trỏ đến cùng thư mục vật lý `skills/ver-3/`. Roadmap spec dùng `skills/ver-3/` làm canonical authoring path (xem roadmap dòng 38). Đây là staging area: author tại `skills/ver-3/` → deploy lên `.claude/skills/`.

### 4.2 Indirect Impact

| Thành phần | Tác động | Lý do |
|:---|:---|:---:|
| `ba-pipeline-runner` agent | Pipeline orchestration success phụ thuộc vào 3 skills được build | Runtime dependency |
| Phase 6 `skill-explorer` | `business-analysis.md` là input trực tiếp | Data dependency |
| Phase 6 `scs-router` | `elicitation-report.md` output dùng cho SCS scoring | Data dependency |
| `quality-scorer` agent | Được invoke để audit từng skill | Resource contention |
| `schema_validator.py` | Validate output artifacts của BA skills | Quality gate |
| `shared/ artifact_registry.yaml` | BA artifacts (3 entries) đã defined, chỉ cần verify | Contract verification |

### 4.3 Data Flow

```text
Input: raw user request (text)
  ↓
[ba-elicitor] → elicitation-report.md + thought-cache.yaml
  ↓                                    ↓ (optional)
[ba-analyst]  → analysis-report.md     ↓ (optional read)
  ↓                                    ↓
[ba-synthesizer] → business-analysis.md (merged + cross-validated)
  ↓
Output: feeds into skill-explorer (Phase 6)
```

### 4.4 API Contracts

- **DRC template** tại `skills/ver-3/_shared/templates/drc_contract_template.yaml` — được dùng làm base cho mỗi skill
- **Elicitation schema** tại `skills/ver-3/_shared/schemas/elicitation.schema.yaml` — 5 required fields
- **Analysis schema** tại `skills/ver-3/_shared/schemas/analysis.schema.yaml` — 4 required fields
- **Synthesis schema** tại `skills/ver-3/_shared/schemas/synthesis.schema.yaml` — 4 required fields
- **Skill skeleton** tại `skills/ver-3/_shared/templates/skill_skeleton.md` — 11 XML section template

---

## §5: Call Chain

### 5.1 Build Sequence

```text
Build ba-elicitor
  → local validator (validate_outputs.py)
  → quality-scorer audit (META-1→3) → fix đến ≥70%
  → test với mock request
  ↓
Build ba-analyst
  → local validator (validate_metrics.py)
  → quality-scorer audit → fix đến ≥70%
  → test với elicitation-report từ ba-elicitor
  ↓
Build ba-synthesizer
  → local validator (check_congruence.py)
  → quality-scorer audit → fix đến ≥70%
  → test với cả 2 artifacts
  ↓
Test full pipeline qua ba-pipeline-runner agent
  ↓
Deploy 3 skills → sync raw → runtime
  ↓
Update registry + state + AC verification
```

### 5.2 Runtime Chain (khi skill được invoke)

```text
User/Agent request
  ↓
ba-pipeline-runner (orchestrator)
  ↓ Task invoke
ba-elicitor → write elicitation-report.md + thought-cache.yaml
  ↓ Gate check: elicitation-report.md tồn tại
ba-analyst → read elicitation-report → write analysis-report.md
  ↓ Gate check: analysis-report.md tồn tại
ba-synthesizer → read cả 2 + thought-cache → write business-analysis.md
  ↓ Gate check: business-analysis.md tồn tại
Pipeline complete → _ba_pipeline_state.yaml updated
```

---

## §6: Affected Components

### 6.1 Files to Create (19 files total)

**ba-elicitor** (7 files):
| # | File path | Content type |
|:---|:---|:---|
| 1 | `skills/ver-3/ba-elicitor/SKILL.md` | Core skill definition (frontmatter + XML sections) |
| 2 | `skills/ver-3/ba-elicitor/knowledge/elicitation_patterns.md` | 4 elicitation pattern reference |
| 3 | `skills/ver-3/ba-elicitor/templates/elicitation_report.template.md` | Output template with YAML frontmatter |
| 4 | `skills/ver-3/ba-elicitor/templates/thought_cache_template.yaml` | 5-section thought-cache |
| 5 | `skills/ver-3/ba-elicitor/loop/scoping_checklist.md` | Self-verification checklist |
| 6 | `skills/ver-3/ba-elicitor/scripts/validate_outputs.py` | Python validator (8 criteria) |
| 7 | `skills/ver-3/ba-elicitor/data/drc.yaml` | DRC contract (per template) |

**ba-analyst** (6 files):
| # | File path | Content type |
|:---|:---|:---|
| 1 | `skills/ver-3/ba-analyst/SKILL.md` | Core skill definition |
| 2 | `skills/ver-3/ba-analyst/knowledge/fr_nfr_taxonomy.md` | FR/NFR classification framework |
| 3 | `skills/ver-3/ba-analyst/templates/analysis_report.template.md` | Analysis report template |
| 4 | `skills/ver-3/ba-analyst/loop/interlock_checklist.md` | Interlock checklist |
| 5 | `skills/ver-3/ba-analyst/scripts/validate_metrics.py` | NFR quantification validator |
| 6 | `skills/ver-3/ba-analyst/data/drc.yaml` | DRC contract |

**ba-synthesizer** (6 files):
| # | File path | Content type |
|:---|:---|:---|
| 1 | `skills/ver-3/ba-synthesizer/SKILL.md` | Core skill definition |
| 2 | `skills/ver-3/ba-synthesizer/knowledge/cross_validation_strategies.md` | Cross-validation strategies |
| 3 | `skills/ver-3/ba-synthesizer/templates/business_analysis_template.md` | Business analysis template |
| 4 | `skills/ver-3/ba-synthesizer/loop/congruence_checklist.md` | Congruence checklist |
| 5 | `skills/ver-3/ba-synthesizer/scripts/check_congruence.py` | Cross-artifact congruence checker |
| 6 | `skills/ver-3/ba-synthesizer/data/drc.yaml` | DRC contract |

### 6.2 Files to Update (3 files)

| # | File path | Update |
|:---|:---|:---|
| 1 | `.claude/skills/ba-{elicitor,analyst,synthesizer}/SKILL.md` | Sync từ skills/ver-3/ sau khi author |
| 2 | `skills-registry.json` | Add 3 BA skills entries (`installed`) |
| 3 | `_state.yaml` | Record Phase 5 completion |

### 6.3 Dependency Files (READ-ONLY — consume during authoring)

| File | Usage |
|:---|:---|
| `skills/ver-3/_shared/schemas/elicitation.schema.yaml` | Reference schema for elicitor output |
| `skills/ver-3/_shared/schemas/analysis.schema.yaml` | Reference schema for analyst output |
| `skills/ver-3/_shared/schemas/synthesis.schema.yaml` | Reference schema for synthesizer output |
| `skills/ver-3/_shared/templates/drc_contract_template.yaml` | Base DRC template for each skill |
| `skills/ver-3/_shared/templates/skill_skeleton.md` | SKILL.md structure reference |
| `.claude/agents/quality-scorer.md` | Quality audit dependency |
| `.claude/agents/ba-pipeline-runner.md` | Pipeline orchestration consumer |

---

## §7: Old v0.0.2 Skills Inventory — Knowledge Mining Analysis

> **Phát hiện mới (2026-07-10)**: Bộ 3 skill phiên bản `ver-0.0.2` tại `skills/ver-0.0.2/ba-{elicitor,analyst,synthesizer}` chứa **~1.330 dòng tài liệu** có thể khai thác làm nguyên liệu cho Phase 5, dù cấu trúc và chuẩn chất lượng chưa đạt yêu cầu mới.

### 7.1 Inventory Overview

```yaml
total_inventory:
  ba_elicitor_old: 19 files, ~530 lines
  ba_analyst_old:   7 files, ~465 lines
  ba_synthesizer_old: 6 files, ~332 lines
  grand_total:     ~19 files, ~1,330 lines

zone_coverage_gap:
  # Old skills use ad-hoc structures — NOT compliant with 7-Zone standard
  zones_present: [core/SKILL.md, knowledge/, templates/, loop/, data/]
  zones_missing: [scripts/, assets/]
  # ba-synthesizer has an extra policy/ directory (not in 7-Zone)
```

### 7.2 ba-elicitor (v0.0.2) — Detailed Asset Map

| Old File | Lines | Content Value | Phase 5 Destination | Extractability |
|:---|:---:|:---|:---|:---:|
| `SKILL.md` | 77 | Persona + workflow + guardrails + output contract | `skills/ver-3/ba-elicitor/SKILL.md` (partial) | ⚠️ Body cần rewrite theo L0 anchor; frontmatter pattern tham khảo |
| `knowledge/elicitation-rules.md` | 81 | 3-Layer Master Prompt Architecture, anti-hallucination rules, MECE, Stop Conditions | `knowledge/elicitation_patterns.md` | ✅ **High** — merge với mindset-keywords |
| `knowledge/mindset-keywords.md` | 98 | 6 Critical Thinking Keywords (Systems Thinking, Root Cause, MECE, First Principles, Impact Analysis, Structural Decomposition) + Cognitive Rules | `knowledge/elicitation_patterns.md` | ✅ **High** — content depth tốt, cần restructure |
| `knowledge/normalization-logic.md` | 40 | Normalization flow + NFR quantification rules + trace tags | `knowledge/elicitation_patterns.md` | ✅ **High** — logic chuẩn hóa có thể extract |
| `knowledge/question-framework.md` | 77 | 5W1H framework + 3-path decomposition (Happy/Alternative/Exception) | `knowledge/elicitation_patterns.md` | ✅ **High** — 5W1H reusable nguyên bản |
| `knowledge/scope-definition.md` | 58 | Entry point, I/O contracts, risks, quality checklist | `knowledge/elicitation_patterns.md` | ⚠️ Phần scope definition tham khảo nhưng cần rewrite |
| `loop/elicitor-checklist.md` | 33 | 7 QC criteria (QC-01→07) với weighted scoring + Mermaid flow | `loop/scoping_checklist.md` | ✅ **Direct** — cấu trúc weighted scoring giữ nguyên |
| `templates/elicitation-report.md.template` | 75 | Full output template với trace tags (`[TỪ INPUT]`, `[SUY LUẬN]`, `[CẦN LÀM RÕ]`) | `templates/elicitation_report.template.md` | ✅ **Direct** — cần thêm 5 thought-cache fields |
| `data/input-schema.yaml` | 72 | JSON Schema cho input (skill_name, description, core_objective, actors, environment, constraints, nfr) | `data/drc.yaml` (partial) | ⚠️ Schema fields có thể dùng để thiết kế DRC |

**Tổng giá trị khai thác cho ba-elicitor mới**: ~6/7 files có thể kế thừa hoặc tham khảo; chỉ `scripts/validate_outputs.py` và `templates/thought_cache_template.yaml` là hoàn toàn mới.

### 7.3 ba-analyst (v0.0.2) — Detailed Asset Map

| Old File | Lines | Content Value | Phase 5 Destination | Extractability |
|:---|:---:|:---|:---|:---:|
| `SKILL.md` | 58 | Workflow 7 bước, guardrails, output contract | `skills/ver-3/ba-analyst/SKILL.md` (partial) | ⚠️ Cần rewrite L0; workflow steps tham khảo |
| `knowledge/classification-rules.md` | 89 | FR/NFR definitions + MoSCoW matrix (P0→P3) + Technical Justification examples + Compliance Mindset | `knowledge/fr_nfr_taxonomy.md` | ✅ **High** — nội dung chuẩn, cần restructure taxonomy |
| `knowledge/gherkin-guide.md` | 102 | Gherkin standards, 3-path scenario coverage, quality rules + real example (payment flow) | `knowledge/fr_nfr_taxonomy.md` | ✅ **High** — gherkin rules + example reusable |
| `knowledge/mermaid-syntax.md` | 153 | Mermaid safety rules + 4 diagram types (Sequence, Flowchart, ERD, Use Case) + templates | `knowledge/fr_nfr_taxonomy.md` | ✅ **High** — quy tắc Mermaid đầy đủ nhất |
| `knowledge/risk-assessment.md` | 74 | Risk matrix (Probability × Impact), MoSCoW integration, mitigation examples | `knowledge/fr_nfr_taxonomy.md` | ✅ **Medium** — cần integrate vào taxonomy |
| `loop/analyst-checklist.md` | 72 | 5 Quality Gates (QG-BA-01→05) + 15 execution check items + approval thresholds | `loop/interlock_checklist.md` | ✅ **Direct** — QG gates + execution steps |
| `templates/analysis-report.md.template` | 148 | Full 6-section report (FR/NFR, Mermaid, Data Schema, Gherkin, Risk, Traceability) | `templates/analysis_report.template.md` | ✅ **Direct** — cấu trúc đầy đủ, cần update frontmatter |

**Tổng giá trị khai thác cho ba-analyst mới**: ~5/6 files kế thừa được. **Giàu tài liệu nhất** trong 3 skill cũ — đặc biệt mermaid-syntax.md và gherkin-guide.md là tài liệu tham khảo giá trị cao.

### 7.4 ba-synthesizer (v0.0.2) — Detailed Asset Map

| Old File | Lines | Content Value | Phase 5 Destination | Extractability |
|:---|:---:|:---|:---|:---:|
| `SKILL.md` | 49 | Cross-validation persona, workflow, guardrails, MAU THUẪN example | `skills/ver-3/ba-synthesizer/SKILL.md` (partial) | ⚠️ Cần rewrite L0; cross-ref logic giữ lại |
| `knowledge/cross-ref-rules.md` | 51 | Actor-Entity matching + MoSCoW-Gherkin matching rules + warning tags | `knowledge/cross_validation_strategies.md` | ✅ **Direct** — quy tắc kiểm định chéo đầy đủ |
| `knowledge/quality-criteria.md` | 60 | 7 deliverables weighted scoring (threshold 0.80) + calculation formula | `knowledge/cross_validation_strategies.md` | ✅ **Direct** — weighted matrix giữ nguyên |
| `loop/synthesizer-checklist.md` | 58 | 3 categories: completeness (7 items), validation (5 items), format (2 items) | `loop/congruence_checklist.md` | ✅ **Direct** — 14 items checklist |
| `templates/business-analysis.md.template` | 118 | Handoff YAML frontmatter + 7 deliverables sections + quality score display | `templates/business_analysis_template.md` | ✅ **Direct** — cấu trúc tốt, cần update frontmatter |
| `policy/quality-matrix.yaml` | 45 | YAML implementation of weighted quality matrix (7 deliverables × weights) | `knowledge/cross_validation_strategies.md` (embedded) | ✅ **Direct** — matrix có thể reuse |

**Tổng giá trị khai thác cho ba-synthesizer mới**: ~5/6 files kế thừa được. **Cấu trúc weighted quality scoring** là phát hiện giá trị nhất — có thể tái sử dụng làm cơ sở cho quality-scorer agent integration.

### 7.5 Extraction Quality Assessment

```yaml
extraction_summary:
  total_old_files: 19
  total_old_lines: ~1,330

  reusability_breakdown:
    direct_use:            # Có thể copy-edit nhẹ
      count: 7
      files:
        - "elicitor/loop/elicitor-checklist.md → loop/scoping_checklist.md"
        - "elicitor/templates/elicitation-report.md.template → templates/elicitation_report.template.md"
        - "analyst/loop/analyst-checklist.md → loop/interlock_checklist.md"
        - "analyst/templates/analysis-report.md.template → templates/analysis_report.template.md"
        - "synthesizer/knowledge/cross-ref-rules.md → knowledge/cross_validation_strategies.md"
        - "synthesizer/knowledge/quality-criteria.md → knowledge/cross_validation_strategies.md"
        - "synthesizer/loop/synthesizer-checklist.md → loop/congruence_checklist.md"
      estimated_lines: ~550

    adaptation_needed:     # Cần restructure/merge
      count: 9
      files:
        - "elicitor/knowledge/*.md (5 files) → knowledge/elicitation_patterns.md (1 merged file)"
        - "analyst/knowledge/*.md (4 files) → knowledge/fr_nfr_taxonomy.md (1 merged file)"
        - "synthesizer/templates/business-analysis.md.template → templates/business_analysis_template.md"
        - "synthesizer/policy/quality-matrix.yaml → embedded into knowledge/"
      estimated_lines: ~660

    new_content_needed_entirely:  # Hoàn toàn không có trong old
      count: 6
      items:
        - "skills/ver-3/ba-elicitor/scripts/validate_outputs.py"
        - "skills/ver-3/ba-elicitor/templates/thought_cache_template.yaml"
        - "skills/ver-3/ba-analyst/scripts/validate_metrics.py"
        - "skills/ver-3/ba-synthesizer/scripts/check_congruence.py"
        - "skills/ver-3/*/data/drc.yaml (3 files)"
        - "skills/ver-3/*/assets/* (3 zones)"
      estimated_lines: ~400

  score_estimate:
    coverage: 70%  # ~930/1,330 lines tái sử dụng được
    quality_gap: "Old content chưa đạt chuẩn Phase 5 (thiếu thought-cache, không có META scoring, không có DRC contracts, SKILL.md quá dài). Cần nâng cấp — extract content, restructure format."
```

### 7.6 Key Findings — Why Old Content is Valuable Despite Standards Gap

1. **3-Layer Master Prompt Architecture** (elicitor) — Kiến trúc Mindset → Knowledge → Skills Layer vẫn là thiết kế tốt, có thể reuse làm architecture reference cho SKILL.md mới.

2. **6 Mindset Keywords** (elicitor) — Systems Thinking, Root Cause Isolation, MECE, First Principles, Impact Analysis, Structural Decomposition — đây là tư duy phản biện xuyên suốt pipeline, có thể dùng làm training material.

3. **Mermaid Safety Rules + Gherkin Standards** (analyst) — 153 dòng + 102 dòng quy tắc viết Mermaid/Gherkin là tài liệu tham khảo giá trị nhất trong toàn bộ old skills. Cần giữ nguyên làm knowledge base.

4. **Weighted Quality Matrix** (synthesizer) — `quality-matrix.yaml` với 7 deliverables × weights + threshold 0.80 là cơ chế chấm điểm đã được thiết kế tốt. Có thể reuse làm input cho quality-scorer agent.

5. **Trace Tags Convention** — `[TỪ INPUT]`, `[SUY LUẬN]`, `[CẦN LÀM RÕ]` xuyên suốt cả 3 skills. Đây là semantic anchor nên được giữ lại.

### 7.7 Risks in Old Content Reuse

| # | Risk | Severity | Mitigation |
|:---:|:------|:--------:|:-----------|
| R-O1 | Old content dùng `${VARIABLE}` template syntax — Phase 5 yêu cầu YAML/frontmatter contracts | Medium | Chuyển đổi sang YAML frontmatter + Jinja2-style trong quá trình author |
| R-O2 | Old SKILL.md chứa inline knowledge (không separation of concerns) — mâu thuẫn L0 anchor rule | High | Extract inline knowledge vào knowledge/ zone; SKILL.md giữ ≤700 tokens |
| R-O3 | Old training data focus vào e-commerce/payment examples — không generalize cho all skill types | Low | Generalize examples hoặc giữ làm reference samples |
| R-O4 | content-before-fix skill references đã outdated (thong-tin-mau.md, raw2.md) | Low | Bỏ references không còn tồn tại, giữ nguyên tắc cốt lõi |
| R-O5 | Old output contracts dùng `.skill-context/` paths — consistent với Phase 5 | None | ✅ Không cần sửa |

---

## §8: Pre-Existing State Assessment

### 7.1 Current Artifacts State

| Path | Status | Content |
|:---|:---|:---|
| `skills/ver-3/ba-elicitor/` | 🟡 Scaffold only | 7 empty subdirs, SKILL.md = 0 bytes, all zones = `.gitkeep` |
| `skills/ver-3/ba-analyst/` | 🟡 Scaffold only | 7 empty subdirs, SKILL.md = 0 bytes, all zones = `.gitkeep` |
| `skills/ver-3/ba-synthesizer/` | 🟡 Scaffold only | 7 empty subdirs, SKILL.md = 0 bytes, all zones = `.gitkeep` |
| `.claude/skills/ba-elicitor/SKILL.md` | 🔴 Empty (0 bytes) | Chưa sync |
| `.claude/skills/ba-analyst/SKILL.md` | 🔴 Empty (0 bytes) | Chưa sync |
| `.claude/skills/ba-synthesizer/SKILL.md` | 🔴 Empty (0 bytes) | Chưa sync |
| `.claude/agents/ba-pipeline-runner.md` | ✅ Complete | 198 lines, full definition + hooks |
| `.claude/agents/quality-scorer.md` | ✅ Complete | Deployed, có thể invoke audit |

### 7.2 Phase 4 Dependency Verification (audited 2026-07-10)

| Dependency | Status | Mechanical Verification |
|:---|:---|:---|
| 14 schemas (elicitation, analysis, synthesis...) | ✅ FULL | 0 stub, 0 empty. All yaml.safe_load/json.load pass. AC-1 ✅ |
| schema_validator.py (173 lines) | ✅ Verified | Click CLI, `--all`, `--artifact`, --skills-registry. Valid→exit 0, broken→exit 1. AC-2 ✅ |
| artifact_lifecycle.py (201 lines) | ✅ Verified | Click CLI, SHA-256 drift detection, WORM enforcement, state persistence |
| drc_resolver.py (202 lines) | ✅ Verified | Click CLI, cross-ref contracts vs registry. `--registry-only` → exit 0. AC-5 ✅ |
| DRC template | ✅ Verified | `drc_contract_template.yaml` — 36 lines, 4 sections. yaml.safe_load pass. AC-3 ✅ |
| Skill skeleton | ✅ Verified | `skill_skeleton.md` — 51 lines, 8 XML sections. name + suite fields present. AC-6 ✅ |
| Skill README template | ✅ Verified | `skill_readme_template.md` — 29 lines |
| artifact_registry.yaml | ✅ Verified | 153 lines, 14 entries, all 8 required fields. AC-4 ✅ |
| 28 test fixtures | ✅ Verified | 14 valid + 14 broken. Real test data covering all 14 schemas incl. BA-critical ones |
| karpathy-standards.md | ⚠️ Partial | 87/100 dòng (AC-7 fail). Content quality tốt nhưng chưa đủ dung lượng |
| run_tests.sh | ✅ Verified | Test harness exercising 26 fixtures |

> **Kết luận**: Phase 4 ~94% hoàn thành. AC-1→AC-6 PASS cơ học. AC-7 fail (karpathy 87/100 dòng — minor gap, không block Phase 5). Plan-checklist đã được cập nhật phản ánh trạng thái thực tế.

---

## §9: Evidence

<evidence>
  <file>skills/ver-3/roadmaps/05-skill-build-ba-pipeline.md</file>
  <line>1-10</line>
  <finding>Phase 5 roadmap: build 3 BA skills, effort L, depends Phase 3+4, downstream Phase 6</finding>
</evidence>

<evidence>
  <file>docs/plans/plan-checklist.2026-07-07.md</file>
  <line>510-597</line>
  <finding>Phase 5 checklist: 15 tasks, 9 AC, 6 DoD items, 3 skills × 6-7 files = ~30 files</finding>
</evidence>

<evidence>
  <file>docs/plans/plan-checklist.2026-07-07.md</file>
  <line>53-54</line>
  <finding>Dashboard: Phase 5 status = 🟡 in_progress, 30% complete (note: "3 BA skills đã author ở raw, chưa deploy"). Actual: raw files are EMPTY stubs</finding>
</evidence>

<evidence>
  <file>.claude/agents/ba-pipeline-runner.md</file>
  <line>1-198</line>
  <finding>ba-pipeline-runner agent đã deploy full: instructions, constraints, task seq, output contract, failure modes F1-F6</finding>
</evidence>

<evidence>
  <file>.claude/agents/quality-scorer.md</file>
  <line>1</line>
  <finding>quality-scorer agent available để audit chất lượng skill (META-1→3)</finding>
</evidence>

<evidence>
  <file>skills/ver-3/ba-elicitor/SKILL.md</file>
  <line>1</line>
  <finding>SKILL.md = 0 bytes — cần author content</finding>
</evidence>

<evidence>
  <file>skills/ver-3/ba-analyst/SKILL.md</file>
  <line>1</line>
  <finding>SKILL.md = 0 bytes — cần author content</finding>
</evidence>

<evidence>
  <file>skills/ver-3/ba-synthesizer/SKILL.md</file>
  <line>1</line>
  <finding>SKILL.md = 0 bytes — cần author content</finding>
</evidence>

<evidence>
  <file>skills/ver-3/_shared/schemas/elicitation.schema.yaml</file>
  <line>1-113</line>
  <finding>Full schema: 5 required fields (skill_name, domain_ontology, stakeholder_analysis, nrfs, thought_cache), 3 sub-sections</finding>
</evidence>

<evidence>
  <file>skills/ver-3/_shared/schemas/analysis.schema.yaml</file>
  <line>1-65</line>
  <finding>Full schema: 4 required fields (skill_name, criteria_analysis, metrics, risk_assessment)</finding>
</evidence>

<evidence>
  <file>skills/ver-3/_shared/schemas/synthesis.schema.yaml</file>
  <line>1-57</line>
  <finding>Full schema: 4 required fields (skill_name, synthesized_requirements, congruence_check, pipeline_ready)</finding>
</evidence>

<evidence>
  <file>skills/ver-3/_shared/templates/skill_skeleton.md</file>
  <line>1-51</line>
  <finding>Template cung cấp 11 section structure (frontmatter + 10 XML tags)</finding>
</evidence>

<evidence>
  <file>skills/ver-3/_shared/artifact_registry.yaml</file>
  <line>112-153</line>
  <finding>BA artifact registry: 3 entries (elicitation-report.md, analysis-report.md, business-analysis.md) với schema và consumer paths</finding>
</evidence>

<evidence>
  <file>docs/context-to-work/phase-4-audit/phase4-audit-report.2026-07-10.md</file>
  <line>1-10</line>
  <finding>Phase 4 audit: 5 subagents + CLI cơ học. 14 schemas FULL, 3 scripts production-grade, 28 fixtures. AC-1→6 PASS. ~94% complete.</finding>
</evidence>

<evidence>
  <file>skills/ver-3/_shared/validators/schema_validator.py</file>
  <line>1-173</line>
  <finding>schema_validator.py verified: valid→exit 0, broken→exit 1 trên elicitation, analysis, synthesis fixtures</finding>
</evidence>

<evidence>
  <file>skills/ver-0.0.2/ba-elicitor/SKILL.md</file>
  <line>1-77</line>
  <finding>Old v0.0.2 ba-elicitor: 77 dòng, persona + XML workflow + guardrails. Cấu trúc cũ nhưng chứa 3-Layer Prompt Architecture (Mindset → Knowledge → Skills) có thể reuse</finding>
</evidence>

<evidence>
  <file>skills/ver-0.0.2/ba-elicitor/knowledge/elicitation-rules.md</file>
  <line>1-81</line>
  <finding>3-Layer Master Prompt Architecture: Mindset Layer (phản biện) + Knowledge Layer (BABOK RAG) + Skills Layer (Mermaid/Gherkin). Anti-hallucination rules + MECE decomposition + Stop Conditions</finding>
</evidence>

<evidence>
  <file>skills/ver-0.0.2/ba-elicitor/knowledge/mindset-keywords.md</file>
  <line>1-98</line>
  <finding>6 Mindset Keywords: Systems Thinking, Root Cause Isolation, MECE, First Principles, Impact Analysis, Structural Decomposition. Kèm vector anchors + behavioral impact cho mỗi keyword</finding>
</evidence>

<evidence>
  <file>skills/ver-0.0.2/ba-elicitor/knowledge/question-framework.md</file>
  <line>1-77</line>
  <finding>5W1H framework: 6 question types (Who/What/Why/How/When/Where) với sub-questions + 3-path decomposition (Happy/Alternative/Exception) + interaction format rules</finding>
</evidence>

<evidence>
  <file>skills/ver-0.0.2/ba-elicitor/loop/elicitor-checklist.md</file>
  <line>1-33</line>
  <finding>7 QC criteria với weighted scoring (QC-01→07, mỗi item 10-15% trọng số). Gate policy yêu cầu 100% pass trước khi ghi file. Cấu trúc này reusable cho Phase 5</finding>
</evidence>

<evidence>
  <file>skills/ver-0.0.2/ba-analyst/knowledge/classification-rules.md</file>
  <line>1-89</line>
  <finding>FR/NFR classification rules + MoSCoW matrix (P0→P3) + Technical Justification examples + Compliance Mindset. Đầy đủ definitions và triggers cho mỗi loại</finding>
</evidence>

<evidence>
  <file>skills/ver-0.0.2/ba-analyst/knowledge/mermaid-syntax.md</file>
  <line>1-153</line>
  <finding>Mermaid safety rules + 4 diagram types (Sequence với ≥3 actors, Flowchart 3-path, ERD PK/FK, Use Case). Có templates cho từng loại — tài liệu tham khảo giá trị nhất trong old skills</finding>
</evidence>

<evidence>
  <file>skills/ver-0.0.2/ba-analyst/knowledge/gherkin-guide.md</file>
  <line>1-102</line>
  <finding>Gherkin standards: User Story template, scenario coverage (min 3 scenarios cho 3 paths), quality rules + real payment flow example. Testability và zero-placeholder rules</finding>
</evidence>

<evidence>
  <file>skills/ver-0.0.2/ba-synthesizer/knowledge/cross-ref-rules.md</file>
  <line>1-51</line>
  <finding>2 cross-reference rules: (1) Actor-Entity matching — SD actor vs ERD entity, (2) MoSCoW-Gherkin matching — Must-Have feature phải có scenario test. Warning tags: [MAU THUẪN NGHIỆP VỤ] + [THIẾU KỊCH BẢN KIỂM THỬ]</finding>
</evidence>

<evidence>
  <file>skills/ver-0.0.2/ba-synthesizer/policy/quality-matrix.yaml</file>
  <line>1-45</line>
  <finding>Weighted quality matrix: 7 deliverables (elicitation 0.15, classification 0.15, sequence 0.15, flowchart 0.15, erd 0.15, acceptance 0.15, risk 0.10). Threshold 0.80 PASS. Có thể reuse làm base cho quality-scorer</finding>
</evidence>

<evidence>
  <file>skills/ver-0.0.2/ba-elicitor/data/input-schema.yaml</file>
  <line>1-72</line>
  <finding>JSON Schema input: 4 required fields (skill_name, description, core_objective, actors) + optional (environment, constraints, nfr với performance/security/token_budget). Schema fields có thể dùng thiết kế DRC contract</finding>
</evidence>

---

## §10: Risk Assessment

| # | Risk | Probability | Impact | Mitigation |
|:---|:---|:---:|:---:|:---|
| ~~R1~~ | ~~Phase 4 schemas chưa complete~~ | ~~Medium~~ | ~~High~~ | ❌ **RESOLVED** — Phase 4 audit: 14 schemas FULL, AC-1→6 PASS |
| R2 | quality-scorer chưa được test với BA skills | Medium | Medium | Chạy dry-run quality-scorer trên skill skeleton trước |
| R3 | 7-Zone structure sai đường dẫn (assets vs knowledge confusion) | Low | Medium | Roadmap map rõ: knowledge, scripts, templates, loop, data, assets |
| R4 | Token budget SKILL.md > 700 tokens (L0 anchor violation) | Medium | High | `wc -w` check trong CI loop; roadmap cho phép ≤800 words |
| R5 | deployment conflict — .claude/skills/ đã có dirs nhưng SKILL.md empty | Low | Low | Overwrite bằng sync script (cp -r skills/ver-3/* .claude/skills/) |
| R6 | ba-elicitor thought-cache quality không đạt META-2 depth gate | High | Medium | validate_outputs.py cần check token count mỗi thought block |
| R7 | Mock full pipeline test thất bại vì artifact chain gap | Medium | High | Test từng skill riêng lẻ trước pipeline test |

---

## §11: Confidence Assessment

```yaml
overall_confidence: 91%  # Tăng từ 90% nhờ phát hiện old v0.0.2 content

breakdown:
  scope_completeness: 97%
    # Roadmap spec + plan-checklist + old v0.0.2 inventory (mới) cung cấp 3 góc nhìn đầy đủ
  dependency_readiness: 92%
    # Phase 3 agents ready ✅. Phase 4 đã audit: 14 schemas FULL, AC-1→6 PASS ✅.
    # Chỉ karpathy-standards.md 87/100 (non-blocking).
  artifact_state_accuracy: 100%
    # Verified: skills/ver-3/ba-* = empty stubs, .claude/skills/ba-* = 0 bytes
    # Old v0.0.2 skills = ~1,330 lines content available to mine
  effort_estimation_confidence: 85%
    # Từ 82% lên 85%: có sẵn ~930/1,330 lines old content tái sử dụng được → giảm effort author từ scratch.
    # Vẫn cần ~400 lines script/DRC/thought-cache mới.
    # quality-scorer strictness chưa rõ.

uncertainty_flags:
  - "quality-scorer agent threshold ≥70% — chưa biết strictness level. Có thể cần nhiều iteration fix."
  - "AC-8 (quality gatekeeper) marked NEEDED_MANUAL — không auto-verify được; cần invoke thủ công."
  - "skills-registry.json schema field (Phase 4 Task 12) chưa verify — minor, trong step 0 pre-verify."
  - "Old v0.0.2 content quality gap: content hay nhưng format chưa đạt chuẩn Phase 5. Cần restructure, không copy nguyên."
```

---

## §12: Open Questions

| # | Question | Priority | Liên quan | Status |
|:---:|:----------|:--------:|:---------:|:------|
| 1 | Phase 4 đã thực sự complete chưa? | 🔴 ~~High~~ | ~~Execution block~~ | ✅ **RESOLVED 2026-07-10** — Audit: ~94% done, 14 schemas FULL, AC-1→6 PASS, chỉ AC-7 fail (karpathy 87/100 — non-blocking). Plan-checklist updated. |
| 2 | quality-scorer agent có invoke được từ task() prompt không? | 🟡 Medium | AC-8 | 🔄 Test invoke với mock skill skeleton trước Phase 5 |
| 3 | SKILL.md ≤ 700 tokens — dùng `wc -w` hay `wc -c`? | 🟢 Low | AC-3 | ✅ **Confirmed**: Dùng `wc -w` ≤ 800 per roadmap |
| 4 | `_state.yaml` hiện tại ở đâu? | 🟡 Medium | Task 14 | 🔄 Cần xác định path format |
| 5 | skills-registry.json hiện tại có entries gì? | 🟡 Medium | Task 13 | 🔄 Đọc và verify trước khi add BA entries |
| 6 | Old v0.0.2 content extract strategy: copy-edit hay rewrite từ concept? | 🟡 Medium | §7 | 🔄 **Phân tích**: 7 files direct-use (copy-edit nhẹ), 9 files adaptation-needed (restructure/merge). Cần quyết định: (A) Copy từ old + edit → nhanh nhưng rủi ro giữ lại lỗi cũ. (B) Rewrite từ concepts → chậm nhưng chất lượng đồng đều. **Recommend A cho templates/loop, B cho knowledge/ vì cần restructure taxonomy**. |

---

## §13: Implementation Sequence Recommendation

```yaml
recommended_build_order:
  phase: "Build + Verify interleaved, không bulk-build rồi mới verify"
  rationale: "Mỗi skill build xong → test ngay → fix → move next. Tránh tích lũy failure."

  step_0_pre_verify:
    - Verify Phase 4 schemas content (chạy schema_validator.py)
    - Verify quality-scorer agent invoke-able
    - Verify .claude/skills/ba-* empty state
    - Read skills-registry.json và _state.yaml format
    - **[NEW] Mine old v0.0.2 skills** — Đọc và extract tất cả nội dung từ `skills/ver-0.0.2/ba-{elicitor,analyst,synthesizer}/` làm nguyên liệu author; phân loại direct-use (copy-edit) vs adaptation-needed (restructure/merge)
  
  step_1_build_ba_elicitor:
    - Author SKILL.md (frontmatter + 8 XML sections)
    - Author knowledge/elicitation_patterns.md
    - Author templates/ x2 (report + thought-cache)
    - Author loop/scoping_checklist.md
    - Author scripts/validate_outputs.py
    - Author data/drc.yaml
    - Run local validator → fix
    - Invoke quality-scorer → fix ≥70%
    - Test với mock request → verify elicitation-report.md + thought-cache.yaml
  
  step_2_build_ba_analyst:
    - Author SKILL.md
    - Author knowledge/fr_nfr_taxonomy.md
    - Author templates/analysis_report.template.md
    - Author loop/interlock_checklist.md
    - Author scripts/validate_metrics.py
    - Author data/drc.yaml
    - quality-scorer audit → fix ≥70%
    - Test với elicitation-report từ Step 1 → verify analysis-report.md
  
  step_3_build_ba_synthesizer:
    - Author SKILL.md
    - Author knowledge/cross_validation_strategies.md
    - Author templates/business_analysis_template.md
    - Author loop/congruence_checklist.md
    - Author scripts/check_congruence.py
    - Author data/drc.yaml
    - quality-scorer audit → fix ≥70%
    - Test với cả 2 artifacts từ Step 1+2 → verify business-analysis.md
  
  step_4_pipeline_test:
    - Invoke ba-pipeline-runner với mock feature
    - Verify _ba_pipeline_state.yaml lifecycle
    - Verify full artifact chain (3 files)
  
  step_5_deploy:
    - Sync skills/ver-3/ba-* → .claude/skills/ba-*
    - Update skills-registry.json
    - Update _state.yaml
    - Run AC-1 đến AC-9
    - Commit: `phase-5: ba pipeline complete`
```

---

## §14: Acceptance Criteria Map

| AC | Mô tả | Verification method | Auto/Manual |
|:---:|:------|:-------------------|:-----------:|
| AC-1 | 3 skills deploy tại `.claude/skills/` | `test -f .claude/skills/*/SKILL.md` | Auto |
| AC-2 | Frontmatter 10 fields hợp lệ | Python yaml.safe_load + field check | Auto |
| AC-3 | SKILL.md ≤ 700 tokens (≤800 words) | `wc -w` | Auto |
| AC-4 | 7-Zone ≥4 zones populate | `ls` per zone | Auto |
| AC-5 | DRC files parse + reference schemas | Python yaml.safe_load | Auto |
| AC-6 | Mock invoke ba-elicitor — artifacts ≥1000 bytes | `wc -c` + schema validate | Auto |
| AC-7 | Mock full BA pipeline — business-analysis.md tồn tại | `test -f` | Auto |
| AC-8 | Aggregate gatekeeper ≥70% score | Invoke quality-scorer agent | Manual |
| AC-9 | ba-pipeline-runner chain 3 skills | pipeline test | Manual |
| DoD | Full verification (6 items) | Checklist | Mixed |

---

**Document Status**: Context Complete — No Code Changes Made
**Document Path**: `docs/context-to-work/phase-5-ba-pipeline/scope.2026-07-10.md`

```
✓ Scope Context Document Complete (Updated 2026-07-10 — Phase 4 audit + Old v0.0.2 mining)
✓ Entry point identified: roadmap 05 + plan-checklist §10
✓ Current state assessed: skills/ver-3 empty stubs, .claude/skills empty
✓ Dependency analysis: Phase 3 done ✅ | Phase 4 ~94% ✅ (audited)
✓ Impact analysis: 19 files create, 3 files update
✓ Call chain mapped: build seq + runtime seq
✓ Old v0.0.2 inventory completed: 19 files, ~1,330 lines, ~930 lines reusable
✓ Knowledge extraction mapped: 7 direct-use + 9 adaptation-needed + 6 new-only
✓ Evidence traced: 24 evidence blocks with specific file:line (+11 old skills blocks)
✓ Implementation sequence recommended: 6-step (step 0 updated: old skills mining)
✓ Confidence assessment: 91% (up from 90% — old content availability reduces risk)
✓ Open questions: 6 items (1 resolved, 5 open — new extraction strategy question)
```

**NO CODE CHANGES — Context ready for fix/deploy phase**
