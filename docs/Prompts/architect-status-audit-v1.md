<instructions>

## Nhiệm vụ

Thực hiện **status audit** cho skill-architect rebuild (Phase 6A, Stage 1) — xác định trạng thái hiện tại của pipeline, đối chiếu với scope requirements, và báo cáo gap. Dừng trước design phase.

### Inputs bắt buộc đọc

1. **scope.2026-07-16.md** — Problem summary, scope/boundary, impact analysis, affected components, IQD spec
2. **synthesis-llm-principles.md** — 7 nguyên lý LLM cốt lõi, 4 Depth Signals (S1-S4), YAML Resilience L1-L3, Fallback Matrix
3. **standards.md** — Format conventions (XML boundaries, YAML constraints, token budgets), 4-layer knowledge model

### Constraints cứng

```yaml
must:
  - Đọc toàn bộ inputs trước khi audit — không skip bước nào
  - Đối chiếu từng affected component (§9.1) với thực tế trên disk
  - Xác định rõ: file nào có nội dung, file nào stub (0 bytes), file nào missing
  - Với mỗi zone (Core, Knowledge, Templates, Scripts, Loop, Data):
    - Trạng thái hiện tại
    - Những gì có thể kế thừa từ skills/ver-0.0.2/skill-architect/
    - Gap so với Phase 6A spec
    - Mức ưu tiên xử lý
  - Áp dụng 7 LLM principles từ synthesis-llm-principles.md vào đánh giá gap
  - Kiểm tra IQD thresholds từ scope §5.4 (glossary size, semantic density, binary gates)
  - Dùng YAML blocks cho constraints/policy
  - Dùng XML-like tags cho semantic boundaries
  - Mọi recommendation phải traceable: [TỪ SCOPE §N], [TỪ SYNTHESIS §N], [TỪ STANDARDS §N]
  - Output duy nhất: `.skill-context/skill-architect-rebuild/status-report.md`

must_not:
  - KHÔNG viết SKILL.md hay bất kỳ file skill zone nào
  - KHÔNG tạo file ngoài `.skill-context/skill-architect-rebuild/`
  - KHÔNG propose design decisions — chỉ report status + gap
  - KHÔNG chạy script hay modify codebase
  - KHÔNG merge technical và cognitive vào 1 artifact (anti-pattern: single-stream)
  - KHÔNG dùng soft checklist thay binary gates
  - KHÔNG để placeholder/TODO — nếu không xác định được, ghi rõ "unresolved" + lý do
  - KHÔNG tự quyết khi confidence <70% (phải ghi rõ "uncertain")

design_blockers:
  - id: A1
    description: "Xác định trạng thái thực tế của skills/ver-3/skill-architect/ — SKILL.md 0 bytes, các zone khác empty"
    severity: "HARD_BLOCKER"
    resolved_by: "file system check"
  - id: A2
    description: "Xác định inheritance mapping từ ver-0.0.2 — file nào giữ nguyên, file nào cần update cho Phase 6A"
    severity: "HARD_BLOCKER"
    resolved_by: "diff old vs new spec requirements"
  - id: A3
    description: "Xác định IQD gaps — scope §5.4 defines thresholds. Đo được không? Cần tools gì?"
    severity: "MEDIUM_BLOCKER"
    depends_on: [A1]
```

</instructions>

---

<context>

## §1. Tổng quan Pipeline Phase 6A

```yaml
phase_6a_discovery_cluster:
  status: in_progress
  skills:
    skill-explorer:           # Stage 0   — ✅ built (9765 bytes SKILL.md)
    skill-knowledge-miner:    # Stage 0.5 — ✅ built (4247 bytes SKILL.md)
    skill-architect:          # Stage 1   — ❌ stub (0 bytes SKILL.md)
    production-quality-gatekeeper: # Stage 1.5 — ❌ stub (0 bytes SKILL.md)
  completed_tasks: 3/12
  checkpoint: "quality-matrix.yaml aggregate ≥80% before Phase 6B"
```

### 1.1 Vị trí của skill-architect trong pipeline

