# 📊 Quy Chuẩn Cú Pháp Vẽ Sơ Đồ Mermaid.js

Tài liệu này hướng dẫn chi tiết cách vẽ sơ đồ Sequence, Flowchart, ERD, và Use Case bằng Mermaid.js. Nhằm tránh các lỗi dựng hình (rendering errors) phổ biến của LLMs khi vẽ sơ đồ.

<context>
Mermaid.js là một công cụ mạnh mẽ để dựng sơ đồ từ văn bản. Tuy nhiên, parser của Mermaid rất nhạy cảm với các ký tự đặc biệt, dấu ngoặc lồng nhau và các từ khóa đặc biệt. Việc tuân thủ nghiêm ngặt quy tắc viết nhãn (labels) là bắt buộc.
</context>

## 1. Nguyên Tắc An Toàn Mermaid (Mermaid Safety Rules)

```yaml
safety_rules:
  label_quoting:
    rule: "BẮT BUỘC bọc tất cả các nhãn (labels), tên tác nhân (actors) hiển thị hoặc điều kiện trong dấu ngoặc kép đôi."
    bad_syntax: "A[Người dùng] --> B{Có lỗi?}"
    good_syntax: 'A["Người dùng"] --> B{"Có lỗi?"}'
  character_restrictions:
    rule: "Không sử dụng ký tự đặc biệt (như parentheses, brackets, braces, slash, commas) bên ngoài dấu ngoặc kép."
  zero_placeholder:
    rule: "Tuyệt đối KHÔNG sử dụng TODO, TBD, mock-up hoặc dấu ba chấm (...) bên trong các sơ đồ. Mọi thành phần phải được đặt tên đầy đủ, rõ nghĩa."
```

## 2. Sequence Diagram (Sơ Đồ Tuần Tự)

```yaml
sequence_rules:
  actors_minimum: "Phải có ít nhất 3 actors/participants tham gia vào sơ đồ."
  flows_required: "Phải thể hiện đầy đủ 3 luồng: Happy Path (chuẩn), Alternative Path (thay thế), Exception Path (lỗi)."
```

### Template Sequence Diagram Chuẩn:
```mermaid
sequenceDiagram
    autonumber
    actor User as "Người dùng (Client)"
    participant Controller as "Bộ điều khiển (Controller)"
    participant Auth as "Dịch vụ Xác thực (Auth Service)"
    participant DB as "Cơ sở dữ liệu (Database)"

    %% Luồng chuẩn (Happy Path)
    Note over User, DB: Happy Path - Luồng Đăng nhập chuẩn
    User->>Controller: "Yêu cầu đăng nhập (email, password)"
    Controller->>Auth: "Xác thực thông tin đăng nhập"
    Auth->>DB: "Truy vấn thông tin tài khoản"
    DB-->>Auth: "Thông tin hợp lệ"
    Auth-->>Controller: "Token đăng nhập thành công"
    Controller-->>User: "Phản hồi mã trạng thái 200 + Token"

    %% Luồng thay thế / ngoại lệ (Alternative / Exception Path)
    Note over User, DB: Exception Path - Sai thông tin đăng nhập
    User->>Controller: "Yêu cầu đăng nhập với sai email/password"
    Controller->>Auth: "Xác thực thông tin"
    Auth->>DB: "Truy vấn thông tin tài khoản"
    DB-->>Auth: "Tài khoản không khớp"
    Auth-->>Controller: "Trả về lỗi 401 Unauthorized"
    Controller-->>User: "Thông báo lỗi sai thông tin"
```

## 3. Flowchart / Activity Diagram (Sơ Đồ Luồng Hoạt Động)

```yaml
flowchart_rules:
  direction: "Sử dụng hướng dọc (TD) hoặc ngang (LR)."
  branching: "Các điểm rẽ nhánh điều kiện phải ghi rõ điều kiện trong hình thoi `{}` và các đường đi ra phải được đặt tên."
```

### Template Flowchart Chuẩn:
```mermaid
flowchart TD
    Start["Bắt đầu quy trình"] --> check_login{"Người dùng đã đăng nhập?"}
    
    %% Happy Path & Alt Path
    check_login -- "Có" --> process_payment["Xử lý thanh toán"]
    check_login -- "Không" --> redirect_login["Chuyển hướng sang trang đăng nhập"]
    
    redirect_login --> login_success{"Đăng nhập thành công?"}
    login_success -- "Đồng ý" --> process_payment
    
    %% Exception Path
    login_success -- "Hủy/Thất bại" --> ErrorEnd["Kết thúc với lỗi 401"]
    
    process_payment --> payment_check{"Thanh toán hợp lệ?"}
    payment_check -- "Thành công" --> End["Hoàn thành thanh toán & Gửi mail"]
    payment_check -- "Lỗi thẻ/Hết tiền" --> RetryPayment["Yêu cầu thẻ khác"]
    RetryPayment --> process_payment
```

## 4. Entity Relationship Diagram - ERD (Sơ Đồ Thực Thể)

```yaml
erd_rules:
  relationship_markers:
    one_to_many: "||--o{"
    one_to_one: "||--||"
    many_to_many: "}o--o{"
  data_types: "BẮT BUỘC khai báo kiểu dữ liệu cho từng cột (string, integer, boolean, timestamp, v.v.)."
  key_constraints: "BẮT BUỘC đánh dấu khóa chính (PK) và khóa ngoại (FK) rõ ràng."
```

### Template ERD Chuẩn:
```mermaid
erDiagram
    USER ||--o{ ORDER : "places"
    ORDER ||--|{ ORDER_ITEM : "contains"
    
    USER {
        integer id PK
        string email
        string password_hash
        timestamp created_at
    }
    
    ORDER {
        integer id PK
        integer user_id FK
        string status
        float total_amount
        timestamp created_at
    }
    
    ORDER_ITEM {
        integer id PK
        integer order_id FK
        string product_name
        integer quantity
        float price
    }
```

## 5. Use Case Diagram (Sơ Đồ Ca Sử Dụng)

<instructions>
Use Case diagram giúp biểu diễn trực quan các chức năng hệ thống cung cấp cho các Actor khác nhau. Nhãn của Use Case phải nằm trong dấu ngoặc tròn `()`.
</instructions>

### Template Use Case Chuẩn:
```mermaid
usecaseDiagram
    actor Admin as "Quản trị viên"
    actor Customer as "Khách hàng"

    rectangle "Hệ thống E-Commerce" {
        usecase UC1 as "Xem sản phẩm"
        usecase UC2 as "Đặt hàng"
        usecase UC3 as "Quản lý kho hàng"
        usecase UC4 as "Xử lý đơn hàng"
    }

    Customer --> UC1
    Customer --> UC2
    Admin --> UC3
    Admin --> UC4
```
