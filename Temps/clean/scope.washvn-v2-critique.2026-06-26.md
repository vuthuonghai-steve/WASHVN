# Scope Document — WASHVN v2.0 Architecture Critique (6 Issues)

**Date**: 2026-06-26
**Status**: Initial
**Language**: Tiếng Việt
**Source Issues**: `WASHVN/Temps/isuse/isuse1.md`, `WASHVN/Temps/isuse/architecture_critique.md`
**Target Design Base**: `WASHVN/Temps/clean/`

---

## §1: Problem Summary

Hệ thống WASHVN v2.0 (Mechanical Pipeline) bị phản biện với **6 điểm yếu / rủi ro kiến trúc** đã được xác thực (Verdict: ĐÚNG). Các vấn đề này không phải sơ suất ngẫu nhiên mà là hệ quả của các quyết định đánh đổi kiến trúc (Architectural Trade-offs) chủ động giữa: Rigidity vs Resilience, Token Economy vs Granular Diagnostics, Latency vs Depth.

---

## §2: Entry Point

| Field | Value |
|:---|:---|
| **Entry Point** | `WASHVN/Temps/clean/architecture-design.md` (thiết kế tổng thể pipeline) |
| **Trigger** | Architecture Critique tại `isuse/architecture_critique.md` |
| **Feature Area** | WASHVN Master Skill Suite — Mechanical Pipeline v2.0 |

---

## §3: Scope Definition

### 3.1 Problem Area

Toàn bộ 6 vấn đề đều nằm trong thiết kế **Mechanical Pipeline v2.0** của WASHVN, thuộc các module:

1. Phase Compression (Branch A) — Nhánh tối ưu cho tác vụ đơn giản
2. Drift Detection & Sampling Audit — Lớp kiểm chứng ngữ nghĩa
3. Quality Gates System — Hệ thống chốt chặn chất lượng
4. Reflection Cache — Bộ nhớ đệm tư duy sâu
5. YAML Resilience — Lớp chịu lỗi YAML
6. Maintenance & Operations — Vận hành tổng thể

### 3.2 Boundary

```
Giới hạn trong phạm vi:
  - Các file đặc tả bổ sung (supplements) tại clean/supplements/
  - File quality gates: clean/quality-gates-matrix.md
  - File orchestration: clean/orchestrator-agent-spec.md
  - File state/protocols: clean/protocols-and-state-spec.md
  - File kiến trúc tổng: clean/architecture-design.md

Không bao gồm:
  - Source code implementation (chưa có)
  - raw/ver-3/ skills source
  - Runtime .claude/skills/
```

---

## §4: Impact Analysis

### 4.1 Direct Impact

| # | Issue | Files bị ảnh hưởng trực tiếp | Lines xác nhận |
|:---:|:---|:---|:---:|
| 1 | Phase Compression Trade-offs | `supplements/phase-compression-spec.md` | L250-L268 |
| 2 | PASS-form FAIL-meaning + Sampling Audit | `supplements/sampling-audit-spec.md` | L40-L47, L86-L98 |
| 3 | Soft Gates Quality Gaps | `raw/build-stage-standards.md` | L75, L101, L103 |
| 4 | Reflection Cache Late Detection | `supplements/reflection-cache-spec.md` | L330-L337, L371-L372 |
| 5 | YAML Resilience Graceful Degradation | `supplements/yaml-resilience-spec.md` | L204-L226 |
| 6 | Maintenance Burden | `architecture-design.md`, toàn bộ supplements | Cross-cutting |

### 4.2 Indirect Impact

**Upstream (ảnh hưởng đến stages trước):**
- Issue 1 (Phase Compression): Ảnh hưởng đến **Stage 0 (Explorer)**, **Stage 1 (Architect)** vì phải thiết kế prompt combined role thay vì stage riêng
- Issue 4 (Reflection Cache): **Stage 0 (BA Elicitor)** bị kéo về để depth recovery khi lỗi phát hiện muộn
- Issue 2 (Sampling Audit): **Stage 1.5 (Gatekeeper)** không thể phát hiện semantic drift → đẩy trách nhiệm lên Oracle audit

**Downstream (ảnh hưởng đến stages sau):**
- Issue 3 (Soft Gates): **Stage 3 (Builder)** nhận plan có thể chứa placeholder code nhưng vẫn pass build
- Issue 5 (YAML Degradation): **Orchestrator (Branch B)** skip orchestration plan, **Planner** skip quality gates → output thiếu chức năng
- Issue 6 (Maintenance): **Human Operator** chịu gánh nặng đồng bộ chéo giữa các file đặc tả

