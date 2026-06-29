# Artifact Registry

> Role: **Registry** | Domain: **Data** | Design: **Contract**
> Source: `architecture-design.md §7, §9` (clean/)

## Files managed by pipeline

| Artifact | Created by | Consumed by | Schema |
|:---|:---|:---|:---|
| `business-analysis.md` | Stage 0 (BA Elicitor) | Stage 0.5, 0.7 | Markdown |
| `domain-handbook.md` | Stage 0.7 (Miner) | Stage 1, 1.7 | Markdown |
| `scs-rating.yaml` | Stage 0.5 (SCS Router) | Stage 1.5, 3 | YAML |
| `design.md` | Stage 1 (Architect) | Stage 1.5, 1.7, 2, 2.5 | Markdown |
| `quality-matrix.yaml` | Stage 1.5 (Gatekeeper) | Stage 2, 2.5, 3 | YAML |
| `criteria.md` | Stage 1.5 (Gatekeeper) | Stage 2, 3 | Markdown |
| `hydrated-context.yaml` | Stage 1.7 (Hydrator) | Stage 2 (Planner) | YAML |
| `thought-cache.yaml` | Stage 0 + 1.5 | Stage 1.7, 3 (Builder) | YAML |
| `todo.md` | Stage 2 (Planner) | Stage 3, 2.5 | Markdown+YAML |
| `orchestration-plan.md` | Stage 2 (Planner, B only) | Stage 3a | Markdown |
| `plan-verification-report.md` | Stage 2.5 (Drift Detector) | Stage 3 | Markdown |
| `build-log.md` | Stage 3/5 (Builder/Delivery) | Stage 3.5 | Markdown |
| `review-report.md` | Stage 3.5 (Reviewer) | Stage 4 | Markdown |
| `verification.md` | Stage 4 (Sandbox) | Stage 5 | Markdown |
| `ssp-contract.yaml` | Stage 2/3a | Stage 3b, 3c | YAML |
| `_state.yaml` | Cross-cutting | Cross-cutting | YAML |
| `context-bus.yaml` | Cross-cutting | Cross-cutting | YAML |

## Path template

All artifacts live under `.skill-context/{target_skill}/` where `{target_skill}` is the skill name being built.
