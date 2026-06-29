# P4: Orchestrator + Integration Assembler

> Phase: **P4** | Priority: **#5** | Depends on: **P0, P1, P2, P3**

## Overview

P4 handles Branch B (SCS >= 3.0) — Micro-Skill Bundle execution with subagent Orchestrator.

## Files in this directory

| File | Role | Domain | Design |
|:---|:---|:---|:---|
| `orchestrator-agent-spec.md` | Orchestrator | Execution | Contract |
| `ssp-protocol.md` | Coordinator | Protocol | Contract |
| `parallel-builders.md` | Coordinator | Execution | Integration |
| `integration-assembler.md` | Assembler | Execution | Integration |
| `dag-execution.md` | Coordinator | Execution | Architecture |

## Dependencies

- **From P0**: `_state.yaml` degraded status, Context Bus
- **From P1**: SCS score >= 3.0 triggers this phase
- **From P2**: hydrated-context.yaml
- **From P3**: orchestration-plan.md (from Planner)
- **→ P5**: Fallback/rollback on builder failure
- **→ P7**: Delta planning for branch B bundles

> Source: `orchestrator-agent-spec.md` (full), `architecture-design.md §S3a, §S3b, §S3c, §5.2` (clean/)
