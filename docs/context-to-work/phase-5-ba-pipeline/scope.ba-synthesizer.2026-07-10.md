# Scope Document — ba-synthesizer Skill (Phase 5 Sub-scope)

**Date**: 2026-07-10
**Status**: Initial — Context Discovery
**Feature**: `ba-synthesizer` (Phase 5: BA Skills Pipeline)
**Skill**: context-before-fix v1.0.0
**Parent Scope**: `docs/context-to-work/phase-5-ba-pipeline/scope.2026-07-10.md`

**Source Documents**:
- `docs/context-to-work/phase-5-ba-pipeline/scope.2026-07-10.md` (parent scope, 758 dòng)
- `docs/plans/plan-checklist.2026-07-07.md` §10 (Phase 5 checklist)
- `skills/ver-3/ba-synthesizer/` (7-Zone scaffold — hiện tại empty)
- `.claude/skills/ba-synthesizer/` (runtime — hiện tại empty)
- `.agents/skills/ba-synthesizer/SKILL.md` (old v0.0.2 runtime, 49 dòng)
- `skills/ver-0.0.2/ba-synthesizer/` (old v0.0.2 source — 5 files, ~332 dòng)
- `skills/ver-3/_shared/schemas/synthesis.schema.yaml` (57 dòng)
- `skills/ver-3/_shared/schemas/elicitation.schema.yaml` (113 dòng)
- `skills/ver-3/_shared/schemas/analysis.schema.yaml` (65 dòng)
- `skills/ver-3/_shared/templates/skill_skeleton.md` (51 dòng)
- `skills/ver-3/_shared/templates/drc_contract_template.yaml` (36 dòng)
- `skills/ver-3/_shared/artifact_registry.yaml` (153 dòng)
- `.claude/agents/ba-pipeline-runner.md` (198 dòng)
- `.claude/agents/quality-scorer.md`

---

## §1: Problem Summary

Xây dựng skill `ba-synthesizer` (Stage BA-0.2) — skill thứ 3 và **cuối cùng** trong BA Skills Pipeline. Skill này chịu trách nhiệm **hợp nhất và kiểm định chéo** output từ `ba-elicitor` (elicitation-report.md) và `ba-analyst` (analysis-report.md) để tạo ra `business-analysis.md` — artifact đầu vào bắt buộc cho Phase 6 (skill-explorer).

**Vai trò trong Pipeline**:
```
ba-elicitor → elicitation-report.md
    ↓
ba-analyst → analysis-report.md
    ↓
ba-synthesizer → business-analysis.md [★ PHASE 6 INPUT]
    ↓
skill-explorer (Phase 6)
```

**Mục tiêu build**:
1. Author 6 files theo 7-Zone structure (SKILL.md, knowledge/, templates/, loop/, scripts/, data/)
2. Pass quality-scorer audit ≥70% (META-1→3)
3. Tích hợp đúng artifact chain với 2 skill upstream
4. Deploy từ `skills/ver-3/ba-synthesizer/` → `.claude/skills/ba-synthesizer/`

---

## §2: Entry Point

| Thuộc tính | Giá trị |
|:---|:---|
| **Roadmap spec** | `skills/ver-3/roadmaps/05-skill-build-ba-pipeline.md` § ba-synthesizer |
| **Plan checklist** | `docs/plans/plan-checklist.2026-07-07.md` lines 556-558 (Tasks 8-10) |
| **Parent scope** | `docs/context-to-work/phase-5-ba-pipeline/scope.2026-07-10.md` §6.1 (ba-synthesizer: 6 files) |
| **Staging path** | `skills/ver-3/ba-synthesizer/` (7 zones, empty — chỉ .gitkeep) |
| **Runtime path** | `.claude/skills/ba-synthesizer/` (7 zones, empty — chỉ .gitkeep) |
| **Old source** | `skills/ver-0.0.2/ba-synthesizer/` (5 files, ~332 dòng) |
| **Pipeline consumer** | `.claude/agents/ba-pipeline-runner.md` lines 70-72 (Stage 3) |

---

## §3: Scope Definition

### 3.1 In Scope (6 files = 6 deliverables)

| # | File | Zone | Content Type | Source Material |
|:---:|:---|:---:|:---|:---|
| D5-3-1 | `SKILL.md` | core | Frontmatter + 8 XML sections | `skill_skeleton.md` + old `SKILL.md` (49 dòng) |
| D5-3-2 | `knowledge/cross_validation_strategies.md` | knowledge | 2 cross-ref rules + weighted quality matrix + trace tags | old `cross-ref-rules.md` (51 dòng) + old `quality-criteria.md` (60 dòng) + old `quality-matrix.yaml` (45 dòng) |
| D5-3-3 | `templates/business_analysis_template.md` | templates | YAML frontmatter + 7 deliverables + quality score | old `business-analysis.md.template` (118 dòng) |
| D5-3-4 | `loop/congruence_checklist.md` | loop | 14-item checklist (3 categories) | old `synthesizer-checklist.md` (58 dòng) |
| D5-3-5 | `scripts/check_congruence.py` | scripts | Python validator — congruence checker | **Mới hoàn toàn** (no old source) |
| D5-3-6 | `data/drc.yaml` | data | DRC contract | `drc_contract_template.yaml` (36 dòng) |

### 3.2 Out of Scope

```yaml
- Không build/author 2 skill upstream (ba-elicitor, ba-analyst) — đã có scope riêng
- Không quality-scorer audit (sẽ thực hiện sau khi build — Task 9)
- Không pipeline test (Task 11 — full pipeline)
- Không deploy (Task 12 — deploy cả 3 skills cùng lúc)
- Không update skills-registry.json hoặc _state.yaml
- Không sửa shared schemas (Phase 4 đã complete)
- Không sửa ba-pipeline-runner agent
```

