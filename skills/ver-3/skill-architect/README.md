---
name: skill-architect
version: 0.0.1
suite: WASHVN
tags: [architect, design, 7-zone, mermaid, stage-1]
---

# skill-architect

## Description

Transforms exploration output (requirements + domain knowledge + criteria) into a formal 7-Zone skill design specification. Produces `design.md` with Mermaid diagrams, zone maps, data contracts, and state transitions plus a DRC routing contract for downstream stages.

## Architecture: 6-Phase Workflow

1. **P1: Read Inputs** — Ingest exploration.md, domain-handbook.md, criteria.md from .skill-context/
2. **P2: Zone Mapping** — Map skill structure to 7 Zones (Core, Knowledge, Templates, Scripts, Data, Loop, Assets) with concrete filenames
3. **P3: Data Contracts** — Define I/O schemas, DRC contract, state persistence rules
4. **P4: State Diagram** — Render skill lifecycle as Mermaid stateDiagram with all transitions and guard conditions
5. **P5: Must-Not Rules** — Enumerate negative constraints (anti-hallucination, ghost output, structural drift)
6. **P6: Emit** — Write design.md + data/drc.yaml to .skill-context/

## Inputs

| Artifact | Source |
|----------|--------|
| exploration.md | skill-explorer (Stage 0) |
| domain-handbook.md | skill-knowledge-miner (Stage 0.5) |
| criteria.md | skill-explorer (Stage 0) |

## Outputs

| Artifact | Path | Schema |
|----------|------|--------|
| design.md | .skill-context/{skill}/design.md | design.schema.yaml |
| drc-skill-architect.yaml | data/drc.yaml | drc_contract_template.yaml |

## Dependencies

- **Upstream:** skill-explorer (Stage 0), skill-knowledge-miner (Stage 0.5)

## Consumers

- **Downstream:** production-quality-gatekeeper (Stage 1.5), skill-planner (Stage 2)

## Quality Gates

| Gate | Condition |
|------|-----------|
| META-1 | Domain anchor + 6 phases + 7-zone table + full frontmatter |
| META-2 | Depth signals S1≥5/phase, S2≥4/aspect, S3≥2 stakeholders, S4 constraints present |
| META-3 | All ARCH gates PASS + BUILD-3.1 ≤700t + zero placeholder |
| ARCH-1 | Semantic anchors in each phase |
| ARCH-2 | Valid I/O schemas for all artifacts |
| ARCH-3 | Complete 7-zone mapping with concrete filenames |
| ARCH-4 | Valid stateDiagram with all states and transitions |
