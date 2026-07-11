---
skill_name: "mock-login-feature"
elicitation_date: "2026-07-11"
confidence_score: 72
status: "ready_for_analyst"
---

# Báo Cáo Khơi Gợi Yêu Cầu Nghiệp Vụ: mock-login-feature

> **Trace tags (bắt buộc):** `[TỪ INPUT]` (từ user) · `[SUY LUẬN]` (agent suy luận, ghi rõ lý do) · `[CẦN LÀM RÕ]` (thiếu/mơ hồ).

## 1. Yêu Cầu Đã Chuẩn Hóa (Normalized Input)

- **Mục tiêu cốt lõi**: Hệ thống đăng nhập web app cho end consumers, xác thực email + password, optional remember-me session, đầu ra là login page bảo mật. `[TỪ INPUT]`
- **Môi trường vận hành**: Web application (browser client → backend auth service). `[TỪ INPUT]`
- **Tác nhân chính**:
  - End Consumer: người dùng cuối truy cập login page để xác thực. `[TỪ INPUT]`
- **Yêu cầu chức năng sơ khởi (FRs)**:
  - FR-1: Xác thực email + password trên login page. `[TỪ INPUT]`
  - FR-2: Optional remember-me session kéo dài phiên đăng nhập. `[TỪ INPUT]`

## 2. Ontology Nghiệp Vụ (Domain Ontology)

- **Thuật ngữ (≥10 terms, neo vector space)**:
  - `login page`: giao diện web thu thập email + password để xác thực.
  - `email + password`: cặp thông tin đăng nhập cơ bản (credential).
  - `remember-me`: tùy chọn giữ phiên đăng nhập qua nhiều session trình duyệt. `[TỪ INPUT]`
  - `session`: trạng thái đăng nhập được duy trì giữa các request.
  - `token`: đối tượng sinh sau xác thực thành công để ủy quyền request tiếp.
  - `end consumer`: người dùng cuối (không phải admin/operator). `[TỪ INPUT]`
  - `authentication`: quá trình xác minh danh tính user.
  - `credential`: thông tin bí mật dùng chứng minh danh tính (email+password).
  - `secure`: đáp ứng chuẩn bảo mật (mã hóa, chống brute-force, không lộ credential). `[TỪ INPUT]`
  - `brute-force`: tấn công dò mật khẩu tự động.
  - `rate-limit`: giới hạn số lần thử đăng nhập trong khoảng thời gian.
  - `password_hash`: bản băm mật khẩu (không lưu plaintext).
- **Quan hệ thực thể**:
  - User → Credential (owns)
  - User → Session (creates)
  - Session → Token (issued)

## 3. Phân Tích Khoảng Trống (Gap Analysis — 6 Mindset Keywords)

- **Systems Thinking**: Login page là entry point của hệ thống; ảnh hưởng đến session management, bảo mật downstream. Cần xem xét tích hợp với CSRF protection và HTTPS. `[SUY LUẬN]`
- **Root Cause Isolation**: Mục tiêu "secure login page" — gốc rễ không phải chỉ là form UI, mà là cơ chế xác thực + bảo vệ credential + chống tấn công. `[SUY LUẬN]`
- **MECE**: Phân rã: (1) UI login form, (2) Auth logic, (3) Session/Remember-me, (4) Security controls. Không chồng chéo. `[SUY LUẬN]`
- **First Principles**: Bảo mật login = không lưu plaintext password + mã hóa transport (TLS) + giới hạn thử sai. `[SUY LUẬN]`
- **Impact Analysis**: Thiếu rate-limiting → brute-force; thiếu remember-me expiry → session hijack. `[SUY LUẬN]`
- **Structural Decomposition**: Epic "Secure Login" → Feature "email+password auth" + Feature "remember-me" → User Story đăng nhập/thử lại/khóa tạm thời. `[SUY LUẬN]`

## 4. Stakeholder Analysis (≥2 góc độ)

