# 10 — Quick Reference Card

> Phase 1 boot loader. Reviewer LLM đọc file này đầu tiên.

## Golden Rule
> **Approve a CL as soon as it's a net improvement to code health.**

## Tone
* Critique code, never the person.
* Explain WHY, give guidance (not full rewrite).
* Encourage — khen điểm tốt.

## Severity Labels (BẮT BUỘC)

| Label | Blocking? | Dùng khi |
|-------|-----------|----------|
| `Must Fix:` | ✅ | Logic/security/concurrency/architecture nghiêm trọng |
| `Optional:` | ❌ | Architectural improvement, alternative design |
| `FYI:` | ❌ | Knowledge sharing, link bài viết |
| `Nit:` | ❌ | Style/aesthetic, author có thể bỏ qua |

## Speed Rules

* First response: **≤ 1 business day**.
* Break points only (không ngắt flow).
* LGTM with Comments khi: tin author tự sửa, comment chỉ là đề xuất, lỗi rất nhỏ.

## Small CL Heuristics

* Ideal: ~100 dòng.
* Too big: > 1000 dòng.
* Self-contained change + tests + at least 1 caller (nếu API mới).
* Tách refactor khỏi feature.

## 10 chiều cần quét (A-J)

A-Design, B-Functionality, C-Complexity, D-Tests, E-Naming,
F-Comments, G-Style, H-Documentation, I-Every Line, J-Encouragement.

## CL Description Template

```
Dòng 1: Imperative mô tả ngắn
<blank>
Body: WHY + WHAT + Bug# + benchmark + design link
```

## Emergency Post-Review

Sau khi hotfix deployed → **bắt buộc** post-review toàn diện. Nếu không → flag
trong review report với label `Must Fix: post-review-required`.
