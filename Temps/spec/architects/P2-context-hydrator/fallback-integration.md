# P2 — Fallback Integration

> Role: **Gatekeeper** | Domain: **Protocol** | Design: **Fallback**
> Source: `protocols-and-state-spec.md §8` (clean/)

## Fallback scenarios

| ID | Condition | Target | Action |
|:---|:---|:---|:---|
| F5 | Context insufficient (missing contracts) | Stage 1 (Architect) | Architect adds data contracts |
| F6 | Glossary < 10 terms | Stage 0.7 (Miner) | Miner expands domain-handbook |
| F18 | thought-cache missing/empty | Stage 0 (BA Elicitor) | Depth Recovery — regenerate thought-cache |

## Phase Compression (Branch A only)

In Phase Compression mode (D3 Plan & Verify phase):
- F5, F6 collapsed into **PC-3** internal retry (max 3)
- F18 becomes part of D1 phase internal check

> Full fallback matrix: see `P5-fallback-and-escalation/`
