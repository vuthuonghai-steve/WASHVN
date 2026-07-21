# Scope Document — Phân Tích Phase Kế Tiếp

**Date**: 2026-07-10
**Status**: Initial
**Skill**: context-before-fix v1.0.0

---

## §1: Problem Summary

Xác định phase tiếp theo cần triển khai trong **Master Skill Suite Rebuild (8-Phase Roadmap)** sau khi Phase 0-3 đã hoàn thành. Dựa trên:

1. `docs/plans/plan-checklist.2026-07-07.md` — checklist tracking toàn lộ trình
2. `Temps/spec/architects/shared/` — thiết kế kiến trúc 5-Layer pipeline + quality gates
3. `Temps/spec/architects/indexes/` — tra cứu spec theo role/domain/design
4. `skills/ver-3/roadmaps/` — roadmap source files cho từng phase
5. Filesystem state thực tế của `skills/ver-3/`

---

## §2: Entry Point

```
Entry: docs/plans/plan-checklist.2026-07-07.md
  → §4 Progress Dashboard (trang 48-62)
  → §9 Phase 4 (Schemas & DRC Contracts)
  → §10 Phase 5 (BA Skills Pipeline)
  → §15 Cross-Phase Tracking Metrics

Spec reference: Temps/spec/architects/
  → README.md (master navigation)
  → P0-context-bus-and-state/ (Context Bus — nền tảng)
  → P4-orchestrator-and-assembler/ (Orchestrator — cho Phase 6+)
  → P5-fallback-and-escalation/ (Fallback — cho Phase 5+)
```

---

## §3: Scope Definition

### 3.1 Trạng thái hiện tại (verified on disk)

| Phase | Status (doc) | Status (actual) | Notes |
|:------|:------------:|:---------------:|:------|
| P0 Foundation | ✅ 100% done | ✅ Done | 10 tasks, 8 AC pass |
| P1 Knowledge Base | ✅ 100% done | ✅ Done | 7 canonical docs (2,603 dòng) |
| P2 Hook Framework | ✅ 100% done | ✅ Done | 6 hook scripts + 7 tests |
| P3 Agent Foundation | ✅ 100% done | ✅ Done | 8 agents deployed |
| **P4 Schemas & DRC** | ⬜ **0% pending** | ⬜ **0%** | 14 stubs `# schema stub — Phase 4 fill` |
| P5 BA Pipeline | 🟡 **30% in_progress** | ⬜ **~0%** | 3 ba-* dirs: SKILL.md = 0 byte, chỉ có .gitkeep |
| P6A Discovery | ⬜ pending | ⬜ 0% | Chưa bắt đầu |
| P6B Execution | ⬜ pending | ⬜ 0% | Chặn bởi P6A gate |
| P7 Sandbox+Indexer | ⬜ pending | ⬜ 0% | Chặn bởi P5+P6 |
| P8 Integration | ⬜ pending | ⬜ 0% | Chặn bởi P2-P7 |

> **Phát hiện**: Phase 5 trong checklist ghi "~30%" nhưng thực tế **3 BA skills chỉ có cấu trúc thư mục rỗng** (0-byte SKILL.md). Đây là skeleton từ Phase 0 Task 2 (7-Zone scaffold), chưa có nội dung skill thật.

### 3.2 Dependency Graph (verified)

```
P0 (done)
├──→ P1 (done) ──→ P2 (done)
├──→ P4 (⬜) ──→ P5 (⬜, phụ thuộc P4)
│                └──→ P6A (⬜, phụ thuộc P5)
│                     └──→ P6B (⬜, gate ≥80%)
│                          └──→ P7 (⬜) ──→ P8 (⬜)
├──→ P3 (done) ──→ P5, P6A
```

### 3.3 Ranh giới phân tích

```yaml
in_scope:
  - Phase 4 (Schemas & DRC Contracts): tasks, deliverables, AC, dependencies
  - Phase 5 (BA Skills Pipeline): tasks, deliverables, AC, dependencies
  - Mối quan hệ giữa Phase 4 và Phase 5
  - Spec architects reference mapping
  - Roadmap source cross-check

out_of_scope:
  - Không triển khai phase (chỉ document)
  - Không sửa code
  - Không design chi tiết skill mới
```

---

## §4: Impact Analysis

### 4.1 Direct Impact — Phase 4 (Schemas & DRC Contracts)

**Dependency**: Chỉ phụ thuộc Phase 0 ✅ (14 schema stubs đã scaffold)

