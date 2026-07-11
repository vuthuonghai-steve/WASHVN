# skill-explorer v1.0 — Cẩm Nang Tri Thức Chuyên Môn (Domain Handbook)

> **Stage**: 0.5 (Knowledge Mining) — tiền đề build v1.0
> **Nguồn**: `skills/ver-0.0.2/skill-explorer` + `skills/ver-0.0.2/skill-knowledge-miner` + `synthesis-llm-principles.md` (7 nguyên lý LLM)
> **Mục đích**: Cấu trúc hóa tri thức đã khai thác để làm input cho Stage 1 (Architect) build skill-explorer v1.0
> **Ngày**: 2026-07-11

<context>
Cẩm nang này là bridging artifact giữa Stage 0 (Exploration — scope.2026-07-11.md) và Stage 1 (Architect).
Nó trích xuất: (1) cấu trúc thực tế của v0.0.2, (2) mapping 7 nguyên lý LLM → v0.0.2 (gap), (3) data contracts xác định
cho các artifact đầu ra mới. Architect dùng §2 để thiết kế, §3 để implement rules, §4 để test edge cases.
</context>

---

## §1. Bối Cảnh & Thuật Ngữ Chuyên Ngành

### A. Bối cảnh
skill-explorer là **Stage 0** trong 8-stage pipeline WASHVN — khảo sát nghiệp vụ, audit tài nguyên, đánh giá 7 Golden Standards,
tính SCS, và sinh `exploration.md` bàn giao cho skill-architect.

Mục tiêu v1.0: nâng cấp v0.0.1 (identical với v0.0.2 reference) bằng cách tích hợp **7 nguyên lý LLM cốt lõi** từ
`synthesis-llm-principles.md`. Điểm khác biệt cốt lõi: chuyển từ **single-stream output** (1 file `exploration.md`) sang
**dual-stream + metadata** (3 artifact: `exploration.md` + `hydrated-context.yaml` + `thought-cache.yaml`).

### B. Thuật ngữ (Glossary — 10+ terms, semantic anchors)

| Thuật ngữ | Định nghĩa | Nguồn |
|:---|:---|:---|
| **Domain Anchoring** | Neo LLM vào đúng không gian vector ngữ nghĩa trước khi suy luận (glossary, thought blocks, stakeholder empathy) | synthesis §2.1 |
| **Thought Block** | Phân tích nghiệp vụ sâu ≥200 từ, làm mỏ neo vector ngữ nghĩa; lưu trong `thought-cache.yaml` | synthesis §1.1 |
| **Hydrated Context** | Gói ngữ cảnh cô đặc (~30-50 dòng YAML): glossary, NFR, edge cases, data contracts, zone map, must_not | synthesis §4.2 |
| **Thought Cache** | Luồng cognitive depth (~100-200 dòng YAML): thought blocks, empathy, defensive reasoning | synthesis §1.3 |
| **Dual Context Ingestion** | Hai luồng song song: Technical (hydrated) + Cognitive (thought-cache), lifecycle/consumer khác nhau | synthesis §1.3 |
| **SCS (Skill Complexity Score)** | Điểm phức tạp 1.0-5.0; <3.0 Fast Track, ≥3.0 Full Track; có 2-phase (Stage 0.5 pre-pass + Stage 1.5 validate) | synthesis §2.2, explorer §3.A |
| **Binary Gate** | Gate nhị phân deterministic, verify bằng script (không thang điểm NLP) | synthesis §3.1 |
| **META-2.1** | 4 Depth Signals: S1 Negation, S2 Reverse Question, S3 Multi-Stakeholder, S4 Constraint. PASS ⇔ S1∧S2∧S3∧S4 | synthesis §2.4 |
| **Graceful Degradation** | Pipeline tiếp tục ở chế độ degraded thay vì Hard Halt với non-critical failures | synthesis §3.2-3.3 |
| **YAML Resilience (L1-L3)** | Middleware: L1 syntax lint, L2 schema validation, L3 cross-ref — auto-repair trước khi commit Context Bus | synthesis §3.4 |
| **Fallback Matrix (F1-F19)** | 19 fallback cases + 4 phase compression (PC-1..4); max 3 iterations/stage; append-only history | synthesis §3.3 |
| **Negative Space** | Dạy LLM điều KHÔNG nên làm: must_not lists, anti-patterns, guardrails, S1 | synthesis §4.5 |
| **Context Bus** | Shared state layer, Single Source of Truth giữa các stage stateless | CLAUDE.md §7 |
| **7 Golden Standards** | Reusability, Composability, Maintainability, Security, Context Efficiency, Portability, Reliability | explorer §3 |

