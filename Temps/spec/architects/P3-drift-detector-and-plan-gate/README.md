# P3: Drift Detector + Plan Quality Gate

> Phase: **P3** | Priority: **#4** | Depends on: **P0, P1, P2**

## Overview

P3 is the final gate before Builder receives handoff. It detects plan-to-design drift and enforces plan quality.

## Files in this directory

| File | Role | Domain | Design |
|:---|:---|:---|:---|
| `drift-detection.md` | Detector | Quality | Verification |
| `plan-quality-gate.md` | Gatekeeper | Quality | Quality |
| `semantic-sampling-audit.md` | Auditor | Quality | Verification |
| `fallback-matrix.md` | Gatekeeper | Protocol | Fallback |

## Dependencies

- **From P0**: Context Bus artifacts, `_state.yaml`
- **From P1**: design.md, criteria
- **From P2**: hydrated-context.yaml, thought-cache.yaml
- **→ P4**: Pass signal triggers Orchestrator (Branch B)
- **→ P5**: Fallback activation writes to `_state.yaml`

> Source: `architecture-design.md §S2.5`, `protocols-and-state-spec.md §F7-F9, §F8-EXT` (clean/)