**Roadmap source**: `skills/ver-3/roadmaps/04-skill-pipeline-scaffold.md` (501 dòng)

**Spec architects mapping**:

| Spec file | Liên quan | Nội dung |
|:----------|:----------|:---------|
| `P0/context-bus-schema.md` | Artifact schema design | ER diagram + YAML schema cho Context Bus |
| `P0/artifact-registry.md` | Artifact lifecycle | 16 artifacts, path template, created-by/consumed-by |
| `P0/state-yaml-protocol.md` | State schema | `_state.yaml` protocol (version, stage tracking, fallback_history) |
| `P0/context-bus-rules.md` | R1-R8 rules | Write-Once-Read-Many, append-only fallback, version artifacts |
| `shared/quality-gates-reference.md` | Schema quality gates | META-1.1→3.3, BUILD-1.1→6.2, YAML-RES-1.0 |
| `shared/architecture-overview.md` | Pipeline architecture | 5-Layer, 2-Branch, 3-Mode |

**Deliverables cần build (12 tasks)**:

| Task | Deliverable | Hiện trạng |
|:-----|:------------|:-----------|
| 1 | Plan Durante — review spec P0-P7 | Chưa làm |
| 2 | 14 schemas (`skills/ver-3/_shared/schemas/`) | Stub `# schema stub — Phase 4 fill` |
| 3 | `schema_validator.py` (~250 dòng) | Empty dir (chỉ .gitkeep) |
| 4 | `artifact_lifecycle.py` (~150 dòng) | Empty dir |
| 5 | `drc_contract_template.yaml` | Chưa tồn tại |
| 6 | Skill skeleton + README templates | Chưa tồn tại |
| 7 | `artifact_registry.yaml` (14 entries) | Chưa tồn tại |
| 8 | `drc_resolver.py` | Chưa tồn tại |
| 9 | 28 test fixtures (2 per schema) | Chưa tồn tại |
| 10 | `karpathy-standards.md` (≥100 dòng) | Chưa tồn tại |
| 11 | Run AC-1→AC-7 | Chưa làm |
| 12 | Update skills-registry.json schema field | Chưa làm |

**14 Schemas cần author**:
1. `exploration.schema.yaml` — exploration.md frontmatter
2. `criteria.schema.json` — criteria.md (≥5 criteria + ≥2 test cases)
3. `design.schema.yaml` — design.md (7-Zone mapping)
4. `quality-matrix.schema.yaml` — quality-matrix.yaml (META-1→3)
5. `todo.schema.yaml` — todo.md (DAG task structure)
6. `build-log.schema.yaml` — build-log.md
7. `review-report.schema.yaml` — review-report.md
8. `audit-metrics.schema.yaml` — audit-metrics.yaml
9. `verification.schema.yaml` — verification.md (PASS/FAIL)
10. `security-review.schema.yaml` — security-review.md
11. `elicitation.schema.yaml` — elicitation-report.md
12. `analysis.schema.yaml` — analysis-report.md
13. `synthesis.schema.yaml` — business-analysis.md
14. `domain-handbook.schema.yaml` — domain-handbook.md

**7 Acceptance Criteria**:
- AC-1: 14 schemas parse (yaml.safe_load/json.load pass)
- AC-2: Schema validator runs (valid → 0, broken → 1)
- AC-3: DRC template parses
- AC-4: Artifact registry parses (14 entries)
- AC-5: DRC resolver exit 0
- AC-6: Skill skeleton có `name:`, `suite: WASHVN`
- AC-7: Karpathy standards ≥100 dòng

**Công sức**: L (~2-3 sessions, ~40 files)
**Blocker**: Không có (chỉ phụ thuộc P0 đã done)

### 4.2 Indirect Impact — Phase 5 (BA Skills Pipeline)

**Dependency**: Phụ thuộc **Phase 3** (✅ done) + **Phase 4** (⬜ pending → cần Phase 4 trước)

**Roadmap source**: `skills/ver-3/roadmaps/05-skill-build-ba-pipeline.md` (642 dòng)

**Spec architects mapping**:

