# SSP Protocol (State & Signal Protocol)

> Role: **Coordinator** | Domain: **Protocol** | Design: **Contract**
> Source: `orchestrator-agent-spec.md`, `architecture-design.md §S3c` (clean/)

## Purpose

Governs inter-micro-skill communication — each micro-skill communicates via signals, not shared state.

## Signal types

| Signal | Meaning |
|:---|:---|
| `START` | Micro-skill begins |
| `OUTPUT_READY` | Micro-skill produced valid output |
| `ERROR` | Micro-skill failed |
| `HANDOFF` | Handover output to downstream micro-skill |

## State transitions

```
IDLE → SPAWNING → RUNNING → OUTPUT_READY → HANDOFF → COMPLETED
RUNNING → ERROR → RETRY (max 2) → FAILED
```

## Contract schema

```yaml
ssp_contract:
  micro_skill_a:
    output_signal: "OTP_VALIDATED"
    output_schema:
      status: "APPROVED" | "REJECTED"
      nonce: string
    downstream: ["micro_skill_b"]
  micro_skill_b:
    input_signal: "OTP_VALIDATED"
    input_schema:
      status: string
      nonce: string
    output_signal: "TRANSACTION_COMPLETED"
    downstream: []
```

## Validation rules

1. Every `output_signal` must match a downstream `input_signal`
2. `output_schema` must be subset of downstream `input_schema` (structural compatibility)
3. No circular dependencies
4. DAG must be acyclic
