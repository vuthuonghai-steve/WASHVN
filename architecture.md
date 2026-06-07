# 🏛️ MASTER SKILL SUITE ARCHITECTURE (VER_3.0.0)
## Hệ thống Phân rã Vật lý (Orchestrated Physical Micro-skills) & 8-Stage Quality Gated Pipeline

Tài liệu này định hình kiến trúc nâng cấp toàn diện cho bộ **Master Skill Suite** lên **Ver_3.0.0 (Production-Ready)**, tuân thủ nghiêm ngặt chỉ thị của Steve về việc **phân rã vật lý hoàn toàn (Physical Micro-skills)**, thiết lập các chốt chặn chất lượng chống AI-Slop / AI-Poor, và đảm bảo tính liên kết tự phục hồi qua giao thức SSP.

> **Cập nhật 2026-06-07**: Đã audit & đồng bộ toàn bộ `raw/ver-3/`. 11 skill sources deployed, 0 broken references. `karpathy-standards.md` integrated vào `_shared/knowledge/`. Xem `docs/context-to-work/architecture-sync/scope.2026-06-07.md`.

---

## 1. 🔄 CHUỖI CUNG ỨNG KỸ NĂNG 8 GIAI ĐOẠN (8-STAGE PIPELINE)

Để triệt tiêu tình trạng phát triển qua loa, thiếu kiểm định, hệ thống quy chuẩn luồng phát triển bắt buộc phải đi qua **8 giai đoạn** độc lập với các chốt chặn tự động (Quality Gates):

```mermaid
flowchart TD
    subgraph ContextLedger ["SỔ CÁI BỐI CẢNH (.skill-context/{skill-name}/)"]
        E[exploration.md - Khảo sát]
        C[criteria.md - Tiêu chí test]
        D[design.md - Bản vẽ 7 Zones]
        QM[quality-matrix.yaml - Chốt thiết kế]
        T[todo.md - Kế hoạch DAG]
        CR[review-report.md - Đánh giá code]
        V[verification.md - Kết quả Sandbox]
    end

    S0[Stage 0: Explorer] -->|Tạo ra| E & C
    E & C --> S1[Stage 1: Architect]
    
    S1 -->|Tạo ra design.md| D
    D --> S1_5[Stage 1.5: Quality Gatekeeper]
    
    S1_5 -->|Thẩm định chất lượng| QM
    QM & D & C --> S2[Stage 2: Planner]
    
    S2 -->|Tạo todo.md dạng DAG| T
    T & QM & D --> S3[Stage 3: Builder]
    
    S3 -->|Build code thực tế| Src[Runtime Physical Skills]
    Src --> S3_5[Stage 3.5: Google Code Reviewer]
    
    S3_5 -->|Phân tích tĩnh code| CR
    CR & Src & C --> S4[Stage 4: Sandbox Tester]
    
    S4 -->|Chạy test trong Docker/gVisor| V
    V --> S5[Stage 5: Indexer]
    S5 -->|Đăng ký chỉ mục| Done([llms.txt & README.md])
    
    %% Vòng lặp phản hồi tự cứu hộ (CASE System)
    V -->|FAIL / Thấp hơn 85% điểm| Rollback[CASE Rollback Trigger]
    Rollback -->|Tạo rollback_request.yaml| S1
```

---

## 2. 📦 CƠ CHẾ PHÂN RÃ VẬT LÝ HOÀN TOÀN (PHYSICAL MICRO-SKILLS)

Khi một Kỹ năng được khảo sát có độ phức tạp **SCS > 3.0**, nó bắt buộc phải được tách thành các **Micro-skills vật lý độc lập** tại runtime cài đặt (`.agents/skills/`).

### Ví dụ: Physical Micro-skill Decomposition

