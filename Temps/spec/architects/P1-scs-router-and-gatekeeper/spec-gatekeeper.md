# Spec Gatekeeper

> Role: **Gatekeeper** | Domain: **Quality** | Design: **Contract**
> Source: `architecture-design.md §S1.5` (clean/)

## Responsibilities

1. Validate SCS score from Stage 0.5
2. Generate binary quality gates for entire pipeline
3. Decompose flow into phases (DAG) with Input/Output Contract
4. Binarize criteria + set `must_not` constraints
5. Export Criteria Contract (YAML)

## Outputs

- `criteria.md` — validated acceptance criteria
- `quality-matrix.yaml` — finalized quality gates for pipeline run

## Validation checklist

- [ ] META-1.1: Domain Anchoring Enforcement
- [ ] META-1.2: Phase deconstruction (3–5 phases minimum)
- [ ] META-2.1: Semantic Depth Gate v2.0 (4 signals AND)
- [ ] META-2.2: Reverse Questioning Framework
- [ ] META-3.1: Mechanical Pass/Fail Verification
- [ ] META-3.2: Negative Space & Guardrails
- [ ] META-3.3: Sandbox Testing & Evidence Preservation

## Fallback

- F3: Criteria fails meta-criteria → back to Stage 1 (Architect revise design)
- F4: SCS score changes after reading design → back to Stage 0.5 (re-evaluate SCS, re-route branch)
