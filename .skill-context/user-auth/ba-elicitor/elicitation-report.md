---
skill_name: "user-auth"
domain_ontology:
  terms:
    - term: "User"
      definition: "End consumer của web/mobile client; chủ sở hữu Account. [TỪ INPUT]"
    - term: "Account"
      definition: "Bản ghi người dùng lưu email + password_hash + trạng thái MFA. [TỪ INPUT]"
    - term: "Credential (email/password)"
      definition: "Phương thức xác thực sơ cấp: email + password băm. [TỪ INPUT]"
    - term: "Google OAuth"
      definition: "Đăng nhập liên kết (federated) qua Google identity provider. [TỪ INPUT]"
    - term: "MFA / TOTP"
      definition: "Xác thực đa yếu tố dùng mã one-time theo thời gian; ưu tiên P1. [TỪ INPUT]"
    - term: "Access Token"
      definition: "Token ngắn hạn (TTL 15 phút) cấp quyền truy cập API. [TỪ INPUT]"
    - term: "Refresh Token"
      definition: "Token dài hạn (TTL 7 ngày) cấp phát access token mới. [TỪ INPUT]"
    - term: "Session"
      definition: "Liên kết logic giữa User và cặp token đang hoạt động. [SUY LUẬN]"
    - term: "Password Reset Token"
      definition: "Token trong link email đặt lại mật khẩu; hết hạn sau 1 giờ. [TỪ INPUT]"
    - term: "Lockout"
      definition: "Khóa tạm thời tài khoản sau 5 lần thất bại (15 phút). [TỪ INPUT]"
    - term: "Client"
      definition: "Ứng dụng web hoặc mobile gọi Auth API. [TỪ INPUT]"
    - term: "Auth Server"
      definition: "Backend phát hành và xác thực token. [SUY LUẬN]"
  relationships:
    - source: "User"
      target: "Account"
      type: "owns"
    - source: "Account"
      target: "Credential"
      type: "has"
    - source: "User"
      target: "GoogleOAuth"
      type: "authenticates_via"
    - source: "User"
      target: "MFA/TOTP"
      type: "enables"
    - source: "Account"
      target: "AccessToken"
      type: "issues"
    - source: "Account"
      target: "RefreshToken"
      type: "issues"
    - source: "Session"
      target: "RefreshToken"
      type: "references"
    - source: "Account"
      target: "PasswordResetToken"
      type: "generates"
    - source: "Client"
      target: "AuthServer"
      type: "calls"
stakeholder_analysis:
  - role: "End-User (Consumer)"
    goals:
      - "Đăng nhập nhanh, mượt trên web và mobile. [TỪ INPUT]"
      - "Bảo mật tài khoản khỏi bị chiếm đoạt. [SUY LUẬN]"
    pain_points:
      - "MFA TOTP thêm bước friction mỗi login. [SUY LUẬN]"
      - "Bị lockout 15 phút sau 5 lần sai gây gián đoạn. [TỪ INPUT]"
  - role: "Security Reviewer"
    goals:
      - "Ngăn account takeover qua token leak / reset yếu. [SUY LUẬN]"
      - "Đảm bảo TTL token tuân thủ least-privilege. [TỪ INPUT]"
    pain_points:
      - "Refresh token dài hạn (7 ngày) là bề mặt tấn công nếu không rotate. [SUY LUẬN]"
      - "Reset link qua email dễ bị intercept nếu không single-use. [SUY LUẬN]"
  - role: "System Operator (DevOps)"
    goals:
      - "Duy trì uptime Auth Server, quan sát rate-limit. [SUY LUẬN]"
    pain_points:
      - "Revoke token hàng loạt khi nghi ngờ breach. [SUY LUẬN]"
  - role: "Developer / Maintainer"
    goals:
      - "API auth nhất quán cho cả web và mobile client. [TỪ INPUT]"
    pain_points:
      - "Xử lý refresh khác biệt giữa SPA (web) và native (mobile). [CẦN LÀM RÕ]"
