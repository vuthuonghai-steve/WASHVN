# Google Code Review Standards — Index

> Stage 3.5 knowledge base. Tổng hợp 10 chương từ Google Code Review Guidelines
> dịch sang tiếng Việt. Đọc file này để biết chapter nào cần load cho từng phase review.

## Cấu trúc chapters/

| Chapter | File | Phase sử dụng |
|---------|------|---------------|
| 01 — Triết lý & Standard of Code Review | `chapters/01-philosophy.md` | Phase 2 (semantic) — mọi review |
| 02 — What to Look For (A-J dimensions) | `chapters/02-what-to-look-for.md` | Phase 2 — quét toàn diện |
| 03 — Navigating a CL in Review | `chapters/03-navigating-cl.md` | Phase 2 — flow 3 bước |
| 04 — Speed of Code Reviews | `chapters/04-speed.md` | Phase 5 (handoff) — quyết định priority |
| 05 — How to Write Comments | `chapters/05-comment-style.md` | Phase 3 — labeled comments |
| 06 — Handling Pushback | `chapters/06-pushback.md` | Phase 3 — khi author phản bác |
| 07 — Writing Good CL Descriptions | `chapters/07-cl-description.md` | Phase 2 — kiểm tra CL description |
| 08 — Small CLs | `chapters/08-small-cls.md` | Phase 2 — kiểm tra scope |
| 09 — Emergencies | `chapters/09-emergencies.md` | Phase 2 — phát hiện hotfix không đạt chuẩn |
| 10 — Quick Reference Card | `chapters/10-quickref.md` | Phase 1 — boot loader cho LLM reviewer |

## Cách load (progressive disclosure Tier 3)

```yaml
phase_1_init:
  load: ["10-quickref.md"]                    # 1 chapter nhỏ, đủ rules summary

phase_2_semantic:
  load: ["01-philosophy.md", "02-what-to-look-for.md", "07-cl-description.md", "08-small-cls.md"]

phase_3_labeling:
  load: ["05-comment-style.md", "06-pushback.md"]   # tone & label guidance

phase_5_priority:
  load: ["04-speed.md", "09-emergencies.md"]        # chỉ khi cần quyết định LGTM now vs later
```

## 1. Giới thiệu & Triết lý cốt lõi

*   **Định nghĩa Code Review**: Quy trình một hoặc nhiều người ngoài tác giả kiểm tra,
    phân tích, đánh giá mã nguồn trước khi tích hợp vào codebase chung.
*   **Mục tiêu tối thượng**: Đảm bảo chất lượng mã nguồn tổng thể (overall code health)
    liên tục được cải thiện theo thời gian.
*   **Triết lý đồng hành**: Code review không chỉ tìm lỗi kỹ thuật, mà còn là cơ hội
    học hỏi, chia sẻ kiến thức, gắn kết văn hóa kỹ thuật và mentoring giữa các kỹ sư.

## 2. Tiêu chuẩn duyệt Code (The Standard of Code Review)

Duyệt code là nghệ thuật cân bằng giữa hai yếu tố đối lập:

1.  **Tiến độ của nhà phát triển** — lập trình viên phải đưa thay đổi vào hệ thống
    trơn tru. Nếu không có thay đổi nào được chấp nhận, hệ thống sẽ không cải tiến.
2.  **Sức khỏe codebase** — reviewer bảo vệ tính nhất quán, dễ bảo trì, hiệu năng.

### Nguyên tắc Vàng (Gold Standard)
> **Reviewer nên phê duyệt một CL ngay khi nó ở trạng thái chắc chắn cải thiện
> chất lượng tổng thể, ngay cả khi chưa thực sự hoàn hảo.**

*   Không tồn tại code "hoàn hảo" — chỉ có code "tốt hơn". Đừng ép tác giả trau
    chuốt từng lỗi nhỏ trước khi đồng ý.
*   Mục tiêu là **Cải tiến liên tục** (Continuous Improvement).
*   Nguyên tắc này không biện hộ cho việc đưa vào CL làm *xấu đi* hệ thống, ngoại
    trừ tình huống emergency đã quy định.

### Nguyên tắc Quyết định
*   **Kỹ thuật và dữ liệu tối cao** — sự thật kỹ thuật và số liệu thực tế có giá
    trị quyết định cao hơn ý kiến cá nhân.
*   **Quy chuẩn Style Guide** — Style Guide chính thức là cơ quan có thẩm quyền.
    Nếu không được quy định → sở thích cá nhân → chấp nhận style của tác giả.
*   **Thiết kế ≠ Sở thích** — quyết định thiết kế dựa trên nguyên tắc công nghệ vững
    (encapsulation, SRP, decoupling). Nếu tác giả chứng minh được nhiều phương án
    tốt tương đương → tôn trọng lựa chọn của tác giả.
*   **Nhất quán** — nếu không có quy tắc áp dụng, yêu cầu nhất quán với code xung quanh
    miễn không suy giảm chất lượng chung.

### Giải quyết Xung đột
1.  **Đồng thuận** — đối thoại dựa trên dữ liệu kỹ thuật.
2.  **Đổi phương thức giao tiếp** — nếu comment qua lại không hiệu quả, họp trực tiếp.
    Bắt buộc ghi lại tóm tắt kết quả lên CL để lưu lịch sử.
3.  **Leo thang** — nếu bế tắc, đưa vấn đề ra nhóm rộng hơn (Tech Lead, Maintainer,
    EM). Tuyệt đối không để CL bị ngâm vô thời hạn.

