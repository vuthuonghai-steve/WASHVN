---
name: design-exemplars
version: 0.0.1
suite: WASHVN
tags: [architect, exemplars, templates, content-spec]
---

# Design Exemplars — skill-architect

## Nguồn gốc

File này bổ sung cho `format-standards.md` — cung cấp **content specification** và **exemplars** để LLM biết VIẾT GÌ và SAI GÌ.

---

## 1. Section Content Specification

Mỗi section cần có những phần tử cụ thể sau:

### §1 Problem Statement — BẮT BUỘC

```yaml
must_have:
  - pain_point: "Vấn đề cụ thể AI agent gặp phải"
  - user: "Ai sử dụng skill này (thường là AI Agent hoặc developer)"
  - expected_output: "Kết quả mong muốn sau khi dùng skill"
  - trigger_keywords: "Từ khóa kích hoạt skill"
```

### §2 Zone Mapping (7-Zone Table) — BẮT BUỘC

```yaml
must_have:
  - zone_table:
      - zone: "Tên zone (Core/Knowledge/Scripts/etc)"
        files: "DANH SÁCH FILE CỤ THỂ, không dùng xxx.md"
        purpose: "MÔ TẢ NGẮN nội dung file"
        constraints: "Giới hạn về token, schema, or phạm vi"
        required: "✅ hoặc ❌"
  - no_placeholders: "Mỗi dòng phải có tên file cụ thể"
```

### §3 Data Contracts — BẮT BUỘC (NEW for ver-3)

```yaml
must_have:
  - input_contracts: "Upstream artifacts với path, schema, required flag"
  - output_contracts: "Downstream artifacts với lifecycle, versioning, validation gate"
  - dual_knowledge_stream: "Technical + cognitive stream consumers"
```

### §4 State Diagram — BẮT BUỘC (thay thế §4 Folder Structure)

```yaml
must_have:
  - initial_state: "Idle"
  - states: "Tất cả phase + gate + fallback states"
  - transitions: "Từ mỗi state đến gate, gate đến next phase or fail"
  - fallback_routes: "F3 (gatekeeper revise) + F8 (drift revise)"
```

### §5 Must-Not Rules — BẮT BUỘC (NEW for ver-3)

```yaml
must_have:
  - per_phase_rules: "≥5 must_not rules per phase (6 phases × 5 = 30+ total)"
  - rule_structure:
      - id: "MN-X.Y"
        rule: "Must NOT ..."
        violation_example: "Cụ thể"
        gate: "ARCH-X or META-X"
```

### §6 Mermaid Diagrams — BẮT BUỘC

```yaml
must_have:
  - pipeline_diagram: "flowchart LR with 8-stage pipeline"
  - dual_stream_diagram: "flowchart TD technical + cognitive streams"
  - state_diagram: "stateDiagram-v2 from §4"
```

### §7 Stakeholder Analysis — BẮT BUỘC (thay thế §7 Progressive Disclosure)

```yaml
must_have:
  - stakeholder_table:
      - stakeholder: "Tên stakeholder"
        role: "Vai trò trong pipeline"
        pain_point: "Vấn đề họ gặp"
        expectation: "Họ cần gì từ architect"
        success_signal: "Làm sao biết thành công"
  - minimum_2_stakeholders
```

### §8 Reverse Questions — BẮT BUỘC (NEW for ver-3)

```yaml
must_have:
  - four_aspects:
      - S1: "Negation implications — ≥4 questions"
      - S2: "Design wrongness — ≥4 questions"
      - S3: "Stakeholder harm — ≥4 questions"
      - S4: "Constraint breaks — ≥4 questions"
```

### §9 Risks & Mitigation — BẮT BUỘC

```yaml
must_have:
  - risk_count: "Ít nhất 3 risks"
  - risk_structure:
      - risk_id: "R1, R2, R3..."
        likelihood: "Low/Medium/High"
        severity: "P0/P1/P2"
        impact: "Mô tả impact"
        mitigation: "Cụ thể, có action"
        contingency: "Nếu mitigation không đủ"
```

### §10 Metadata — CONTRACT

```yaml
must_have:
  - skill_name: "kebab-case"
  - skill_version: "3.0.0"
  - pipeline_stage: "Stage 1 (L2)"
  - iqd_thresholds: "glossary_size, anchor_density, thought_block_depth, dual_anchor_types"
  - drc_reference: "contract_path, template_path, required_fields"
  - quality_matrix: "META-1/2/3 weights + components + pass_threshold"
  - degradation: "graceful fallback paths"
```

---

## 2. Good Design.md Exemplar — 6-Phase Workflow with META/ARCH Gates

```markdown
---
skill_name: "example-skill"
target_variable: "target_skill"
zone_mapping: ...
data_contracts: ...
state_machine: ...
must_not_rules: ...
quality_gates: [ARCH-1 PASS, ARCH-2 PASS, ARCH-3 PASS, ARCH-4 PASS]
---

# example-skill — Architecture Design

## 1. Problem Statement
[TỪ USER INPUT] **Pain Point**: ...
[TỪ USER INPUT] **User**: ...
[TỪ USER INPUT] **Expected Output**: ...

**Architectural Patterns Applied**:
- `semantic-anchor-domain-decomposition`: domain glossary + thought blocks
- `binary-gate-deterministic-verification`: all PASS/FAIL
- `negative-space-per-phase`: ≥5 rules/phase

## 2. 7-Zone Mapping Table
| Zone | Files | Purpose | Constraints | Required? |
|------|-------|---------|-------------|-----------|
| Core | SKILL.md | L0 anchor | ≤700t | YES |
| Knowledge | knowledge/domain.md | Domain reference | glossary≥10 | YES |
| ... rest 5 zones | ... | ... | ... | ... |

## 3. Data Contracts
Input: exploration.md + domain-handbook.md + criteria.md. Output: design.md + drc.yaml.

## 4. State Diagram
[stateDiagram-v2 with Idle→P1→ARCH-1→P2→...→Complete + F3/F8 fallbacks]

## 5. Must-Not Rules
≥5 per phase, all with violation example + gate mapping.

## 6. Mermaid Diagrams
Pipeline flow (8-stage) + dual knowledge stream + state machine.

## 7. Stakeholder Analysis
≥2 stakeholders with pain point, expectation, success signal.

## 8. Reverse Questions
4 aspects × ≥4 questions = ≥16 total.

## 9. Risks & Mitigation
≥3 risks with likelihood, severity, impact, mitigation, contingency.

## 10. Metadata
IQD thresholds, DRC reference, quality matrix formula, gate status, degradation paths.
```

