# Plan Quality Gate

> Role: **Gatekeeper** | Domain: **Quality** | Design: **Quality**
> Source: `architecture-design.md §S2, §S2.5` (clean/)

## Criteria (PLAN-1 → PLAN-5)

| ID | Criteria | Check |
|:---|:---|:---|
| PLAN-1.0 | Upstream Context Fidelity | Plan references correct versions of design artifacts |
| PLAN-2.0 | Semantic Density & Format | `todo.md` < 1200 tokens, no prose bloat |
| PLAN-3.0 | Deterministic Contracts | Every task has input_schema + output_schema |
| PLAN-4.0 | Negative Space & Guardrails | Complex tasks (Priority ≥ High) have `must_not` |
| PLAN-5.0 | Mechanical Verification | Each task has CLI verification command |

## Execution

1. After Drift Detection Pass, run PLAN-1 through PLAN-5
2. Each check is binary: PASS or FAIL
3. Any FAIL → trigger F7 (back to Stage 2 re-plan) or F8 (back to Stage 1)

## Output

`plan-verification-report.md` includes:
- Per-criteria verdict table
- Overall verdict (Pass / Drift / Fail)
- Recommended action if not Pass