| Spec file | Liên quan | Nội dung |
|:----------|:----------|:---------|
| `P0/context-bus-rules.md` | R2, R7, R8 | Hydrator, Builder context rules |
| `P0/state-yaml-protocol.md` | State tracking | fallback_history cho BA pipeline |
| `P1/scs-routing.md` | SCS scoring | Đầu vào cho BA Elicitor |
| `P1/spec-gatekeeper.md` | Quality gates | META-criteria cho BA design |
| `P1/meta-criteria.md` | META-1→3 | Quality scoring reference |
| `P5/fallback-matrix-full.md` | F16-F19 | BA-specific fallbacks |
| `P5/escalation-protocol.md` | Escalation | 3-iteration escalate |
| `shared/quality-gates-reference.md` | Stage gates | BA-1→4, SCS-1→2, MIN-1→3 |
| `indexes/by-role.md` | BA Elicitor role | P1, P2, P5 spec files |

**Deliverables cần build (15 tasks, 3 skills ~30 files)**:
- `ba-elicitor` (7-Zone: SKILL.md, knowledge, templates, loop, scripts, data, assets)
- `ba-analyst` (7-Zone)
- `ba-synthesizer` (7-Zone)

**Blocker**: Phase 4 chưa xong → schema validators + DRC contracts chưa có → Phase 5 không thể build đúng design contract.

### 4.3 Spec Architects Indexes — Cross-Reference cho cả 2 Phase

| Index | Content | Dùng cho |
|:------|:--------|:---------|
| `indexes/by-role.md` | Role → phase files | Xác định ai làm gì |
| `indexes/by-domain.md` | Domain → phase files | Data/Protocol/Quality/Execution |
| `indexes/by-design.md` | Design concern → files | Architecture/Contract/Integration |
| `shared/architecture-overview.md` | 5-Layer overview | Cả 2 phase |
| `shared/glossary.md` | Thuật ngữ pipeline | Cả 2 phase |
| `shared/pipeline-flowchart.md` | Pipeline visual | Cả 2 phase |
| `shared/quality-gates-reference.md` | Quality gate matrix | Phase 4 schemas + Phase 5 gates |

---

## §5: Call Chain

**Dependency chain cho "next phase" decision:**

```
Status hiện tại:
  P0 (done) → P1 (done) → P2 (done)
  P0 (done) → P3 (done)
  P0 (done) → P4 (stub)  ← next theo dependency
  P4 → P5 (empty dirs)
  P3 → P5
  P5 → P6A → P6B → P7 → P8

Gánh nặng block:
  Phase 5 BLOCKED on Phase 4 (schema validators + DRC contracts)
  Phase 6A BLOCKED on Phase 4 + Phase 5
  Phase 8 BLOCKED on Phase 2,3,5,6,7
```

---

## §6: Data Flow

### 6.1 Input (đã có)
- `docs/plans/plan-checklist.2026-07-07.md` — 1,169 dòng tracking
- `Temps/spec/architects/{P0-P7}/` — ~45 spec files, ~2,049 dòng
- `skills/ver-3/roadmaps/04-skill-pipeline-scaffold.md` — Phase 4 roadmap (501 dòng)
- `skills/ver-3/roadmaps/05-skill-build-ba-pipeline.md` — Phase 5 roadmap (642 dòng)
- `skills/ver-3/_shared/schemas/` — 14 schema stubs (31 bytes each)
- `skills/ver-3/_shared/validators/` — empty
- `skills/ver-3/ba-{elicitor,analyst,synthesizer}/` — empty SKILL.md + .gitkeep

### 6.2 Output scope
- Scope document này (không fix code)
- Khuyến nghị phase ưu tiên dựa trên dependency + thực tế

### 6.3 Dependencies
| Item | Phụ thuộc vào | Trạng thái |
|:-----|:-------------|:-----------|
| Phase 4 | P0 Foundation | ✅ Done |
| Phase 5 | P3 Agents + P4 Schemas | ✅ P3 done, ⬜ P4 pending |
| Phase 5 | schema_validator.py | ⬜ Chưa có (Phase 4) |
| Phase 5 | DRC templates | ⬜ Chưa có (Phase 4) |
| Phase 5 | quality-matrix schema | ⬜ Chưa có (Phase 4) |

---

## §7: Affected Components

### 7.1 Files (Phase 4 scope)
```
skills/ver-3/_shared/schemas/            ← 14 files cần author (từ stub)
skills/ver-3/_shared/validators/         ← 2 scripts cần tạo mới
skills/ver-3/_shared/templates/          ← 3 templates cần tạo mới
skills/ver-3/_shared/knowledge/          ← karpathy-standards.md cần tạo
skills/ver-3/_shared/data/               ← artifact_registry.yaml cần tạo
skills/ver-3/_shared/scripts/            ← drc_resolver.py cần tạo
skills/ver-3/_shared/tests/              ← 28 fixtures cần tạo
```

