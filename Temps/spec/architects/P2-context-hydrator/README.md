# P2: Context Hydrator

> Phase: **P2** | Priority: **#3** | Depends on: **P0, P1**

## Overview

P2 implements the Context Hydrator — the component that prepares condensed context for Planner, solving the "Planner overload" problem.

## Files in this directory

| File | Role | Domain | Design |
|:---|:---|:---|:---|
| `hydration-schema.md` | Hydrator | Data | Contract |
| `dual-context-ingestion.md` | Hydrator | Protocol | Integration |
| `thought-cache-check.md` | Hydrator | Quality | Fallback |
| `fallback-integration.md` | Gatekeeper | Protocol | Fallback |

## Dependencies

- **From P0**: Context Bus artifacts, thought-cache reference
- **From P1**: SCS score, design.md, criteria
- **→ P3**: Hydrated context is input to Drift Detector + Planner

> Source: `architecture-design.md §4.A, §S1.7`, `protocols-and-state-spec.md §R7, §R8, §F5, §F6, §F18` (clean/)
