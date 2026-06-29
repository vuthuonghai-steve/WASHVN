# Dual-Mode Pipeline (CREATE / UPDATE / REBUILD)

> Role: **Gatekeeper** | Domain: **Migration** | Design: **Architecture**
## Dual-Mode Flow

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

> Source: `skill-migration-spec.md §14.1` (clean/)

## Three execution modes

| Mode | When | What happens |
|:---|:---|:---|
| **CREATE** | New skill, no prior | Standard pipeline from Stage 0 |
| **UPDATE** | Existing WASHVN skill | Internal Deconstructor + Miner analyzes old → Delta Planning → In-place Builder |
| **REBUILD** | External/non-standard skill | External Deconstructor → full re-design → fresh Builder |

## Flow diagram

```
Input: old skill path + prompt

    ├── CREATE → Miner std → Architect → Planner std → Builder new
    │
    ├── UPDATE → Deconstructor (internal)
    │           → Miner analyze intent + knowledge
    │           → Architect design Delta
    │           → Planner Delta tasks
    │           → Builder patch in-place
    │
    └── REBUILD → Deconstructor (external)
                 → Miner convert to metadata
                 → Architect full re-design
                 → Planner standard
                 → Builder fresh
```

## Key difference

- **UPDATE**: Builder modifies existing files in-place (patches)
- **REBUILD/CREATE**: Builder creates new directory + files from scratch

> See `P7-delta-planning-and-builder/` for Delta planning details
