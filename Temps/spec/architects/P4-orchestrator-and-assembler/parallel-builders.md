# Parallel Builders (Stage 3b)

> Role: **Coordinator** | Domain: **Execution** | Design: **Integration**
> Source: `architecture-design.md §5, §5.1` (clean/)

## Branch Splitting

```mermaid
flowchart LR
    DECISION{"SCS Score<br/>(từ Stage 0.5,<br/>validate Stage 1.5)"}
    
    DECISION -->|"SCS < 3.0<br/>Fast Track"| A["Branch A<br/>Single Skill"]
    DECISION -->|"SCS >= 3.0<br/>Full Track OMSP"| B["Branch B<br/>Micro-Skill Bundle"]
    
    A --> A1["Stage 3: Builder<br/>(1 agent)"]
    A1 --> A2["Output: 1 SKILL.md + knowledge/ + scripts/"]
    A2 --> A3["Stage 3.5: Code Reviewer"]
    
    B --> B1["Stage 3a: Orchestrator"]
    B1 --> B2["Stage 3b: Parallel Builders"]
    B2 --> B3["Stage 3c: Integration Assembler"]
    B3 --> B4["Output: N micro-skills + orchestrate.py"]
    B4 --> B5["Stage 3.5: Reviewer + Integration Tester"]
    
    A3 --> COMMON["Stage 4: Sandbox"]
    B5 --> COMMON
    COMMON --> DELIVERY["Stage 5: Delivery"]
    
    style DECISION fill:#d1ecf1,stroke:#0dcaf0,stroke-width:2px
    style B1 fill:#f8d7da,stroke:#dc3545,stroke-width:2px
```

## Builder 5 Phases

```mermaid
flowchart LR
    P0["Phase 0<br/>Intake Verification"] --> P1["Phase 1<br/>Context Hydration<br/>(Dual Context Ingestion)"]
    P1 --> P2["Phase 2<br/>Clarification Gate"]
    P2 --> P3["Phase 3<br/>Contract Implementation"]
    P3 --> P4["Phase 4<br/>Verification & Security"]
    P4 --> P5["Phase 5<br/>Physical Delivery"]
```

## Mechanism

After Orchestrator decomposes the bundle into micro-tasks:

1. Each micro-skill gets a **Builder subagent**
2. Builder reads its context partition from Context Bus (filtered by Orchestrator)
3. All independent micro-skills build **in parallel**
4. Each builder follows standard 5-Phase Builder pipeline

## Execution rules

- If micro-skills have no cross-dependency → **parallel** (default)
- If A → B dependency → A runs first, then B runs in parallel with others
- Orchestrator monitors all builders via SSP signals

## Output

Each micro-skill produces:
- `SKILL.md` + `knowledge/` + `scripts/` package
- SSP signal on completion

## Quality gates

| Gate | Check |
|:---|:---|
| ORCH-1.0 | SSP contracts defined for every micro-skill |
| ORCH-2.0 | Schema matching validated across contracts |
| ORCH-3.0 | Parallel execution (no unnecessary serialization) |
| ORCH-4.0 | Integration test run and passed |
