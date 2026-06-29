# P7: Delta Planning + In-place Builder

> Phase: **P7** | Priority: **#8** | Depends on: **P3, P4, P6**

## Overview

P7 handles UPDATE/REBUILD execution — planning only what changed (Delta) and building in-place.

## Files in this directory

| File | Role | Domain | Design |
|:---|:---|:---|:---|
| `delta-planning.md` | Planner | Execution | Contract |
| `in-place-builder.md` | Builder | Execution | Integration |
| `token-budget-soft-gate.md` | Reviewer | Quality | Quality |
| `rebuild-workflow.md` | Gatekeeper | Migration | Architecture |

## Dependencies

- **From P0**: `_state.yaml`, Context Bus artifact paths
- **From P3**: Drift-free plan (base for delta)
- **From P6**: Deconstructed context (what exists + what needs changing)

> Source: `skill-migration-spec.md §13.7`, `architecture-design.md §13.7` (clean/)
