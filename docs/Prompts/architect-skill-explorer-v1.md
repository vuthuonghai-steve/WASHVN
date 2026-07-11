# Architect Prompt: skill-explorer v1.0 — Architecture Design

> **Stage:** Stage 1 (Architect)
> **Target:** skill-explorer (Stage 0 of WASHVN 8-Stage Pipeline)
> **Input Source:** `.skill-context/skill-explorer-main-build/` (scope, domain-handbook, business-analysis)
> **Supporting Knowledge:** `synthesis-llm-principles.md`, `standards.md`
> **Ngày:** 2026-07-11

---

<instructions>

## Nhiệm vụ

Thiết kế kiến trúc cho **skill-explorer v1.0** — nâng cấp từ v0.0.2 (single-stream) lên v1.0 (dual-stream + 7 LLM principles).

### Inputs bắt buộc đọc

1. **scope.2026-07-11.md** — Problem summary, scope/boundary, impact analysis, affected components, open questions
2. **domain-handbook.md** — Data contracts (3 artifacts), schema frontmatter, gap analysis, edge cases, anti-patterns
3. **business-analysis.md** — 20 synthesized requirements (REQ-01→20: 10 FR + 10 NFR), pipeline readiness

### Outputs yêu cầu

Architect phải sinh **3 artifacts** vào `.skill-context/skill-explorer-main-build/`:

| Artifact | Path | Format | Consumer |
|----------|------|--------|----------|
| Architecture Design | `design.md` | Markdown + YAML + Mermaid | skill-planner, skill-builder |
| Zone Mapping | `zone-map.yaml` | YAML | skill-planner |
| Data Contracts | `data-contracts.yaml` | YAML | skill-builder, schema_validator |

### Constraints cứng

```yaml
must:
  - Đọc toàn bộ inputs trước khi thiết kế — không skip bước nào
  - Thiết kế dual-stream output: hydrated-context.yaml (30-50 dòng) + thought-cache.yaml (100-200 dòng)
  - Áp dụng 7 LLM principles từ synthesis-llm-principles.md vào architecture
  - Sinh data contracts cho 3 artifacts (exploration.md + hydrated-context + thought-cache)
  - Thiết kế zone mapping cho skill-explorer (core, knowledge, policy, loop, scripts, templates, data)
  - Đưa ra quyết định rõ ràng cho mọi Open Question (Q1-Q8) — KHÔNG để unresolved
  - Dùng Mermaid diagrams cho architecture, sequence, data flow
  - Dùng YAML cho constraints, contracts, policy
  - Dùng Markdown + XML-like tags cho explanation và rationale
  - Mọi design decision phải traceable: [TỪ SCOPE §N], [TỪ HANDBOOK §N], [TỪ BA REQ-N], [SUY LUẬN]

design_blockers:
  - id: A1
    description: "Xác định vị trí và đọc `_shared/schemas/exploration.schema.yaml` hiện tại — không design output schema nếu không biết giới hạn"
    severity: "HARD_BLOCKER"
    depends_on: [Q1]
  - id: A2
    description: "Đọc `skill-architect/SKILL.md` để verify input format hiện tại — architect sẽ fail nếu format thay đổi"
    severity: "HARD_BLOCKER"
    depends_on: [Q2]
  - id: A3
    description: "Quyết định output strategy (Q3): giữ exploration.md + 2 artifact mới (additive) vs thay thế hoàn toàn 3 artifact riêng"
    severity: "HARD_BLOCKER"
    depends_on: [Q3]
  - note: "A1-A3 PHẢI resolve trước khi design data contracts. Nếu blocker, dừng và hỏi user."

must_not:
  - KHÔNG viết prose dài >900 tokens mỗi section (standards.md token budget)
  - KHÔNG để placeholder '...' hoặc TODO trong output
  - KHÔNG edit source code ngoài `.skill-context/`
  - KHÔNG merge technical và cognitive vào 1 artifact (anti-pattern: single-stream output)
  - KHÔNG dùng soft checklist thay binary gates
  - KHÔNG tự quyết khi confidence <70% (phải hỏi user)
```

