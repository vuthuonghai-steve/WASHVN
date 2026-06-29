# Architecture Overview — 5-Layer Pipeline

> Design concern: **Architecture** | Applies to: **All phases P0-P7**

## 5 Layers

| Layer | Name | Responsibility | Components |
|:---|:---|:---|:---|
| **L0** | Intake & Routing | Receive requests, assess complexity, route | BA Elicitor, SCS Router |
| **L1** | Knowledge Foundation | Mine knowledge, build domain-handbook | Miner |
| **L2** | Design & Contract | Static design, semantic anchors, contracts | Architect, Spec Gatekeeper |
| **L3** | Planning & Verification | Context hydration, planning, drift detection | Hydrator, Planner, Drift Detector |
| **L4** | Implementation & Delivery | Build, review, sandbox, deliver | Builder / Orchestrator, Reviewer, Sandbox |

## 2 Branches

- **Branch A** (SCS < 3.0): Fast Track — Phase Compression (3 phases D1-D3)
- **Branch B** (SCS >= 3.0): Full Track OMSP — Orchestrator + N Parallel Builders

## 3 Execution Modes

- **CREATE**: New skill from scratch
- **UPDATE**: In-place modification of existing skill
- **REBUILD**: Reconstruct skill preserving original intent

## Design Principles

```mermaid
graph TD
    P1["Single Source of Truth"] --> R[Context Bus là nguồn ngữ cảnh]
    P2["Separation of Concerns"] --> R2[Hydrator tách khỏi Planner, Router tách khỏi Builder]
    P3["Fail-Fast & Rollback"] --> R3[Mọi stage fail có đường quay vòng]
    P4["Branch on Complexity"] --> R4[SCS score quyết định Fast vs Full Track]
    P5["Mechanical Verification"] --> R5[Gate chạy lệnh kiểm chứng, không tự chấm điểm]
```

## Before vs After

```mermaid
graph LR
    subgraph BEFORE["Trước (8 stage tuyến tính)"]
        B1["Context Leak"] --> B4["Điểm sụt giảm 80→55"]
        B2["Planner overload"] --> B4
        B3["No SCS Router"] --> B4
    end
    subgraph AFTER["Sau (5 Layer + branch)"]
        A1["Context Bus"] --> A4["Giải quyết Context Leak"]
        A2["Hydrator tách"] --> A5["Planner tập trung planning"]
        A3["SCS Router"] --> A6["Task đơn giản không đi pipeline nặng"]
        A7["Drift Detector"] --> A8["Chặn drift trước Builder"]
        A9["Rollback protocol"] --> A10["Fail-fast + recovery"]
        A11["Orchestrator"] --> A12["Micro-skill tự động"]
    end
    style BEFORE fill:#f8d7da
    style AFTER fill:#d4edda
```

> See `shared/pipeline-flowchart.md` for full pipeline view
