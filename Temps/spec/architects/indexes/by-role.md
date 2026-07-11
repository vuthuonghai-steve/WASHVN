# Index by Role

> Tra cứu spec theo **vai trò** trong pipeline

## BA Chain (extension — not in original spec)

> Runtime mở rộng BA thành 3-skill chain, chạy độc lập qua `ba-pipeline-runner` (KHÔNG qua `pipeline-orchestrator`). Gốc spec chỉ có "BA Elicitor" 1 stage.

| Phase | File | Content |
|:---|:---|:---|
| P1 | `scs-routing.md` | Input to SCS evaluation (ba-elicitor) |
| P2 | `thought-cache-check.md` | F16, F17, F19 — thought-cache quality |
| P5 | `fallback-matrix-full.md` | F16-F19 fallbacks |
| — | `ba-pipeline-runner` agent | Orchestrate elicitor→analyst→synthesizer chain |
| — | `quality-scorer` agent | META-1→3 scoring (maps to Spec Gatekeeper P1) |

## BA Elicitor (Stage -1, L0)

| Phase | File | Content |
|:---|:---|:---|
| P1 | `scs-routing.md` | Input to SCS evaluation |
| P2 | `thought-cache-check.md` | F16, F17, F19 — thought-cache quality |
| P5 | `fallback-matrix-full.md` | F16-F19 fallbacks |

## SCS Router

| Phase | File | Content |
|:---|:---|:---|
| P1 | `scs-routing.md` | SCS scoring + routing decision |
| P5 | `fallback-matrix-full.md` | F1, F4 |
| P5 | `phase-compression-fallback.md` | PC-1 → collapsed fallback |

## Miner

| Phase | File | Content |
|:---|:---|:---|
| P6 | `miner-analyzer.md` | Standard + deconstruction mining |
| P2 | `hydration-schema.md` | Glossary ≥10 requirement |
| P5 | `fallback-matrix-full.md` | F2, F6 |

## Architect

| Phase | File | Content |
|:---|:---|:---|
| P1 | `spec-gatekeeper.md` | Design validation criteria |
| P1 | `meta-criteria.md` | META-1→3 for design quality |
| P3 | `drift-detection.md` | F8 — drift major → revise design |
| P0 | `artifact-registry.md` | design.md artifact spec |
| P7 | `delta-planning.md` | UPDATE mode design changes |

## Spec Gatekeeper

| Phase | File | Content |
|:---|:---|:---|
| P1 | `spec-gatekeeper.md` | Full responsibilities |
| P1 | `meta-criteria.md` | META-1.1→3.3 criteria |
| P1 | `re-validation-rule.md` | F16-F19 thought block re-validation |
| P5 | `fallback-matrix-full.md` | F3, F4 |

## Context Hydrator

| Phase | File | Content |
|:---|:---|:---|
| P2 | `hydration-schema.md` | hydrated-context.yaml schema |
| P2 | `dual-context-ingestion.md` | Two-stream context model |
| P2 | `thought-cache-check.md` | HYD-4, F18 trigger |
| P2 | `fallback-integration.md` | F5, F6 |
| P0 | `context-bus-rules.md` | R7, R8 |

## Planner

| Phase | File | Content |
|:---|:---|:---|
| P3 | `plan-quality-gate.md` | PLAN-1→5 criteria |
| P3 | `drift-detection.md` | F7 — drift minor → re-plan |
| P7 | `delta-planning.md` | UPDATE mode delta planning |
| P4 | `ssp-protocol.md` | orchestration-plan SSP contracts |

## Drift Detector

| Phase | File | Content |
|:---|:---|:---|
| P3 | `drift-detection.md` | DRIFT-1→4 checks |
| P3 | `plan-quality-gate.md` | Post-drift quality validation |
| P3 | `semantic-sampling-audit.md` | Audit layer (SAUDIT) |
| P3 | `fallback-matrix.md` | F7-F9, F8-EXT |

## Orchestrator

| Phase | File | Content |
|:---|:---|:---|
| P4 | `orchestrator-agent-spec.md` | Full agent definition + sequence diagram |
| P4 | `branch-b-sequence.md` | Full Branch B pipeline sequence view |
| P4 | `ssp-protocol.md` | SSP signal protocol |
| P4 | `parallel-builders.md` | Stage 3b spawning |
| P4 | `dag-execution.md` | DAG dependency execution |

## Builder

| Phase | File | Content |
|:---|:---|:---|
| P4 | `parallel-builders.md` | 5-Phase builder pipeline |
| P2 | `dual-context-ingestion.md` | Mandatory thought-cache read |
| P7 | `in-place-builder.md` | UPDATE mode in-place edits |
| P7 | `token-budget-soft-gate.md` | BUILD-2.1, BUILD-3.1 |

## Integration Assembler

| Phase | File | Content |
|:---|:---|:---|
| P4 | `integration-assembler.md` | Merge + orchestrate.py generation |
| P4 | `ssp-protocol.md` | SSP validation across micro-skills |

## Code Reviewer

| Phase | File | Content |
|:---|:---|:---|
| P7 | `token-budget-soft-gate.md` | REV-3.0 Refactor Trigger |
| shared | `quality-gates-reference.md` | All REV gates |
| P5 | `fallback-matrix-full.md` | F10, F11, F12 |

## Deconstructor

| Phase | File | Content |
|:---|:---|:---|
| P6 | `internal-adapter.md` | Internal skill reading |
| P6 | `external-adapter.md` | External skill conversion |
| P6 | `dual-mode-create-update.md` | Mode routing |

## Escalator

| Phase | File | Content |
|:---|:---|:---|
| P5 | `escalation-protocol.md` | 3-iteration rule + escalate path |
| P5 | `fallback-matrix-full.md` | All F1-F19 |

## Validator

| Phase | File | Content |
|:---|:---|:---|
| P5 | `yaml-resilience-layer.md` | 3-level YAML pre-check |
| shared | `quality-gates-reference.md` | YAML-RES-1.0 |
| shared | `pipeline-flowchart.md` | Full pipeline visual reference |