### 3.3 Boundary — Input/Output Contract

```yaml
inputs:
  - artifact: ".skill-context/{feature}/ba-elicitor/elicitation-report.md"
    schema: "skills/ver-3/_shared/schemas/elicitation.schema.yaml"
    required: true
    format: markdown
    consumed_fields:
      - skill_name, domain_ontology, stakeholder_analysis, nrfs, thought_cache

  - artifact: ".skill-context/{feature}/ba-analyst/analysis-report.md"
    schema: "skills/ver-3/_shared/schemas/analysis.schema.yaml"
    required: true
    format: markdown
    consumed_fields:
      - skill_name, criteria_analysis, metrics, risk_assessment

  - artifact: ".skill-context/{feature}/thought-cache.yaml" (optional)
    format: yaml
    required: false  # Optional read từ ba-elicitor

outputs:
  - artifact: ".skill-context/{feature}/ba-synthesizer/business-analysis.md"
    schema: "skills/ver-3/_shared/schemas/synthesis.schema.yaml"
    format: markdown
    lifecycle: WORM
    required_fields:
      - skill_name, synthesized_requirements, congruence_check, pipeline_ready

upstream_skills:
  - ba-elicitor (Stage BA-1)
  - ba-analyst (Stage BA-0.5)

downstream_consumers:
  - skill-explorer (Phase 6A) — business-analysis.md là input direct
  - scs-router (Phase 6A) — tham khảo

write_zone:
  - ".skill-context/{feature}/ba-synthesizer/" — chỉ ghi vào zone này
  - "data/drc.yaml" — DRC contract tại staging area
```

---

## §4: Impact Analysis

### 4.1 Direct Impact

| Thành phần | Tác động | Mức độ | Evidence |
|:---|:---|:---:|:---|
| `skills/ver-3/ba-synthesizer/SKILL.md` | Author content (hiện 0 bytes) | 🔴 Tạo mới | `[file:skills/ver-3/ba-synthesizer/SKILL.md:1]` |
| `skills/ver-3/ba-synthesizer/knowledge/cross_validation_strategies.md` | Author từ old sources | 🔴 Tạo mới | `[file:skills/ver-3/ba-synthesizer/knowledge/.gitkeep]` |
| `skills/ver-3/ba-synthesizer/templates/business_analysis_template.md` | Author từ old template | 🔴 Tạo mới | `[file:skills/ver-3/ba-synthesizer/templates/.gitkeep]` |
| `skills/ver-3/ba-synthesizer/loop/congruence_checklist.md` | Author từ old checklist | 🔴 Tạo mới | `[file:skills/ver-3/ba-synthesizer/loop/.gitkeep]` |
| `skills/ver-3/ba-synthesizer/scripts/check_congruence.py` | Author mới hoàn toàn | 🔴 Tạo mới | `[file:skills/ver-3/ba-synthesizer/scripts/.gitkeep]` |
| `skills/ver-3/ba-synthesizer/data/drc.yaml` | Author từ DRC template | 🔴 Tạo mới | `[file:skills/ver-3/ba-synthesizer/data/.gitkeep]` |
| `.claude/skills/ba-synthesizer/SKILL.md` | Sync từ ver-3 sau deploy | 🟡 Overwrite | `[file:.claude/skills/ba-synthesizer/SKILL.md:1]` (0 bytes) |

### 4.2 Indirect Impact

| Thành phần | Tác động | Lý do |
|:---|:---|:---|
| `ba-pipeline-runner` agent | Stage 3 phụ thuộc vào ba-synthesizer | Pipeline orchestrator gọi skill này (lines 70-72) |
| `quality-scorer` agent | Được invoke audit (Task 9) | Resource contention, cần đảm bảo ≥70% |
| Phase 6 `skill-explorer` | business-analysis.md là input trực tiếp | Data dependency chain |
| Phase 6 `scs-router` | Tham khảo business-analysis.md | Data dependency |
| `schema_validator.py` | Validate synthesis output artifacts | Quality gate |
| `skills-registry.json` | Cần add entry sau deploy | Registry update |

### 4.3 Data Flow — Chi tiết

```yaml
INPUT LAYER (read-only):
  .skill-context/{feature}/ba-elicitor/elicitation-report.md:
    - domain_ontology.terms → actor-entity matching
    - domain_ontology.relationships → entity relationship check
    - stakeholder_analysis → stakeholder coverage validation
    - thought_cache → optional reflection

  .skill-context/{feature}/ba-analyst/analysis-report.md:
    - criteria_analysis → FR/NFR classification check
    - metrics → MoSCoW-Gherkin matching
    - risk_assessment → risk matrix completeness

PROCESSING LAYER:
  [Cross-Validation Engine]
    ├── Actor-Entity Matching (SD participants vs ERD entities)
    ├── MoSCoW-Gherkin Matching (Must-Have features vs Gherkin scenarios)
    ├── Quality Score Calculation (7 deliverables × weights)
    └── Congruence Check (pass/fail verdict)

OUTPUT LAYER (write-only → WORM):
  .skill-context/{feature}/ba-synthesizer/business-analysis.md:
    - skill_handoff: frontmatter (target_skill, scs, quality_score)
    - §1: Cross-Reference Validation Results (actor-entity + moscow-gherkin)
    - §2: Consolidated 7 Deliverables (synthesized)
    - §3: Quality Score Assessment (weighted + verdict)
    - §4: Pipeline Readiness Flag
```

---

## §5: Call Chain

### 5.1 Build Sequence (trong Phase 5 execution)

