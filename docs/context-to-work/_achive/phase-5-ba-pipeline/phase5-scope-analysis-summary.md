# Phase 5 BA Pipeline — Phân Tích Scope Documents

**Generated**: 2026-07-10
**Source files analyzed**:
- `scope.ba-elicitor-build.2026-07-10.md` (683 lines)
- `scope.ba-analyst.2026-07-10.md` (577 lines)
- `scope.ba-synthesizer.2026-07-10.md` (841 lines)
- `phase-5-ba-pipeline-business-analysis.md` (291 lines)

---

## (1) Cấu trúc 7-Zone Skill Design

Mỗi skill trong Phase 5 (ba-elicitor, ba-analyst, ba-synthesizer) được triển khai theo **7-Zone structure** chuẩn hóa:

| Zone | Directory | Nội dung | Mục đích |
|:----:|:----------|:---------|:---------|
| **1 — Core** | `SKILL.md` | Frontmatter (10-11 fields) + 8 XML sections (instructions, safety_contract, knowledge_anchors, workflow_phases, input_contract, output_contract, acceptance_criteria, failure_modes) | L0 anchor rules, ranh giới hoạt động, định tuyến. Token limit ≤700 tokens (~800 words). |
| **2 — Knowledge** | `knowledge/` | 1 file duy nhất per skill. Merged từ nhiều file old v0.0.2. | Tri thức nghiệp vụ cốt lõi (taxonomy FR/NFR, Mermaid rules, cross-validation rules). Chống phân mảnh ngữ nghĩa. |
| **3 — Templates** | `templates/` | Báo cáo mẫu dạng WORM (Write Once Read Many) với YAML frontmatter chuẩn hóa. | Output artifact templates, align với schema dữ liệu. |
| **4 — Loop** | `loop/` | Checklist tự đánh giá chất lượng (weighted scoring). | Cơ chế tự đóng gói chất lượng đầu ra, gate policy. |
| **5 — Scripts** | `scripts/` | Python validator scripts chạy local. | Kiểm tra cú pháp và cấu trúc dữ liệu tự động. |
| **6 — Data** | `data/drc.yaml` | Dynamic Routing Contract (DRC) — hợp đồng định tuyến động. | Định nghĩa luồng dữ liệu vào/ra, ràng buộc kiểu, cơ chế fallback. |
| **7 — Assets** | `assets/` | Tài nguyên bổ trợ tĩnh. | Giai đoạn đầu chỉ cần `.gitkeep`. |

**Chi tiết per skill**:

| Skill | Files | Old source | New content | Reuse rate |
|:------|:-----:|:----------:|:-----------:|:----------:|
| ba-elicitor | 7 files (~450 dòng) | 9 files, ~530 dòng | validate_outputs.py + thought_cache_template.yaml + drc.yaml | ~81% |
| ba-analyst | 6 files (~550 dòng) | 7 files, ~465 dòng | validate_metrics.py + drc.yaml | ~75% |
| ba-synthesizer | 6 files (~430 dòng) | 5 files, ~332 dòng | check_congruence.py + drc.yaml | ~84% |

---

## (2) Quy trình Merge 5 Knowledge Files → 1

### ba-elicitor: `elicitation_patterns.md`
```
5 old files (354 dòng) → 1 merged file (120-150 dòng target)
  ├── §1: "Elicitation Rules & Master Prompt Architecture"   ← elicitation-rules.md (81 dòng)
  ├── §2: "Normalization & NFR Quantification Logic"          ← normalization-logic.md (40 dòng)
  ├── §3: "5W1H Elicitation Framework"                        ← question-framework.md (77 dòng)
  ├── §4: "6 Critical Thinking Mindset Keywords"              ← mindset-keywords.md (98 dòng)
  └── §5: "Scope Definition & Handoff Contract"               ← scope-definition.md (58 dòng)
```

### ba-analyst: `fr_nfr_taxonomy.md`
```
5 old files → 1 merged file (~200-250 dòng)
  ├── §FR/NFR: classification-rules.md (89 dòng) — Taxonomy + MoSCoW
  ├── §Gherkin: gherkin-guide.md (102 dòng) — User Story + 3-path
  ├── §Mermaid: mermaid-syntax.md (153 dòng) — Safety Rules + 4 diagram types
  └── §Risk: risk-assessment.md (74 dòng) — Risk Matrix + MoSCoW integration
```

