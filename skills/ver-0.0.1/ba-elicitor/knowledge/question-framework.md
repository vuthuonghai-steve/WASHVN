# 5W1H Elicitation Question Framework

Tài liệu này đặc tả cấu trúc bộ câu hỏi 5W1H và cơ chế phân tách luồng (Path Decomposition) mà BA Elicitor sử dụng để thu thập thông tin còn thiếu.

## 1. Cấu trúc Bộ Câu Hỏi Chuẩn Hóa

Khi yêu cầu của người dùng bị mơ hồ hoặc thiếu các khía cạnh nghiệp vụ, Agent kích hoạt bộ câu hỏi 5W1H dưới đây:

```yaml
question_types:
  who:
    label: "Tác nhân (Actor)"
    sub_questions:
      - "Ai thực hiện thao tác này? (Người dùng / Hệ thống / Hệ thống thứ ba)"
      - "Ai là người hưởng lợi từ kết quả?"
      - "Ai chịu trách nhiệm phê duyệt?"
  
  what:
    label: "Hành động / Đối tượng"
    sub_questions:
      - "Thao tác cụ thể là gì? (CRUD? Báo cáo? Phê duyệt?)"
      - "Dữ liệu nào được tạo ra / thay đổi?"
      - "Sản phẩm đầu ra là gì?"
  
  why:
    label: "Mục đích / Lý do"
    sub_questions:
      - "Tại sao cần tính năng này? (Mục tiêu kinh doanh?)"
      - "Nếu không có, điều gì xảy ra?"
      - "Giá trị mang lại là gì?"
  
  how:
    label: "Phương thức"
    sub_questions:
      - "Quy trình thực hiện ra sao? (Có bao nhiêu bước?)"
      - "Dữ liệu đầu vào từ đâu? / Đầu ra đi đâu?"
      - "Xử lý đồng bộ hay bất đồng bộ?"
  
  when:
    label: "Thời điểm / Tần suất"
    sub_questions:
      - "Khi nào sự kiện được kích hoạt? (Theo lịch / Sự kiện / Thủ công)"
      - "Tần suất xử lý? (Real-time / Batch / Theo ca)"
  
  where:
    label: "Vị trí / Kênh"
    sub_questions:
      - "Tính năng hoạt động ở đâu? (Web / Mobile / API / Internal)"
      - "Dữ liệu được lưu ở đâu? (DB / Cache / File / External Service)"
```

## 2. Cơ chế Phân tách Luồng (Path Decomposition)

Mỗi yêu cầu nghiệp vụ bắt buộc phải được phân tách thành 3 luồng xử lý độc lập để tránh bỏ sót các trường hợp ngoại lệ hoặc lỗi hệ thống:

```yaml
path_types:
  - path: "Happy Path"
    desc: "Luồng chuẩn — mọi điều kiện đều đúng và hệ thống thực hiện thành công quy trình chính."
    min_scenarios: 1
  - path: "Alternative Path"
    desc: "Luồng thay thế — người dùng đi theo các bước khác nhưng cuối cùng vẫn đạt kết quả thành công."
    min_scenarios: 1
  - path: "Exception Path"
    desc: "Luồng lỗi — xảy ra lỗi hệ thống, xác thực thất bại, hoặc dữ liệu không hợp lệ và hệ thống cần xử lý an toàn."
    min_scenarios: 1
```

## 3. Định dạng Tương tác (Interaction Format)

Khi cần làm rõ thông tin, Agent KHÔNG đặt câu hỏi mở chung chung. Thay vào đó, sử dụng:

```yaml
response_format:
  type: "Multiple-choice hoặc Bullet points"
  guideline: "Đưa ra các phương án lựa chọn cụ thể hoặc gợi ý sẵn để người dùng dễ dàng trả lời hoặc chọn lựa, giúp tăng tốc độ thu thập thông tin nghiệp vụ định lượng."
```
