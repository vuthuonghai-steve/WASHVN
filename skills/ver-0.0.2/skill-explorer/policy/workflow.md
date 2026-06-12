# Hướng Dẫn Quy Trình Vận Hành (Workflow Phases)

> **Mã số**: STG0-POL-01
> **Mục tiêu**: Chuẩn hóa quy trình 4 Phase làm việc của Explorer Agent.

---

## Phase 1: Input Acceptance & Intent Analysis

1.  **Tiếp nhận yêu cầu**: Nhận mô tả ý tưởng ban đầu của người dùng về kỹ năng cần tạo.
2.  **Khởi tạo bối cảnh**: Chạy script `python3 scripts/init_context.py {target_skill}` để khởi tạo thư mục làm việc.
3.  **Phân tích nghiệp vụ**:
    - Xác định mục tiêu tối cao của skill đích.
    - Làm rõ các hệ thống, API hoặc file mã nguồn mà skill này sẽ tương tác trực tiếp.

---

## Phase 2: Golden Standards Assessment

1.  **Đọc các file Tri thức**: Gọi `view_file` nạp `knowledge/exploration-standards.md` và `knowledge/security-standards.md`.
2.  **Đánh giá 7 Tiêu chuẩn Vàng**:
    - Phân tích và đưa ra giải pháp thiết kế cho từng tiêu chí: Tái sử dụng, Ghép chuỗi, Bảo trì prompt (Goldilocks), Bảo mật (XML/Docker), Tối ưu token (Progressive Disclosure), Tính di động và Khả năng chịu lỗi.
    - *Ghi chú bảo mật*: Bắt buộc phải xác định xem kỹ năng đích có cần thực thi code hay không để quy hoạch sandbox.

---

## Phase 3: Resource Gathering & Mining

1.  **Tra cứu Codebase nội bộ**:
    - Tra cứu các thư viện, hàm helper, API hiện hữu trong codebase bằng `search_files` và LSP.
    - Dùng `data/search-blacklist.yaml` để loại bỏ các file hệ thống không liên quan.
2.  **Tra cứu tri thức bên ngoài**:
    - Gọi `search_web` và `read_url_content` để tìm hiểu các tiêu chuẩn kỹ thuật hoặc best practices.
3.  **Lưu trữ tài nguyên**:
    - Ghi nhận tất cả tài liệu nghiệp vụ, mã nguồn mẫu, API spec thu thập được vào các file độc lập bên dưới `.skill-context/{target_skill}/resources/`.

---

## Phase 4: Synthesis & Deliver

1.  **Nạp tệp mẫu**: Đọc `templates/exploration.md.template`.
2.  **Biên soạn báo cáo**: Ghi toàn bộ kết quả tổng hợp vào `.skill-context/{target_skill}/exploration.md`.
3.  **Chạy kiểm định chất lượng**:
    - Tự kiểm tra bằng checklist `loop/exploration-checklist.md`.
    - Chạy bộ xác thực frontmatter: `python3 ../_shared/validators/schema_validator.py --schema ../_shared/schemas/exploration.schema.yaml .skill-context/{target_skill}/exploration.md`.
4.  **Bàn giao Stage 0**: Trình bày báo cáo tóm tắt bằng tiếng Việt cho người dùng và kết thúc turn.
