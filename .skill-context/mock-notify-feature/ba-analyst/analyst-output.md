---
skill_name: "mock-notify-feature"
criteria_analysis:
  - criterion_id: "FR-01"
    description: "Phân phối push notification khi có sự kiện cập nhật đơn hàng (order_update)."
    classification: "FR"
  - criterion_id: "FR-02"
    description: "Phân phối push notification khi người dùng bị đề cập (mention)."
    classification: "FR"
  - criterion_id: "FR-03"
    description: "Phát cảnh báo hệ thống (system_alert) đến người dùng."
    classification: "FR"
  - criterion_id: "FR-04"
    description: "Người dùng cấu hình preference thông báo bật/tắt theo danh mục (order_update, mention, system_alert)."
    classification: "FR"
  - criterion_id: "NFR-01"
    description: "Latency p95 của luồng tạo và gửi thông báo ≤ 500ms."
    classification: "NFR"
  - criterion_id: "NFR-02"
    description: "Throughput duy trì tối đa 100 request/giây dưới tải đỉnh."
    classification: "NFR"
  - criterion_id: "NFR-03"
    description: "Availability dịch vụ thông báo ≥ 99.9% uptime hàng tháng."
    classification: "NFR"
  - criterion_id: "NFR-04"
    description: "Tuân thủ WCAG AA cho giao diện cấu hình preference và lịch sử."
    classification: "NFR"
  - criterion_id: "NFR-05"
    description: "Ép buộc opt-in: thông báo chỉ gửi khi preference cho phép (deny by default)."
    classification: "NFR"
  - criterion_id: "NFR-06"
    description: "Phân trang danh sách thông báo 12 mục mỗi trang."
    classification: "NFR"
  - criterion_id: "NFR-07"
    description: "Bộ lọc thông báo dùng simple text match trên nội dung."
    classification: "NFR"
metrics:
  - name: "Latency p95"
    value: 500
    unit: "ms"
  - name: "Throughput"
    value: 100
    unit: "rps"
  - name: "Availability"
    value: 99.9
    unit: "%"
  - name: "Pagination Size"
    value: 12
    unit: "items_per_page"
  - name: "History Retention"
    value: 30
    unit: "days"
  - name: "WCAG Conformance Level"
    value: 2
    unit: "level"
  - name: "Delivery Channels"
    value: 2
    unit: "count"
  - name: "Notification Categories"
    value: 3
    unit: "count"
risk_assessment:
  - risk_id: "RR-01"
    edge_case: "Device token hết hạn nhưng hệ thống vẫn cố gửi push → lỗi 4xx từ provider, lãng phí nỗ lực gửi, không sập hệ thống."
    mitigation: "Kiểm tra TTL token trước gửi; pruning token hết hạn định kỳ; feedback receipt loop cập nhật trạng thái token."
  - risk_id: "RR-02"
    edge_case: "Preference opt-in bị bỏ qua (gửi khi chưa đồng ý) → vi phạm bảo mật/luật, PII lọt ra ngoài."
    mitigation: "Preference gate bắt buộc tại Delivery Pipeline; deny-by-default; unit test chặn gửi khi preference off."
  - risk_id: "RR-03"
    edge_case: "Giới hạn 100 rps bị vượt trong giờ cao điểm (burst order_update) → thông báo rớt hoặc trễ p95."
    mitigation: "Token bucket + hàng đợi có backpressure; drop oldest non-critical khi queue đầy; cảnh báo operator."
  - risk_id: "RR-04"
    edge_case: "Dịch vụ push (FCM/APNs) ngưng hoàn toàn → gửi thất bại liên tục."
    mitigation: "Exponential backoff retry; Dead Letter Queue; alert operator; không sập core flow."
  - risk_id: "RR-05"
    edge_case: "Payload chứa PII thô → lộ trên lock screen thiết bị của bên thứ ba."
    mitigation: "Không đưa PII vào payload; chỉ gửi reference id; mã hóa at rest (AES-256); security review."
  - risk_id: "RR-06"
    edge_case: "Lịch sử 30 ngày tăng trưởng không kiểm soát → đầy storage, truy vấn chậm."
    mitigation: "TTL purge job xóa bản ghi > 30 ngày; phân trang 12/page; index trên (user_id, created_at)."
---

> [!NOTE]
> **Artifact Metadata (KHÔNG thuộc frontmatter schema-validated — schema dùng `additionalProperties: false`).**
> ```yaml
> analyzed_by: "ba-analyst"
> analyzed_at: "2026-07-11T14:30:00Z"
> status: "completed"
> schema_ref: "skills/ver-3/_shared/schemas/analysis.schema.yaml"
> artifact_lifecycle: "WORM"
> validated_by: "schema_validator.py + validate_metrics.py"
> ```