```text
[Pre-condition] ba-elicitor + ba-analyst đã build & test PASS
    ↓
Task 8: Author ba-synthesizer (D5-3-1→D5-3-6)
  ├── 8a: Author SKILL.md (frontmatter + 8 XML sections) → reference skill_skeleton.md
  ├── 8b: Author knowledge/cross_validation_strategies.md → merge old 3 files
  ├── 8c: Author templates/business_analysis_template.md → adapt old template
  ├── 8d: Author loop/congruence_checklist.md → adapt old checklist
  ├── 8e: Author scripts/check_congruence.py → NEW (Python)
  └── 8f: Author data/drc.yaml → adapt DRC template
    ↓
Task 9: Invoke quality-scorer audit ba-synthesizer → fix ≥70%
    ↓
Task 10: Test với output từ Task 4 + 7 → verify business-analysis.md
    ↓  (validate with synthesis.schema.yaml)
[Post-condition] Ready cho pipeline test (Task 11)
```

### 5.2 Runtime Chain (khi skill được invoke)

```text
ba-pipeline-runner (orchestrator)
    │
    ├── Gate check: analysis-report.md tồn tại
    │
    ▼
ba-synthesizer invoked via Task
    │
    ├── 1. Read: elicitation-report.md (ba-elicitor output)
    ├── 2. Read: analysis-report.md (ba-analyst output)
    ├── 3. Optional: thought-cache.yaml (ba-elicitor)
    │
    ├── 4. CROSS-VALIDATION PHASE:
    │   ├── 4a. Actor-Entity Matching
    │   │   ├── Extract actors/participants từ SD Mermaid
    │   │   ├── Extract entities từ ERD Mermaid
    │   │   └── Compare → [MAU THUẪN NGHIỆP VỤ] nếu mismatch
    │   │
    │   ├── 4b. MoSCoW-Gherkin Matching
    │   │   ├── Extract Must-Have features từ MoSCoW matrix
    │   │   ├── Extract Gherkin scenarios
    │   │   └── Compare → [THIẾU KỊCH BẢN KIỂM THỬ] nếu thiếu
    │   │
    │   └── 4c. Quality Score Calculation
    │       ├── Score 7 deliverables (0.0-1.0 each)
    │       ├── Weighted sum (threshold 0.80)
    │       └── Verdict: PASS / WARNING
    │
    ├── 5. SYNTHESIS PHASE:
    │   ├── Merge elicitation + analysis → unified requirements
    │   ├── Embed cross-validation results
    │   └── Attach quality score
    │
    ├── 6. VERIFICATION PHASE:
    │   ├── Run congruence checklist (14 items)
    │   ├── Validate against synthesis.schema.yaml
    │   └── Check no placeholders (TODO/TBD/mock/...)
    │
    └── 7. OUTPUT: Write business-analysis.md
        └── Gate: ba-pipeline-runner kiểm tra file tồn tại
```

---

## §6: Affected Components

### 6.1 Files to Create (6 files)

#### D5-3-1: `SKILL.md` (core)

| Thuộc tính | Giá trị |
|:---|:---|
| **Format** | YAML frontmatter (10 fields) + 8 XML sections |
| **Frontmatter fields required** | name, description, suite, version, category, stage, target_variable, tags, when_to_use, output_contract |
| **XML sections required** | instructions, safety_contract, knowledge_anchors, workflow_phases, input_contract, output_contract, acceptance_criteria, failure_modes |
| **Token limit** | ≤700 tokens (≤800 words per AC-3) |
| **Source** | `skill_skeleton.md` template + old `SKILL.md` (49 dòng) |
| **Old content value** | ⚠️ Partial — workflow steps, guardrails có thể tham khảo; cần rewrite L0 |

#### D5-3-2: `knowledge/cross_validation_strategies.md` (knowledge)

| Thuộc tính | Giá trị |
|:---|:---|
| **Format** | Markdown with YAML code blocks |
| **Sections required** | Actor-Entity matching rules, MoSCoW-Gherkin matching rules, quality criteria (7 deliverables × weights), trace tags convention |
| **Old sources to merge (3 files)** | |
| ① `cross-ref-rules.md` (51 dòng) | ✅ **Direct use** — 2 cross-ref rules (actor-entity matching, moscow-gherkin matching), warning tags: [MAU THUẪN NGHIỆP VỤ], [THIẾU KỊCH BẢN KIỂM THỬ] |
| ② `quality-criteria.md` (60 dòng) | ✅ **Direct use** — 7 deliverables weighted scoring, pass threshold 0.80, weighted_sum calculation |
| ③ `quality-matrix.yaml` (45 dòng) | ✅ **Embed** — YAML matrix (7 deliverables × weights) có thể nhúng làm code block |
| **Output**: 1 merged file | Khoảng 100-120 dòng |

#### D5-3-3: `templates/business_analysis_template.md` (templates)

| Thuộc tính | Giá trị |
|:---|:---|
| **Format** | Markdown với YAML frontmatter + 7 deliverables sections |
| **Old source** | `business-analysis.md.template` (118 dòng) |
| **Extractability** | ✅ **Direct use** — cần cập nhật frontmatter theo synthesis schema |
| **Frontmatter fields** | skill_name, version, scs_complexity_score, decomposition_recommended, sub_skills_proposed, scope_boundary (in/out), technical_frameworks, detected_risks, quality_gate_status, quality_score_percentage |
| **Sections** | §1 Cross-Reference Validation (actor-entity + moscow-gherkin), §2 Quality Score Assessment (7 deliverables weighted), §3 Consolidated Requirements, §4 Pipeline Ready flag |
| **Khoảng** | 80-100 dòng |

#### D5-3-4: `loop/congruence_checklist.md` (loop)