### 7.2 Functions/APIs (Phase 4 scope)
- `schema_validator.py` CLI: `--all`, `--artifact <name>`, `--skills-registry`
- `artifact_lifecycle.py` CLI: existence + mtime + version pinning check
- `drc_resolver.py` CLI: resolve DRC contracts từ registry
- 14 schema definitions (YAML/JSON): field types, required, constraints, examples

### 7.3 Agents liên quan
| Agent | Vai trò trong Phase 4 |
|:------|:---------------------|
| `design-validator` | Validate schema completeness |
| `quality-scorer` | Score schema quality (META) |
| `pipeline-orchestrator` | Orchestrate Phase 4 tasks |
| `subagent-forge` | Có thể forge schema helper subagent |

---

## §8: Evidence

<evidence>
<file>skills/ver-3/_shared/schemas/exploration.schema.yaml</file>
<line>1</line>
<finding>Schema stub: chỉ có `# schema stub — Phase 4 fill` — chưa có field definitions</finding>
</evidence>

<evidence>
<file>skills/ver-3/_shared/schemas/criteria.schema.json</file>
<line>1</line>
<finding>JSON stub: `{}` — empty object, chưa có criteria schema</finding>
</evidence>

<evidence>
<file>skills/ver-3/_shared/validators/</file>
<line>1</line>
<finding>Validators directory empty — schema_validator.py và artifact_lifecycle.py chưa tồn tại</finding>
</evidence>

<evidence>
<file>skills/ver-3/ba-elicitor/SKILL.md</file>
<line>1</line>
<finding>BA skill: 0 byte — chưa có nội dung SKILL.md thực tế</finding>
</evidence>

<evidence>
<file>skills/ver-3/ba-analyst/SKILL.md</file>
<line>1</line>
<finding>BA skill: 0 byte — chưa có nội dung SKILL.md thực tế</finding>
</evidence>

<evidence>
<file>skills/ver-3/ba-synthesizer/SKILL.md</file>
<line>1</line>
<finding>BA skill: 0 byte — chưa có nội dung SKILL.md thực tế</finding>
</evidence>

<evidence>
<file>skills/ver-3/roadmaps/04-skill-pipeline-scaffold.md</file>
<line>1-501</line>
<finding>Phase 4 roadmap: 501 dòng, định nghĩa 12 tasks, 14 schemas, 7 AC, 8 DoD</finding>
</evidence>

<evidence>
<file>skills/ver-3/roadmaps/05-skill-build-ba-pipeline.md</file>
<line>1-642</line>
<finding>Phase 5 roadmap: 642 dòng, định nghĩa 15 tasks, 3 skills BA, 9 AC</finding>
</evidence>

<evidence>
<file>docs/plans/plan-checklist.2026-07-07.md</file>
<line>48-62</line>
<finding>Progress dashboard: Phase 4 pending 0%, Phase 5 in_progress 30% (stale)</finding>
</evidence>

<evidence>
<file>Temps/spec/architects/P0-context-bus-and-state/context-bus-schema.md</file>
<line>1-81</line>
<finding>Context Bus schema spec: ER diagram + YAML schema — reference cho Phase 4 artifact schemas</finding>
</evidence>

<evidence>
<file>Temps/spec/architects/P0-context-bus-and-state/artifact-registry.md</file>
<line>1-30</line>
<finding>Artifact registry spec: 16 artifacts with created-by/consumed-by — reference cho artifact_registry.yaml</finding>
</evidence>

<evidence>
<file>Temps/spec/architects/shared/quality-gates-reference.md</file>
<line>1-49</line>
<finding>Quality gates matrix: tất cả stage gates từ BA đến Sandbox — reference cho schema constraints</finding>
</evidence>

---

## §9: Confidence Assessment

```yaml
overall_confidence: 92%

breakdown:
  phase_state_verification: 98%
    - reason: "Đã verify trực tiếp filesystem cho schemas + BA skills"
    - uncertainty: "plan-checklist ghi Phase 5 30% nhưng thực tế empty"
    
  dependency_accuracy: 95%
    - reason: "Dependency graph verified với roadmap index.md + scope.2026-07-07.md"
    
  spec_reference_mapping: 90%
    - reason: "Đã map spec architects P0-P7 vào từng phase deliverable"
    - uncertainty: "Chưa đọc hết 45 spec files — đọc sample đại diện"
    
  effort_estimation: 85%
    - reason: "Dựa trên roadmap estimates + line counts spec files"
    - uncertainty: "Công sức thực tế có thể thay đổi tùy complexity từng schema"

uncertainty_flags:
  - "Phase 5 ghi 30% nhưng thực tế chỉ có empty stubs — cần update checklist"
  - "Spec architects definition (5-Layer) khác với Master Skill Suite 8-Stage — cần reconcile architecture"
  - "Chưa verify roadmap 04 và 05 có conflict gì với spec architects không"
```