**Data Flow bị ảnh hưởng:**
- Thought cache → Hydrator → Builder: Phát hiện thiếu chiều sâu quá muộn (Issue 4)
- Design intent → todo.md: Intent bị mất trong quá trình truyền đạt (Issue 2)
- Token budget → prompt design: Prompt phình to 150% làm giảm hiệu quả tiết kiệm (Issue 1)

**API Contracts bị break:**
- Fallback matrix F1-F9 bị thay thế bằng PC-1 đến PC-4 (Issue 1)
- `_state.yaml.phase_retry_history` thay thế `stage_status` tracking chi tiết (Issue 1)
- `artifact_warnings` field mới cho phép skip step thay vì hard halt (Issue 5)

---

## §5: Call Chain

```
Issue 1 (Phase Compression)
  ├── Trực tiếp: phase-compression-spec.md §4.2 (Trade-off table)
  ├── Gọi đến:  pipeline flow → Branch A → 3 phases gộp (PC-1..PC-4)
  └── Được gọi từ: architecture-design.md (decision record)

Issue 2 (PASS-form FAIL-meaning)
  ├── Trực tiếp: sampling-audit-spec.md §1.1 (Drift Detector limits)
  ├── Gọi đến: Oracle audit, Human audit modes
  └── Được gọi từ: Stage 2.5 (Drift Detector) → Stage 3 (Builder)

Issue 3 (Soft Gates)
  ├── Trực tiếp: raw/build-stage-standards.md (BUILD-2.1, BUILD-3.1)
  ├── Gọi đến: Stage 3 Builder delivery check
  └── Được gọi từ: architecture-design.md (quality gates policy)

Issue 4 (Reflection Cache)
  ├── Trực tiếp: reflection-cache-spec.md §5 (Fallback F16-F18)
  ├── Gọi đến: Stage 0 BA Elicitor (depth recovery)
  └── Được gọi từ: Stage 1.7 Hydrator (không detection) → Stage 3 Builder

Issue 5 (YAML Resilience)
  ├── Trực tiếp: yaml-resilience-spec.md §5 (Graceful Degradation)
  ├── Gọi đến: Orchestrator, Planner (skip step behavior)
  └── Được gọi từ: Context Bus → artifact_warnings → stage downstream

Issue 6 (Maintenance Burden)
  └── Cross-cutting: tất cả supplements + architecture-design.md
```

---

## §6: Data Flow

### 6.1 Input

| Input | Source | Description |
|:---|:---|:---|
| Issue analysis | `isuse/isuse1.md` | Phân tích 6 nhược điểm chi tiết |
| Verdict & evidence | `isuse/architecture_critique.md` | Đối chiếu chứng cứ, phán quyết ĐÚNG |
| Spec files | `clean/supplements/*.md` | Bằng chứng thiết kế gốc |

### 6.2 Output

| Output | Destination | Description |
|:---|:---|:---|
| Scope document | `clean/scope.washvn-v2-critique.*.md` | File này — context cho fix phase |

### 6.3 Dependency Map (quan hệ giữa các issue — không phải priority)

```yaml
relationship_map:
  tightly_coupled:
    - Issue 4 (Reflection Cache) ↔ Stage 0 (BA Elicitor) → phát hiện muộn, chi phí rollback cao
    - Issue 2 (Semantic Audit) ↔ Issue 5 (YAML Degradation) → cùng thuộc lớp kiểm soát chất lượng
    
  loosely_coupled:
    - Issue 1 (Phase Compression) → độc lập, không blocking issue khác
    - Issue 3 (Soft Gates) → có thể xử lý riêng
    
  cross_cutting:
    - Issue 6 (Maintenance) → chịu ảnh hưởng từ resolution của các issue khác
```

---

## §7: Affected Components

### 7.1 Files

| File | Role | Issues liên quan |
|:---|:---|:---:|
| `clean/architecture-design.md` | Thiết kế tổng thể | 1, 6 |
| `clean/supplements/phase-compression-spec.md` | Đặc tả Phase Compression | 1 |
| `clean/supplements/sampling-audit-spec.md` | Đặc tả Sampling Audit | 2 |
| `clean/quality-gates-matrix.md` | Ma trận Quality Gates | 3 |
| `raw/build-stage-standards.md` | Build stage standards (raw source) | 3 |
| `clean/supplements/reflection-cache-spec.md` | Đặc tả Reflection Cache | 4 |
| `clean/supplements/yaml-resilience-spec.md` | Đặc tả YAML Resilience | 5 |
| `clean/orchestrator-agent-spec.md` | Đặc tả Orchestrator | 5, 6 |
| `clean/protocols-and-state-spec.md` | State & protocols | 4, 5, 6 |
| `clean/supplements/depth-gate-criteria.md` | Depth gate criteria | 4 |

