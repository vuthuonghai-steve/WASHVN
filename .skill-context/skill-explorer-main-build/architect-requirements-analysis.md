# Architectural Requirements Analysis — skill-explorer v1.0
> Generated for Stage 1 (Architect) — 2026-07-11
> Sources: scope.2026-07-11.md + domain-handbook.md (business-analysis.md: NOT FOUND/empty)

---

## §1: Core Requirements Matrix

### 1.1 Functional Requirements (FR)

| ID | Requirement | Source | Priority | Artifact |
|:---|:---|---|:---:|:---|
| **FR-01** | Chuyển từ single-stream output (1 file `exploration.md`) sang dual-stream + metadata (3 artifacts: `exploration.md` + `hydrated-context.yaml` + `thought-cache.yaml`) | scope §6.2, domain §2.B | **P0-CRITICAL** | Output |
| **FR-02** | Thêm Domain Anchoring: thought blocks ≥200 từ trong `thought-cache.yaml`, glossary 10+ terms trong SKILL boot | scope §Summary#1, domain §2.D | **P0-CRITICAL** | thought-cache.yaml |
| **FR-03** | Thêm Context Pre-processing Phase (Phase 2.5): Context Hydrator giữa Resource Gathering và Synthesis | scope §7.1#5, domain §3.D | **P0-CRITICAL** | workflow.md |
| **FR-04** | Thêm Dual Knowledge Stream ingestion: Technical (hydrated-context.yaml) + Cognitive (thought-cache.yaml) là 2 streams riêng biệt | scope §Summary#4, domain §1.B | **P0-CRITICAL** | SKILL.md |
| **FR-05** | Thêm Depth Signal Verification Phase (Phase 3.5) sau Synthesis | scope §7.1#5, domain §3.D | **P1-HIGH** | workflow.md |
| **FR-06** | Thêm Binary Mechanical Gates (META-2.1): S1 Negation AND S2 Reverse Question AND S3 Multi-Stakeholder AND S4 Constraint Anchoring = PASS | scope §Summary#5, domain §3.C | **P1-HIGH** | exploration-checklist.md |
| **FR-07** | Thêm YAML Resilience Layer L1-L3: syntax lint → schema validation → cross-ref, auto-repair trước commit Context Bus | scope §4.1, domain §4.C | **P1-HIGH** | security-standards.md |
| **FR-08** | Thêm Schema Frontmatter cho `hydrated-context.yaml`: glossary, nfr, edge_cases, data_contracts, zone_map, must_not | domain §2.C | **P1-HIGH** | hydrated-context.yaml |
| **FR-09** | Thêm Schema Frontmatter cho `thought-cache.yaml`: thought_blocks (≥200 từ), stakeholder_empathy, defensive_reasoning, META-2.1 signals | domain §2.D | **P1-HIGH** | thought-cache.yaml |
| **FR-10** | Thêm Negative Space: anti-patterns section riêng (6 anti-patterns), S1 Negation gate | scope §Summary#6, domain §4.A | **P2-MEDIUM** | exploration.md.template |
| **FR-11** | Thêm Graceful Degradation: fallback matrix (subset F1-F19), max 3 iterations/stage, append-only history | scope §Summary#7, domain §1.B | **P2-MEDIUM** | security-standards.md |
| **FR-12** | Update `init_context.py::handle_single_init()`: tạo 3 artifacts thay vì 1 (exploration.md + hydrated-context.yaml + thought-cache.yaml) | scope §6.2, domain §2.E | **P0-CRITICAL** | init_context.py |
| **FR-13** | Update `init_context.py::handle_split_run()`: copy cả hydrated-context.yaml + thought-cache.yaml xuống micro-skill | domain §2.E | **P1-HIGH** | init_context.py |
| **FR-14** | Update `init_context.py::parse_frontmatter()`: parse dual artifacts với decomposed flag | domain §2.E | **P2-MEDIUM** | init_context.py |
| **FR-15** | Update `schema_validator.py` để hỗ trợ multi-artifact validation | scope §4.2, §7.2 | **P1-HIGH** | schema_validator.py |
| **FR-16** | Update `exploration.schema.yaml` để hỗ trợ dual stream output schema | scope §6.3 | **P0-CRITICAL** | exploration.schema.yaml |
| **FR-17** | Thêm SCS 2-phase: Stage 0.5 pre-pass + Stage 1.5 validate (thay vì single-pass Stage 0) | scope §4.1, domain §1.B | **P2-MEDIUM** | exploration-standards.md |
| **FR-18** | Thêm sampling audit (default 30% rate, có thể tăng 100% cho P0) vào security pipeline | scope §4.1, domain §3.D | **P2-MEDIUM** | security-standards.md |
| **FR-19** | Update `exploration.md.template` để chứa YAML blocks reference đến hydrated-context + thought-cache | scope §7.1#6 | **P1-HIGH** | exploration.md.template |
| **FR-20** | Cập nhật SKILL.md boot config: dual context ingestion routing, binary gates config, thought block injection | scope §7.1#1 | **P0-CRITICAL** | SKILL.md |

