# 06 — Handling Pushback

> Phase 3 reference. Dùng khi author phản bác nhận xét của reviewer.

## Quy trình cho Reviewer

1. **Xem xét nghiêm túc ý kiến tác giả** — họ trực tiếp viết code, có thể nắm chi tiết
   thực tế bạn bỏ sót. Nếu họ đúng → cởi mở thừa nhận, đồng ý.
2. **Giải thích sâu hơn** — nếu chắc chắn đề xuất giúp code health, kiên trì bảo lưu
   quan điểm. Đưa lập luận chặt chẽ + dữ liệu kỹ thuật.
3. **Kiên trì lịch sự (Polite Persistence)** — "Tôi hiểu góc nhìn của bạn, nhưng
   tôi không đồng ý vì...". Giữ thái độ hòa nhã.

## "No Cleanup Later" — Bẫy phổ biến

* Tác giả: "Hãy duyệt đi, tôi sẽ dọn ở CL sau."
* **Thực tế**: Nếu không dọn ngay → sẽ **không bao giờ** dọn. Tác giả bị cuốn
  vào task khác, lời hứa trôi mất.
* **Yêu cầu**: Dọn ngay trong CL này trước khi submit.

### Ngoại lệ

* **Emergency** thực sự (chương 09).
* Code xung quanh quá lớn để sửa trong CL này → **bắt buộc**:
  1. Tạo bug ticket, gán cho chính mình.
  2. Viết comment `# TODO(<ticket-id>): ...` trong code.
