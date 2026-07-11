---
skill_name: "skill-explorer-main-build"
criteria_analysis:
  - criterion_id: "FR-01"
    description: "Map v0.0.2 skill-explorer architecture sang 7 LLM principles (Domain Anchoring, Semantic, Pre-processing, Dual Stream, Binary Gates, Negative Space, Graceful Degradation)."
    classification: "FR"
  - criterion_id: "FR-02"
    description: "Thực hiện Gap Analysis 7 principles dạng MECE (7 gap độc lập, không chồng lấp) với priority HIGH/MEDIUM."
    classification: "FR"
  - criterion_id: "FR-03"
    description: "Sinh dual-stream output thay vì single exploration.md: hydrated-context.yaml (~30-50 dòng) + thought-cache.yaml (~100-200 dòng)."
    classification: "FR"
  - criterion_id: "FR-04"
    description: "Chỉ document findings; KHÔNG sửa SKILL.md/policy/templates, KHÔNG chạy init_context.py, KHÔNG tạo branch."
    classification: "FR"
  - criterion_id: "FR-05"
    description: "Định nghĩa standalone thought-cache.schema.yaml (không extend exploration.schema.yaml do vi phạm additionalProperties:false)."
    classification: "FR"
  - criterion_id: "FR-06"
    description: "Thêm 2 entry vào artifact_registry.yaml (hydrated_context, thought_cache) với lifecycle WORM để schema_validator.py quét được."
    classification: "FR"
  - criterion_id: "FR-07"
    description: "Triển khai Binary Mechanical Gates META-2.1: PASS iff S1 AND S2 AND S3 AND S4 present; deterministic, verify bằng script."
    classification: "FR"
  - criterion_id: "FR-08"
    description: "Triển khai YAML Resilience Layer L1 (syntax) + L2 (schema) + L3 (cross-ref) làm interceptor trước mọi YAML commit."
    classification: "FR"
  - criterion_id: "FR-09"
    description: "Triển khai Negative Space: must_not lists + anti-patterns section + S1 Negation Density trong output."
    classification: "FR"
  - criterion_id: "FR-10"
    description: "Triển khai Graceful Degradation fallback matrix subset critical (F1 missing_skill, F2 ambiguous, F3 injection, F4 validation_fail), max 3 iter/stage."
    classification: "FR"
  - criterion_id: "NFR-01"
    description: "hydrated-context.yaml giới hạn tối đa 50 dòng để không vi phạm L2_token_budget 2200 tokens."
    classification: "NFR"
  - criterion_id: "NFR-02"
    description: "thought-cache.yaml duy trì 100-200 dòng (cognitive depth, mỗi thought block >200 từ)."
    classification: "NFR"
  - criterion_id: "NFR-03"
    description: "L2_token_budget cứng 2200 tokens cho context hydration; enforcement hard gate."
    classification: "NFR"
  - criterion_id: "NFR-04"
    description: "YAML Resilience gồm 3 levels (L1 syntax, L2 schema, L3 cross-ref)."
    classification: "NFR"
  - criterion_id: "NFR-05"
    description: "Binary gate META-2.1 gồm 4 depth signals (S1-S4) AND-deterministic."
    classification: "NFR"
  - criterion_id: "NFR-06"
    description: "exploration.schema.yaml giữ additionalProperties:false (constraint = 0 nghĩa là forbidden)."
    classification: "NFR"
  - criterion_id: "NFR-07"
    description: "Semantic Sampling Audit default rate 30%, nhảy 100% khi có FAIL."
    classification: "NFR"
  - criterion_id: "NFR-08"
    description: "Graceful Degradation giới hạn tối đa 3 iterations per stage trước escalate."
    classification: "NFR"
  - criterion_id: "NFR-09"
    description: "Domain glossary tối thiểu 10 thuật ngữ chuyên ngành làm semantic anchor."
    classification: "NFR"
  - criterion_id: "NFR-10"
    description: "Mỗi thought block trong thought-cache yêu cầu tối thiểu 200 từ."
    classification: "NFR"
metrics:
  - name: "hydrated_context_max_lines"
    value: 50
    unit: "lines"
  - name: "thought_cache_min_lines"
    value: 100
    unit: "lines"
  - name: "thought_cache_max_lines"
    value: 200
    unit: "lines"
  - name: "L2_token_budget"
    value: 2200
    unit: "tokens"
  - name: "yaml_resilience_levels"
    value: 3
    unit: "levels"
  - name: "binary_gate_signals"
    value: 4
    unit: "signals"
  - name: "additional_properties_allowed"
    value: 0
    unit: "boolean"
  - name: "sampling_audit_default_rate"
    value: 30
    unit: "percent"
  - name: "fallback_max_iterations"
    value: 3
    unit: "iterations"
  - name: "glossary_min_terms"
    value: 10
    unit: "terms"
  - name: "thought_block_min_words"
    value: 200
    unit: "words"
