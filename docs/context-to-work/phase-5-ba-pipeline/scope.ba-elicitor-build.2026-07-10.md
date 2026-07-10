# Scope Document — Build ba-elicitor Skill (Phase 5, Part 1/3)

**Date**: 2026-07-10
**Status**: Initial
**Skill**: context-before-fix v1.0.0
**Feature**: ba-elicitor build (Phase 5 — BA Pipeline)
**Context Source**: `docs/context-to-work/phase-5-ba-pipeline/scope.2026-07-10.md`

---

## §1: Problem Summary

Xây dựng skill `ba-elicitor` phiên bản ver-3 với 7-Zone structure, là skill đầu tiên trong BA Pipeline (elicitor → analyst → synthesizer). Skill này chịu trách nhiệm khơi gợi (elicit), chuẩn hóa yêu cầu nghiệp vụ thô từ người dùng và lượng hóa NFR.

**Mục tiêu:**
1. Author 7 files content cho `skills/ver-3/ba-elicitor/` (hiện tại là empty scaffold)
2. Skill phải pass quality-scorer ≥70% (META-1→3 criteria)
3. Test với mock request: `"I need an e-commerce skill for selling Vietnamese handcrafted goods internationally"`
4. Deploy từ `skills/ver-3/` → `.claude/skills/`

## §2: Entry Point

- **Scope master document**: `docs/context-to-work/phase-5-ba-pipeline/scope.2026-07-10.md` (758 dòng)
- **Roadmap spec**: `skills/ver-3/roadmaps/05-skill-build-ba-pipeline.md`
- **Plan checklist**: `docs/plans/plan-checklist.2026-07-07.md` §10 (Phase 5, lines 510-597)
- **Skill skeleton template**: `skills/ver-3/_shared/templates/skill_skeleton.md` (51 dòng, 11 section)
- **DRC template**: `skills/ver-3/_shared/templates/drc_contract_template.yaml` (36 dòng, 4 sections)
- **Elicitation schema**: `skills/ver-3/_shared/schemas/elicitation.schema.yaml` (113 dòng, 5 required fields)
- **Old v0.0.2 legacy source**: `skills/ver-0.0.2/ba-elicitor/` (7 files, ~530 dòng — nguồn khai thác knowledge)

## §3: Scope Definition

### 3.1 In Scope

```yaml
in_scope:
  build_sk_md: "Author skills/ver-3/ba-elicitor/SKILL.md theo skill_skeleton.md (frontmatter + 8 XML sections)"
  build_knowledge: "Author knowledge/elicitation_patterns.md — merge từ 5 old knowledge files"
  build_template_report: "Author templates/elicitation_report.template.md (adapt từ old template)"
  build_template_thought_cache: "Author templates/thought_cache_template.yaml (5-section thought-cache) ← NEW"
  build_loop: "Author loop/scoping_checklist.md (adapt từ old elicitor-checklist.md)"
  build_scripts: "Author scripts/validate_outputs.py (8 criteria Python validator) ← NEW"
  build_drc: "Author data/drc.yaml theo drc_contract_template.yaml"
  assets: "assets/ giữ .gitkeep (không cần content)"
  quality_audit: "Chạy quality-scorer audit → fix ≥70%"
  mock_test: "Test với mock request, verify elicitation-report.md + thought-cache.yaml"
  deploy: "Sync skills/ver-3/ba-elicitor/ → .claude/skills/ba-elicitor/"
```

### 3.2 Out of Scope

```yaml
out_of_scope:
  - Không build ba-analyst hay ba-synthesizer (Phase 5 Part 2 và 3)
  - Không test full BA pipeline (chỉ test riêng ba-elicitor)
  - Không update skills-registry.json (làm sau khi build cả 3 skills)
  - Không update _state.yaml (làm sau khi build cả 3 skills)
  - Không fix architectural defects ngoài skill boundary
  - Không migrate knowleages/ → knowledge/ (deferred toàn bộ dự án)
```

### 3.3 Boundary

```yaml
boundary:
  upstream_dependencies:
    - Phase 3: ba-pipeline-runner agent ✅ deployed (tại .claude/agents/ba-pipeline-runner.md — 198 lines)
    - Phase 3: quality-scorer agent ✅ deployed (tại .claude/agents/quality-scorer.md — 233 lines)
    - Phase 4: elicitation.schema.yaml ✅ FULL (skills/ver-3/_shared/schemas/elicitation.schema.yaml — 113 lines)
    - Phase 4: skill_skeleton.md ✅ tồn tại (skills/ver-3/_shared/templates/skill_skeleton.md — 51 lines)
    - Phase 4: drc_contract_template.yaml ✅ tồn tại (skills/ver-3/_shared/templates/drc_contract_template.yaml — 36 lines)
    - Phase 4: schema_validator.py ✅ validated (skills/ver-3/_shared/validators/schema_validator.py — 173 lines)
    - Phase 4: artifact_registry.yaml ✅ có BA entry (skills/ver-3/_shared/artifact_registry.yaml lines 112-153)
    - Phase 0: 7-Zone scaffold ✅ tồn tại (skills/ver-3/ba-elicitor/ — 7 empty subdirs)

  downstream_dependency:
    - ba-analyst (Phase 5 Part 2) — cần elicitation-report.md làm input
    - ba-pipeline-runner — dispatch ba-elicitor ở Stage 1

  artifact_zone:
    - Write: .skill-context/{feature_name}/ba-elicitor/elicitation-report.md
    - Write: .skill-context/{feature_name}/ba-elicitor/thought-cache.yaml
    - Reference: .claude/skills/ba-elicitor/SKILL.md (runtime target)
```

---

## §4: Impact Analysis

### 4.1 Direct Impact