---

## 3. Bad Design.md Anti-Patterns

### ❌ Anti-pattern 1: Không có Trace Tags
**Vấn đề**: Không phân biệt được đâu là từ user, đâu là AI suy luận.
**Fix**: Thêm [TỪ USER INPUT], [GỢI Ý BỔ SUNG] trước mỗi assertion.

### ❌ Anti-pattern 2: Zone Mapping có placeholders
**Vấn đề**: Planner không biết tạo file gì.
**Fix**: Thay xxx.md bằng tên file cụ thể.

### ❌ Anti-pattern 3: §4 không khớp §3
**Vấn đề**: Handoff contract bị vi phạm.
**Fix**: §4 phải liệt kê chính xác files từ §3.

### ❌ Anti-pattern 4: §8 Risks không có mitigation cụ thể
**Vấn đề**: Risks không có action, không useful cho Builder.
**Fix**: Mỗi risk phải có severity + mitigation + contingency.

### ❌ Anti-pattern 5: Section ngoài spec (§11, §12)
**Vấn đề**: Output spec chỉ có §1-§10.
**Fix**: Chỉ viết §1-§10. Nếu cần bổ sung, gộp vào §10 Metadata.

---

## 4. Zone Decision Tree (ver-3 paths)

```mermaid
flowchart TD
    Start([New Skill]) --> CoreQ{Core Zone?}
    CoreQ -->|Yes| Core_Req[SKILL.md bắt buộc]
    CoreQ -->|No| Error_Missing[ERROR: Core là bắt buộc]

    Start --> KnowledgeQ{Knowledge cần thiết?}
    KnowledgeQ -->|Yes| Knowledge_Add[knowledge/*.md]
    KnowledgeQ -->|No| Knowledge_Skip[Không cần knowledge zone]

    Start --> ScriptQ{Cần automation?}
    ScriptQ -->|Yes| Scripts_Add[scripts/*.py]
    ScriptQ -->|No| Scripts_Skip[Không cần scripts zone]

    Start --> LoopQ{Cần verification?}
    LoopQ -->|Yes| Loop_Add[loop/design-checklist.md + .yaml]
    LoopQ -->|No| Loop_Skip[Không cần loop zone]

    Start --> DataQ{Cần DRC or config?}
    DataQ -->|Yes| Data_Add[data/drc.yaml + data/*.yaml]
    DataQ -->|No| Data_Skip[Không cần data zone]

    Start --> TemplateQ{Cần output format?}
    TemplateQ -->|Yes| Template_Add[templates/*.template]
    TemplateQ -->|No| Template_Skip[Không cần templates zone]

    Core_Req --> Result[Zone Mapping Complete]
    Knowledge_Add --> Result
    Scripts_Add --> Result
    Loop_Add --> Result
    Data_Add --> Result
    Template_Add --> Result

    Error_Missing -->|[fix]| Core_Req

    style Core_Req fill:#f8d7da,stroke:#721c24
    style Error_Missing fill:#ffebee,stroke:#c62828
    style Result fill:#e8f5e9,stroke:#2e7d32
```

---

## 5. Token Budget

```yaml
skill_architect_budget:
  SKILL_md_max: 700            # BUILD-3.1 soft gate — auto-refactor if exceeded
  design_md_target: 1500-2500  # Design output target range
  design_md_max: 4000          # Hard warning threshold

section_budget_design_md:
  §1_problem: "150-300t"
  §2_zone_mapping: "200-400t"
  §3_data_contracts: "300-500t"
  §4_state_diagram: "200-350t"
  §5_must_not_rules: "300-500t"
  §6_mermaid: "200-400t"
  §7_stakeholder: "200-350t"
  §8_reverse_questions: "300-500t"
  §9_risks: "200-350t"
  §10_metadata: "100-200t"
```

---

## 6. Quick Reference — Section Checklist

| § | Must Have | Must NOT Have |
|---|-----------|---------------|
| §1 | pain_point + user + expected_output | No trace tags |
| §2 | 7-zone table with specific filenames | xxx.md placeholders |
| §3 | I/O schemas + DRC routing + dual stream | Missing schema refs |
| §4 | stateDiagram-v2 with fallbacks | Non-deterministic transitions |
| §5 | ≥5 rules/phase (≥30 total) | <5/phase or generic rules |
| §6 | 8-stage pipeline + dual stream diagram | Missing META/ARCH gates |
| §7 | ≥2 stakeholders with expectations | Only 1 stakeholder |
| §8 | ≥4 questions per aspect | <4 questions/aspect |
| §9 | ≥3 risks with mitigation+contingency | Missing contingency |
| §10 | IQD thresholds + DRC ref + quality matrix | Missing required fields |

> **Last Updated**: 2026-07-22
> **Purpose**: Content specification for ver-3 design.md output
