# Scope Document — Skill Architect Rebuild (Phase 6A)

**Date**: 2026-07-16
**Status**: Initial
**Feature**: `skill-architect-rebuild`
**Skill**: context-before-fix v1.0.0

---

## §1: Problem Summary

Skill Architect (Stage 1, L2) cần được rebuild toàn diện cho Phase 6A của Master Skill Suite Rebuild. Hiện tại:

- **ver-3 target** tại `skills/ver-3/skill-architect/SKILL.md` — **0 bytes** (empty stub)
- **Deploy target** tại `.claude/skills/skill-architect/SKILL.md` — **0 bytes** (empty stub)
- **Last working version** tại `skills/ver-0.0.2/skill-architect/` — sử dụng mô hình cũ (3-phase, §1-§10, 7 guardrails G1-G7) **không tương thích** với spec Phase 6A mới (6-phase, META-driven, quantified ACs)

Skill architect là **rào cản cứng (hard gate)** cho toàn bộ pipeline — nếu architect output không đạt META criteria, toàn bộ Phase 6A checkpoint (≥80% quality-matrix) sẽ FAIL, block Phase 6B.

- **Information Quality Density (IQD) gap**: synthesis-llm-principles.md specifies 7 nguyên lý (Domain Anchoring, Semantic over Ceremony, Context Pre-processing, Dual Knowledge Stream, Binary Mechanical Gates, Negative Space, Graceful Degradation) — architect output hiện tại thiếu metrics định lượng để đảm bảo mật độ chất lượng thông tin. IQD gap gây risk semantic void khi downstream (planner, builder, gatekeeper) consume architect artifacts. Cần define IQD thresholds (glossary size, semantic density %, gate binary determinism, dual stream completeness, degradation path coverage) trước khi build.

---

## §2: Entry Point

| Type | Location | Trạng thái |
|------|----------|-----------|
| **Pipeline role** | Stage 1 (L2) — Design & Contract layer | Cần rebuild |
| **Build source** | `skills/ver-3/skill-architect/` | Stub (chỉ .gitkeep) |
| **Deploy target** | `.claude/skills/skill-architect/` | Stub (chỉ .gitkeep) |
| **Old reference** | `skills/ver-0.0.2/skill-architect/` | Full content (outdated model) |
| **Spec reference** | `Temps/spec/architects/P1/`, `P3/`, `P7/` | Architecture spec |
| **Roadmap spec** | `skills/ver-3/roadmaps/06-skill-build-main-pipeline.md` (Stage 1) | Phase 6A requirements |

---

## §3: Scope Definition

### 3.1 In Scope

1. **SKILL.md** — Full 7-Zone skill với:
   - Frontmatter (name, description, suite, version, category, stage, target_variable, tags, when_to_use, output_contract)
   - 6-phase workflow (Read → Zone Mapping → Data Contracts → State Diagram → Must-Not Rules → Emit)
   - 6 Acceptance Criteria từ META (7-zone table, ≥1 Mermaid, ≥5 must_not/phase, ≥4 reverse questions, ≥2 stakeholders, constraint anchoring)
   - Token budget ≤700 tokens (~2800 chars body)
   - Zero placeholder strings

2. **Knowledge Zone** (3 files kế thừa + cập nhật từ ver-0.0.2):
   - `knowledge/architect.md` — 3 Pillars framework, 4 trace tags, anti-hallucination, META integration
   - `knowledge/design-exemplars.md` — Content spec, good/bad exemplars, anti-patterns, token budget table, zone decision tree
   - `knowledge/visualization-guidelines.md` — Mermaid diagram standards, "Show then explain" principle

3. **Templates Zone** (cập nhật từ ver-0.0.2):
   - `templates/design.md.template` — Output template aligned với design.schema.yaml và 7-Zone mapping

4. **Scripts Zone** (cập nhật từ ver-0.0.2):
   - `scripts/init_context.py` — Context directory initializer, kebab-case validation
   - `scripts/export-pipeline.py` — Pipeline diagram generator

5. **Loop Zone** (cập nhật từ ver-0.0.2):
   - `loop/design-checklist.md` — Quality checklist (human-readable)
   - `loop/design-checklist.yaml` — Machine-readable quality gates (transitional — xem §3.2)

6. **Data Zone** (MỚI — theo spec Phase 6A):
   - `data/drc.yaml` — DRC output contract

7. **Assets Zone**:
   - `assets/.gitkeep`

