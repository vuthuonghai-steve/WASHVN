# Drift Detection

> Role: **Detector** | Domain: **Quality** | Design: **Verification**
> Source: `architecture-design.md §S2.5` (clean/)

## Purpose

Checks if `todo.md` has drifted from `design.md` intent. A valid-looking plan that builds the wrong thing is worse than an invalid plan.

## Detection checks

| Check | What it validates | Criteria |
|:---|:---|:---|
| DRIFT-1.0 | Back-link integrity | Every task links to `design.md §3` zone |
| DRIFT-2.0 | Contract alignment | Data contracts in todo.md match design.md |
| DRIFT-3.0 | State alignment | State transitions match design.md spec |
| DRIFT-4.0 | Zone alignment | No task assigned to zones not in `design.md §3` |

## Output

`plan-verification-report.md` with verdict:

```
verdict: "Pass" | "Drift" | "Fail"
drift_items:
  - task_id: "T3"
    zone: "knowledge/"
    design_zone: "core/"
    severity: "minor"
    action: "update zone mapping"
```

## Fallback logic (3 levels)

| Level | Condition | Action |
|:---|:---|:---|
| **Minor drift** | Task misaligned but fixable | → Stage 2 (re-plan) — F7 |
| **Major drift** | Plan wrong domain vs design | → Stage 1 (revise design) — F8 |
| **Critical** | Design fundamentally wrong | → Stage 0.5 (re-anchor domain) — F9 |