| Thuộc tính | Giá trị |
|:---|:---|
| **Format** | Markdown with YAML code blocks |
| **Old source** | `synthesizer-checklist.md` (58 dòng) |
| **Extractability** | ✅ **Direct use** — 14 items, 3 categories |
| **Categories** | completeness_check (7 items: CHK_DEL_01→07), validation_and_integrity (5 items: CHK_VAL_01→05), format_and_cleanliness (2 items: CHK_FMT_01→02) |
| **Pass rule** | All completeness + format items must pass before write |
| **Khoảng** | 50-60 dòng |

#### D5-3-5: `scripts/check_congruence.py` (scripts) — **MỚI HOÀN TOÀN**

| Thuộc tính | Giá trị |
|:---|:---|
| **Format** | Python script (Click CLI) |
| **Old source** | ❌ **Không có** — phải viết mới |
| **Chức năng** | Cross-artifact congruence checker: validate business-analysis.md vs synthesis.schema.yaml |
| **Input** | business-analysis.md path, [optional] --schema path |
| **Validation criteria** | (a) YAML frontmatter parse hợp lệ, (b) 4 required fields present, (c) synthesized_requirements array valid, (d) congruence_check object valid (conflicts_found, conflicts_resolved, check_verdict), (e) pipeline_ready boolean |
| **Exit codes** | 0 = PASS (valid), 1 = FAIL (invalid) |
| **Reference** | `schema_validator.py` (173 dòng, verified) — pattern: Click CLI + yaml.safe_load + field check |
| **Khoảng** | ~80-100 dòng |
| **Recommendation** | Follow pattern của `schema_validator.py`: Click CLI, --artifact flag, yaml.safe_load, structured field validation |

#### D5-3-6: `data/drc.yaml` (data)

| Thuộc tính | Giá trị |
|:---|:---|
| **Format** | YAML (per DRC contract template) |
| **Source** | `drc_contract_template.yaml` (36 dòng) |
| **Fields cần điền** | skill_name (ba-synthesizer), inputs (elicitation-report.md + analysis-report.md + thought-cache.yaml), outputs (business-analysis.md), routing (upstream: ba-elicitor, ba-analyst; downstream: skill-explorer, scs-router), state_persistence (context_bus_write, state_yaml_write) |
| **Khoảng** | 30-40 dòng |

### 6.2 Files to Update (after build complete — out of scope for this sub-scope)

| File | Update | Timing |
|:---|:---|:---:|
| `.claude/skills/ba-synthesizer/SKILL.md` | Sync từ ver-3 | Task 12 (deploy) |
| `skills-registry.json` | Add ba-synthesizer entry | Task 13 |
| `_state.yaml` | Record Phase 5 completion | Task 14 |

### 6.3 Dependency Files (READ-ONLY — consume during authoring)

| File | Usage |
|:---|:---|
| `skills/ver-3/_shared/schemas/synthesis.schema.yaml` (57 dòng) | **Required** — output schema reference cho business-analysis.md |
| `skills/ver-3/_shared/schemas/elicitation.schema.yaml` (113 dòng) | **Reference** — input schema để hiểu upstream data structure |
| `skills/ver-3/_shared/schemas/analysis.schema.yaml` (65 dòng) | **Reference** — input schema để hiểu upstream data structure |
| `skills/ver-3/_shared/templates/skill_skeleton.md` (51 dòng) | **Required** — SKILL.md structure template |
| `skills/ver-3/_shared/templates/drc_contract_template.yaml` (36 dòng) | **Required** — DRC contract template |
| `skills/ver-3/_shared/artifact_registry.yaml` lines 133-142 | **Reference** — synthesis artifact definition |
| `.claude/agents/ba-pipeline-runner.md` lines 70-72, 130-132 | **Required** — consumer interface: output path, format |
| `skills/ver-3/_shared/validators/schema_validator.py` (173 dòng) | **Reference pattern** — Click CLI validator structure cho check_congruence.py |

---

## §7: Old v0.0.2 Asset Mining Analysis — Cụ thể cho ba-synthesizer

### 7.1 Inventory

| Old File | Lines | Giá trị | Phase 5 Destination | Extract Strategy |
|:---|:---:|:---|:---|:---:|
| `SKILL.md` | 49 | Persona + workflow + guardrails + MAU THUẪN example | `SKILL.md` | ⚠️ **Adapt** — workflow steps và guardrails tham khảo; cần rewrite theo L0 anchor + 8 XML sections |
| `knowledge/cross-ref-rules.md` | 51 | Actor-Entity matching (3 steps) + MoSCoW-Gherkin matching (3 steps) + 3 warning tags | `knowledge/cross_validation_strategies.md` | ✅ **Direct merge** — giữ nguyên rules, merge với quality-criteria.md + quality-matrix.yaml |
| `knowledge/quality-criteria.md` | 60 | 7 deliverables weighted scoring (0.15×5 + 0.10×1), threshold 0.80, calculation formula | `knowledge/cross_validation_strategies.md` | ✅ **Direct merge** — giữ nguyên weighted matrix |
| `loop/synthesizer-checklist.md` | 58 | 14 items (3 categories: completeness 7, validation 5, format 2) | `loop/congruence_checklist.md` | ✅ **Direct** — giữ nguyên cấu trúc 3 categories |
| `templates/business-analysis.md.template` | 118 | Full output template: frontmatter + 7 deliverables + quality score + risk matrix | `templates/business_analysis_template.md` | ✅ **Direct** — cập nhật frontmatter per synthesis schema |
| `policy/quality-matrix.yaml` | 45 | YAML implementation quality matrix (7 deliverables × weights) | → Embed vào `knowledge/cross_validation_strategies.md` | ✅ **Embed** — nhúng làm code block |

### 7.2 Extraction Tổng hợp

