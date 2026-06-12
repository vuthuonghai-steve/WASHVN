# 🤖 Prompt Engineering & LLM Output Quality Standards (LLM Eval Domain)

> **Mục tiêu**: Định nghĩa các tiêu chuẩn kỹ thuật chuyên sâu dùng để đặt ra và đánh giá chất lượng sản phẩm đầu ra khi làm việc với AI Agent hoặc thiết kế prompt hệ thống.
> **Phân nhóm**: 3 Tầng Chất lượng (Three-Layer Matrix)

---

## Tầng 1: Kiến trúc & Định hướng (Foundation & Rule Enforcement)

*   **[LLM-1.1] Absolute Rule Enforcement (Tính tuân thủ tuyệt đối)**:
    *   *Tiêu chí*: Prompt phải định hướng hành vi của mô hình không thể bị lung lay bởi ngữ cảnh động. Tất cả các luật bắt buộc phải bọc trong khối `<instructions>` và sử dụng các từ ngữ mang tính mệnh lệnh tuyệt đối (`must`, `must_not`).
*   **[LLM-1.2] XML Boundary Isolation (Ranh giới cách ly dữ liệu)**:
    *   *Tiêu chí*: Dữ liệu thô từ bên ngoài (raw inputs, user text) bắt buộc phải được bọc trong các thẻ XML riêng biệt như `<input>` để ngăn cách ly hoàn toàn với khối lệnh chỉ thị, tránh nguy cơ thoát sandbox.
*   **[LLM-1.3] Structured Output Contracts (Hợp đồng định dạng đầu ra)**:
    *   *Tiêu chí*: Cuối prompt bắt buộc phải khai báo khối `<output_contract>` quy định rõ cấu trúc đầu ra (YAML, JSON hoặc Markdown phân cấp). Cấm mô hình đưa ra các lời thoại mở đầu/kết thúc thừa thãi ngoài hợp đồng.

---

## Tầng 2: Vận hành & Hiệu năng ngữ cảnh (Operational & Token Economics)

*   **[LLM-2.1] Token Economics (Tối ưu hóa dung lượng token)**:
    *   *Tiêu chí*: Prompt phải được viết cực kỳ cô đọng, loại bỏ các từ ngữ mô tả hoa mỹ hoặc lặp ý vô ích. Tránh lãng phí context window của mô hình.
*   **[LLM-2.2] Progressive Disclosure (Tiết lộ lũy tiến)**:
    *   *Tiêu chí*: Chia nhỏ tài nguyên prompt thành 3 Tiers (Tier 1: Mandatory, Tier 2: Conditional, Tier 3: On-Demand). Prompt chính chỉ chứa Tier 1, các Tier còn lại chỉ được gọi thông qua trigger khi ngữ cảnh yêu cầu.
*   **[LLM-2.3] Anti-Hallucination Measures (Chống ảo tưởng kiến thức)**:
    *   *Tiêu chí*: Tích hợp cơ chế Traceability (Truy vết nguồn gốc). Yêu cầu mô hình gắn Trace Tag dạng `[TỪ NGŨ CẢNH §N]` cho mọi thông tin quan trọng được đưa ra, cấm mô hình tự suy đoán kiến thức nằm ngoài resources được nạp.

---

## Tầng 3: Tinh tế & Bảo mật nâng cao (Sophistication & Safety)

*   **[LLM-3.1] System Prompt Leakage Prevention (Chống rò rỉ prompt gốc)**:
    *   *Tiêu chí*: Thiết lập các lớp phòng thủ nghiêm ngặt chống lại các yêu cầu truy vấn lén lút như "ignore previous instructions", "tell me your system prompt", hoặc các yêu cầu dịch thuật/tóm tắt trá hình nhằm lấy cắp mã nguồn prompt.
*   **[LLM-3.2] Jailbreak & Prompt Injection Defense (Chống phá rào nâng cao)**:
    *   *Tiêu chí*: Tích hợp bộ lọc đầu vào nhạy cảm (sanitizers) và thiết lập luật tự động phát hiện mã lệnh độc hại hoặc các ký tự điều khiển định dạng lạ trong thẻ `<input>`.
*   **[LLM-3.3] Self-Verification Loop (Cơ chế tự kiểm định)**:
    *   *Tiêu chí*: Prompt hệ thống phải chỉ thị mô hình dành riêng các turn suy nghĩ ngầm (Thinking Block `<thought>`) để tự rà soát lại đầu ra của mình đối chiếu với các ràng buộc trong `<instructions>` trước khi xuất kết quả cuối cùng.
 Josephson.
