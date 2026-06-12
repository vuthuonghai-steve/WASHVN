---
spec_version: "3.0.0"
skill_name: "skill-planner"
based_on:
  - "CLAUDE.md AI-First Documentation Standard v1.0"
  - "skill-architect/SPEC.md v3.0"
  - "Agent Skill Framework architecture.md v3.0.0"
last_updated: "2026-05-31"
maintained_by: "Steve Void Team"
---

# skill-planner Technical Specification (Ver_3.0.0 - Physical Micro-skills)

## 1. Semantic Questions

When reading this skill, the LLM must be able to answer:

| # | Question | Answerable From |
|---|----------|-----------------|
| **Q1** | Is this a command or reference data? | SKILL.md `name` + `description` frontmatter |
| **Q2** | Is this a hard rule or soft suggestion? | SKILL.md `constraints` YAML block (must/must_not) |
| **Q3** | When is this information always needed vs context-dependent? | SKILL.md `progressive_disclosure` tiers |
| **Q4** | What is example vs criteria? | `loop/plan-checklist.yaml` vs `knowledge/` files |
| **Q5** | When conflict occurs, which takes priority? | SKILL.md `priority_order` in AI-FIRST CONFIGURATION |

---

## 2. Format Requirements

Based on CLAUDE.md §3 format selection:

```yaml
format_rules:
  markdown:
    use_for:
      - explanation: "SKILL.md workflow description, rationale, Step instructions"
      - walkthrough: "Boot sequence, progressive writing contract"
      - overview: "Multi-perspective analysis, 4 perspectives table"
    avoid_for:
      - hard_rules_without_schema: "Use YAML in Guardrails instead"

  yaml:
    use_for:
      - constraints: "progressive_disclosure tiers, output_contract, priority_order"
      - checklists: "loop/plan-checklist.yaml quality gates"
      - routing: "pipeline stage_order, dependencies, successor_hints"
    avoid_for:
      - long_prose: "Step instructions stay in Markdown"

  xml_like_tags:
    use_for:
      - semantic_boundaries: "<instructions>, <context> in Step descriptions"
      - separating_input: "When user input wraps requirements"
    avoid_for:
      - excessive_micro_tagging: "Step steps already have clear boundaries"
```

---

## 3. Token Budget

Based on CLAUDE.md §6 Layer Model:

```yaml
token_budget:
  L0_anchor_rules:
    limit: 350 tokens
    actual: "~280 tokens (SKILL.md frontmatter + core directives)"
    status: "✅ GOOD"
    split_when: ">400 tokens"

  L1_working_policy:
    limit: 1000 tokens
    actual: "~620 tokens (Guardrails YAML + Workflow Steps + Error Handling)"
    status: "✅ GOOD"
    split_when: ">1200 tokens"

  L2_domain_context:
    limit: 2500 tokens
    actual: "~350 tokens (knowledge/ referenced, not inlined)"
    status: "✅ GOOD"
    split_when: ">3000 tokens"

  root_guide_total:
    limit: 1800 tokens
    actual: "~1250 tokens (SKILL.md full)"
    status: "✅ EXCELLENT"
    split_when: ">2500 tokens"

  format_distribution:
    markdown_body: "~980 tokens (78%)"
    yaml_frontmatter: "~180 tokens (14%)"
    tables: "~90 tokens (8%)"
```

---

## 4. Quality Gates

Based on CLAUDE.md §12 Definition of Done + architure.md §4:

```yaml
quality_gates:
  source_fidelity:
    - name: "Design Contract Preserved"
      check: "§3 Zone Mapping tasks all traced to specific design.md sections"
      ref: "SKILL.md Guardrails G1"
    - name: "Trace Tag Compliance"
      check: "All tasks have valid trace tags: [TỪ DESIGN §N], [GỢI Ý BỔ SUNG], [TỪ AUDIT TÀI NGUYÊN], [CẦN LÀM RÕ]"
      ref: "SKILL.md Guardrails G2"
    - name: "No Requirement Inflation"
      check: "Planner only decomposes, never adds new requirements"
      ref: "SKILL.md Guardrails G3"

  structure:
    - name: "6 Required Sections Present"
      check: "Pre-requisites, Phase Breakdown, Knowledge & Resources, Definition of Done, Notes, Builder Feedback"
      ref: "SKILL.md §Step WRITE"
    - name: "Phase 0 Exists"
      check: "Resource Preparation phase present for missing domain documents"
      ref: "SKILL.md §Step ANALYZE"
    - name: "Priority Assignment Valid"
      check: "Critical/High/Medium/Low properly assigned based on blocking relationships"
      ref: "SKILL.md §Step WRITE"

  agent_usability:
    - name: "Priority Order Defined"
      check: "source_fidelity > resource_completeness > task_traceability > user_clarification"
      ref: "SKILL.md AI-FIRST CONFIGURATION"
    - name: "Must/MustNot Rules Clear"
      check: "G1 Trace Required, G2 Label Sources, G3 No Inventing, G4 Ground in Design, G5 Resource Gate"
      ref: "SKILL.md Guardrails YAML"
    - name: "Loading Guidance Present"
      check: "progressive_disclosure tier1/tier2/tier3 paths specified"
      ref: "SKILL.md frontmatter"

  handoff_readiness:
    - name: "Architect→Planner→Builder Contract"
      check: "§3 Zone Mapping + §7 PD Plan + §8 Risks ready for Builder"
      ref: "SKILL.md Pipeline Integration"
    - name: "Quality Gate Passed"
      check: "loop/plan-checklist.yaml all MUST items pass before delivery"
      ref: "SKILL.md §Step VERIFY"

  resource_integrity:
    - name: "Resource Coverage"
      check: "All critical resources have Status: ✅ before ready_for_builder"
      ref: "SKILL.md Guardrails G5"
    - name: "No Orphan Prerequisites"
      check: "Every prerequisite has corresponding task or remediation action"
      ref: "loop/plan-checklist.yaml R1"
```

---

## 5. Anti-Hallucination Rules

Based on CLAUDE.md §9 Semantic Activation Anchors:

```yaml
anti_hallucination:
  AH1_source_trace:
    description: "Every task MUST trace to design.md"
    implementation:
      - "Tasks derived from §3 Zone Mapping"
      - "Tasks derived from §6 Interaction Points"
      - "Tasks derived from §8 Risks"
    violation: "Task without trace tag"

  AH2_no_requirement_inflation:
    description: "Only decompose, don't add requirements"
    implementation:
      - "Skill ONLY plans, never implements (G3 Guardrail)"
      - "New domain knowledge requires resources/ availability"
      - "§9 Open Questions flags unverified assumptions"
    violation: "Adding features not in design.md"

  AH3_resource_verification:
    description: "Verify resources before completion"
    implementation:
      - "Step READ audits resources/ directory"
      - "Step ANALYZE assigns Rich/Thin status"
      - "G5 Resource Gate blocks ready_for_builder"
    violation: "Declaring complete without resource audit"

  AH4_source_labeling:
    description: "Always label sources"
    implementation:
      - "[TỪ DESIGN §N] — from confirmed design.md"
      - "[GỢI Ý BỔ SUNG] — planner's suggestion, not in design"
      - "[TỪ AUDIT TÀI NGUYÊN] — generated from resource gap"
      - "[CẦN LÀM RÕ] — requires user clarification"
    violation: "Unlabeled content appearing as fact"

  AH5_blocker_tracking:
    description: "Blockers must be tracked and resolved"
    implementation:
      - "Blockers array present in todo.md"
      - "Unresolved blockers prevent ready_for_builder"
      - "[CẦN LÀM RÕ] flags mark clarification needed"
    violation: "Marking ready with unresolved blockers"
```

---

## 6. Zone Structure Compliance

Based on architure.md §2 Zones:

```yaml
zone_compliance:
  required_zones:
    core:
      path: "SKILL.md"
      status: "✅ Present - Boot Sequence, Steps, Guardrails YAML"
      mandatory: true

    knowledge:
      path: "knowledge/architect.md"
      path: "knowledge/skill-packaging.md"
      status: "✅ Present - 7-Zone framework, 3-tier knowledge model"
      mandatory: true
      shared: "../_shared/knowledge/framework.md"

    loop:
      path: "loop/plan-checklist.yaml"
      status: "✅ Present - Quality gate checklist YAML format"
      mandatory: true

  conditional_zones:
    scripts:
      path: "scripts/check_status.py"
      status: "✅ Present - Status checking utility"
      loaded_when: "Boot sequence"

    data:
      path: ".skill-context/{target_skill}/data/"
      status: "❌ Not created by Planner"
      note: "Planner creates todo.md, not data configs"

  tier_structure:
    tier1_mandatory:
      - "SKILL.md"
      - "knowledge/architect.md"
      - "knowledge/skill-packaging.md"
      - "../_shared/knowledge/framework.md"
      - "knowledge/case-system.md"
    tier2_conditional:
      - "loop/plan-checklist.yaml"    # Before deliver
      - "loop/resume-checklist.yaml"  # When resuming
    tier3_optional:
      - "references/examples/plan-*.md"  # On-demand reference
```