</instructions>

---

<context>

## §1. Tổng quan dự án

### 1.1 Vấn đề

skill-explorer là **Stage 0** trong 8-stage pipeline WASHVN. Nhiệm vụ: khảo sát nghiệp vụ, audit tài nguyên, đánh giá 7 Golden Standards, tính SCS, và sinh `exploration.md` bàn giao cho skill-architect.

### 1.2 Kiến trúc hiện tại (v0.0.2 — As-Is)

```
skill-explorer/
├── SKILL.md                     # Boot config, 4 phases, must/must_not (8 rules)
├── knowledge/
│   ├── exploration-standards.md # 7 Golden Standards + SCS table
│   └── security-standards.md    # Prompt Injection + Docker sandbox
├── policy/
│   ├── workflow.md              # 4-phase workflow
│   ├── guardrails.md            # G1-G5 guardrails
│   └── output-spec.md           # 8-section output contract
├── loop/
│   └── exploration-checklist.md # Quality gate (soft questions)
├── templates/
│   └── exploration.md.template  # 8-section report template
├── scripts/
│   └── init_context.py          # single_init + split_run
└── data/
    └── search-blacklist.yaml    # folders/files skip
```

**4 phases hiện tại:**
1. Phase 1: Input Acceptance & Intent Analysis
2. Phase 2: Golden Standards & Scale Assessment
3. Phase 3: Resource Gathering & Mining
4. Phase 4: Synthesis & Deliver

**Output hiện tại:** 1 artifact — `exploration.md` (single-stream)

### 1.3 Mục tiêu v1.0 (To-Be)

Chuyển từ single-stream → **dual-stream + metadata**:

```yaml
v1.0_output:
  - artifact: exploration.md
    format: "markdown + frontmatter"
    size: "comprehensive report (simplified)"
    consumer: [skill-architect]

  - artifact: hydrated-context.yaml
    format: "yaml"
    size: "30-50 dòng (ngắn gọn)"
    consumer: [skill-planner (mandatory), skill-builder (mandatory)]

  - artifact: thought-cache.yaml
    format: "yaml"
    size: "100-200 dòng (cognitive depth)"
    consumer: [skill-planner (optional), skill-builder (mandatory)]

  - artifact: criteria.md
    format: "markdown"
    consumer: [skill-tester]
```

### 1.4 Data flow change

```
v0.0.2:
  User Input → skill-explorer → exploration.md (single) → skill-architect

v1.0:
  User Input → skill-explorer
    ├── exploration.md (report)
    ├── hydrated-context.yaml (technical contracts ~30-50 dòng)
    └── thought-cache.yaml (cognitive depth ~100-200 dòng)
  → skill-architect (đọc cả 3)
```

</context>

---

<design_requirements>

## §2. Yêu cầu thiết kế

### 2.1 Functional Requirements (10 FR)

| # | Requirement | Priority | Source |
|:--|:------------|:--------:|:-------|
| REQ-01 | Map v0.0.2 architecture → 7 LLM principles | HIGH | scope + synthesis |
| REQ-02 | Gap Analysis 7 principles dạng MECE | HIGH | scope + synthesis |
| REQ-03 | Dual-stream output (hydrated-context + thought-cache) | HIGH | scope + synthesis |
| REQ-04 | Document only — no code/branch | HIGH | scope |
| REQ-05 | Standalone thought-cache.schema.yaml | HIGH | BA analysis [SUY LUẬN] |
| REQ-06 | 2 registry entries trong artifact_registry.yaml (WORM) | HIGH | BA analysis [SUY LUẬN] |
| REQ-07 | Binary Mechanical Gates META-2.1 (S1-S4 AND) | MEDIUM | BA analysis [SUY LUẬN] |
| REQ-08 | YAML Resilience Layer L1-L3 | MEDIUM | BA analysis [SUY LUẬN] |
| REQ-09 | Negative Space (must_not + anti-patterns + S1) | MEDIUM | BA analysis [SUY LUẬN] |
| REQ-10 | Graceful Degradation fallback matrix (F1-F4 subset) | MEDIUM | BA analysis [SUY LUẬN] |