| Thành phần | Trạng thái hiện tại | Tác động | Mức độ |
|:---|:---|:---|:---:|
| `skills/ver-3/ba-elicitor/SKILL.md` | Empty (0 bytes) | Author 51+ dòng theo skill_skeleton.md | 🔴 Tạo mới |
| `skills/ver-3/ba-elicitor/knowledge/` | `.gitkeep` duy nhất | Author `elicitation_patterns.md` (~120-150 dòng, merge từ 5 old files) | 🔴 Tạo mới |
| `skills/ver-3/ba-elicitor/templates/elicitation_report.template.md` | `.gitkeep` duy nhất | Author template (~75-90 dòng, adapt từ old) | 🔴 Tạo mới |
| `skills/ver-3/ba-elicitor/templates/thought_cache_template.yaml` | `.gitkeep` duy nhất | Author mới (~40-50 dòng, 5-section thought-cache) | 🔴 Tạo mới |
| `skills/ver-3/ba-elicitor/loop/scoping_checklist.md` | `.gitkeep` duy nhất | Author (~33-40 dòng, adapt từ old weighted scoring) | 🔴 Tạo mới |
| `skills/ver-3/ba-elicitor/scripts/validate_outputs.py` | `.gitkeep` duy nhất | Author mới (~80-120 dòng Python, 8 criteria) | 🔴 Tạo mới |
| `skills/ver-3/ba-elicitor/data/drc.yaml` | `.gitkeep` duy nhất | Author theo drc_contract_template.yaml (~30-36 dòng) | 🔴 Tạo mới |
| `skills/ver-3/ba-elicitor/assets/` | `.gitkeep` | Giữ nguyên (no content needed) | 🟢 Không đổi |
| `.claude/skills/ba-elicitor/SKILL.md` | Empty (0 bytes) | Sync từ skills/ver-3/ sau khi author | 🟡 Overwrite |

### 4.2 Indirect Impact

| Thành phần | Tác động | Lý do |
|:---|:---|:---|
| `ba-pipeline-runner` agent (F1 failure mode) | Pipeline Stage 1 sẽ fail nếu ba-elicitor chưa build | Runtime dependency |
| `ba-analyst` skill | Cần `elicitation-report.md` làm input cho phân tích | Data dependency |
| `quality-scorer` agent | Được invoke để audit chất lượng SKILL.md | Resource contention |
| `schema_validator.py` | Validate output artifact (elicitation-report.md) | Quality gate |
| Old v0.0.2 `skills/ver-0.0.2/ba-elicitor/` | ~~Có thể xóa sau khi migrate~~ → Giữ lại làm reference | Knowledge preservation |

### 4.3 Data Flow

```text
Input: raw user request (text/XML trong <user_skill_request>)
  ↓
[ba-elicitor] — Workflow 4 phases:
  Phase 1: Normalization (lọc nhiễu, bóc tách thực thể)
  Phase 2: Gap Analysis (6 mindset keywords, anti-hallucination)
  Phase 3: 5W1H Questioning (multiple-choice, 3-path decomposition)
  Phase 4: Self-verification (7 QC criteria, weighted scoring)
  ↓
Output artifacts:
  → .skill-context/{feature}/ba-elicitor/elicitation-report.md  (YAML frontmatter + 6 sections)
  → .skill-context/{feature}/ba-elicitor/thought-cache.yaml      (5-section reasoning trace)
  ↓
Next: ba-analyst consumes elicitation-report.md làm input
```

### 4.4 API Contracts

- **Elicitation schema**: `skills/ver-3/_shared/schemas/elicitation.schema.yaml` — 5 required fields: `skill_name`, `domain_ontology` (terms + relationships), `stakeholder_analysis` (role/goals/pain_points), `nrfs` (id/category/metric/value/unit), `thought_cache` (business_thought_process/stakeholder_empathy/reverse_questions)
- **Skill skeleton**: `skills/ver-3/_shared/templates/skill_skeleton.md` — 11 XML section template (frontmatter + instructions, safety_contract, knowledge_anchors, workflow_phases, input_contract, output_contract, acceptance_criteria, failure_modes)
- **DRC template**: `skills/ver-3/_shared/templates/drc_contract_template.yaml` — 4 sections: inputs, outputs, routing, state_persistence
- **Artifact registry**: `skills/ver-3/_shared/artifact_registry.yaml` lines 112-153 — BA artifact paths (elicitation-report.md → `.skill-context/{feature}/ba-elicitor/elicitation-report.md`)

---

## §5: Call Chain

### 5.1 Build Sequence (cho riêng ba-elicitor)

```text
Step 1: Author data/drc.yaml (đơn giản nhất, theo template)
  → yaml.safe_load verify
  ↓
Step 2: Author templates/thought_cache_template.yaml (mới hoàn toàn, 5-section)
  → yaml.safe_load verify
  ↓
Step 3: Author templates/elicitation_report.template.md (adapt từ old, cần update frontmatter)
  → So khớp với elicitation.schema.yaml
  ↓
Step 4: Author loop/scoping_checklist.md (adapt từ old, giữ weighted scoring)
  → Verify 7 QC criteria format
  ↓
Step 5: Author knowledge/elicitation_patterns.md (MERGE từ 5 old files — phức tạp nhất)
  → Extract từ: elicitation-rules.md + mindset-keywords.md + normalization-logic.md
    + question-framework.md + scope-definition.md
  ↓
Step 6: Author SKILL.md (theo skill_skeleton.md + old SKILL.md làm reference)
  → Frontmatter 10 fields + 8 XML sections
  → wc -w ≤ 800 (per roadmap AC-3)
  ↓
Step 7: Author scripts/validate_outputs.py (mới hoàn toàn, 8 criteria)
  → Python syntax verify
  ↓
Step 8: Run local validator (schema_validator.py)
  → Fix lỗi nếu có
  ↓
Step 9: Invoke quality-scorer agent → audit META-1→3
  → Fix đến ≥70%
  ↓
Step 10: Test với mock request
  → "I need an e-commerce skill for selling Vietnamese handcrafted goods internationally"
  → Verify elicitation-report.md (≥1000 bytes per AC-6)
  → Verify thought-cache.yaml (tồn tại + parse được)
  ↓
Step 11: Deploy .claude/skills/ba-elicitor/SKILL.md
  → cp skills/ver-3/ba-elicitor/SKILL.md .claude/skills/ba-elicitor/SKILL.md
```

