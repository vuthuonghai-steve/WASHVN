# 📋 Quy Tắc Phân Loại Yêu Cầu và Ma Trận MoSCoW

Tài liệu này định nghĩa logic phân tách yêu cầu hệ thống thành các yêu cầu chức năng (FR), yêu cầu phi chức năng (NFR) lượng hóa, và cách thức áp dụng ma trận MoSCoW để sắp xếp độ ưu tiên kỹ thuật.

<context>
Trong phát triển phần mềm, việc phân biệt rõ ràng giữa các tính năng hệ thống thực hiện (Functional Requirements) và các ràng buộc/tiêu chuẩn vận hành (Non-Functional Requirements) là tối quan trọng để định hình kiến trúc hệ thống và lập kế hoạch kiểm thử chính xác.
</context>

## 1. Phân Loại Yêu Cầu (FR vs NFR)

<instructions>
Agent thực hiện phân loại tự động dựa trên các nguyên tắc và định nghĩa sau:
</instructions>

```yaml
classification_rules:
  functional_requirements:
    definition: "Yêu cầu chức năng mô tả hành động, quy trình nghiệp vụ, CRUD (Create, Read, Update, Delete), hoặc luồng tương tác mà hệ thống BẮT BUỘC phải thực thi."
    triggers:
      - "Mô tả luồng nghiệp vụ"
      - "Thao tác dữ liệu (CRUD)"
      - "Các bước xử lý hệ thống"
      - "Tương tác giữa Actor và Hệ thống"
  
  non_functional_requirements:
    definition: "Yêu cầu phi chức năng mô tả các ràng buộc về mặt chất lượng, hiệu năng, bảo mật, khả năng mở rộng, tính sẵn sàng và trải nghiệm hệ thống."
    rule_quantification: "Mọi yêu cầu phi chức năng dạng cảm tính (như 'chạy rất nhanh', 'bảo mật cao') BẮT BUỘC phải được lượng hóa cụ thể thành các chỉ số kỹ thuật đo lường được."
    quantified_metrics:
      throughput: "Ví dụ: 1000 req/s, 500 TPS"
      latency: "Ví dụ: Latency < 200ms cho 95% API calls"
      availability: "Ví dụ: Uptime 99.9% hằng tháng"
      security: "Ví dụ: Mã hóa dữ liệu tĩnh AES-256, HTTPS TLS 1.3"
```

## 2. Ma Trận MoSCoW (Prioritization Matrix)

<instructions>
Áp dụng ma trận MoSCoW để tự động phân bổ độ ưu tiên cho từng yêu cầu kỹ thuật dựa theo các định nghĩa sau:
</instructions>

```yaml
moscow_matrix:
  must_have:
    priority: "P0"
    description: "Bắt buộc phải có (MVP). Không thể phát hành hoặc vận hành hệ thống nếu thiếu yêu cầu này."
    example_criteria: "Lưu trữ dữ liệu giao dịch thành công, xác thực người dùng."
    
  should_have:
    priority: "P1"
    description: "Quan trọng nhưng không chặn phát hành. Có thể dùng giải pháp tạm thời (workaround) nếu chưa có, nhưng rất cần thiết cho trải nghiệm người dùng hoặc vận hành."
    example_criteria: "Gửi email xác nhận ngay lập tức, tự động retry khi upload thất bại."
    
  could_have:
    priority: "P2"
    description: "Có thì tốt (Nice-to-have). Yêu cầu có độ rủi ro thấp, ít tác động và có thể dời sang các pha sau mà không ảnh hưởng tới core flow."
    example_criteria: "Gợi ý thông minh dựa trên lịch sử, xuất báo cáo định dạng Excel tùy chỉnh."
    
  wont_have:
    priority: "P3"
    description: "Chưa thực hiện trong pha này. Xác định rõ ràng các phạm vi nằm ngoài (Out of Scope) của dự án để tránh trượt phạm vi (Scope Creep)."
    example_criteria: "Hỗ trợ đa ngôn ngữ trong phiên bản đầu tiên."
```

## 3. Lý Do Kỹ Thuật Mẫu (Technical Justification Examples)

<instructions>
Khi gán độ ưu tiên MoSCoW, Agent phải điền lý do kỹ thuật rõ ràng trong cột "Lý do kỹ thuật" ở bảng phân loại yêu cầu.
</instructions>

- **Cho Must Have (P0):** *"Nếu không lưu được log giao dịch, hệ thống sẽ vi phạm luật an toàn tài chính và không thể đối soát khi xảy ra sự cố."*
- **Cho Should Have (P1):** *"Việc gửi email xác nhận giúp giảm tỷ lệ người dùng bấm nút thanh toán nhiều lần gây trùng lặp giao dịch."*
- **Cho Could Have (P2):** *"Tính năng xuất PDF giúp người dùng lưu trữ ngoại tuyến nhanh hơn, nhưng họ vẫn có thể xem trực tiếp trên giao diện web hoặc chụp màn hình làm giải pháp thay thế."*

## 4. Chuẩn Tư Duy & Tuân Thủ (Compliance Mindset)

```yaml
compliance_standards:
  mindset: "Tư duy Chuẩn hóa và Tuân thủ (Compliance Mindset) từ Business đến System."
  rules:
    - "Sử dụng thuật ngữ chuẩn quốc tế theo tài liệu BABOK và Agile/Scrum."
    - "Đảm bảo tính nhất quán tuyệt đối giữa yêu cầu nghiệp vụ (Business) và đặc tả kỹ thuật (System)."
  required_sources:
    - "SRS - Software Requirement Specification"
    - "Wireframe Specs"
    - "User Story template (As a... I want... So that...)"
    - "Gherkin Acceptance Criteria (Given-When-Then)"
    - "Mermaid.js System Diagrams"
    - "Data Schema & ERD Design"
```
