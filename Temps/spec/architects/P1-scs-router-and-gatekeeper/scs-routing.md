# SCS Routing

> Role: **Router** | Domain: **Protocol** | Design: **Contract**
> Source: `architecture-design.md §S0.5, §S1.5` (clean/)

## Purpose

SCS (Skill Complexity Score) evaluates task complexity to determine which pipeline branch to use.

## Scoring

| Score | Track | Branch | Pipeline |
|:---|:---|:---|:---|
| 1.0–2.9 | Fast Track | Branch A (Single Skill) | 3 phases D1-D3 |
| 3.0–5.0 | Full Track OMSP | Branch B (Micro-Skill Bundle) | 13-stage full pipeline |

## Output schema

```yaml
scs_evaluation:
  score: 3.5
  mode: "Full-Track OMSP"
  rationale: "Feature involves auth + payment + 3 micro-skills required"
  routing_decision: "branch_b_micro_skill"
  context_bus_id: "cb_20260625_001"
```

## Implementation (2-phase)

1. **Stage 0.5 (pre-pass)**: Quick SCS assessment for early routing — Architect needs to know whether to generate orchestration-plan
2. **Stage 1.5 (re-validation)**: Gatekeeper validates SCS score after design exists — can re-route (F4) if score changed

## Fallback

- F1: Insufficient info for SCS → back to Stage 0 (BA Elicitor)
- F4: SCS score changes after design → back to Stage 0.5 (re-evaluate)
