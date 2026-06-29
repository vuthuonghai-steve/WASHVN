# Glossary — Pipeline Terms

> Domain: **Glossary** | Applies to: **All phases P0-P7**

| Term | Definition |
|:---|:---|
| **Context Bus** | Shared state layer — every stage reads/writes here. Single source of truth |
| **`_state.yaml`** | Pipeline state protocol — tracks stage status, fallback history, iteration |
| **SCS** | Skill Complexity Score (1.0–5.0). Determines Fast Track vs Full Track |
| **SCS Router** | Component that evaluates SCS and routes to Branch A or B |
| **Spec Gatekeeper** | Validates design quality, enforces META-criteria, re-validates SCS |
| **Context Hydrator** | Prepares condensed context package for Planner from Bus artifacts |
| **Drift Detector** | Detects plan-to-design misalignment before Builder starts |
| **Hydrated Context** | Condensed context package: glossary, NFR, contracts, must_not |
| **thought-cache.yaml** | Cognitive depth artifact — thought blocks, empathy, reasoning |
| **Orchestrator** | Subagent that coordinates parallel micro-skill builders (Branch B) |
| **SSP** | State & Signal Protocol — inter-micro-skill communication |
| **Dual-Mode** | Pipeline supporting CREATE / UPDATE / REBUILD execution modes |
| **Deconstructor** | Adapter that reads existing skill structure into Context Bus |
| **Phase Compression** | Branch A optimization — collapses 8 stages into 3 phases (D1-D3) |
| **YAML Resilience Layer** | Middleware that validates YAML artifacts before Context Bus commit |
| **Fallback (F1-F19)** | Defined rollback paths when a stage fails |
| **Quality Gates** | Binary pass/fail criteria checked at each stage |
| **META-criteria** | Gatekeeper-level criteria for design quality (META-1→3) |
| **REV-3.0** | Automatic refactor trigger when token budget or placeholder soft gates fire |

> Source: `architecture-design.md`, `protocols-and-state-spec.md` (clean/)
