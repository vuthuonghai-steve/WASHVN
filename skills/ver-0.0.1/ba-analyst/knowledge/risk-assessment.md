# ⚠️ Khung Đánh Giá Rủi Ro và Phạm Vi Ảnh Hưởng

Tài liệu này quy định cách thức xây dựng ma trận đánh giá rủi ro hệ thống, định lượng mức độ nghiêm trọng và thiết lập các kế hoạch giảm thiểu (mitigation paths) tương thích với độ ưu tiên MoSCoW.

<context>
Khi chuyển đổi các yêu cầu nghiệp vụ thành đặc tả kỹ thuật, việc phân tích rủi ro giúp đội ngũ phát triển lường trước các vấn đề về kiến trúc, bảo mật, hiệu năng hoặc tích hợp bên thứ ba, từ đó tối ưu hóa thiết kế hệ thống ngay từ đầu.
</context>

## 1. Ma Trận Đánh Giá Rủi Ro (Risk Matrix)

```yaml
risk_matrix:
  dimensions:
    probability:
      - "Thấp (Low)"
      - "Trung bình (Medium)"
      - "Cao (High)"
    impact:
      - "Thấp (Low)"
      - "Trung bình (Medium)"
      - "Cao (High)"
  
  risk_scoring_levels:
    acceptable:
      probability: "Thấp"
      impact: "Thấp"
      level: "Chấp nhận được (Acceptable)"
      action: "Theo dõi định kỳ, không cần hành động ngay."
    needs_mitigation:
      probability: "Trung bình"
      impact: "Cao"
      level: "Cần kế hoạch giảm thiểu (Mitigation Needed)"
      action: "Thiết kế giải pháp dự phòng hoặc kiến trúc thay thế."
    unacceptable:
      probability: "Cao"
      impact: "Cao"
      level: "Không thể chấp nhận (Unacceptable)"
      action: "Yêu cầu giải pháp giảm thiểu ngay lập tức trước khi triển khai hoặc cấu trúc lại phạm vi."
```

## 2. Quy Tắc Xử Lý Rủi Ro Của Agent (Action Rules)

<instructions>
Khi thực hiện phân tích, Agent phải tuân thủ các quy tắc sau:
</instructions>

1. **Khoanh vùng ảnh hưởng (Change Impact Vector)**: Xác định tất cả các module, API, hoặc bảng cơ sở dữ liệu sẽ bị ảnh hưởng trực tiếp hay gián tiếp bởi tính năng hoặc thay đổi mới.
2. **Đánh giá trước khi thay đổi (Pre-change Risk Estimation)**: Ước lượng rủi ro kỹ thuật về hiệu năng, bảo mật, và khả năng mở rộng trước khi thực hiện thiết kế chi tiết.
3. **Đề xuất giải pháp cụ thể (Mitigation Paths)**: Mọi rủi ro được liệt kê phải đi kèm ít nhất một giải pháp kỹ thuật cụ thể (ví dụ: dùng caching, rate limiting, mã hóa, DB replica) thay vì ghi chung chung.

## 3. Tích Hợp Rủi Ro với MoSCoW (MoSCoW Integration Rules)

```yaml
moscow_integration:
  high_risk_must_have:
    condition: "Rủi ro Cao + Độ ưu tiên Must Have (P0)"
    strategy: "Bắt buộc ưu tiên lập kế hoạch giảm thiểu (Mitigation Planning) và đưa giải pháp kỹ thuật vào làm một phần của MVP."
    
  high_risk_wont_have:
    condition: "Rủi ro Cao + Độ ưu tiên Wont Have (P3)"
    strategy: "Đánh giá lại phạm vi (Scope Assessment) để loại bỏ hoàn toàn rủi ro hoặc khoanh vùng biên an toàn."
    
  low_risk_could_have:
    condition: "Rủi ro Thấp + Độ ưu tiên Could Have (P2)"
    strategy: "Chấp nhận rủi ro và tiến hành theo dõi (Monitor & Accept) trong các pha sau."
```

## 4. Ví Dụ Đánh Giá Rủi Ro Hệ Thống

| Mã RR | Mô tả rủi ro | Xác suất (L/M/H) | Tác động (L/M/H) | Giải pháp giảm thiểu |
|:---|:---|:---|:---|:---|
| **RR-01** | Khóa bí mật (S3 AWS Credential) bị rò rỉ khi lưu trực tiếp trong mã nguồn. | Trung bình | Cao | Sử dụng AWS IAM Instance Role hoặc lưu trong HashiCorp Vault / ENV Secrets thay vì hardcode. |
| **RR-02** | Tiến trình backup DB Postgres bị timeout do dữ liệu lớn hơn dự kiến (>10GB). | Trung bình | Trung bình | Thực hiện nén dữ liệu streaming hoặc phân tách backup (incremental backup) thay vì backup full hằng ngày. |
| **RR-03** | Khách hàng spam API gửi yêu cầu backup liên tục làm treo máy chủ. | Cao | Trung bình | Áp dụng Rate Limiting (tối đa 3 request backup/giờ/user) ở API Gateway. |