### 5.2 Runtime Chain (khi skill được invoke)

```text
User/ba-pipeline-runner → Task invoke ba-elicitor
  ↓
Skill boot: nạp SKILL.md → knowledge/elicitation_patterns.md → loop/scoping_checklist.md
  ↓
Phase 1: Normalization
  - XML boundary enforcement (<user_skill_request>)
  - Khử nhiễu, bóc tách thực thể
  - Map vào input schema fields
  ↓
Phase 2: Gap Analysis
  - Kích hoạt 6 mindset keywords (Systems Thinking, Root Cause, MECE, First Principles, Impact Analysis, Structural Decomposition)
  - Anti-hallucination check
  - NFR quantification (từ mơ hồ → metrics)
  ↓
Phase 3: 5W1H Questioning
  - Multiple-choice question generation
  - 3-path decomposition (Happy/Alternative/Exception)
  ↓
Phase 4: Report Generation
  - Self-verification qua 7 QC criteria (weighted scoring)
  - Gate: 100% pass → ghi file, else quay lại Phase 3
  ↓
Output: elicitation-report.md + thought-cache.yaml
```

---

## §6: Affected Components

### 6.1 Files to Create (7 files + deploy target)

| # | File path | Content type | Estimated LOC | Từ old v0.0.2? |
|:---:|:---|:---|:---:|:---:|
| 1 | `skills/ver-3/ba-elicitor/SKILL.md` | Core skill (frontmatter + 8 XML sections) | ~60-80 | ⚠️ Tham khảo (cần rewrite theo skill_skeleton.md) |
| 2 | `skills/ver-3/ba-elicitor/knowledge/elicitation_patterns.md` | 4+ elicitation patterns (merged knowledge) | ~120-150 | ✅ Merge từ 5 old files (~354 dòng) |
| 3 | `skills/ver-3/ba-elicitor/templates/elicitation_report.template.md` | Output template YAML frontmatter + 6 sections | ~75-90 | ✅ Adapt từ old (75 dòng) |
| 4 | `skills/ver-3/ba-elicitor/templates/thought_cache_template.yaml` | 5-section thought-cache schema | ~40-50 | 🔴 Hoàn toàn mới |
| 5 | `skills/ver-3/ba-elicitor/loop/scoping_checklist.md` | Self-verification checklist (weighted scoring) | ~33-40 | ✅ Adapt từ old (33 dòng) |
| 6 | `skills/ver-3/ba-elicitor/scripts/validate_outputs.py` | Python validator (8 criteria) | ~80-120 | 🔴 Hoàn toàn mới |
| 7 | `skills/ver-3/ba-elicitor/data/drc.yaml` | DRC contract | ~30-36 | 🔴 Mới (theo template) |
| — | `assets/.gitkeep` | Giữ nguyên | 0 | 🟢 Giữ |
| — | `.claude/skills/ba-elicitor/SKILL.md` | Deploy target (sync) | ~60-80 | 🟡 Overwrite |

### 6.2 Files to Reference (READ-ONLY)

| File path | Usage | Dòng quan trọng |
|:---|:---|:---:|
| `skills/ver-3/_shared/templates/skill_skeleton.md` | Template cho SKILL.md structure | Lines 1-51 (11 XML sections) |
| `skills/ver-3/_shared/templates/drc_contract_template.yaml` | Template cho data/drc.yaml | Lines 1-36 (4 sections) |
| `skills/ver-3/_shared/schemas/elicitation.schema.yaml` | Validate output format | Lines 1-113 (5 required fields) |
| `skills/ver-3/_shared/artifact_registry.yaml` | Xác nhận artifact path | Lines 112-153 (BA entries) |
| `skills/ver-3/_shared/validators/schema_validator.py` | Run local validation sau build | Lines 1-173 |
| `.claude/agents/quality-scorer.md` | Quality audit sau build | Lines 1-233 |
| `docs/context-to-work/phase-5-ba-pipeline/scope.2026-07-10.md` | Scope master (knowledge mining map) | §7.2 (ba-elicitor asset map, lines 301-315) |

### 6.3 Old v0.0.2 Files — Knowledge Mining Map (chi tiết)

| Old file (v0.0.2) | Lines | Content | Chiến lược extract | Destination (ver-3) |
|:---|:---:|:---|:---|:---|
| `SKILL.md` | 77 | Persona + workflow + guardrails + output contract | **Tham khảo**: frontmatter fields, 3-Layer Architecture concept, execution_policies, guardrails. Cần rewrite theo skill_skeleton.md (8 XML sections). Old dùng YAML custom tags không chuẩn với skeleton. | `SKILL.md` — partial reference |
| `knowledge/elicitation-rules.md` | 81 | 3-Layer Master Prompt Architecture + anti-hallucination rules + stop conditions + 3-layer mapping table | **Merge** vào elicitation_patterns.md. Giữ nguyên: 3-Layer Arch, anti-hallucination rules, stop conditions, MECE decomposition. Bỏ: outdated references (thong-tin-mau.md). | `knowledge/elicitation_patterns.md` — §Elicitation Rules |
| `knowledge/mindset-keywords.md` | 98 | 6 Mindset Keywords (Systems Thinking, Root Cause, MECE, First Principles, Impact Analysis, Structural Decomposition) + Cognitive Rules | **Merge** vào elicitation_patterns.md. Giữ nguyên: 6 vector anchors + behavioral_impact. Bỏ: outdated source references. Cognitive Rules consolidate với anti-hallucination từ elicitation-rules.md. | `knowledge/elicitation_patterns.md` — §6 Mindset Keywords |
| `knowledge/normalization-logic.md` | 40 | Normalization flow + NFR quantification + trace tags | **Merge** vào elicitation_patterns.md. Giữ nguyên: Skills Flow, Input Normalization steps, NFR quantification mapping, trace tags convention. Là logic cốt lõi cho workflow Phase 1. | `knowledge/elicitation_patterns.md` — §Normalization Logic |
| `knowledge/question-framework.md` | 77 | 5W1H framework + 3-path decomposition + interaction format | **Merge** vào elicitation_patterns.md. Giữ nguyên: 6 question types, sub-questions, 3-path decomposition rules, multiple-choice format. | `knowledge/elicitation_patterns.md` — §5W1H Framework |
| `knowledge/scope-definition.md` | 58 | Entry point + I/O contracts + dependencies + handoff + risks | **Merge** vào elicitation_patterns.md (tinh gọn). Phần scope definition, handoff, risks tham khảo. Output contract cần align với elicitation.schema.yaml. | `knowledge/elicitation_patterns.md` — §Scope & Handoff |
| `loop/elicitor-checklist.md` | 33 | 7 QC criteria weighted scoring (QC-01→07) + Mermaid flow | **Direct use** (copy-edit). Giữ: 7 QC criteria, 15% weights mỗi item, gate policy 100%. Update: thêm thought-cache check (QC-08?), đổi tên thành scoping_checklist.md. | `loop/scoping_checklist.md` |
| `templates/elicitation-report.md.template` | 75 | Full output template với YAML frontmatter + 6 sections + trace tags | **Adaptation**: Giữ frontmatter structure + 6 sections + trace tags. Update: ${VARIABLE} → Jinja2-style hoặc YAML/frontmatter contracts. Thêm thought_cache section. Align với elicitation.schema.yaml. | `templates/elicitation_report.template.md` |
| `data/input-schema.yaml` | 72 | JSON Schema input (4 required + optional NFR) | **Reference** cho DRC design. Schema fields dùng làm base cho DRC input contract. | `data/drc.yaml` — input section |