Khi một kỹ năng có SCS > 3.0 được phát triển trong tương lai, nó sẽ được phân rã theo mô hình:
1.  **`{skill-name}-{sub-module-1}` (Core logic):** Xử lý nghiệp vụ chính $\rightarrow$ Ghi state JSON.
2.  **`{skill-name}-{sub-module-2}` (Knowledge retrieval):** Tra cứu tri thức chuyên ngành.
3.  **`{skill-name}-{sub-module-3}` (Synthesis):** Tổng hợp & luận giải.
4.  **`{skill-name}-{sub-module-4}` (Action planner):** Lập kế hoạch hành động.
5.  **`{skill-name}-adviser` (Master Orchestrator):** Kỹ năng nhạc trưởng điều phối toàn luồng.

> [!NOTE]
> Hiện tại `raw/ver-3/` chưa có micro-skill cluster nào được phân rã vật lý. Các skill hiện tại đều là monolithic skills phù hợp với SCS < 3.0. Khi có skill phức tạp mới, mô hình này sẽ được áp dụng.

---

## 3. 🛡️ CHỐT CHẶN CHẤT LƯỢNG NGĂN NGỪA AI-SLOP (QUALITY GATES)

### 🔴 Chốt 1: Stage 1.5 - Thẩm định Thiết kế (Quality Gatekeeper)
*   **Mục tiêu:** Ngăn chặn Builder nhận bản vẽ lỗi, thiếu file, đặt tên file chung chung (placeholders như `utils.py`, `script_new.sh`).
*   **Cách thức:** `production-quality-gatekeeper` chạy script `loop_refiner.py` chấm điểm `design.md`. Chỉ khi đạt **100% tiêu chuẩn thiết kế** mới tạo ra file chữ ký số `quality-matrix.yaml` để cho phép `skill-planner` chạy.

### 🔴 Chốt 2: Stage 3.5 - Google Code Reviewer
*   **Mục tiêu:** Loại bỏ hoàn toàn mã nguồn kém chất lượng, lạm dụng comment, thiếu xử lý lỗi hoặc chứa placeholder (`// TODO`, `pass`).
*   **Cách thức:** `production-code-reviewer` chạy trình phân tích tĩnh `code_auditor.py` kiểm định cú pháp, cyclomatic complexity và docstring. Nếu phát hiện bất kỳ lỗi `Must Fix` nào, nó sẽ từ chối ký file `review-report.md`, buộc Builder phải tái cấu trúc mã nguồn.

### 🔴 Chốt 3: Stage 4 - Sandbox Tester
*   **Mục tiêu:** Đảm bảo code hoạt động thực tế 100% trong môi trường Docker sandbox cô lập, không gây lỗi hệ thống host.
*   **Cách thức:** Thực thi tối thiểu 2 kịch bản kiểm thử ghi nhận trong `criteria.md`. Nếu kết quả sai lệch hoặc phát hiện mật độ placeholder > 0, nó sẽ tự động kích hoạt **CASE Rollback** trả bối cảnh về Stage 1.

---

## 4. 📝 PHÂN BỔ BỐI CẢNH PROGRESSIVE DISCLOSURE (TOKEN ECONOMICS)

Để hỗ trợ load 5 Kỹ năng vật lý độc lập mà không gây quá tải Token budget của Agent, chúng ta áp dụng chính sách Progressive Disclosure nghiêm ngặt:

```yaml
progressive_disclosure_policy:
  skill-orchestrator:
    load_always: ["SKILL.md", "scripts/orchestrate.py"]
    load_on_demand: ["state/report.md"]
    token_budget: 400
  skill-sub-module-1:
    load_always: ["SKILL.md", "data/config.yaml"]
    token_budget: 350
  skill-sub-module-2:
    load_always: ["SKILL.md", "scripts/core.py"]
    token_budget: 350
  skill-sub-module-3:
    load_always: ["SKILL.md", "knowledge/domain-rules.md"]
    token_budget: 450
```

---

## 5. 🛠️ QUY TRÌNH TỰ PHỤC HỒI & CASE RECOVERY

