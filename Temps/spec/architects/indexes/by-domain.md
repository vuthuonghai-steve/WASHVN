# Index by Domain

> Tra cứu spec theo **lĩnh vực domain**

## Data

| File | Content |
|:---|:---|
| P0/context-bus-schema.md | Context Bus YAML schema |
| P0/artifact-registry.md | All artifacts, paths, ownership |
| P2/hydration-schema.md | hydrated-context.yaml schema |

## Protocol

| File | Content |
|:---|:---|
| P0/context-bus-rules.md | R1-R8 rules |
| P0/state-yaml-protocol.md | _state.yaml state protocol |
| P0/state-diagram.md | Pipeline state machine visual |
| P0/phase-integration.md | Foundation integration rules |
| P1/scs-routing.md | SCS → Branch routing protocol |
| P2/dual-context-ingestion.md | Two-stream ingestion protocol |
| P2/fallback-integration.md | Hydrator fallback paths |
| P3/fallback-matrix.md | P3-specific fallbacks |
| P4/ssp-protocol.md | SSP inter-micro-skill protocol |
| P5/fallback-matrix-full.md | F1-F19 complete |
| P5/escalation-protocol.md | 3-iteration escalation |
| P5/phase-compression-fallback.md | PC-1→PC-4 collapse |

## Quality

| File | Content |
|:---|:---|
| shared/quality-gates-reference.md | Master quality gate matrix |
| P1/spec-gatekeeper.md | Gatekeeper responsibilities |
| P1/meta-criteria.md | META-1→3 criteria |
| P1/re-validation-rule.md | Thought block re-validation |
| P2/thought-cache-check.md | HYD-4 thought-cache gates |
| P3/plan-quality-gate.md | PLAN-1→5 criteria |
| P3/drift-detection.md | DRIFT-1→4 alignment checks |
| P3/semantic-sampling-audit.md | SAUDIT-1→1.2 |
| P7/token-budget-soft-gate.md | BUILD-2.1, BUILD-3.1, REV-3.0 |

## Execution

| File | Content |
|:---|:---|
| P4/orchestrator-agent-spec.md | Orchestrator definition + sequence |
| P4/branch-b-sequence.md | Full Branch B pipeline sequence view |
| P4/parallel-builders.md | Parallel spawning + 5-phase |
| P4/integration-assembler.md | Merge + orchestrate.py |
| P4/dag-execution.md | DAG dependency execution |
| P7/delta-planning.md | Delta planning logic |
| P7/in-place-builder.md | In-place modification |

## Resilience

| File | Content |
|:---|:---|
| P5/yaml-resilience-layer.md | 3-level pre-check, auto-repair, degraded mode |

## Migration

| File | Content |
|:---|:---|
| P6/internal-adapter.md | Internal skill deconstructor |
| P6/external-adapter.md | External skill deconstructor |
| P6/dual-mode-create-update.md | CREATE/UPDATE/REBUILD routing |
| P7/rebuild-workflow.md | Full REBUILD process |

## Knowledge

| File | Content |
|:---|:---|
| P6/miner-analyzer.md | Domain-handbook construction |
| shared/glossary.md | Pipeline glossary |
| shared/architecture-overview.md | 5-Layer overview (compact) |
| shared/pipeline-flowchart.md | Full pipeline flowchart visual |

## Glossary

| File | Content |
|:---|:---|
| shared/glossary.md | Common pipeline terminology |
