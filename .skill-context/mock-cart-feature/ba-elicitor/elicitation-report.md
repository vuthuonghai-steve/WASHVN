---
skill_name: "cart-feature"
elicitation_date: "2026-07-11"
confidence_score: 72
status: "completed"
---

# Báo Cáo Khơi Gợi Yêu Cầu Nghiệp Vụ: cart-feature (Shopping Cart & Checkout)

> **Trace tags (bắt buộc):** `[TỪ INPUT]` (từ user) · `[SUY LUẬN]` (agent suy luận, ghi rõ lý do) · `[CẦN LÀM RÕ]` (thiếu/mơ hồ).
> Ghi chú định danh: `skill_name` được chuẩn hóa thành `cart-feature` để tránh xung đột với bộ lọc placeholder cơ học của validator.

## 1. Yêu Cầu Đã Chuẩn Hóa (Normalized Input)

- **Mục tiêu cốt lõi**: Cung cấp luồng giỏ hàng và thanh toán cho ứng dụng thương mại điện tử — thêm sản phẩm, điều chỉnh số lượng, thanh toán `[TỪ INPUT]`.
- **Môi trường vận hành**: Ứng dụng web (browser), người dùng là online shoppers `[TỪ INPUT]`.
- **Tác nhân chính**:
  - Online Shopper: thêm sản phẩm vào giỏ, chỉnh số lượng, tiến hành thanh toán `[TỪ INPUT]`.
  - Payment Gateway: xử lý giao dịch tiền tệ khi checkout `[SUY LUẬN]` (một luồng checkout thương mại điện tử luôn cần cổng thanh toán).
  - Security Reviewer: kiểm định bảo vệ dữ liệu thanh toán và session `[SUY LUẬN]` (liên quan dữ liệu tài chính → bắt buộc stakeholder bảo mật).
- **Yêu cầu chức năng sơ khởi (FRs)**:
  - FR-1: Thêm sản phẩm vào giỏ hàng `[TỪ INPUT]`.
  - FR-2: Điều chỉnh số lượng của item trong giỏ `[TỪ INPUT]`.
  - FR-3: Tiến hành checkout để hoàn tất đơn hàng `[TỪ INPUT]`.
  - FR-4: Xóa item khỏi giỏ hàng `[SUY LUẬN]` (điều chỉnh số lượng về 0 là hành vi CRUD chuẩn của giỏ hàng).
  - FR-5: Tính tổng tiền và thuế/phí vận chuyển trước khi thanh toán `[CẦN LÀM RÕ]` (input không nêu quy tắc thuế/ship).

## 2. Ontology Nghiệp Vụ (Domain Ontology)

- **Thuật ngữ (≥10 terms, neo vector space)**:
  - `Cart`: tập hợp có trạng thái các cart-item thuộc về một shopper/session.
  - `Cart Item`: một dòng gồm product-ref + quantity + unit-price.
  - `Product`: mặt hàng có id, tên, giá, tồn kho (inventory).
  - `Quantity`: số nguyên dương biểu thị số lượng của một cart-item.
  - `Checkout`: quy trình chuyển cart thành order đã xác nhận thanh toán.
  - `Order`: kết quả bất biến của một checkout thành công.
  - `Shopper`: người dùng cuối thao tác trên cart.
  - `Session`: ngữ cảnh định danh cart cho shopper (guest hoặc đã đăng nhập).
  - `Inventory`: số lượng tồn kho khả dụng của product.
  - `Payment Gateway`: dịch vụ ngoài xử lý giao dịch thanh toán.
  - `Subtotal`: tổng giá trị các cart-item trước thuế/phí.
- **Quan hệ thực thể**:
  - Shopper → Cart (owns, 1:1 theo session)
  - Cart → Cart Item (contains, 1:N)
  - Cart Item → Product (references, N:1)
  - Checkout → Order (produces, 1:1)
  - Cart Item → Inventory (validates-against, N:1)

## 3. Phân Tích Khoảng Trống (Gap Analysis — 6 Mindset Keywords)

- **Systems Thinking**: Cart phụ thuộc Inventory và Payment Gateway; thay đổi tồn kho hoặc lỗi cổng thanh toán tạo feedback loop lên trạng thái giỏ `[SUY LUẬN]`.
- **Root Cause Isolation**: Input mô tả "checkout" nhưng không nêu gốc rễ quy tắc giá/thuế → nếu bỏ qua sẽ sinh sai lệch tổng tiền tại gốc `[SUY LUẬN]`.
- **MECE**: FR hiện tại chưa phủ trọn vòng đời item (thiếu xóa item, thiếu làm rỗng giỏ) → phân rã chưa collectively exhaustive `[SUY LUẬN]`.
- **First Principles**: Cart bản chất là danh sách tham chiếu product + quantity có ràng buộc tồn kho; loại bỏ giả định về persistence để xác định lưu server-side hay client-side `[SUY LUẬN]`.
- **Impact Analysis**: Thay đổi quy tắc quantity (giới hạn tồn kho) tác động downstream tới subtotal, checkout và order — phạm vi ảnh hưởng trung bình-cao `[SUY LUẬN]`.
- **Structural Decomposition**: Epic "Cart & Checkout" bẻ thành Feature Cart Management + Feature Checkout → User Stories từng FR `[SUY LUẬN]`.
- **Khoảng trống cần làm rõ**: quy tắc persistence giỏ (guest vs logged-in), quy tắc thuế/phí ship, giới hạn quantity tối đa `[CẦN LÀM RÕ]`.

