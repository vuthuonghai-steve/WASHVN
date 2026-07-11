---
skill_schema_version: "3.0.0"
artifact_type: "exploration"
skill_name: "{skill_name}"
generated_by: "skill-explorer"
generated_at: "{generated_at}"
stage: "exploration"
status: "in_progress"
required_sections:
  - "1_pain_point_and_core_objective"
  - "2_existing_resources_audit"
  - "3_seven_golden_standards_assessment"
  - "3.3_skill_scale_and_decomposition_assessment"
  - "4_ai_instruction_standards_and_rules"
  - "5_process_flow_and_automation_mapping"
  - "6_architectural_recommendations"
  - "7_risks_and_open_questions"
  - "8_metadata"
handoff:
  next_stage: "architect"
  ready_condition:
    required:
      frontmatter_valid: true
      resources_audited: true
      seven_standards_assessed: true
      no_blockers: true
---

# {skill_name} — Báo Cáo Khảo Sát Nghiệp Vụ & Khai Thác Tài Nguyên

> **Ngày khảo sát**: {date}
> **Trạng thái**: Đang khảo sát (`in_progress`)

---

## 1. Pain Point & Core Objective

### A. Vấn đề thực tế (Pain Points)

### B. Mục tiêu tự động hóa (Core Objective)

---

## 2. Existing Resources Audit

Bảng khảo sát hiện trạng tài nguyên nghiệp vụ trong dự án:

| Đường dẫn tài nguyên | Nội dung tóm tắt | Phân loại chất lượng (Thin/Rich) | Ghi chú bổ sung |
|----------------------|------------------|----------------------------------|-----------------|
|                      |                  |                                  |                 |

---

## 3. Seven Golden Standards Assessment

Phân tích và thiết lập định hướng thiết kế cho skill dựa trên 7 tiêu chuẩn vàng:

1. **Khả năng tái sử dụng (Reusability)**:
2. **Khả năng kết hợp (Composability)**:
3. **Khả năng bảo trì (Maintainability)**:
4. **Độ an toàn và bảo mật (Security)**:
   - *Biện pháp chống Prompt Injection*:
   - *Thiết lập Docker Sandboxing*:
5. **Hiệu suất ngữ cảnh (Context Efficiency)**:
6. **Tính di động (Portability)**:
7. **Độ tin cậy & Luồng dự phòng (Reliability & Fallback)**:

---

## 3.3. Skill Scale & Decomposition Assessment

### A. Bảng tính điểm phức tạp kỹ năng (Complexity Score Table)

| Tiêu chí | Điểm SCS (1 - 5) | Dẫn chứng nghiệp vụ thực tế |
|----------|------------------|-----------------------------|
| **Số bước quy trình** | | |
| **Số công cụ / API tương tác** | | |
| **Kích thước SKILL.md dự kiến** | | |
| **Độ nhạy cảm an ninh (Security Risk)** | | |

- **Điểm SCS Trung bình**: 
- **Kết luận (Monolithic vs Micro-Skills)**: 

### B. Phương án phân rã thành các Micro-Skills đề xuất

### C. Sơ đồ phối hợp luồng tuần tự (Mermaid Flow)
```mermaid
graph TD
  
```

---

## 4. AI Instruction Standards & Rules

Các chỉ dẫn nghiệp vụ cứng và ràng buộc kỹ thuật bắt buộc AI phải tuân thủ để tránh đoán mò:

```yaml
rules_for_ai:
  must:
    - 
  must_not:
    - 
```

---

## 5. Process Flow & Automation Mapping

### A. Luồng nghiệp vụ hiện tại (As-Is - Thủ công)

### B. Luồng tự động hóa đích (To-Be - Lí tưởng)

---

## 6. Architectural Recommendations

Đề xuất quy hoạch 7 Zones cho kỹ năng đích:

- **Core**: 
- **Knowledge**: 
- **Scripts**: 
- **Templates**: 
- **Data**: 
- **Loop**: 

---

## 7. Risks & Open Questions

### A. Bảng rủi ro & giải pháp giảm thiểu
| # | Rủi ro tiềm ẩn | Mức độ ảnh hưởng | Giải pháp giảm thiểu (Mitigation) |
|---|----------------|-------------------|-----------------------------------|
| 1 |                |                   |                                   |

### B. Các câu hỏi mở cần làm rõ (Open Questions)
- 

---

## 8. Metadata

- **Skill Name**: {skill_name}
- **Stage**: exploration
- **Artifact Type**: exploration
- **Author**: Skill Explorer