nrfs:
  - id: "perf-1"
    category: "performance"
    metric: "auth_latency_p95"
    value: 2000
    unit: "ms"
  - id: "sec-1"
    category: "security"
    metric: "access_token_ttl"
    value: 15
    unit: "minute"
  - id: "sec-2"
    category: "security"
    metric: "refresh_token_ttl"
    value: 7
    unit: "day"
  - id: "sec-3"
    category: "security"
    metric: "password_reset_ttl"
    value: 1
    unit: "hour"
  - id: "sec-4"
    category: "security"
    metric: "lockout_threshold"
    value: 5
    unit: "attempt"
  - id: "sec-5"
    category: "security"
    metric: "lockout_duration"
    value: 15
    unit: "minute"
thought_cache:
  business_thought_process:
    - "Systems Thinking: Auth là ranh giới tin cậy cốt lõi của toàn bộ app; mọi downstream API phụ thuộc vào token hợp lệ. Feedback loop: failed attempts → lockout → giảm brute force nhưng tăng friction UX. [SUY LUẬN]"
    - "Root Cause Isolation: Rủi ro chiếm đoạt tài khoản thường xuất phát từ (1) reset flow yếu, (2) refresh token không rotate, (3) thiếu MFA. Không giải quyết triệu chứng mà giải quyết gốc: enforce MFA P1 + single-use reset + rotate refresh. [SUY LUẬN]"
    - "First Principles: Token phải stateless (JWT) hoặc stateful (opaque + store) — chọn dựa trên nhu cầu revoke tức thời. Refresh 7 ngày bắt buộc có rotation + revocation list để giới hạn blast radius. [SUY LUẬN]"
    - "Impact Analysis: Đổi TTL access token (15min) không ảnh hưởng DB load nhiều; đổi refresh rotation ảnh hưởng schema Session + logout-all logic. [SUY LUẬN]"
    - "Structural Decomposition: Epic 'Secure Login' → Features (email/pwd, OAuth, MFA, session, reset, rate-limit) → User Stories → Acceptance Criteria (Gherkin). [SUY LUẬN]"
  stakeholder_empathy:
    - "End-User: muốn login < 2s, không bị lockout oan; MFA chấp nhận nếu chỉ bắt khi device lạ. [SUY LUẬN]"
    - "Security Reviewer: cần refresh rotate + reset single-use + rate-limit đủ chặt. [SUY LUẬN]"
    - "System Operator: cần metric rate-limit hit + token revoke API. [SUY LUẬN]"
    - "Developer: cần contract API đồng nhất web/mobile, tài liệu rõ ràng. [SUY LUẬN]"
  reverse_questions:
    - "Nếu refresh token bị leak, hệ thống revoke thế nào trước khi 7 ngày hết hạn? [SUY LUẬN]"
    - "Reset link có single-use và bind vào user session không? Nếu intercept thì sao? [SUY LUẬN]"
    - "Rate-limit 5 attempts áp dụng per-IP hay per-account? Brute force qua nhiều IP? [CẦN LÀM RÕ]"
    - "MFA TOTP bắt buộc cho mọi login hay chỉ device chưa trust? [CẦN LÀM RÕ]"
    - "OAuth fallback khi Google outage? [CẦN LÀM RÕ]"
---

> **Status:** `completed` (ready_for_analyst) — confidence_score: 85 (0-100).
> **Trace tags:** `[TỪ INPUT]` (từ user) · `[SUY LUẬN]` (agent suy luận) · `[CẦN LÀM RÕ]` (thiếu/mơ hồ).

## 1. Yêu Cầu Đã Chuẩn Hóa (Normalized Input)

- **Mục tiêu cốt lõi**: Hệ thống auth cho web/mobile app, bảo mật tài khoản người dùng cuối. `[TỪ INPUT]`
- **Môi trường vận hành**: Web app + Mobile app (native), backend Auth Server. `[TỪ INPUT]`
- **Tác nhân chính**: End consumer (User) — login/reset qua Client. `[TỪ INPUT]`
- **Yêu cầu chức năng sơ khởi (FRs)**:
  - FR-1: Email/password login + phát token. `[TỪ INPUT]`
  - FR-2: Google OAuth login. `[TỪ INPUT]`
  - FR-3: MFA TOTP (P1). `[TỪ INPUT]`
  - FR-4: Session / refresh token (access 15m, refresh 7d). `[TỪ INPUT]`
  - FR-5: Password reset (email link, 1h). `[TỪ INPUT]`
  - FR-6: Rate-limit 5 fails → lockout 15m. `[TỪ INPUT]`

