# Quy tắc Kiểm định Chéo (Cross-Reference Validation Rules)

Tài liệu này chi tiết các quy tắc kiểm định tính nhất quán chéo giữa các Deliverables trong báo cáo phân tích nghiệp vụ.

<context>
Mục tiêu là phát hiện sớm sự không tương thích giữa thiết kế luồng tương tác (Sequence Diagram), cấu trúc dữ liệu (ERD), mức độ ưu tiên tính năng (MoSCoW) và kịch bản kiểm thử (Acceptance Criteria Gherkin).
</context>

<output_contract>
```yaml
rules:
  actor_entity_matching:
    description: "Quét Sequence Diagram Mermaid để đối chiếu với ERD Mermaid. Đảm bảo mọi thực thể được thao tác trong SD đều tồn tại trong ERD."
    steps:
      - "1. Quét mã nguồn Sequence Diagram Mermaid để trích xuất danh sách các Actor và Participant."
      - "2. Quét mã nguồn ERD Mermaid để trích xuất danh sách các thực thể (Entities)."
      - "3. So khớp các thực thể được thao tác trong Sequence Diagram với danh sách thực thể của ERD."
    fail_trigger: "Nếu SD thao tác với thực thể không tồn tại trong ERD"
    warning_tag: "[MAU THUẪN NGHIỆP VỤ: Thực thể CSDL thiếu hụt]"
    mitigation: "Bổ sung thực thể bị thiếu vào ERD hoặc điều chỉnh SD cho đúng cấu trúc thực tế."

  moscow_gherkin_matching:
    description: "Quét bảng phân loại MoSCoW để đối chiếu với danh sách kịch bản Acceptance Criteria. Đảm bảo mọi tính năng Must-Have đều có kịch bản kiểm thử."
    steps:
      - "1. Quét bảng MoSCoW và lọc ra toàn bộ các tính năng có mức độ ưu tiên 'Must' (Must-Have)."
      - "2. Quét tài liệu Acceptance Criteria để trích xuất tên các Feature/Scenario."
      - "3. So khớp tên các tính năng Must-Have với các Scenario Gherkin tương ứng."
    fail_trigger: "Nếu một tính năng Must-Have thiếu kịch bản kiểm thử Gherkin tương ứng"
    warning_tag: "[THIẾU KỊCH BẢN KIỂM THỬ: Tính năng cốt lõi chưa có kiểm thử]"
    mitigation: "Bổ sung các kịch bản kiểm thử (Given-When-Then) cho tính năng Must-Have bị thiếu."

warning_tags:
  - tag: "[MAU THUẪN NGHIỆP VỤ]"
    trigger: "Entity hoặc Actor trong Sequence Diagram không khớp với ERD"
    description: "Không nhất quán giữa thiết kế luồng hệ thống và thiết kế cơ sở dữ liệu."
  - tag: "[THIẾU KỊCH BẢN KIỂM THỬ]"
    trigger: "Tính năng Must-Have không có Scenario Gherkin"
    description: "Thiếu kịch bản kiểm định cho các chức năng quan trọng nhất."
  - tag: "[THIẾU THÔNG TIN]"
    trigger: "Thiếu dữ liệu chéo hoặc thiếu một trong 7 deliverables bắt buộc"
    description: "Không thể thực hiện kiểm định chéo do thiếu tài liệu đầu vào."

output_effect:
  consistent:
    status: "PASS"
    description: "Không phát hiện mâu thuẫn chéo hoặc thiếu hụt kịch bản kiểm thử quan trọng."
  inconsistent:
    status: "WARNING"
    description: "Có ít nhất một cảnh báo mâu thuẫn hoặc thiếu kịch bản kiểm thử được kích hoạt."
```
</output_contract>
