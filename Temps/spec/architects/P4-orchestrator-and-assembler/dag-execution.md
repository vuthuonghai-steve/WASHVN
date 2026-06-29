# DAG Execution

> Role: **Coordinator** | Domain: **Execution** | Design: **Architecture**
> Source: `architecture-design.md §S3a, §5.2` (clean/)

## Purpose

Orchestrator manages DAG-based execution order for micro-skills with dependencies.

## DAG rules

1. **Independent tasks** → spawn in parallel
2. **Dependent tasks** → A must complete before B starts
3. **Fan-in** → multiple tasks must complete before aggregator
4. **Fan-out** → one task triggers multiple downstream tasks

## Example DAG

```
ms-01 (OTP validation) ──→ ms-03 (Webhook handler)
ms-02 (Payment gateway) ──→ ms-03
                              │
                              ▼
                         ms-04 (Notification)
```

## Execution strategy

```yaml
execution_order:
  - wave_1: [ms-01, ms-02]       # parallel
  - wave_2: [ms-03]              # after wave_1
  - wave_3: [ms-04]              # after wave_2
```

## Orchestrator monitoring

- Track each micro-skill state via SSP signals
- If a micro-skill in wave N fails → do NOT block wave N+1 if independent
- If critical dependency fails → trigger fallback F11/F12
- Log all state transitions to `orchestrator-log.md`
