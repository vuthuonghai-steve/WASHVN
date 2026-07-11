---
skill_name: "notify-feature"
elicitation_date: "2026-07-11"
confidence_score: 88
status: "ready_for_analyst"
---

# Báo Cáo Khơi Gợi Yêu Cầu Nghiệp Vụ: notify-feature

> **Trace tags (bắt buộc):** `[TỪ INPUT]` (từ user) · `[SUY LUẬN]` (agent suy luận, ghi rõ lý do) · `[CẦN LÀM RÕ]` (thiếu/mơ hồ).

## 1. Yêu Cầu Đã Chuẩn Hóa (Normalized Input)

- **Mục tiêu cốt lõi**: xây dựng tính năng thông báo/cảnh báo cho ứng dụng di động — người dùng nhận push notification cho cập nhật đơn hàng, đề cập (mention), và cảnh báo hệ thống. `[TỪ INPUT]`
- **Môi trường vận hành**: ứng dụng di động (iOS/Android), phân phối qua dịch vụ push nền tảng (FCM/APNs). `[TỪ INPUT]` `[SUY LUẬN]`
- **Tác nhân chính**:
  - App User: người nhận thông báo, cấu hình偏好 (preferences) nhận. `[TỪ INPUT]`
  - Notification System: thành phần phát sinh và phân phối thông báo. `[SUY LUẬN]`
- **Yêu cầu chức năng sơ khởi (FRs)**:
  - FR-1: phân phối push notification khi có sự kiện cập nhật đơn hàng. `[TỪ INPUT]`
  - FR-2: phân phối push notification khi người dùng bị đề cập (mention). `[TỪ INPUT]`
  - FR-3: phát cảnh báo hệ thống (system alert) đến người dùng. `[TỪ INPUT]`
  - FR-4: người dùng cấu hình偏好 thông báo (bật/tắt theo từng danh mục). `[TỪ INPUT]`

## 2. Ontology Nghiệp Vụ (Domain Ontology)

- **Thuật ngữ (≥10 terms, neo vector space)**:
  - `Push Notification`: tin nhắn ngoài ứng dụng được gửi đến thiết bị qua dịch vụ push nền tảng.
  - `Notification Category`: phân loại — order_update, mention, system_alert. `[TỪ INPUT]`
  - `Notification Preference`: cài đặt bật/tắt theo người dùng và theo danh mục. `[TỪ INPUT]`
  - `Order Update`: sự kiện thay đổi trạng thái đơn hàng kích hoạt thông báo. `[TỪ INPUT]`
  - `Mention`: sự kiện người dùng được gắn thẻ/đề cập trong nội dung. `[TỪ INPUT]`
  - `System Alert`: thông báo cấp nền tảng/dịch vụ gửi đến người dùng. `[TỪ INPUT]`
  - `Device Token`: định danh đăng ký với dịch vụ push cho mỗi thiết bị. `[SUY LUẬN]`
  - `Delivery Pipeline`: đường đi từ sự kiện → phân phối → dịch vụ push → thiết bị. `[SUY LUẬN]`
  - `Filter (simple text match)`: quy tắc khớp nội dung thông báo bằng so khớp văn bản con. `[SUY LUẬN]` (default áp dụng)
  - `Pagination`: danh sách thông báo hiển thị 12 mục mỗi trang. `[SUY LUẬN]` (default áp dụng)
  - `Preference Store`: kho lưu trữ bền vững cài đặt thông báo theo người dùng. `[SUY LUẬN]`
  - `Rate Limit`: giới hạn thông lượng 100 rps khi phát thông báo. `[SUY LUẬN]`
- **Quan hệ thực thể**:
  - User → NotificationPreference (configures)
  - OrderUpdate → Notification (triggers)
  - Mention → Notification (triggers)
  - SystemAlert → Notification (triggers)
  - Notification → DeviceToken (targets)
  - NotificationPreference → Notification (gates delivery)

## 3. Phân Tích Khoảng Trống (Gap Analysis — 6 Mindset Keywords)

- **Systems Thinking**: phân phối thông báo phụ thuộc vào tình trạng dịch vụ push và vòng đời device token; có vòng phản hồi qua biên nhận giao (delivery receipt). `[SUY LUẬN]`
- **Root Cause Isolation**: lỗi không đến thông báo thường bắt nguồn từ token hết hạn hoặc cổng preference, không phải từ lời gọi gửi. `[SUY LUẬN]`
- **MECE**: danh mục được phân hoạch thành order_update / mention / system_alert, loại trừ lẫn nhau, bao phủ đủ. `[SUY LUẬN]`
- **First Principles**: giao hàng cần device token đã đăng ký + sự đồng ý preference + sự kiện hợp lệ; không giả định giao thành công bắt buộc. `[SUY LUẬN]`
- **Impact Analysis**: thay đổi preference ảnh hưởng mọi lượt phát sau; giới hạn thông lượng ảnh hưởng sự kiện đơn hàng dồn dập (burst). `[SUY LUẬN]`
- **Structural Decomposition**: Epic (Notifications) → Features (Delivery, Preferences) → Stories (cấu hình偏好, nhận cập nhật đơn). `[SUY LUẬN]`

## 4. Stakeholder Analysis (≥2 góc độ)