```yaml
total_old_lines: ~332  (5 files)
reusable_lines: ~280   (~84% — cao nhất trong 3 skills)
new_lines_needed: ~150 (check_congruence.py ~80-100 + SKILL.md rewrite ~50 + drc.yaml ~30-40)

extraction_breakdown:
  direct_use (copy-edit nhẹ):
    - loop/synthesizer-checklist.md → loop/congruence_checklist.md
    - templates/business-analysis.md.template → templates/business_analysis_template.md
    - knowledge/cross-ref-rules.md → merged into knowledge/cross_validation_strategies.md
    - knowledge/quality-criteria.md → merged into knowledge/cross_validation_strategies.md
    - policy/quality-matrix.yaml → embedded into knowledge/cross_validation_strategies.md
    estimated_lines: ~274

  adaptation_needed (restructure):
    - old SKILL.md (49 dòng) → new SKILL.md (cần rewrite format)
    estimated_lines: ~49 (rewrite ~50 dòng)

  new_content (no old source):
    - scripts/check_congruence.py
    - data/drc.yaml
    estimated_lines: ~120-140

score_estimate:
  coverage: 84%
  quality_gap: "Old content quality tốt nhất trong 3 skills — weighted quality matrix là phát hiện giá trị. Cần restructure knowledge/ thành 1 file merged và viết scripts mới."
```

### 7.3 Key Findings từ Old Content

1. **Weighted Quality Matrix** (quality-matrix.yaml + quality-criteria.md) — Cơ chế chấm điểm 7 deliverables × weights với threshold 0.80 là thiết kế đã hoàn chỉnh. Có thể sử dụng nguyên bản, chỉ cần restructure vào file knowledge chung.

2. **2 Cross-Reference Rules** (cross-ref-rules.md) — Actor-Entity matching (sequence diagram vs ERD) và MoSCoW-Gherkin matching (Must-Have vs scenario coverage) là 2 quy tắc kiểm định chéo đầy đủ. Warning tags [MAU THUẪN NGHIỆP VỤ] và [THIẾU KỊCH BẢN KIỂM THỬ] là semantic anchors cần giữ.

3. **14-item Checklist** (synthesizer-checklist.md) — 3 categories (completeness 7, validation 5, format 2) với CHK_xxx ID conventions. Có thể sử dụng nguyên bản, cần update minor references.

4. **Template Structure** (business-analysis.md.template) — Frontmatter + 7 deliverables + quality score. Cấu trúc đầy đủ, cần update frontmatter fields để match synthesis schema và thêm field `pipeline_ready`.

### 7.4 Risks in Old Content Reuse (cụ thể cho ba-synthesizer)

| # | Risk | Severity | Mitigation |
|:---:|:------|:--------:|:-----------|
| R-S1 | Old quality matrix chỉ tính 7 deliverables. Phase 5 synthesis schema yêu cầu `synthesized_requirements`, `congruence_check`, `pipeline_ready` — khác với 7 deliverables model | Medium | Map 7 deliverables vào `synthesized_requirements[]` với `source: both`. `congruence_check` và `pipeline_ready` là fields mới cần thêm vào template |
| R-S2 | old template uses `{{VARIABLE}}` syntax → Phase 5 yêu cầu YAML frontmatter | Medium | Chuyển sang YAML frontmatter + Jinja2-style hoặc placeholders với chú thích |
| R-S3 | Old cross-ref rules chỉ cover 2 loại matching (actor-entity, moscow-gherkin). Phase 5 congruence_check cần thêm `conflicts_found` + `conflicts_resolved` + `check_verdict` | Low | Thêm 3 fields vào template phía dưới phần matching results |
| R-S4 | check_congruence.py không có old source — phải viết từ đầu mà không có reference implementation | Low | Tham khảo pattern từ schema_validator.py (đã verified: Click CLI + yaml.safe_load) |
| R-S5 | Old quality-criteria.md dùng threshold 0.80. Synthesis schema không specify threshold — có thể conflict với quality-scorer agent threshold (70%) | Medium | Dùng threshold 0.80 cho internal scoring (giữ nguyên old), quality-scorer dùng threshold 70% riêng |

---

## §8: Pre-Existing State Assessment

### 8.1 Current Artifacts

| Path | Status | Content |
|:---|:---|:---|
| `skills/ver-3/ba-synthesizer/` (7 zones) | 🟡 Scaffold | SKILL.md = 0 bytes, tất cả zones = .gitkeep |
| `.claude/skills/ba-synthesizer/` (7 zones) | 🟡 Scaffold | SKILL.md = 0 bytes, tất cả zones = .gitkeep |
| `.agents/skills/ba-synthesizer/SKILL.md` | ✅ Old v0.0.2 | 49 dòng, format cũ (không dùng runtime) |
| `skills/ver-0.0.2/ba-synthesizer/` (5 files) | ✅ Old source | ~332 dòng, available để mine |

### 8.2 Dependency Readiness

| Dependency | Status | Notes |
|:---|:---:|:---|
| `skills/ver-3/_shared/schemas/synthesis.schema.yaml` | ✅ Complete | 57 dòng, 4 required fields |
| `skills/ver-3/_shared/schemas/elicitation.schema.yaml` | ✅ Complete | 113 dòng, 5 required fields (upstream input) |
| `skills/ver-3/_shared/schemas/analysis.schema.yaml` | ✅ Complete | 65 dòng, 4 required fields (upstream input) |
| `skills/ver-3/_shared/templates/skill_skeleton.md` | ✅ Complete | 51 dòng, 8 XML sections |
| `skills/ver-3/_shared/templates/drc_contract_template.yaml` | ✅ Complete | 36 dòng, 4 sections |
| `skills/ver-3/_shared/artifact_registry.yaml` | ✅ Complete | synthesis artifact defined at lines 133-142 |
| `.claude/agents/ba-pipeline-runner.md` | ✅ Complete | Stage 3 definition at lines 70-72 |
| `skills/ver-3/_shared/validators/schema_validator.py` | ✅ Complete | 173 dòng, verified — pattern reference cho check_congruence.py |
| `skills/ver-0.0.2/ba-synthesizer/` | ✅ Available | 5 files, ~332 dòng, ~84% reusable |
| ba-elicitor + ba-analyst (upstream) | 🟡 In progress | Build trước ba-synthesizer trong sequence |