```text
BA Pipeline (Stage -1 → -0.2)         [ba-elicitor ✅, ba-analyst ✅, ba-synthesizer ✅]
  ↓
skill-explorer (Stage 0)              [✅ built]
  ↓  exploration.md + criteria.md
skill-knowledge-miner (Stage 0.5)     [✅ built]
  ↓  domain-handbook.md
SKILL-ARCHITECT (Stage 1)             [← YOU ARE HERE — 0 bytes]
  ↓  design.md + drc-skill-architect.yaml
production-quality-gatekeeper (Stage 1.5) [❌ stub]
  ↓
[Phase 6B: planner → builder → code-reviewer → security-reviewer]
```

### 1.2 Kiến trúc hiện tại (ver-0.0.2 — As-Is)

```text
skills/ver-0.0.2/skill-architect/
├── SKILL.md                     # 3-phase model (Collect→Analyze→Design), 4915 bytes
├── knowledge/
│   ├── architect.md             # 3 Pillars framework
│   ├── design-exemplars.md      # Content spec, good/bad exemplars
│   └── visualization-guidelines.md  # Mermaid standards
├── policy/
│   ├── workflow.md              # 3-phase detail
│   ├── guardrails.md            # G1-G7
│   └── output-spec.md           # §1-§10 contract
├── loop/
│   ├── design-checklist.md      # Soft checklist
│   └── design-checklist.yaml    # YAML gates
├── templates/
│   └── design.md.template       # 10-section output
├── scripts/
│   ├── init_context.py          # Context initializer
│   └── export-pipeline.py       # Pipeline diagram generator
└── references/
    └── examples/                # Reference design examples
```

**Vấn đề:** Mô hình cũ (3-phase, G1-G7, 7 guardrails, single-stream output) **không tương thích** với spec Phase 6A mới (6-phase, META-driven, quantified ACs, dual-stream).

### 1.3 Target architecture (ver-3 — To-Be per scope)

```yaml
v3_target:
  zones: 7  # Core, Knowledge, Templates, Scripts, Loop, Data, Assets
  phases: 6  # Read → Zone Mapping → Data Contracts → State Diagram → Must-Not Rules → Emit
  acs: 6     # 7-zone table, ≥1 Mermaid, ≥5 must_not/phase, ≥4 reverse Q, ≥2 stakeholders, constraint anchoring
  token_budget: "≤700 tokens (~2800 chars body)"
  outputs:
    - ".skill-context/{target_skill}/design.md"
    - "data/drc-skill-architect.yaml"
```

</context>

---

<quality_framework>

## §2. Quality Framework (từ synthesis-llm-principles.md + scope §5)

### 2.1 7 LLM Principles — Checklist đánh giá gap

| # | Nguyên lý | Hiện trạng ver-0.0.2 | Target ver-3 | Gap |
|:-:|:----------|:---------------------|:-------------|:----|
| 1 | Domain Anchoring | Thiếu thought blocks, glossary not quantified | Thought blocks >200 từ, glossary ≥10 terms | [Cần xác định] |
| 2 | Semantic over Ceremony | Yếu — thin content trong templates | Hydrated context, binary gates, data contracts | [Cần xác định] |
| 3 | Context Pre-processing | Không có hydration step | Phase 2 → Context Hydrator | [Cần xác định] |
| 4 | Dual Knowledge Stream | Single-stream output | hydrated-context + thought-cache riêng | [Cần xác định] |
| 5 | Binary Mechanical Gates | Soft checklist (G1-G7) | META-1/2/3 + ARCH-1→4 binary gates | [Cần xác định] |
| 6 | Negative Space | must_not cơ bản trong instructions | must_not lists, anti-patterns, S1 density | [Cần xác định] |
| 7 | Graceful Degradation | Không có fallback | Degraded modes per artifact, fallback F3/F8/F9 | [Cần xác định] |

### 2.2 IQD Thresholds (scope §5.4) — Đo lường gap

```yaml
iqd_checks:
  domain_anchoring:
    - metric: "Glossary size"
      threshold: "≥10 domain-specific terms"
      artifact: "knowledge/architect.md"
    - metric: "Semantic anchor density"
      threshold: "≥1 anchor per 200 tokens"
      artifact: "design.md (all sections)"
    - metric: "Dual anchor types"
      threshold: "Both technical + stakeholder"
      artifact: "design.md §1 + §7"

  semantic_density:
    - metric: "Keyword density (technical)"
      min: 30%  target: 40%  max: 60%
    - metric: "Meaningful content ratio"
      min: 60%  target: 75%  max: 100%

  binary_gates:
    - gate: "META-1 Structural"
      pass: "Domain anchor present + 6 phases"
    - gate: "META-2 Semantic Depth"
      pass: "4/4 Depth Signals (S1 AND S2 AND S3 AND S4)"
    - gate: "META-3 Mechanical"
      pass: "PASS/FAIL gates pass, negative space present"

  depth_signals:
    s1_negation_density: "≥5 must_not rules/phase"
    s2_reverse_question: "≥4 reverse questions/aspect"
    s3_multi_stakeholder: "≥2 stakeholders"
    s4_constraint_anchoring: "Token budget ≤700, NFR constraints"
```