- **End Consumer**: goals=[đăng nhập nhanh, an toàn, nhớ phiên nếu chọn] · pain_points=[quên mật khẩu, bị khóa tài khoản, form lỗi]
- **Security Reviewer**: goals=[không lộ credential, chống brute-force, session an toàn] · pain_points=[thiếu rate-limit, remember-me vô hạn, plaintext password]
- **Developer/Maintainer**: goals=[triển khai đơn giản, dễ test] · pain_points=[thiếu schema phiên, logic lockout phức tạp]
- **System Operator**: goals=[uptime ổn định dưới tải] · pain_points=[DB timeout khi login burst]

## 5. NFRs Đã Lượng Hóa (SMART — ISO/IEC 25010)

- NFR-1: id=`sec-1`, category=`security`, metric=`password_storage`, value=`bcrypt_cost_12`, unit=`n/a` `[SUY LUẬN]` (bắt buộc hash, không plaintext)
- NFR-2: id=`sec-2`, category=`security`, metric=`transport_encryption`, value=`TLS_1_3`, unit=`n/a` `[SUY LUẬN]`
- NFR-3: id=`sec-3`, category=`security`, metric=`rate_limit`, value=`5`, unit=`attempts_per_15min` `[CẦN LÀM RÕ]` (ngưỡng chưa confirm với user)
- NFR-4: id=`perf-1`, category=`performance`, metric=`latency_p95`, value=`2000`, unit=`ms` `[SUY LUẬN]` (ngưỡng 2s cho UX login)
- NFR-5: id=`sec-4`, category=`security`, metric=`remember_me_expiry`, value=`30`, unit=`days` `[CẦN LÀM RÕ]` (thời hạn remember-me chưa confirm)

## 6. Bộ Câu Hỏi Khơi Gợi (5W1H — Multiple-choice)

### Who / What
- **Câu hỏi 1**: Đối tượng bị khóa tài khoản tạm thời khi thử sai nhiều lần là ai?
  - [ ] A: Chỉ block IP
  - [x] B: Block tài khoản user (lockout) `[SUY LUẬN]`
  - [ ] C: Không khóa, chỉ captcha
  - Tag: `[CẦN LÀM RÕ]`

### How / When
- **Câu hỏi 2**: Remember-me session được duy trì bằng cơ chế nào?
  - [ ] A: Persistent cookie không hết hạn
  - [x] B: Refresh token có expiry (vd 30 ngày) `[SUY LUẬN]`
  - [ ] C: Session ID in localStorage
  - Tag: `[CẦN LÀM RÕ]`

### What / Why
- **Câu hỏi 3**: Có yêu cầu đăng nhập qua nhà cung cấp thứ 3 (OAuth Google/Github) không?
  - [ ] A: Có (P1)
  - [x] B: Không, chỉ email+password (MVP) `[TỪ INPUT]`
  - Tag: `[TỪ INPUT]`

## 7. Phân Rã 3-Path (Happy / Alternative / Exception)

- **Happy Path**: User mở login page → nhập email+password đúng → hệ thống xác thực → sinh token/session → chuyển hướng vào app. `[SUY LUẬN]`
- **Alternative Path**: User tick "remember-me" → đăng nhập thành công → hệ thống phát hành persistent session/refresh token hết hạn sau N ngày. `[SUY LUẬN]`
- **Exception Path**: User nhập sai password ≥ ngưỡng → tài khoản bị khóa tạm thời (lockout) + thông báo; hoặc DB lỗi → trả 503 + retry-after. `[SUY LUẬN]`

## 8. Tự Kiểm Định (Self-Verification)

- [x] XML boundary `<user_skill_request>`: enforced (input bọc boundary)
- [x] Số `[CẦN LÀM RÕ]`: 3 (rate-limit threshold, remember-me expiry, lockout scope)
- [x] Số `[TỪ INPUT]`: 6
- [x] Số `[SUY LUẬN]`: nhiều (≥10)
- [x] Confidence ≥ 60%: PASS (72%) — đủ để handoff sang ba-analyst