risk_assessment:
  - risk_id: "RR-01"
    edge_case: "exploration.schema.yaml giữ additionalProperties:false nhưng dev cố nhét field mới vào frontmatter → schema_validator.py exit 1 → WORM integrity violation tại Stage 4."
    mitigation: "Tạo standalone thought-cache.schema.yaml; tuyệt đối KHÔNG extend exploration.schema.yaml (vi phạm constraint NFR-06)."
  - risk_id: "RR-02"
    edge_case: "skill-architect hiện chỉ đọc exploration.md (SKILL.md dòng 36); dual-stream là breaking change chưa migrate → architect nhận context mỏng, design drift."
    mitigation: "Thêm 2 registry entries (FR-06) + migrate architect boot sequence đọc cả hydrated-context.yaml và thought-cache.yaml; cập nhật input contract."
  - risk_id: "RR-03"
    edge_case: "thought-cache.yaml chứa raw external prompts chưa sanitize → prompt injection qua web resource mà không có YAML Resilience L3 cross-ref check."
    mitigation: "Áp dụng YAML Resilience L3 cross-ref (path tồn tại, file non-empty) + sanitize raw prompts trước commit vào Context Bus."
  - risk_id: "RR-04"
    edge_case: "hydrated-context.yaml vượt 50 dòng → vi phạm L2_token_budget 2200 tokens → Planner mang depth không cần, token waste."
    mitigation: "Smart Splitter ép max 50 dòng (NFR-01); hard gate block khi vượt; tách prose thừa sang thought-cache."
  - risk_id: "RR-05"
    edge_case: "Fallback matrix F1-F19 quá rộng implement trong v1.0 → scope creep vượt MVP, trễ tiến độ."
    mitigation: "Chỉ implement subset critical F1-F4 cho v1.0 (FR-10); defer F5-F19 sang phase sau, đánh dấu wont_have P3."
  - risk_id: "RR-06"
    edge_case: "SCS score chuyển 2-phase (Stage 0.5 + 1.5) nhưng explorer giữ single-pass → routing sai, orchestration-plan thiếu."
    mitigation: "Quyết định phasing rõ: giữ single-pass Stage 0 cho v1.0; ghi [CẦN LÀM RÕ] để Steve confirm trước chuyển 2-phase."
---

> [!NOTE]
> **Artifact Metadata (KHÔNG thuộc frontmatter — schema dùng `additionalProperties: false`).**
> ```yaml
> analyzed_by: "ba-analyst"
> analyzed_at: "2026-07-11T15:00:00Z"
> status: "completed"
> schema_ref: "skills/ver-3/_shared/schemas/analysis.schema.yaml"
> artifact_lifecycle: "WORM"
> validated_by: "schema_validator.py + validate_metrics.py"
> trace_tags: ["TỪ INPUT", "SUY LUẬN", "CẦN LÀM RÕ"]
> ```

# Báo Cáo Phân Tích Nghiệp Vụ & Đặc Tả Kỹ Thuật

## §1: Classification & MoSCoW Matrix

