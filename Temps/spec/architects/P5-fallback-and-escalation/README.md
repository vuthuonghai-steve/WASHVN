# P5: Fallback + Escalation Protocol

> Phase: **P5** | Priority: **#6** | Depends on: **P0 (`_state.yaml`)**

## Overview

P5 consolidates ALL fallback and escalation mechanisms — the safety net for the entire pipeline.

## Files in this directory

| File | Role | Domain | Design |
|:---|:---|:---|:---|
| `fallback-matrix-full.md` | Gatekeeper | Protocol | Fallback |
| `escalation-protocol.md` | Escalator | Protocol | Fallback |
| `phase-compression-fallback.md` | Gatekeeper | Protocol | Compression |
| `yaml-resilience-layer.md` | Validator | Resilience | Architecture |

## Dependencies

- **From P0**: `_state.yaml.fallback_history`, iteration counting
- **From P1**: F1-F4 for SCS/Gatekeeper fallbacks
- **From P2**: F5, F6, F18 for Hydrator fallbacks
- **From P3**: F7-F9, F8-EXT for Drift detection fallbacks
- **From P4**: F10-F12 for Orchestrator/Builder fallbacks

> Source: `protocols-and-state-spec.md §8` (full), `architecture-design.md §State Diagram` (clean/)
