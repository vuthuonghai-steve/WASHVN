# Visualization & Diagram Guidelines

This guide defines how to create effective, concrete, and unambiguous architecture diagrams for Agent Skills. Use these when designing a new skill to ensure clarity for both humans and AI.

## Principle: "Show, then explain"

For each major concept, FIRST draw a diagram, THEN add a table or text that explains details the diagram cannot convey. Never replace a diagram with a table.

## Diagram Types & When to Use

| #  | Diagram Type       | Mermaid Syntax  | Use When                                          |
| -- | ------------------ | --------------- | ------------------------------------------------- |
| D1 | **Folder Structure** | `mindmap`     | ALWAYS — show the skill's directory tree           |
| D2 | **Execution Flow**   | `sequenceDiagram` | ALWAYS — show runtime interaction between participants |
| D3 | **Workflow Phases**  | `flowchart LR` | Skill has multi-phase workflow with clear stages   |
| D4 | **Relationship**     | `flowchart TD` | Skill connects to external systems or other skills |
| D5 | **Data Flow**        | `flowchart LR` | Skill transforms data through multiple stages      |

## Mermaid Skeletons

Use these as starting points. Adapt them to the specific skill being designed.

### D1 — Folder Structure (Mindmap)
```mermaid
mindmap
  root((skill-name))
    SKILL.md
      Persona
      Phases
      Guardrails
    knowledge
      domain-ref.md
    scripts
      tool.py
    templates
      output.md.template
    loop
      checklist.md
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

## Quality Checklist for Diagrams

- [ ] Each diagram has a clear title or is placed under a descriptive heading.
- [ ] Participants/nodes use short, readable labels.
- [ ] Decision points (alt/else, diamond nodes) are visible where logic branches.
- [ ] Interaction points with user are explicitly marked.
- [ ] Diagram renders correctly in standard Mermaid (no unsupported syntax).

---

## Skill Creation Specific Diagrams

These diagrams are specifically designed for the skill creation workflow (skill-architect → skill-planner → skill-builder pipeline).

### SD1 — Master Pipeline Diagram

Shows the complete skill development pipeline with all 3 roles:

```mermaid
flowchart LR
    subgraph MasterPipeline [Master Skill Suite Pipeline]
        direction LR
        A[skill-architect<br/>Design] -->|design.md| P[skill-planner<br/>Plan] -->|todo.md| B[skill-builder<br/>Build]
    end

    User -->|Requirements| A
    B -->|Skill Files| User

    style A fill:#ffcdd2,stroke:#e53935
    style P fill:#fff9c4,stroke:#fbc02d
    style B fill:#c8e6c9,stroke:#388e3c
```

### SD2 — Skill Lifecycle Diagram

Shows how a skill is created, used, and maintained:

```mermaid
flowchart TD
    subgraph Lifecycle [Skill Lifecycle]
        Init[Initialize] --> Design[Design]
        Design --> Plan[Plan]
        Plan --> Build[Build]
        Build --> Test[Test]
        Test --> Deploy[Deploy]
        Deploy --> Maintain[Maintain]
        Maintain -.->|Feedback| Design
    end

    Init -.->|init_context.py| Design

    style Init fill:#e3f2fd,stroke:#1e88e5
    style Design fill:#ffcdd2,stroke:#e53935
    style Plan fill:#fff9c4,stroke:#fbc02d
    style Build fill:#c8e6c9,stroke:#388e3c
    style Test fill:#e1f5fe,stroke:#01579b
    style Deploy fill:#f3e5f5,stroke:#7b1fa2
    style Maintain fill:#fff3e0,stroke:#ef6c00
```

### SD3 — 3-Pillar Analysis Flow

Visualize how the 3 Pillars (Knowledge, Process, Guardrails) map to the skill zones:

```mermaid
flowchart LR
    subgraph Knowledge[Pillar 1: Knowledge]
        K1[Domain Info]
        K2[Standards]
        K3[Best Practices]
    end

    subgraph Process[Pillar 2: Process]
        P1[Workflow]
        P2[Phases]
        P3[Decision Points]
    end

    subgraph Guardrails[Pillar 3: Guardrails]
        G1[Quality Checks]
        G2[Error Handling]
        G3[Verification]
    end

    Knowledge --> Skill[Agent Skill]
    Process --> Skill
    Guardrails --> Skill

    style Knowledge fill:#e8f5e9,stroke:#2e7d32
    style Process fill:#e3f2fd,stroke:#1e88e5
    style Guardrails fill:#ffebee,stroke:#c62828
    style Skill fill:#f9f9f9,stroke:#333,stroke-width:4px
```
