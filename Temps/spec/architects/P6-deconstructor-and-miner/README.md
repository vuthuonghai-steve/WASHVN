# P6: Deconstructor + Miner Analyzer

> Phase: **P6** | Priority: **#7** | Depends on: **P0 (Context Bus)**

## Overview

P6 handles skill deconstruction and analysis for UPDATE/REBUILD modes — reading existing skills, extracting intent and knowledge.

## Files in this directory

| File | Role | Domain | Design |
|:---|:---|:---|:---|
| `internal-adapter.md` | Deconstructor | Migration | Contract |
| `external-adapter.md` | Deconstructor | Migration | Contract |
| `miner-analyzer.md` | Miner | Knowledge | Integration |
| `dual-mode-create-update.md` | Gatekeeper | Migration | Architecture |

## Dependencies

- **From P0**: Context Bus deconstructed_context section, _state.yaml execution_mode
- **→ P7**: Deconstructed context feeds Delta Planning
- **→ P2**: Miner output enriches domain-handbook

> Source: `skill-migration-spec.md` (full), `architecture-design.md §13.6, §14` (clean/)
