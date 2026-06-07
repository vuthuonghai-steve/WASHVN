# Tiêu Chuẩn Khảo Sát Nghiệp Vụ Nghiệp Vụ (Exploration Standards)

> **Mã số**: STG0-KNOW-01
> **Vai trò**: Xác định các tiêu chí định lượng và thực hành tốt nhất cho việc đánh giá chất lượng Agent Skills.

---

## 1. Bản Đặc Tả 7 Tiêu Chuẩn Vàng

### A. Khả năng tái sử dụng (Reusability)
- **Tiêu chuẩn**: Không được mã hóa cứng các bối cảnh, đường dẫn cục bộ, hoặc logic nghiệp vụ rườm rà. Skill chỉ đóng vai trò là "chương trình điều khiển hành vi", còn dữ liệu tĩnh phải nằm ngoài.
- **Tiêu chí đánh giá**:
  - `Rich (Đạt)`: Skill thiết kế các file tri thức độc lập tại `knowledge/` để nạp động, cho phép áp dụng cho nhiều tệp dữ liệu khác nhau.
  - `Thin (Mơ hồ)`: Skill chỉ giải quyết một case hẹp và cụ thể (Ví dụ: "Viết kịch bản kiểm tra cho hàm checkout.ts" thay vì "Quy chuẩn viết unit test chung cho dự án").

### B. Khả năng kết hợp (Composability)
- **Tiêu chuẩn**: Kỹ năng phải có Input/Output Contract rõ ràng, tương tác mượt mà thông qua thư mục `.skill-context/` làm kho lưu trữ trạng thái.
- **Quy tắc giải quyết xung đột**:
  - Khi hai kỹ năng có hướng dẫn mâu thuẫn (Ví dụ: Một bên yêu cầu cài đặt mọi gói để test nhanh, một bên yêu cầu bảo mật nghiêm ngặt chặn cài đặt), Agent bắt buộc phải thiết lập **Cơ chế Phân cấp quyền ưu tiên (Prompt Hierarchy)** trong `SKILL.md` để xác định rõ kỹ năng nào giữ vai trò neo chính.

### C. Khả năng bảo trì (Maintainability - Goldilocks Prompting Zone)
- **Tiêu chuẩn**: Prompt của skill phải ở trong vùng "Goldilocks" - không quá dài để tránh tốn token và nhiễu ngữ cảnh, không quá ngắn dẫn đến thiếu logic chỉ dẫn.
- **Cấu trúc 4 lớp tri thức**:
  - `L0`: Core Constitution (`SKILL.md` dưới 1800 tokens).
  - `L1`: Operating Policies (`policy/*.md`).
  - `L2`: Domain Knowledge (`knowledge/*.md`).
  - `L3`: Contextual examples (`examples/*.md`, `specs/`).

### D. Độ an toàn và bảo mật (Security)
- Xem chi tiết tại `knowledge/security-standards.md`.
- **Ranh giới an toàn**: Chống Prompt Injection thông qua thẻ XML bọc dữ liệu và Structured tool calling; chạy sandbox biệt lập cho scripts.

### E. Hiệu suất ngữ cảnh (Context Efficiency)
- **Tiêu chuẩn**: Áp dụng triệt để mô hình **Bộc lộ lũy tiến (Progressive Disclosure)**:
  - Chỉ nạp các tệp tin cấu hình neo cứng lúc boot (Tier 1).
  - Chỉ nạp tri thức domain nghiệp vụ khi thực hiện phase cụ thể (Tier 2).
  - Chỉ nạp ví dụ chi tiết lúc chuẩn bị ghi file (Tier 3).

### F. Tính di động (Portability)
- **Tiêu chuẩn**: Không được trói buộc ngầm vào API đặc thù của một mô hình cụ thể, ngoại trừ các trường hợp bắt buộc (như cấu trúc gọi công cụ riêng của hệ thống). Hướng tới viết prompt độc lập, dùng ngôn ngữ tự nhiên chuẩn hóa.

### G. Khả năng phục hồi và dự phòng (Reliability & Fallback)
- **Tiêu chuẩn**: Khi hệ thống xảy ra lỗi (API sập, sai định dạng đầu vào), Agent không được phép đoán mò (hallucinate).
- **Hành vi bắt buộc**:
  - Ghi nhận nhật ký (execution logging) các bước thực hiện.
  - Kích hoạt phương án dự phòng (fallback) hoặc kích hoạt kênh Human-in-the-loop (HITL) thông qua các Stop Conditions để hỏi ý kiến người dùng.

---

## 2. Chuẩn đánh giá chất lượng tài nguyên (Rich vs Thin Resources)

