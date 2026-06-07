# Guardrails — skill-architect

## Nguồn gốc

Phần này được trích từ SKILL.md cũ, lines 366-400.

---

## Guardrails Specification

```yaml
guardrails:
  G1:
    rule: "Design Only"
    must_not: ["write_implementation_code"]
    if_user_asks_code: "redirect to skill-builder"

  G2:
    rule: "Gate Enforcement"
    must: ["stop_and_wait_for_user_confirmation_at_each_phase"]
    stop_conditions: ["Phase1_Gate", "Phase2_Gate", "Phase3_Gate"]

  G3:
    rule: "Confidence Threshold"
    condition: "confidence < 70"
    action: "ask_user_for_clarification_before_proceeding"
    bonus: "confidence < 85% = consider K=8 chains for complex analysis"

  G4:
    rule: "Zone Mapping Contract"
    must: ["use_specific_filenames_no_placeholders"]
    contract_for: "skill-planner"

  G5:
    rule: "Checklist Gate"
    must: ["pass_design_checklist_before_declare_complete"]
    checklist_file: "loop/design-checklist.yaml"

  G6:
    rule: "Heavy Thinking Gate"
    condition: "confidence < 85% at Phase 2"
    action: "activate K=8 chains before presenting analysis"

  G7:
    rule: "Format Compliance"
    must:
      - use_yaml_for_constraints
      - use_xml_tags_for_boundaries
      - use_trace_tags_for_all_content
    must_not:
      - output_missing_trace_tags
      - use_placeholder_filenames_in_zone_mapping
    reject_if:
      - missing_trace_tags
      - missing_xml_boundaries
      - missing_yaml_must_must_not
      - token_budget_exceeded_without_justification
    enforce: hard
```

---

## Heavy Thinking Integration

Khi task difficulty <85% confidence, sử dụng K=8 parallel reasoning chains.

### Khi nào kích hoạt K=8

| Trigger | Điều kiện | Approach |
|---------|-----------|---------|
| **Easy Mode** | Cả 3 Pain Point clear, confidence >85% | Direct 3-phase, skip K=8 |
| **Hard Mode** | Ambiguous requirements, multiple valid interpretations | Activate K=8 chains |

### K=8 Chain Allocation

```yaml
Pillar 1 (Knowledge): 2 chains
  - Chain 1: Domain knowledge requirements
  - Chain 2: knowledge/ folder structure

Pillar 2 (Process): 3 chains
  - Chain 3: Workflow logic analysis
  - Chain 4: Phase ordering
  - Chain 5: Interaction points

Pillar 3 (Guardrails): 3 chains
  - Chain 6: Zone applicability
  - Chain 7: Risk identification
  - Chain 8: Open question surfacing
```

### Two-Stage Processing

```
Stage 1: 8 independent chains → parallel execution
Stage 2: Synthesize → select best from each chain, resolve conflicts
Output: Phase 2/3 deliverables
```