### 7.2 Stages/Agents ảnh hưởng

| Stage/Agent | Issue | Impact |
|:---|:---:|:---|
| Stage 0 (BA Elicitor) | 4 | Bị kéo về depth recovery (F16-F18) |
| Stage 1 (Architect) | 1, 6 | Phải thiết kế combined role prompts |
| Stage 1.5 (Gatekeeper) | 2, 4 | Không detect được semantic drift; không check thought-cache |
| Stage 1.7 (Hydrator) | 4 | Không chạm vào thought-cache → điểm mù |
| Stage 2 (Planner) | 2, 5 | Có thể nhận plan sai ngữ nghĩa; skip quality gates nếu matrix dangling |
| Stage 2.5 (Drift Detector) | 2 | Chỉ check form, không check meaning |
| Stage 3 (Builder) | 2, 3, 4 | Build sai plan; nhận placeholder code; phát hiện cache thiếu quá muộn |
| Orchestrator (Branch B) | 5 | Skip orchestration nếu plan dangling |
| Oracle Audit | 2 | Chỉ audit 10-20% plans |
| Human Operator | 6 | Gánh nặng đồng bộ chéo |

---

## §8: Evidence

<evidence>
  <issue>1 — Phase Compression Trade-offs</issue>
  <file>supplements/phase-compression-spec.md</file>
  <lines>L250-L268</lines>
  <finding>
    Bảng trade-off (L263-268) xác nhận mất Isolation, Reusability, Granular Fallback.
    Note (L258-260) thừa nhận token saving chỉ ~50-56% (không 62.5%) vì prompt phình to 150%.
    Internal retry loop PC-1 đến PC-4 (L336-348) thay thế ma trận F1-F9.
  </finding>
  <confidence>95%</confidence>
</evidence>

<evidence>
  <issue>2 — PASS-form FAIL-meaning & Sampling Audit</issue>
  <file>supplements/sampling-audit-spec.md</file>
  <lines>L46-L47, L86-L98</lines>
  <finding>
    L46-47 thừa nhận: "PASS-form nhưng FAIL-meaning — Drift Detector không có cơ chế phát hiện".
    L86-98 định nghĩa sampling rate: Default 20%, Relaxation 10% → 80-90% plans không được audit.
    L125-141: Human Audit mode tạo bottleneck vì chờ user review thủ công.
  </finding>
  <confidence>95%</confidence>
</evidence>

<evidence>
  <issue>3 — Soft Gates Quality Gaps</issue>
  <file>raw/build-stage-standards.md</file>
  <lines>L75, L101, L103</lines>
  <finding>
    L75: Token Budget < 700 tokens được xếp là "Nice-to-Have".
    L101: BUILD-2.1 (Placeholder Density ≥ 10): Soft Gate (Nice-to-Have) — "Chỉ đưa ra cảnh báo tối ưu hóa, không chặn build".
    L103: BUILD-3.1 (Token Budget > 700 tokens): Nice-to-Have (Mềm) — "Chỉ đưa ra cảnh báo tối ưu, không chặn build".
    Cả hai đều cho phép code chưa hoàn thiện / context phình to lọt qua Delivery.
  </finding>
  <confidence>95%</confidence>
</evidence>

<evidence>
  <issue>4 — Reflection Cache Late Detection</issue>
  <file>supplements/reflection-cache-spec.md</file>
  <lines>L330-L337, L371-L372</lines>
  <finding>
    F16-F18 fallback quay về Stage 0 (L330-337).
    L371-372: "Fallback F16, F17, F18 là thủ công — không có automatic detection mechanism ở Stage 1.7 Hydrator".
    Lỗi chỉ phát hiện ở Stage 3 → chi phí rollback cao nhất.
  </finding>
  <confidence>95%</confidence>
</evidence>

<evidence>
  <issue>5 — YAML Resilience Graceful Degradation</issue>
  <file>supplements/yaml-resilience-spec.md</file>
  <lines>L204-L226</lines>
  <finding>
    L204-226: Level 3 cross-ref check không Hard Halt khi phát hiện dangling ref.
    Stage downstream skip step phụ thuộc artifact → không crash, chỉ log warning.
    L223-226: Orchestration-plan dangling → Orchestrator chỉ build single skill.
    Quality-matrix dangling → Planner skip quality gate validation.
  </finding>
  <confidence>95%</confidence>
</evidence>