# Báo Cáo Phân Tích Kỹ Thuật — mock-notify-feature

## §1: Classification & MoSCoW Matrix

| ID | Yêu cầu | Loại | MoSCoW | Giải thích kỹ thuật |
|:---|:--------|:----:|:------:|:-------------------|
| FR-01 | Push khi order_update | FR | P0 — Must | Core delivery, thiếu thì tính năng vô nghĩa |
| FR-02 | Push khi mention | FR | P0 — Must | Core delivery, MECE với FR-01/03 |
| FR-03 | Phát system_alert | FR | P0 — Must | Cảnh báo bắt buộc cho người dùng |
| FR-04 | Cấu hình preference theo danh mục | FR | P0 — Must | Cổng kiểm soát gửi, deny-by-default |
| NFR-01 | Latency p95 ≤ 500ms | NFR | P0 — Must | retention threshold, đo trên create→enqueue |
| NFR-02 | Throughput ≤ 100 rps | NFR | P0 — Must | burst protection, token bucket |
| NFR-03 | Availability ≥ 99.9% | NFR | P0 — Must | uptime tháng, SLA operator |
| NFR-04 | WCAG AA | NFR | P1 — Should | a11y giao diện config/lịch sử |
| NFR-05 | Mandatory opt-in | NFR | P0 — Must | tuân thủ đồng ý, chặn gửi trái phép |
| NFR-06 | Pagination 12/page | NFR | P1 — Should | giới hạn payload list |
| NFR-07 | Filter simple_text_match | NFR | P2 — Could | default lọc nội dung, nâng cấp sau |

## §2: System Diagrams

### Sequence Diagram (5 actors, double-quote labels)

```mermaid
sequenceDiagram
    autonumber
    actor User as "App User (Client)"
    participant NS as "Notification System"
    participant PS as "Preference Store"
    participant DQ as "Delivery Queue"
    participant PP as "Push Provider (FCM/APNs)"
    User->>NS: "Sự kiện nghiệp vụ (order_update/mention/alert)"
    NS->>PS: "Truy vấn preference opt-in theo danh mục"
    PS-->>NS: "Trạng thái cho phép/gạch bỏ"
    NS->>DQ: "Enqueue notification (nếu được phép)"
    DQ->>PP: "Gửi push qua FCM/APNs (token hợp lệ)"
    PP-->>DQ: "Delivery receipt (thành công/thất bại)"
    DQ-->>NS: "Cập nhật trạng thái giao + log"
    NS-->>User: "Ghi lịch sử 30 ngày (in-app)"
```

### Flowchart (3-path: Happy / Alternative / Exception)

```mermaid
flowchart TD
    Start["Sự kiện nghiệp vụ"] --> Pref{"Preference opt-in?"}
    Pref -- "Có (Happy)" --> Send["Gửi push FCM/APNs"]
    Send -- "Thành công" --> Done["Ghi lịch sử + receipt"]
    Pref -- "Tắt (Alternative)" --> Suppress["Ức chế (suppress) + log"]
    Suppress --> History["Hiện trong lịch sử in-app"]
    Send -- "Lỗi/Token hết hạn (Exception)" --> Backoff["Xếp hàng + exponential backoff"]
    Backoff -- "Thất bại kéo dài" --> DLQ["Dead Letter Queue + alert operator"]
```

### ERD (PK/FK + kiểu dữ liệu)

```mermaid
erDiagram
    APP_USER ||--o{ DEVICE_TOKEN : "registers"
    APP_USER ||--o{ NOTIFICATION_PREFERENCE : "configures"
    APP_USER ||--o{ NOTIFICATION : "receives"
    NOTIFICATION_PREFERENCE ||--o{ NOTIFICATION : "gates"
    DEVICE_TOKEN ||--o{ NOTIFICATION : "targets"

    APP_USER {
        integer id PK
        string email
        timestamp created_at
    }
    DEVICE_TOKEN {
        integer id PK
        integer user_id FK
        string token_value
        timestamp token_expiry
        string platform
    }
    NOTIFICATION_PREFERENCE {
        integer id PK
        integer user_id FK
        string category
        boolean enabled
    }
    NOTIFICATION {
        integer id PK
        integer user_id FK
        string category
        string title
        string body_ref
        string status
        timestamp created_at
    }
```

## §3: Data Schema Design