**Tổng quan khai thác**: ~8/9 files cũ có thể tái sử dụng. Chỉ cần 3 files hoàn toàn mới (validate_outputs.py, thought_cache_template.yaml, drc.yaml). Khoảng **430/530 dòng** (81%) nội dung cũ có thể khai thác qua merge/adapt.

---

## §7: Knowledge Mining — Chi tiết từ Old v0.0.2

### 7.1 Nội dung giữ nguyên (copy-edit nhẹ)

| Nội dung | Old file | Lý do giữ |
|:---|:---|:---|
| 7 QC criteria weighted scoring | `loop/elicitor-checklist.md` QC-01→07 | Cấu trúc ≥100% gate policy đã được validation qua thực tế. Chỉ cần đổi tên file và thêm thought-cache criterion. |
| Output template 6 sections + trace tags | `templates/elicitation-report.md.template` | Cấu trúc YAML frontmatter + normalized_input + gap_analysis + questionnaires + 3-path + self_verification là đầy đủ. Cần convert variable syntax. |
| 3-Layer Master Prompt Architecture | `knowledge/elicitation-rules.md` §4 | Mindset → Knowledge → Skills Layer là thiết kế kiến trúc tốt. Mindset Layer với critical thinking rules vẫn relevant. |
| 6 Mindset Keywords vector anchors | `knowledge/mindset-keywords.md` | 6 từ khóa với behavioral_impact + vector_anchors là tài liệu training giá trị cao. |
| 5W1H 6 question types + sub-questions | `knowledge/question-framework.md` §1 | Cấu trúc who/what/why/how/when/where với sub-questions là elicitation core. |

### 7.2 Nội dung cần restructure

| Nội dung | Lý do restructure | Cách xử lý |
|:---|:---|:---|
| 5 knowledge files riêng lẻ → 1 consolidated file | Phase 5 yêu cầu knowledge/ zone chỉ chứa 1 file per skill. 5 files nhỏ tạo fragmentation. | Merge vào `elicitation_patterns.md`: §1 Elicitation Rules, §2 Normalization Logic, §3 5W1H Framework, §4 6 Mindset Keywords, §5 Scope & Handoff |
| `${VARIABLE}` template syntax | Phase 5 yêu cầu YAML frontmatter contracts, không dùng biến shell-style | Chuyển sang Jinja2-style `{{ variable }}` hoặc frontmatter fields |
| Outdated source references (`thong-tin-mau.md`, `raw2.md`) | Các file này không còn tồn tại trong codebase | Bỏ references, giữ nguyên tắc cốt lõi |
| Old frontmatter (7 fields) | Phase 5 yêu cầu 10-field frontmatter per skill_skeleton.md | Thêm: suite, version, category, stage, target_variable, output_contract |
| Old SKILL.md inline knowledge | L0 anchor rule: SKILL.md phải separation of concerns, ≤700 tokens | Extract inline knowledge vào knowledge/ zone |

### 7.3 Nội dung hoàn toàn mới

| File | Lý do mới | Nội dung dự kiến |
|:---|:---|:---|
| `scripts/validate_outputs.py` | Old v0.0.2 không có validator script | Python script 8 criteria: (1) XML boundary, (2) NFR quantification, (3) trace tags presence, (4) 3-path decomposition, (5) 5W1H min questions, (6) zero placeholder, (7) thought-cache completeness, (8) schema compliance |
| `templates/thought_cache_template.yaml` | Old v0.0.2 không có thought-cache concept | 5-section: (1) business_thought_process, (2) stakeholder_empathy, (3) reverse_questions, (4) confidence_breakdown, (5) uncertainty_areas |
| `data/drc.yaml` | Phase 5 yêu cầu DRC contract per skill | 4-section DRC: inputs (raw_request), outputs (elicitation-report.md, thought-cache.yaml), routing (upstream: user, downstream: ba-analyst), state_persistence |

---

## §8: Pre-Existing State Assessment

### 8.1 Current Artifacts State

