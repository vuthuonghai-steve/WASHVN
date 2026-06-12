# Logic Chuẩn Hóa và Phản Biện Đầu Vào (Normalization & Clarification Logic)

Tài liệu này chi tiết hóa luồng xử lý và logic nghiệp vụ để chuẩn hóa thông tin đầu vào tự do và phản biện lượng hóa NFR.

## 1. Luồng Kỹ Năng (Skills Flow)

```
RawInput (bọc trong XML) → 1. Chuẩn hóa → 2. Phân tích Khoảng trống → 3. Sinh 5W1H → 4. Đóng gói Report
```

## 2. Input Normalization (Chuẩn hóa Đầu vào)

**Nhiệm vụ**: Nhận văn bản thô từ người dùng, loại bỏ nhiễu và bóc tách thành các trường dữ liệu có cấu trúc.

- **Ranh giới đầu vào**: Enforce bọc trong thẻ XML `<user_skill_request>...</user_skill_request>`.
- **Khử nhiễu**: Loại bỏ các đoạn văn cảnh thừa, chào hỏi xã giao, giải thích ngoài lề không mang giá trị kỹ thuật.
- **Bóc tách thực thể**: Ánh xạ thông tin vào cấu trúc của `input-schema.yaml` để thu được các trường chính như `skill_name`, `core_objective`, `environment`.

## 3. Proactive Clarification (Phản biện Chủ động)

**Nhiệm vụ**: Quét tìm các từ ngữ mô tả mang tính cảm tính, định tính để ép lượng hóa thành chỉ số kỹ thuật cụ thể (NFR).

- **Nhận diện tính từ cảm tính**: Phát hiện các từ khóa mơ hồ như "nhanh", "dễ dùng", "tốt", "mượt mà", "an toàn tối đa".
- **Ánh xạ chỉ số NFR**: Chuyển đổi các từ mơ hồ thành chỉ số đo lường:
  - "nhanh" → Latency (ms), Throughput (requests/sec).
  - "mượt mà" → Response time (ms), Frame rate (fps).
  - "an toàn" → Security gates, authentication method, rate limiting thresholds.
  - "tối ưu token" → Token budget limits.
- **Trường hợp không lượng hóa được**: Gắn trace tag `[CẦN LÀM RÕ]` và tự động sinh câu hỏi 5W1H tương ứng để yêu cầu người dùng xác nhận.

## 4. Structured Output Generation (Sinh Báo cáo Có Cấu trúc)

**Nhiệm vụ**: Xuất file `elicitation-report.md` theo template chuẩn tại `.skill-context/{feature_name}/ba-elicitor/elicitation-report.md`.

- **Nguyên tắc bảo toàn thông tin**: Bảo đảm zero information loss từ yêu cầu thô của người dùng.
- **Đường dẫn xuất file**: `.skill-context/{feature_name}/ba-elicitor/elicitation-report.md`
- **Ràng buộc Trace Tags**: Buộc phải gắn các thẻ nguồn gốc thông tin:
  - `[TỪ INPUT]`: Dữ liệu có nguồn gốc trực tiếp từ văn bản của người dùng.
  - `[SUY LUẬN]`: Dữ liệu do Agent suy luận logic dựa trên bối cảnh và tri thức (phải ghi rõ lý do).
  - `[CẦN LÀM RÕ]`: Dữ liệu còn thiếu, chưa rõ ràng hoặc mơ hồ cần người dùng trả lời hoặc làm rõ thêm.
