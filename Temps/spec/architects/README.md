# 🌐 Spec Architects — Master Navigation Map

> **Version:** 1.0 | **Date:** 2026-06-29
> **Source:** 5 design files from `Temps/clean/` — **~1,764 dòng → 45+ file nhỏ**
> **Mục đích:** Phân tán tài liệu thiết kế kiến trúc thành các spec nhỏ, theo phase, role, domain, design concern

---

## 🗺️ Cấu trúc thư mục

```text
spec/architects/
├── README.md                          ← Bạn đang ở đây
├── P0-context-bus-and-state/          ← Foundation: Context Bus + _state.yaml
├── P1-scs-router-and-gatekeeper/      ← Routing: SCS + Spec Gatekeeper
├── P2-context-hydrator/               ← Hydration: Context Hydrator
├── P3-drift-detector-and-plan-gate/   ← Verification: Drift Detector + Plan Gate
├── P4-orchestrator-and-assembler/     ← Branch B: Orchestrator + Assembler
├── P5-fallback-and-escalation/        ← Safety: Fallback + Escalation + YAML Resilience
├── P6-deconstructor-and-miner/        ← Migration: Deconstructor + Miner Analyzer
├── P7-delta-planning-and-builder/     ← Update: Delta Planning + In-place Builder
├── shared/                            ← Cross-cutting references
└── indexes/                           ← Tra cứu theo 3 chiều
```

---

## 📋 Phase dependency

| Phase | Priority | Content | Depends on | ~files | ~lines |
|:---|:---|:---|:---|:---:|:---:|
| **P0** | #1 | Context Bus + _state.yaml | None | 6 | ~110 |
| **P1** | #2 | SCS Router + Gatekeeper + META | P0 | 5 | ~90 |
| **P2** | #3 | Hydrator + Dual Context + thought-cache | P0, P1 | 5 | ~90 |
| **P3** | #4 | Drift Detector + Plan Gate + Audit | P0, P1, P2 | 5 | ~100 |
| **P4** | #5 | Orchestrator + SSP + Branch B | P0, P1, P2, P3 | 6 | ~130 |
| **P5** | #6 | Full Fallback + Escalation + YAML | P0 | 5 | ~130 |
| **P6** | #7 | Deconstructor + Miner + Dual-Mode | P0 | 5 | ~90 |
| **P7** | #8 | Delta Planning + In-place Builder | P3, P4, P6 | 5 | ~100 |

**Tổng spec: ~1,515 dòng** (content P0-P7 + shared). + indexes/ (~293) + README (~153) = ~2,049 tổng thể.
Mỗi file nhỏ: **~43 dòng/file** (giảm ~88% so với 353 dòng/file gốc)

---

## 🎭 Tra cứu theo Role (indexes/by-role.md)

Mỗi vai trò trong pipeline được gom vào một bảng đầy đủ:

| Role | Phase files chính |
|:---|:---|
| BA Elicitor | P1, P2, P5 |
| SCS Router | P1, P5 |
| Miner | P6, P2, P5 |
| Architect | P1, P3, P7 |
| Spec Gatekeeper | P1, P5 |
| Hydrator | P2, P0 |
| Planner | P3, P7, P4 |
| Drift Detector | P3 |
| Orchestrator | P4 |
| Builder | P4, P2, P7 |
| Assembler | P4 |
| Reviewer | P7, shared |
| Deconstructor | P6 |
| Escalator | P5 |
| Validator | P5, shared |

---

## 📂 Tra cứu theo Domain (indexes/by-domain.md)

| Domain | Mô tả | Key files |
|:---|:---|:---|
| **Data** | Schema, artifacts | P0/context-bus-schema, P0/artifact-registry, P2/hydration-schema |
| **Protocol** | Rules, state, routing | P0/rules, P0/state-yaml, P1/scs-routing, P4/ssp |
| **Quality** | Gates, criteria, audit | shared/quality-gates, P1/meta-criteria, P3/plan-quality-gate |
| **Execution** | Build, orchestrate, assemble | P4/*, P7/delta-planning, P7/in-place-builder |
| **Resilience** | YAML safety, degraded mode | P5/yaml-resilience-layer |
| **Migration** | Deconstruct, dual-mode, rebuild | P6/*, P7/rebuild-workflow |
| **Knowledge** | Domain-handbook, glossary | P6/miner-analyzer, shared/glossary |

---

## 🔧 Tra cứu theo Design Concern (indexes/by-design.md)

| Concern | Mô tả | Key files |
|:---|:---|:---|
| **Architecture** | Cấu trúc tổng thể | shared/architecture-overview, P0/state-yaml, P4/dag |
| **Contract** | Ràng buộc data/protocol | P0/context-bus-schema, P4/ssp, P6/adapters |
| **Integration** | Kết nối components | P0/phase-integration, P4/parallel-builders, P4/assembler |
| **Quality** | Chất lượng thiết kế | P1/meta-criteria, P3/plan-gate, P7/token-budget |
| **Fallback** | Xử lý lỗi | P5/fallback-full, P5/escalation, P3/fallback-matrix |
| **Verification** | Kiểm chứng cơ học | P3/drift-detection, P3/sampling-audit |

---

## 📊 So sánh: Trước vs Sau

| Tiêu chí | Trước (5 file) | Sau (48 file) |
|:---|:---|:---|
| Tổng dòng | ~1,764 | ~2,049 (spec 1,515 + index 293 + nav 153) |
| File lớn nhất | 1,041 (architecture-design) | ~55 (mỗi spec file) |
| Dòng trung bình/file | ~353 | ~43 |
| Cách tra cứu | Manual scroll | 3 indexes + phase map |
| Cross-cutting | Trùng lặp nội dung | Shared/ + forward refs |
| Role-specific | Phải lọc thủ công | Index by-role |
| Domain-specific | Không có | Index by-domain |
| Design concern | Không có | Index by-design |

---

## 🚀 Thứ tự đọc đề xuất

### Foundation (bắt buộc)
```
1. shared/architecture-overview.md      ← context nền
2. shared/glossary.md                   ← thuật ngữ
3. P0/ → đọc 6 files                   ← foundation
4. P1/ → đọc 5 files                   ← routing
```

### Core pipeline
```
5. P2/ → đọc 5 files                   ← hydration
6. P3/ → đọc 5 files                   ← drift detection
7. P5/fallback-matrix-full.md          ← fallback tổng thể
```

### Nâng cao (khi cần)
```
8. P4/ → khi SCS >= 3.0                ← orchestrator
9. P6/ → khi UPDATE/REBUILD            ← deconstructor
10. P7/ → khi UPDATE mode              ← delta planning
```

---

## 🔗 External references

| Reference | Phase | Location |
|:---|:---|:---|
| Phase Compression Spec | P0-P3 | `supplements/phase-compression-spec.md` |
| Depth Gate Criteria v2.0 | P1 | `supplements/depth-gate-criteria.md` |
| Sampling Audit Spec | P3 | `supplements/sampling-audit-spec.md` |
| Build Stage Standards | P4, P7 | `build-stage-standards.md` |

---

## 📝 Notes

- **File gốc giữ nguyên** tại `Temps/clean/` — không xóa, để làm reference
- **Mỗi file < 70 dòng** — tối thiểu hóa kích thước
- **Forward reference** — dùng cross-links thay vì copy content
- **Source tags** — mỗi file ghi rõ source từ material gốc