---

## §9: Build Specifications Chi tiết

### 9.1 SKILL.md Specification

```yaml
frontmatter:
  name: "ba-synthesizer"
  description: "Hợp nhất và kiểm định chéo báo cáo BA."
  suite: "WASHVN"
  version: "0.0.1"
  category: "general"
  stage: 0
  target_variable: "feature_name"
  tags: ["ba", "synthesis", "cross-validation", "quality-gate"]
  when_to_use: "Khi cần hợp nhất và kiểm định chéo output từ ba-elicitor và ba-analyst"
  output_contract: "skills/ver-3/_shared/templates/drc_contract_template.yaml"

xml_sections:
  - instructions      # Core logic: cross-validation → quality scoring → synthesis
  - safety_contract   # Token limit, WORM write enforcement, no placeholder rule
  - knowledge_anchors # References: cross_validation_strategies.md, synthesis schema
  - workflow_phases   # 7-phase workflow (read → cross-validate → score → synthesize → verify → output)
  - input_contract    # 2 required artifacts + 1 optional
  - output_contract   # business-analysis.md, WORM, schema validation required
  - acceptance_criteria  # 14-item checklist + schema validation pass
  - failure_modes     # Missing artifact, schema validation fail, quality score < threshold

token_budget: ≤700 tokens (≤800 words per AC-3)
```

### 9.2 check_congruence.py Specification

```yaml
language: Python
framework: Click CLI (pattern: schema_validator.py)
file_name: check_congruence.py

interface:
  command: python check_congruence.py --artifact <path> [--schema <path>]

validation_checks:
  - Check 1: YAML frontmatter parse
  - Check 2: 4 required fields present
    - skill_name (string, kebab-case)
    - synthesized_requirements (array, each item có req_id, title, description, source, classification)
    - congruence_check (object, có conflicts_found, conflicts_resolved, check_verdict)
    - pipeline_ready (boolean)
  - Check 3: synthesized_requirements[].source ∈ [elicitation, analysis, both]
  - Check 4: synthesized_requirements[].classification ∈ [FR, NFR]
  - Check 5: congruence_check.check_verdict ∈ [PASS, FAIL]
  - Check 6: pipeline_ready is boolean

exit_codes:
  0: PASS (all checks pass)
  1: FAIL (any check fails)

output:
  - Human-readable validation report (stdout)
  - Exit code (for CI/script integration)

estimated_lines: 80-100
```

### 9.3 business_analysis_template.md Specification

```yaml
frontmatter_fields:
  required:
    - skill_name: string
    - target_skill: string
    - scs_complexity_score: number (0-10)
    - quality_gate_status: enum [PASS, WARNING]
    - quality_score_percentage: number (0-100)
    - pipeline_ready: boolean
  optional:
    - decomposition_recommended: boolean
    - sub_skills_proposed: string[]
    - scope_boundary: { in_scope: string[], out_scope: string[] }
    - detected_risks: string[]

sections:
  §1: Cross-Reference Validation Results
    1A: Actor-Entity Matching (status + warning)
    1B: MoSCoW-Gherkin Matching (status + warning)
    1C: Congruence Check Verdict (conflicts_found, conflicts_resolved, check_verdict)

  §2: Quality Score Assessment
    2A: 7 deliverables individual scores
    2B: Weighted sum calculation
    2C: Quality gate verdict (PASS ≥ 80%, WARNING < 80%)

  §3: Consolidated Requirements
    Merged từ elicitation + analysis, deduplicated, cross-referenced

  §4: Pipeline Readiness
    pipeline_ready flag + conditions met / blockers list
```

### 9.4 data/drc.yaml Specification

```yaml
skill_name: "ba-synthesizer"
skill_version: "0.0.1"
suite: "WASHVN"
last_updated: "2026-07-10"

inputs:
  - name: "elicitation-report"
    path_template: ".skill-context/{target_skill}/ba-elicitor/elicitation-report.md"
    format: "markdown"
    schema: "skills/ver-3/_shared/schemas/elicitation.schema.yaml"
    required: true
    consumed_by: "ba-synthesizer"
    downstream_phase: "phase-5"

  - name: "analysis-report"
    path_template: ".skill-context/{target_skill}/ba-analyst/analysis-report.md"
    format: "markdown"
    schema: "skills/ver-3/_shared/schemas/analysis.schema.yaml"
    required: true
    consumed_by: "ba-synthesizer"
    downstream_phase: "phase-5"

  - name: "thought-cache"
    path_template: ".skill-context/{target_skill}/ba-elicitor/thought-cache.yaml"
    format: "yaml"
    schema: null
    required: false
    consumed_by: "ba-synthesizer"
    downstream_phase: "phase-5"

outputs:
  - file_id: "synthesis_report"
    path_template: ".skill-context/{skill_name}/ba-synthesizer/business-analysis.md"
    format: "markdown"
    schema: "skills/ver-3/_shared/schemas/synthesis.schema.yaml"
    lifecycle_status: "WORM"
    versioning: "semver"

routing:
  upstream_skills: ["ba-elicitor", "ba-analyst"]
  downstream_skills: ["skill-explorer", "scs-router"]
  fallback_targets:
    - trigger: "validation_fail"
      target_skill: "fallback-escalation"
      target_stage: "escalate"

state_persistence:
  context_bus_write: true
  state_yaml_write: true
  fields_to_write:
    - "quality_gate_status"
    - "pipeline_ready"
    - "congruence_check_verdict"
```

