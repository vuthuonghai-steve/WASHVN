Edited architecture-design.md
Edited architecture-design.md
Viewed architecture-design.md:1125-1178

Với mật độ thông tin dày đặc (~1300 dòng và hơn 60KB dữ liệu) của [architecture-design.md](file:///home/stveve/Documents/workspace/build-workflow/Temps/architecture-design.md), việc duy trì toàn bộ trong một file duy nhất sẽ gây ra hai vấn đề lớn:
1.  **Lãng phí Token**: Khi các Agent con (như Builder, Planner, hoặc Orchestrator) làm việc, họ chỉ cần đọc đúng phần đặc tả của mình nhưng bắt buộc phải nuốt toàn bộ Sequence Diagram và ER Diagram, gây hao phí 80-90% token.
2.  **Khó bảo trì**: Bất kỳ cập nhật nhỏ nào ở một Stage cũng dễ làm xê dịch cấu trúc file lớn và tăng nguy cơ xung đột (conflict).

Để quản lý và khai thác hiệu quả nhất, mình đề xuất chia nhỏ tài liệu này thành một **Hệ sinh thái Tri thức Kiến trúc (Architecture Knowledge Sub-system)** với cấu trúc phân rã như sau:

---

### Đề xuất cấu trúc phân rã tài liệu:

#### 1. Core Blueprint (Tập tin Bản đồ Trung tâm): `architecture-design.md` (Giữ lại làm gốc)
*   **Trách nhiệm**: Đóng vai trò là "mục lục và bản đồ định tuyến tổng thể".
*   **Nội dung**:
    *   Tổng quan 5 Layer (Layer Overview).
    *   Sơ đồ Kiến trúc tổng thể (Mermaid Flowchart).
    *   Sơ đồ chuỗi thực thi 2 luồng (Sequence Diagrams).
    *   Sơ đồ Trạng thái (State Diagram).
    *   Liên kết dẫn tới các tập tin đặc tả chi tiết bên dưới.

#### 2. Đặc tả State & Shared Layer: `protocols-and-state-spec.md` (Tạo mới)
*   **Trách nhiệm**: Nguồn tri thức cho các module đọc/ghi dữ liệu hệ thống.
*   **Nội dung**:
    *   [Context Bus Schema & Rules](file:///home/stveve/Documents/workspace/build-workflow/Temps/architecture-design.md#7-context-bus---shared-state-layer).
    *   [_state.yaml State Tracking Schema](file:///home/stveve/Documents/workspace/build-workflow/Temps/architecture-design.md#9-_stateyaml-protocol-chuẩn).
    *   [Cơ chế Rollback & Ma trận Fallback toàn tuyến](file:///home/stveve/Documents/workspace/build-workflow/Temps/architecture-design.md#8-cơ-chế-fallback--rollback-toàn-tuyến) (F1 - F15).

#### 3. Đặc tả Điều phối & Subagents: `orchestrator-agent-spec.md` (Tạo mới)
*   **Trách nhiệm**: Đặc tả dành riêng cho **Micro-Skill Orchestrator** và **Integration Assembler** (Nhánh B).
*   **Nội dung**:
    *   [Micro-Skill Orchestrator Agent YAML Spec](file:///home/stveve/Documents/workspace/build-workflow/Temps/architecture-design.md#6-micro-skill-orchestrator-agent-mới).
    *   Giao thức truyền tin SSP (State & Signal Protocol) và kịch bản chạy song song.

#### 4. Đặc tả Nâng cấp & Di trú: `skill-migration-spec.md` (Tạo mới)
*   **Trách nhiệm**: Đặc tả dành riêng cho luồng **UPDATE** và **REBUILD** skill cũ.
*   **Nội dung**:
    *   Luồng thực thi Dual-Mode chi tiết (Mục 14).
    *   Định nghĩa Internal & External Deconstructor Adapters.
    *   Nguyên tắc Soft Gate cho Token Budget.

#### 5. Ma trận Kiểm định Chất lượng: `quality-gates-matrix.md` (Tạo mới)
*   **Trách nhiệm**: Chỉ dành cho **Spec Gatekeeper**, **Drift Detector** và **Code Reviewer** kiểm tra đầu ra.
*   **Nội dung**:
    *   [Ma trận Quality Gates tổng thể](file:///home/stveve/Documents/workspace/build-workflow/Temps/architecture-design.md#12-ma-trận-chốt-chặn-chất-lượng-quality-gates-matrix).
    *   Quy định cụ thể của từng Gate nhị phân.

---

### Lợi ích khi phân rã:
*   **Tối ưu hóa Context**: Ví dụ, khi Agent Builder chạy ở L4, nó chỉ cần nạp file `protocols-and-state-spec.md` để biết cách viết trạng thái, không cần đọc sơ đồ Sequence Diagram ở L1.
*   **Clean Code & Clean Docs**: Giúp các Agent dễ dàng định vị lỗi hoặc cập nhật tài liệu khi có drift phát sinh mà không ảnh hưởng đến phần khác.

Bạn thấy phương án phân rã này thế nào? Mình có nên tiến hành thực hiện tách file và cập nhật các liên kết dẫn chéo (cross-linking) giữa chúng luôn không?