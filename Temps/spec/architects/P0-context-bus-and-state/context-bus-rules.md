# Context Bus Rules (R1-R8)

> Role: **Registry** | Domain: **Protocol** | Design: **Contract**
> Source: `protocols-and-state-spec.md §7` (clean/)

```mermaid
graph TD
    R1["R1: Write-Once-Read-Many"] --> E1["Stage writes artifact once, later stages read"]
    R2["R2: Hydrated Context is inline"] --> E2["Planner reads hydrated_context from Bus, not domain-handbook"]
    R3["R3: Append-only fallback history"] --> E3["All rollbacks go to fallback_history"]
    R4["R4: Version artifacts"] --> E4["Each revision creates new version, no overwrite"]
    R5["R5: Bus = single source of truth"] --> E5["Stages do NOT read upstream files directly"]
    R6["R6: Deconstruction Ingestion"] --> E6["UPDATE/REBUILD: all old knowledge deconstructed into Bus"]
    R7["R7: Hydrator checks thought-cache"] --> E7["Hydrator MUST verify thought-cache.yaml exists and is valid"]
    R8["R8: Optional for Planner, Mandatory for Builder"] --> E8["Builder MUST read thought-cache for Dual Context Ingestion"]
```

| Rule | Description | Enforced by |
|:---|:---|:---|
| R1 | Write-Once-Read-Many | YAML Resilience Layer |
| R2 | Hydrated Context is inline | Context Bus schema |
| R3 | Append-only fallback history | `_state.yaml` protocol |
| R4 | Version artifacts | Context Bus commit hook |
| R5 | Bus = single source of truth | Architectural constraint |
| R6 | Deconstruction Ingestion | UPDATE/REBUILD path |
| R7 | Hydrator checks thought-cache | Stage 1.7 (F18 trigger) |
| R8 | Optional for Planner, Mandatory for Builder | Builder Phase 1 |