---

## §2. Sơ Đồ Kiến Trúc & Data Specifications

### A. Cấu trúc thực tế v0.0.2 (đã xác nhận từ 13 files)

```
skill-explorer/
├── SKILL.md                     # Boot config, 4 phases, must/must_not (8 rules)
├── knowledge/
│   ├── exploration-standards.md # 7 Golden Standards + SCS table
│   └── security-standards.md    # Prompt Injection + Docker sandbox
├── policy/
│   ├── workflow.md              # 4-phase chi tiết
│   ├── guardrails.md            # G1-G5 guardrails (yaml)
│   └── output-spec.md           # 8-section output contract
├── loop/
│   └── exploration-checklist.md # Quality gate (soft questions)
├── templates/
│   └── exploration.md.template  # 8-section report + frontmatter
├── scripts/
│   └── init_context.py          # single_init + split_run
└── data/
    └── search-blacklist.yaml    # folders/files skip
```

### B. Data Contract — Output Artifacts (v1.0 target)

**Thay đổi cốt lõi**: từ 1 artifact → 3 artifact. Schema xác định:

```yaml
# Contract v1.0 — 3 artifacts (thay vì 1)
artifacts:
  - id: exploration_report
    path: ".skill-context/{target_skill}/exploration.md"
    format: markdown + frontmatter
    schema: "skills/ver-3/_shared/schemas/exploration.schema.yaml"
    consumer: ["skill-architect"]
  - id: hydrated_context
    path: ".skill-context/{target_skill}/hydrated-context.yaml"
    format: yaml
    size_budget: "30-50 lines"
    consumer: ["skill-planner (mandatory)", "skill-builder (mandatory)"]
    contains: ["glossary", "nfr", "edge_cases", "data_contracts", "zone_map", "must_not"]
  - id: thought_cache
    path: ".skill-context/{target_skill}/thought-cache.yaml"
    format: yaml
    size_budget: "100-200 lines"
    consumer: ["skill-planner (optional)", "skill-builder (mandatory)"]
    contains: ["thought_blocks(>200 words each)", "stakeholder_empathy", "defensive_reasoning"]
  - id: test_criteria
    path: ".skill-context/{target_skill}/criteria.md"
    format: markdown
    consumer: ["skill-tester"]
```

### C. Schema Frontmatter — hydrated-context.yaml (proposed)

```yaml
# hydrated-context.yaml — Technical Contracts stream
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

### D. Schema Frontmatter — thought-cache.yaml (proposed)

```yaml
# thought-cache.yaml — Cognitive Depth stream
skill_name: "{target_skill}"
thought_blocks:
  - id: "tb-1"
    topic: "string"
    content: "string (>=200 words)"   # META-2.1 anti-gaming anchor
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

### E. init_context.py Contract (v1.0 required change)

| Function | v0.0.2 behavior | v1.0 required |
|:---|:---|:---|
| `handle_single_init()` | tạo `exploration.md` + `resources/` | + tạo `hydrated-context.yaml` + `thought-cache.yaml` từ template |
| `handle_split_run()` | copy `resources/` xuống micro-skill | + copy cả `hydrated-context.yaml` + `thought-cache.yaml` |
| `parse_frontmatter()` | parse `exploration.md` | + parse dual artifacts (decomposed flag) |

### F. Open Questions chưa giải (từ scope §10 — CẦN user/stage 1 quyết)

