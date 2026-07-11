# Đặc Tả Hợp Đồng Đầu Ra (Output Specification)

> **Mã số**: STG0-POL-02
> **Mục tiêu**: Định nghĩa 3 artifact đầu ra của Explorer Agent, mỗi artifact có schema, consumer, và size budget riêng.

---

## Data Flow v1.0

```text
Explorer ──┬──→ exploration.md ──→ skill-architect (report)
           ├──→ hydrated-context.yaml ──→ planner (mandatory), builder (mandatory)
           └──→ thought-cache.yaml ──→ builder (mandatory), planner (optional)
```

---

## Artifact 1: exploration.md

```yaml
artifact: ".skill-context/{target_skill}/exploration.md"
format: markdown_with_yaml_frontmatter
size_budget: "Không giới hạn cứng, ưu tiên đầy đủ chi tiết"
consumer: "skill-architect"
required_sections:
  - "§1_pain_point_and_core_objective"
  - "§2_existing_resources_audit"
  - "§3_seven_golden_standards_assessment"
  - "§3.3_skill_scale_and_decomposition_assessment"
  - "§4_ai_instruction_standards_and_rules"
  - "§5_process_flow_and_automation_mapping"
  - "§6_architectural_recommendations"
  - "§7_risks_and_open_questions"
  - "§8_metadata"
handoff_to: "skill-architect"
```

### Đặc tả chi tiết 9 Chương mục

### §1. Pain Point & Core Objective
- Mô tả chi tiết vấn đề nghiệp vụ cần giải quyết, nỗi đau của người dùng, và mục tiêu tự động hóa tối cao của kỹ năng mới.

### §2. Existing Resources Audit
- Bảng kiểm kê chất lượng của toàn bộ tài nguyên đã thu thập được trong dự án (bao gồm đường dẫn file, nội dung tóm tắt, phân loại mức độ sẵn sàng: `Thin` vs `Rich`).

### §3. Seven Golden Standards Assessment
- Đánh giá chi tiết kỹ năng cần tạo dựa trên **7 Tiêu chuẩn Vàng** (Reusability, Composability, Maintainability, Security, Context Economics, Portability, Reliability). Thiết lập rõ giải pháp an toàn bảo mật, chống Prompt Injection và cách thức cấu hình sandbox Docker.

### §3.3. Skill Scale & Decomposition Assessment
- Bài toán tính điểm phức tạp định lượng của kỹ năng (Complexity Score Table).
- Kết luận phủ quyết giải pháp Monolithic nếu SCS > 3.0 hoặc chạm ngưỡng đỏ (5 điểm).
- Đề xuất mô hình phân rã thành các Micro-skills và vẽ sơ đồ phối hợp luồng (Mermaid flow).

### §4. AI Instruction Standards & Rules
- Phần cực kỳ quan trọng: Thiết lập các luật chỉ dẫn cứng nghiệp vụ và ràng buộc kỹ thuật chi tiết để hướng dẫn AI thực thi kỹ năng một cách bền vững, tránh đoán mò.

### §5. Process Flow & Automation Mapping
- So sánh chi tiết luồng thao tác thủ công (As-Is) và luồng tự động hóa lý tưởng (To-Be). Định hình rõ tham số đầu vào, kết quả đầu ra và kịch bản bắt lỗi nghiệp vụ.

### §6. Architectural Recommendations
- Đề xuất sơ bộ về việc quy hoạch 7 Zones cho kỹ năng đích (file nào nên đưa vào zone `core`, zone `knowledge`, zone `scripts`, zone `loop`) để định hướng trực tiếp cho `skill-architect`.

### §7. Risks & Open Questions
- Liệt kê các rủi ro hệ thống kèm giải pháp giảm thiểu, và các câu hỏi nghiệp vụ còn mơ hồ cần làm rõ với người dùng.

### §8. Metadata
- Khối YAML frontmatter cấu hình: `skill_name`, `generated_by`, `generated_at`, `status`, `stage`, `handoff`.

---

## Artifact 2: hydrated-context.yaml

```yaml
artifact: ".skill-context/{target_skill}/hydrated-context.yaml"
format: yaml
size_budget: "≤ 50 lines, ≤ 2200 tokens"
schema_path: "schemas/hydrated-context.schema.yaml"
consumer:
  - "planner (mandatory)"
  - "builder (mandatory)"
purpose: "Technical context — parameters, dependencies, security profile, output contracts"
content_structure:
  - "meta: skill_name, stage, generated_at"
  - "technical_params: key-value pairs for build-time configuration"
  - "dependencies: list of internal/external dependencies with versions"
  - "security_profile: sandbox type, network policy, mount rules"
  - "output_contract: expected artifact list with schema refs"
```

---

## Artifact 3: thought-cache.yaml

```yaml
artifact: ".skill-context/{target_skill}/thought-cache.yaml"
format: yaml
size_budget: "100-200 lines; each thought block ≥ 200 words"
schema_path: "schemas/thought-cache.schema.yaml"
consumer:
  - "builder (mandatory)"
  - "planner (optional)"
purpose: "Cognitive context — design rationale, tradeoff analysis, negative space mapping"
content_structure:
  - "meta: skill_name, stage, generated_at"
  - "thought_blocks: list of cognitive artifacts, each ≥ 200 words"
  - "  - id: T001"
  - "    title: short descriptor"
  - "    content: full reasoning (≥ 200 words)"
  - "    tags: [domain_anchoring, negative_space, etc.]"
  - "tradeoff_log: key decisions with alternatives considered and rejection rationale"
  - "open_questions: unresolved items deferred to builder"
```
