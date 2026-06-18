# 07 — Writing Good CL Descriptions

> Phase 2 reference. Kiểm tra CL description có đạt chuẩn không.

## Cấu trúc bắt buộc

```
Dòng 1: Imperative mô tả ngắn
<dòng trống bắt buộc>
Body: WHY + WHAT
Bug #, benchmark, design link
```

## Dòng 1 (First Line)

* Tóm tắt cực ngắn, cụ thể hành vi chính.
* **Imperative** (mệnh lệnh).
  * Tốt: "Delete the FizzBuzz RPC and replace it with the new system."
  * Xấu: "Deleting the FizzBuzz RPC..." / "Deleted the..." / "Fix bug"
* Sau dòng 1 phải có **1 dòng trống**.

## Body

* Vấn đề cần giải quyết là gì?
* Tại sao giải pháp này tối ưu?
* Hạn chế của giải pháp?
* Đính kèm: Bug #, benchmark, design doc link.

## Cập nhật trước submit

Nếu trong review, cấu trúc/logic CL thay đổi lớn so với thiết kế ban đầu →
**phải cập nhật lại CL description** trước khi submit, đảm bảo tính lịch sử đồng nhất.
