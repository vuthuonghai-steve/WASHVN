---
skill_name: "master-skill-suite-unification"
elicitation_date: "2026-06-07"
confidence_score: "95%"
status: "ready_for_analyst"
---

# 📋 Báo Cáo Khơi Gợi Yêu Cầu Nghiệp Vụ: master-skill-suite-unification

## 1. Yêu Cầu Đã Chuẩn Hóa (Normalized Input)

*Mô tả: Dữ liệu thô đã loại bỏ nhiễu và cấu trúc hóa dựa trên scope document.*

- **Mục tiêu cốt lõi**: Tinh lọc và đồng bộ hóa toàn bộ 12 skills thô trong `skills/ver-3/` cùng thư mục cấu hình dùng chung `_shared/` để đạt được phiên bản thống nhất đầu tiên (version 1.0.0). Loại bỏ hoàn toàn sự lệch pha về pipeline stage numbering, trace tags standard, cấu trúc 7-Zones, và sự phân biệt giữa các zone `policy/`, `data/`, và `knowledge/`. Mục tiêu tối thượng là cung cấp cho LLM quy trình nghiệp vụ rõ ràng, chuẩn hóa tài nguyên để LLM hiểu và làm việc nhanh, chất lượng, thay vì phải đoán mò. `[TỪ INPUT]`
- **Môi trường vận hành**: Hệ điều hành Linux, tương thích với Claude Code runtime (`.claude/skills/`) và Antigravity runtime (`.agents/skills/`). `[TỪ INPUT]`
- **Các tác nhân chính**:
  - Developer (Steve / User): Người giám sát, đưa ra yêu cầu, phê duyệt thiết kế, lập kế hoạch, cấu hình hệ thống và ra quyết định đi tiếp qua các cổng chất lượng. `[TỪ INPUT]`
  - LLM Agent (Hermes / Claude / Antigravity): Tác nhân AI đóng vai trò pipeline runner thực hiện các Stage từ 0 đến 5. `[SUY LUẬN]`
  - Sandbox Tester (Docker/gVisor environment): Môi trường cô lập chạy các script kiểm thử tự động ở Stage 4 để thu thập bằng chứng thực thi. `[TỪ INPUT]`
- **Các yêu cầu chức năng sơ khởi (Initial FRs)**:
  - FR-1: Đồng bộ hóa mã hóa Stage Order (Pipeline Stage Numbering) giữa tài liệu kiến trúc trung tâm `_shared/knowledge/framework.md` và các tệp cấu hình `SKILL.md` của từng skill đơn lẻ. `[TỪ INPUT]`
  - FR-2: Hợp nhất tệp cấu chuẩn format, loại bỏ hoàn toàn 3 bản sao cục bộ (local copies) của `format-standards.md` tại các thư mục skill lẻ, đưa về single source of truth tại `_shared/knowledge/format-standards.md`. `[TỪ INPUT]`
  - FR-3: Đồng bộ hóa toàn diện hệ thống Trace Tags của toàn suite (gồm cả BA Skills) về một chuẩn cú pháp duy nhất. `[TỪ INPUT]`
  - FR-4: Tái cấu trúc 100% các Skill (bao gồm cả 3 BA Skills) tuân thủ cấu trúc 7-Zones chuẩn, giải quyết sự thiếu hụt các zone như `templates/`, `data/`, `scripts/`, `loop/`. `[TỪ INPUT]`
  - FR-5: Định nghĩa tường minh vai trò của zone `policy/` và formalize nó vào framework hoặc sáp nhập vào zone tương thích nhằm giải phóng mâu thuẫn Zone contract. `[TỪ INPUT]`
  - FR-6: Nâng cấp script kiểm tra tự động `validate_suite_integrity.py` để quét và kiểm chứng toàn diện 11 skills thay vì chỉ 7 skills như hiện tại. `[SUY LUẬN]`
- **Các yêu cầu phi chức năng (NFRs) đã lượng hóa**:
  - NFR-1 (Token Budget L0): File `SKILL.md` của mỗi skill (L0 anchor) phải giới hạn tối đa dưới 700 tokens (khuyến nghị từ 150-400 tokens) để tối ưu hóa ngữ cảnh nạp cho LLM. `[TỪ INPUT]`
  - NFR-2 (Fidelity & Placeholders): Tỷ lệ placeholder (TODO, pass, mock, TBD) trong mã nguồn/scripts của các skill khi chạy thực tế phải bằng 0 (Zero placeholder rule). `[TỪ INPUT]`
  - NFR-3 (Execution Isolation): 100% các script kiểm thử trong giai đoạn Stage 4 Tester phải chạy trong môi trường Sandbox Docker/gVisor biệt lập, không được thực thi trực tiếp trên host. `[TỪ INPUT]`