| Path | Status | Content |
|:---|:---|:---|
| `skills/ver-3/ba-elicitor/SKILL.md` | 🔴 Empty (0 bytes) | Cần author |
| `skills/ver-3/ba-elicitor/knowledge/` | 🔴 `.gitkeep` duy nhất | Cần author elicitation_patterns.md |
| `skills/ver-3/ba-elicitor/templates/` | 🔴 `.gitkeep` duy nhất | Cần author 2 templates |
| `skills/ver-3/ba-elicitor/loop/` | 🔴 `.gitkeep` duy nhất | Cần author scoping_checklist.md |
| `skills/ver-3/ba-elicitor/scripts/` | 🔴 `.gitkeep` duy nhất | Cần author validate_outputs.py |
| `skills/ver-3/ba-elicitor/data/` | 🔴 `.gitkeep` duy nhất | Cần author drc.yaml |
| `skills/ver-3/ba-elicitor/assets/` | 🟢 `.gitkeep` | Giữ nguyên |
| `.claude/skills/ba-elicitor/SKILL.md` | 🔴 Empty (0 bytes) | Chưa sync |
| `.claude/skills/ba-elicitor/assets/` | 🟢 Tồn tại (7 subdirs) | Scaffold đã có, chờ content |

### 8.2 Dependency Readiness

| Dependency | Status | Ghi chú |
|:---|:---:|:---|
| elicitation.schema.yaml | ✅ FULL | 5 required fields, 113 lines, verified Phase 4 |
| skill_skeleton.md | ✅ Complete | 51 lines, 11 XML sections |
| drc_contract_template.yaml | ✅ Complete | 36 lines, 4 sections |
| schema_validator.py | ✅ Verified | valid→exit 0, broken→exit 1 |
| artifact_registry.yaml | ✅ Complete | 153 lines, BA entries lines 112-153 |
| ba-pipeline-runner agent | ✅ Deployed | 198 lines, F1 handles missing skill gracefully |
| quality-scorer agent | ✅ Deployed | 233 lines, có thể invoke audit |
| Old v0.0.2 ba-elicitor | ✅ Available | 7 files, ~530 lines — knowledge mining ready |

---

## §9: Evidence

<evidence>
  <file>docs/context-to-work/phase-5-ba-pipeline/scope.2026-07-10.md</file>
  <line>228-237</line>
  <finding>ba-elicitor cần 7 files: SKILL.md, knowledge/elicitation_patterns.md, templates/ x2 (report + thought-cache), loop/scoping_checklist.md, scripts/validate_outputs.py, data/drc.yaml</finding>
</evidence>

<evidence>
  <file>docs/context-to-work/phase-5-ba-pipeline/scope.2026-07-10.md</file>
  <line>301-315</line>
  <finding>Old v0.0.2 ba-elicitor asset map: 6/7 files có thể kế thừa; chỉ validate_outputs.py và thought_cache_template.yaml là hoàn toàn mới</finding>
</evidence>

<evidence>
  <file>docs/context-to-work/phase-5-ba-pipeline/scope.2026-07-10.md</file>
  <line>362-383</line>
  <finding>Extraction summary: 7 direct-use files (~550 lines), 9 adaptation-needed (~660 lines), 6 new-only items (~400 lines). Coverage 70%</finding>
</evidence>

<evidence>
  <file>docs/context-to-work/phase-5-ba-pipeline/scope.2026-07-10.md</file>
  <line>636-640</line>
  <finding>Confidence breakdown: scope_completeness 97%, dependency_readiness 92%, artifact_state_accuracy 100%, effort_estimation 85%</finding>
</evidence>

<evidence>
  <file>skills/ver-3/_shared/templates/skill_skeleton.md</file>
  <line>1-51</line>
  <finding>Template 11 XML sections cần dùng làm structure cho SKILL.md mới: frontmatter (10 fields) + instructions + safety_contract + knowledge_anchors + workflow_phases + input_contract + output_contract + acceptance_criteria + failure_modes</finding>
</evidence>

<evidence>
  <file>skills/ver-3/_shared/schemas/elicitation.schema.yaml</file>
  <line>1-113</line>
  <finding>5 required output fields: skill_name, domain_ontology (terms + relationships), stakeholder_analysis (role/goals/pain_points), nrfs (id/category/metric/value/unit), thought_cache (business_thought_process/stakeholder_empathy/reverse_questions)</finding>
</evidence>

<evidence>
  <file>skills/ver-3/_shared/templates/drc_contract_template.yaml</file>
  <line>1-36</line>
  <finding>4-section DRC template: inputs, outputs, routing, state_persistence. Cần điền skill-specific fields cho ba-elicitor</finding>
</evidence>

<evidence>
  <file>skills/ver-3/_shared/artifact_registry.yaml</file>
  <line>112-153</line>
  <finding>BA artifact registry: elicitation-report.md path = .skill-context/{feature}/ba-elicitor/elicitation-report.md, schema = elicitation.schema.yaml</finding>
</evidence>

<evidence>
  <file>skills/ver-0.0.2/ba-elicitor/SKILL.md</file>
  <line>1-77</line>
  <finding>Old SKILL.md: 77 dòng, 4 execution_policies, 4 workflow phases, guardrails, output contract. Cần rewrite theo skill_skeleton.md</finding>
</evidence>

<evidence>
  <file>skills/ver-0.0.2/ba-elicitor/knowledge/elicitation-rules.md</file>
  <line>1-81</line>
  <finding>3-Layer Master Prompt Architecture: Mindset → Knowledge → Skills Layer. Anti-hallucination rules + stop conditions + 3-layer mapping table</finding>
</evidence>

<evidence>
  <file>skills/ver-0.0.2/ba-elicitor/knowledge/mindset-keywords.md</file>
  <line>1-98</line>
  <finding>6 Mindset Keywords: Systems Thinking, Root Cause Isolation, MECE, First Principles, Impact Analysis, Structural Decomposition. Vector anchors + behavioral_impact per keyword</finding>
</evidence>

<evidence>
  <file>skills/ver-0.0.2/ba-elicitor/knowledge/normalization-logic.md</file>
  <line>1-40</line>
  <finding>Normalization flow: RawInput → 4-step process. NFR quantification mapping (nhanh → latency, mượt → response time). Trace tags convention [TỪ INPUT]/[SUY LUẬN]/[CẦN LÀM RÕ]</finding>
