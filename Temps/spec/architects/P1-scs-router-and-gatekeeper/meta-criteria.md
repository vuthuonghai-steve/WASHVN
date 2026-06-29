# META-Criteria (META-1 → META-3)

> Role: **Gatekeeper** | Domain: **Quality** | Design: **Quality**
> Source: `architecture-design.md §S1.5` (clean/)

## META-1: Structural Integrity

| ID | Criteria | Check |
|:---|:---|:---|
| META-1.1 | Domain Anchoring Enforcement | Design must reference domain terms from domain-handbook |
| META-1.2 | Phase Deconstruction | Pipeline split into 3–5 phases with I/O contracts |

## META-2: Semantic Depth Gate v2.0 (4 signals AND)

| ID | Signal | Description |
|:---|:---|:---|
| S1 | Negation Density | `must_not` rules ≥ 5 per phase |
| S2 | Reverse Question | 4-aspect probing present |
| S3 | Multi-Stakeholder | Goals/pain points for each role |
| S4 | Constraint Anchoring | All constraints traceable to domain rules |

**All 4 signals must PASS** for META-2.1 to pass.

## META-3: Mechanical Quality

| ID | Criteria | Check |
|:---|:---|:---|
| META-3.1 | Mechanical Pass/Fail | Every gate has executable verification command |
| META-3.2 | Negative Space & Guardrails | `must_not` list covers anti-patterns + security |
| META-3.3 | Sandbox Testing | Test cases specified with expected PASS/FAIL |

## Depth Gate (supplements)

> See `supplements/depth-gate-criteria.md` for full META-2.1 v2.0 implementation