| ID | Yêu cầu | Loại | MoSCoW | Giải thích kỹ thuật |
|:---|:--------|:----:|:------:|:-------------------|
| FR-01 | Map v0.0.2 ↔ 7 LLM principles | FR | P0 — Must | Nền tảng analysis, thiếu thì không biết tích hợp gì. |
| FR-02 | Gap Analysis 7 principles (MECE) | FR | P0 — Must | Xác định 7 gap độc lập, định hướng build. |
| FR-03 | Dual-stream output (hydrated + thought cache) | FR | P0 — Must | Thay single exploration.md, cốt lõi v1.0. |
| FR-04 | Document only, no code/branch | FR | P0 — Must | Scope ràng buộc từ input; vi phạm = out of scope. |
| FR-05 | Standalone thought-cache.schema.yaml | FR | P1 — Should | Giải quyết RR-01; có thể defer nếu extend bị cấm. |
| FR-06 | 2 registry entries WORM | FR | P1 — Should | Cần để validator quét được dual-stream. |
| FR-07 | Binary Gates META-2.1 (S1-S4 AND) | FR | P1 — Should | Deterministic verify, giảm drift. |
| FR-08 | YAML Resilience L1-L3 | FR | P1 — Should | Interceptor bảo vệ trước mọi YAML commit. |
| FR-09 | Negative Space (must_not + anti-patterns) | FR | P2 — Could | Tăng chất lượng, không block MVP. |
| FR-10 | Fallback matrix subset F1-F4 | FR | P2 — Could | Graceful degradation, defer F5-F19. |
| NFR-01 | hydrated-context ≤ 50 dòng | NFR | P0 — Must | Bảo vệ token budget, hard gate. |
| NFR-02 | thought-cache 100-200 dòng | NFR | P0 — Must | Cognitive depth yêu cầu. |
| NFR-03 | L2_token_budget = 2200 tokens | NFR | P0 — Must | Ràng buộc cứng hydration. |
| NFR-04 | YAML Resilience 3 levels | NFR | P1 — Should | L1/L2/L3 defenses. |
| NFR-05 | Binary gate 4 signals AND | NFR | P1 — Should | META-2.1 depth gate. |
| NFR-06 | additionalProperties:false | NFR | P0 — Must | Ngăn nhét field bừa, bảo vệ schema. |
| NFR-07 | Sampling audit 30% | NFR | P2 — Could | Deterrence effect. |
| NFR-08 | Max 3 iter/stage | NFR | P1 — Should | Fallback discipline. |
| NFR-09 | Glossary ≥ 10 terms | NFR | P0 — Must | Semantic anchor bắt buộc. |
| NFR-10 | Thought block ≥ 200 words | NFR | P0 — Must | Cognitive depth tối thiểu. |

## §2: System Diagrams (Sequence + Flowchart + ERD)

### Sequence Diagram

```mermaid
sequenceDiagram
    autonumber
    actor User as "Steve (Owner)"
    participant Elicitor as "BA Elicitor"
    participant Explorer as "skill-explorer"
    participant Validator as "schema_validator.py"
    participant Architect as "skill-architect"
    User->>Elicitor: "Phê duyệt scope + 7 LLM principles"
    Elicitor->>Explorer: "Đọc v0.0.2 + sinh dual-stream proposal"
    Explorer->>Explorer: "Map gap + viết hydrated-context.yaml"
    Explorer->>Explorer: "Viết thought-cache.yaml (cognitive depth)"
    Explorer->>Validator: "Quét 2 artifact qua registry entries"
    Validator-->>Explorer: "PASS (L1-L3 resilient)"
    Explorer->>Architect: "Handoff hydrated + thought cache"
    Architect-->>User: "Design ít drift, context chuẩn"
```

### Flowchart

```mermaid
flowchart TD
    Start["Bắt đầu Stage 0"] --> MapGap{"Map gap 7 principles?"}
    MapGap -- "Đủ (Happy)" --> GenDual["Sinh hydrated + thought cache"]
    GenDual --> Validate{"schema_validator PASS?"}
    Validate -- "PASS (Happy)" --> Handoff["Handoff sang architect"]
    Validate -- "FAIL (Alt)" --> FixSchema["Sửa standalone schema, không extend"]
    FixSchema --> GenDual
    MapGap -- "Thiếu (Exception)" --> Block["Block pipeline, escalate Steve"]
    Block --> Start
```

### ERD

```mermaid
erDiagram
    EXPLORATION_REPORT ||--o{ HYDRATED_CONTEXT : "has"
    EXPLORATION_REPORT ||--o{ THOUGHT_CACHE : "has"
    ARTIFACT_REGISTRY ||--o{ HYDRATED_CONTEXT : "registers"
    ARTIFACT_REGISTRY ||--o{ THOUGHT_CACHE : "registers"
    EXPLORATION_REPORT {
        integer id PK
        string skill_name
        string status
        timestamp created_at
    }
    HYDRATED_CONTEXT {
        integer id PK
        integer report_id FK
        integer line_count
        integer token_count
        string lifecycle
    }
    THOUGHT_CACHE {
        integer id PK
        integer report_id FK
        integer line_count
        integer block_count
        string lifecycle
    }
    ARTIFACT_REGISTRY {
        integer entry_id PK
        string artifact_type
        string schema_ref
        string lifecycle
    }
```

## §3: Data Schema Design (tables + JSON Schema)