### ba-synthesizer: `cross_validation_strategies.md`
```
3 old files → 1 merged file (~100-120 dòng)
  ├── §Actor-Entity matching rules         ← cross-ref-rules.md (51 dòng)
  ├── §MoSCoW-Gherkin matching rules       ← cross-ref-rules.md
  ├── §Quality criteria (7 deliverables)   ← quality-criteria.md (60 dòng)
  └── §Quality matrix embed (YAML block)   ← quality-matrix.yaml (45 dòng)
```

**Rủi ro khi merge**:
- Mất context khi gộp (Medium) — giải pháp: section headings rõ ràng
- Outdated references (`thong-tin-mau.md`, `raw2.md`) — cần grep trước merge
- `${VARIABLE}` syntax sót — cần grep pattern `\$\{`
- Giảm từ 354 dòng xuống 120-150 dòng (giảm ~60%) để tránh tràn context

---

## (3) Các Failure Modes Hiện Tại Của Pipeline

### F1-F6 từ ba-pipeline-runner agent (Stage 1-3):
| ID | Failure Mode | Mô tả | Stage |
|:--:|:-------------|:------|:-----:|
| **F1** | **Missing skill** | BA skill chưa được build (Phase 5). Cannot dispatch stage. | Dispatch |
| **F2** | **Missing artifact** | Artifact đầu ra của stage trước không tồn tại (ví dụ: `elicitation-report.md` missing khi chạy ba-analyst). | Gate check |
| **F3** | **Timeout** | Skill invocation timeout — pipeline bị block. | Runtime |
| **F4** | **Invalid feature name** | Tên feature sai format (kebab-case không hợp lệ). | Input validation |
| **F5** | **Schema validation fail** | Output artifact không pass `schema_validator.py`. | Quality gate |
| **F6** | **Ambiguous context** | Ngữ cảnh quá mơ hồ, không đủ để skill xử lý. | Input validation |

### Failure modes mở rộng per skill (từ scope documents):
- **SKILL.md > 700 tokens (800 words)** — L0 anchor rule violation
- **quality-scorer threshold < 70%** — không đạt META-1→3 scoring
- **Cascading failure** — nếu `business-analysis.md` lỗi, Phase 6 (skill-explorer) không có đầu vào chuẩn → lỗi dây chuyền
- **Self-verification gate fail** — weighted scoring không đạt 100% pass → output không được ghi
- **DRC contract sai** — schema path sai hoặc missing fields
- **Recursive spawning** — `ba-pipeline-runner` gọi chính nó (blocked bởi Hook anti-recursion)

---

## (4) Cách Skills, Agents, Hooks Kết Hợp Trong Phase 5

### Kiến trúc 3 lớp:

