# P0: Context Bus + _state.yaml Protocol

> Phase: **P0** | Priority: **#1** | Depends on: **None** (foundation)

## Overview

P0 establishes the foundation that every other phase depends on:
- **Context Bus**: Shared state layer — all stages read/write here
- **`_state.yaml`**: Pipeline state protocol — stage tracking, fallback history, iteration management

## Files in this directory

| File | Role | Domain | Design |
|:---|:---|:---|:---|
| `context-bus-schema.md` | Registry | Data | Contract |
| `context-bus-rules.md` | Registry | Protocol | Contract |
| `state-yaml-protocol.md` | Registry | Protocol | Architecture |
| `artifact-registry.md` | Registry | Data | Contract |
| `phase-integration.md` | Gatekeeper | Protocol | Integration |

## Dependencies to other phases

- **→ P1**: SCS Router reads Context Bus artifacts
- **→ P2**: Hydrator reads Context Bus + checks `_state.yaml`
- **→ P3**: Drift Detector reads Context Bus artifacts
- **→ P4**: Orchestrator reads `_state.yaml` degraded status
- **→ P5**: Fallback matrix writes to `_state.yaml.fallback_history`
- **→ P6**: Deconstructor writes raw context to Context Bus
- **→ P7**: Delta planner reads `_state.yaml.stage_status`

> Source: `architecture-design.md §7, §9`, `protocols-and-state-spec.md §7, §9` (clean/)