### 2.2 Non-Functional Requirements (10 NFR)

| # | Requirement | Constraint | Source |
|:--|:------------|:-----------|:-------|
| REQ-11 | hydrated-context ≤ 50 lines | Hard gate | scope + analysis |
| REQ-12 | thought-cache 100-200 lines | Soft gate | scope + analysis |
| REQ-13 | L2_token_budget = 2200 tokens (hard) | Hard gate | BA analysis [SUY LUẬN] |
| REQ-14 | YAML Resilience 3 levels (L1 syntax, L2 schema, L3 cross-ref) | Hard design | BA analysis [SUY LUẬN] |
| REQ-15 | Binary gate 4 signals AND-deterministic | Hard design | BA analysis [SUY LUẬN] |
| REQ-16 | exploration.schema.yaml giữ additionalProperties:false | Hard constraint | scope + analysis |
| REQ-17 | Sampling audit default 30%, 100% on FAIL | Policy | BA analysis [SUY LUẬN] |
| REQ-18 | Max 3 iterations per stage | Policy | BA analysis [SUY LUẬN] |
| REQ-19 | Domain glossary ≥ 10 terms | Hard design | BA analysis [SUY LUẬN] |
| REQ-20 | Mỗi thought block ≥ 200 words | Hard design | BA analysis [SUY LUẬN] |

</design_requirements>

---

<principles_mapping>

## §3. 7 LLM Principles — Mapping & Architecture Impact

### Principle #1: Domain Anchoring
**Cơ chế:** Neo LLM vào đúng không gian vector ngữ nghĩa trước khi suy luận.
**v0.0.2 status:** ❌ Thiếu thought blocks
**Effort:** LOW (new file + template)
**Yêu cầu architecture:**
- SKILL.md boot phase: inject thought blocks làm semantic anchors
- thought-cache.yaml: lưu thought blocks (>200 từ mỗi block)
- Glossary ≥ 10 terms trong hydrated-context.yaml
- Stakeholder empathy section trong thought-cache.yaml

### Principle #2: Semantic over Ceremony
**Cơ chế:** Nội dung đậm đặc ngữ nghĩa > Format cầu kỳ
**v0.0.2 status:** ⚠️ Template có nhưng thin content
**Effort:** MEDIUM (restructure existing)
**Yêu cầu architecture:**
- Data contracts xác định (input_schema / output_schema) trong mọi artifact
- Binary gates thay soft checklist
- hydrated-context.yaml: chỉ giữ glossary, NFR, edge cases, data contracts, zone map, must_not
- Loại bỏ prose không cần thiết

### Principle #3: Context Pre-processing
**Cơ chế:** Pre-process ngữ cảnh trước khi đưa cho LLM làm việc chính
**v0.0.2 status:** ❌ Không có hydration step
**Effort:** MEDIUM (add workflow phase)
**Yêu cầu architecture:**
- Thêm **Phase 2.5: Context Hydrator** vào workflow
- Hydrator tách khỏi Planner: hydrated-context.yaml (~30-50 dòng)
- L2_token_budget = 2200 tokens hard gate

### Principle #4: Dual Knowledge Stream
**Cơ chế:** Technical + Cognitive là 2 luồng riêng, lifecycle riêng
**v0.0.2 status:** ❌ Single stream
**Effort:** HIGH (new data model, templates, init, schema — multi-file)
**Yêu cầu architecture:**
- 2 artifact riêng biệt: hydrated-context.yaml (technical) + thought-cache.yaml (cognitive)
- hydrated-context: inline trong Context Bus
- thought-cache: file reference trong Context Bus
- Planner đọc thought-cache optional, Builder đọc mandatory