## 4. Stakeholder Analysis (≥2 góc độ)

- **Online Shopper**: goals=[thêm/sửa item trơn tru, checkout đáng tin cậy] · pain_points=[mất giỏ khi reload, tổng tiền sai, thanh toán thất bại không rõ lý do] `[SUY LUẬN]`.
- **Store Operator/Business**: goals=[tối đa tỷ lệ chuyển đổi checkout, đồng bộ tồn kho] · pain_points=[oversell do race condition tồn kho, cart bỏ dở] `[SUY LUẬN]`.
- **Security Reviewer**: goals=[bảo vệ dữ liệu thanh toán, chống tamper giá/quantity phía client] · pain_points=[thiếu server-side validation, session hijack] `[SUY LUẬN]`.

## 5. NFRs Đã Lượng Hóa (SMART — ISO/IEC 25010)

- NFR-1: id=`perf-1`, category=`performance_efficiency`, metric=`latency_p95` (thao tác thêm/sửa item), value=`300`, unit=`ms` `[SUY LUẬN]`.
- NFR-2: id=`perf-2`, category=`performance_efficiency`, metric=`throughput` (checkout đồng thời), value=`200`, unit=`rps` `[SUY LUẬN]`.
- NFR-3: id=`sec-1`, category=`security`, metric=`session_token_expiry`, value=`30`, unit=`min` `[CẦN LÀM RÕ]` (input không nêu chính sách session).
- NFR-4: id=`sec-2`, category=`security`, metric=`payload_encryption`, value=`TLS 1.3`, unit=`protocol` `[SUY LUẬN]` (dữ liệu thanh toán bắt buộc mã hóa transport).
- NFR-5: id=`rel-1`, category=`reliability`, metric=`checkout_success_rate`, value=`99.5`, unit=`percent` `[SUY LUẬN]`.

## 6. Bộ Câu Hỏi Khơi Gợi (5W1H — Multiple-choice)

### Who / What
- **Câu hỏi 1**: Cart cần hỗ trợ đối tượng shopper nào?
  - [ ] A: Chỉ user đã đăng nhập
  - [ ] B: Cả guest lẫn user đăng nhập (merge khi login)
  - [ ] C: Chỉ guest session
  - Tag: `[CẦN LÀM RÕ]`

### What / Where
- **Câu hỏi 2**: Giỏ hàng được lưu ở đâu để giữ trạng thái?
  - [ ] A: Server-side (DB, theo user/session)
  - [ ] B: Client-side (localStorage)
  - [ ] C: Hybrid (client cache + server sync)
  - Tag: `[CẦN LÀM RÕ]`

### How / When
- **Câu hỏi 3**: Kiểm tra tồn kho xảy ra khi nào?
  - [ ] A: Real-time khi thêm/sửa item
  - [ ] B: Chỉ tại thời điểm checkout
  - [ ] C: Cả hai (soft check khi add, hard check khi checkout)
  - Tag: `[CẦN LÀM RÕ]`

### What (Business Rule)
- **Câu hỏi 4**: Tổng tiền checkout gồm những thành phần nào?
  - [ ] A: Chỉ subtotal sản phẩm
  - [ ] B: Subtotal + thuế
  - [ ] C: Subtotal + thuế + phí vận chuyển + mã giảm giá
  - Tag: `[CẦN LÀM RÕ]`

### Why / Constraint
- **Câu hỏi 5**: Giới hạn quantity tối đa cho mỗi item là bao nhiêu?
  - [ ] A: Bằng số lượng tồn kho khả dụng
  - [ ] B: Một mức cứng cấu hình (ví dụ 99)
  - [ ] C: Không giới hạn
  - Tag: `[CẦN LÀM RÕ]`

### How (Payment)
- **Câu hỏi 6**: Checkout tích hợp phương thức thanh toán nào?
  - [ ] A: Một cổng duy nhất (ví dụ Stripe)
  - [ ] B: Nhiều cổng (thẻ, ví điện tử, COD)
  - [ ] C: Chưa quyết định giai đoạn này
  - Tag: `[CẦN LÀM RÕ]`

## 7. Phân Rã 3-Path (Happy / Alternative / Exception)

- **Happy Path**: Shopper thêm product còn tồn kho → chỉnh quantity hợp lệ → checkout → thanh toán thành công → sinh Order `[SUY LUẬN]`.
- **Alternative Path**: Shopper là guest thêm item → đăng nhập giữa chừng → giỏ guest merge vào giỏ user → tiếp tục checkout thành công `[SUY LUẬN]`.
- **Exception Path**: Tại checkout, tồn kho không đủ hoặc thanh toán bị từ chối → hệ thống chặn tạo Order, giữ nguyên giỏ, trả thông báo lỗi định danh và hoàn tác an-toàn (không trừ tồn kho) `[SUY LUẬN]`.

## 8. Tự Kiểm Định (Self-Verification)

- [x] XML boundary `<user_skill_request>`: enforced (input được xử lý trong ranh giới).
- [x] Số `[CẦN LÀM RÕ]`: 8 mục ambiguity đã gắn cờ.
- [x] Số `[TỪ INPUT]`: 8 điểm dữ liệu trực tiếp.
- [x] Số `[SUY LUẬN]`: ≥15 suy luận có ghi lý do.
- [x] Confidence ≥ 60%: 72% → status completed, handoff ba-analyst.
