# Phase Compression Fallback (Branch A)

> Role: **Gatekeeper** | Domain: **Protocol** | Design: **Compression**
> Source: `protocols-and-state-spec.md §8` (clean/)

## Collapsed fallback mapping

Under Phase Compression (Branch A, SCS < 3.0), F1-F9 stage-specific fallbacks collapse into 4 paths:

| Path | Phase | Old fallbacks | Action |
|:---|:---|:---|:---|
| **PC-1** | D1 Discovery | F1, F2 | Internal retry (max 3) — agent self-supplements |
| **PC-2** | D2 Design & Contract | F3, F4 | Internal retry (max 3) — agent self-revises design |
| **PC-3** | D3 Plan & Verify | F5, F6, F7, F8, F15 | Internal retry (max 3) — agent self-re-plans |
| **PC-4** | D3 Plan & Verify | F9 | **Escalate** — design domain wrong, no retry |

## Collapsed mapping detail

| Old fallback | Original stage | Phase | Collapsed path |
|:---|:---|:---|---:|
| F1, F2 | S0.5 / S0.7 | D1 Discovery | PC-1 |
| F3, F4 | S1.5 | D2 Design & Contract | PC-2 |
| F5, F6 | S1.7 | D3 Plan & Verify | PC-3 |
| F7, F8 | S2.5 | D3 Plan & Verify | PC-3 |
| F9 | S2.5 | D3 Plan & Verify | **PC-4** escalate |
| F15 | Stage 4 (Sandbox) | D3 Plan & Verify | PC-3 re-plan |

## Branch B exception

Branch B (SCS >= 3.0) **does NOT use Phase Compression** — full F1-F15 fallback matrix applies unchanged.
