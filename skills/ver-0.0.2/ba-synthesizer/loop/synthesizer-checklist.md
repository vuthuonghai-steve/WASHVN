# Checklist Hợp nhất và Kiểm tra Hoàn thiện (Synthesizer Checklist)

Tài liệu này cung cấp checklist tự kiểm tra cuối cùng cho `ba-synthesizer` trước khi bàn giao tài liệu cho Explorer (Stage 0).

<context>
Checklist này đảm bảo tính hoàn thiện cấu trúc, tính hợp lệ của cú pháp sơ đồ Mermaid và tính nhất quán chéo theo đúng cam kết chất lượng của Stage -1.
</context>

<output_contract>
```yaml
checklists:
  completeness_check:
    description: "Kiểm tra tính hoàn thiện cấu trúc của 7 Deliverables bắt buộc."
    items:
      - id: CHK_DEL_01
        text: "Elicitation Report có đầy đủ phần chuẩn hóa mô tả hệ thống, Pain Points và Giả định hệ thống."
      - id: CHK_DEL_02
        text: "Requirements Classification phân biệt rõ Functional/Non-Functional và hoàn thiện bảng MoSCoW."
      - id: CHK_DEL_03
        text: "Sequence Diagram viết bằng Mermaid hợp lệ và hiển thị đúng luồng giao tiếp giữa ít nhất 3 tác nhân."
      - id: CHK_DEL_04
        text: "Flowchart Activity viết bằng Mermaid hợp lệ và mô tả đủ 3 luồng: Happy Path, Alternative Path, Exception Path."
      - id: CHK_DEL_05
        text: "ERD Schema viết bằng Mermaid hợp lệ, định nghĩa rõ các khóa chính (PK), khóa ngoại (FK) và kiểu dữ liệu thuộc tính."
      - id: CHK_DEL_06
        text: "Acceptance Criteria viết bằng Gherkin định dạng Given-When-Then chuẩn với tối thiểu 3 kịch bản."
      - id: CHK_DEL_07
        text: "Risk Matrix có tối thiểu 3 rủi ro nghiệp vụ/kỹ thuật và giải pháp giảm thiểu rõ ràng."

  validation_and_integrity:
    description: "Kiểm định cú pháp và tính nhất quán chéo."
    items:
      - id: CHK_VAL_01
        text: "Đã thực hiện kiểm định chéo Actor-Entity và ghi nhận kết quả hoặc cảnh báo chéo."
      - id: CHK_VAL_02
        text: "Đã thực hiện kiểm định chéo MoSCoW-Gherkin và ghi nhận cảnh báo nếu tính năng Must-Have thiếu Scenario."
      - id: CHK_VAL_03
        text: "Điểm chất lượng được tính toán chính xác bằng công thức weighted sum theo đúng ma trận trọng số."
      - id: CHK_VAL_04
        text: "Cổng chất lượng được xác định chính xác: PASS nếu điểm >= 0.80, WARNING nếu điểm < 0.80."
      - id: CHK_VAL_05
        text: "Tài liệu business-analysis.md được sinh đầy đủ phần YAML frontmatter bàn giao (handoff metadata)."

  format_and_cleanliness:
    description: "Đảm bảo chất lượng định dạng và sạch mã nguồn."
    items:
      - id: CHK_FMT_01
        text: "Tài liệu hoàn toàn bằng tiếng Việt chuẩn (ngoại trừ thuật ngữ kỹ thuật và mã nguồn Gherkin/Mermaid)."
      - id: CHK_FMT_02
        text: "Tuyệt đối không chứa bất kỳ placeholder nào như TODO, TBD, mock, pass hoặc dấu ba chấm '...'."
```
</output_contract>

<instructions>
1. Trước khi ghi file `business-analysis.md`, duyệt qua từng checklist item.
2. Chỉ bàn giao tài liệu khi tất cả các checklist items thuộc nhóm `completeness_check` và `format_and_cleanliness` đều được đánh dấu hoàn thành.
3. Nếu phát hiện vi phạm quy tắc `format_and_cleanliness` (ví dụ còn placeholder), từ chối xuất bản tài liệu và yêu cầu điều chỉnh lại.
</instructions>