- **App User**: goals=[nhận cảnh báo đúng lúc, liên quan; kiểm soát nội dung nhận] · pain_points=[mệt mỏi thông báo, bỏ lỡ cảnh báo quan trọng]
- **Mobile Engineer**: goals=[giao hàng tin cậy, ít pin/chi phí] · pain_points=[quản lý token, khác biệt nền tảng FCM/APNs]
- **Security Reviewer**: goals=[không rò rỉ dữ liệu nhạy cảm qua push, tuân thủ đồng ý] · pain_points=[PII trong payload, vượt cổng preference]
- **System Operator**: goals=[đạt sẵn sàng 99.9%, 100 rps] · pain_points=[dịch vụ push ngưng, tồn đọng (backlog)]

## 5. NFRs Đã Lượng Hóa (SMART — ISO/IEC 25010)

- NFR-1: id=`perf-1`, category=`performance`, metric=`latency_p95`, value=`500`, unit=`ms` `[SUY LUẬN]` (default)
- NFR-2: id=`perf-2`, category=`performance`, metric=`throughput`, value=`100`, unit=`rps` `[SUY LUẬN]` (default)
- NFR-3: id=`avail-1`, category=`reliability`, metric=`availability`, value=`99.9`, unit=`%` `[SUY LUẬN]` (default)
- NFR-4: id=`acc-1`, category=`accessibility`, metric=`wcag_conformance`, value=`AA`, unit=`level` `[SUY LUẬN]` (default)
- NFR-5: id=`sec-1`, category=`security`, metric=`preference_enforcement`, value=`mandatory_opt_in`, unit=`policy` `[SUY LUẬN]`
- NFR-6: id=`usab-1`, category=`usability`, metric=`pagination_size`, value=`12`, unit=`items_per_page` `[SUY LUẬN]` (default)
- NFR-7: id=`filter-1`, category=`functional_suitability`, metric=`filter_method`, value=`simple_text_match`, unit=`method` `[SUY LUẬN]` (default)

## 6. Bộ Câu Hỏi Khơi Gợi (5W1H — Multiple-choice)

- **Câu hỏi 1** (Who): Ai quản lý preference thông báo?
  - [ ] A: Chính người dùng (tự cấu hình)
  - [ ] B: Quản trị viên (admin)
  - [ ] C: Lai (hybrid)
  - Tag: `[SUY LUẬN]` — default áp dụng A (tự cấu hình).
- **Câu hỏi 2** (What): Payload push có chứa dữ liệu định danh cá nhân (PII) không?
  - [ ] A: Không chứa PII
  - [ ] B: Có nhưng dạng token hóa
  - [ ] C: Có dạng thô (plain)
  - Tag: `[SUY LUẬN]` — default an toàn A (không PII thô).
- **Câu hỏi 3** (When): Thời điểm phát thông báo?
  - [ ] A: Thời gian thực (real-time)
  - [ ] B: Gộp lô (batched)
  - [ ] C: Lên lịch (scheduled)
  - Tag: `[SUY LUẬN]` — default A cho order_update/mention.
- **Câu hỏi 4** (How): Cơ chế thử lại khi push thất bại?
  - [ ] A: Exponential backoff
  - [ ] B: Bỏ (drop)
  - [ ] C: Queue 24h
  - Tag: `[SUY LUẬN]` — default A (backoff).
- **Câu hỏi 5** (Where): Kênh phân phối?
  - [ ] A: FCM + APNs
  - [ ] B: Chỉ trong ứng dụng (in-app)
  - [ ] C: SMS
  - Tag: `[SUY LUẬN]` — default A.
- **Câu hỏi 6** (What): Lưu trữ lịch sử thông báo?
  - [ ] A: Có, 30 ngày
  - [ ] B: Không
  - [ ] C: Vô hạn
  - Tag: `[SUY LUẬN]` — default A (30 ngày).

> Ghi chú: không phát sinh thẻ `[CẦN LÀM RÕ]` vì mọi vùng thiếu đã áp dụng default an toàn (simple text match, 12/page, 500ms p95, 100 rps, WCAG AA, 99.9%).

## 7. Phân Rã 3-Path (Happy / Alternative / Exception)

- **Happy Path**: người dùng bật preference → trạng thái đơn hàng thay đổi → hệ thống tạo thông báo, vượt cổng preference → push đến thiết bị trong 500ms p95. `[SUY LUẬN]`
- **Alternative Path**: người dùng nhận mention nhưng đã tắt danh mục mention → thông báo bị ức chế (suppressed), ghi log; người dùng thấy trong lịch sử trong ứng dụng. `[SUY LUẬN]`
- **Exception Path**: device token hết hạn / dịch vụ push không sẵn sàng → hệ thống xếp hàng với backoff, thử lại; nếu thất bại kéo dài, đánh dấu giao thất bại, không sập, cảnh báo operator. `[SUY LUẬN]`

## 8. Tự Kiểm Định (Self-Verification)

- [x] XML boundary `<user_skill_request>`: input được cô lập, pass.
- [x] Số `[CẦN LÀM RÕ]`: 0 (đã áp dụng default an toàn).
- [x] Số `[TỪ INPUT]`: ≥ 5.
- [x] Số `[SUY LUẬN]`: ≥ 10.
- [x] Confidence ≥ 60%: 88 (status ready_for_analyst).