### Principle #5: Binary Mechanical Gates
**Cơ chế:** Gate phải nhị phân, deterministic, verify bằng script
**v0.0.2 status:** ❌ Checklist mềm
**Effort:** MEDIUM (replace checklist logic)
**Yêu cầu architecture:**
- META-2.1: PASS ⇔ S1 ∧ S2 ∧ S3 ∧ S4 (AND-deterministic)
- YAML Resilience: L1 syntax lint → L2 schema validation → L3 cross-ref
- Thêm **Phase 3.5: Depth Signal Verification** vào workflow
- Cơ chế auto-repair subagent (max 2 attempts mỗi level)

### Principle #6: Negative Space
**Cơ chế:** Dạy LLM điều KHÔNG nên làm
**v0.0.2 status:** ⚠️ Có must_not cơ bản
**Effort:** LOW (add section + gate)
**Yêu cầu architecture:**
- must_not lists trong mọi stage design
- Anti-patterns section riêng (không gộp vào must_not)
- S1 Negation Density trong META-2.1 signals
- Guardrails mở rộng (G1-G5 → G1-G7)

### Principle #7: Graceful Degradation
**Cơ chế:** Pipeline tiếp tục ở chế độ degraded thay vì Hard Halt
**v0.0.2 status:** ❌ Không có fallback
**Effort:** MEDIUM (new fallback logic)
**Yêu cầu architecture:**
- Fallback matrix subset F1-F4 (missing_skill, ambiguous, injection, validation_fail)
- Max 3 iterations per stage → escalate
- Append-only fallback history trong Context Bus
- Non-critical dangling ref → degraded mode (không block)

</principles_mapping>

---

<data_contracts_spec>

## §4. Data Contracts Specifications

### 4.1 hydrated-context.yaml schema

```yaml
# hydrated-context.yaml — Technical Contracts stream
# Size: 30-50 dòng (hard gate: REQ-11)
skill_name: "{target_skill}"          # kebab-case required
stage: "exploration"
glossary:                             # ≥10 terms (REQ-19)
  - term: "string"
    definition: "string"
nfr:                                  # Non-functional requirements
  - id: "string"
    requirement: "string"
    constraint: "hard|soft"
edge_cases:
  - scenario: "string"                # Edge case mô tả
    expected: "string"                # Expected behavior
data_contracts:
  input: "schema reference"
  output: "schema reference"
zone_map:
  core: ["SKILL.md"]
  knowledge: ["knowledge/*.md"]
  policy: ["policy/*.md"]
  loop: ["loop/*.md"]
  scripts: ["scripts/*.py"]
  templates: ["templates/*"]
  data: ["data/*.yaml"]
must_not:
  - "string"                          # Negative space rules
```

### 4.2 thought-cache.yaml schema

```yaml
# thought-cache.yaml — Cognitive Depth stream
# Size: 100-200 dòng (soft gate: REQ-12)
skill_name: "{target_skill}"
thought_blocks:                       # Mỗi block ≥200 words (REQ-20)
  - id: "tb-{n}"
    topic: "string"
    content: "string (≥200 words)"     # META-2.1 anti-gaming anchor
    signals:
      s1_negation: true               # Chứa must_not / "không"
      s2_reverse_question: true        # Chứa dấu "?"
      s3_multi_stakeholder: true       # Đề cập user/dev/agent/người
      s4_constraint_anchoring: true    # Chứa constraint/ràng buộc
stakeholder_empathy:
  - role: "string"                    # User / Developer / Agent
    pain: "string"
defensive_reasoning:
  - guardrail: "string"
    rationale: "string"
```

### 4.3 Fallback Matrix (F1-F4 subset)