| Tên trường | Kiểu | Ràng buộc | Mô tả |
|:---|:---|:---|:---|
| `id` | `integer` | `PK, AUTO_INCREMENT` | Khóa chính |
| `report_id` | `integer` | `FK → EXPLORATION_REPORT.id` | Liên kết báo cáo gốc |
| `line_count` | `integer` | `NOT NULL, ≤ 50 (hydrated) / 100-200 (thought)` | Số dòng artifact |
| `token_count` | `integer` | `NOT NULL, ≤ 2200` | Token budget L2 |
| `lifecycle` | `string` | `NOT NULL, enum[WORM]` | Vòng đời bất biến |
| `created_at` | `timestamp` | `NOT NULL` | Thời gian sinh |

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "HydratedContextSchema",
  "type": "object",
  "properties": {
    "skill_name": { "type": "string", "minLength": 1 },
    "glossary": {
      "type": "array",
      "items": { "type": "string" },
      "minItems": 10
    },
    "nfrs": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "id": { "type": "string" },
          "metric": { "type": "string" },
          "value": { "type": "number" },
          "unit": { "type": "string" }
        },
        "required": ["id", "metric", "value", "unit"]
      }
    },
    "data_contracts": { "type": "object" },
    "must_not": { "type": "array", "items": { "type": "string" } },
    "line_count": { "type": "integer", "maximum": 50 },
    "token_count": { "type": "integer", "maximum": 2200 }
  },
  "required": ["skill_name", "glossary", "nfrs", "line_count"]
}
```

## §4: Gherkin Acceptance Criteria (3-path)

**User Story:** As a BA Elicitor, I want to generate dual-stream hydrated-context.yaml + thought-cache.yaml so that skill-architect receives standardized technical and cognitive context with minimal design drift.

```gherkin
Feature: skill-explorer dual-stream output v1.0
  Scenario: Happy Path — Sinh dual-stream PASS
    Given elicitor đọc scope doc + 7 LLM principles + v0.0.2 code
    When elicitor map 7 gap và sinh hydrated-context.yaml (≤ 50 dòng) + thought-cache.yaml (100-200 dòng)
    Then schema_validator.py quét 2 registry entries và trả về PASS (L1-L3 resilient)
    And skill-architect đọc được cả 2 artifact không drift

  Scenario: Alternative Path — Giữ exploration.md + 2 artifact
    Given option A được chọn (giữ exploration.md tóm tắt + thêm 2 artifact)
    When validator chạy trên 3 entry (exploration, hydrated, thought_cache)
    Then architect có thể đọc 1 hoặc 3 file tùy config mà không break

  Scenario: Exception Path — Schema vi phạm additionalProperties:false
    Given exploration.schema.yaml giữ additionalProperties:false
    When dev cố nhét field mới vào frontmatter exploration.md
    Then schema_validator.py FAIL (exit 1) và WORM break
    And pipeline quay lại thiết kế schema standalone, KHÔNG tự sửa
```

## §5: Risk Assessment Matrix (P×I + mitigation)

| Mã RR | Mô tả rủi ro | Xác suất | Tác động | Giải pháp giảm thiểu |
|:---|:---|:---:|:---:|:---|
| RR-01 | Extend schema vi phạm additionalProperties:false | Cao | Cao | Standalone thought-cache.schema.yaml (FR-05) |
| RR-02 | Architect breaking change chưa migrate | Cao | Cao | 2 registry entries + migrate boot sequence (FR-06) |
| RR-03 | Prompt injection qua raw prompts | Trung bình | Cao | YAML Resilience L3 + sanitize (FR-08) |
| RR-04 | hydrated-context vượt 50 dòng | Trung bình | Trung bình | Smart Splitter + hard gate (NFR-01) |
| RR-05 | Scope creep fallback F1-F19 | Trung bình | Trung bình | Chỉ F1-F4, defer còn lại (FR-10) |
| RR-06 | SCS phasing sai (single vs 2-phase) | Thấp | Trung bình | Giữ single-pass v1.0, [CẦN LÀM RÕ] confirm |

## §6: Traceability Mapping (requirement → diagram → test → risk)

- **FR-01, FR-02, FR-03, FR-04**: [TỪ INPUT] ánh xạ trực tiếp từ `elicitation-report.md` §1 (mục tiêu, env, actors, FRs, size NFRs).
- **FR-05 → RR-01, FR-06 → RR-02**: [SUY LUẬN] từ gap analysis §3 (First Principles: additionalProperties:false → tách file bắt buộc).
- **NFR-01..NFR-10**: [TỪ INPUT] + [SUY LUẬN] từ scope §6.2 và synthesis-llm-principles (token budget, resilience levels, signals).
- **Sequence/Flowchart/ERD**: [SUY LUẬN] từ data flow impact scope §4.3 (v0.0.2 → v1.0 dual-stream).
- **Điểm chưa rõ**: [CẦN LÀM RÕ] output strategy (Q1), SCS phasing (Q2), fallback subset (Q3), binary gate stage (Q4), thought-cache schema (Q5), registry entries (Q6) — ESCALATE Steve trước build phase.
