# 05 — How to Write Comments

> Phase 3 critical. Đây là "tone" của reviewer. Load trước khi viết nhận xét.

## A. Courtesy — Critique code, not the person

* **Tồi**: "Tại sao **bạn** dùng thread ở đây khi rõ ràng concurrency chẳng mang lại lợi ích gì?"
* **Tốt**: "Mô hình concurrency ở đây đang tăng độ phức tạp mà tôi chưa thấy lợi ích hiệu năng cụ thể nào. Vì không có lợi ích rõ rệt, đoạn code này nên thiết kế chạy đơn luồng."

## B. Explain Why

Đưa bối cảnh, tài liệu, nguyên tắc thiết kế đằng sau nhận xét.

## C. Giving Guidance, not Doing the Work

* **Sửa CL là nhiệm vụ của tác giả**, không phải reviewer.
* Cân bằng giữa "chỉ ra lỗi" và "hướng đi cụ thể".
* Chỉ ra lỗi để tác giả tự suy nghĩ giúp họ học nhanh hơn.

## D. Severity Labels (BẮT BUỘC dùng)

| Label | Ý nghĩa | Blocking? |
|-------|----------|-----------|
| `Nit:` | Thẩm mỹ nhỏ nhặt. Author nên làm nhưng có thể bỏ qua | Không |
| `Optional:` / `Consider:` | Gợi ý mở rộng, hướng đi khác có thể tốt hơn | Không |
| `FYI:` | Knowledge sharing, link bài viết, không yêu cầu action | Không |
| `Must Fix:` (blocking) | Critical logic/security/concurrency/architecture | **Có** |

## E. Accept Explanations in the Right Place

* Nếu tác giả giải thích code khó hiểu trên review tool → **bắt buộc đưa vào code**
  (refactor cho rõ hơn hoặc comment trực tiếp).
* Không chấp nhận "explain trên tool" — sẽ trôi mất, không giúp future dev.
