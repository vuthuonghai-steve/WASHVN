---
skill_name: "raw-ver-3-production-sync"
elicitation_date: "2026-06-07"
confidence_score: "92%"
status: "ready_for_analyst"
---

# 📋 Báo Cáo Khơi Gợi Yêu Cầu: raw-ver-3-production-sync

## 1. Yêu Cầu Đã Chuẩn Hóa (Normalized Input)

<user_skill_request>
  <core_objective>Đưa bộ skill raw/ver-3 vào môi trường production với kiến trúc thống nhất</core_objective>
  <known_issues>
    <issue id="IS-01">Input/output giữa các stage không được enforce tự động</issue>
    <issue id="IS-02">Không có cơ chế rollback — stage sau phát hiện lỗi không biết quay lại stage nào</issue>
    <issue id="IS-03">LLM/AI mù tổng thể — chỉ thấy skill đang dùng, không thấy pipeline</issue>
    <issue id="IS-04">Thêm skill mới → đồng bộ hàng loạt thủ công</issue>
    <issue id="IS-05">Stage numbering lệch pha (planner/builder vs framework.md)</issue>
    <issue id="IS-06">format-standards.md bị nhân bản 3 bản sao cục bộ</issue>
    <issue id="IS-07">BA skills không tuân thủ 7-Zones, không trace tags</issue>
  </known_issues>
  <existing_artifacts>
    <artifact path="docs/context-to-work/architecture-sync/scope.2026-06-07.md"/>
    <artifact path="docs/context-to-work/arch-sync/analysis-report.md"/>
    <artifact path="docs/context-to-work/arch-sync/elicitation-report.md"/>
    <artifact path="docs/context-to-work/arch-sync/business-analysis.md"/>
    <artifact path="raw/ver-3/_shared/knowledge/framework.md"/>
  </existing_artifacts>
</user_skill_request>

**[TỪ INPUT]** — Các vấn đề được trích xuất trực tiếp từ yêu cầu của user.

## 2. Phân Tích Khoảng Trống Nghiệp Vụ (Gap Analysis)

### Khoảng trống 1: Systems Thinking — Thiếu Orchestration Layer [SUY LUẬN]
- **Phát hiện**: framework.md định nghĩa handoff contracts (Explorer→Architect→Planner→Builder) nhưng **không có cơ chế enforce**. Stage sau không validate input từ stage trước.
- **Vector anchor**: dependency mapping, systemic interaction, feedback loop analysis
- **Hậu quả**: LLM agent chạy skill đơn lẻ không biết mình đang ở stage nào, output không đúng format → stage sau fail.

### Khoảng trống 2: Root Cause — Thiếu Rollback Protocol [SUY LUẬN]
- **Phát hiện**: framework.md mô tả pipeline flow tuyến tính (0→0.5→1→2→3→3.5→4→X). Khi stage N phát hiện lỗi ở stage N-1, không có cơ chế "return to sender".
- **Vector anchor**: root cause isolation, causal decomposition
- **Hậu quả**: Lỗi tích lũy — càng về cuối pipeline càng nhiều lỗi chồng.

### Khoảng trống 3: MECE — Thiếu Global Context Registry [SUY LUẬN]
- **Phát hiện**: Mỗi skill là một silo. LLM dùng `skill-explorer` chỉ thấy exploration.md, không biết design.md (từ architect) hay todo.md (từ planner).
- **Vector anchor**: mutually exclusive, collectively exhaustive
- **Hậu quả**: LLM không thể đưa ra quyết định sáng suốt vì thiếu bức tranh toàn cảnh.

### Khoảng trống 4: First Principles — Không có cơ chế đồng bộ khi thêm skill mới [SUY LUẬN]
- **Phát hiện**: Khi thêm skill mới vào raw/ver-3, phải check thủ công: (1) stage order, (2) trace tags, (3) 7-Zones compliance, (4) format-standards sync, (5) _shared refs, (6) SKILL.md token budget, (7) validate_suite_integrity.py register.
- **Vector anchor**: fundamental truths, deconstruct assumptions
- **Giải pháp nền tảng**: Cần một suite_config.yaml làm single source of truth + auto-registration protocol.

### Khoảng trống 5: Impact Analysis — Stage Numbering Lệch Pha [TỪ INPUT]
- **Phát hiện**: `skill-planner` ghi `stage_order: 2`, `skill-builder` ghi `stage_order: 3` nhưng framework.md ghi Planner=Stage 3, Builder=Stage 4.
- **Vector anchor**: change impact vector, scope boundary detection
- **Hậu quả**: Nếu dùng stage_order để routing tự động → sai stage.

### Khoảng trống 6: Structural Decomposition — format-standards.md Nhân Bản [TỪ INPUT]
- **Phát hiện**: 3 bản sao local của format-standards.md tồn tại, nội dung có thể lệch so với master tại _shared/.
- **Vector anchor**: functional breakdown, granularity decomposition
- **Fix**: Xóa local copies, trỏ relative path về `_shared/knowledge/format-standards.md`.