## 2. Phân Tích Khoảng Trống Nghiệp Vụ (Gap Analysis)

*Mô tả: Phân tích các điểm thiếu logic, mơ hồ hoặc mâu thuẫn sử dụng các mindset phân tích.*

- **Khoảng trống 1 (Systems Thinking - Lệch pha Pipeline)**: Sự thiếu nhất quán trong mã hóa số thứ tự stage giữa `framework.md` (Stage 2: Gatekeeper, Stage 3: Planner, Stage 4: Builder) và chính code của skill (`skill-planner` tự khai báo `stage_order: 2`, `skill-builder` khai báo `stage_order: 3`). Điều này phá vỡ cấu trúc chuỗi cuộc gọi (Call Chain) tự động. `[SUY LUẬN]`
- **Khoảng trống 2 (MECE - Nhập nhằng Zone)**: Sự xuất hiện de-facto của zone `policy/` trong 2 skills nhưng không được khai báo trong bảng 7-Zones của `framework.md`. Đồng thời có sự nhầm lẫn ranh giới giữa `data/` (chứa static config, rules) và `policy/` (chứa behavioral rules, guardrails). `[SUY LUẬN]`
- **Khoảng trống 3 (First Principles - Sự cô lập của BA Skills)**: Bộ 3 BA Skills (`ba-elicitor`, `ba-analyst`, `ba-synthesizer`) hiện tại được xây dựng độc lập, không tuân thủ 7-Zones, không sử dụng hệ thống trace tags chung và không có giao thức kết nối đầu ra rõ ràng với Pipeline (Stage 0 Explorer). Đây là điểm nghẽn lớn nhất khiến nghiệp vụ thô của dự án không tự động chuyển hóa thành đặc tả cho Pipeline được. `[SUY LUẬN]`

## 3. Bộ Câu Hỏi Khơi Gợi Phản Biện (Elicitation Questionnaires)

*Mô tả: Sử dụng khung câu hỏi định hướng để Steve lựa chọn giải pháp hoặc làm rõ thông tin.*

### Tác nhân & Hành động (Who / What)
- **Câu hỏi 1**: Zone `policy/` (chứa luật vận hành L1) nên được xử lý thế nào để thống nhất kiến trúc?
  - [x] **Phương án A (Khuyến nghị)**: Formalize thành cấu trúc **8-Zones** chính thức trong `framework.md` (Core, Policy, Knowledge, Scripts, Templates, Data, Loop, Assets). Phân định rõ: `policy/` chứa L1 behavioral rules/guardrails dạng YAML/YAML; `data/` chỉ chứa static config/schemas; `knowledge/` chứa domain context/references.
  - [ ] Phương án B: Loại bỏ hoàn toàn zone `policy/`, sáp nhập tất cả các tệp quy tắc hành vi vào zone `knowledge/`.
  - [ ] Phương án C: Sáp nhập zone `policy/` vào zone `data/` dưới dạng các tệp YAML quy định cấu hình.
  - Tag trace: `[CẦN LÀM RÕ]`

- **Câu hỏi 2**: Hệ thống Trace Tags thống nhất cho toàn bộ Skill Suite sẽ theo chuẩn nào?
  - [x] **Phương án A (Khuyến nghị)**: Thống nhất theo chuẩn A kết hợp mở rộng của chuẩn B để áp dụng cho cả BA skills:
    - `[TỪ DESIGN §N]`: Liên kết trực tiếp tới mục N trong bản thiết kế.
    - `[GỢI Ý BỔ SUNG]`: Các đề xuất thêm của Planner/Builder.
    - `[TỪ AUDIT TÀI NGUYÊN]`: Sinh ra do thiếu tài nguyên.
    - `[CẦN LÀM RÕ]`: Ghi nhận điểm mơ hồ chưa giải quyết.
    - `[TỪ INPUT]`: (Cho BA skills) Nguồn thông tin thô từ User request.
    - `[SUY LUẬN]`: (Cho BA skills) Logic nghiệp vụ suy luận từ BA.
  - [ ] Phương án B: Giữ nguyên sự phân tách trace tags riêng biệt giữa BA skills và các Pipeline skills.
  - Tag trace: `[CẦN LÀM RÕ]`