<evidence>
  <issue>6 — Maintenance Burden</issue>
  <files>architecture-design.md, supplements/*.md, orchestrator-agent-spec.md, protocols-and-state-spec.md</files>
  <finding>
    Hệ quả cấu trúc Multi-Agent đa tầng: phân mảnh tri thức thành nhiều file.
    Mỗi thay đổi nhỏ đòi hỏi cập nhật thủ công: Mermaid diagrams, schema, config.
    Subagent phụ trợ (YAML Auto-repair, Spec Gatekeeper, Drift Detector) → latency tax.
  </finding>
  <confidence>85%</confidence>
</evidence>

---

## §9: Confidence Assessment

| Issue | Confidence | Basis |
|:---:|:---:|:---|
| 1 — Phase Compression | 95% | Spec tự thừa nhận trade-off + số liệu token |
| 2 — PASS-form FAIL-meaning | 95% | Spec tự thừa nhận lỗ hổng + sampling rate math |
| 3 — Soft Gates | 95% | Đã đọc raw/build-stage-standards.md (L75, L101, L103) |
| 4 — Reflection Cache | 95% | Spec thừa nhận không có automatic detection |
| 5 — YAML Degradation | 95% | Spec mô tả rõ hành vi graceful degradation |
| 6 — Maintenance | 85% | Phân tích hệ quả, không có spec riêng |

**Overall Confidence**: 95%

---

## §10: Open Questions (đã clarify)

1. ~~**Issue 3**: File `build-stage-standards.md` nằm ở raw hay clean?~~ → **Đã xác nhận**: tại `raw/build-stage-standards.md`
2. ~~**Issue 6**: Có metric nào đo lường cụ thể latency tax không?~~ → **Đã clarify**: Chưa có metric — đây là phase thiết kế kiến trúc, chưa đến mức đo lường
3. ~~**Priority**: Cần xác định thứ tự ưu tiên fix?~~ → **Đã clarify**: Chưa cần xác định thứ tự ưu tiên ở phase này
4. ~~**Scope**: Có muốn mở rộng scope phân tích không?~~ → **Đã clarify**: Scope đóng gói trong phase thiết kế kiến trúc, không mở rộng
5. ~~**Remediation preference**: Ưu tiên tighten gates hay redesign?~~ → **Đã clarify**: Ưu tiên hiện tại là **mở khóa sức mạnh LLM** (intelligence, knowledge, deep thinking) — không phải tighten gates theo hướng cứng hóa kiểm soát

### Constraint bổ sung từ thiết kế

```yaml
design_priority:
  goal: "Unlock LLM power — intelligence, knowledge base, deep thinking"
  implication: >
    Các issue 1-6 cần được đánh giá lại dưới góc nhìn này:
    Không phải "làm sao để kiểm soát LLM chặt hơn"
    Mà là "làm sao để tận dụng tối đa sức mạnh LLM mà vẫn quản lý được rủi ro"
  
  design_tension:
    trade_off: "Kiểm soát càng chặt → LLM càng bị gò bó, mất đi sự sáng tạo và chiều sâu tư duy"
    opportunity: "Các issue hiện tại (Soft Gates, Graceful Degradation, Sampling Audit) có thể là intentional design choice để LLM có không gian thinking"
```

---

## §11: Design Tension Heatmap (theo mức độ ảnh hưởng đến design goal)

> **Lưu ý**: Theo design priority hiện tại (mở khóa sức mạnh LLM), các "issue" này được nhìn nhận là **design tensions** — không phải bug cần fix, mà là trade-offs cần cân bằng.

| Mức độ tension | Issue | Bản chất |
|:---:|:---|:---|
| 🔴 **Cao** | 4 — Reflection Cache Late Detection | Mâu thuẫn giữa deep thinking (cần thought-cache) và phát hiện lỗi sớm |
| 🔴 **Cao** | 5 — YAML Graceful Degradation | Mâu thuẫn giữa resilience (không crash) và đảm bảo完整性 đầu ra |
| 🟠 **Trung-Cao** | 2 — Semantic Audit Gap | Mâu thuẫn giữa LLM freedom (không bị kiểm soát quá mức) và độ chính xác |
| 🟠 **Trung-Cao** | 3 — Soft Gates | Mâu thuẫn giữa flexibility (cho LLM không gian sáng tạo) và chất lượng đầu ra |
| 🟡 **Trung bình** | 1 — Phase Compression Trade-offs | Trade-off đã biết: tiết kiệm token vs mất granularity — intentional choice |
| 🟢 **Thấp** | 6 — Maintenance Burden | Hệ quả tự nhiên của multi-agent architecture — operational cost |

---

**Document Status**: Context Complete — No Code Changes Made
**Current Design Priority**: Unlock LLM power — các design tensions cần được đánh giá dưới góc nhìn tận dụng tối đa intelligence, knowledge, deep thinking của LLM, thay vì cứng hóa kiểm soát.
