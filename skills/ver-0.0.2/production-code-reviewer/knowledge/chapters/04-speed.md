# 04 — Speed of Code Reviews

> Phase 5 priority. Dùng để quyết định LGTM now vs hẹn review sau.

## Hậu quả của review chậm

* Vận tốc đội giảm mạnh (CL bị treo → tắc nghẽn → merge conflict).
* Developer ức chế (đặc biệt khi reviewer chậm + khắt khe).
* Ảnh hưởng xấu tới code health (áp lực deadline → bỏ qua tiêu chuẩn).

## Tiêu chuẩn tốc độ

* **First response ≤ 1 business day** (muộn nhất sáng hôm sau).
* Nếu không bận tập trung cao độ → ưu tiên review ngay.

## Speed vs Interruption

**Không tự ngắt flow**. Review tại break points:
* Sau task lập trình nhỏ.
* Sau ăn trưa / uống nước.
* Sau họp.
* Đầu/cuối ngày.

## Fast responses quan trọng hơn

Tốc độ từng lượt phản hồi quan trọng hơn tốc độ toàn bộ quá trình. Nếu quá bận →
gửi tin nhắn ngắn hẹn giờ, hoặc đề xuất reviewer khác để unblock.

## LGTM With Comments

Phê duyệt luôn kể cả khi còn comment chưa resolve, NẾU:
* Tin tác giả sẽ tự sửa đúng.
* Comment chỉ là đề xuất.
* Lỗi rất nhỏ (typo, reformat).

Đặc biệt hữu ích khi hai bên lệch múi giờ.