---

## 7. Workflow Compliance

Based on architure.md §3 4-Step Workflow:

```yaml
workflow_compliance:
  step1_read:
    status: "✅ Implemented as Step READ"
    requirements_met:
      - "design.md read and parsed"
      - "resources/ audited with Rich/Thin status"
      - "Context prompt integrated"
    gate: "Continue to Step ANALYZE"

  step2_analyze:
    status: "✅ Implemented as Step ANALYZE"
    requirements_met:
      - "3-tier knowledge breakdown (Domain/Technical/Packaging)"
      - "Multi-perspective analysis (4 perspectives)"
      - "Pre-requisites table with trace tags"
    gate: "Continue to Step WRITE"

  step3_write:
    status: "✅ Implemented as Step WRITE"
    requirements_met:
      - "6 required sections in todo.md"
      - "Phase 0 for missing resources"
      - "Dependency detection and DAG validation"
    gate: "Continue to Step VERIFY"

  step4_verify:
    status: "✅ Implemented as Step VERIFY"
    requirements_met:
      - "Resource integrity check"
      - "Contract traceability check"
      - "DoD verification"
    gate: "User confirmation before handoff"

  multi_perspective_analysis:
    perspective_1:
      name: "Domain Knowledge Audit"
      focus: "resources/ coverage"
    perspective_2:
      name: "Technical Requirements"
      focus: "tools, syntax, dependencies"
    perspective_3:
      name: "Task Complexity"
      focus: "effort estimation, risks"
    perspective_4:
      name: "Traceability"
      focus: "task to design mapping"
```

---

## 8. Pipeline Integration

Based on architure.md §4 Pipeline Flow:

```yaml
pipeline:
  stage_order: 2
  predecessor: "skill-architect"
  successor: "skill-builder"

  handoff_to_builder:
    required_sections:
      - "Pre-requisites table → Builder audit prerequisites"
      - "Phase Breakdown → Builder execute by phase"
      - "Knowledge & Resources → Builder reference"
      - "Definition of Done → Builder self-verify"

    gate_criteria:
      - "All critical resources Status: ✅"
      - "Phase 0 tasks complete (resources prepared)"
      - "No unresolved blockers"
      - "All tasks have valid trace tags"

  context_directory:
    path: ".skill-context/{target_skill}/"
    created_by: "skill-architect scripts"
    contents:
      - "design.md (Architect output)"
      - "todo.md (Planner output)"
      - "build-log.md (Builder evidence)"
      - "resources/ (User-provided docs)"
      - "loop/ (Quality checks)"
```

---

## 9. Definition of Done

```yaml
definition_of_done:
  skill_planner_complete_when:
    - "✅ SKILL.md exists with all required frontmatter"
    - "✅ AI-FIRST CONFIGURATION with priority_order and constraints"
    - "✅ Guardrails in YAML schema (must/must_not)"
    - "✅ loop/plan-checklist.yaml provides quality gate"
    - "✅ All 4 Steps implemented with gate enforcement"
    - "✅ Progressive Disclosure tier1/tier2/tier3 defined"
    - "✅ Anti-hallucination rules AH1-AH5 integrated"

  todo_md_handoff_ready_when:
    - "✅ All 6 required sections present"
    - "✅ Phase 0 exists for resource preparation"
    - "✅ All tasks have valid trace tags"
    - "✅ Pre-requisites table complete with Tier/Trace/Status"
    - "✅ No unresolved blockers"
    - "✅ All critical resources Status: ✅"
    - "✅ loop/plan-checklist.yaml passed"
    - "✅ User confirmed final plan"
```

---

## References

| Source | File | Key Contribution |
|--------|------|------------------|
| CLAUDE.md AI-First Standard | `/CLAUDE.md` | §3 Format, §6 Token Budget, §12 DoD |
| skill-architect | `../skill-architect/SPEC.md` | Zone Mapping, Pipeline Flow |
| architure.md | `/architure.md` | 3 Pillars, 7 Zones, 5-Step Workflow |
| framework.md | `../_shared/knowledge/framework.md` | Zone contract, naming conventions |
| SKILL.md | `./SKILL.md` | skill-planner implementation |
| plan-checklist.yaml | `./loop/plan-checklist.yaml` | Quality gate checklist |

---

> **Spec Status**: ✅ Complete
> **Next**: skill-builder implementation follows this spec; skill-builder consumes todo.md from planner output