```yaml
fallback_matrix_v1:
  max_iterations_per_stage: 3         # REQ-18
  history_mode: "append-only"
  cases:
    - id: F1
      name: "missing_skill_context"
      trigger: "skill_name không tìm thấy trong codebase"
      action: "hỏi user cung cấp thêm context"
      severity: "major"
    - id: F2
      name: "ambiguous_intent"
      trigger: "confidence < 70%"
      action: "dừng, trình bày analysis, hỏi user confirm"
      severity: "major"
    - id: F3
      name: "prompt_injection_detected"
      trigger: "YAML Resilience L1 fail sau 2 attempts"
      action: "Hard Halt — không graceful"
      severity: "critical"
    - id: F4
      name: "schema_validation_fail"
      trigger: "L2 schema validation fail sau 2 attempts"
      action: "Hard Halt — escalate lên stage 1"
      severity: "critical"
```

</data_contracts_spec>

---

<open_questions>

## §5. Open Questions cần Architect quyết định

> [!IMPORTANT]
> Đây là các câu hỏi từ scope document §10 + domain-handbook §2.F mà Architect PHẢI trả lời.
> Mỗi câu hỏi: (1) phân tích trade-off, (2) đưa ra recommendation, (3) gắn trace tag `[SUY LUẬN]`.

| # | Question | Context | Impact if Unresolved | Recommend |
|:--|:---------|:--------|:--------------------|:----------|
| **Q1** | exploration.schema.yaml có hỗ trợ multi-artifact không? | Schema compatibility | **BLOCKER** — không thể design output schema | Cần locate file + verify schema hiện tại |
| **Q2** | skill-architect đọc exploration.md format nào? Có cần update? | Downstream breaking | **BLOCKER** — architect fail nếu format đổi | Cần đọc skill-architect SKILL.md |
| **Q3** | Giữ exploration.md + 2 artifact mới, hay thay thế hoàn toàn? | Output strategy | **HIGH** — ảnh hưởng data flow | **Additive**: giữ report tổng + thêm 2 artifact. Giảm breaking change |
| **Q4** | thought-cache.yaml schema riêng hay chung? | Schema design | **MEDIUM** | **Standalone** (REQ-05): cognitive depth khác technical |
| **Q5** | SCS: single-pass (Stage 0) hay 2-phase (0.5+1.5)? | Pipeline redesign | **MEDIUM** | 2-phase nhưng Stage 1.5 optional v1.0 |
| **Q6** | Fallback: subset F1-F4 hay full F1-F19? | Scope sizing | **LOW-MEDIUM** | F1-F4 cho v1.0 (REQ-10), full deferred |
| **Q7** | Binary gates META-2.1 implement Stage 0 hay chỉ downstream? | Phasing | **MEDIUM** | **Implement ngay** — đây là quality gate cốt lõi |
| **Q8** | Sampling audit 30% có phù hợp exploration stage? | Rate tuning | **LOW** | Default 30%, cho phép 100% khi debug |

</open_questions>

---

<integration_points>

## §6. Integration Points (Files cần thiết kế)

### 6.1 Core files thay đổi

| File | Thay đổi cần thiết kế | Principle |
|:-----|:----------------------|:----------|
| `SKILL.md` | Boot sequence: + thought block injection, dual context routing, binary gates config | #1,#4,#5 |
| `knowledge/exploration-standards.md` | Expand 7 Golden Standards → integrate 7 LLM principles; SCS 2-phase | #1,#3,#5 |
| `knowledge/security-standards.md` | + YAML Resilience L1-L3, sampling audit | #5,#7 |
| `policy/output-spec.md` | Restructure: 3 artifacts thay 1 | #4 |
| `policy/workflow.md` | + Phase 2.5 (hydration), Phase 3.5 (depth verify) | #3,#5 |
| `templates/exploration.md.template` | + references to hydrated-context + thought-cache | #4 |
| `loop/exploration-checklist.md` | Binary gates + META-2.1 signals | #5,#6 |
| `scripts/init_context.py` | + init 2 artifacts (hydrated + thought cache) | #4 |