</evidence>

<evidence>
  <file>skills/ver-0.0.2/ba-elicitor/knowledge/question-framework.md</file>
  <line>1-77</line>
  <finding>5W1H framework: 6 question types (who/what/why/how/when/where) với sub-questions. 3-path decomposition (Happy/Alternative/Exception). Multiple-choice interaction format</finding>
</evidence>

<evidence>
  <file>skills/ver-0.0.2/ba-elicitor/knowledge/scope-definition.md</file>
  <line>1-58</line>
  <finding>Scope definition: entry point Stage -1, input contract (XML boundary), output contract (6 sections), handoff to ba-analyst, risks with mitigations</finding>
</evidence>

<evidence>
  <file>skills/ver-0.0.2/ba-elicitor/loop/elicitor-checklist.md</file>
  <line>1-33</line>
  <finding>7 QC criteria with weighted scoring (QC-01→07): QC-01 XML boundary 15%, QC-02 anti-subjective 15%, QC-03 traceability 15%, QC-04 3-paths 15%, QC-05 5W1H 15%, QC-06 zero placeholder 15%, QC-07 confidence 10%. Gate: 100% pass = ghi file</finding>
</evidence>

<evidence>
  <file>skills/ver-0.0.2/ba-elicitor/templates/elicitation-report.md.template</file>
  <line>1-75</line>
  <finding>Output template: YAML frontmatter (4 fields: skill_name, elicitation_date, confidence_score, status) + 6 sections (normalized_input, gap_analysis, questionnaires, 3-path, impact_assessment, self_verification). Dùng ${VARIABLE} syntax — cần chuyển sang frontmatter</finding>
</evidence>

<evidence>
  <file>skills/ver-0.0.2/ba-elicitor/data/input-schema.yaml</file>
  <line>1-72</line>
  <finding>JSON Schema với 4 required fields (skill_name, description, core_objective, actors) + optional (environment, constraints, nfr với performance/security/token_budget). Có thể dùng base cho DRC contract</finding>
</evidence>

<evidence>
  <file>skills/ver-3/ba-elicitor/SKILL.md</file>
  <line>1</line>
  <finding>SKILL.md = 0 bytes — cần author content (confirmed empty)</finding>
</evidence>

<evidence>
  <file>skills/ver-3/ba-elicitor</file>
  <line>1</line>
  <finding>7-Zone scaffold tồn tại: assets/, data/, knowledge/, loop/, scripts/, SKILL.md, templates/. Tất cả zone đều empty (chỉ .gitkeep)</finding>
</evidence>

<evidence>
  <file>.claude/skills/ba-elicitor/SKILL.md</file>
  <line>1</line>
  <finding>Runtime target SKILL.md = 0 bytes — chưa sync từ skills/ver-3/</finding>
</evidence>

<evidence>
  <file>.claude/agents/ba-pipeline-runner.md</file>
  <line>174-176</line>
  <finding>F1 failure mode: "BA skill ba-elicitor chưa được build (Phase 5). Cannot dispatch stage." — xác nhận ba-elicitor launch dependency từ pipeline runner</finding>
</evidence>

---

## §10: Knowledge Merge Strategy — Chi tiết

### 10.1 Cấu trúc `knowledge/elicitation_patterns.md` đề xuất

```yaml
file: "skills/ver-3/ba-elicitor/knowledge/elicitation_patterns.md"
estimated_lines: 120-150
structure:
  §1: "Elicitation Rules & Master Prompt Architecture"
    source: "elicitation-rules.md (81 lines) — extract 3-Layer Architecture, anti-hallucination, stop conditions"
    content: "3-Layer Architecture (Mindset → Knowledge → Skills), MECE decomposition, anti-hallucination rules, stop conditions với confidence threshold"
    
  §2: "Normalization & NFR Quantification Logic"
    source: "normalization-logic.md (40 lines) — extract normalization flow, NFR mapping, trace tags"
    content: "4-step normalization flow, NFR quantification mapping table (từ mơ hồ → metrics), trace tags convention [TỪ INPUT]/[SUY LUẬN]/[CẦN LÀM RÕ]"
    
  §3: "5W1H Elicitation Framework"
    source: "question-framework.md (77 lines) — extract 5W1H framework, 3-path decomposition, interaction format"
    content: "6 question types with sub-questions, 3-path decomposition (Happy/Alternative/Exception), multiple-choice interaction format rules"
    
  §4: "6 Critical Thinking Mindset Keywords"
    source: "mindset-keywords.md (98 lines) — extract 6 keywords + vector anchors + cognitive rules"
    content: "Systems Thinking, Root Cause Isolation, MECE, First Principles, Impact Analysis, Structural Decomposition. Mỗi keyword kèm technical_essence + vector_anchors + behavioral_impact"
    
  §5: "Scope Definition & Handoff Contract"
    source: "scope-definition.md (58 lines) — extract entry point, I/O contracts, handoff, risks (tinh gọn)"
    content: "Entry point Stage -1, input contract (XML boundary), output contract aligned với elicitation.schema.yaml, handoff to ba-analyst, risk matrix"
```

**Lưu ý**: Không copy nguyên 354 dòng từ 5 files cũ. Cần tinh lọc, loại bỏ outdated references (`thong-tin-mau.md`, `raw2.md`), giữ nguyên tắc cốt lõi. Target 120-150 dòng (giảm ~60% so với tổng old).

### 10.2 Rủi ro khi merge knowledge

| Rủi ro | Mức | Mitigation |
|:---|:---:|:---|
| Mất context khi merge 5 files → 1 file | Medium | Giữ các section heading rõ ràng, không gộp nội dung khác logic vào chung |
| Outdated references bị giữ lại | Low | Grep tất cả references trước merge: `thong-tin-mau.md`, `raw2.md` → xóa |
| ${VARIABLE} syntax sót trong template | Medium | Convert tất cả `${VAR}` sang `{{ var }}` hoặc frontmatter fields. Check bằng grep pattern `\$\{` |
| Conflict giữa old Mermaid + Phase 5 mermaid rules | Low | Knowledge/elicitation_patterns.md không cần Mermaid rules (đã chuyển sang ba-analyst) |

