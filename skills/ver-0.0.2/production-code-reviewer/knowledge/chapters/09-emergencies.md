# 09 — Emergencies

> Phase 2 reference. Phát hiện hotfix thiếu chuẩn.

## Thế nào là Emergency?

Thay đổi **nhỏ** nhằm:
* Vá lỗ hổng bảo mật nghiêm trọng.
* Giải quyết sự cố nghiêm trọng trên production.
* Xử lý vấn đề pháp lý khẩn cấp.
* Unblock major launch.

## KHÔNG phải Emergency

* Muốn launch tính năng tuần này thay vì tuần sau.
* Đã làm việc lâu trên CL, nôn nóng submit.
* Cuối ngày thứ Sáu, muốn check-in trước cuối tuần.
* Manager yêu cầu hoàn thành vì soft deadline.
* Rollback CL thường gây test fail (rollback thường KHÔNG phải emergency trừ khi sập prod).

## Hard vs Soft Deadline

* **Hard deadline**: lỡ = hậu quả thảm khốc (vi phạm pháp lý, mất cơ hội thị trường,
  lỡ firmware cycle đối tác phần cứng). → OK sacrifice.
* **Soft deadline**: chỉ là mong muốn. **Tuyệt đối không** sacrifice code health.

## Quy trình duyệt Emergency

1. Ưu tiên tối đa.
2. Nới lỏng tiêu chuẩn — chỉ tập trung **tốc độ** + **tính đúng đắn** của giải pháp.
   Chấp nhận bỏ qua style, structure chưa sạch.
3. **Bắt buộc post-review** — sau khi sự cố dập tắt, reviewer **phải** quay lại
   review toàn diện. Yêu cầu tác giả gửi CL bổ sung dọn nợ kỹ thuật, viết bù test.
