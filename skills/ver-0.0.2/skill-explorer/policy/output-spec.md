# Đặc Tả Hợp Đồng Đầu Ra (Output Specification)

> **Mã số**: STG0-POL-02
> **Mục tiêu**: Định hình cấu trúc 8 phần bắt buộc của tài liệu đầu ra `exploration.md`.

---

## Output Contract

```yaml
output_contract:
  artifact: ".skill-context/{target_skill}/exploration.md"
  format: markdown_with_yaml_frontmatter
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

---

## Đặc tả chi tiết 9 Chương mục

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