```
┌──────────────────────────────────────────────────┐
│                   USER / DEVELOPER                │
└──────────────────┬───────────────────────────────┘
                   │
┌──────────────────▼───────────────────────────────┐
│  AGENTS (Orchestration & Quality)                 │
│                                                   │
│  ba-pipeline-runner (Pipeline Orchestrator)       │
│    - Dispatch Stage 1 → ba-elicitor (Task)        │
│    - Gate check elicitation-report.md             │
│    - Dispatch Stage 2 → ba-analyst (Task)         │
│    - Gate check analysis-report.md                │
│    - Dispatch Stage 3 → ba-synthesizer (Task)     │
│    - Gate check business-analysis.md              │
│    - Error handling F1-F6                         │
│                                                   │
│  quality-scorer (Quality Gatekeeper)              │
│    - META-1: domain anchor density (0-5)          │
│    - META-2.1: semantic depth (S1-S4)             │
│    - META-2.1: must_not ≥5 constraint entries     │
│    - META-3: verification framework               │
│    - Threshold ≥70% per skill                     │
└──────────────────┬───────────────────────────────┘
                   │
┌──────────────────▼───────────────────────────────┐
│  SKILLS (Business Logic — 7-Zone each)            │
│                                                   │
│  ba-elicitor → elicitation-report.md              │
│    + thought-cache.yaml                           │
│         │                                         │
│         ▼                                         │
│  ba-analyst → analysis-report.md                  │
│         │                                         │
│         ▼                                         │
│  ba-synthesizer → business-analysis.md            │
│         │                                         │
│         ▼                                         │
│  Phase 6: skill-explorer                          │
└──────────────────┬───────────────────────────────┘
                   │
┌──────────────────▼───────────────────────────────┐
│  HOOKS (System-level Guardrails)                  │
│                                                   │
│  PreToolUse (Write):                              │
│    - Path confinement: chỉ được ghi vào            │
│      .skill-context/{feature}/ba-*/               │
│    - Block write outside zone → exit 2            │
│                                                   │
│  PreToolUse (Task):                               │
│    - Anti-recursion: chặn ba-pipeline-runner      │
│      spawning lồng nhau → exit 2                  │
│                                                   │
│  Stop / SubagentStop:                             │
│    - Self-healing loop (continueOnBlock: true)     │
│    - Kiểm tra output artifact validity            │
│    - Trả về ok:false + reason nếu lỗi             │
│    - Runtime nạp lại lỗi vào context turn kế tiếp  │
└──────────────────────────────────────────────────┘
```

### Hook Configuration:
- **Dual placement**: trong `ba-pipeline-runner.md` (bảo vệ ranh giới ghi) + trong frontmatter YAML của từng SKILL.md (quản lý vòng đời, self-healing)
- **continueOnBlock: true** — không tắt session khi lỗi, cho phép self-healing iteration

### Build-Verify-Fix Interleaved Process:
```
Xây dựng ba-elicitor → validate_outputs.py + quality-scorer → Fix → PASS
    ↓
Xây dựng ba-analyst → validate_metrics.py + quality-scorer → Fix → PASS
    ↓
Xây dựng ba-synthesizer → check_congruence.py + quality-scorer → Fix → PASS
    ↓
Pipeline test (ba-pipeline-runner) → full end-to-end
    ↓
Deploy cả 3 skills + update registry
```

---

## (5) Các Pain Points Về Chất Lượng Đầu Ra LLM

### 5.1 Quality-Scorer "Chấm Điểm Vô Hồn"
- **META-2.1 negation density**: yêu cầu `must_not ≥5` constraint entries — nhưng LLM dễ generate must_not giả tạo, không phản ánh real constraints
- **Threshold 70% chưa được test**: chưa dry-run quality-scorer với BA skill content thực tế → không biết strictness level
- **S1-S4 semantic depth signals**: 4 signals chưa được calibration cho BA domain
- **Thiếu correlation giữa điểm số và chất lượng thực tế**: skill đạt 70% có thể vẫn thiếu depth

### 5.2 LLM Output Thiếu Chiều Sâu (Shallow Output)
- **Anti-hallucination rules không đủ mạnh**: chỉ dùng stop conditions với confidence threshold, không có cơ chế fact-checking
- **5W1H questioning có thể hình thức**: LLM có thể generate câu hỏi multiple-choice nhưng thiếu real business insight
- **NFR quantification mapping mơ hồ**: từ `"nhanh" → latency`, `"mượt" → response time` — mapping quá đơn giản, thiếu context-specific quantification
- **Template placeholders sót**: `${VARIABLE}` syntax cũ chưa được convert hết → output chứa placeholder

### 5.3 Thiếu Cơ Chế Self-Healing Thực Sự
- **Self-verification gate 100% pass**: yêu cầu pass tất cả QC criteria trước khi ghi file — nhưng nếu fail, quay lại Phase 3 (5W1H questioning) — mà không có cơ chế phân tích *tại sao* fail
- **continueOnBlock: true** trong Hook chỉ retry chứ không có adaptive strategy
- **Không có learning loop**: fail ở iteration N không cải thiện iteration N+1

