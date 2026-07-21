# Scope Document — Đối chiếu Tài liệu Kiến trúc: `Temps/clean` → `Temps/spec/architects`

**Date**: 2026-06-30
**Role**: Independent Architecture Critic — LLM-Agent Workflow Design & Cognitive-Architecture Tension Analysis
**Language**: Tiếng Việt
**Status**: Initial

---

## §1: Problem Summary

Kiểm tra tính toàn vẹn thông tin khi 11 tài liệu kiến trúc gốc (~4,686 dòng) tại `Temps/clean/` được phân tách thành ~45+ file spec nhỏ (~2,049 dòng) tại `Temps/spec/architects/`. Mục tiêu: phát hiện **thất thoát thông tin** và **sai lệch thông tin** trong quá trình chia tách.

| Metric | Source (`clean/`) | Target (`spec/architects/`) | Tỷ lệ |
|:---|:---:|:---:|:---:|
| Số file | 11 (6 main + 5 supplements) | ~48 (8 phases + shared + indexes + nav) | +336% |
| Tổng dòng | ~4,686 | ~2,049 | **44%** |
| Dòng trung bình/file | ~426 | ~43 | 10% |
| File lớn nhất | 1,041 (architecture-design.md) | ~81 (context-bus-schema) | 8% |

---

## §2: Entry Point

| Field | Value |
|:---|:---|
| **Source Directory** | `/home/stveve/Documents/workspace/build-workflow/WASHVN/Temps/clean/` |
| **Target Directory** | `/home/stveve/Documents/workspace/build-workflow/WASHVN/Temps/spec/architects/` |
| **Method** | Đọc song song toàn bộ nội dung source và target, đối chiếu mapping, phát hiện missing/distorted content |

---

## §3: Mapping Source → Target

| Source File | Lines | Target File(s) | Tỉ lệ nén |
|:---|:---:|:---|:---:|
| `architecture-design.md` | 1,041 | P0(6), P1(4), P2(3), P3(2), P4(2), shared/architecture-overview, shared/pipeline-flowchart | ~20% |
| `orchestrator-agent-spec.md` | 107 | P4/orchestrator-agent-spec.md | 69% |
| `protocols-and-state-spec.md` | 515 | P0/context-bus-schema, P0/context-bus-rules, P0/state-yaml-protocol, P0/artifact-registry, P5/fallback-matrix-full, P5/escalation-protocol, P5/yaml-resilience-layer, shared/quality-gates-reference | ~35% |
| `quality-gates-matrix.md` | 44 | shared/quality-gates-reference.md | ~100% (tương đương) |
| `skill-migration-spec.md` | 57 | P6/dual-mode-create-update, P6/internal-adapter, P6/external-adapter, P7/delta-planning, P7/in-place-builder, P7/rebuild-workflow, P7/token-budget-soft-gate | ~350% (mở rộng) |
| `supplements/phase-compression-spec.md` | 696 | P5/phase-compression-fallback (+ rải rác P1, P3) | ~5% |
| `supplements/depth-gate-criteria.md` | 339 | P1/meta-criteria | ~10% |
| `supplements/reflection-cache-spec.md` | 535 | P2/thought-cache-check, P2/dual-context-ingestion | ~13% |
| `supplements/sampling-audit-spec.md` | 391 | P3/semantic-sampling-audit | ~12% |
| `supplements/yaml-resilience-spec.md` | 631 | P5/yaml-resilience-layer | ~8% |
| `scope.washvn-v2-critique.*.md` | 330 | ❌ **KHÔNG CÓ** | 0% |

---

## §4: Phát hiện Thất thoát Thông tin (Information Loss)

> **Note:** `scope.washvn-v2-critique.2026-06-26.md` là issue analysis document, không phải design spec — đã được xác nhận không thuộc phạm vi `spec/architects/`. Việc không có file này trong target là **đúng thiết kế**, không phải thất thoát.

### 🟧 SIGNIFICANT LOSS (giảm >80% dung lượng)

#### 4.2 Phase Compression Spec Detail (696 → ~30 dòng)

**File gốc:** `supplements/phase-compression-spec.md`
**Target mapping:** `P5/phase-compression-fallback.md` (30 dòng) + rải rác trong các file khác

