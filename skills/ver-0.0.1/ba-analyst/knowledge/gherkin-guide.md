# 🥒 Quy Chuẩn Viết Acceptance Criteria Bằng Gherkin

Tài liệu này hướng dẫn chi tiết cách viết Acceptance Criteria (Tiêu chí nghiệm thu) sử dụng ngôn ngữ Gherkin kết hợp với định dạng User Story chuẩn.

<context>
Gherkin giúp chuyển dịch yêu cầu nghiệp vụ thành các kịch bản kiểm thử có thể tự động hóa và dễ hiểu cho cả Business và Development.
</context>

## 1. Cấu Trúc User Story Chuẩn

<instructions>
Mỗi chức năng/tính năng phải đi kèm với một User Story mô tả rõ ràng đối tượng sử dụng, mục đích và giá trị mang lại:
</instructions>

```markdown
**User Story:**
As a [Vai trò người dùng - Actor]
I want to [Hành động muốn thực hiện]
So that [Giá trị/Lợi ích mang lại]
```

## 2. Cấu Trúc Gherkin Bắt Buộc

<instructions>
Sử dụng các từ khóa `Feature`, `Scenario`, `Given`, `When`, `Then` và `And` để thiết kế kịch bản:
</instructions>

```gherkin
Feature: [Tên chức năng]
  [Mô tả ngắn gọn về chức năng]

  Scenario: [Tên kịch bản]
    Given [Bối cảnh / Trạng thái tiền đề bắt đầu]
    When [Hành động của người dùng hoặc hệ thống kích hoạt]
    Then [Kết quả mong đợi trực tiếp]
    And [Các kết quả bổ sung nếu có]
```

## 3. Ràng Buộc Số Lượng Kịch Bản (Scenario Coverage)

```yaml
scenario_coverage_rules:
  minimum_scenarios: 3
  required_paths:
    happy_path:
      desc: "Luồng chuẩn - Mọi điều kiện đều lý tưởng, giao dịch hoặc chức năng hoàn thành thành công."
      min_count: 1
    alternative_path:
      desc: "Luồng thay thế - Xử lý các nhánh rẽ hợp lệ khác để đạt mục đích (ví dụ: dùng ví điện tử thay vì thẻ tín dụng)."
      min_count: 1
    exception_path:
      desc: "Luồng lỗi/ngoại lệ - Xử lý khi xảy ra lỗi validation, mất kết nối, hoặc sai thông tin đầu vào."
      min_count: 1
```

## 4. Quy Tắc Viết Gherkin Chất Lượng (Quality Rules)

```yaml
gherkin_quality_rules:
  testability:
    rule: "Các câu Given/When/Then phải lượng hóa được, không dùng các từ cảm tính, mơ hồ như 'nhanh', 'tiện lợi', 'đẹp'."
    bad_example: "Then hệ thống phải tải trang thật nhanh"
    good_example: "Then hệ thống phải hiển thị kết quả trong vòng dưới 2.0 giây"
  zero_placeholder:
    rule: "Tuyệt đối không chứa TODO, TBD, mock data, hoặc các phần bỏ trống."
  sync_format:
    rule: "Đồng bộ bằng Markdown headers (##, ###) hoặc tables để sẵn sàng import vào các công cụ quản lý dự án (Git/Notion)."
```

## 5. Ví Dụ Áp Dụng Thực Tế

### Ví dụ: Xử lý giao dịch thanh toán trực tuyến

```gherkin
Feature: Xử lý thanh toán hóa đơn giỏ hàng
  Là một khách hàng đã chọn sản phẩm
  Tôi muốn thực hiện thanh toán trực tuyến
  Để hoàn tất việc mua hàng nhanh chóng

  Scenario: Happy Path — Thanh toán thành công bằng thẻ tín dụng
    Given Khách hàng đã đăng nhập vào hệ thống
    And Giỏ hàng của khách hàng có tổng giá trị là 500,000 VND
    And Thẻ tín dụng của khách hàng còn đủ hạn mức thanh toán
    When Khách hàng xác nhận thanh toán
    Then Hệ thống ghi nhận giao dịch thành công
    And Trạng thái đơn hàng chuyển thành "Đã thanh toán"
    And Hệ thống gửi email hóa đơn điện tử cho khách hàng trong vòng 1 phút

  Scenario: Alternative Path — Thanh toán bằng ví điện tử MoMo thành công
    Given Khách hàng đã chọn hình thức thanh toán "Ví điện tử MoMo"
    And Số dư ví MoMo của khách hàng lớn hơn hoặc bằng 500,000 VND
    When Khách hàng quét mã QR code và xác nhận thanh toán trên App MoMo
    Then Hệ thống nhận được webhook xác nhận từ MoMo
    And Hệ thống chuyển trạng thái đơn hàng thành "Đã thanh toán"

  Scenario: Exception Path — Thẻ tín dụng hết hạn sử dụng
    Given Khách hàng đã nhập thông tin thẻ tín dụng có ngày hết hạn nhỏ hơn ngày hiện tại
    When Khách hàng thực hiện xác nhận thanh toán
    Then Hệ thống báo lỗi "Thẻ tín dụng đã hết hạn sử dụng"
    And Hệ thống không trừ tiền trong tài khoản
    And Giỏ hàng vẫn được giữ nguyên trạng thái "Chờ thanh toán"
```