---

## §10: Open Questions

| # | Question | Priority | Phase | Status |
|---|----------|----------|-------|--------|
| 1 | **Phase 4 hay Phase 5 trước?** — Dependency đúng là P4→P5, nhưng P5 đã có skeleton. Có nên ưu tiên P5 hay bắt buộc P4 trước? | **High** | P4/P5 | **OPEN — cần user decision** |
| 2 | **14 schemas format**: Nên dùng YAML (kiểu OpenAPI-like) hay JSON Schema? Roadmap ghi `exploration.schema.yaml` và `criteria.schema.json` — inconsistency nhỏ | Medium | P4 | Open |
| 3 | **Spec architects vs 8-Stage pipeline**: Spec architects (5-Layer) ở Temps/ khác với Master Skill Suite (8-Stage) ở skills/ — spec này dùng cho Phase 4 hay Phase 8 reconcile? | **High** | Cross | Open |
| 4 | **Validator language**: Python (như roadmap) hay Bash? Python có sẵn trên môi trường không? | Low | P4 | Open |
| 5 | **BA skills đã có ở `.claude/skills/` chưa?** Cần kiểm tra runtime có bản cũ không | Medium | P5 | Open |
| 6 | **aggregate-quality-gatekeeper skill thiếu** (drift audit P3 note) — blocker cho Phase 5/6/8 | **High** | P3/P5 | Open |

---

## §11: Khuyến nghị — Two-Phase Roadmap

### Recommended: Phase 4 → Phase 5 (sequential)

Lý do:
1. **Dependency binding**: Phase 5 cần schema validators + DRC contracts từ Phase 4
2. **Filesystem reality**: Cả Phase 4 và Phase 5 đều ở trạng thái gần như 0%
3. **Effort balance**: Phase 4 là "nền tảng dữ liệu" (schemas + validators) — Phase 5 là "xây dựng kỹ năng" (3 BA skills)
4. **Risk reduction**: Làm Phase 4 trước giảm risk làm lại Phase 5 khi schema thay đổi

### Option B: Phase 5 trước (nếu cần BA pipeline gấp)

Có thể làm Phase 5 trước nếu:
- Tạm dùng schema stubs hiện tại (không validators)
- Chấp nhận technical debt
- BA pipeline cần gấp để elicit business requirements

### Optional parallelism

Một số spec có thể song song:
- **Phase 4 Task 1** (Plan Durante) + review `Temps/spec/architects/P0-P7` độc lập
- **Phase 4 schemas authoring**: 14 schemas có thể author song song (3-4 schemas per batch)
- **Phase 4 scripts** (validators) có thể viết độc lập sau schemas có định hướng

---

## Summary

```yaml
phase_4:
  status: "⏳ Next phase (khuyến nghị)"
  actual_state: "14 schema stubs + empty validators"
  effort: "L (~40 files, 12 tasks)"
  blocks: "Phase 5, 6A, 6B, 7, 8"
  dependency: "Chỉ cần P0 (✅ done)"

phase_5:
  status: "⏳ Sau Phase 4 (khuyến nghị)"
  actual_state: "3 empty skill dirs (0-byte SKILL.md)"
  effort: "L (~30 files, 15 tasks, 3 skills)"
  blocked_by: "Phase 4 schemas + validators"
  partial_work: "Cấu trúc thư mục 7-Zone đã scaffold (Phase 0)"
```

---

**Document Status**: Context Complete — No Code Changes Made

```
NO CODE CHANGES — Context ready for fix phase
✓ Entry point identified và verified
✓ Tất cả related files đã được search
✓ Impact map đầy đủ (direct + indirect)
✓ Evidence ghi nhận cụ thể (file:line)
✓ Confidence assessment đã làm
✓ Document viết bằng tiếng Việt
✓ Document lưu đúng path pattern
```

---

**Document**: `docs/context-to-work/next-phase-analysis/scope.2026-07-10.md`
**Generated by**: context-before-fix v1.0.0
**Language**: Vietnamese
