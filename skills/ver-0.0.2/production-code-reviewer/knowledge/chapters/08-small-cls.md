# 08 — Small CLs

> Phase 2 reference. Kiểm tra scope của CL.

## Tại sao CL nhỏ?

* Duyệt nhanh hơn (5 phút thay vì 1 tiếng).
* Duyệt kỹ hơn.
* Ít bug hơn (kiểm soát tác động biên dễ hơn).
* Tránh lãng phí nếu bị bác.
* Dễ merge, dễ rollback.

## Định nghĩa "Small"

* Một self-contained change khép kín.
* Có tests đi kèm.
* System vẫn build + chạy trơn tru sau khi submit.
* Không quá nhỏ đến mất context (API mới → cần ít nhất 1 caller).
* **Định lượng**: ~100 dòng lý tưởng. > 1000 dòng = quá lớn.
* Reviewer có quyền bác thẳng thừng chỉ vì CL quá lớn.

## Chiến lược chia nhỏ

1. **Stacking** — viết CL 1, gửi review, không chờ → viết tiếp CL 2 phân nhánh
   từ CL 1. Hầu hết VCS (Git/Piper) hỗ trợ.
2. **Tách theo file/tầng** — gửi riêng Protobuf definition CL và CL sử dụng nó.
   Có thể review song song bởi nhóm chuyên biệt.
3. **Tách biệt Refactoring** — **luôn** tách refactor (rename, move file) khỏi
   feature change. Trộn lẫn = thảm họa reviewer.