---

## §11: Risk Assessment

| # | Risk | Probability | Impact | Mitigation |
|:---:|:---|:---:|:---:|:---|
| R1 | SKILL.md > 800 tokens (AC-3 fail) | Medium | High | `wc -w` check sau mỗi draft; tách inline knowledge vào knowledge/ zone |
| R2 | quality-scorer threshold ≥70% không đạt ngay lần đầu | High | Medium | Xây dựng SKILL.md với đủ must_not ≥5 constraint entries (META-2.1 S1), reverse questions coverage ≥4 aspects (S2), multi-stakeholder ≥2 (S3) |
| R3 | thought_cache_template.yaml không align với elicitation.schema.yaml thought_cache section | Medium | High | Validate sau khi author: kiểm tra 3 required sub-fields (business_thought_process, stakeholder_empathy, reverse_questions) |
| R4 | validate_outputs.py thiếu criteria coverage | Low | Medium | Thiết kế 8 criteria phủ: XML boundary, NFR quant, trace tags, 3-path, 5W1H, placeholder, thought-cache, schema |
| R5 | elicitation_report.template.md không align với elicitation.schema.yaml output fields | Low | High | Map từng section trong template với 5 required fields của schema |
| R6 | Deploy conflict — .claude/skills/ba-elicitor/ đã có SKILL.md empty (0 bytes) | Low | Low | Overwrite bằng cp. Hook registry không cần update. |
| R7 | Old knowledge content quá dài nếu copy nguyên → tràn context | Medium | Medium | Target 120-150 dòng cho knowledge file. Giảm 60% từ 354 dòng old. |

---

## §12: Confidence Assessment

```yaml
overall_confidence: 87%  # Giảm từ 91% (Phase 5 overall) vì đây là build phase đầu tiên

breakdown:
  scope_completeness: 95%
    # Scope master doc + old v0.0.2 inventory + schema/skeleton templates cung cấp coverage đầy đủ
  dependency_readiness: 92%
    # Phase 3 agents ready ✅. Phase 4 schemas full ✅. karpathy-standards 87/100 non-blocking.
  old_content_reusability: 85%
    # ~81% (430/530 dòng) nội dung cũ có thể khai thác. Rủi ro: merge 5→1 file cần chọn lọc kỹ.
  output_accuracy: 100%
    # Verified: skills/ver-3/ba-elicitor/ = 7 empty subdirs + SKILL.md 0 bytes ✅
  effort_estimation_confidence: 82%
    # 4 files adapt từ old (ước ~230 dòng), 3 files mới (ước ~220 dòng). Tổng ~450 dòng content.
    # quality-scorer strictness chưa rõ — có thể cần 1-2 iteration fix.

uncertainty_flags:
  - "quality-scorer threshold 70% — chưa test với BA skill content. META-2.1 negation density requirement (must_not ≥5) cần thiết kế ngay từ đầu."
  - "validate_outputs.py 8 criteria scope — cần xác định rõ từng criterion là structural check (yaml.safe_load) vs semantic check (content quality)."
  - "thought_cache_template.yaml — không có reference từ old v0.0.2. Cần design từ elicitation.schema.yaml thought_cache section (3 required fields)."
```

---

## §13: Build Sequence Recommendations

### 13.1 Thứ tự build đề xuất

```yaml
recommended_order:
  step_1: "Author data/drc.yaml"
    reason: "Đơn giản nhất, theo template. Tạo momentum."
    validation: "yaml.safe_load pass"
    
  step_2: "Author templates/thought_cache_template.yaml"
    reason: "Mới hoàn toàn — cần align với elicitation.schema.yaml §thought_cache (3 required fields)"
    validation: "yaml.safe_load + field check vs schema"
    
  step_3: "Author templates/elicitation_report.template.md"
    reason: "Adapt từ old — cần convert ${VARIABLE} syntax + update frontmatter + align với schema"
    validation: "Manual review: 6 sections + 5 schema fields coverage"
    
  step_4: "Author loop/scoping_checklist.md"
    reason: "Adapt từ old (33 dòng) — thêm thought-cache criterion (QC-08?)"
    validation: "Verify 7+ QC criteria format + weighted scoring ≤100%"
    
  step_5: "Author knowledge/elicitation_patterns.md"
    reason: "Phức tạp nhất — merge 5 files → 1. Cần nhiều iteration."
    validation: "wc -w estimate, content review: không còn outdated refs"
    
  step_6: "Author SKILL.md"
    reason: "Phụ thuộc vào knowledge content để reference. Viết cuối để biết chính xác link."
    validation: "wc -w ≤800, yaml frontmatter parse, 8 XML sections"
    
  step_7: "Author scripts/validate_outputs.py"
    reason: "Có thể viết song song với step 1-6 (ít phụ thuộc)"
    validation: "python3 -m py_compile validate_outputs.py"
    
  step_8: "Quality audit + fix"
    reason: "Chạy quality-scorer → fix ≥70%"
    validation: "quality-matrix.yaml verdict ≥ BORDERLINE"
    
  step_9: "Mock test"
    reason: "Test với mock request → verify artifacts"
    validation: "elicitation-report.md ≥1000 bytes, thought-cache.yaml tồn tại"
    
  step_10: "Deploy"
    reason: "Sync lên .claude/skills/"
    validation: ".claude/skills/ba-elicitor/SKILL.md tồn tại và không empty"
```

### 13.2 Song song hóa

```yaml
parallel_groups:
  group_A_independent:
    - "step_1 data/drc.yaml"
    - "step_2 templates/thought_cache_template.yaml"
    - "step_7 scripts/validate_outputs.py"
    rationale: "3 files này không phụ thuộc lẫn nhau, có thể author song song"
    
  group_B_sequential:
    - "step_5 knowledge/elicitation_patterns.md"
    - "step_6 SKILL.md"
    rationale: "SKILL.md cần biết knowledge structure để reference đúng đường dẫn"
    
  group_C_independent:
    - "step_3 templates/elicitation_report.template.md"
    - "step_4 loop/scoping_checklist.md"
    rationale: "2 files adapt từ old, không phụ thuộc lẫn nhau"
```