### 3.2 Out of Scope

| Item | Lý do |
|------|-------|
| Sửa schemas (`_shared/schemas/`) | Phase 4 đã done, architect chỉ consume, không modify |
| Sửa validators (`_shared/validators/`) | Phase 4 đã done |
| Sửa handoff validator logic | Thuộc Phase 8 (integration hardening) |
| Build `design-validator` agent | Đã deploy ở Phase 3 |
| Build `quality-scorer` agent | Đã deploy ở Phase 3 |
| Migration `knowleages/` → `knowledge/` | Out of scope per roadmap |
| K=8 chains generalization | Out of scope — giữ nguyên cơ chế cũ |
| consolidate .md + .yaml checklist | Chưa clear, retain cả 2 format cho Phase 8 |

### 3.3 Boundary

```
Input boundary: exploration.md + domain-handbook.md + criteria.md (từ skill-explorer + skill-knowledge-miner)
Output boundary: design.md + drc-skill-architect.yaml → production-quality-gatekeeper (Stage 1.5)
Quality boundary: META-1/2/3 validation (ARCH-1→4 gates)
Pipeline location: Phase 6A, Stage 1, L2 (Design & Contract layer)
```

---

## §4: Impact Analysis

### 4.1 Direct Impact

| Component | Impact | Chi tiết |
|-----------|--------|----------|
| `skills/ver-3/skill-architect/SKILL.md` | **Full rewrite** | Từ empty stub → full 7-Zone content |
| `.claude/skills/skill-architect/SKILL.md` | **Full write** | Deploy từ ver-3 build source |
| `skills/ver-3/roadmaps/index.md` | **Status update** | Phase 6A skill-architect từ pending → built |
| `plan-checklist.2026-07-07.md` | **Status update** | §11 Phase 6A skill-architect tasks đánh dấu done |
| `skills-registry.json` | **Registry update** | skill-architect entry lifecycle → built/installed |

### 4.2 Indirect Impact

| Component | Impact | Chi tiết |
|-----------|--------|----------|
| `production-quality-gatekeeper` (Stage 1.5) | **Downstream consumer** | Gatekeeper validates architect's output — cần architect output đúng format |
| `skill-planner` (Stage 2) | **Downstream consumer** | Planner decompose design.md thành tasks — phụ thuộc vào zone mapping |
| `skill-builder` (Stage 3) | **Downstream consumer (gián tiếp)** | Builder implement từ plan của planner |
| `P3/drift-detection.md` | **Feedback loop** | F8 major drift → architect revise design |
| `P1/spec-gatekeeper.md` | **Validation gate** | Gatekeeper validate design tại S1.5 |
| Phase 6B execution cluster | **Checkpoint gate** | skill-architect output quality ảnh hưởng checkpoint ≥80% |
| `P7/delta-planning.md` | **UPDATE mode** | Architect design.md vN+1 cho UPDATE scenario |

### 4.3 Architectural Defects Addressed

- **Γ-1 (Self-Referential Blindness)**: Architect produce design.md với trace tags rõ ràng, anti-hallucination checklist, external co-validation
- **Γ-4 (Hydrator Info Loss)**: architect output phải đủ precision để hydrator không cần guess

---

## §5: Knowledge Map & Information Architecture

### 5.1 Core LLM Semantic Activation Keywords & Architectural Pattern Catalog

Dựa trên `synthesis-llm-principles.md` và cơ chế biến đổi văn bản thành ID string / embedding vector trong Vector Database (như HNSW, FAISS, Milvus, Chroma), LLM cần các **mỏ neo từ vựng kiến trúc đậm đặc (High Semantic Density Keywords)** để tự động kích hoạt (activate) các cụm vector tri thức chuyên sâu trong không gian đa chiều (high-dimensional vector space).

Khi mật độ từ khóa ngữ nghĩa cao được nạp vào context, trọng số chú ý (attention weight) của Transformer model được dồn mạnh vào không gian kỹ thuật/kiến trúc, loại bỏ hiện tượng "Semantic Void" (khoảng trống ngữ nghĩa) và làm tăng độ chính xác của output từ downstream agents (Planner, Builder, Gatekeeper).

#### 5.1.1 Danh mục Keyword & Pattern Kiến trúc Đậm đặc Ngữ nghĩa (Architectural Semantic Density Matrix)