### 6.2 New files cần thiết kế

| File | Purpose | Schema |
|:-----|:--------|:-------|
| `schemas/hydrated-context.schema.yaml` | Schema cho technical contracts stream | Standalone |
| `schemas/thought-cache.schema.yaml` | Schema cho cognitive depth stream | Standalone (REQ-05) |
| `templates/hydrated-context.yaml.template` | Template mẫu | YAML |
| `templates/thought-cache.yaml.template` | Template mẫu | YAML |

### 6.3 Zone Map đề xuất

```yaml
zone_map:
  core:
    - "SKILL.md"
  knowledge:
    - "knowledge/exploration-standards.md"
    - "knowledge/security-standards.md"
  policy:
    - "policy/workflow.md"
    - "policy/guardrails.md"
    - "policy/output-spec.md"
  loop:
    - "loop/exploration-checklist.md"
  scripts:
    - "scripts/init_context.py"
  templates:
    - "templates/exploration.md.template"
    - "templates/hydrated-context.yaml.template"    # NEW
    - "templates/thought-cache.yaml.template"        # NEW
  data:
    - "data/search-blacklist.yaml"
  schemas:                                           # NEW zone
    - "schemas/hydrated-context.schema.yaml"
    - "schemas/thought-cache.schema.yaml"
```

</integration_points>

---

<quality_gates>

## §7. Quality Gates Architecture

### 7.1 Binary Gates Chain

```yaml
quality_gates:
  - gate: "META-2.1 Depth Signals"
    type: "hard"
    condition: "s1 AND s2 AND s3 AND s4"
    verify: "regex/script (mechanical)"
    fail_action: "WARNING (word<100) or FAIL (missing signal)"

  - gate: "L2_token_budget"
    type: "hard"
    condition: "≤ 2200 tokens"
    verify: "token count script"
    fail_action: "FAIL — request compression"

  - gate: "YAML_Resilience_L1"
    type: "interceptor"
    handler: "yaml.safe_load() → auto-repair (max 2)"
    fail_action: "Hard Halt"

  - gate: "YAML_Resilience_L2"
    type: "interceptor"
    handler: "schema validation required keys+types"
    fail_action: "Hard Halt after auto-repair fail"

  - gate: "YAML_Resilience_L3"
    type: "interceptor"
    handler: "cross-ref check path exists, non-empty"
    fail_action: "Critical→Hard Halt, Non-critical→Graceful Degradation"

  - gate: "Semantic_Sampling_Audit"
    type: "probabilistic"
    rate: "30% default → 100% on FAIL → 15% after 8 PASS"
    fail_action: "F8-EXT: audit-fail-report → re-route"
```

### 7.2 META-2.1 Verification (mechanical, regex-based)

```
S1 = "must_not" IN thought_block OR "không" IN thought_block
S2 = "?" IN thought_block
S3 = ANY("user", "dev", "agent", "người") IN thought_block
S4 = "constraint" IN thought_block OR "ràng buộc" IN thought_block
PASS = S1 AND S2 AND S3 AND S4
```

### 7.3 Sampling Audit Rate

```yaml
sampling_audit:
  default_rate: "30%"
  fail_escalation: "100%"
  relaxation_after: "8 consecutive PASS → 15%"
  scope: "thought_block content (semantic depth)"
```

</quality_gates>

---

<anti_patterns>

## §8. Anti-Patterns (Negative Space cho Architect)

| Anti-pattern | Description | Consequence |
|:-------------|:------------|:------------|
| **Single-stream output** | Gộp technical + cognitive vào 1 exploration.md | Planner phải mang depth dù không cần; phình to file |
| **Soft-only checklist** | Dùng câu hỏi mềm thay binary gate | LLM "tăng điểm" bằng padding; không verify được bằng script |
| **Thought block <200 từ** | Viết ngắn gọn thay vì deep analysis | Mất cognitive depth; LLM code đúng contract sai intent |
| **Hallucinate khi thiếu docs** | Đoán mò API/cấu trúc khi chưa có source | Builder implement sai; vi phạm KM must_not |
| **Edit workspace code** | Architect sửa source ngoài `.skill-context/` | Vi phạm G1_DesignOnly guardrail |
| **Skip HITL khi confidence <70%** | Tự quyết thay hỏi user | Sai intent từ đầu; tốn chi phí rebuild |