| # | Câu hỏi | Liên quan |
|:---|:---|:---|
| Q1 | `exploration.schema.yaml` hiện tại có hỗ trợ multi-artifact không? | Schema compatibility |
| Q2 | skill-architect đọc `exploration.md` format nào? Có cần update? | Downstream breaking |
| Q3 | Giữ `exploration.md` làm report tổng + 2 artifact, hay thay thế hoàn toàn? | Output strategy |
| Q4 | `thought-cache.yaml` có schema riêng hay chung exploration.schema? | Schema design |
| Q5 | SCS: giữ single-pass (Stage 0) hay 2-phase (0.5 + 1.5)? | Pipeline redesign |
| Q6 | Implement bao nhiêu F1-F19 cho v1.0 (subset hay full)? | Scope sizing |
| Q7 | Binary gates META-2.1 implement ngay Stage 0 hay chỉ downstream? | Phasing |
| Q8 | Sampling audit rate 30% có phù hợp exploration stage? | Rate tuning |

---

## §3. Hướng Dẫn Lập Trình Tối Giản & Mã Mẫu

### A. Mapping 7 Nguyên Lý → v0.0.2 (GAP ANALYSIS)

| # | Nguyên lý | v0.0.2 Status | v1.0 Required | Priority | Evidence (file:line) |
|:---:|:---|:---|:---|:---:|:---|
| 1 | Domain Anchoring | ❌ Thiếu thought blocks | + `thought-cache.yaml`, glossary 10+ terms trong SKILL boot | HIGH | explorer/SKILL.md:12-27 (7 rules, không có thought blocks) |
| 2 | Semantic over Ceremony | ⚠️ Template có nhưng thin content | + data contracts, binary gates thay soft checklist | HIGH | exploration-standards.md:50-58 (Rich vs Thin) |
| 3 | Context Pre-processing | ❌ Không có hydration step | + Phase 2.5: Context Hydrator | HIGH | SKILL.md:73-104 (4 phases, không có hydrate) |
| 4 | Dual Knowledge Stream | ❌ Single stream | `hydrated-context.yaml` + `thought-cache.yaml` | HIGH | output-spec.md:10-25 (1 artifact) |
| 5 | Binary Mechanical Gates | ❌ Checklist mềm | META-2.1 (S1-S4), YAML Resilience L1-L3 | MEDIUM | exploration-checklist.md:7-28 (soft questions) |
| 6 | Negative Space | ⚠️ must_not cơ bản | + anti-patterns section, S1 gate | MEDIUM | template §4 (có must_not, thiếu anti-patterns riêng) |
| 7 | Graceful Degradation | ❌ Không có fallback | Fallback matrix (subset F1-F19) | MEDIUM | security-standards.md:1-48 (không có fallback) |

### B. Mã mẫu — init_context.py v1.0 (dual artifact init)

```python
# ponytail: snippet min tối, chưa chạy runtime. Upgrade path: tách template path thành dict.
def handle_single_init(skill_name, project_root, script_dir):
    skill_dir = project_root / ".skill-context" / skill_name
    skill_dir.mkdir(parents=True, exist_ok=True)
    (skill_dir / "resources").mkdir(exist_ok=True)

    # v1.0: 3 artifacts thay vì 1
    for art in ("exploration.md", "hydrated-context.yaml", "thought-cache.yaml"):
        tmpl = script_dir.parent / "templates" / art  # cần tạo 2 template mới
        if tmpl.is_file():
            content = replace_placeholders(tmpl.read_text(), replacements)
            safe_create_file(skill_dir / art, content)
    return 0
```

### C. Mã mẫu — Exploration Quality Gate (binary, META-2.1)

```python
# ponytail: regex-based mechanical gate, không NLP. Upgrade: tích hợp vào schema_validator.py
def meta_2_1_pass(thought_block: str) -> bool:
    s1 = "must_not" in thought_block.lower() or "không" in thought_block
    s2 = "?" in thought_block                        # reverse question marker
    s3 = any(role in thought_block for role in ("user", "dev", "agent", "người"))
    s4 = "constraint" in thought_block.lower() or "ràng buộc" in thought_block
    return s1 and s2 and s3 and s4                   # binary AND
```

### D. Integration Points (cut points cho builder)