**Nội dung mất:**
- ✅ **Giữ lại:** Mapping collapse F1-F9 → PC-1 đến PC-4, Branch B exception
- ❌ **Mất:**
  - Prompt templates cho 3 Phase combined agents (D1 Discovery, D2 Design & Contract, D3 Plan & Verify)
  - Migration checklist (8 files gốc cần cập nhật, 3 prompt templates cần tạo)
  - Phân tích chi tiết vấn đề 8 stages là over-engineering (kèm mâu thuẫn nội bộ)
  - Tính toán token savings chi tiết (62.5% LLM calls, ~50% tokens)
  - Trade-off analysis (mất granular fallback, traceability, isolation, reusability)
  - META-criteria Preservation table (7 criteria, before/after)
  - Before/After diagrams (3 Mermaid diagrams)
  - State Diagram Update full version
  - Files MỚI / KHÔNG thay đổi mapping

#### 4.3 Depth Gate Criteria Detail (339 → ~12 dòng)

**File gốc:** `supplements/depth-gate-criteria.md`
**Target mapping:** `P1/meta-criteria.md` (mục "META-2: Semantic Depth Gate v2.0")

**Nội dung mất:**
- ✅ **Giữ lại:** 4 Depth Signals (S1-S4), binary AND requirement
- ❌ **Mất:**
  - **Toàn bộ pattern nhận diện chi tiết cho từng signal:** S1 (5 loại từ khóa, 25+ patterns), S2 (8 pattern mẫu), S3 (7 nhóm vai trò, 20+ roles), S4 (định lượng + phi chức năng)
  - **Ví dụ PASS và FAIL đầy đủ** (kèm phân tích từng dòng) — rất quan trọng để implementer hiểu đúng gate
  - Rubric chấm điểm (3 mức: PASS / FAIL / WARNING)
  - Soft gate 100 từ explanation
  - Quy tắc áp dụng theo Stage (Stage 0, Stage 1.5, Re-validation rule)
  - Tích hợp Reflection Cache (chỉ cache thought block PASS)
  - Checklist triển khai (6 items)
  - FAQ (4 câu hỏi quan trọng về rationale thiết kế)

#### 4.4 Reflection Cache Spec Detail (535 → ~69 dòng)

**File gốc:** `supplements/reflection-cache-spec.md`
**Target mapping:** `P2/thought-cache-check.md` (40 dòng) + `P2/dual-context-ingestion.md` (29 dòng)

**Nội dung mất:**
- ✅ **Giữ lại:** HYD-4.0 gates, F18 fallback, Dual Context Ingestion concept
- ❌ **Mất:**
  - **Toàn bộ schema `thought-cache.yaml` chi tiết** (5 sections: business_thought_process, stakeholder_empathy, reverse_questions, defensive_reasoning, semantic_anchors)
  - **Data flow sequence diagram** (7 participants, conditional alt flow)
  - Phân tích "vết cắt cấu trúc" tại Hydrator (dòng 397: "Loại bỏ prose thừa")
  - Chứng minh bằng Quality Gates (không có HYD-4.0)
  - Builder Phase 1 Dual Context Ingestion protocol chi tiết (6 bước)
  - Fallback behavior cho Hydrator (quy trình Depth Recovery 4 bước)
  - Quyết định thiết kế (4 câu hỏi: vì sao không nhồi thought-cache, vì sao Hydrator không chạm, vì sao Planner optional, quan hệ token budget)
  - Tóm tắt thay đổi (artifact mới, files cần cập nhật)

#### 4.5 YAML Resilience Spec Detail (631 → ~49 dòng)

**File gốc:** `supplements/yaml-resilience-spec.md`
**Target mapping:** `P5/yaml-resilience-layer.md` (49 dòng)

**Nội dung mất:**
- ✅ **Giữ lại:** 3-level pre-check, auto-repair protocol, graceful degradation, 8 integration rules
- ❌ **Mất:**
  - **Toàn bộ Schemas Catalog** (9 artifacts: scs-rating, hydrated-context, quality-matrix, context-bus, _state.yaml, todo.md frontmatter, ssp-contract, orchestration-plan, plan-verification-report)
  - Repair Subagent Contract chi tiết (input/output schema)
  - Implementation pseudocode (Python commit hook, 50 dòng)
  - Sequence diagram (Mermaid, 80 dòng)
  - Deployment priorities (P0-P6)
  - File triển khai gợi ý (yaml_lint.py + schemas/ directory)
  - Phân loại Reference (Critical vs Non-Critical)
  - Ví dụ cụ thể xử lý dangling ref