| Trường | Kiểu | Ràng buộc | Mô tả |
|:---|:---|:---|:---|
| `id` | `integer` | `PK, AUTO_INCREMENT` | Khóa chính |
| `user_id` | `integer` | `FK → app_user.id, NOT NULL` | Người nhận |
| `category` | `string` | `enum[order_update,mention,system_alert]` | Danh mục |
| `title` | `string` | `NOT NULL, max 80` | Tiêu đề (không PII) |
| `body_ref` | `string` | `NOT NULL` | Tham chiếu nội dung, không PII thô |
| `status` | `string` | `enum[queued,sent,failed,suppressed]` | Trạng thái giao |
| `created_at` | `timestamp` | `NOT NULL` | Thời gian tạo (TTL 30d) |

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "NotificationSchema",
  "type": "object",
  "properties": {
    "id": { "type": "integer" },
    "user_id": { "type": "integer" },
    "category": { "type": "string", "enum": ["order_update", "mention", "system_alert"] },
    "title": { "type": "string", "maxLength": 80 },
    "body_ref": { "type": "string" },
    "status": { "type": "string", "enum": ["queued", "sent", "failed", "suppressed"] },
    "created_at": { "type": "string", "format": "date-time" }
  },
  "required": ["id", "user_id", "category", "title", "body_ref", "status", "created_at"]
}
```

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "NotificationPreferenceSchema",
  "type": "object",
  "properties": {
    "id": { "type": "integer" },
    "user_id": { "type": "integer" },
    "category": { "type": "string", "enum": ["order_update", "mention", "system_alert"] },
    "enabled": { "type": "boolean" }
  },
  "required": ["id", "user_id", "category", "enabled"]
}
```

## §4: Gherkin Acceptance Criteria

**User Story:** As an App User, I want to receive push notifications for order updates, mentions, and system alerts only when I opt in, so that I stay informed without notification fatigue.

```gherkin
Feature: Mobile Notification Delivery
  Scenario: Happy Path — Gửi thành công khi opt-in
    Given user bật preference danh mục "order_update"
    And device token hợp lệ chưa hết hạn
    When sự kiện cập nhật đơn hàng xảy ra
    Then hệ thống tạo notification và enqueue trong vòng 500ms p95
    And push đến thiết bị qua FCM/APNs thành công
    And bản ghi lịch sử được ghi với status "sent"

  Scenario: Alternative Path — Bị ức chế khi tắt preference
    Given user tắt preference danh mục "mention"
    When sự kiện mention xảy ra
    Then hệ thống đánh dấu notification status "suppressed"
    And sự kiện được ghi log không gửi push
    And user vẫn thấy mục trong lịch sử in-app

  Scenario: Exception Path — Token hết hạn / provider lỗi
    Given device token của user đã hết hạn
    When hệ thống cố gửi push qua FCM/APNs
    Then provider trả lỗi 4xx và receipt báo failed
    And hệ thống xếp vào Delivery Queue với exponential backoff
    And sau thất bại kéo dài đưa vào Dead Letter Queue và alert operator
    And core flow không sập, lịch sử vẫn ghi status "failed"
```

## §5: Risk Assessment Matrix (P×I)

| Mã RR | Rủi ro | Xác suất | Tác động | P×I | Giải pháp giảm thiểu |
|:---|:---|:---:|:---:|:---:|:---|
| RR-01 | Token hết hạn gửi tiếp | Trung bình | Cao | 6 | TTL check + prune + receipt loop |
| RR-02 | Bỏ qua opt-in | Thấp | Cao | 3 | Preference gate deny-by-default + test |
| RR-03 | Vượt 100 rps burst | Cao | Trung bình | 6 | Token bucket + backpressure + drop oldest |
| RR-04 | Push provider outage | Trung bình | Cao | 6 | Exponential backoff + DLQ + alert |
| RR-05 | PII trong payload | Thấp | Cao | 3 | Chỉ reference id, mã hóa at rest |
| RR-06 | Lịch sử 30d phình | Trung bình | Trung bình | 4 | TTL purge + pagination 12 + index |

Rủi ro Cao (RR-01, RR-03, RR-04) đều gắn với P0 → mitigation đưa vào MVP.

## §6: Traceability Mapping

- `[TỪ INPUT]` FR-01..04, danh mục 3 loại, FCM+APNs, 30-day history, backoff.
- `[SUY LUẬN]` NFR defaults (500ms, 100rps, 99.9%, WCAG AA, 12/page, simple_text_match, mandatory opt-in), ERD entities, risk matrix.
- `[CẦN LÀM RÕ]` 0 — mọi khoảng trống đã áp default an toàn (theo elicitation-report §6/§8).