### 1.2 Non-Functional Requirements (NFR)

| ID | Requirement | Source | Priority | Metric |
|:---|:---|---|:---:|:---|
| **NFR-01** | Hydrated-context.yaml ≤ 30-50 lines (technical contracts cô đặc) | domain §2.B | **P1-HIGH** | ≤50 YAML lines |
| **NFR-02** | Thought-cache.yaml ≤ 100-200 lines (cognitive depth, không phình to) | domain §2.B | **P1-HIGH** | ≤200 YAML lines |
| **NFR-03** | YAML Resilience: auto-repair max 2 attempts, nếu fail → Hard Halt cho critical, Graceful Degradation cho non-critical | domain §4.C | **P1-HIGH** | ≤2 repair cycles |
| **NFR-04** | META-2.1 binary gates: deterministic, regex-based (không NLP), MUST pass all 4 signals (S1∧S2∧S3∧S4) | domain §3.C | **P1-HIGH** | 100% deterministic |
| **NFR-05** | Fallback matrix: max 3 iterations per stage, append-only history | domain §1.B | **P2-MEDIUM** | ≤3 iterations/stage |
| **NFR-06** | Graceful degradation khi web fetch thất bại: dùng resources nội bộ, mark [CẦN LÀM RÕ] | domain §4.B#E7 | **P2-MEDIUM** | Zero hard halt for non-critical |
| **NFR-07** | Safe create: KHÔNG overwrite file đã tồn tại (resume mode) | domain §4.B#E2 | **P1-HIGH** | No data loss |
| **NFR-08** | HITL gate: dừng và hỏi user nếu confidence <70% | domain §4.B#E6 | **P1-HIGH** | Confidence ≥70% |
| **NFR-09** | Backward compatibility: skill-architect và skill-planner phải đọc được format mới | scope §4.2 | **P0-CRITICAL** | No downstream breakage |
| **NFR-10** | init_context.py: validate skill_name là kebab-case trước khi tạo directory | domain §4.B#E1 | **P2-MEDIUM** | Reject non-kebab-case |

### 1.3 Pipeline Readiness

| Pipeline Stage | v0.0.2 | v1.0 Target | READINESS |
|:---|---|:---|:---:|
| Stage 0 (skill-explorer) | Single exploration.md | 3 artifacts + dual stream + binary gates | **TO-BE-DESIGNED** |
| Stage 1 (skill-architect) | Reads exploration.md | Must read exploration.md + hydrated-context.yaml + thought-cache.yaml | **UNCERTAIN (Q2)** |
| Stage 2 (skill-planner) | Reads exploration.md | hydrated-context.yaml mandatory + thought-cache.yaml optional | **NEEDS UPDATE** |
| Stage 3 (skill-builder) | Reads planner handoff | Must read hydrated-context.yaml + thought-cache.yaml (both mandatory) | **NEEDS UPDATE** |
| Stage 4 (skill-tester) | Reads criteria.md | criteria.md (cập nhật) | **LOW IMPACT** |
| Shared schemas | exploration.schema.yaml | Must support multi-artifact | **UNCERTAIN (Q1)** |
| Shared validators | schema_validator.py | Must support multi-artifact validation | **NEEDS UPDATE (Q8)** |

