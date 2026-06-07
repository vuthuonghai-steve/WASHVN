# Định Nghĩa Phạm Vi Hoạt Động (Scope & Contract Definition)

Tài liệu này đặc tả ranh giới, các hợp đồng đầu vào/đầu ra, độ tin cậy và cơ chế bàn giao (handoff) của BA Elicitor.

## 1. Điểm Khởi Đầu (Entry Point)

- **Vị trí**: Hoạt động ở Stage -1 (MS-1), là bộ lọc đầu tiên của pipeline nghiệp vụ.
- **Trigger**: Nhận được yêu cầu xây dựng hoặc nâng cấp kỹ năng dưới dạng văn bản thô từ người dùng.
- **Boot Sequence (Chuỗi Khởi động)**: Kích hoạt `SKILL.md` → Nạp `knowledge/mindset-keywords.md` → Nạp `knowledge/elicitation-rules.md`.

## 2. Hợp Đồng Đầu Vào (Input Contract)

- **Định dạng**: Văn bản tự do (free-text) hoặc YAML có cấu trúc.
- **Ràng buộc**: Bắt buộc bọc trong thẻ XML `<user_skill_request>...</user_skill_request>` để ngăn chặn Prompt Injection.
- **Cấu trúc tham chiếu**: Định nghĩa tại `data/input-schema.yaml`.

## 3. Hợp Đồng Đầu Ra (Output Contract)

- **Tệp kết quả**: `elicitation-report.md` được ghi vào thư mục ledger của kỹ năng: `.skill-context/{feature_name}/ba-elicitor/elicitation-report.md`.
- **Định dạng**: Markdown tích hợp YAML Frontmatter.
- **Các phần bắt buộc (Required Sections)**:
  - `frontmatter` (chứa confidence score, metadata).
  - `normalized_input` (dữ liệu thô đã được cấu trúc hóa).
  - `gap_analysis` (khoảng trống nghiệp vụ phát hiện được).
  - `elicitation_questionnaires` (bộ câu hỏi 5W1H và gợi ý lựa chọn).
  - `initial_impact_assessment` (phân tích tác động chéo sơ khởi).
  - `self_verification_checklist` (kết quả tự kiểm định chất lượng).
- **Ràng buộc Trace Tags**: Gắn chặt các nhãn `[TỪ INPUT]`, `[SUY LUẬN]`, `[CẦN LÀM RÕ]`.

## 4. Danh Sách Phụ Thuộc (Dependencies)

| Tên file | Vai trò | Bắt buộc |
|:---|:---|:---|
| `SKILL.md` | Chứa persona và các luồng xử lý chính | Có |
| `knowledge/mindset-keywords.md` | Cung cấp 6 từ khóa tư duy phản biện | Có |
| `knowledge/elicitation-rules.md` | Quy tắc anti-hallucination và stop conditions | Có |

## 5. Cơ Chế Bàn Giao (Handoff)

Sau khi file `elicitation-report.md` được ghi thành công với 100% checklist kiểm định vượt qua, bối cảnh sạch sẽ được chuyển giao trực tiếp cho **ba-analyst (Stage 0 / MS-2)** để thực hiện pha phân tích chi tiết.

## 6. Rủi Ro & Giải Pháp Giảm Thiểu (Risks & Mitigations)

| Rủi ro | Mức độ | Phương án giảm thiểu |
|:---|:---|:---|
| Input quá mơ hồ, thiếu thông tin nghiêm trọng | **Cao** | Nếu confidence score < 60%, dừng quy trình và tạo bộ câu hỏi khơi gợi HITL. Nếu chạy tự động, giả định an toàn và đánh dấu `[CẦN LÀM RÕ]`. |
| Prompt Injection qua input tự do của người dùng | **Cao** | Cô lập input bằng thẻ XML `<user_skill_request>`, cấm thực thi câu lệnh động. |
| Hallucination (Tự bịa đặt chi tiết kỹ thuật/nghiệp vụ) | **Trung bình** | Phân tách rạch ròi bằng trace tags. Nghiêm cấm coi `[SUY LUẬN]` là sự thật nghiệp vụ chưa kiểm chứng. |
| Tràn ngữ cảnh của Agent (Context Overflow) | **Trung bình** | Áp dụng cơ chế Progressive Disclosure (chỉ nạp các file tri thức theo pha cần thiết). |

## 7. Tiêu Chuẩn Chất Lượng (Quality Checklist)

- [ ] Lọc và cô lập thành công đầu vào qua thẻ XML `<user_skill_request>`.
- [ ] Gắn tối thiểu 3 nhãn `[CẦN LÀM RÕ]` nếu input ban đầu mơ hồ.
- [ ] Đầy đủ bộ câu hỏi 5W1H và cơ chế phân tách 3 paths (Happy/Alternative/Exception).
- [ ] Ghi nhận Confidence Score rõ ràng trong frontmatter của báo cáo đầu ra.
- [ ] Đạt 100% các tiêu chí tự kiểm định trước khi xuất báo cáo.
- [ ] Tuyệt đối không chứa bất kỳ placeholder (`TODO`, `pass`, `...`) nào trong báo cáo.
