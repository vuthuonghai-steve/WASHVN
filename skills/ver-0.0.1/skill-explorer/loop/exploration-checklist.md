# Quality Gate: Exploration Quality Checklist

> **Vai trò**: Tự kiểm định chất lượng tệp tin đầu ra `exploration.md` trước khi tiến hành bàn giao Stage 0.

---

## 1. Kiểm tra 7 Tiêu chuẩn Vàng

- [ ] **Khả năng tái sử dụng (Reusability)**: Đã đề xuất tách biệt tri thức nghiệp vụ tĩnh và chỉ dẫn hành động động chưa?
- [ ] **Khả năng kết hợp (Composability)**: Đã quy định rõ thứ tự ưu tiên hoặc meta-prompting khi ghép chuỗi chưa?
- [ ] **Khả năng bảo trì (Maintainability)**: SKILL.md đề xuất có tuân thủ cấu trúc 4 lớp và Goldilocks zone không?
- [ ] **Bảo mật (Security)**:
  - [ ] Đã có giải pháp bọc XML delimiters để cách ly dữ liệu thô chống Prompt Injection?
  - [ ] Đã chỉ định chạy trong Docker Sandbox biệt lập nếu skill đích có đi kèm thực thi mã?
- [ ] **Hiệu suất Token**: Đã lên phương án Progressive Disclosure nạp dynamic Tier 1/2/3 chưa?
- [ ] **Tính di động**: Đường dẫn file đề xuất có ở dạng tương đối không? Có bị trói buộc ngầm vào mô hình nào không?
- [ ] **Độ phục hồi**: Đã thiết lập cơ chế ghi log thực thi và fallback HITL rõ ràng khi lỗi chưa?
- [ ] **Đánh giá quy mô (Scale & Complexity)**: Đã chạy bảng tính điểm SCS nghiệp vụ chưa? Đã đưa ra kết luận phân rã Micro-skills rõ ràng khi SCS > 3.0 chưa?
- [ ] **Thiết lập luồng (Orchestration)**: Đã vẽ sơ đồ Mermaid điều phối luồng phối hợp giữa các Micro-skills chưa?

---

## 2. Kiểm tra Cấu trúc & Định dạng Tệp

- [ ] Frontmatter đầy đủ các trường yêu cầu và khớp chuẩn `exploration.schema.yaml`.
- [ ] Tồn tại đầy đủ **8 chương mục tiêu đề bắt buộc** từ §1 đến §8.
- [ ] Mọi đề xuất tri thức domain đều có nguồn tham chiếu thực tế tại thư mục `resources/`.
- [ ] Tài liệu được biên soạn 100% bằng Tiếng Việt chuẩn mực kỹ thuật.