---

## §2: Open Questions Cần Resolve

| # | Question | Domain | Impact if Unresolved | Recommended Decision (for Architect) |
|:---:|---|:---:|:---|:---|
| **Q1** | `exploration.schema.yaml` hiện tại có hỗ trợ multi-artifact output không? | Schema compatibility | **BLOCKER** — không thể design output schema nếu không biết giới hạn | Cần locate file thực tế và đọc schema hiện tại |
| **Q2** | skill-architect hiện tại đọc `exploration.md` ở format nào? Có cần update không? | Downstream breaking | **BLOCKER** — architect sẽ fail nếu format thay đổi | Cần đọc skill-architect SKILL.md để verify |
| **Q3** | Giữ `exploration.md` làm report tổng + 2 artifact mới, hay thay thế hoàn toàn bằng 3 artifact riêng? | Output strategy | **HIGH** — ảnh hưởng toàn bộ data flow | **Đề xuất**: Giữ exploration.md làm report tổng hợp (simplified), thêm 2 artifact mới. Giảm breaking change. |
| **Q4** | `thought-cache.yaml` có schema riêng hay dùng chung `exploration.schema.yaml`? | Schema design | **MEDIUM** — ảnh hưởng validator | **Đề xuất**: Schema riêng cho thought-cache.yaml (cognitive depth khác biệt về cấu trúc so với technical contracts) |
| **Q5** | SCS score: giữ single-pass (Stage 0) hay chuyển sang 2-phase (Stage 0.5 + Stage 1.5)? | Pipeline redesign | **MEDIUM** — ảnh hưởng workflow complexity | **Đề xuất**: Implement 2-phase nhưng đánh dấu Stage 1.5 là optional cho v1.0, mandatory cho v1.1 |
| **Q6** | Implement bao nhiêu fallback cases từ F1-F19 cho v1.0? Subset hay full? | Scope sizing | **LOW-MEDIUM** — ảnh hưởng scope | **Đề xuất**: Subset critical: F1-F5 (network/API/parse/schema/timeout) + F19 (unknown). Phần còn lại deferred. |
| **Q7** | Binary gates META-2.1 implement ngay trong Stage 0 (exploration) hay chỉ ở downstream? | Phasing | **MEDIUM** — ảnh hưởng exploration-checklist | **Đề xuất**: Implement ngay trong exploration v1.0 vì đây là quality gate cốt lõi của 7 LLM principles. |
| **Q8** | Sampling audit rate 30% có phù hợp với exploration stage không? | Rate tuning | **LOW** — có thể config sau | **Đề xuất**: Default 30%, cho phép override = 100% khi debug. Không cần quyết định ngay. |

---

## §3: Affected Components & Integration Points

### 3.1 Directly Modified Files (7 files + 2 new)

| # | File | Change Type | FR/NFR Ref | Complexity |
|:---:|---|:---:|:---:|:---:|
| 1 | `.agents/skills/skill-explorer/SKILL.md` | **MODIFY** — boot sequence | FR-04, FR-20 | **HIGH** |
| 2 | `.agents/skills/skill-explorer/knowledge/exploration-standards.md` | **MODIFY** — expand 7 Golden Standards | FR-17 | **MEDIUM** |
| 3 | `.agents/skills/skill-explorer/knowledge/security-standards.md` | **MODIFY** — add YAML Resilience + sampling audit | FR-07, FR-11, FR-18 | **HIGH** |
| 4 | `.agents/skills/skill-explorer/policy/output-spec.md` | **MODIFY** — restructure for 3 artifacts | FR-01 | **MEDIUM** |
| 5 | `.agents/skills/skill-explorer/policy/workflow.md` | **MODIFY** — add Phase 2.5 + Phase 3.5 | FR-03, FR-05 | **MEDIUM** |
| 6 | `.agents/skills/skill-explorer/templates/exploration.md.template` | **MODIFY** — add YAML ref blocks | FR-10, FR-19 | **LOW** |
| 7 | `.agents/skills/skill-explorer/loop/exploration-checklist.md` | **MODIFY** — replace soft questions with binary gates | FR-06 | **HIGH** |
| 8 | `.agents/skills/skill-explorer/scripts/init_context.py` | **MODIFY** — add dual artifact init + split | FR-12, FR-13, FR-14 | **HIGH** |
| — | (NEW) `templates/hydrated-context.yaml` | **CREATE** — template cho new artifact | FR-08 | **LOW** |
| — | (NEW) `templates/thought-cache.yaml` | **CREATE** — template cho new artifact | FR-09 | **LOW** |

