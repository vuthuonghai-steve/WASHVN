# 🏛️ MASTER SKILL SUITE ARCHITECTURE (VER_3.0.0)
## Hệ thống 5-Layer Pipeline, Phân rã Vật lý & Tự Phục Hồi

Tài liệu này định hình kiến trúc cho bộ **Master Skill Suite** phiên bản **Ver_3.0.0 (Production-Ready)** sử dụng **Mô hình 5-Layer Gated Pipeline**, hỗ trợ phân rã vật lý hoàn toàn (**Physical Micro-skills**) cho các tác vụ phức tạp, thiết lập chốt chặn chất lượng và cơ chế tự phục hồi tự động qua hệ thống **Context Bus** và **CASE Recovery**.

---

### 1. 🔄 TỔNG QUAN KIẾN TRÚC 5 LAYER (5-LAYER PIPELINE ARCHITECTURE)

Hệ thống được tổ chức thành **5 lớp chức năng (Layers)** độc lập từ khâu tiếp nhận yêu cầu cho đến khâu phân phối kỹ năng hoàn thiện:

| Layer | Tên Layer | Nhiệm vụ chính | Các Component chịu trách nhiệm |
|:---|:---|:---|:---|
| **L0** | Intake & Routing | Tiếp nhận yêu cầu thô từ người dùng, khơi gợi nghiệp vụ (BA Elicitation), đánh giá độ phức tạp (SCS) và điều phối nhánh thực thi thích hợp. | [BA Elicitor](file:///home/stveve/Documents/workspace/build-workflow/WASHVN/.agents/skills/ba-elicitor/SKILL.md), SCS Router |
| **L1** | Knowledge Foundation | Khai thác tri thức hiện hữu từ codebase, tài liệu và các skill cũ để xây dựng Cẩm nang Tri thức Dự án (Domain Handbook). | Miner Analyzer |
| **L2** | Design & Contract | Thiết kế kiến trúc tĩnh cho Skill dưới dạng bản vẽ 7 Zones, định rõ các hợp đồng dữ liệu (Data Contracts) và neo ngữ nghĩa (Semantic Anchors). | Architect, Spec Gatekeeper |
| **L3** | Planning & Verification | Nạp đầy đủ ngữ cảnh (Hydration), lập kế hoạch thực thi dạng đồ thị định hướng không chu trình (DAG) và kiểm tra độ lệch thiết kế (Drift Detection). | Context Hydrator, Planner, Drift Detector |
| **L4** | Implementation & Delivery | Triển khai mã nguồn (đơn khối hoặc song song), đánh giá chất lượng mã nguồn (Google Code Reviewer), kiểm thử sandbox cô lập và phân phối kỹ năng. | Builder / Orchestrator, Reviewer, Sandbox Tester |

#### 📊 Sơ đồ Dòng Chảy Pipeline (Pipeline Flowchart)
```mermaid
flowchart TB
    subgraph L0["🔬 LAYER 0: INTAKE & ROUTING"]
        direction TB
        S0["Stage 0<br/>BA Elicitor"]
        S05["Stage 0.5<br/>SCS Router + Domain Anchoring"]
        S0 --> S05
    end
    subgraph L1["📚 LAYER 1: KNOWLEDGE FOUNDATION"]
        direction TB
        S07["Stage 0.7<br/>Miner"]
    end
    subgraph L2["📐 LAYER 2: DESIGN & CONTRACT"]
        direction TB
        S1["Stage 1<br/>Architect"]
        S15["Stage 1.5<br/>Spec Gatekeeper"]
        S1 --> S15
    end
    subgraph L3["🧭 LAYER 3: PLANNING & VERIFICATION"]
        direction TB
        S17["Stage 1.7<br/>Context Hydrator"]
        S2["Stage 2<br/>Planner"]
        S25["Stage 2.5<br/>Drift Detector + Plan Quality Gate"]
        S17 --> S2 --> S25
    end
    subgraph L4["⚙️ LAYER 4: IMPLEMENTATION & DELIVERY"]
        direction TB
        ROUTE{"SCS Router<br/>Decision Point"}
        subgraph BRANCH_A["🟢 BRANCH A: Single Skill (SCS < 3.0)"]
            S3A["Stage 3<br/>Builder"]
            S35A["Stage 3.5<br/>Code Reviewer"]
            S3A --> S35A
        end
        subgraph BRANCH_B["🔴 BRANCH B: Micro-Skill Bundle (SCS >= 3.0)"]
            S3B0["Stage 3a<br/>Micro-Skill Orchestrator"]
            S3B1["Stage 3b<br/>Parallel Builders"]
            S3B2["Stage 3c<br/>Integration Assembler"]
            S35B["Stage 3.5<br/>Reviewer + Integration Tester"]
            S3B0 --> S3B1 --> S3B2 --> S35B
        end
        ROUTE -->|"SCS < 3.0"| BRANCH_A
        ROUTE -->|"SCS >= 3.0"| BRANCH_B
        S4["Stage 4<br/>Sandbox Validation"]
        S5["Stage 5<br/>Delivery"]
        S35A --> S4
        S35B --> S4
        S4 --> S5
    end
    CB[("🗂️ CONTEXT BUS<br/>Shared State Layer")]
    L0 --> L1 --> L2 --> L3 --> ROUTE
    L0 -.->|"ghi glossary, NFR"| CB
    L1 -.->|"ghi domain-handbook"| CB
    L2 -.->|"ghi design.md, contracts"| CB
    L3 -.->|"ghi todo.md"| CB
    L4 -.->|"ghi build-log, verification"| CB
    S25 -.->|"drift detected"| S2
    S25 -.->|"design invalid"| S1
    S15 -.->|"criteria fail"| S1
    S05 -.->|"thiếu thông tin"| S0
    S35A -.->|"review fail"| S3A
    S35B -.->|"integration fail"| S3B2
    S4 -.->|"sandbox fail"| S3A
    S4 -.->|"sandbox fail"| S3B2
    style CB fill:#fff3cd,stroke:#ffc107,stroke-width:3px
    style ROUTE fill:#d1ecf1,stroke:#0dcaf0,stroke-width:2px
    style S17 fill:#fff3cd,stroke:#ffc107,stroke-width:2px
    style S25 fill:#fff3cd,stroke:#ffc107,stroke-width:2px
    style S3B0 fill:#f8d7da,stroke:#dc3545,stroke-width:2px
```



---

### 2. 🚦 CƠ CHẾ PHÂN LUỒNG: 2 BRANCHES & CHỈ SỐ SCS (SKILL COMPLEXITY SCORE)

Để tối ưu chi phí token và thời gian thực thi, hệ thống sử dụng điểm **SCS (Skill Complexity Score)** được tính toán tại Layer 0 để tự động rẽ nhánh tại Layer 4:

*   **Branch A (Fast-Track Mode | SCS < 3.0):** Dành cho các kỹ năng đơn giản, nén các bước Gatekeeper/Reviewer thành self-applied checklist, xây dựng duy nhất một file kỹ năng monolithic nhanh gọn.
*   **Branch B (Full-Track OMSP | SCS >= 3.0):** Dành cho các hệ thống phức tạp, bắt buộc phân rã thành một bó kỹ năng vật lý (**Micro-Skill Bundle**) giao tiếp thông qua giao thức **SSP (Shared State Protocol)**. Một Orchestrator sẽ điều phối hoạt động song song của các Builder trước khi Integration Assembler tích hợp lại.

#### ⏱️ Sơ đồ Tuần tự của Branch B (Branch B Sequence)
```mermaid
sequenceDiagram
    participant U as User
    participant CB as Context Bus
    participant PL as Planner
    participant DD as Drift Detector
    participant OR as Orchestrator
    participant B1 as Builder 1
    participant B2 as Builder 2
    participant B3 as Builder 3
    participant IA as Integration Assembler
    participant RV as Reviewer
    participant SB as Sandbox

    Note over PL: Planner đã nhận hydrated-context
    PL->>CB: Ghi todo.md + orchestration-plan.md
    PL->>DD: Trigger Stage 2.5
    DD->>CB: Đọc todo.md + design.md + orchestration-plan
    DD->>DD: Drift detection (SSP contract check)
    DD->>CB: Ghi plan-verification-report.md (Pass)
    DD->>OR: Trigger Stage 3a (Branch B)
    
    OR->>CB: Đọc orchestration-plan + hydrated-context
    OR->>OR: Phân rã 3 micro-tasks + SSP contracts
    par Spawn song song
        OR->>B1: Micro-task: OTP validation
        OR->>B2: Micro-task: Payment gateway
        OR->>B3: Micro-task: Webhook handler
    end
    par Build song song
        B1->>B1: 5 Phase (partitioned context)
        B2->>B2: 5 Phase (partitioned context)
        B3->>B3: 5 Phase (partitioned context)
    end
    B1-->>OR: OUTPUT_READY (OTP_VALIDATED)
    B2-->>OR: OUTPUT_READY (PAYMENT_COMPLETED)
    B3-->>OR: OUTPUT_READY (WEBHOOK_HANDLED)
    
    OR->>OR: Validate SSP contracts
    OR->>IA: Handoff 3 micro-skills + SSP map
    IA->>IA: Merge + sinh orchestrate.py
    IA->>IA: Run integration test
    IA->>CB: Ghi micro-skill-bundle/ + integration-test-report.md
    IA->>RV: Trigger Stage 3.5
    
    RV->>CB: Đọc micro-skill-bundle
    RV->>RV: Review từng micro-skill
    RV->>CB: Ghi review-report.md (Pass)
    RV->>SB: Trigger Stage 4
    SB->>SB: Sandbox test (orchestrate.py included)
    SB->>CB: Ghi verification.md (Pass)
    SB->>U: Delivery - build-completed
```

---

### 3. 🛠️ 3 CHẾ ĐỘ THI CÔNG (CREATE / UPDATE / REBUILD)

Hệ thống hỗ trợ 3 chế độ thi hành độc lập dựa trên thực trạng của Kỹ năng đầu vào:

| Chế độ | Điều kiện áp dụng | Mô hình hoạt động | Cơ chế Builder |
|:---|:---|:---|:---|
| **CREATE** | Tạo kỹ năng hoàn toàn mới, chưa từng tồn tại trong hệ thống. | Pipeline đi từ đầu: Elicitor $\rightarrow$ Miner $\rightarrow$ Architect $\rightarrow$ Planner $\rightarrow$ Builder. | Builder tạo mới thư mục và toàn bộ cấu trúc file từ đầu. |
| **UPDATE** | Nâng cấp hoặc sửa đổi một Kỹ năng chuẩn WASHVN đang có. | **Deconstructor** phân tích mã nguồn và bối cảnh cũ $\rightarrow$ **Miner** bóc tách tri thức và ý chí cũ $\rightarrow$ **Architect** lập bản vẽ delta $\rightarrow$ **Planner** lập delta-tasks $\rightarrow$ **Builder** vá lỗi tại chỗ. | Builder chỉnh sửa trực tiếp trên file hiện hữu (**In-place Modification/Patching**), bảo toàn logic cũ. |
| **REBUILD** | Tái cấu trúc một kỹ năng phi tiêu chuẩn (External/Legacy). | **Deconstructor** đọc cấu trúc ngoài $\rightarrow$ **Miner** chuyển đổi thành siêu dữ liệu (metadata) $\rightarrow$ **Architect** tái thiết kế toàn bộ $\rightarrow$ **Planner** lập kế hoạch chuẩn $\rightarrow$ **Builder** tạo mới. | Builder tạo mới thư mục và file dựa trên cấu trúc đã chuẩn hóa mới. |

#### 🗺️ Sơ đồ Dòng Chảy Chế Độ Kép (Dual-Mode Flow)
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

---

### 4. 🗂️ SỔ CÁI BỐI CẢNH & HỆ THỐNG CONTEXT BUS

Để triệt tiêu tình trạng trôi ngữ cảnh (Context Drift) và đảm bảo nguyên tắc **Single Source of Truth (SSoT)**, hệ thống giao tiếp thông qua **Context Bus** được quản lý tại thư mục trạng thái của kỹ năng: `.skill-context/{skill-name}/`.

#### 📌 Quy tắc Vận hành Context Bus (Rules R1-R8)
```mermaid
graph TD
    R1["R1: Write-Once-Read-Many"] --> E1["Stage ghi artifact một lần, stage sau chỉ đọc"]
    R2["R2: Hydrated Context Inline"] --> E2["Planner đọc trực tiếp hydrated_context từ Bus"]
    R3["R3: Append-Only Fallback History"] --> E3["Mọi rollback được ghi append vào lịch sử trạng thái"]
    R4["R4: Version Artifacts"] --> E4["Mỗi thay đổi tạo phiên bản revision mới, không ghi đè"]
    R5["R5: Bus = Single Source of Truth"] --> E5["Các Stage KHÔNG đọc trực tiếp các file upstream"]
    R6["R6: Deconstruction Ingestion"] --> E6["UPDATE/REBUILD: Bắt buộc giải nén tri thức cũ vào Bus"]
    R7["R7: Hydrator check thought-cache"] --> E7["Hydrator bắt buộc kiểm tra sự tồn tại của thought-cache.yaml"]
    R8["R8: Mandatory for Builder"] --> E8["Builder bắt buộc nạp thought-cache để hiểu tư duy sâu"]
```

#### 📐 Sơ đồ ER Mối Quan Hệ Giữa Các Artifact
```mermaid
erDiagram
    USER_REQUEST ||--o{ BUSINESS_ANALYSIS : "sinh ra"
    BUSINESS_ANALYSIS ||--|| DOMAIN_HANDBOOK : "anchor bởi"
    CONTEXT_BUS ||--|| BUSINESS_ANALYSIS : "chứa ref"
    CONTEXT_BUS ||--|| DOMAIN_HANDBOOK : "chứa ref"
    CONTEXT_BUS ||--|| DESIGN_MD : "chứa ref"
    CONTEXT_BUS ||--|| QUALITY_MATRIX : "chứa ref"
    CONTEXT_BUS ||--|| TODO_MD : "chứa ref"
    CONTEXT_BUS ||--|| STATE_YAML : "track bởi"
    DESIGN_MD ||--|| QUALITY_MATRIX : "validated bởi"
    DESIGN_MD ||--o{ ZONE_MAP : "định nghĩa"
    DESIGN_MD ||--o{ DATA_CONTRACT : "định nghĩa"
    TODO_MD ||--o{ TASK : "chứa"
    TASK ||--|| DATA_CONTRACT : "tuân thủ"
    TASK ||--o{ MUST_NOT : "ràng buộc"
    TASK ||--|| VERIFICATION_CMD : "kiểm chứng bởi"
    TODO_MD ||--o{ SKILL_PACKAGE : "sinh ra"
    SKILL_PACKAGE ||--|| SKILL_MD : "chứa L0-L1"
    SKILL_PACKAGE ||--o{ KNOWLEDGE_FILE : "chứa L2"
    SKILL_PACKAGE ||--o{ LOOP_CHECKLIST : "chứa L3"
    SKILL_PACKAGE ||--o{ SCRIPT_FILE : "chứa I/O utility"
    MICRO_SKILL_BUNDLE ||--o{ MICRO_SKILL : "chứa"
    MICRO_SKILL ||--|| SKILL_PACKAGE : "là một"
    MICRO_SKILL_BUNDLE ||--|| ORCHESTRATE_PY : "điều phối bởi"
    MICRO_SKILL_BUNDLE ||--|| SSP_CONTRACT : "giao tiếp qua"
```

---

### 5. 🛡️ CHỐT CHẶN CHẤT LƯỢNG NGĂN NGỪA AI-SLOP (QUALITY GATES)

Hệ thống áp dụng các chốt chặn chất lượng tự động nghiêm ngặt bằng cách sử dụng các script kiểm tra cơ học thay vì để AI tự xác nhận:

```mermaid
graph TD
    subgraph GATES["Hệ Thống Quality Gates theo Stage"]
        G0["Stage 0: BA<br/>BA-1.0 Domain Ontology<br/>BA-2.0 Stakeholder<br/>BA-3.0 Edge-Case<br/>BA-4.0 Quantifiable"]
        G05["Stage 0.5: SCS<br/>SCS-1.0 Score 1.0-5.0<br/>SCS-2.0 Routing decision"]
        G07["Stage 0.7: Miner<br/>MIN-1.0 Glossary 10+<br/>MIN-2.0 Anti-patterns<br/>MIN-3.0 Exemplars"]
        G1["Stage 1: Architect<br/>ARCH-1.0 Semantic Anchors<br/>ARCH-2.0 Data Contracts<br/>ARCH-3.0 Zone Mapping<br/>ARCH-4.0 State Machine"]
        G15["Stage 1.5: Gatekeeper<br/>META-1.1 Domain Anchor<br/>META-1.2 Phase deconstruct<br/>META-2.1 Semantic Depth Gate v2.0<br/>META-2.2 Reverse Q<br/>META-3.1 Mechanical<br/>META-3.2 Negative Space<br/>META-3.3 Sandbox"]
        G17["Stage 1.7: Hydrator<br/>HYD-1.0 Glossary hydrate<br/>HYD-2.0 NFR hydrate<br/>HYD-3.0 Contracts hydrate<br/>---<br/>HYD-4.0 Depth Cache Presence<br/>HYD-4.1 thought-cache.yaml tồn tại<br/>HYD-4.2 thought-cache không rỗng"]
        G2["Stage 2: Planner<br/>PLAN-1.0 Context Fidelity<br/>PLAN-2.0 Semantic Density<br/>PLAN-3.0 Contracts+State<br/>PLAN-4.0 Negative Space<br/>PLAN-5.0 Mechanical Verify"]
        G25["Stage 2.5: Drift+Gate<br/>DRIFT-1.0 Back-link check<br/>DRIFT-2.0 Contract alignment<br/>DRIFT-3.0 State alignment<br/>DRIFT-4.0 Zone alignment<br/>---<br/>SAUDIT-1.0 Sampling audit enabled<br/>SAUDIT-1.1 Adaptive rate tracking<br/>SAUDIT-1.2 audit-fail-report.md generated on FAIL"]
        G3["Stage 3: Builder<br/>BUILD-1.1 Zone Contract<br/>BUILD-1.2 Fidelity<br/>BUILD-2.1 Placeholder<br/>BUILD-2.2 Cognitive Sep<br/>BUILD-3.1 Token Budget (Soft)<br/>BUILD-4.1 Executable<br/>BUILD-5.1 Security<br/>---<br/>BUILD-6.0 Depth Context Loaded<br/>BUILD-6.1 thought-cache.yaml loaded<br/>BUILD-6.2 Business intent traceable"]
        G3B["Stage 3a-c: Orchestrator<br/>ORCH-1.0 SSP contracts<br/>ORCH-2.0 Schema matching<br/>ORCH-3.0 Parallel exec<br/>ORCH-4.0 Integration test"]
        G35["Stage 3.5: Reviewer<br/>REV-1.0 All BUILD gates<br/>REV-2.0 Integration (B)<br/>REV-3.0 Refactor Trigger"]
        G4["Stage 4: Sandbox<br/>SAND-1.0 verification.md<br/>SAND-2.0 Exit code 0"]
    end
```

#### 📋 Chi tiết Tiêu Chí Nghiệm Thu của Các Gates
*   **BA-1.0 đến BA-4.0:** Phải làm rõ Domain Ontology (từ điển thuật ngữ), Stakeholder (đối tượng tác động), các trường hợp biên nguy cơ cao (Edge-Cases) và lượng hóa các yêu cầu phi chức năng (NFR).
*   **META-2.1 (Semantic Depth Gate v2.0):** Chốt chặn chất lượng bản vẽ kiến trúc. Kiểm tra xem `design.md` có đầy đủ 7 Zones hay không. Yêu cầu kết quả chấm điểm cơ học qua `loop_refiner.py` đạt **100% tiêu chuẩn** mới cấp chữ ký số `quality-matrix.yaml`.
*   **SAUDIT-1.0 (Sampling Audit):** Chốt chặn độ lệch thiết kế (Drift Gate). Cho phép kiểm tra ngẫu nhiên và theo tỷ lệ thích ứng. Nếu phát hiện sai khác giữa code/plan thực tế và bản vẽ kiến trúc, nó sẽ tạo `audit-fail-report.md` và buộc rollback.
*   **BUILD-2.1 (Zero Placeholder Rule):** Tuyệt đối không chấp nhận các đoạn mã giả, mock hoặc comments trì hoãn (`// TODO`, `pass`). Nếu phát hiện, mật độ placeholder > 0 sẽ lập tiếp đánh rớt bản build.
*   **SAND-1.0 (Sandbox Isolation):** Toàn bộ script kiểm thử (ít nhất 2 kịch bản từ `criteria.md`) phải được thực thi thành công (exit code 0) trong môi trường Docker/gVisor cô lập hoàn toàn trước khi cho phép cài đặt vào runtime.

---

### 6. 🔄 CHUYỂN TRẠNG THÁI & HỆ THỐNG TỰ PHỤC HỒI (STATE & FALLBACK PROTOCOL)

Khi bất kỳ Stage nào trong pipeline gặp lỗi validation thất bại hoặc điểm chất lượng nằm dưới ngưỡng an toàn (85%), hệ thống sẽ tự động dừng quy trình, ghi lại nhật ký lỗi và kích hoạt cơ chế quay lui (**CASE Fallback**).

#### 📉 Sơ đồ Chuyển Trạng thái và Phản hồi (State Transitions)
```mermaid
stateDiagram-v2
    [*] --> Stage0_BA
    [*] --> PhaseD1_Discovery : Branch A Phase Compression
    
    Stage0_BA --> Stage0_5_SCS : elicitation completed
    Stage0_5_SCS --> Stage0_BA : F1
    Stage0_5_SCS --> Stage0_7_Miner : SCS rated
    
    Stage0_7_Miner --> Stage0_BA : F2
    Stage0_7_Miner --> Stage1_Architect : domain-handbook ready
    
    Stage1_Architect --> Stage1_5_Gatekeeper : design.md ready
    Stage1_5_Gatekeeper --> Stage1_Architect : F3
    Stage1_5_Gatekeeper --> Stage0_5_SCS : F4
    Stage1_5_Gatekeeper --> Stage1_7_Hydrator : criteria pass
    
    Stage1_7_Hydrator --> Stage1_Architect : F5
    Stage1_7_Hydrator --> Stage0_7_Miner : F6
    Stage1_7_Hydrator --> Stage2_Planner : hydrated-context ready
    
    Stage2_Planner --> Stage2_5_Drift : todo.md ready
    Stage2_5_Drift --> Stage2_Planner : F7
    Stage2_5_Drift --> Stage1_Architect : F8
    Stage2_5_Drift --> Stage0_5_SCS : F9
    
    Stage2_5_Drift --> BranchA_Builder : Pass + SCS < 3.0
    Stage2_5_Drift --> BranchB_Orchestrator : Pass + SCS >= 3.0
    
    PhaseD1_Discovery --> PhaseD1_Retry : PC-1
    PhaseD1_Retry --> PhaseD1_Discovery : retry (max 3)
    PhaseD1_Retry --> Escalated : 3 fails
    PhaseD1_Discovery --> PhaseD2_Design : discovery-package ready
    
    PhaseD2_Design --> PhaseD2_Retry : PC-2
    PhaseD2_Retry --> PhaseD2_Design : retry (max 3)
    PhaseD2_Retry --> Escalated : 3 fails
    PhaseD2_Design --> PhaseD3_Plan : design + criteria pass
    
    PhaseD3_Plan --> PhaseD3_Retry : PC-3
    PhaseD3_Retry --> PhaseD3_Plan : retry (max 3)
    PhaseD3_Retry --> Escalated : 3 fails
    PhaseD3_Plan --> PhaseD3_Retry_Critical : PC-4
    PhaseD3_Retry_Critical --> Escalated : escalate immediately
    PhaseD3_Plan --> BranchA_Builder : plan verified
    
    BranchA_Builder --> Stage3_5_Reviewer : build completed
    BranchB_Orchestrator --> BranchB_Builders : spawn parallel
    BranchB_Builders --> BranchB_Assembler : all builders done
    BranchB_Assembler --> Stage3_5_Reviewer : integration completed
    
    Stage3_5_Reviewer --> BranchA_Builder : F10
    Stage3_5_Reviewer --> BranchB_Assembler : F11
    Stage3_5_Reviewer --> Stage2_Planner : F12
    Stage3_5_Reviewer --> Stage4_Sandbox : review pass
    
    Stage4_Sandbox --> BranchA_Builder : F13
    Stage4_Sandbox --> BranchB_Assembler : F14
    Stage4_Sandbox --> PhaseD3_Plan : F15 (A)
    Stage4_Sandbox --> Stage2_Planner : F15 (B)
    Stage4_Sandbox --> Stage5_Delivery : sandbox pass
    Stage5_Delivery --> [*] : build-completed
    
    Stage2_5_Drift --> Escalated : 3 iterations fail
    Stage3_5_Reviewer --> Escalated : 3 iterations fail
    Stage4_Sandbox --> Escalated : 3 iterations fail
    Escalated --> [*] : oracle/user intervene
```

#### 📋 Ma trận Fallback (Fallback Matrix F1 - F19)

| ID | Stage Bị Lỗi | Nguyên Nhân Lỗi | Quay Về | Hành Động Phục Hồi |
|:---|:---|:---|:---|:---|
| **F1** | S0.5 SCS Router | Thiếu thông tin phân tích SCS | Stage 0 | Khơi gợi lại nghiệp vụ (BA re-elicitation) |
| **F2** | S0.7 Miner | Tài liệu Domain Handbook không đủ sâu | Stage 0 | Thu thập thêm thông tin/tài liệu đầu vào |
| **F3** | S1.5 Gatekeeper | Thiết kế (`design.md`) lỗi kiểm tra tĩnh | Stage 1 | Architect sửa lại bản thiết kế |
| **F4** | S1.5 Gatekeeper | Thay đổi điểm SCS trong lúc thiết kế | Stage 0.5 | Đánh giá lại SCS và rẽ nhánh lại |
| **F5** | S1.7 Hydrator | Context nạp bị thiếu | Stage 1 | Architect bổ dung hợp đồng/zone map |
| **F6** | S1.7 Hydrator | Glossary chứa ít hơn 10 thuật ngữ | Stage 0.7 | Miner bổ sung thuật ngữ chuyên môn |
| **F7** | S2.5 Drift Gate | Phát hiện sai lệch thiết kế mức độ nhỏ (Minor) | Stage 2 | Planner sắp xếp lại các task trong `todo.md` |
| **F8** | S2.5 Drift Gate | Phát hiện sai lệch thiết kế mức độ lớn (Major) | Stage 1 | Architect sửa đổi thiết kế `design.md` |
| **F8-EXT** | S2.5 Semantic Audit | Pass bề mặt nhưng sai nghĩa bản chất | S1 / S0 | Thiết kế lại hoặc khơi gợi lại yêu cầu từ đầu |
| **F9** | S2.5 Drift Gate | Thiết kế sai lệch Domain phân vùng | Stage 0.5 | Đánh giá lại SCS và phân vùng nghiệp vụ |
| **F10** | S3.5 Reviewer | Review code thất bại (Branch A) | Stage 3 | Builder sửa đổi và hoàn thiện mã nguồn |
| **F11** | S3.5 Reviewer | Review code thất bại (Branch B) | Stage 3c | Assembler lắp ghép và fix code tích hợp |
| **F12** | S3.5 Reviewer | Lỗi tích hợp luồng (Integration) | Stage 2 | Planner sửa đổi kế hoạch điều phối orchestration-plan |
| **F13** | S4 Sandbox | Lỗi sandbox chạy thử (Branch A) | Stage 3 | Builder vá lỗi thực thi |
| **F14** | S4 Sandbox | Lỗi sandbox chạy thử (Branch B) | Stage 3c | Assembler sửa lỗi tích hợp thực thi |
| **F15** | S4 Sandbox | Kế hoạch chạy thử bị sai (Lỗi gốc Planner) | Stage 2 | Planner tái lập kế hoạch `todo.md` |
| **F16** | S0 BA | `thought-cache` thiếu tư duy giải pháp | Stage 0 | Thực hiện lại khơi gợi nghiệp vụ chuyên sâu |
| **F17** | S1.5 Gatekeeper | `thought-cache` thiếu phân tích stakeholder | Stage 0 | Thu thập phân tích đối tượng tương tác |
| **F18** | S1.7 Hydrator | `thought-cache` bị trống hoặc thiếu | Stage 0 | Thực hiện quy trình Khôi phục Độ sâu (Depth Recovery) |
| **F19** | S0 BA | Phân tích tư duy sâu thất bại chặn bởi META-2.1 | Stage 0 | Thực hiện lại phiên Deep Thinking |

*Quy tắc giới hạn:* Hệ thống khống chế **tối đa 3 vòng lặp (iterations)** quay ngược cho mỗi lỗi. Nếu vượt quá, hệ thống sẽ chuyển sang trạng thái **Escalated** để nhà phát triển (Steve) can thiệp trực tiếp.

---

### 7. 📝 PROGRESSIVE DISCLOSURE & TOKEN ECONOMICS

Để đảm bảo không vượt quá giới hạn ngữ cảnh (Context Window) của Agent khi nạp nhiều micro-skills, hệ thống triển khai cơ chế **Progressive Disclosure**:

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

**Trạng thái tài liệu:** Đã được cập nhật và đồng bộ theo Kiến trúc Đặc tả 5-Layer Ver 3.0.0 chính thức của hệ sinh thái WASHVN.