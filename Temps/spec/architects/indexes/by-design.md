# Index by Design Concern

> Tra cứu spec theo **mối quan tâm thiết kế**

## Architecture (cấu trúc tổng thể)

| File | Content |
|:---|:---|
| shared/architecture-overview.md | 5-Layer, 2-Branch, 3-Mode overview |
| shared/pipeline-flowchart.md | Full pipeline flowchart visual |
| P0/state-yaml-protocol.md | Pipeline state protocol |
| P0/state-diagram.md | Pipeline state machine visual |
| P4/dag-execution.md | DAG execution architecture |
| P5/yaml-resilience-layer.md | YAML interceptor architecture |
| P6/dual-mode-create-update.md | Dual-Mode pipeline design |
| P7/rebuild-workflow.md | REBUILD flow architecture |

## Contract (ràng buộc dữ liệu + giao thức)

| File | Content |
|:---|:---|
| P0/context-bus-schema.md | Context Bus schema contract |
| P0/context-bus-rules.md | R1-R8 behavioral contract |
| P0/artifact-registry.md | Artifact path + lifecycle contract |
| P1/scs-routing.md | SCS scoring + routing contract |
| P1/spec-gatekeeper.md | Gatekeeper validation contract |
| P2/hydration-schema.md | hydrated-context.yaml schema |
| P4/orchestrator-agent-spec.md | Orchestrator agent contract + sequence |
| P4/ssp-protocol.md | SSP inter-skill contract |
| P6/internal-adapter.md | Internal deconstruction contract |
| P6/external-adapter.md | External deconstruction contract |
| P7/delta-planning.md | Delta planning contract |

## Integration (kết nối giữa các thành phần)

| File | Content |
|:---|:---|
| P0/phase-integration.md | P0 integration with other phases |
| P2/dual-context-ingestion.md | Dual stream merge integration |
| P4/parallel-builders.md | Orchestrator ↔ Builder integration |
| P4/branch-b-sequence.md | Full Branch B pipeline sequence |
| P4/integration-assembler.md | Micro-skill merge integration |
| P6/miner-analyzer.md | Miner ↔ Deconstructor integration |
| P7/in-place-builder.md | Builder ↔ existing skill integration |

## Quality (chất lượng thiết kế + kiểm chứng)

| File | Content |
|:---|:---|
| shared/quality-gates-reference.md | Master quality gate matrix |
| P1/meta-criteria.md | META-1→3 quality criteria |
| P2/thought-cache-check.md | HYD-4 depth cache gates |
| P3/plan-quality-gate.md | PLAN-1→5 quality criteria |
| P3/semantic-sampling-audit.md | SAUDIT sampling audit |
| P7/token-budget-soft-gate.md | BUILD-2.1, BUILD-3.1, REV-3.0 |

## Fallback (xử lý lỗi + rollback)

| File | Content |
|:---|:---|
| P1/re-validation-rule.md | F16-F19 re-validation |
| P2/fallback-integration.md | F5, F6, F18 |
| P3/fallback-matrix.md | F7-F9, F8-EXT |
| P5/fallback-matrix-full.md | F1-F19 complete + fallback flow |
| P5/escalation-protocol.md | 3-iteration escalate |
| P5/phase-compression-fallback.md | PC-1→PC-4 collapse |

## Compression (tối ưu pipeline)

| File | Content |
|:---|:---|
| P5/phase-compression-fallback.md | Phase Compression fallback mapping |

## Verification (kiểm chứng cơ học)

| File | Content |
|:---|:---|
| P3/drift-detection.md | DRIFT-1→4 alignment verification |
| P3/semantic-sampling-audit.md | Semantic audit verification |

## Migration (di trú skill)

| File | Content |
|:---|:---|
| P6/dual-mode-create-update.md | Mode selection design + Dual-Mode flow |
| P7/rebuild-workflow.md | REBUILD design |
