# 01 — Triết lý & Standard of Code Review

> Phase 2 reference. Load khi cần nền tảng triết lý để quyết định LGTM / Reject.

## 1.1 Định nghĩa

Code Review là quy trình **một hoặc nhiều người ngoài tác giả** kiểm tra, phân tích, đánh
giá mã nguồn trước khi tích hợp vào codebase chung.

## 1.2 Mục tiêu tối thượng

**Overall code health** liên tục được cải thiện theo thời gian. Mọi công cụ, chính
sách, quy trình đều phục vụ mục tiêu này.

## 1.3 Triết lý đồng hành

Code review không đơn thuần là tìm lỗi kỹ thuật — còn là:
* Cơ hội học hỏi
* Chia sẻ kiến thức
* Gắn kết văn hóa kỹ thuật
* Mentoring giữa các kỹ sư

## 1.4 Hai cực cân bằng

| Cực | Hậu quả nếu lệch |
|-----|------------------|
| **Tiến độ nhà phát triển** | Nếu chặn quá nhiều → lập trình viên nản lòng, giảm đóng góp |
| **Sức khỏe codebase** | Nếu bỏ qua → technical debt tích lũy, suy giảm dần theo thời gian |

## 1.5 Gold Standard

> **Reviewer nên phê duyệt một CL ngay khi nó ở trạng thái chắc chắn giúp cải thiện
> chất lượng tổng thể, ngay cả khi CL đó chưa thực sự hoàn hảo.**

* Không có code "hoàn hảo" — chỉ có code "tốt hơn".
* Mục tiêu: **Continuous Improvement**.
* Ngoại lệ: emergency theo chương 09.

## 1.6 Core Principles

1. **Kỹ thuật và dữ liệu tối cao** — facts > opinions.
2. **Style Guide là thẩm quyền** — ngoài Style Guide = sở thích = chấp nhận.
3. **Thiết kế ≠ sở thích** — quyết định dựa trên encapsulation/SRP/decoupling.
4. **Nhất quán** — nếu không có quy tắc, đòi hỏi consistent với code xung quanh.

## 1.7 Conflict Resolution

1. Đồng thuận dựa trên technical facts.
2. Đổi sang sync trực tiếp nếu async kém hiệu quả → bắt buộc ghi summary lên CL.
3. Leo thang (Tech Lead, Maintainer, EM) nếu bế tắc kéo dài.