### 3.2 Indirectly Affected Components (downstream)

| Component | File | Impact | Risk |
|:---|---|:---:|:---:|
| Shared schemas | `_shared/schemas/exploration.schema.yaml` | **HIGH** — must support multi-artifact (Q1) | ⚠️ **BLOCKER if not updated** |
| Shared validators | `_shared/validators/schema_validator.py` | **MEDIUM** — must support multi-artifact validation (Q8) | ⚠️ May fail silently |
| skill-architect | `.agents/skills/skill-architect/SKILL.md` | **HIGH** — downstream consumer (Q2) | ⚠️ **BLOCKER if not verified** |
| skill-planner | `.agents/skills/skill-planner/SKILL.md` | **HIGH** — mandatory consumer of hydrated-context.yaml | Medium |
| skill-builder | `.agents/skills/skill-builder/SKILL.md` | **MEDIUM** — consumer of both new artifacts | Low |
| skill-tester | `.agents/skills/skill-tester/SKILL.md` | **LOW** — criteria.md changes minimal | Low |
| Framework knowledge | `_shared/knowledge/framework.md` | **LOW** — reference only | None |

### 3.3 API/Function Changes

| Function | File | Change | Risk |
|:---|---|:---:|:---:|
| `handle_single_init()` | `init_context.py` | Init 3 artifacts (was 1) | **HIGH** — core logic change |
| `handle_split_run()` | `init_context.py` | Copy 2 new artifacts to micro-skill | **MEDIUM** |
| `parse_frontmatter()` | `init_context.py` | Parse dual artifacts + decomposed flag | **MEDIUM** |
| Schema validator | `schema_validator.py` | Multi-artifact validation support | **MEDIUM** — depends on Q1 |

---

## §4: Data Contract Specifications — 3 Artifacts

### 4.1 Artifact Overview

```
v0.0.2 (As-Is):                    v1.0 (To-Be):
  .skill-context/{skill}/           .skill-context/{skill}/
  ├── exploration.md                ├── exploration.md          (simplified report)
  └── criteria.md                   ├── hydrated-context.yaml   (NEW: ~30-50 lines YAML)
                                    ├── thought-cache.yaml      (NEW: ~100-200 lines YAML)
                                    └── criteria.md             (updated)
```

### 4.2 Artifact 1: `exploration.md`

| Field | Specification |
|:---|---|
| **Path** | `.skill-context/{target_skill}/exploration.md` |
| **Format** | Markdown + YAML frontmatter |
| **Schema** | `_shared/schemas/exploration.schema.yaml` (cần update) |
| **Consumer(s)** | skill-architect (mandatory), skill-planner (reference) |
| **Content** | 8-section exploration report (simplified), YAML block references đến hydrated-context + thought-cache |
| **Lifecycle** | Created at Stage 0, consumed by Stage 1-2 |
| **Changes from v0.0.2** | Thêm Negative Space section (anti-patterns), references đến 2 artifact mới |

### 4.3 Artifact 2: `hydrated-context.yaml`

| Field | Specification |
|:---|---|
| **Path** | `.skill-context/{target_skill}/hydrated-context.yaml` |
| **Format** | YAML |
| **Size Budget** | **30-50 lines** (strict — technical contracts cô đặc) |
| **Consumer(s)** | skill-planner (mandatory), skill-builder (mandatory) |
| **Contains** | glossary, nfr, edge_cases, data_contracts, zone_map, must_not |
| **Lifecycle** | Created at Stage 0, consumed by Stage 2-3. **NOT read by skill-architect.**
| **Validation** | YAML Resilience L1-L3 trước commit Context Bus |