### 2.3 Inconsistencies cần resolve (scope §5.3)

1. **Section count**: Old template §1-§12 vs spec §1-§10 — resolve: giữ §1-§10
2. **Template bugs**: Old §8 chỉ 1 risk row (cần ≥3). §6 chỉ 1 interaction point
3. **Checklist format**: Cả .md lẫn .yaml — retain cả 2
4. **Confidence/K=8**: Cơ chế heuristic cũ — giữ nguyên hoặc generalize
5. **Token budget**: 700 soft gate vs design-exemplars nói 1500-2500 — align với BUILD-3.1

</quality_framework>

---

<output_contract>

## §3. Output Contract — status-report.md

File duy nhất tại `.skill-context/skill-architect-rebuild/status-report.md`

### Required Sections

| § | Section | Format | Content |
|:-:|:--------|:-------|:--------|
| 1 | Pipeline Status | YAML table | Stage → status → SKILL.md size → notes |
| 2 | Zone Readiness Matrix | Markdown table | Zone → file → status → gap → action | 7 zones: Core, Knowledge, Templates, Scripts, Loop, Data, Assets |
| 3 | Inheritance Mapping | Markdown table | ver-0.0.2 file → keep? → update needed? → Phase 6A delta |
| 4 | IQD Gap Analysis | YAML + notes | Per §2.2 IQD thresholds — đạt/chưa/không đo được |
| 5 | LLM Principles Gap | Table | Per §2.1 — principle → hiện trạng → target → gap → priority |
| 6 | Inconsistencies Status | YAML | Per §2.3 — resolved/unresolved + recommendation |
| 7 | Next-Step Recommendation | Ordered list | Priority-ordered actions, blockers, dependencies, estimated effort |
| 8 | Metadata | YAML | Confidence per assessment, flags, open issues |

### Format Rules (per standards.md)

```yaml
format_rules:
  yaml_for: [constraints, policy, checklists, metrics, contracts]
  markdown_for: [explanation, rationale, comparison tables]
  xml_like_tags: [semantic boundaries between sections]
  token_budget:
    status_report_total: "~1500-2500 tokens"     # L2 domain context
    yaml_blocks: "≤700 tokens each"
    explanation_prose: "≤400 tokens per section"
```

### Định nghĩa "Done" cho status-report.md

```yaml
definition_of_done:
  - [] Mỗi affected component từ scope §9.1 được kiểm tra thực tế
  - [] Mỗi IQD threshold từ scope §5.4 được đánh giá (pass/fail/unmeasurable)
  - [] Mỗi LLM principle từ synthesis-llm-principles.md được map vào gap
  - [] Format tuân thủ standards.md: XML boundaries + YAML constraints + token budget
  - [] Zero placeholder/TODO — unresolved items ghi rõ lý do
  - [] Mọi claim có trace tag [TỪ NGUỒN]
  - [] Recommendation có priority, blocker flag, và effort estimate
```

</output_contract>

---

<stop_conditions>

## §4. Stop Conditions

```yaml
stop_immediately:
  - condition: "Output file written to .skill-context/skill-architect-rebuild/status-report.md"
    action: "Báo cáo hoàn tất, không tiếp tục design"
  - condition: "User yêu cầu dừng hoặc chuyển hướng"
    action: "Tuân thủ ngay"

do_not_proceed:
  - "KHÔNG viết SKILL.md — user tự làm design phase thủ công"
  - "KHÔNG tạo skill zone files (knowledge/templates/loop/scripts/data)"
  - "KHÔNG modify codebase ngoài .skill-context/skill-architect-rebuild/"
  - "KHÔNG run script hay thực thi code"
  - "KHÔNG commit/push thay đổi"
```

</stop_conditions>
