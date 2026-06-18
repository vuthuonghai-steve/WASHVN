# 02 — What to Look For (10 chiều A-J)

> Phase 2 reference. Load khi quét toàn diện. Phase 3 dùng để label chính xác.

## A. Design (Quan trọng nhất)

* Tương tác giữa module mới và cũ có hợp lý?
* Code có đặt đúng chỗ (shared library vs inline)?
* Tích hợp hài hòa với hệ thống?
* Có thực sự cần thiết tại thời điểm này?

## B. Functionality

* Code có chạy đúng mục đích?
* Hành vi có lợi cho end-user và future dev maintain?
* **Concurrency safety** — race conditions, deadlocks, async correctness.
* UI changes — reviewer kiểm tra kỹ, yêu cầu demo nếu cần.

## C. Complexity

* Kiểm tra mọi cấp: dòng, hàm, class.
* Quá phức tạp = đọc giả không hiểu nhanh, future dev dễ viết sai.
* **Cảnh giác over-engineering / speculative programming**.

## D. Tests

* Mọi thay đổi chức năng → unit/integration/e2e test cùng CL.
* Test có thực sự fail khi code lỗi? Có false positive khi refactor?
* Test cũng là code cần bảo trì → không rườm rà.

## E. Naming

* Tên truyền tải rõ mục đích.
* Độ dài vừa đủ — không quá ngắn (mơ hồ), không quá dài (khó đọc).

## F. Comments

* Viết ngôn ngữ rõ ràng, dễ hiểu.
* Comment **WHY** (bối cảnh quyết định), không WHAT.
* Ngoại lệ: regex phức tạp, math algorithms.

## G. Style

* Tuân thủ Style Guide chính thức.
* Cá nhân → `Nit:`.
* **Nghiêm cấm gộp**: format cleanup riêng CL, không mix với logic.

## H. Documentation

* Nếu CL thay đổi build/config/interaction/release → update README, g3doc, API ref.

## I. Every Line

* Reviewer phải đọc **từng dòng**. Không scan qua loa.
* Code khó đọc → yêu cầu tái cấu trúc trước khi tiếp tục.
* Ngoại lệ: reviewer chỉ cover một phần CL → ghi rõ phạm vi đã duyệt.

## J. Encouragement

* Khen điểm tốt — thúc đẩy văn hóa tích cực, mentoring hiệu quả.
