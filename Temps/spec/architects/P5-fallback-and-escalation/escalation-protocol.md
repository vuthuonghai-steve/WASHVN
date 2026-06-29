# Escalation Protocol

> Role: **Escalator** | Domain: **Protocol** | Design: **Fallback**
> Source: `protocols-and-state-spec.md §8, §9` (clean/)

## Trigger

Pipeline escalates when a stage exceeds **3 iterations** (max_iterations).

## Escalation path

```
3 iterations fail
      │
      ▼
Pipeline state → "escalated"
      │
      ├── escalated_to: "oracle"  (AI subagent with broader context)
      └── escalated_to: "user"    (human intervention required)
```

## `_state.yaml` escalation block

```yaml
escalation:
  triggered: true
  reason: "Stage 2.5 Drift Detector failed 3 iterations — design still drifting"
  escalated_to: "oracle"
```

## Escalation sources

| Source | 3-iteration limit applies to |
|:---|:---|
| Stage 2.5 Drift Detector | F7/F8/F9 iterations |
| Stage 3.5 Code Reviewer | F10/F11/F12 iterations |
| Stage 4 Sandbox | F13/F14/F15 iterations |
| Phase D1-D3 (Branch A) | PC-1/PC-2/PC-3 internal retries |

## Human mode timeout (Sampling Audit)

If configured as `human` mode and no response within **5 minutes**:
1. Auto-fallback to Oracle audit
2. Or switch to degraded mode (pipeline continues without audit)

## Degraded mode

When `_state.yaml.status = "degraded"`:
- Non-critical refs broken → warning, not halt
- Downstream agents see `degraded` status and activate defensive mode
- Automatic default/fallback values used where refs are missing
