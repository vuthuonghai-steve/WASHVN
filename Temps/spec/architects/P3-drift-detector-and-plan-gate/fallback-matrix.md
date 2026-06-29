# P3 — Fallback Matrix

> Role: **Gatekeeper** | Domain: **Protocol** | Design: **Fallback**
> Source: `protocols-and-state-spec.md §8` (clean/)

## P3-specific fallbacks

| ID | Condition | Target | Action |
|:---|:---|:---|:---|
| F7 | Drift minor | Stage 2 (Planner) | Re-plan todo.md |
| F8 | Drift major | Stage 1 (Architect) | Revise design.md |
| F8-EXT | Semantic audit FAIL | Stage 1 / Stage 0 | Design revise or re-elicitation |
| F9 | Design wrong domain | Stage 0.5 | Re-evaluate SCS + re-anchor domain |

## Phase Compression (Branch A only)

In D3 phase:
- F7, F8 collapsed into **PC-3** (internal retry, max 3)
- F9 becomes **PC-4** (escalate immediately, no retry)

## Common rules

- Max 3 iterations per stage → escalate to oracle/user
- Append-only `_state.yaml.fallback_history`
- Root cause first: fallback to nearest stage, then deeper if repeat

> Full matrix: see `P5-fallback-and-escalation/`
