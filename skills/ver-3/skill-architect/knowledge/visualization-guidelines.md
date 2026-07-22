---
name: visualization-guidelines
version: 0.0.1
suite: WASHVN
tags: [architect, mermaid, diagrams, visualization]
---

# Visualization & Diagram Guidelines

This guide defines how to create effective, concrete, and unambiguous architecture diagrams for Agent Skills. Use when designing a new skill to ensure clarity for both humans and AI.

## Principle: "Show, then explain"

For each major concept, FIRST draw a diagram, THEN add a table or text that explains details the diagram cannot convey. Never replace a diagram with a table.

### "Show, then explain" Examples

**Good** — Data Contract Visualization:
```mermaid
flowchart LR
    subgraph Inputs[Input Contracts]
        EX[exploration.md] --> A
        DH[domain-handbook.md] --> A
        CR[criteria.md] --> A
    end
    A[Architect] --> DM[design.md]
    A --> DRC[drc.yaml]
```
Then explain: "Three upstream artifacts feed the architect. Two outputs: design.md (primary, WORM lifecycle) and drc.yaml (routing contract). Design.md consumed by gatekeeper S1.5 and planner S2. drc.yaml consumed by gatekeeper S1.5 only."

**Good** — State Machine Visualization:
```mermaid
stateDiagram-v2
    [*] --> Idle
    Idle --> Phase1: inputs_ready
    Phase1 --> Gate1: consumed
```
Then explain: "The workflow starts in Idle. When all 3 inputs are ready, transition to Phase 1. After consumption, gate evaluation."

## Diagram Types & When to Use

| # | Diagram Type | Mermaid Syntax | Use When |
|---|---|---|---|
| D1 | **Folder Structure** | `mindmap` | ALWAYS — show the skill's directory tree |
| D2 | **Execution Flow** | `sequenceDiagram` | ALWAYS — show runtime interaction |
| D3 | **Workflow Phases** | `flowchart LR` | Multi-phase with clear stages |
| D4 | **Relationship** | `flowchart TD` | External systems or skill connections |
| D5 | **Data Flow** | `flowchart LR` | Data transforms through multiple stages |

## Mermaid Skeletons

### D1 — Folder Structure (Mindmap)
```mermaid
mindmap
  root((skill-name))
    SKILL.md
    knowledge
      domain-ref.md
    scripts
      init-context.py
    templates
      design.md.template
    loop
      checklist.md
    data
      drc.yaml
    assets
```

### D2 — Execution Flow (Sequence)
```mermaid
sequenceDiagram
    participant U as User
    participant S as Skill
    participant K as Knowledge
    participant L as Loop

    U->>S: Input
    S->>K: Read references
    S->>S: Process
    S->>L: Self-verify
    alt Pass
        S->>U: Output
    else Fail
        L-->>S: Retry
    end
```

### D3 — Workflow Phases (Flowchart)
```mermaid
flowchart LR
    P1[Phase 1] -->|gate| P2[Phase 2] -->|gate| P3[Phase 3]
    P1 -.-> I1[Interaction Point]
    P2 -.-> I2[Interaction Point]
    P3 -.-> I3[Output Gate]
```

### D4 — Relationship (Flowchart)
```mermaid
flowchart TD
    User -->|input| SkillA
    SkillA -->|output| ContextDir
    ContextDir -->|input| SkillB
    SkillB -->|output| FinalProduct
```

## State Diagram Syntax (stateDiagram-v2)

### Skeleton for §4 State Machine

```mermaid
stateDiagram-v2
    [*] --> InitialState
    InitialState --> Phase1: trigger_condition

    Phase1 --> Gate1: phase_complete
    Gate1 --> Phase2: PASS (condition)
    Gate1 --> Fail_Fallback: FAIL (reason)

    Phase2 --> Gate2: phase_complete
    Gate2 --> Complete: PASS
    Gate2 --> Fail_Fallback: FAIL

    Fail_Fallback --> InitialState: revise_initiated
    Complete --> InitialState: new_request
```