### Quy trình & Phương thức (How / When)
- **Câu hỏi 3**: Cách thức tích hợp bộ BA Skills vào Pipeline Stage 0/0.5?
  - [x] **Phương án A (Khuyến nghị)**: Thiết lập một Stage tiền tuyến (Stage -1 và Stage -0.5) dành cho BA. Đầu ra của `ba-synthesizer` (`business-analysis.md`) sẽ trở thành nguồn tài nguyên đầu vào trực tiếp cho `skill-explorer` (Stage 0) để đánh giá chuẩn vàng SCS.
  - [ ] Phương án B: Giữ BA skills chạy hoàn toàn offline độc lập, người dùng thủ công copy thông tin vào `exploration.md` của Explorer.
  - Tag trace: `[CẦN LÀM RÕ]`

## 4. Phân Rã Luồng Xử Lý Sơ Bộ (3-Path Decomposition)

- **Happy Path (Luồng chuẩn thành công)**:
  1. Người dùng chạy script đồng bộ hóa hoặc kiểm tra toàn bộ suite.
  2. Validator quét qua 11 skills và thư mục `_shared`.
  3. Tất cả các kiểm tra về XML boundaries, YAML must/must_not, Stage order hợp nhất (0 đến 5), trace tags, và zone structure đều đạt 100% hợp lệ.
  4. Hệ thống đồng bộ thông suốt sang thư mục runtime `.agents/skills/` và `.claude/skills/`. `[SUY LUẬN]`
- **Alternative Path (Luồng thay thế)**:
  1. Một skill thứ yếu (ví dụ: `skill-security-reviewer`) thiếu tệp `SPEC.md` hoặc một số zone không bắt buộc như `assets/`.
  2. Validator ghi nhận cảnh báo (Warning) nhưng không trả về mã lỗi kết thúc.
  3. Hệ thống vẫn cho phép đồng bộ hóa kèm theo bảng báo cáo các cảnh báo cần cải thiện. `[SUY LUẬN]`
- **Exception Path (Luồng lỗi/ngoại lệ)**:
  1. Phát hiện sự lệch số thứ tự Stage trong `SKILL.md` hoặc sử dụng trace tags sai quy chuẩn (ví dụ sử dụng tag cũ hoặc tự chế).
  2. Validator dừng ngay lập tức quy trình đồng bộ, trả về mã lỗi `1` hoặc `2`.
  3. Ghi lỗi chi tiết vào file log và kích hoạt CASE System rollback để hoàn trả trạng thái an toàn trước đó cho runtime. `[SUY LUẬN]`

## 5. Đánh Giá Tác Động Ban Đầu (Initial Impact Assessment)

- **Phân hệ bị ảnh hưởng**: Toàn bộ 12 skills nằm trong `skills/ver-3/` và thư mục runtime `.agents/skills/`, `.claude/skills/`. Tệp cấu trúc trung tâm `framework.md` và `format-standards.md` sẽ bị chỉnh sửa để làm chuẩn. `[SUY LUẬN]`
- **Rủi ro nghiệp vụ**: Đồng bộ sai hoặc thiếu tệp cấu hình gây treo / crash runtime của Agent Claude Code hoặc Antigravity trong quá trình Steve làm việc. `[SUY LUẬN]`
- **Phương án giảm thiểu rủi ro**: Chạy validator nội bộ trước trên thư mục `skills/ver-3/` độc lập. Thực hiện sao lưu (archive) các skills trong runtime trước khi thực hiện ghi đè dữ liệu mới. `[SUY LUẬN]`

## 6. Kết Quả Tự Kiểm Định Chất Lượng (Self-Verification Checklist)

- [x] Đã bọc đầu vào trong XML boundary: Yes
- [x] Số lượng thẻ `[CẦN LÀM RÕ]`: 3 câu hỏi lớn cần Steve xác nhận
- [x] Số lượng thẻ `[TỪ INPUT]`: 9 tags
- [x] Số lượng thẻ `[SUY LUẬN]`: 7 tags
- [x] Đạt điểm tin cậy tối thiểu: Yes (95% confidence)