---

## §14: Acceptance Criteria (cho ba-elicitor riêng)

| AC | Mô tả | Verification | Auto/Manual |
|:---:|:------|:-------------|:-----------:|
| AC-E1 | 7 files tồn tại tại `skills/ver-3/ba-elicitor/` | `ls -la skills/ver-3/ba-elicitor/*/` | Auto |
| AC-E2 | SKILL.md frontmatter 10 fields parse được | Python yaml.safe_load | Auto |
| AC-E3 | SKILL.md ≤ 800 words | `wc -w` | Auto |
| AC-E4 | 7-Zone ≥4 zones populated | `find . -not -name '.gitkeep' -type f \| wc -l` | Auto |
| AC-E5 | DRC file parse + schema reference valid | `yaml.safe_load` | Auto |
| AC-E6 | thought_cache_template.yaml có 3 required fields | Field check vs elicitation.schema.yaml | Auto |
| AC-E7 | validate_outputs.py compile không lỗi | `python3 -m py_compile` | Auto |
| AC-E8 | quality-scorer audit ≥70% score | Invoke quality-scorer agent | Manual |
| AC-E9 | Mock invoke → elicitation-report.md ≥ 1000 bytes | `wc -c` + schema validate | Auto |
| AC-E10 | thought-cache.yaml tồn tại sau mock invoke | `test -f` | Auto |
| AC-E11 | `.claude/skills/ba-elicitor/SKILL.md` sync thành công | `file` + size check | Auto |

---

## §15: Open Questions

| # | Question | Priority | Liên quan | Status |
|:---:|:----------|:--------:|:---------:|:------|
| 1 | Quality-scorer agent threshold ≥70% — strictness level chưa rõ cho BA skill content. Cần dry-run test với skill skeleton trước không? | 🟡 Medium | AC-E8 | 🔄 Đề xuất: dry-run quality-scorer trên skill skeleton + 1 knowledge section trước khi author full |
| 2 | `thought_cache_template.yaml` — 5 sections hay align chặt với elicitation.schema.yaml (3 required fields)? Schema yêu cầu 3 fields: business_thought_process, stakeholder_empathy, reverse_questions. Có nên thêm confidence_breakdown + uncertainty_areas? | 🟡 Medium | AC-E6 | 🔄 Cần quyết định: schema-compliant (3 fields) hay extended (5 fields). Recommended: 5 fields (3 bắt buộc + 2 optional) |
| 3 | `validate_outputs.py` — 8 criteria structure: nên dùng function-per-criteria (testable) hay single check function? | 🟢 Low | AC-E7 | 🔄 Recommend: function-per-criteria pattern (giống schema_validator.py) |
| 4 | Old trace tags convention (`[TỪ INPUT]`, `[SUY LUẬN]`, `[CẦN LÀM RÕ]`) — có giữ nguyên không? | 🟢 Low | Template | ✅ **Confirmed**: scope master doc §7.6 khẳng định nên giữ làm semantic anchor |
| 5 | `assets/` zone — có cần content gì không? | 🟢 Low | AC-E4 | 🔄 Recommend: giữ .gitkeep. Nếu quality-scorer yêu cầu ≥4 zones populated, assets không tính là zone có content. Cần ensure scripts/ + data/ + templates/ + loop/ + knowledge/ ≥4 zones. |

---

## §16: Effort Estimation

```yaml
estimated_effort:
  total_new_content: ~450 lines
  
  per_file_breakdown:
    SKILL.md: 60-80 lines
    knowledge/elicitation_patterns.md: 120-150 lines (merge từ 354 lines old)
    templates/elicitation_report.template.md: 75-90 lines (adapt từ 75 lines old)
    templates/thought_cache_template.yaml: 40-50 lines (mới)
    loop/scoping_checklist.md: 33-40 lines (adapt từ 33 lines old)
    scripts/validate_outputs.py: 80-120 lines (mới)
    data/drc.yaml: 30-36 lines (mới theo template)
  
  quality_iterations:
    initial_build: ~70%
    fix_round_1: ~85%  (sau quality-scorer feedback)
    fix_round_2: ~95%  (nếu cần)
    final_audit: ≥70% target
  
  total_build_time_estimate: "Medium (2-3 agent sessions)"
    # Step 1-7 authoring: ~1-2 sessions
    # Step 8 quality audit + fix: ~0.5 session
    # Step 9-10 test + deploy: ~0.5 session
```

---

**Document Status**: Context Complete — No Code Changes Made
**Document Path**: `docs/context-to-work/phase-5-ba-pipeline/scope.ba-elicitor-build.2026-07-10.md`

```
✓ Entry point identified: Phase 5 scope master + old v0.0.2 ba-elicitor
✓ Current state assessed: ver-3 scaffold empty (7 zone .gitkeep), .claude/skills/ empty
✓ Knowledge mining mapped: 9 old files → 7 new files (4 adapt + 3 new)
✓ Merge strategy designed: 5 knowledge files → 1 consolidated (120-150 lines target)
✓ Direct-use identified: loop checklist + report template
✓ New content identified: validate_outputs.py + thought_cache_template.yaml + drc.yaml
✓ Build sequence recommended: 10 steps with parallelization groups (3 parallel independent tracks)
✓ Acceptance criteria defined: 11 AC (9 auto, 2 manual)
✓ Risk assessment: 7 risks with mitigations
✓ Evidence traced: 24 evidence blocks with specific file:line
✓ Confidence assessment: 87% (scope 95%, dependencies 92%, content reusability 85%)
✓ Open questions: 5 items (1 resolved, 4 open)
✓ Effort estimation: ~450 lines new content, 2-3 agent sessions
```

**NO CODE CHANGES — Context ready for build phase**