### Rules for State Diagrams
- Initial state must be named (not just `[*]`)
- Every transition must have a trigger label
- All decision gates must have both PASS and FAIL transitions (no single-branch gates)
- Fallback states (F3, F8) must be reachable from every gate
- Use `stateDiagram-v2` syntax (not `stateDiagram`)
- Guard conditions in parentheses: `PASS (condition_met)`
- States should be CamelCase (Phase1_Read, Gate_ARCH1)

### Example: 6-Phase State Machine

```mermaid
stateDiagram-v2
    [*] --> Idle
    Idle --> Phase1_Read: inputs_ready
    Phase1_Read --> Gate_ARCH1: consumed
    Gate_ARCH1 --> Phase2_ZoneMapping: PASS (anchors_present)
    Gate_ARCH1 --> Fail_F3_Revise: FAIL (missing_anchors)
    Phase2_ZoneMapping --> Gate_ARCH3: zones_mapped
    Gate_ARCH3 --> Phase3_DataContracts: PASS (7_zones)
    Gate_ARCH3 --> Fail_F3_Revise: FAIL (incomplete)
    Phase3_DataContracts --> Gate_ARCH2: contracts_defined
    Gate_ARCH2 --> Phase4_StateDiagram: PASS (valid_schemas)
    Gate_ARCH2 --> Fail_F3_Revise: FAIL (schema_invalid)
    Phase4_StateDiagram --> Gate_ARCH4: rendered
    Gate_ARCH4 --> Phase5_MustNotRules: PASS (valid_diagram)
    Gate_ARCH4 --> Fail_F3_Revise: FAIL (invalid_diagram)
    Phase5_MustNotRules --> Gate_META2_S1: rules_defined
    Gate_META2_S1 --> Phase6_Emit: PASS (≥5/phase)
    Gate_META2_S1 --> Fail_F3_Revise: FAIL (<5/phase)
    Phase6_Emit --> Gate_Final_META123: written
    Gate_Final_META123 --> Complete: PASS (all)
    Gate_Final_META123 --> Fail_F3_Revise: FAIL (meta)
    Gate_Final_META123 --> Fail_F8_Drift: DRIFT
    Fail_F3_Revise --> Idle: revise
    Fail_F8_Drift --> Idle: re_elicit
    Complete --> Idle: new_request
```

## Pipeline Integration Diagram Styling

```mermaid
flowchart LR
    subgraph Pipeline[8-Stage Pipeline]
        E[Explorer] --> KM[Miner]
        KM --> A[Architect]
        A --> GK[Gatekeeper]
        GK --> P[Planner]
        P --> B[Builder]
        B --> R[Reviewer]
        R --> T[Tester]
        T --> I[Indexer]
    end

    style E fill:#e8f5e9,stroke:#2e7d32
    style KM fill:#c8e6c9,stroke:#388e3c
    style A fill:#ffcdd2,stroke:#e53935,stroke-width:3px
    style GK fill:#fff9c4,stroke:#fbc02d
    style P fill:#bbdefb,stroke:#1565c0
    style B fill:#90caf9,stroke:#1976d2
    style R fill:#e1f5fe,stroke:#01579b
    style T fill:#f3e5f5,stroke:#7b1fa2
    style I fill:#fff3e0,stroke:#ef6c00
```

## Quality Checklist for Diagrams

- [ ] Each diagram has a clear title or is under a descriptive heading
- [ ] Participants/nodes use short, readable labels
- [ ] Decision points (alt/else, gates) are visible where logic branches
- [ ] Interaction points with user are explicitly marked
- [ ] Diagram renders correctly in standard Mermaid (no unsupported syntax)
- [ ] State diagrams have both PASS and FAIL transitions from all gates
- [ ] Fallback routes (F3, F8) are present where applicable

---

> **Last Updated**: 2026-07-22
> **Purpose**: Mermaid visualization standards for skill-architect ver-3
