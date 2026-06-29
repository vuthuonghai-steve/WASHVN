# Semantic Sampling Audit Layer

> Role: **Auditor** | Domain: **Quality** | Design: **Verification**
> Source: `architecture-design.md §S2.5`, `protocols-and-state-spec.md §8, §9` (clean/)

## Purpose

An overlay audit that catches "PASS-form but FAIL-meaning" scenarios. After Drift Detector PASS, a probabilistic sampling checks semantic alignment.

## Mechanism

- **Default rate**: 30% of pipeline runs
- **Adaptive rate**: Any FAIL in last 8 runs → 100% (Hard Gate)
- **Relaxation**: 8 consecutive PASS → 15%

## Audit method

Planner MUST generate `todo-intent.yaml` explaining business rationale of the plan. Oracle subagent answers 3 questions:

| AUDIT-# | Question |
|:---|:---|
| AUDIT-1 | Does the plan serve the original business goal? |
| AUDIT-2 | Are edge cases from `thought-cache.yaml` addressed? |
| AUDIT-3 | Does plan constrain match `design.md` guardrails? |

## Outcomes

- **PASS**: Pipeline continues to Stage 3 (Builder)
- **FAIL**: Generate `audit-fail-report.md`, trigger **F8-EXT**:
  - Root cause: design wrong → Stage 1 revise
  - Root cause: plan wrong intent → Stage 0 re-elicitation

## Human mode fallback

If configured as `human` mode and no response within 5 min → auto-fallback to Oracle audit or degraded mode to avoid bottleneck.

## Tracking in `_state.yaml`

```yaml
sampling_audit:
  enabled: true
  mode: "oracle"
  sampling_rate: 30
  last_8_results: ["PASS",...]
  escalation_active: false
```

> See `supplements/sampling-audit-spec.md` for full implementation