### 5.4 Vấn Đề Token Budget
- **SKILL.md ≤ 700 tokens**: constraint tốt cho separation of concerns, nhưng dễ dẫn đến thiếu depth trong instructions nếu không tối ưu
- **LLM dễ vượt token limit**: đặc biệt khi generate Mermaid diagrams + Gherkin scenarios trong cùng một turn

### 5.5 Quality Threshold Conflict
- **Internal threshold vs external threshold**: ba-synthesizer internal scoring threshold 0.80, quality-scorer threshold 70% — có thể conflict nếu internal PASS nhưng external FAIL
- **7 deliverables model vs synthesis schema**: old model tính 7 điểm, schema mới yêu cầu `synthesized_requirements`, `congruence_check`, `pipeline_ready` — mapping chưa rõ ràng

### 5.6 Lack of Business Depth Correlation
- **Confidence breakdown trong thought-cache**: 5-section thought-cache (business_thought_process, stakeholder_empathy, reverse_questions, confidence_breakdown, uncertainty_areas) — nhưng confidence_breakdown chỉ là self-assessment của LLM, không có external validation
- **Trace tags `[TỪ INPUT]/[SUY LUẬN]/[CẦN LÀM RÕ]`**: là semantic anchors tốt, nhưng LLM có thể gắn tags sai
- **Reverse questions coverage ≥4 aspects (S2)**: requirement hình thức, không đảm bảo chất lượng questions

---

## (6) Mối Quan Hệ Giữa 3 Skills (Elicitor → Analyst → Synthesizer)

### Data Flow Chain
```
Raw user request (XML: <user_skill_request>)
    │
    ▼
┌─────────────────────────────────────────────────┐
│ ba-elicitor (Stage BA-1) — "Khơi gợi & Chuẩn hóa"│
│                                                   │
│ Phase 1: Normalization (lọc nhiễu, bóc tách)      │
│ Phase 2: Gap Analysis (6 mindset keywords)         │
│ Phase 3: 5W1H Questioning (3-path decomposition)  │
│ Phase 4: Self-verification (7 QC criteria)        │
│                                                   │
│ Output: elicitation-report.md + thought-cache.yaml│
└─────────────────────┬─────────────────────────────┘
                      │ consumes elicitation-report.md
                      ▼
┌─────────────────────────────────────────────────┐
│ ba-analyst (Stage BA-0.5) — "Phân tích & Thiết kế"│
│                                                   │
│ Phase 1: Alignment (metadata sync, status check) │
│ Phase 2: Classification (FR/NFR + MoSCoW)        │
│ Phase 3: Diagram Generation (Seq/Flow/ERD)        │
│ Phase 4: Data Schema Design (JSON Schema)         │
│ Phase 5: Gherkin Scenarios (3-path coverage)      │
│ Phase 6: Risk Assessment (P×I matrix)             │
│                                                   │
│ Output: analysis-report.md                        │
└─────────────────────┬─────────────────────────────┘
                      │ consumes BOTH upstream outputs
                      ▼
┌─────────────────────────────────────────────────┐
│ ba-synthesizer (Stage BA-0.2) — "Hợp nhất &     │
│                       Kiểm định chéo"            │
│                                                   │
│ Phase 1: Cross-Validation                         │
│   ├── Actor-Entity Matching (Seq vs ERD)          │
│   └── MoSCoW-Gherkin Matching (Must-have vs test) │
│ Phase 2: Quality Scoring (7 deliverables × weight)│
│ Phase 3: Synthesis (merge + dedup)                │
│ Phase 4: Self-check (14-item congruence checklist)│
│                                                   │
│ Output: business-analysis.md ★ PHASE 6 INPUT      │
└─────────────────────┬─────────────────────────────┘
                      ▼
            Phase 6: skill-explorer
```

### Contract Dependencies

| Skill | Input | Output | Schema | Script Validator |
|:------|:------|:-------|:-------|:----------------|
| **ba-elicitor** | Raw user request (XML) | `elicitation-report.md` + `thought-cache.yaml` | `elicitation.schema.yaml` (5 required fields) | `validate_outputs.py` (8 criteria) |
| **ba-analyst** | `elicitation-report.md` | `analysis-report.md` | `analysis.schema.yaml` (4 required fields) | `validate_metrics.py` (8 criteria) |
| **ba-synthesizer** | `elicitation-report.md` + `analysis-report.md` + (optional `thought-cache.yaml`) | `business-analysis.md` | `synthesis.schema.yaml` (4 required fields) | `check_congruence.py` (6 checks) |

