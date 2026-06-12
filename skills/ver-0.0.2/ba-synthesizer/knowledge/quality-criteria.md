# Tiêu chí Chất lượng Tài liệu (Quality Criteria)

Tài liệu này định nghĩa bộ tiêu chuẩn kiểm định định lượng cho 7 Deliverables được kế thừa từ Stage -1.

<context>
Mục tiêu là cung cấp các định nghĩa chi tiết về chất lượng tối thiểu cho từng deliverable để làm cơ sở cho pha chấm điểm và đánh giá chất lượng tài liệu trước khi bàn giao cho Explorer.
</context>

<output_contract>
```yaml
quality_gate:
  pass_threshold: 0.80
  calculation_method: weighted_sum
  deliverables:
    elicitation_report:
      weight: 0.15
      min_criteria:
        - "Phải chuẩn hóa (normalize) mô tả hệ thống"
        - "Phải chỉ rõ các Pain Points hiện tại"
        - "Phải có danh sách các Giả định hệ thống (System Assumptions)"
    requirements_classification:
      weight: 0.15
      min_criteria:
        - "Phải phân biệt rõ ràng Functional Requirements (FR) và Non-Functional Requirements (NFR)"
        - "Phải có bảng phân loại độ ưu tiên MoSCoW đầy đủ"
    sequence_diagram:
      weight: 0.15
      min_criteria:
        - "Cú pháp Mermaid sequenceDiagram hợp lệ và không lỗi hiển thị"
        - "Phải có tối thiểu 3 tác nhân tham gia (ví dụ: User, Agent, Tool)"
    flowchart_activity:
      weight: 0.15
      min_criteria:
        - "Cú pháp Mermaid flowchart hoặc graph hợp lệ"
        - "Phải mô tả đầy đủ 3 luồng nghiệp vụ: Luồng chuẩn (Happy Path), Luồng thay thế (Alternative Path), Luồng ngoại lệ (Exception Path)"
    erd_schema:
      weight: 0.15
      min_criteria:
        - "Sơ đồ Mermaid ERD hợp lệ"
        - "Phải định nghĩa rõ ràng Primary Key (PK) và Foreign Key (FK)"
        - "Phải ghi rõ kiểu dữ liệu cho từng thuộc tính"
    acceptance_criteria:
      weight: 0.15
      min_criteria:
        - "Viết theo định dạng Gherkin chuẩn (Given-When-Then)"
        - "Phải có tối thiểu 3 kịch bản kiểm thử chi tiết"
    risk_matrix:
      weight: 0.10
      min_criteria:
        - "Phải xác định tối thiểu 3 rủi ro kỹ thuật hoặc nghiệp vụ"
        - "Mỗi rủi ro phải đi kèm với phương án giảm thiểu (Mitigation Plan) tương ứng"
```
</output_contract>

<instructions>
1. Khi đánh giá từng deliverable, gán điểm score_i từ 0.0 đến 1.0 dựa trên tỷ lệ đáp ứng các `min_criteria`.
2. Tính điểm chất lượng tổng hợp (Quality Score) theo công thức:
   `Quality Score = Sum(weight_i * score_i)`
3. Nếu Quality Score >= 0.80, gán trạng thái `PASS`. Nếu Quality Score < 0.80, gán trạng thái `WARNING`.
</instructions>
