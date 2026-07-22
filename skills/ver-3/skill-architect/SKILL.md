---
name: skill-architect
description: "Senior Architect — 6-phase META-driven design with ARCH binary gates and DRC output contract."
version: 0.0.1
suite: WASHVN
category: stage-1-architect
stage: 1
target_variable: target_skill
tags: [architect, design, mermaid, contracts, skill-pipeline]
when_to_use: "Stage 1 of Master Skill Suite pipeline. Design Agent Skills from exploration.md + domain-handbook.md + criteria.md. Produce design.md + drc.yaml."
output_contract:
  primary: ".skill-context/{target_skill}/design.md"
  secondary: "data/drc.yaml"
  schema: "skills/ver-3/_shared/schemas/design.schema.yaml"
disable-model-invocation: true
user-invocable: true
---

<instructions>
## 6-Phase Workflow
| Phase | Output | Gate |
|-------|--------|------|
| P1 Read | §1 Problem Statement | ARCH-1 (anchors) |
| P2 Zone Map | §2 7-Zone Table | ARCH-3 (complete) |
| P3 Contracts | §3 I/O Schemas | ARCH-2 (valid) |
| P4 State Diagram | §4 State Machine | ARCH-4 (diagram) |
| P5 Must-Not Rules | §5 Rules (≥5/phase) | META-2 S1 (count) |
| P6 Emit | design.md + drc.yaml | META-1/2/3 final |

## META Gates
- META-1: domain anchor + 6 phases + 7-zone + frontmatter
- META-2: S1≥5/phase ∧ S2≥4/aspect ∧ S3≥2 stakeholders ∧ S4 constraints
- META-3: all ARCH PASS + BUILD-3.1 ≤700t + zero placeholder

## ARCH Gates
- ARCH-1: Semantic anchors in §1 | ARCH-2: Valid I/O schemas
- ARCH-3: Complete 7-zone table | ARCH-4: Valid stateDiagram

## Must-Not (condensed)
P1: No hallucination, no skip input, no stream mixing.
P2: No placeholder filenames, no zone omission, no §11/§12.
P3: No schema violation, no DRC without routing.
P4: No invalid diagram, no disconnected states, no missing fallbacks.
P5: No <5/phase, no generic rules, no contradictions.
P6: No HTML comments, no unverified handoff, no degraded without flag.

## Graceful Degradation
Token >700t → degraded:true + refactor. Missing template → inline fallback. Schema mismatch → annotate §10.

## Dual Knowledge Stream
Technical: design.md + drc.yaml → Gatekeeper S1.5, Planner S2.
Cognitive: knowledge/*.md → Builder S3.
</instructions>

## Routing Map
- Tier 1 (Boot): `../_shared/knowledge/framework.md`, `format-standards.md`
- Tier 2: `knowledge/architect.md`, `design-exemplars.md`, `visualization-guidelines.md`, `templates/design.md.template`, `loop/design-checklist.md`
- Tier 3: `loop/design-checklist.yaml`, `data/drc.yaml`, `scripts/`

## Boot Sequence
1. Read SKILL.md (done). 2. Read shared framework.md. 3. Check `.skill-context/{target_skill}/` exists. 4. Proceed P1 Read.
