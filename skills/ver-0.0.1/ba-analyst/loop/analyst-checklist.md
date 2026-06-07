# 🏁 Checklist Tự Kiểm Định Chất Lượng Báo Cáo Phân Tích

Tài liệu này đóng vai trò là Quality Gate tự động cho Agent trước khi hoàn thành công việc phân tích nghiệp vụ và bàn giao đặc tả kỹ thuật.

<context>
Để đảm bảo đầu ra của pha phân tích đạt chất lượng tốt nhất, không có lỗi cú pháp và đầy đủ thông tin kỹ thuật, Agent phải chạy checklist tự kiểm định này trên tệp `analysis-report.md` đã sinh ra.
</context>

## 1. Bảng Trạng Thái Tự Kiểm Định (Verification Checklist)

```yaml
quality_gates:
  QG-BA-01:
    name: "Tuân thủ XML/YAML frontmatter"
    criteria: "YAML Frontmatter đầy đủ 4 khóa: skill_name, analyzed_by, analyzed_at, status. Đã align analyzed_at sang elicited_at và status sang completed."
    mandatory: true
  QG-BA-02:
    name: "Đầy đủ 7 deliverables"
    criteria: "Tài liệu chứa đủ 7 phần bắt buộc mà không có bất kỳ TODO, TBD hoặc placeholder trống nào."
    mandatory: true
  QG-BA-03:
    name: "Mermaid syntax chính xác"
    criteria: "Tất cả các nhãn trong sơ đồ Sequence, Flowchart, ERD được bọc trong dấu ngoặc kép đôi. Sơ đồ Sequence có ≥3 actors. Sơ đồ Flowchart có Happy/Alt/Exception paths."
    mandatory: true
  QG-BA-04:
    name: "Gherkin coverage ≥ 3 scenarios"
    criteria: "Có ít nhất 3 kịch bản kiểm thử Given-When-Then tương ứng với Happy, Alternative, và Exception paths."
    mandatory: true
  QG-BA-05:
    name: "Traceability mapping đầy đủ"
    criteria: "Các yêu cầu phân loại, trường cơ sở dữ liệu và kịch bản kiểm thử được gắn trace tags chuẩn [TỪ INPUT]/[SUY LUẬN]/[CẦN LÀM RÕ]."
    mandatory: true
```

## 2. Các Bước Thực Thi Kiểm Định (Execution Checklist)

<instructions>
Agent thực hiện duyệt qua từng câu hỏi kiểm định dưới đây. Chỉ khi tất cả các mục "Must" đạt trạng thái "PASS" thì tài liệu mới được coi là đạt yêu cầu.
</instructions>

### A. Pha 1: Alignment & Stop Condition
- [ ] **Must**: Đầu vào có status là `pending_clarification` thì đầu ra có ghi chú dừng rõ ràng và không sinh giả định?
- [ ] **Must**: Đầu vào có status là `elicitation-completed` thì đầu ra đã được đổi tên thành `completed`?
- [ ] **Must**: Thuộc tính `analyzed_at` trong frontmatter đã được đồng bộ hóa với giá trị của `elicited_at` chưa?

### B. Pha 2: Phân loại FR/NFR & MoSCoW
- [ ] **Must**: 100% các yêu cầu phi chức năng (NFR) đã được lượng hóa bằng con số đo lường cụ thể?
- [ ] **Must**: Mỗi yêu cầu trong bảng MoSCoW có cột "Lý lý kỹ thuật" giải thích logic gán độ ưu tiên cụ thể không?

### C. Pha 3 & 4: Mermaid Diagrams & Data Schema
- [ ] **Must**: Có tối thiểu 3 thực thể tham gia vào sơ đồ Sequence Diagram?
- [ ] **Must**: Sơ đồ Flowchart có đầy đủ các nhánh Happy, Alternative và Exception chưa?
- [ ] **Must**: Các trường cơ sở dữ liệu trong ERD và Data Schema có kiểu dữ liệu rõ ràng (ví dụ: integer, string, timestamp)?
- [ ] **Must**: Sơ đồ Mermaid không có lỗi cú pháp do thiếu dấu ngoặc kép hoặc dùng ký tự đặc biệt ngoài nhãn?

### D. Pha 5 & 6: Gherkin & Risk Assessment
- [ ] **Must**: Có ít nhất 3 kịch bản Given-When-Then tương ứng với Happy, Alternative, và Exception paths?
- [ ] **Must**: Bảng đánh giá rủi ro có cột "Giải pháp giảm thiểu" ghi rõ giải pháp kỹ thuật cụ thể?
- [ ] **Must**: Có sự đồng bộ giữa Rủi ro cao + Must Have trong giải pháp kỹ thuật?

### E. Pha 7: Traceability Mapping
- [ ] **Must**: Toàn bộ các yêu cầu, trường cơ sở dữ liệu và scenarios kiểm thử đã được gán trace tag ngược về tài liệu khảo sát chưa?

---

## 3. Tiêu Chuẩn Phê Duyệt Đầu Ra (Approval Thresholds)

```yaml
approval_rules:
  pass_threshold: "100% các mục kiểm định 'Must' đạt PASS."
  failure_action: "Nếu có bất kỳ mục nào FAIL, Agent phải tái tạo hoặc chỉnh sửa lại tệp tin đầu ra cho đến khi pass hoàn toàn."
```
