---
skill_name: "mock-notify-feature"
synthesized_requirements:
  - req_id: "FR-01"
    title: "Phân phối push notification khi có sự kiện order_update"
    description: "Hệ thống tạo và enqueue notification qua FCM/APNs khi trạng thái đơn hàng thay đổi, chỉ khi preference danh mục order_update được opt-in."
    source: "both"
    classification: "FR"
  - req_id: "FR-02"
    title: "Phân phối push notification khi người dùng bị mention"
    description: "Khi sự kiện mention xảy ra, hệ thống gửi push cho người dùng được gắn thẻ, vượt cổng preference danh mục mention; nếu tắt thì đánh dấu suppressed."
    source: "both"
    classification: "FR"
  - req_id: "FR-03"
    title: "Phát cảnh báo hệ thống (system_alert)"
    description: "Hệ thống phát system_alert đến người dùng theo danh mục system_alert, tuân thủ preference gate."
    source: "both"
    classification: "FR"
  - req_id: "FR-04"
    title: "Cấu hình preference thông báo theo danh mục"
    description: "Người dùng tự cấu hình bật/tắt preference theo 3 danh mục (order_update, mention, system_alert). Preference Store lưu trạng thái bền vững, deny-by-default."
    source: "both"
    classification: "FR"
  - req_id: "NFR-01"
    title: "Latency p95 ≤ 500ms"
    description: "Luồng tạo và enqueue notification đạt p95 ≤ 500ms đo từ create đến enqueue."
    source: "both"
    classification: "NFR"
  - req_id: "NFR-02"
    title: "Throughput ≤ 100 rps"
    description: "Duy trì thông lượng tối đa 100 request/giây dưới tải đỉnh (burst) bằng token bucket + backpressure."
    source: "both"
    classification: "NFR"
  - req_id: "NFR-03"
    title: "Availability ≥ 99.9%"
    description: "Dịch vụ thông báo đạt ≥ 99.9% uptime hàng tháng."
    source: "both"
    classification: "NFR"
  - req_id: "NFR-04"
    title: "Tuân thủ WCAG AA"
    description: "Giao diện cấu hình preference và lịch sử thông báo tuân thủ WCAG AA."
    source: "both"
    classification: "NFR"
  - req_id: "NFR-05"
    title: "Ép buộc opt-in (mandatory opt-in)"
    description: "Thông báo chỉ gửi khi preference cho phép; deny-by-default tại Delivery Pipeline, chặn gửi trái phép."
    source: "both"
    classification: "NFR"
  - req_id: "NFR-06"
    title: "Phân trang danh sách 12 mục/mỗi trang"
    description: "Danh sách thông báo/lịch sử phân trang 12 items_per_page."
    source: "both"
    classification: "NFR"
  - req_id: "NFR-07"
    title: "Bộ lọc simple_text_match"
    description: "Lọc thông báo dùng simple text match trên nội dung (default, nâng cấp sau)."
    source: "both"
    classification: "NFR"
congruence_check:
  conflicts_found: 0
  conflicts_resolved: 0
  check_verdict: "PASS"
pipeline_ready: true
---

# Business Analysis — mock-notify-feature

## Executive Summary

Tính năng notification/push cho ứng dụng di động (iOS/Android) qua FCM/APNs. 4 FR + 7 NFR đã được khơi gợi và phân tích đồng thuận. Phân phối 3 danh mục (order_update, mention, system_alert) qua preference gate deny-by-default. Lịch sử 30 ngày, backoff retry, DLQ khi provider lỗi. 6 rủi ro đã có mitigation gắn P0. Input elicitation + analysis hoàn toàn khớp nhau (zero conflict).

## Consolidated Requirements

**Handoff metadata (template-level, không thuộc frontmatter):**
- `target_skill`: skill-explorer (Phase 6)
- `scs_complexity_score`: 0.58 (Medium — 11 reqs, 5 actors, 4 entities, 6 risks)
- `quality_gate_status`: PASS
- `quality_score_percentage`: 100

Consolidated 11 requirements (FR-01..04, NFR-01..07) — xem frontmatter `synthesized_requirements`. Deduplicate: elicitation FR-1..4 ≡ analysis FR-01..04; NFR-1..7 ≡ NFR-01..07. Không phát sinh requirement mới, không mâu thuẫn.

## Acceptance Criteria

Dựa trên 3 Gherkin scenarios (analysis §4) — bao phủ toàn bộ Must-Have:
- AC-1 (Happy): opt-in order_update + token hợp lệ → tạo + enqueue ≤ 500ms p95, push thành công, status "sent".
- AC-2 (Alternative): tắt preference mention → status "suppressed", log, hiển thị lịch sử in-app.
- AC-3 (Exception): token hết hạn/provider lỗi → receipt failed, backoff, DLQ + alert, core flow không sập, status "failed".
- AC-4 (NFR): throughput ≤ 100 rps (burst token bucket); availability ≥ 99.9%; WCAG AA; pagination 12/page; filter simple_text_match; mandatory opt-in deny-by-default.

## Traceability

- `[TỪ INPUT]` FR-01..04, 3 danh mục, FCM+APNs, 30-day history, backoff, self-config preference.
- `[SUY LUẬN]` NFR defaults (500ms, 100rps, 99.9%, WCAG AA, 12/page, simple_text_match, mandatory opt-in), ERD (APP_USER/DEVICE_TOKEN/NOTIFICATION_PREFERENCE/NOTIFICATION), 6 risks.
- `[CẦN LÀM RÕ]` 0 — mọi khoảng trống áp default an toàn.
- Actor↔Entity: App User→APP_USER, Preference Store→NOTIFICATION_PREFERENCE, Notification System→NOTIFICATION, Push Provider→DEVICE_TOKEN. Consistent.
- MoSCoW P0 Must (FR-01..04, NFR-01,02,03,05) ↔ 3 Gherkin scenarios present. Covered.
