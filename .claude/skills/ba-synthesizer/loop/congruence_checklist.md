# Congruence Self-Check Checklist

Checklist tự kiểm tra tính toàn vẹn và nhất quán cho `ba-synthesizer` trước khi xuất bản `business-analysis.md`. Kế thừa từ `ver-0.0.2/synthesizer-checklist.md`, tái cấu trúc theo chuẩn Congruence Check của WASHVN ver-3.

Checklist này đóng vai trò cổng chất lượng cuối cùng (final quality gate) trước khi tài liệu rời khỏi BA pipeline. Agent bắt buộc phải chạy checklist này như một bước tự động trong quy trình synthesize. Không được phép bỏ qua hoặc rút gọn. Kết quả kiểm tra phải được ghi lại trong phần handoff metadata của business-analysis.md để downstream stages có thể truy vết.

## Danh mục kiểm tra

### Completeness (7 items — MUST pass before write)

Nhóm Completeness kiểm tra 7 deliverables bắt buộc của business-analysis.md. Mỗi deliverable phải có đủ nội dung tối thiểu theo quy định. Agent phải duyệt từng item và xác nhận PASS trước khi ghi file. Chỉ cần một item FAIL là đủ điều kiện từ chối xuất bản và yêu cầu quay lại bước synthesize.

Cách đọc: mỗi hàng trong bảng tương ứng với một deliverable cụ thể. Agent kiểm tra từ trên xuống dưới, đánh dấu PASS nếu nội dung đáp ứng đủ tiêu chí, FAIL nếu thiếu hoặc sai. Nếu có từ 1 FAIL trở lên ở Completeness, toàn bộ quá trình synthesize bị hủy và phải chạy lại.

| ID | Item |
|---|---|
| CHK-DEL-01 | Elicitation Report frontmatter + stakeholder analysis + NFR quantified đầy đủ |
| CHK-DEL-02 | Classification FR/NFR rõ ràng + bảng MoSCoW (P0-P3) đầy đủ |
| CHK-DEL-03 | Sequence Diagram ≥3 actors, Mermaid labels double-quote, đúng business flow |
| CHK-DEL-04 | Flowchart 3 paths rõ ràng (Happy / Alternative / Exception) |
| CHK-DEL-05 | ERD có PK/FK đầy đủ, data types per field |
| CHK-DEL-06 | Gherkin ≥3 scenarios (Given-When-Then), bao phủ 3 paths |
| CHK-DEL-07 | Risk Matrix Probability×Impact + mitigation cụ thể |

### Validation (5 items — WARNING, không block)

Nhóm Validation kiểm tra tính nhất quán chéo giữa các deliverable và chất lượng tổng thể. Các item này chỉ phát ra cảnh báo (WARNING), không chặn xuất bản. Tuy nhiên pipeline_ready (CHK-VAL-05) chỉ đặt true khi toàn bộ validation items đều PASS — nếu còn WARNING, pipeline chưa sẵn sàng.

Cách xử lý WARNING: agent ghi nhận vào phần handoff metadata, kèm lý do và đề xuất khắc phục. Downstream stage có thể dựa vào đó để quyết định có tiếp nhận hay yêu cầu làm lại. WARNING kéo dài qua nhiều vòng sẽ được escalate lên developer.

| ID | Item |
|---|---|
| CHK-VAL-01 | Actor-Entity consistent — không có warning [MAU THUẪN NGHIỆP VỤ] |
| CHK-VAL-02 | MoSCoW-Gherkin consistent — không có warning [THIẾU KỊCH BẢN KIỂM THỬ] |
| CHK-VAL-03 | Quality score weighted sum ≥ 0.80 (80%) |
| CHK-VAL-04 | Schema validation PASS (schema_validator.py exit 0) |
| CHK-VAL-05 | pipeline_ready chỉ true khi mọi điều kiện thỏa mãn |

### Format (2 items — MUST pass before write)

Nhóm Format đảm bảo chất lượng định dạng tài liệu đầu ra. YAML frontmatter phải parse hợp lệ để các công cụ downstream có thể đọc metadata. Tuyệt đối không chứa placeholder (TODO, TBD, mock, pass, dấu ba chấm ...). FAIL bất kỳ item nào đồng nghĩa với việc từ chối xuất bản ngay lập tức, không cần kiểm tra tiếp các item còn lại.

| ID | Item |
|---|---|
| CHK-FMT-01 | YAML frontmatter parse hợp lệ |
| CHK-FMT-02 | Không placeholder (TODO/TBD/mock/...) |

<instructions>
Trước khi write business-analysis.md, duyệt 14 items. ALL completeness (CHK-DEL-01..07) + format (CHK-FMT-01..02) MUST pass. Validation items WARNING không block.
</instructions>
