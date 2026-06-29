# Dual Context Ingestion

> Role: **Hydrator** | Domain: **Protocol** | Design: **Integration**
> Source: `architecture-design.md §4.A, §5.1` (clean/)

## Concept

The system maintains TWO parallel context streams:

| Stream | Artifact | Content | Consumed by |
|:---|:---|:---|:---|
| **Technical** | `hydrated-context.yaml` | Contracts, NFR, glossary, zone map | Planner (mandatory), Builder (mandatory) |
| **Cognitive** | `thought-cache.yaml` | Thought blocks, empathy, reasoning, edge cases | Builder (mandatory), Planner (optional) |

## Lifecycle

| Artifact | Created by | Planner reads | Builder reads |
|:---|:---|:---|:---|
| `hydrated-context.yaml` | Stage 1.7 Hydrator | ✅ Mandatory | ✅ Mandatory |
| `thought-cache.yaml` | Stage 0 + Stage 1.5 | Optional | **✅ Mandatory** |

## Builder Phase 1 process

1. Read `hydrated-context.yaml` — get technical scaffolding ("what to code")
2. Read `thought-cache.yaml` — get cognitive depth ("why code this way", "who for")
3. Merge into single context package
4. If `thought-cache.yaml` missing → Fallback F18 (back to Stage 0)

> See `P0/artifact-registry.md` for artifact paths
