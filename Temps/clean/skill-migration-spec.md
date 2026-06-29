# 🚀 Đặc tả Nâng cấp & Di trú (Skill Migration & Refactoring Specification)

> [!NOTE]
> Tài liệu này được tách ra từ [Tài liệu Thiết kế Kiến trúc Gốc (architecture-design.md)](architecture-design.md) để quản lý chi tiết về kiến trúc di trú, nâng cấp và giải mã skill (Dual-Mode Pipeline).
>
> **Mục lục điều hướng:**
> - [Quay lại Bản đồ Kiến trúc Trung tâm](architecture-design.md)
> - [Đặc tả State & Shared Layer (Context Bus, Fallback, _state.yaml)](protocols-and-state-spec.md)
> - [Đặc tả Micro-Skill Orchestrator Agent](orchestrator-agent-spec.md)
> - [Ma trận Chốt chặn Chất lượng (Quality Gates Matrix)](quality-gates-matrix.md)

---

### 13.6 Quyết định thiết kế #3: Hỗ trợ Khai thác và Nâng cấp Skill (Dual-Mode Pipeline)
- **Vấn đề:** Ban đầu hệ thống chỉ thiết kế để tạo mới skill từ yêu cầu thô. Khi muốn tối ưu hóa hoặc chuẩn hóa một skill cũ (cả nội bộ và bên ngoài), hệ thống sẽ phải tạo lại từ đầu, gây lãng phí tri thức cũ và tăng nguy cơ ảo giác từ LLM.
- **Giải pháp:** Tích hợp bộ giải mã (Skill Deconstructor) vào Stage 0.5 để đọc cấu trúc nguồn. Miner (Stage 0.7) có nhiệm vụ bóc tách tri thức, ưu điểm và ý chí của skill cũ, đưa vào `domain-handbook.md`. Đối với chế độ `UPDATE`, Architect và Planner chỉ thiết kế phần Delta (chênh lệch) và Builder chỉnh sửa trực tiếp các file tại chỗ (in-place modification).

### 13.7 Quyết định thiết kế #4: Chuyển Token Budget thành Soft Gate / Warning kết hợp Refactor Loop (REV-3.0)
- **Vấn đề:** Ràng buộc Token Budget của `SKILL.md` (ví dụ `<= 700` tokens) nếu bị ép cứng và tự động cắt xén bởi Builder có thể phá hủy các ngữ cảnh nghiệp vụ đặc thù, gây ảo giác lớn cho các LLM vận hành phía sau (ai-loop, ai-poor).
- **Giải pháp:** Tiêu chí Token Budget được chuyển thành **Soft Gate (Warning)**. Builder/Reviewer sẽ không tự động cắt xén file gây mất mát nghiệp vụ. Tuy nhiên, nếu phát hiện cảnh báo vượt budget (hoặc cảnh báo placeholder ở `BUILD-2.1`) trong `build-log.md`, Stage 3.5 Code Reviewer sẽ tự động kích hoạt **subagent Refactor** để tự động dọn dẹp các placeholder hoặc tái cấu trúc nén `SKILL.md` (tách chi tiết sang thư mục `knowledge/`) trước khi bàn giao xuống Sandbox, giải quyết triệt để rác hệ thống một cách tự động.

---

## 14. Khung Kiến trúc Khai thác và Nâng cấp Skill (Skill Migration & Refactoring Subsystem)

### 14.1 Luồng thực thi chi tiết của Dual-Mode

```mermaid
flowchart TD
    INPUT["Đầu vào: Đường dẫn skill cũ + Prompt mục tiêu"] --> L0_Intake["L0: Stage 0.5 SCS Router & Deconstructor"]
    L0_Intake --> Mode_Check{"Phân loại Mode"}
    
    Mode_Check -->|"CREATE (Tạo mới)"| L1_Miner_Std["L1: Miner tiêu chuẩn (Tạo domain-handbook từ tài liệu)"]
    Mode_Check -->|"UPDATE / REBUILD"| L0_Deconstruct["L0: Đọc cấu trúc cũ (nội bộ/external) -> Context Bus"]
    
    L0_Deconstruct --> L1_Miner_Deconstruct["L1: Miner phân tích ý chí, ưu điểm & bóc tách tri thức cũ"]
    L1_Miner_Deconstruct --> L1_Handbook["L1: Tích hợp tri thức cũ vào domain-handbook.md"]
    
    L1_Miner_Std --> L2_Architect["L2: Architect thiết kế design.md"]
    L1_Handbook --> L2_Architect
    
    L2_Architect --> Mode_Check_Builder{"Phân loại Mode"}
    Mode_Check_Builder -->|"UPDATE"| L3_Planner_Delta["L3: Planner lập kế hoạch chỉnh sửa (Delta Task trong todo.md)"]
    Mode_Check_Builder -->|"REBUILD / CREATE"| L3_Planner_Std["L3: Planner lập kế hoạch tạo mới từ đầu"]
    
    L3_Planner_Delta --> L4_Builder_Patch["L4: Builder sửa đổi file tại chỗ (In-place modification)"]
    L3_Planner_Std --> L4_Builder_New["L4: Builder tạo thư mục và file mới từ đầu"]
    
    L4_Builder_Patch --> L4_Review["L4: Code Reviewer & Sandbox (Kiểm thử bảo toàn năng lực)"]
    L4_Builder_New --> L4_Review
    
    L4_Review --> L5_Delivery["L5: Delivery & Cập nhật _state.yaml"]
```

### 14.2 Định nghĩa các Adapter giải mã (Deconstructor Adapters)
- **Internal Skill Adapter:** Khai thác file `SKILL.md` (phần frontmatter và XML tags), nạp nhanh tri thức trong `knowledge/` và checklists của `loop/`.
- **External Skill Adapter:** Đọc toàn bộ mã nguồn (.py, .js, .go), tệp prompts và cấu hình. Sử dụng LLM phân tích mục tiêu thực thi để chuyển đổi thành Metadata và Contracts chuẩn hóa cho hệ sinh thái mới.