</anti_patterns>

---

<edge_cases>

## §9. Edge Cases cần Architecture Coverage

| # | Edge Case | Expected Architecture Treatment |
|:--|:----------|:-------------------------------|
| E1 | skill_name không phải kebab-case | validate_skill_name() reject; init_context báo lỗi |
| E2 | `.skill-context/{skill}/` đã tồn tại | Resume, KHÔNG overwrite (safe_create_file SKIPPED) |
| E3 | `init_context.py --split` trên exploration.md chưa `decomposed: true` | In info, return 0, không split |
| E4 | YAML frontmatter lỗi syntax | YAML Resilience L1 auto-repair (max 2 attempts) → fail → Hard Halt |
| E5 | Thought block thiếu 1/4 META-2.1 signal | Binary gate FAIL → WARNING (word<100) hoặc FAIL (thiếu signal) |
| E6 | Confidence khảo sát <70% | Dừng, hỏi user (G5_HumanInTheLoop) |
| E7 | Web fetch thất bại (network egress blocked) | Graceful degradation: dùng resources nội bộ, mark [CẦN LÀM RÕ] |
| E8 | thought-cache.yaml >200 dòng | Soft gate warning token budget, không block |
| E9 | Schema exploration.schema.yaml chưa update cho dual stream | Validator fail → escalate lên stage 1 trước khi build |

</edge_cases>

---

<output_contract>

## §10. Output Contract — Architecture Design

Design.md phải có các section sau:

```yaml
design_output:
  artifact: "design.md"
  format: "Markdown + YAML + Mermaid"
  required_sections:
    - "§1: Overview & Design Decisions"
      trace: "Mọi decision có trace tag [TỪ SCOPE], [TỪ HANDBOOK], [TỪ BA REQ-N], [SUY LUẬN]"
    - "§2: Architecture Diagram (Mermaid)"
      trace: "component diagram, sequence diagram, data flow"
    - "§3: Zone Mapping (YAML)"
      trace: "REQ-01→04"
    - "§4: Data Contracts (YAML)"
      trace: "REQ-05, REQ-06, REQ-11, REQ-12, REQ-16, REQ-19, REQ-20"
    - "§5: Workflow Design (Mermaid + YAML)"
      trace: "REQ-03, REQ-07→10"
    - "§6: Quality Gates Architecture (YAML)"
      trace: "REQ-07, REQ-08, REQ-14, REQ-15, REQ-17, REQ-18"
    - "§7: Negative Space Design (YAML)"
      trace: "REQ-09"
    - "§8: Graceful Degradation Design (YAML)"
      trace: "REQ-10"
    - "§9: Open Questions Resolution"
      trace: "Q1→Q8 — mỗi Q có decision + rationale"
    - "§10: Risk Assessment (table)"
      trace: "E1→E9 coverage"
  handoff_to: [skill-planner, skill-builder]
```

</output_contract>

---

> **Prompt status:** Complete
> **Design target:** skill-explorer v1.0 — từ single-stream lên dual-stream + 7 LLM principles
> **Synthesis method:** Direct reading of scope + domain-handbook + business-analysis + synthesis-llm-principles + standards + 12 resource files
> **Supporting knowledge applied:** synthesis-llm-principles.md (7 principles mapping), standards.md (format rules, token budget, 4-layer model)
> **REQ Coverage:** 20/20 requirements (10 FR + 10 NFR)
> **Edge Cases Coverage:** 9/9 (E1-E9)
> **Anti-Patterns:** 6 listed
</parameter>