### Semantic Relationship

```
ba-elicitor          →  WHAT & WHY (khơi gợi nhu cầu, xác định vấn đề)
ba-analyst           →  HOW (phân tích, thiết kế, đặc tả kỹ thuật)
ba-synthesizer       →  VERIFY (kiểm định chéo, đảm bảo consistency)
```

### Key Design Decisions in the Chain:
1. **WORM lifecycle**: mỗi artifact chỉ ghi 1 lần, không sửa — đảm bảo traceability
2. **DRC contracts**: mỗi skill có hợp đồng định tuyến riêng, xác định rõ upstream/downstream
3. **Quality gate kép**: internal (self-verification checklist) + external (quality-scorer META)
4. **Self-healing loop**: `continueOnBlock: true` cho phép sửa lỗi qua nhiều iteration, nhưng **thiếu adaptive strategy** — cùng một cách tiếp cận cho mọi lỗi
5. **Separation of concerns**: ba-pipeline-runner chỉ dispatch, không xử lý nội dung; quality-scorer chỉ chấm điểm, không viết content

### Pipeline Failure Cascade:
```
ba-elicitor fail (F1/F2) → no elicitation-report.md
    → ba-analyst không có input → fail F2
        → ba-synthesizer không có cả 2 input → fail F2
            → business-analysis.md không được tạo
                → Phase 6 skill-explorer không có input → **CASCADING FAILURE**
```

---

## Tổng Hợp Pain Points Chính

| # | Pain Point | Severity | Scope | Giải pháp đề xuất |
|:--:|:-----------|:--------:|:-----:|:-----------------|
| PP1 | Quality-scorer chấm điểm vô hồn, threshold 70% chưa calibrated | 🔴 High | Cả 3 skills | Dry-run quality-scorer trên skeleton trước; define domain-specific META criteria |
| PP2 | LLM output thiếu chiều sâu, NFR quantification mapping đơn giản | 🔴 High | ba-elicitor | Thêm context-specific quantification rules; dùng số liệu thực tế thay vì mapping mơ hồ |
| PP3 | Self-healing loop thiếu adaptive strategy | 🟡 Medium | Cả pipeline | Log which QC criteria fail → adaptive retry strategy (không chỉ re-ask 5W1H) |
| PP4 | Template placeholders sót (`${VARIABLE}` → `{{var}}`) | 🟡 Medium | Cả 3 skills | Grep pattern `\$\{` trước deploy; auto-detect placeholder trong validator |
| PP5 | Token budget 700 tokens quá tight cho skill phức tạp | 🟡 Medium | Cả 3 skills | Tối ưu separation of concerns: extract càng nhiều vào knowledge/ càng tốt |
| PP6 | Merge 5→1 knowledge file dễ mất traceability | 🟡 Medium | Cả 3 skills | YAML sub-sections rõ ràng, maintain table of contents |
| PP7 | No learning loop giữa các pipeline runs | 🟡 Medium | Cả pipeline | Store failure patterns trong thought-cache để iteration sau tham khảo |
| PP8 | Internal threshold (0.80) vs external (70%) có thể conflict | 🟢 Low | ba-synthesizer | Document rõ: internal cho quality scoring, external cho deploy gate |
| PP9 | Recursive spawning guard chỉ block chứ không repair | 🟢 Low | Hooks | Thêm repair suggestion khi block (ví dụ: "Use Task with different agent") |
| PP10 | assets/ zone không có content → chỉ đạt 6/7 zones | 🟢 Low | Cả 3 skills | Thêm diagram mẫu hoặc .gitkeep (hiện tại AC chỉ yêu cầu ≥4 zones) |

---

**Document Status**: Analysis Complete — 6 extraction points mapped in detail
**File Path**: `docs/context-to-work/phase-5-ba-pipeline/phase5-scope-analysis-summary.md`