### Khoảng trống 7: BA Skills Không Tuân Thủ Chuẩn [TỪ INPUT]
- **Phát hiện**: ba-elicitor, ba-analyst, ba-synthesizer không có templates/, data/, scripts/, loop/ zones. Không dùng trace tags chuẩn. Không có YAML frontmatter đầy đủ.
- **Vector anchor**: structural integrity, hierarchical task mapping
- **Hậu quả**: BA skills là "công dân hạng hai" — không tích hợp được vào pipeline chính.

## 3. Bộ Câu Hỏi Khơi Gợi Phản Biện (Elicitation Questionnaires)

### Question 1: Cơ chế Rollback — Hành vi khi stage N phát hiện lỗi?
- [x] **A (Khuyến nghị)**: Tự động gửi error signal về stage gây lỗi kèm error context (stage, artifact, line, reason). Stage nhận error tự động re-run hoặc patch. Pipeline BLOCKED cho đến khi resolved.
- [ ] **B**: Log lỗi vào file, dừng pipeline, chờ human manual fix.
- **Tag trace**: `[CẦN LÀM RÕ]`

### Question 2: Global Context — LLM cần thấy gì khi vận hành?
- [x] **A (Khuyến nghị)**: Tạo `pipeline-state.yaml` — file real-time chứa: current stage, completed stages, artifacts produced, blockers, next stage. Load mandatory ở boot sequence mọi skill.
- [ ] **B**: Chỉ cần mỗi skill biết input/output contract của nó, không cần biết tổng thể.
- **Tag trace**: `[CẦN LÀM RÕ]`

### Question 3: Auto-Registration — Khi thêm skill mới?
- [x] **A (Khuyến nghị)**: Tạo `suite_config.yaml` (theo JSON Schema đã design) — khai báo tất cả skills, stage map, dependencies. Script `validate_suite_integrity.py` đọc từ config này, không hardcode.
- [ ] **B**: Giữ nguyên validate_suite_integrity.py hardcode 11 skills, update thủ công mỗi lần thêm.
- **Tag trace**: `[CẦN LÀM RÕ]`

## 4. Phân Rã Luồng Xử Lý Sơ Bộ (3-Path Decomposition)

### Happy Path
1. Suite config centralized (`suite_config.yaml`) — single source of truth
2. Mọi skill khi boot đều load pipeline-state.yaml → biết context tổng thể
3. Stage N output được validate schema trước khi handoff sang Stage N+1
4. Khi Stage N+1 phát hiện lỗi → gửi error signal → Stage N tự động patch
5. Thêm skill mới → chỉ cần update suite_config.yaml + chạy auto-register

### Alternative Path
1. Suite config tồn tại nhưng chưa đầy đủ (thiếu vài skill)
2. Validator warning nhưng vẫn cho sync runtime
3. Pipeline chạy với cảnh báo — skill missing bị skip

### Exception Path
1. Stage numbering mismatch bị validator chặn cứng
2. Rollback protocol kích hoạt — pipeline-state.yaml revert về checkpoint an toàn
3. Error notification + build-log.md cập nhật chi tiết

## 5. Đánh Giá Tác Động Ban Đầu (Initial Impact Assessment)

| Hạng mục | Tác động | Mức độ |
|----------|----------|--------|
| raw/ver-3/ toàn bộ 11 skills | Thay đổi cấu trúc SKILL.md để load pipeline-state.yaml | Cao |
| _shared/knowledge/framework.md | Thêm rollback protocol + error signal contract | Trung bình |
| validate_suite_integrity.py | Viết lại toàn bộ — đọc từ suite_config.yaml | Cao |
| BA skills (3 skills) | Thêm 7-Zones + trace tags + YAML frontmatter | Thấp |
| format-standards.md | Xóa 3 local copies, fix refs | Thấp |
| Stage numbering | Sửa skill-planner→3, skill-builder→4 | Thấp |

## 6. Kết Quả Tự Kiểm Định Chất Lượng (Self-Verification Checklist)

- [x] QC-01: Input đã bọc trong XML boundary — ✅
- [x] QC-02: Loại bỏ cảm tính — ✅ (100% issues là kỹ thuật, đã lượng hóa)
- [x] QC-03: Trace tags — ✅ (gắn `[TỪ INPUT]`, `[SUY LUẬN]`, `[CẦN LÀM RÕ]`)
- [x] QC-04: Phân rã 3-Paths — ✅ (Happy/Alternative/Exception)
- [x] QC-05: 5W1H — ✅ (3 câu hỏi khơi gợi multiple-choice)
- [x] QC-06: Zero Placeholder — ✅ (không TODO/pass/mock)
- [x] QC-07: Độ tin cậy — ✅ (confidence 92% > 60%, ready_for_analyst)