**1. Domain Anchoring & Domain-Driven Scaffolding (Nguyên lý #1)**:
```text
[Bối cảnh tiếng Việt] kiến trúc phần mềm, phân rã miền (domain decomposition), ranh giới bối cảnh (bounded context), mỏ neo ngữ nghĩa (semantic anchor), quy ước dữ liệu (data contract), quy định cấm kỵ (must_not rules), trạng thái chuyển giao (state transition), ràng buộc kỹ thuật (technical constraint), luồng nhận thức (cognitive stream), ma trận chất lượng (quality matrix)

[English Vector Triggers] domain-driven architecture, bounded context, ubiquitous language, architectural decomposition, structural scaffolding, domain entity mapping, semantic anchor, cognitive depth, domain invariant, architectural intent, contextual boundary, system responsibility matrix
```

**2. Semantic Density & Contract Formalization (Nguyên lý #2)**:
```text
data contract, input_schema, output_schema, dynamic routing contract (DRC), state & signal protocol (SSP), 7-zone architectural mapping, Progressive Disclosure, zero-placeholder constraint, deterministic interface, schema validation, payload boundary, idempotency key, immutable ledger, format resilience
```

**3. Dual Context & Reflection Cache Ingestion (Nguyên lý #4)**:
```text
technical scaffolding, cognitive depth, hydrated context, thought cache, thought block (>200 words), reflection cache, stakeholder empathy, defensive reasoning, edge-case topology, non-functional requirements (NFR), domain glossary, anti-pattern taxonomy, architectural exemplar, decision rationale
```

**4. Binary Quality Gates & Mechanical Verification (Nguyên lý #5)**:
```text
META-1 structural gate, META-2 semantic depth gate (S1-S4 AND), META-3 mechanical gate, ARCH-1 semantic anchor gate, ARCH-2 data contract gate, ARCH-3 zone mapping gate, ARCH-4 state machine gate, binary deterministic check, pass/fail assertion, automated regex verification, hard halt, soft gate (BUILD-3.1 token budget), graceful degradation
```

**5. Negative Space & Defense-in-Depth Patterns (Nguyên lý #6)**:
```text
negation density (S1), anti-pattern guardrail, negative space definition, kill switch, hard constraint, non-negotiable must_not, scope creep isolation, anti-hallucination checklist, zero-mock policy, fault isolation boundary, threat mitigation taxonomy
```

**6. State Machine & Workflow Orchestration Patterns**:
```text
finite state machine (FSM), state transition matrix, deterministic state graph, state invariant, entry/exit criteria, state ledger (_state.yaml), fallback route (F1-F19), phase compression (Branch A D1-D3), parallel micro-skill orchestration (Branch B), state persistence engine
```

### 5.1.2 Depth Signal Mapping (META-2.1 alignment)

Mapping từ 4 Depth Signals (synthesis-llm-principles.md §2.4) vào architect output:

| Signal | Định nghĩa | Áp dụng trong architect output |
|--------|-----------|-------------------------------|
| **S1 — Negation Density** | Mật độ must_not, anti-pattern, negative space | ≥5 must_not rules/phase trong design.md (§5); anti-pattern section trong knowledge/architect.md |
| **S2 — Reverse Question** | Câu hỏi phản biện "điều gì có thể sai" | ≥4 reverse questions/aspect trong design.md (§8); defensive reasoning trong knowledge/ |
| **S3 — Multi-Stakeholder** | Phân tích ai bị ảnh hưởng | ≥2 stakeholders trong design.md (§7); stakeholder empathy trong thought blocks |
| **S4 — Constraint Anchoring** | Ràng buộc cụ thể từ thực tế | Token budget ≤700; NFR constraints; schema validation rules; input/output contract alignment |

**Semantic Density Target per Artifact**:

| Artifact | Token Target | Semantic Density Target | Measurement |
|----------|-------------|------------------------|-------------|
| SKILL.md | ≤700 tokens | ≥40% meaningful keywords/total | `keyword_token_count / total_token_count` — excludes structural YAML keys, markdown formatting |
| design.md | ~1500-2500 tokens | ≥50% technical + domain terms | Technical terms + domain terms / total content tokens |
| knowledge/*.md | ~500-1500 tokens/file | ≥35% glossary + anti-pattern | Domain glossary + anti-pattern descriptions / total |

### 5.2 Existing Knowledge Resources

| Resource | Location | Giá trị | Sử dụng cho |
|----------|----------|---------|-------------|
| **Old skill-architect** | `skills/ver-0.0.2/skill-architect/` | 13 files, 3-phase model, 7 guardrails G1-G7 | Kế thừa 3 knowledge docs, template design, checklist |
| **Synthesis LLM Principles** | `/synthesis-llm-principles.md` | 7 nguyên lý cốt lõi, 4 depth signals, SCS framework | Semantic anchor definition, quality gate design |
| **Spec/architects shared** | `Temps/spec/architects/shared/` | 4 files: architecture overview, glossary, quality gates, pipeline flowchart | Architecture alignment, terminology |
| **Spec P1** | `Temps/spec/architects/P1/` | 5 files: SCS routing, META criteria, gatekeeper, re-validation | Quality framework cho architect output |
| **Spec P3** | `Temps/spec/architects/P3/` | 5 files: drift detection, plan gate, sampling audit, fallback | Fallback awareness (F8/F9 → architect) |
| **Spec P7** | `Temps/spec/architects/P7/` | 5 files: delta planning, rebuild workflow, in-place builder, token budget | Downstream consumer awareness |
| **Phase 6A roadmap** | `skills/ver-3/roadmaps/06-skill-build-main-pipeline.md` | Stage 1 spec: 6 phases, 6 ACs | Requirement spec cho rebuild |
| **Plan checklist** | `docs/plans/plan-checklist.2026-07-07.md` | Phase 6A status, dependencies, checkpoint gate | Progress tracking |
| **Role indexes** | `Temps/spec/architects/indexes/by-role.md` | Architect maps to P0/P1/P3/P7 | Scope boundary |
| **Built-unit index** | `Temps/spec/architects/indexes/by-built-unit.md` | skill-architect = Stage 1, L2, lifecycle "built" | Pipeline position |

### 5.3 Key Inconsistencies cần resolve

1. **Section count**: Old template có §1-§12 nhưng design-exemplars.md flag sections ngoài §1-§10 là anti-pattern → **resolve**: giữ §1-§10, không dùng §11/§12
2. **Template bugs**: Old template §8 chỉ có 1 risk row, cần ≥3. §6 chỉ 1 interaction point.
3. **Checklist format**: Cả .md và .yaml — retain cả 2, .md cho human reading, .yaml cho machine validation
4. **Confidence/K=8**: Cơ chế cũ gắn với specific LLM API chains — cần generalization hoặc giữ nguyên dạng heuristic
5. **Token budget**: Old spec dùng soft gate 700 tokens, design-exemplars nói 1500-2500 — cần align với BUILD-3.1 (700 tokens soft gate)

### 5.4 Information Quality Density Specification

Based on synthesis-llm-principles.md 7 nguyên lý, architect output phải đạt các ngưỡng IQD sau:

#### 5.4.1 Domain Anchoring Quality

| Metric | Threshold | Measurement Method | Artifact |
|--------|-----------|-------------------|----------|
| Glossary size | ≥10 domain-specific terms | Count distinct technical terms in knowledge/architect.md | knowledge/architect.md |
| Semantic anchor density | ≥1 anchor per 200 tokens | `anchor_count / section_token_count` trong mỗi section của design.md | design.md (all sections) |
| Thought block depth | ≥200 từ/block nếu dùng thought-cache | Word count per thought block | thought-cache.yaml (if used) |
| Dual anchor types | Both technical + stakeholder | Check presence of both: glossary terms AND stakeholder empathy | design.md §1 + §7 |

#### 5.4.2 Semantic Density Thresholds

| Metric | Min | Target | Max | Notes |
|--------|-----|--------|-----|-------|
| Keyword density (technical) | 30% | 40% | 60% | `(domain_keywords + technical_keywords) / total_words` per section |
| Meaningful content ratio | 60% | 75% | 100% | `(total_words - structural_words - formatting_chars) / total_words` |
| Prose-to-contract ratio | 1:1 | 1:2 | 1:4 | Prose sentences vs. structured data (tables, YAML, schemas) |

#### 5.4.3 Binary Gate Mechanical Verification

Mọi gate trong architect output (META-1/2/3, ARCH-1→4, AC-1→6) phải có:

```yaml
gate:
  name: [gate name]
  type: binary  # MUST be binary — no scoring scales
  pass_condition: [deterministic condition, verifiable by regex/script]
  fail_behavior: [FALLBACK ROUTE or HARD HALT]
  verification_method: "[command or script to verify]"
```

**Current gate coverage trong architect scope**:

| Gate | Binary? | PASS condition | Fail behavior |
|------|---------|---------------|---------------|
| META-1 (Structural) | ✅ | Domain anchor present + 6 phases | F3 → revise design |
| META-2 (Semantic Depth) | ✅ | 4/4 Depth Signals (S1 AND S2 AND S3 AND S4) | F3 → revise design |
| META-3 (Mechanical) | ✅ | PASS/FAIL gates pass, negative space present | F3 → revise design |
| ARCH-1 (Semantic Anchors) | ✅ | design.md §1 has anchoring keywords | F3 → revise |
| ARCH-2 (Data Contracts) | ✅ | design.md §3 has valid input/output schemas | F3 → revise |
| ARCH-3 (Zone Mapping) | ✅ | design.md §2 has complete 7-zone table | F3 → revise |
| ARCH-4 (State Machine) | ✅ | design.md §4 has valid stateDiagram | F3 → revise |
| BUILD-3.1 (Token Budget) | ⚠️ Soft Gate | ≤700 tokens | Warning → REV-3.0 auto-refactor trigger |

#### 5.4.4 Dual Knowledge Stream Provision

Architect phải đảm bảo downstream (planner + builder) có cả technical VÀ cognitive context:

| Consumer | Technical (required) | Cognitive (optional/required) |
|----------|---------------------|------------------------------|
| Gatekeeper (S1.5) | design.md + drc.yaml | — (not needed) |
| Planner (S2) | design.md + hydrated zone map | thought-cache.yaml (optional) |
| Builder (S3) | design.md + data contracts + templates | knowledge/*.md (required) + scripts (required) |

**Architect responsibility**: Tạo design.md và knowledge/*.md có cognitive depth đủ để builder không cần guess semantic intent — giải quyết Γ-4 Hydrator Info Loss.

#### 5.4.5 Graceful Degradation Paths

| Component | Degraded Mode | Trigger | Recovery |
|-----------|--------------|---------|----------|
| design.md (if incomplete) | Flag `degraded: true` in frontmatter | META gate fail non-critical | Revise before planner dispatch |
| knowledge/ (missing exemplars) | Architect inject exemplars inline | No `domain-exemplars.md` | Create stub, flag in design.md §10 |
| templates/ (schema mismatch) | Manual alignment notation in design.md metadata | design.schema.yaml mismatch | Flag as open issue, resolve in design phase |
| Token budget exceeded | Soft gate warning (BUILD-3.1) | >700 tokens | REV-3.0 auto-refactor on deploy |

---

## §6: Call Chain

### 6.1 Upstream (Input providers)

```
BA Pipeline (P5)
  └─ ba-elicitor → thought-cache.yaml, elicitation-report.md
  └─ ba-analyst → analysis-report.md  
  └─ ba-synthesizer → business-analysis.md
       │
       ▼
Skill Explorer (Phase 6A, Stage 0)
  └─ exploration.md (SCS factors, domain scan)
  └─ criteria.md (acceptance criteria)
       │
       ▼
Skill Knowledge Miner (Phase 6A, Stage 0.5)
  └─ domain-handbook.md (glossary, anti-patterns, exemplars)
       │
       ▼
SKILL-ARCHITECT (Phase 6A, Stage 1) ← YOU ARE HERE
```

### 6.2 Downstream (Output consumers)

```
SKILL-ARCHITECT
  └─ design.md ─────────────────────────────────────────┐
  └─ drc-skill-architect.yaml ──────────────────────────┤
                                                        │
                                                        ▼
                                  Production Quality Gatekeeper (Stage 1.5)
                                    ├── PASS → skill-planner (Stage 2)
                                    └── FAIL (F3) → BACK TO ARCHITECT (revise design)
                                                        │
                                                        ▼
                                  Skill Planner (Stage 2)
                                    └─ todo.md (DAG tasks)
                                                        │
                                                        ▼
                                  Drift Detector (P3, Stage 2.5)
                                    ├── PASS → skill-builder (Stage 3)
                                    ├── Minor drift (F7) → planner re-plan
                                    ├── Major drift (F8) → BACK TO ARCHITECT (revise design)
                                    └── Semantic FAIL (F8-EXT) → ARCHITECT or BA
                                                        │
                                                        ▼
                                  Skill Builder (Stage 3) → Review → Sandbox → Deploy
```

### 6.3 Fallback Routes đến Architect

| Fallback | Origin | Condition | Architect Action |
|----------|--------|-----------|------------------|
| F3 | Gatekeeper (S1.5) | META criteria fail | Revise design |
| F4 | Gatekeeper (S1.5) | SCS score changes | Re-evaluate SCS + re-route |
| F8 | Drift Detector (S2.5) | Major drift | Revise design (Stage 1) |
| F8-EXT | Sampling Audit (S2.5) | Semantic meaning fail | Revise design hoặc re-elicit |
| F9 | Fallback Matrix | Design wrong domain | Re-anchor domain (Stage 0.5) |

---

## §7: Data Flow

### 7.1 Input Schema

| Tham số | Format | Source | Bắt buộc? |
|---------|--------|--------|-----------|
| `target_skill` | string (kebab-case) | User input | ✅ |
| `exploration.md` | Markdown + YAML frontmatter | skill-explorer | ✅ |
| `domain-handbook.md` | Markdown | skill-knowledge-miner | ✅ |
| `criteria.md` | Markdown | skill-explorer | ✅ |

### 7.2 Output Schema

| Artifact | Format | Schema | Consumer |
|----------|--------|--------|----------|
| `design.md` | Markdown + YAML frontmatter | `design.schema.yaml` | Gatekeeper + Planner |
| `drc-skill-architect.yaml` | YAML | DRC template | Pipeline orchestrator |

### 7.3 Output Contract (design.md) — 10 Sections

| § | Section | Format | Ghi sau phase | META alignment |
|---|---------|--------|---------------|----------------|
| §1 | Problem Statement | Markdown | Phase 1 read | — |
| §2 | 7-Zone Mapping Table | Markdown table | Phase 2 zone_mapping | ARCH-3.0 |
| §3 | Data Contracts | YAML blocks | Phase 3 data_contracts | ARCH-2.0 |
| §4 | State Diagram | Mermaid stateDiagram | Phase 4 state_diagram | ARCH-4.0 |
| §5 | Must-Not Rules | YAML list (≥5/phase) | Phase 5 must_not_rules | META-2.1 S1 |
| §6 | Mermaid Diagrams (≥1) | Mermaid (flow/sequence) | Phase 5 | ARCH-1.0 |
| §7 | Stakeholder Analysis (≥2) | Markdown table | Phase 5 | META-2.1 S3 |
| §8 | Reverse Questions (≥4/aspect) | Markdown list | Phase 5 | META-2.2 S2 |
| §9 | Risks & Mitigation | Markdown table (≥3) | Phase 5 | — |
| §10 | Metadata | YAML | Final | — |

---

## §8: Evidence

<evidence>
  <file>skills/ver-3/skill-architect/SKILL.md</file>
  <line>1</line>
  <finding>SKILL.md rỗng (0 bytes) — chưa có nội dung, cần full rebuild</finding>
</evidence>

<evidence>
  <file>.claude/skills/skill-architect/SKILL.md</file>
  <line>1</line>
  <finding>Deploy target cũng rỗng (0 bytes) — cần deploy từ ver-3 sau khi build</finding>
</evidence>

<evidence>
  <file>skills/ver-0.0.2/skill-architect/</file>
  <line>1</line>
  <finding>13 files tồn tại với 3-phase model (Collect→Analyze→Design), 7 guardrails G1-G7, 10-section output §1-§10. Có thể kế thừa knowledge/, templates/, loop/, scripts/ sau khi điều chỉnh cho Phase 6A spec</finding>
</evidence>

<evidence>
  <file>skills/ver-0.0.2/skill-architect/SKILL.md</file>
  <line>64</line>
  <finding>Pipeline design-only: architect → [design.md] → planner → [todo.md] → builder → [skill files] — cần giữ nguyên design-only constraint</finding>
</evidence>

<evidence>
  <file>skills/ver-3/roadmaps/06-skill-build-main-pipeline.md</file>
  <line>210-253</line>
  <finding>Stage 1 spec: 6 workflow phases, 6 ACs, 3 inputs (exploration.md + domain-handbook.md + criteria.md), 2 outputs (design.md + drc-skill-architect.yaml)</finding>
</evidence>

<evidence>
  <file>Temps/spec/architects/P1-scs-router-and-gatekeeper/meta-criteria.md</file>
  <line>1</line>
  <finding>META-1: Structural (Domain Anchor + Phase Deconstruction). META-2: Semantic Depth (4 signals AND — S1 Negation Density ≥5/phase, S2 Reverse Q, S3 Multi-Stakeholder ≥2, S4 Constraint Anchoring). META-3: Mechanical (PASS/FAIL, Negative Space, Sandbox)</finding>
</evidence>

<evidence>
  <file>Temps/spec/architects/shared/quality-gates-reference.md</file>
  <line>1</line>
  <finding>ARCH-1→4: Semantic Anchors, Data Contracts, Zone Mapping, State Machine — 4 gates architect phải pass</finding>
</evidence>

<evidence>
  <file>Temps/spec/architects/P3-drift-detector-and-plan-gate/drift-detection.md</file>
  <line>1</line>
  <finding>DRIFT-1.0→4.0: Back-link integrity, Contract alignment, State alignment, Zone alignment. Output verdict: Pass/Drift/Fail</finding>
</evidence>

<evidence>
  <file>synthesis-llm-principles.md</file>
  <line>1</line>
  <finding>7 nguyên lý cốt lõi: Domain Anchoring, Semantic over Ceremony, Context Pre-processing, Dual Knowledge Stream, Binary Mechanical Gates, Negative Space, Graceful Degradation</finding>
</evidence>

<evidence>
  <file>Temps/spec/architects/P7-delta-planning-and-builder/delta-planning.md</file>
  <line>1</line>
  <finding>UPDATE mode: architect tạo design.md vN+1 → delta planner diff với vN → tạo delta todo.md với 4 change types (create/modify/delete/unchanged)</finding>
</evidence>

<evidence>
  <file>Temps/spec/architects/P7-delta-planning-and-builder/token-budget-soft-gate.md</file>
  <line>1</line>
  <finding>Token budget ≤700 tokens = Soft Gate (BUILD-3.1). REV-3.0 auto-refactor trigger. Architect phải design SKILL.md structure accommodating budget constraints.</finding>
</evidence>

<evidence>
  <file>docs/plans/plan-checklist.2026-07-07.md</file>
  <line>630-686</line>
  <finding>Phase 6A status: in_progress, 3/12 tasks completed (skill-explorer + skill-knowledge-miner done). skill-architect is Skill 3, pending: SKILL.md + knowledge/templates/loop/scripts/data + gatekeeper audit + test + commit</finding>
</evidence>

---

## §9: Affected Components

### 9.1 Files cần tạo/sửa (trong skill-architect)

| Zone | File | Action |
|------|------|--------|
| Core | `SKILL.md` | **CREATE** — full rewrite (0 bytes → full content) |
| Knowledge | `knowledge/architect.md` | **UPDATE** — kế thừa từ ver-0.0.2, thêm META integration |
| Knowledge | `knowledge/design-exemplars.md` | **UPDATE** — fix section count inconsistency, thêm exemplars cho Phase 6A workflow |
| Knowledge | `knowledge/visualization-guidelines.md` | **UPDATE** — cập nhật diagram standards |
| Templates | `templates/design.md.template` | **UPDATE** — align với design.schema.yaml, fix template bugs |
| Scripts | `scripts/init_context.py` | **UPDATE** — kế thừa, thêm DRC contract init |
| Scripts | `scripts/export-pipeline.py` | **UPDATE** — kế thừa |
| Loop | `loop/design-checklist.md` | **UPDATE** — thêm META criteria checks, 6 ACs |
| Loop | `loop/design-checklist.yaml` | **UPDATE** — thêm machine-readable gates |
| Data | `data/drc.yaml` | **CREATE** — MỚI theo spec Phase 6A |
| Assets | `assets/.gitkeep` | Giữ nguyên |

### 9.2 Files bị ảnh hưởng ngoài skill

| File | Impact |
|------|--------|
| `skills/ver-3/roadmaps/index.md` | Update skill-architect status |
| `docs/plans/plan-checklist.2026-07-07.md` | Update §11 Phase 6A tasks |
| `.claude/skills/skill-architect/SKILL.md` | Deploy từ ver-3 build source |
| `skills-registry.json` | Update lifecycle status |
| `.claude/knowledge/agents/configuration.md` | Nếu architect reference thay đổi |

---

## §10: Confidence Assessment

| Area | Confidence | Evidence | Flags |
|------|-----------|----------|-------|
| Problem scope | 95% | Ver-3 SKILL.md là empty stub, ver-0.0.2 là outdated model | Không có ambiguity |
| Pipeline position | 95% | Stage 1 (L2) clearly defined in roadmaps + indexes | — |
| META criteria requirements | 90% | Directly from P1/meta-criteria.md + quality-gates-reference.md | Cần confirm exact META-2.2 spec |
| Input/output contracts | 85% | From Phase 6A roadmap + shared glossary | Cần verify design.schema.yaml hiện tại |
| Old knowledge inheritance | 85% | ver-0.0.2 knowledge files are comprehensive | Cần check META alignment |
| Inconsistencies | 70% | Section count mismatch, template bugs, token budget conflict | **Cần resolve trước khi build** |
| Fallback integration | 85% | F3/F8/F9 clearly defined | — |
| Phase 6A checkpoint impact | 90% | quality-matrix ≥80% gate | — |
| Semantic density coverage | 65% | synthesis-llm-principles §2 metrics chưa applied | Cần define IQD thresholds §5.4.1-§5.4.2 |
| Binary gate completeness | 85% | 8/8 gates defined, 1 soft gate | BUILD-3.1 soft gate cần monitoring |
| Dual context provision | 80% | Technical artifacts clear, cognitive path chưa explicit | knowledge/* role trong cognitive stream cần clarify |
| Graceful degradation coverage | 60% | Fallback matrix references F3/F8/F9 — chưa define degraded mode cho từng artifact | §5.4.5 added — cần verify đủ coverage |

**Overall Confidence**: 85% — Findings có IQD gaps cần resolve trước design phase, nhưng đã có §5.4 framework để address.

### Open Questions & Verification Results

1. **design.schema.yaml exact format**: ✅ **RESOLVED (Đã kiểm chứng)**
   - Path: `skills/ver-3/_shared/schemas/design.schema.yaml`
   - Keys bắt buộc: `skill_name`, `target_variable`, `zone_mapping` (7 zones), `data_contracts` (contract_id, description, input_schema, output_schema), `state_machine` (initial_state, states, transitions), `must_not_rules` (minItems: 5).
   - Keys mở rộng: `semantic_anchors`, `phase_deconstruction`, `quality_gates`.

2. **META-2.2 spec**: ✅ **RESOLVED (Đã kiểm chứng từ P1 spec)**
   - Reverse questioning framework giữ nguyên 4 aspects (S1 Negation Density, S2 Reverse Questioning ≥4 câu hỏi phản biện, S3 Multi-Stakeholder ≥2, S4 Constraint Anchoring).

3. **Token budget alignment**: ✅ **RESOLVED (Đã kiểm chứng từ P7 spec)**
   - `SKILL.md` body bắt buộc ≤700 tokens (~2800 kí tự body) — áp dụng Soft Gate (`BUILD-3.1`), kích hoạt `REV-3.0` auto-refactor trigger nếu vượt.
   - `design.md` artifact sinh ra có quy mô ~1500-2500 tokens (nằm ở level L2 artifact, không bị giới hạn 700 tokens của `SKILL.md`).

4. **DRC contract format**: ✅ **RESOLVED (Đã kiểm chứng)**
   - Path: `skills/ver-3/_shared/templates/drc_contract_template.yaml`
   - Cấu trúc DRC gồm: `skill_name`, `skill_version`, `suite`, `last_updated`, `inputs` (path_template, format, schema, required, consumed_by, downstream_phase), `outputs` (file_id, path_template, format, schema, lifecycle_status, versioning), `routing` (upstream_skills, downstream_skills, fallback_targets), `state_persistence` (context_bus_write, state_yaml_write, fields_to_write).

5. **K=8 generalization**: ✅ **RESOLVED**
   - Khái quát hóa cơ chế thành orchestration heuristic giữa các micro-skill subagents, loại bỏ phụ thuộc cứng vào LLM API vendor-specific.

---

## Document Status

**Next Phase**: skill-architect design (Stage 1)
**Verification Summary**:
1. 100% schema và template đã được kiểm chứng thực tế từ mã nguồn dự án (`design.schema.yaml`, `drc_contract_template.yaml`).
2. Danh mục từ khóa & pattern ngữ nghĩa đậm đặc (Architectural Semantic Density Matrix) đã được bổ sung nhằm tối ưu hóa việc chuyển hóa vector DB ID strings và Transformer attention triggering cho LLM.
3. Toàn bộ 5 Open Questions đã được giải đáp đầy đủ.

**NO CODE CHANGES — Context ready for fix phase**