## 3. Những điểm cần tìm khi Code Review (10 chiều A-J)

| Dim | Tên | Trọng tâm |
|-----|-----|-----------|
| A | **Design** | Decoupling, encapsulation, placement, có thực sự cần thiết không |
| B | **Functionality** | Đúng mục đích? Concurrency safety? UI changes demo được? |
| C | **Complexity** | Đơn giản hay phức tạp quá mức? Cảnh giác over-engineering |
| D | **Tests** | Có unit/integration/e2e test? Test có thật sự fail khi code lỗi? |
| E | **Naming** | Tên có truyền tải rõ mục đích? Độ dài vừa đủ |
| F | **Comments** | Giải thích WHY (không WHAT). Ngoại lệ: regex, math algorithms |
| G | **Style** | Tuân thủ Style Guide. Cá nhân → `Nit:`. Không mix format với logic |
| H | **Documentation** | README/g3doc/API ref cập nhật theo code |
| I | **Every Line** | Reviewer phải đọc **từng dòng**. Code khó hiểu → yêu cầu refactor |
| J | **Encouragement** | Khen điểm tốt. Văn hóa tích cực thúc đẩy chất lượng |

## 4. Tốc độ Code Review (Speed)

*   **Mục tiêu**: Tối đa **1 ngày làm việc** để phản hồi lần đầu.
*   Không ngắt quãng bản thân khi đang trong flow → review tại **break points**
    (sau task, sau ăn trưa, sau họp, đầu/cuối ngày).
*   **LGTM With Comments** — phê duyệt luôn nếu bạn tin tác giả sẽ tự sửa, hoặc
    comment chỉ là đề xuất, hoặc lỗi rất nhỏ. Đặc biệt hữu ích khi lệch múi giờ.

## 5. Cách viết nhận xét

### A. Lịch sự & Tôn trọng
*   Critique **code**, không critique **con người**.
*   *Tồi*: "Tại sao **bạn** dùng thread ở đây?"
*   *Tốt*: "Mô hình concurrency đang tăng độ phức tạp mà chưa thấy lợi ích hiệu năng."

### B. Giải thích WHY
Đưa bối cảnh, tài liệu, nguyên tắc thiết kế đằng sau nhận xét.

### C. Định hướng, không làm hộ
Sửa CL là việc của tác giả. Cân bằng giữa "chỉ ra lỗi" và "hướng đi cụ thể".

### D. Severity labels
*   `Nit:` — nhỏ nhặt, thẩm mỹ
*   `Optional:` / `Consider:` — gợi ý mở rộng
*   `FYI:` — knowledge sharing
*   `Must Fix:` (blocking) — logic/security/concurrency nghiêm trọng

### E. Giải thích đúng nơi
Nếu tác giả giải thích code khó hiểu trên tool → bắt buộc đưa vào code (comment hoặc refactor).

## 6. Xử lý Pushback

1.  **Xem xét nghiêm túc** — tác giả có thể nắm chi tiết thực tế bạn bỏ sót.
2.  **Giải thích sâu hơn** — nếu chắc chắn đề xuất giúp code health, bảo lưu quan điểm
    bằng dữ liệu kỹ thuật.
3.  **Kiên trì lịch sự** — "Tôi hiểu góc nhìn của bạn, nhưng...".

### "No Cleanup Later"
*   CL "để dọn sau" = không bao giờ dọn. Yêu cầu dọn ngay trong CL này.
*   Ngoại lệ: emergency, hoặc code xung quanh quá lớn → bắt buộc tạo bug ticket +
    `# TODO(<ticket>):` trong code.

## 7. CL Description

```
Dòng 1: Imperative mô tả ngắn
<dòng trống>
Body: WHY + WHAT
Bug #: benchmark, design link
```

*   Dòng 1 imperative ("Delete X", không phải "Deleting X").
*   Update lại mô tả nếu CL thay đổi lớn trong review.

## 8. Small CLs

*   Lý tưởng ~100 dòng, trên 1000 = quá lớn.
*   Một self-contained change + tests + calling context.
*   **Tách Refactoring khỏi logic** — trộn lẫn = thảm họa cho reviewer.
*   Chiến lược: stacking CLs, tách theo file/tầng.

## 9. Emergencies

*   **Là** emergency: vá security, fix production outage, vấn đề pháp lý, unblock major launch.
*   **Không phải** emergency: muốn launch sớm, sắp hết ngày, manager yêu cầu deadline mềm.
*   Hard deadline: vi phạm pháp lý, mất cơ hội thị trường → OK sacrifice.
*   Soft deadline: **không** sacrifice code health.
*   Quy trình: ưu tiên tối đa, nới lỏng style, **bắt buộc post-review** để dọn nợ.

## 10. Quick Reference

```yaml
reviewer_golden_rule: "Approve a CL as soon as it's a net improvement to code health."
tone: "Critique code, never the person."
labels:
  must_fix:  "Logic/security/concurrency — blocking"
  optional:  "Architectural improvement — non-blocking"
  fyi:       "Knowledge sharing — no action"
  nit:       "Style/aesthetic — author can ignore"
speed:
  first_response: "≤ 1 business day"
  break_points:  ["after small task", "after lunch", "after meeting", "start/end day"]
lgtm_with_comments_when:
  - "Trust author will fix"
  - "Comment is suggestion only"
  - "Tiny typo/reformat"
small_cls:
  ideal_lines: 100
  too_big: 1000
  split_strategies: ["stacking", "by file/layer", "refactor vs logic"]
emergencies_require_post_review: true
```