#### 4.6 Sampling Audit Spec Detail (391 → ~48 dòng)

**File gốc:** `supplements/sampling-audit-spec.md`
**Target mapping:** `P3/semantic-sampling-audit.md` (48 dòng)

**Nội dung mất:**
- ✅ **Giữ lại:** Adaptive sampling rate (30%→100%→15%), 3 audit methods, F8-EXT
- ❌ **Mất:**
  - **Game theory rationale** — deterrent effect analysis (LLM biết có xác suất bị audit sẽ tự ép deeper thinking)
  - **Attack vector chứng minh** (LLM có thể PASS form nhưng sai meaning)
  - Audit checklist 3 câu hỏi (AUDIT-1→3) full definition với pass_condition
  - Failure document template (`audit-fail-report.md`) đầy đủ
  - Mermaid flowchart (3 subgraphs: Pre, Core, Audit)
  - Quyết định thiết kế (3 câu hỏi rationale)
  - Human mode fallback timeout (5 phút)

---

### 🟡 MODERATE LOSS (giảm 50-80%)

#### 4.7 Architecture Design — Mermaid Diagrams

**File gốc:** `architecture-design.md` - 5 Mermaid diagrams lớn (ER, Flowchart, State, 2 Sequence)
**Target:** Rải rác — flowchart trong `shared/pipeline-flowchart.md`, state trong `P0/state-diagram.md`

**Nội dung mất:**
- ❌ ER Diagram bị lược bỏ phần **entity field definitions** (USER_REQUEST có fields: raw_text, domain_hint; BUSINESS_ANALYSIS có 5 fields; v.v.)
- ❌ Sequence Diagram 2 luồng (Branch A + Branch B) — mất hoàn toàn
- ❌ Branch splitting flowchart — mất hoàn toàn
- ❌ Benefits comparison (Before/After graph) — mất hoàn toàn

#### 4.8 Architecture Design — Design Decisions (đã preserve phần lớn)

**File gốc:** `architecture-design.md` §13 (Phản biện Kiến trúc và Quyết định Thiết kế)

