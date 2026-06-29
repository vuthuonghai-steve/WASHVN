# P1: SCS Router + Spec Gatekeeper

> Phase: **P1** | Priority: **#2** | Depends on: **P0 (Context Bus)**

## Overview

P1 implements routing and quality assurance:
- **SCS Router**: Evaluates skill complexity, routes to Branch A or B
- **Spec Gatekeeper**: Validates design quality, enforces META-criteria

## Files in this directory

| File | Role | Domain | Design |
|:---|:---|:---|:---|
| `scs-routing.md` | Router | Protocol | Contract |
| `spec-gatekeeper.md` | Gatekeeper | Quality | Contract |
| `meta-criteria.md` | Gatekeeper | Quality | Quality |
| `re-validation-rule.md` | Gatekeeper | Quality | Fallback |

## Dependencies

- **From P0**: Context Bus artifacts, `_state.yaml` protocol
- **→ P2**: SCS score influences Hydrator behavior
- **→ P3**: Gatekeeper criteria used by Drift Detector
- **→ P4**: SCS score determines Branch B Orchestrator invocation

> Source: `architecture-design.md §S0.5, §S1.5`, `protocols-and-state-spec.md §F4` (clean/)