**Proposed Schema (frontmatter):**
```yaml
skill_name: "{target_skill}"
stage: "exploration"
glossary:
  - term: "string"
    definition: "string"
nfr:
  - id: "string"
    requirement: "string"
edge_cases:
  - scenario: "string"
    expected: "string"
data_contracts:
  input: "schema reference"
  output: "schema reference"
zone_map:
  core: ["SKILL.md"]
  knowledge: ["knowledge/*.md"]
must_not:
  - "string"
```

### 4.4 Artifact 3: `thought-cache.yaml`

| Field | Specification |
|:---|---|
| **Path** | `.skill-context/{target_skill}/thought-cache.yaml` |
| **Format** | YAML |
| **Size Budget** | **100-200 lines** (cognitive depth, chứa thought blocks ≥200 từ) |
| **Consumer(s)** | skill-planner (optional), skill-builder (mandatory) |
| **Contains** | thought_blocks (≥200 words each), stakeholder_empathy, defensive_reasoning, META-2.1 signals |
| **Lifecycle** | Created at Stage 0, consumed by Stage 2-3 |
| **Validation** | META-2.1 binary gate (S1∧S2∧S3∧S4 = PASS) + YAML Resilience L1-L3 |

**Proposed Schema (frontmatter):**
```yaml
skill_name: "{target_skill}"
thought_blocks:
  - id: "tb-1"
    topic: "string"
    content: "string (>=200 words)"
    signals:
      s1_negation: true
      s2_reverse_question: true
      s3_multi_stakeholder: true
      s4_constraint_anchoring: true
stakeholder_empathy:
  - role: "string"
    pain: "string"
defensive_reasoning:
  - guardrail: "string"
    rationale: "string"
```

### 4.5 Data Flow Diagram (v1.0 Target)

```
User Input → skill-explorer (Stage 0)
  │
  ├─ Phase 1: Input & Intent  ─── Domain Anchoring (thought blocks)
  ├─ Phase 2: Golden Standards  ── Binary Gates (META-2.1) + SCS 2-phase
  ├─ Phase 2.5: Context Hydration ─ Create hydrated-context.yaml (NEW)
  ├─ Phase 3: Resource Gathering ─ YAML Resilience L1-L3
  ├─ Phase 3.5: Depth Verification ─ META-2.1 gate verification (NEW)
  └─ Phase 4: Synthesis & Deliver ─ Graceful Degradation check
       │
       ├── exploration.md          → skill-architect
       ├── hydrated-context.yaml    → skill-planner (mandatory), skill-builder (mandatory)
       ├── thought-cache.yaml       → skill-planner (optional), skill-builder (mandatory)
       └── criteria.md              → skill-tester
```

---

## §5: Gap Analysis Summary (v0.0.2 → v1.0)

### 5.1 7 LLM Principles — Gap Mapping

| # | Principle | v0.0.2 Status | v1.0 Required | Priority | Estimated Effort |
|:---:|:---|---|:---|:---:|:---:|
| 1 | **Domain Anchoring** | ❌ Thiếu thought blocks, glossary có nhưng không semantic anchors | Thêm `thought-cache.yaml`, thought blocks ≥200 từ, glossary 10+ terms trong SKILL boot | **HIGH** | **L** (new file + template) |
| 2 | **Semantic over Ceremony** | ⚠️ Template có sẵn nhưng thin content, thiếu data contracts | Thêm data contracts trong hydrated-context.yaml, binary gates thay soft checklist | **HIGH** | **M** (restructure existing) |
| 3 | **Context Pre-processing** | ❌ Không có hydration step giữa Resource Gathering và Synthesis | Thêm Phase 2.5: Context Hydrator trong workflow.md | **HIGH** | **M** (add workflow phase) |
| 4 | **Dual Knowledge Stream** | ❌ Single stream output (exploration.md only) | Tách thành 2 streams: hydrated-context.yaml (technical) + thought-cache.yaml (cognitive) | **HIGH** | **H** (new data model, templates, init, schema) |
| 5 | **Binary Mechanical Gates** | ❌ Checklist mềm (soft questions), không deterministic | META-2.1 (S1-S4) binary AND gates, YAML Resilience L1-L3, sampling audit | **MEDIUM** | **M** (replace checklist logic) |
| 6 | **Negative Space** | ⚠️ Có must_not cơ bản trong template §4, thiếu anti-patterns riêng | Thêm anti-patterns section (6 items), S1 Negation gate | **MEDIUM** | **L** (add section + gate) |
| 7 | **Graceful Degradation** | ❌ Không có fallback matrix, pipeline hard halt khi fail non-critical | Fallback matrix subset F1-F19, max 3 iterations, append-only history | **MEDIUM** | **M** (new fallback logic) |