---

## §10: Authoring Sequence Recommendation

```yaml
recommended_order:
  - "Build D5-3-6 (data/drc.yaml) first — nhanh, ít effort, xác định contract trước"
  - "Build D5-3-2 (knowledge/cross_validation_strategies.md) — merge 3 old files, content core"
  - "Build D5-3-3 (templates/business_analysis_template.md) — adapt old template"
  - "Build D5-3-4 (loop/congruence_checklist.md) — adapt old checklist"
  - "Build D5-3-1 (SKILL.md) — cần biết knowledge + templates + loop trước khi viết"
  - "Build D5-3-5 (scripts/check_congruence.py) — cuối cùng, dễ test với template đã có"

rationale: "DRC first → contract rõ ràng. Knowledge + templates + loop → content layer. SKILL.md → core, cần context từ các layer khác. Script → cuối, dễ test nhất."
```

---

## §11: Quality Gate Map

```yaml
internal_validation:
  - check_congruence.py run PASS (exit 0)
  - 14-item congruence checklist ALL pass
  - No placeholders (TODO/TBD/mock/...)

external_validation:
  - quality-scorer audit ≥70% (META-1→3)
  - synthesis.schema.yaml validation PASS
  - artifact_registry.yaml contract verified

acceptance_criteria (from parent scope):
  AC-2: Frontmatter 10 fields hợp lệ
  AC-3: SKILL.md ≤ 700 tokens (≤800 words)
  AC-4: 7-Zone ≥4 zones populate (knowledge, scripts, templates, loop, data)
  AC-5: DRC files parse + reference synthesis schema
  AC-6/7: pipeline test with ba-elicitor + ba-analyst artifacts
```

---

## §12: Evidence

<evidence>
  <file>docs/context-to-work/phase-5-ba-pipeline/scope.2026-07-10.md</file>
  <line>249-257</line>
  <finding>Parent scope defines 6 files for ba-synthesizer (D5-3-1→D5-3-6)</finding>
</evidence>

<evidence>
  <file>docs/plans/plan-checklist.2026-07-07.md</file>
  <line>556-558</line>
  <finding>Tasks 8-10: build ba-synthesizer, quality audit, test với upstream output</finding>
</evidence>

<evidence>
  <file>docs/plans/plan-checklist.2026-07-07.md</file>
  <line>585-591</line>
  <finding>ba-synthesizer deliverables: 6 files checklist items</finding>
</evidence>

<evidence>
  <file>skills/ver-3/_shared/schemas/synthesis.schema.yaml</file>
  <line>1-57</line>
  <finding>Output schema: 4 required fields (skill_name, synthesized_requirements, congruence_check, pipeline_ready)</finding>
</evidence>

<evidence>
  <file>skills/ver-3/_shared/templates/skill_skeleton.md</file>
  <line>1-51</line>
  <finding>SKILL.md template: frontmatter 10 fields + 8 XML sections</finding>
</evidence>

<evidence>
  <file>skills/ver-3/_shared/templates/drc_contract_template.yaml</file>
  <line>1-36</line>
  <finding>DRC contract template: 4 sections (inputs, outputs, routing, state_persistence)</finding>
</evidence>

<evidence>
  <file>skills/ver-3/_shared/artifact_registry.yaml</file>
  <line>133-142</line>
  <finding>synthesis_report artifact: business-analysis.md, path template, consumed_by skill-explorer + scs-router</finding>
</evidence>

<evidence>
  <file>.claude/agents/ba-pipeline-runner.md</file>
  <line>70-72</line>
  <finding>Stage 3 — Invoke ba-synthesizer, gate: business-analysis.md tồn tại</finding>
</evidence>

<evidence>
  <file>.claude/agents/ba-pipeline-runner.md</file>
  <line>130-132</line>
  <finding>Output artifact: .skill-context/{feature}/ba-synthesizer/business-analysis.md, format: markdown</finding>
</evidence>

<evidence>
  <file>skills/ver-3/ba-synthesizer/SKILL.md</file>
  <line>1</line>
  <finding>SKILL.md = 0 bytes — cần author content</finding>
</evidence>

<evidence>
  <file>skills/ver-0.0.2/ba-synthesizer/SKILL.md</file>
  <line>1-49</line>
  <finding>Old SKILL.md: 49 dòng, workflow + guardrails, có thể tham khảo</finding>
</evidence>

<evidence>
  <file>skills/ver-0.0.2/ba-synthesizer/knowledge/cross-ref-rules.md</file>
  <line>1-51</line>
  <finding>2 cross-ref rules: actor-entity matching + moscow-gherkin matching, 3 warning tags</finding>
</evidence>

<evidence>
  <file>skills/ver-0.0.2/ba-synthesizer/knowledge/quality-criteria.md</file>
  <line>1-60</line>
  <finding>7 deliverables weighted scoring: threshold 0.80, weighted_sum calculation, min_criteria per deliverable</finding>
</evidence>

<evidence>
  <file>skills/ver-0.0.2/ba-synthesizer/policy/quality-matrix.yaml</file>
  <line>1-45</line>
  <finding>Quality matrix: weights (0.15×6 + 0.10×1), min_criteria per deliverable</finding>
</evidence>

<evidence>
  <file>skills/ver-0.0.2/ba-synthesizer/templates/business-analysis.md.template</file>
  <line>1-118</line>
  <finding>Full template: frontmatter + 7 deliverables + quality score + risk matrix. Cần update frontmatter per synthesis schema</finding>