## 2. Ontology Nghiệp Vụ (Domain Ontology)

Xem frontmatter `domain_ontology` (12 terms, 9 relationships). `[TỪ INPUT]` / `[SUY LUẬN]`

## 3. Phân Tích Khoảng Trống (Gap Analysis — 6 Mindset Keywords)

- **Systems Thinking**: Auth là trust boundary duy nhất; mọi API phụ thuộc. `[SUY LUẬN]`
- **Root Cause Isolation**: Gốc rủi ro = reset yếu + refresh không rotate + thiếu MFA. `[SUY LUẬN]`
- **MECE**: 6 feature con (login/pwd, OAuth, MFA, session, reset, rate-limit) bao phủ đủ; thiếu logout-all/revoke rõ ràng. `[SUY LUẬN]`
- **First Principles**: Refresh 7d cần rotation + revocation bắt buộc. `[SUY LUẬN]`
- **Impact Analysis**: Đổi TTL access không ảnh hưởng nhiều; đổi rotation ảnh hưởng schema Session. `[SUY LUẬN]`
- **Structural Decomposition**: Epic → 6 Features → User Story → Gherkin. `[SUY LUẬN]`

## 4. Stakeholder Analysis (≥2 góc độ)

Xem frontmatter `stakeholder_analysis` (End-User, Security Reviewer, System Operator, Developer). `[TỪ INPUT]` / `[SUY LUẬN]`

## 5. NFRs Đã Lượng Hóa (SMART — ISO/IEC 25010)

Xem frontmatter `nrfs` (perf-1 latency 2000ms; sec-1..5 TTL/lockout). `[TỪ INPUT]` / `[SUY LUẬN]`
- `[CẦN LÀM RÕ]` perf-1 SLA chính xác chưa confirm (giả định 2000ms).

## 6. Bộ Câu Hỏi Khơi Gợi (5W1H — Multiple-choice)

### Who / What
- **Câu hỏi 1**: MFA TOTP bắt buộc cho mọi login hay chỉ device chưa trust?
  - [ ] A: Mọi login (strict) `[CẦN LÀM RÕ]`
  - [ ] B: Chỉ device chưa trust (adaptive) `[CẦN LÀM RÕ]`
  - [ ] C: Tùy user enable `[CẦN LÀM RÕ]`

### How / When
- **Câu hỏi 2**: Rate-limit 5 attempts áp dụng per-account hay per-IP?
  - [ ] A: per-account `[CẦN LÀM RÕ]`
  - [ ] B: per-IP `[CẦN LÀM RÕ]`
  - [ ] C: cả hai `[CẦN LÀM RÕ]`

## 7. Phân Rã 3-Path (Happy / Alternative / Exception)

- **Happy Path**: User nhập email/pwd đúng → verify → phát access+refresh → login thành công. `[SUY LUẬN]`
- **Alternative Path**: User chọn Google OAuth → redirect → verify id_token → link/create account → phát token. `[SUY LUẬN]`
- **Exception Path**: 5 lần sai → lockout 15 phút; hoặc reset link hết hạn → từ chối. `[TỪ INPUT]`

## 8. Tự Kiểm Định (Self-Verification)

- [x] XML boundary `<user_skill_request>`: N/A (inline context, không có injection).
- [x] Số `[CẦN LÀM RÕ]`: 5 (perf SLA, MFA scope, rate-limit scope, OAuth fallback, web/mobile refresh).
- [x] Số `[TỪ INPUT]`: nhiều (FRs, TTL, lockout).
- [x] Số `[SUY LUẬN]`: nhiều (ontology, gaps, paths).
- [x] Confidence ≥ 60%: 85 — PASS.