### 5.2 Effort Summary

| Effort Level | Count | Items |
|:---:|:---:|:---|
| **HIGH** (complex, multi-file) | 1 | Dual Knowledge Stream (#4) — affects output-spec, templates, init, schema, validators |
| **MEDIUM** (moderate changes) | 4 | Semantic (#2), Context Pre-processing (#3), Binary Gates (#5), Graceful Degradation (#7) |
| **LOW** (new file/section) | 2 | Domain Anchoring (#1), Negative Space (#6) |

### 5.3 Risk Assessment

| Risk | Level | Mitigation |
|:---|---|:---|
| Downstream breaking change (Q1, Q2) | **🔴 HIGH** | Verify exploration.schema.yaml và skill-architect SKILL.md trước khi design output schema |
| init_context.py dual artifact logic | **🟡 MEDIUM** | Template-based approach, không hardcode path |
| META-2.1 false positives (regex) | **🟡 MEDIUM** | Binary gate is mechanical check, không thay thế human review |
| YAML Resilience L1-L3 infinite loop | **🟢 LOW** | Cap auto-repair at 2 attempts, then Hard Halt |
| Schema backward compat (Q3, Q4) | **🟡 MEDIUM** | Giữ exploration.md làm report tổng, add don't replace |

---

## §6: Architect Action Items (Pre-Design)

Before Stage 1 can complete the architecture design, the following MUST be resolved:

| # | Action | Depends On | BLOCKER? |
|:---:|---|:---:|:---:|
| A1 | Locate and read `_shared/schemas/exploration.schema.yaml` thực tế | File discovery | ✅ YES |
| A2 | Locate and read `skill-architect/SKILL.md` để verify input format hiện tại | File discovery | ✅ YES |
| A3 | Quyết định output strategy (Q3): giữ exploration.md + 2 artifact mới vs thay thế hoàn toàn | Team decision | ✅ YES |
| A4 | Quyết định schema strategy (Q4): schema riêng cho thought-cache.yaml hay dùng chung | Team decision | ⚠️ Only if Q3=replace |
| A5 | Xác nhận implement scope (Q6): subset F1-F5+F19 vs full F1-F19 | Team decision | No |
| A6 | Xác nhận SCS 2-phase (Q5): optional cho v1.0 hay mandatory | Team decision | No |

**NOTE**: A1-A3 are hard blockers. Architect cannot finalize data contracts without knowing:
- Existing schema constraints (A1)
- Downstream consumer format expectations (A2)
- Whether output strategy is additive or replacement (A3)

---

## §7: Summary — Key Statistics

| Metric | Value |
|:---|---|
| Total FRs | 20 (FR-01 → FR-20) |
| Total NFRs | 10 (NFR-01 → NFR-10) |
| P0-CRITICAL priority | 6 (FR-01,02,03,04,12,16,20) + NFR-09 |
| P1-HIGH priority | 10 (FR-05→09,13,15,19) + NFR-01→04,07,08 |
| P2-MEDIUM priority | 7 (FR-10,11,14,17,18) + NFR-05,06,10 |
| Open questions | 8 (Q1-Q8) |
| Blocker questions | 3 (Q1, Q2, Q3 → Q4 dependent) |
| Files to modify | 7 existing files |
| Files to create | 2 new templates |
| Indirectly affected | 6 components |
| Gap analysis principes | 7/7 need changes |
| Overall confidence | 82% (medium-high) until Q1-Q3 resolved |

---

*Generated from: scope.2026-07-11.md (347 lines) + domain-handbook.md (283 lines)*
*⚠️ business-analysis.md was NOT FOUND (empty/zero bytes) — verify this file if additional business context is needed*