| File cần sửa | Thay đổi | Ref principle |
|:---|:---|:---|
| `SKILL.md` | boot sequence: + thought block injection, dual context routing, binary gates config | #1,#4,#5 |
| `knowledge/exploration-standards.md` | mở rộng 7 Golden Standards + SCS 2-phase | #1,#3,#5 |
| `knowledge/security-standards.md` | + YAML Resilience L1-L3, sampling audit | #5,#7 |
| `policy/output-spec.md` | 3 artifacts thay 1 | #4 |
| `policy/workflow.md` | + Phase 2.5 (hydration), 3.5 (depth verify) | #3,#5 |
| `templates/exploration.md.template` | + hydrated-context + thought-cache refs | #4 |
| `loop/exploration-checklist.md` | binary gates + META-2.1 signals | #5,#6 |
| `scripts/init_context.py` | + init 2 artifacts | #4 |

---

## §4. Ranh Giới Xử Lý Lỗi & Các Trường Hợp Biên (Edge Cases)

### A. Anti-Patterns (từ Negative Space principle — ĐIỀU KHÔNG NÊN LÀM)

| Anti-pattern | Mô tả | Hậu quả |
|:---|:---|:---|
| **Single-stream output** | Gộp technical + cognitive vào 1 `exploration.md` | Planner phải mang depth dù không cần; phình to file |
| **Soft-only checklist** | Dùng câu hỏi mềm thay binary gate | LLM "tăng điểm" bằng padding; không verify được bằng script |
| **Thought block <200 từ** | Viết ngắn gọn thay vì deep analysis | Mất cognitive depth; LLM code đúng contract sai intent |
| **Hallucinate khi thiếu docs** | Đoán mò API/cấu trúc khi chưa có source | Builder implement sai; vi phạm KM must_not |
| **Edit workspace code** | Explorer sửa source ngoài `.skill-context/` | Vi phạm G1_DesignOnly guardrail |
| **Skip HITL khi confidence <70%** | Tự quyết thay hỏi user | Sai intent từ đầu; tốn chi phí rebuild |

### B. Edge Cases bắt buộc kiểm thử (cho Stage 4 Tester)

| # | Edge case | Expected behavior |
|:---|:---|:---|
| E1 | `skill_name` không phải kebab-case | `validate_skill_name()` reject; init_context báo lỗi |
| E2 | `.skill-context/{skill}/exploration.md`已 tồn tại | resume, KHÔNG overwrite (safe_create_file SKIPPED) |
| E3 | `init_context.py --split` trên exploration.md chưa `decomposed: true` | in info, return 0, không split |
| E4 | YAML frontmatter lỗi syntax | YAML Resilience L1 auto-repair (max 2 attempts) → fail → Hard Halt |
| E5 | Thought block thiếu 1/4 META-2.1 signal | Binary gate FAIL → WARNING (word<100) hoặc FAIL (thiếu signal) |
| E6 | Confidence khảo sát <70% | Dừng, hỏi user (G5_HumanInTheLoop) |
| E7 | Web fetch thất bại (network egress blocked) | Graceful degradation: dùng resources nội bộ, mark [CẦN LÀM RÕ] |
| E8 | `thought-cache.yaml` >200 dòng | Soft gate warning token budget, không block |
| E9 | Schema `exploration.schema.yaml` chưa update cho dual stream (Q1) | Validator fail → escalate lên stage 1 trước khi build |

### C. YAML Resilience Chain (áp dụng trước mọi commit Context Bus)

```
L1 Syntax:  yaml.safe_load()        → FAIL → auto-repair subagent (max 2)
L2 Schema:  required keys+types      → FAIL → auto-repair subagent (max 2)
L3 Cross-ref: path exists, non-empty → FAIL(critical) → Hard Halt
                                    → FAIL(non-critical) → Graceful degradation
```

### D. Validation Commands (mechanical verification)

```bash
# Frontmatter validation (hiện tại — cần update schema cho dual stream)
python3 skills/ver-3/_shared/validators/schema_validator.py \
  --schema skills/ver-3/_shared/schemas/exploration.schema.yaml \
  .skill-context/{target_skill}/exploration.md

# Mining self-check (Stage 0.5 gate)
# - 100% không có placeholder '...' / TODO trong domain-handbook.md
# - ≥3 sections chính (§1-§4)
# - mọi code example trong markdown code block có syntax highlight
```

---
> **Handbook status**: Mined from 14 source files. Ready for Stage 1 (Architect).
> **Confidence**: 82% (medium-high) — uncertainty flags tại §2.F (Q1-Q8) cần resolve trước build.
> **NO CODE CHANGES** — handbook only.