| Chỉ số đánh giá | Trạng thái Sơ sài (Thin) | Trạng thái Đầy đủ (Rich) |
|-----------------|--------------------------|--------------------------|
| **Độ phủ Tri thức** | Thiếu tài liệu nghiệp vụ cơ bản, chỉ có mô tả ngắn bằng 1-2 câu thô sơ. | Có đầy đủ các file tri thức domain nghiệp vụ cụ thể nằm trong thư mục `resources/`. |
| **Mẫu mã và Schema** | Không có tệp code ví dụ thực tế hoặc API schema cấu trúc. | Có file code mẫu thực tế thu thập từ codebase và đặc tả API schema chi tiết. |
| **Ranh giới Bảo mật** | Không phân tách dữ liệu thô và chỉ dẫn, prompt ghép chuỗi tự do. | Phân định rõ XML boundaries cho mọi file thô, có luật chống Prompt Injection rõ ràng. |
| **Sẵn sàng cho Builder** | Planner bắt buộc phải sinh thêm Phase 0 để viết tài nguyên bổ trợ. | Builder có thể trực tiếp triển khai code mà không cần hỏi lại nghiệp vụ. |

---

## 3. Quy chuẩn đánh giá Quy mô & Định hướng Micro-Skills

Khi quy mô nghiệp vụ hoặc quy trình của kỹ năng đích quá lớn, việc thiết kế thành một kỹ năng duy nhất sẽ làm giảm đáng kể tính an toàn, bảo trì và tin cậy của AI Agent. Explorer bắt buộc phải thực hiện đánh giá quy mô định lượng và đề xuất phương án phân rã.

### A. Bộ chỉ số và Ngưỡng đánh giá Quy mô (Complexity Score Table)

Sử dụng thang đo định lượng dưới đây để tính toán **Điểm Phức tạp của Kỹ năng (Skill Complexity Score - SCS)**:

| Tiêu chí | Ngưỡng định lượng | Trọng số điểm | Điểm SCS |
|----------|-------------------|---------------|----------|
| **Số bước quy trình** | • ≤ 3 bước: 1 điểm<br/>• 4 - 5 bước: 3 điểm<br/>• > 5 bước: **5 điểm (Phải phân rã)** | 30% | |
| **Số công cụ / API tương tác** | • ≤ 2 công cụ: 1 điểm<br/>• 3 - 4 công cụ: 3 điểm<br/>• > 4 công cụ: **5 điểm (Phải phân rã)** | 30% | |
| **Kích thước chỉ dẫn SKILL.md dự kiến** | • < 800 tokens: 1 điểm<br/>• 800 - 1500 tokens: 3 điểm<br/>• > 1500 tokens: **5 điểm (Phải phân rã)** | 20% | |
| **Độ nhạy cảm an ninh (Security Risk)** | • Không chạy scripts/shell: 1 điểm<br/>• Chạy scripts đọc/quét: 3 điểm<br/>• Chạy scripts ghi/biên dịch hoặc gọi API bên thứ ba không tin cậy: **5 điểm (Phải phân rã)** | 20% | |

*   **Luật Neo cứng**:
    *   Nếu **Điểm trung bình SCS > 3.0** HOẶC **có bất kỳ tiêu chí nào đạt 5 điểm (ngưỡng đỏ)**: Explorer Agent bắt buộc phải **phủ quyết giải pháp Monolithic** và đề xuất **Hệ thống Micro-skills phối hợp**.

### B. Các mẫu thiết kế phối hợp Micro-skills (Orchestration Design Patterns)

Khi phân rã kỹ năng, AI phải định hình luồng phối hợp theo các mẫu chuẩn sau:

1.  **Sequential Pipeline (Chuỗi tuần tự)**:
    - *Mô tả*: Đầu ra của Micro-skill A là đầu vào trực tiếp của Micro-skill B.
    - *Giao thức giao tiếp*: Ghi dữ liệu trạng thái dưới dạng tệp tin YAML/JSON cục bộ tại `.skill-context/` (Ví dụ: `A.md` $\rightarrow$ `B.md`).
2.  **Condition Router (Phân nhánh rẽ hướng)**:
    - *Mô tả*: Một Micro-skill trung tâm phân tích kết quả đầu ra và điều hướng sang các Micro-skills chuyên biệt khác dựa trên điều kiện thực tế.
3.  **Meta-Orchestrator (Điều phối trung tâm)**:
    - *Mô tả*: Sử dụng một Micro-skill chính đóng vai trò "nhạc trưởng" gọi và quản lý vòng đời của các Micro-skills phụ thuộc thông qua Subagent calls.