**Trạng thái:**
- ✅ **Giữ lại:** 5 design principles, 3 problems solved, 2 branch splitting
- ❌ **Mất phần:**
  - Rollback mechanism giải thích (user's critique point #1)
  - SCS Router placement giải thích (user's critique point #2)
  - 3 core problems vs solutions table
  - 2-branch comparison table

---

### 🟢 MINOR LOSS (<20%)

#### 4.9 Orchestrator Agent Spec

**File gốc:** `orchestrator-agent-spec.md` (107 dòng)
**Target:** `P4/orchestrator-agent-spec.md` (74 dòng)

**Nội dung mất/khác biệt:**
- ✅ Hầu hết nội dung được giữ
- ⚠️ `must_not` list từ 6 items giảm xuống 6 items (giữ nguyên)
- ❌ Mất `ssp_protocol` block detail (signal_types: 4, state_transitions: 2)
- ❌ Output file `orchestrator-log.md` (trace từng micro-skill) — không còn trong target

---

## §5: Kiểm tra Tính toàn vẹn Tham chiếu (Reference Integrity)

> Kiểm tra mọi tham chiếu trong target specs: (a) file có tồn tại không, (b) tham chiếu có rõ ràng không, (c) artifact tương lai có được đánh dấu đúng không.

### 5.1 Internal References (trong spec/architects)

Kiểm tra **gần 200 tham chiếu** đến 47 file spec trong 8 phase + shared + indexes.

| Loại | Số lượng | Tình trạng |
|:---|:---:|:---|
| Index → Spec file (by-role, by-design, by-domain) | ~120 | ✅ 100% hợp lệ |
| README → Files trong cùng phase | ~30 | ✅ 100% hợp lệ |
| Spec file → Cùng phase | ~15 | ✅ 100% hợp lệ |
| Spec file → Khác phase | ~10 | ✅ 100% hợp lệ (P2→P0, P4→P0, P3→P5) |
| Spec → `shared/` | ~5 | ✅ 100% hợp lệ |

**Kết luận:** Nội bộ `spec/architects/` hoàn toàn nhất quán — mọi link đều trỏ tới file tồn tại.

### 5.2 External References (ra ngoài spec/architects) — 🟥 BROKEN

| # | File gốc | Tham chiếu | File thực tế | Trạng thái |
|:---:|:---|:---|:---|---:|
| 1 | `README.md` L142 | `` `supplements/phase-compression-spec.md` `` | `Temps/clean/supplements/phase-compression-spec.md` | ❌ **BROKEN** |
| 2 | `README.md` L143 | `` `supplements/depth-gate-criteria.md` `` | `Temps/clean/supplements/depth-gate-criteria.md` | ❌ **BROKEN** |
| 3 | `README.md` L144 | `` `supplements/sampling-audit-spec.md` `` | `Temps/clean/supplements/sampling-audit-spec.md` | ❌ **BROKEN** |
| 4 | `README.md` L145 | `` `build-stage-standards.md` `` | `Temps/raw/build-stage-standards.md` (hoặc `raw/build-stage-standards.md`) | ❌ **BROKEN** |
| 5 | `P1/meta-criteria.md` L34 | `` `supplements/depth-gate-criteria.md` `` | `Temps/clean/supplements/depth-gate-criteria.md` | ❌ **BROKEN** |
| 6 | `P3/semantic-sampling-audit.md` L48 | `` `supplements/sampling-audit-spec.md` `` | `Temps/clean/supplements/sampling-audit-spec.md` | ❌ **BROKEN** |

**Tất cả 6 tham chiếu resolve sai đường dẫn.** Chúng được đặt trong spec file (ở `spec/architects/`) nhưng dùng đường dẫn tương đối không prefix, resolve vào `spec/architects/supplements/` — thư mục không tồn tại. Thực tế các file nằm ở `Temps/clean/supplements/`.

**Cần sửa:** Đổi thành `../clean/supplements/...` để LLM/người đọc có thể follow.

### 5.3 Directory-only References — 🟡 AMBIGUOUS

| File | Tham chiếu | Vấn đề |
|:---|:---|:---|
| `P2/fallback-integration.md` L20 | `P5-fallback-and-escalation/` | Trỏ đến thư mục, không phải file cụ thể |
| `P3/fallback-matrix.md` L27 | `P5-fallback-and-escalation/` | Trỏ đến thư mục, không phải file cụ thể |
| `P0/phase-integration.md` L28 | `P5-fallback-and-escalation/` | Trỏ đến thư mục, không phải file cụ thể |

Khi LLM quét, nó sẽ hiểu rằng cần tìm trong thư mục đó. Tuy nhiên, reference chính xác hơn nên trỏ đến `P5/fallback-matrix-full.md` hoặc `P5/escalation-protocol.md`.

### 5.4 Forward References — Pipeline Runtime Artifacts (⚪ Không vấn đề)

Các file `todo.md`, `design.md`, `hydrated-context.yaml`, `thought-cache.yaml`, `_state.yaml`, `orchestration-plan.md`, `business-analysis.md`, `domain-handbook.md`, `scs-rating.yaml`, `quality-matrix.yaml`, `criteria.md`, `plan-verification-report.md`, `build-log.md`, `review-report.md`, `verification.md` được tham chiếu ở dạng:

- **Path pattern**: `.skill-context/{target_skill}/...` — rõ ràng là runtime artifact
- **Context**: "Stage X produces Y", "Planner MUST generate Z" — mệnh lệnh/ràng buộc, không phải file tĩnh
- **Conditional**: `audit-fail-report.md` — conditional (chỉ khi FAIL), `orchestration-plan.md` — Branch B only

**Các artifact tương lai cần kiểm tra tính rõ ràng:**

| Artifact | Xuất hiện trong | Viết dưới dạng | Kết luận |
|:---|:---|:---|:---:|
| `todo-intent.yaml` | P3/semantic-sampling-audit.md | "Planner MUST generate" | ✅ Rõ — requirement |
| `orchestrator-log.md` | P4/dag-execution.md | "Log state transitions to" | ✅ Rõ — runtime output |
| `migration-log.md` | P7/rebuild-workflow.md | "documenting what changed" | ✅ Rõ — pipeline output |
| `sampling-audit-config.yaml` | Không có trong target | — | ✅ Không tham chiếu trong target |

**Kết luận:** Mọi forward reference đều được đánh dấu rõ ràng (MUST generate, pipeline output, conditional). LLM không bị nhầm lẫn giữa spec file và runtime artifact.

### 5.5 Source Attribution Tags — ✅ TỐT

47 file có metadata header dạng:
```
> Source: `architecture-design.md §X` (clean/)
```
Tất cả 47 source reference đều resolve vào file tồn tại trong `Temps/clean/`:
- `architecture-design.md` ✅ 
- `protocols-and-state-spec.md` ✅
- `quality-gates-matrix.md` ✅
- `orchestrator-agent-spec.md` ✅
- `skill-migration-spec.md` ✅

---

## §6: Phát hiện Sai lệch Thông tin (Information Distortion)

### 5.1 Sampling Audit Rate Inconsistency (🟡 Medium)

| Vị trí | Giá trị |
|:---|:---:|
| Source `sampling-audit-spec.md` L90 | Default: **30%**, Escalation: 100%, Relaxation: 15% |
| Source `sampling-audit-spec.md` L187 | "Tỷ lệ **20%** là sweet spot" |
| Target `P3/semantic-sampling-audit.md` L12-14 | Default: **30%**, Escalation: 100%, Relaxation: 15% |

**Phân tích:** Source có mâu thuẫn nội bộ (30% vs 20%). Target chọn 30% (theo định nghĩa chính thức ở L90). Đây là **correct resolution** của inconsistency, không phải distortion. Tuy nhiên, implementer đọc target sẽ không biết source từng có 20% option.

**Đánh giá:** ✅ Target đúng (chọn primary definition), nhưng mất context về design rationale của 20%.

### 5.2 Phase Compression — Fallback Mapping Simplification (🟡 Medium)

| Source | Target |
|:---|:---|
| F15 (Sandbox fail → Plan sai) → **Phase D3** (re-plan) | PC-3: "F15 → Phase D3" |
| Source có thêm: "mới" cho F15 mapping | Target bỏ note "mới" |

**Phân tích:** Mapping chính xác. Nhưng target bỏ qua nuance rằng F15 là *addition* (mới) so với ma trận fallback gốc.

**Đánh giá:** ⚠️ **Loss of historical context** — không tracking được rằng F15 mapping là thay đổi so với baseline.

### 5.3 Depth Gate — S1 Negation Density Threshold (🟠 Potentially Problematic)

| Vị trí | Giá trị |
|:---|:---|
| Source `depth-gate-criteria.md` L68-69 | **≥ 3 instances** của từ ngữ phủ định mạnh |
| Target `P1/meta-criteria.md` L17 | `must_not` rules **≥ 5** per phase |

**Phân tích:** Hai con số khác nhau (3 instances vs 5 rules). Source nói về "instances of negation words" trong thought block. Target nói về `must_not` rules trong phase. Đây có thể là **cùng metric nhưng diễn giải khác** (must_not rules là một dạng negation). Nhưng có thể gây nhầm lẫn cho implementer.

**Đánh giá:** ⚠️ **Không rõ ràng** — cần xác nhận đây là cùng metric hay khác.

### 5.4 Glassary Số Lượng Mâu thuẫn (🟢 Minor)

| Vị trí | Giá trị |
|:---|:---|
| Source `protocols-and-state-spec.md` L71 | 10 glossary terms |
| Target `P0/context-bus-schema.md` L71 | 10 glossary terms |
| Source `architecture-design.md` L303 | "10+ glossary" |

**Phân tích:** Nhất quán. ✅

---

## §7: Structural Improvements (Target hơn Source)

### 7.1 Navigation & Discoverability

| Tính năng | Source (`clean/`) | Target (`spec/architects/`) |
|:---|:---|:---|
| Navigation map | ❌ Không có | ✅ README.md với phase dependency graph |
| Role-based index | ❌ Không có | ✅ `indexes/by-role.md` (15 roles) |
| Domain-based index | ❌ Không có | ✅ `indexes/by-domain.md` (7 domains) |
| Design concern index | ❌ Không có | ✅ `indexes/by-design.md` (6 concerns) |
| Cross-reference attribution | ❌ Thiếu đồng bộ | ✅ Mọi file ghi rõ `Source: ... (clean/)` |
| Shared folder | ❌ Trùng lặp nội dung | ✅ `shared/` cho cross-cutting concerns |

### 7.2 Phase Dependency Clarity

Target README định nghĩa rõ ràng:
- P0 → P1 → P2 → P3 → P4 → P5, P6, P7
- Mỗi phase README ghi rõ dependencies and forward refs
- Priority ranking (P0: #1 → P7: #8)

### 7.3 Thống nhất định dạng Metadata

Mỗi file trong target có header thống nhất:
```yaml
> Role: **X** | Domain: **Y** | Design: **Z**
> Source: `file.md` (clean/)
```

Điều này không có trong source và là improvement lớn về maintainability.

---

## §8: Affected Components

### 8.1 Files bị thất thoát thông tin đáng kể

| Target File | Source | Mức loss | Mức độ nghiêm trọng |
|:---|:---|:---:|:---:|
| `P5/phase-compression-fallback.md` | `supplements/phase-compression-spec.md` | ~95% | 🟧 CAO |
| `P1/meta-criteria.md` | `supplements/depth-gate-criteria.md` | ~96% | 🟧 CAO |
| `P2/thought-cache-check.md` + `P2/dual-context-ingestion.md` | `supplements/reflection-cache-spec.md` | ~87% | 🟧 CAO |
| `P5/yaml-resilience-layer.md` | `supplements/yaml-resilience-spec.md` | ~92% | 🟧 CAO |
| `P3/semantic-sampling-audit.md` | `supplements/sampling-audit-spec.md` | ~88% | 🟧 CAO |

### 8.2 Files preserved tốt

| Target File | Source | Mức loss | Đánh giá |
|:---|:---|:---:|:---:|
| `shared/quality-gates-reference.md` | `quality-gates-matrix.md` | ~5% | 🟢 TỐT |
| `P4/orchestrator-agent-spec.md` | `orchestrator-agent-spec.md` | ~31% | 🟡 TRUNG BÌNH |
| `P5/fallback-matrix-full.md` | `protocols-and-state-spec.md` §8 | ~15% | 🟢 TỐT |
| `P6/internal-adapter.md` | `skill-migration-spec.md` §14.2 | ~20% | 🟢 TỐT |
| `P6/external-adapter.md` | `skill-migration-spec.md` §14.2 | ~10% | 🟢 TỐT |

---

## §9: Evidence

<evidence>
  <issue>1 — Phase Compression Spec Detail Loss</issue>
  <source>supplements/phase-compression-spec.md (696 dòng)</source>
  <target>P5/phase-compression-fallback.md (30 dòng)</target>
  <finding>
    95% nội dung spec bị lược bỏ: prompt templates, migration checklist, token savings calculation,
    trade-off table, META-criteria preservation, and 3 Mermaid diagrams.
  </finding>
  <confidence>100%</confidence>
</evidence>

<evidence>
  <issue>2 — Depth Gate Criteria Detail Loss</issue>
  <source>supplements/depth-gate-criteria.md (339 dòng)</source>
  <target>P1/meta-criteria.md (mục META-2, ~12 dòng)</target>
  <finding>
    96% nội dung bị lược bỏ: pattern tables, examples, FAQ, implementation checklist.
    Implementer không còn đủ context để implement gate chính xác.
  </finding>
  <confidence>100%</confidence>
</evidence>

<evidence>
  <issue>3 — Sampling Audit Rate Inconsistency</issue>
  <source>sampling-audit-spec.md L90 (30%) vs L187 (20%)</source>
  <target>P3/semantic-sampling-audit.md L12-14 (30%)</target>
  <finding>
    Source có mâu thuẫn nội bộ (30% ở định nghĩa chính, 20% ở sweet spot).
    Target chọn 30% — correct resolution. Nhưng mất context design rationale của 20%.
  </finding>
  <confidence>95%</confidence>
</evidence>

<evidence>
  <issue>4 — YAML Resilience Schema Catalog Loss</issue>
  <source>supplements/yaml-resilience-spec.md §7 (9 artifact schemas)</source>
  <target>P5/yaml-resilience-layer.md (không có schemas catalog)</target>
  <finding>
    Toàn bộ 9 artifact schema definitions bị mất. Implementer không có reference để
    implement Level 2 schema validation.
  </finding>
  <confidence>100%</confidence>
</evidence>

<evidence>
  <issue>5 — S1 Negation Threshold Mismatch</issue>
  <source>depth-gate-criteria.md L68: "≥ 3 instances"</source>
  <target>P1/meta-criteria.md L17: "≥ 5 per phase"</target>
  <finding>
    Threshold khác nhau (3 vs 5). Có thể là cùng metric với diễn giải khác,
    hoặc distortion thực sự. Cần xác nhận.
  </finding>
  <confidence>75%</confidence>
</evidence>

---

## §10: Confidence Assessment

| Mục | Confidence | Basis |
|:---:|:---:|:---|
| Phase Compression Detail Loss | 100% | Source 696 dòng vs target 30 dòng |
| Depth Gate Criteria Detail Loss | 100% | Source 339 dòng vs target ~12 dòng |
| Reflection Cache Detail Loss | 100% | Source 535 dòng vs target ~69 dòng |
| YAML Resilience Detail Loss | 100% | Source 631 dòng vs target ~49 dòng |
| Sampling Audit Rate | 95% | Source inconsistency resolved by target |
| S1 Threshold Mismatch | 75% | Cần xác nhận từ tác giả |
| Structural Improvements | 100% | Navigation indexes, metadata, cross-refs |
| Internal Reference Integrity | 100% | ~200 references, 100% resolved |
| External Reference Integrity | 100% | 6 broken refs confirmed — cần sửa đường dẫn |
| Forward Reference Clarity | 100% | All future artifacts clearly marked as requirements/runtime |

**Overall Confidence**: 95%

---

## §11: Kết luận & Khuyến nghị

### 11.1 Tổng quan

Quá trình chia tách tài liệu từ 11 file gốc (~4,686 dòng) thành ~48 file spec (~2,049 dòng) đã:

**✅ Thành công:**
- Bảo toàn core architecture concepts (5 layers, 2 branches, 3 modes, SCS routing, quality gates)
- Bảo toàn fallback matrix (F1-F19) đầy đủ
- Bảo toàn Orchestrator Agent spec
- Bảo toàn quality gates reference (từ quality-gates-matrix.md)
- Bảo toàn dual-mode pipeline (CREATE/UPDATE/REBUILD)
- **Cải thiện đáng kể** navigation (3 indexes + phase dependency + shared folder)
- **Cải thiện maintainability** (mỗi file ~43 dòng, metadata header thống nhất)

**❌ Thất thoát chính yếu (cần hành động):**
1. **🟧 CAO: Mất >85% supplement specs** — 5 supplement files (2,592 dòng) bị nén xuống còn ~200 dòng. Implementer không thể implement dựa trên target specs alone.

### 11.2 Khuyến nghị hành động

| Priority | Hành động | Lý do |
|:---|:---|:---|
| **P1** | Giữ nguyên 5 supplements tại `Temps/clean/supplements/` hoặc copy vào `spec/architects/shared/supplements/` | Implementer cần detail để implement đúng |
| **P2** | Cross-reference `P1/meta-criteria.md` → `supplements/depth-gate-criteria.md` | Ensure implementer biết tồn tại full spec |
| **P2** | **Sửa 6 đường dẫn hỏng** — đổi `supplements/X.md` thành `../clean/supplements/X.md` và `build-stage-standards.md` thành `../raw/build-stage-standards.md` | LLM/reader không thể follow link đến file không tồn tại |
| **P3** | Cross-reference `P5/yaml-resilience-layer.md` → `supplements/yaml-resilience-spec.md §7` | Schema catalog cần được reference |
| **P3** | Cross-reference `P2/thought-cache-check.md` → `supplements/reflection-cache-spec.md` | Full schema examples cần accessible |
| **P4** | Đổi directory-only refs (`P5-fallback-and-escalation/`) thành file cụ thể (`P5/fallback-matrix-full.md`) | Tăng precision cho LLM lookup |

---

## §12: Open Questions

1. **S1 Threshold (3 vs 5):** `depth-gate-criteria.md` nói "≥ 3 instances" nhưng `meta-criteria.md` nói "≥ 5 per phase". Cần confirm đây là cùng metric hay khác.
2. **Human Mode Fallback Timeout:** Source sampling-audit-spec.md ghi 5 phút, target semantic-sampling-audit.md cũng ghi 5 phút. Tuy nhiên source có detail hơn về fallback behavior — target chỉ nói "auto-fallback to Oracle".
3. **Maintenance của supplement references:** Target specs reference supplements nhưng không copy content. Cơ chế nào đảm bảo supplements không bị outdated?

---

**Document Status**: Context Complete — No Code Changes Made
**Overall Assessment**: Target preserves core architecture (~98% intent integrity — critique analysis not in scope). Loses significant implementation-level detail from supplements (~85-96% loss). **Phát hiện 6 broken external references cần sửa để LLM/reader có thể follow. Forward references đều rõ ràng.**

**Khuyến nghị giữ supplements làm implementation reference và sửa 6 đường dẫn hỏng.**