</evidence>

<evidence>
  <file>skills/ver-0.0.2/ba-synthesizer/loop/synthesizer-checklist.md</file>
  <line>1-58</line>
  <finding>14-item checklist: completeness 7 items, validation 5 items, format 2 items. Pass all completeness + format before write</finding>
</evidence>

<evidence>
  <file>.agents/skills/ba-synthesizer/SKILL.md</file>
  <line>1-49</line>
  <finding>Runtime old SKILL.md: 49 dòng, hiện không dùng cho ver-3. Có thể tham khảo workflow steps</finding>
</evidence>

---

## §13: Confidence Assessment

```yaml
overall_confidence: 88%

breakdown:
  scope_completeness: 95%
    # Parent scope (758 dòng) + plan-checklist + 6 old files (~332 dòng) đã đọc full
    # Tất cả 6 deliverables đã được map chi tiết
  dependency_readiness: 90%
    # Synthesis schema FULL ✅, skill skeleton ✅, DRC template ✅, pipeline-runner ✅
    # quality-scorer strictness chưa rõ (uncertainty flag)
  artifact_state_accuracy: 100%
    # Verified: ver-3 = empty stubs, old v0.0.2 = ~332 dòng available
  extraction_quality: 85%
    # ~84% old content reusable. Weighted quality matrix là phát hiện giá trị
    # check_congruence.py là mới hoàn toàn — phải viết từ đầu
  effort_estimation: 80%
    # ~150 dòng mới + ~280 dòng copy-edit. Tổng ~430 dòng cho 6 files
    # quality-scorer strictness có thể require nhiều iteration fix

uncertainty_flags:
  - "quality-scorer agent threshold ≥70% — chưa biết strictness level với BA skills"
  - "check_congruence.py không có old source — phải viết mới, pattern tham khảo từ schema_validator.py"
  - "AC-8 (quality gatekeeper) marked NEEDED_MANUAL — không auto-verify được"
```

---

## §14: Open Questions

| # | Question | Priority | Status |
|:---:|:----------|:--------:|:------:|
| 1 | quality-scorer agent có invoke được từ task() prompt cho ba-synthesizer không? | 🟡 Medium | 🔄 Cần test invoke với draft skill |
| 2 | check_congruence.py nên dùng --artifact flag hay nhận input từ stdin? | 🟢 Low | **Recommend**: follow schema_validator.py pattern (--artifact path) |
| 3 | `assets/.gitkeep` có cần nội dung gì không? (7-Zone rule yêu cầu ≥4 zones populate) | 🟢 Low | AC-4 chỉ yêu cầu 5 zones (knowledge, scripts, templates, loop, data). assets có thể để .gitkeep |
| 4 | Old quality matrix threshold 0.80 có conflict với quality-scorer 70% không? | 🟡 Medium | Nội bộ dùng 0.80, quality-scorer dùng 70% riêng — không conflict |
| 5 | Template business_analysis_template.md nên dùng `{{variable}}` (Jinja2) hay YAML frontmatter? | 🟢 Low | **Recommend**: YAML frontmatter cho structured fields + `{{variable}}` cho inline content placeholders |

---

## §15: Summary — Context cho Build Phase

```yaml
scope: "ba-synthesizer sub-scope (Phase 5, Stage BA-0.2)"
total_files_to_create: 6
total_estimated_lines: ~430

old_content_reuse:
  direct_use: ~274 dòng (loop, templates, knowledge)
  adaptation: ~49 dòng (SKILL.md)
  new_content: ~120-140 dòng (scripts + drc)

key_design_decisions:
  - "Merge 3 old knowledge files (cross-ref-rules.md + quality-criteria.md + quality-matrix.yaml) → 1 file cross_validation_strategies.md"
  - "check_congruence.py follow schema_validator.py pattern: Click CLI + yaml.safe_load"
  - "Template frontmatter update: thêm congruence_check + pipeline_ready fields per synthesis schema"
  - "DRC contract: 2 required inputs + 1 optional (thought-cache)"

critical_path_dependencies:
  - ba-elicitor + ba-analyst must exist before ba-synthesizer can be tested (Task 10)
  - synthesis.schema.yaml (✅ ready)
  - DRC template (✅ ready)
  - skill_skeleton.md (✅ ready)

build_sequence: drc.yaml → knowledge → template → loop → SKILL.md → check_congruence.py
```

---

**Document Status**: Context Complete — No Code Changes Made
**Document Path**: `docs/context-to-work/phase-5-ba-pipeline/scope.ba-synthesizer.2026-07-10.md`

```
✓ Problem Summary: ba-synthesizer là skill thứ 3 trong BA pipeline, output business-analysis.md
✓ Entry Point: 6 deliverables (D5-3-1→D5-3-6) tại skills/ver-3/ba-synthesizer/
✓ Scope Definition: 6 files in scope, input/output contracts mapped chi tiết
✓ Impact Analysis: 6 direct + 5 indirect components mapped
✓ Call Chain: build sequence + runtime sequence (7-phase) mapped chi tiết
✓ Data Flow: input layer → processing layer (3 engines) → output layer
✓ Affected Components: 6 create + 3 update + 7 dependency files
✓ Old Asset Mining: 5 files (~332 dòng), ~84% reusable
✓ Build Specifications: SKILL.md spec, check_congruence.py spec, template spec, DRC spec
✓ Authoring Sequence: DRC first → knowledge → templates → loop → SKILL.md → scripts
✓ Quality Gate Map: internal + external validation criteria
✓ Evidence: 17 evidence blocks with specific file:line
✓ Confidence Assessment: 88% — high confidence
✓ Open Questions: 5 items
```

**NO CODE CHANGES — Context ready for build phase**