Khi một Stage trong 8 giai đoạn phát hiện lỗi, nó bắt buộc phải tuân thủ giao thức **CASE System**:
1.  **Phát hiện (Detect):** Nếu validator trả trạng thái `FAIL` hoặc điểm chất lượng < 85%.
2.  **Khóa & Cảnh báo (Log-Notify-Stop):** Ghi nhận lỗi chi tiết vào `.skill-context/{skill-name}/rollback_request.yaml`.
3.  **Tự phục hồi (Recover):** Agent quay ngược bối cảnh về giai đoạn chịu trách nhiệm trước đó (ví dụ: Lỗi logic code quay về Architect/Planner), không cho phép tiếp tục triển khai các tác vụ lỗi.

---

## 6. DYNAMIC PIPELINE & ADAPTIVE COMPOSITION (TÍNH LINH ĐỘNG ĐỘNG)

Để đảm bảo bộ **Master Skill Suite** luôn giữ được tính linh động cao nhất, không bị rơi vào bẫy "quá tải cấu trúc" (Over-engineering) khi xử lý các kỹ năng từ đơn giản đến cực kỳ phức tạp, hệ thống tích hợp **Cơ chế Thích ứng Động (Adaptive Engine)**:

### ⚡ A. Công tắc Phân luồng Độ Phức Tạp (Dynamic SCS Mode Switcher)
Hệ thống sẽ không ép buộc mọi kỹ năng phải đi qua đầy đủ 8 giai đoạn phân rã vật lý. Thay vào đó, điểm **SCS (Skill Complexity Score)** được tính ở Stage 0 sẽ tự động điều khiển luồng đi (Mode Switcher):

| Ngưỡng SCS | Chế độ Hoạt động | Mô tả Luồng đi |
| :--- | :--- | :--- |
| **SCS < 3.0** *(Đơn giản)* | **Fast-Track Mode** (Đơn khối) | Gộp gọn Stage 1.5/3.5 làm pre-check nội bộ. Build duy nhất 1 skill monolithic cực kỳ nhanh gọn để tiết kiệm token và thời gian. |
| **SCS >= 3.0** *(Phức tạp)* | **Full-Track OMSP** (Phân rã Vật lý) | Kích hoạt luồng 8-Stage hoàn chỉnh. Bắt buộc phân rã Micro-skills vật lý độc lập và chạy kiểm thử Sandbox nghiêm ngặt. |

### ⚙️ B. Nạp Cấu Hình Lớp Phủ Động (Dynamic Configuration Overlay)
Tất cả các Stage Skills trong bộ suite tuyệt đối không được fix cứng (hardcode) đường dẫn cài đặt, tên thư mục, hay các biến môi trường của hệ thống.
*   Mỗi Agent khi boot lên sẽ đọc tệp cấu hình động chung tại `.skill-context/suite_config.yaml` (hoặc `CLAUDE.md`).
*   Tệp cấu hình này sẽ tự động cung cấp các thông tin môi trường thời thực (Real-time overlay): Hệ điều hành của host, đường dẫn cài đặt đích của runtime (`.hermes/skills/` hoặc `.agents/skills/`), và các cờ tối ưu hóa (ví dụ: `enable_docker_sandbox: true/false`).
*   Điều này giúp **Antigravity, Hermes, hay Claude Code** khi tiếp quản dự án đều có thể thích ứng ngay lập tức mà không gây đứt gãy logic hệ thống.

---

**Trạng thái kiến trúc:** Đã được Steve phê duyệt đi theo **Phương án 2 (Physical Micro-skills)**. Bộ suite master Ver_3.0.0 chính thức có hiệu lực làm kim chỉ nam phát triển!

> ✅ **Audit 2026-06-07**: 11 skills deployed tại `raw/ver-3/`. 0 broken references. Toàn bộ sync với `.agents/skills/`. Workspace routing map (`workspce_tree.md`) đã được tạo. `karpathy-standards.md` integrated vào `_shared/knowledge/`.