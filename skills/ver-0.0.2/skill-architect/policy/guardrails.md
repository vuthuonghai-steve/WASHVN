# Guardrails — skill-architect v2.0.0

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
    conditions:
      - condition: "confidence < 70%"
        action: "STOP + BLOCK Phase — cannot proceed without domain knowledge. Ask user to provide knowledge files."
      - condition: "70% <= confidence < 85%"
        action: "Ask user for clarification, activate K=8 chains BEFORE presenting analysis"
      - condition: "confidence >= 85%"
        action: "Proceed normally"
    note: "Per FR-11: knowledge gap is a hard stop, not a soft pause"

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

  G8:
    rule: "Script Determinism"
    must:
      - scripts_zone_io_only
      - no_business_logic_in_scripts
      - each_script_has_deterministic_boundary_comment
      - input_output_schema_required
    must_not:
      - business_logic_in_scripts
      - decision_trees_in_scripts
      - prompt_templates_in_scripts

  G9:
    rule: "Knowledge Traceability"
    must:
      - trace_every_s2_assertion_to_source
      - specific_trace_tags_required
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
