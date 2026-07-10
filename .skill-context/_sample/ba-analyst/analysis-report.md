---
skill_name: "ba-analyst"
criteria_analysis:
  - criterion_id: "FR-01"
    description: "Người dùng đăng nhập bằng email và password hợp lệ."
    classification: "FR"
  - criterion_id: "FR-02"
    description: "Người dùng đăng nhập bằng Google OAuth."
    classification: "FR"
  - criterion_id: "NFR-01"
    description: "Thời gian xác thực đăng nhập phải dưới ngưỡng người dùng chấp nhận."
    classification: "NFR"
  - criterion_id: "NFR-02"
    description: "Hệ thống phải sẵn sàng phục vụ liên tục."
    classification: "NFR"
metrics:
  - name: "Latency p95"
    value: 2000
    unit: "ms"
  - name: "Availability"
    value: 99.9
    unit: "%"
  - name: "Concurrent Users"
    value: 5000
    unit: "users"
risk_assessment:
  - risk_id: "RR-01"
    edge_case: "Secret (JWT signing key) hardcode trong source → rò rỉ khi repo public."
    mitigation: "Lưu secret trong AWS Secrets Manager / ENV, xoay key định kỳ 30 ngày."
  - risk_id: "RR-02"
    edge_case: "DB không khả dụng khi user đăng nhập → auth không query được."
    mitigation: "Primary-replica failover + circuit breaker, trả 503 kèm retry-after."
  - risk_id: "RR-03"
    edge_case: "Brute-force password do không giới hạn thử."
    mitigation: "Rate limit 5 lần/phút/IP + khóa 15 phút sau 3 lần sai."
---

> [!NOTE]
> **Artifact Metadata (không thuộc frontmatter schema).**
> analyzed_by: "ba-analyst"
> analyzed_at: "2026-07-11T14:30:00Z"
> status: "completed"
> schema_ref: "skills/ver-3/_shared/schemas/analysis.schema.yaml"
> artifact_lifecycle: "WORM"
> validated_by: "schema_validator.py"
> trace_tags: ["TỪ INPUT", "SUY LUẬN", "CẦN LÀM RÕ"]

# Báo Cáo Phân Tích — Tính năng Đăng nhập

## §1: Classification & MoSCoW Matrix

| ID | Yêu cầu | Loại | MoSCoW | Giải thích kỹ thuật |
|:---|:--------|:----:|:------:|:-------------------|
| FR-01 | Đăng nhập email/password | FR | P0 — Must | Core auth, thiếu không vận hành được |
| FR-02 | Đăng nhập Google OAuth | FR | P1 — Should | Tăng UX, có workaround |
| NFR-01 | Latency đăng nhập ≤ 2s | NFR | P0 — Must | Giữ chân user |
| NFR-02 | Availability ≥ 99.9% | NFR | P0 — Must | SLA vận hành |

## §2: System Diagrams

### Sequence

```mermaid
sequenceDiagram
    autonumber
    actor User as "Người dùng (Client)"
    participant Gateway as "API Gateway"
    participant Auth as "Auth Service"
    participant DB as "Cơ sở dữ liệu"
    User->>Gateway: "POST /login (email, password)"
    Gateway->>Auth: "Xác thực thông tin"
    Auth->>DB: "Truy vấn tài khoản"
    DB-->>Auth: "Thông tin hợp lệ"
    Auth-->>Gateway: "JWT token"
    Gateway-->>User: "200 + token"
```

### Flowchart

```mermaid
flowchart TD
    Start["Nhận request login"] --> Valid{"Thông tin hợp lệ?"}
    Valid -- "Hợp lệ (Happy)" --> Issue["Cấp JWT token"]
    Valid -- "Sai (Alt)" --> Retry["Khóa 15p sau 3 lần sai"]
    Valid -- "Lỗi hệ thống (Exception)" --> Error["503 + retry-after"]
```

### ERD

```mermaid
erDiagram
    USER ||--o{ SESSION : "has"
    USER {
        integer id PK
        string email
        string password_hash
        timestamp created_at
    }
    SESSION {
        integer id PK
        integer user_id FK
        string token
        timestamp expires_at
    }
```

## §3: Data Schema Design

| Tên trường | Kiểu | Ràng buộc | Mô tả |
|:---|:---|:---|:---|
| `id` | `integer` | `PK, AUTO_INCREMENT` | Khóa chính |
| `email` | `string` | `UNIQUE, NOT NULL` | Email đăng nhập |
| `password_hash` | `string` | `NOT NULL` | Bcrypt hash |
| `created_at` | `timestamp` | `NOT NULL` | Thời gian tạo |

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "UserSchema",
  "type": "object",
  "properties": {
    "id": { "type": "integer" },
    "email": { "type": "string", "format": "email" },
    "created_at": { "type": "string", "format": "date-time" }
  },
  "required": ["id", "email", "created_at"]
}
```

## §4: Gherkin Acceptance Criteria

**User Story:** As a user, I want to log in with email and password so that I can access my account securely.

```gherkin
Feature: User Authentication
  Scenario: Happy Path — Đăng nhập thành công
    Given user có tài khoản hợp lệ
    When user gửi email và password chính xác
    Then hệ thống trả về JWT token và status 200

  Scenario: Alternative Path — Đăng nhập Google OAuth
    Given user chọn đăng nhập Google
    When user xác thực thành công trên Google
    Then hệ thống tạo tài khoản/nối phiên và trả JWT token

  Scenario: Exception Path — Hệ thống lỗi DB
    Given database không khả dụng
    When user cố gắng đăng nhập
    Then hệ thống trả về lỗi 503 kèm header retry-after
```

## §5: Risk Assessment Matrix

| Mã RR | Mô tả rủi ro | Xác suất | Tác động | Giải pháp giảm thiểu |
|:---|:---|:---:|:---:|:---|
| RR-01 | Secret rò rỉ do hardcode | Trung bình | Cao | Secrets Manager / ENV, xoay key 30 ngày |
| RR-02 | DB down khi auth | Cao | Cao | Replica failover + circuit breaker |
| RR-03 | Brute-force password | Cao | Trung bình | Rate limit + khóa 15p |

## §6: Traceability Mapping

- **Yêu cầu phân loại**: [TỪ INPUT] ánh xạ từ elicitation-report (FR-01, FR-02).
- **Sơ đồ & logic**: [SUY LUẬN] ERD USER/SESSION suy từ luồng session.
- **Điểm chưa rõ**: [CẦN LÀM RÕ] chính sách expire token cụ thể chưa được Elicitor cung cấp.
