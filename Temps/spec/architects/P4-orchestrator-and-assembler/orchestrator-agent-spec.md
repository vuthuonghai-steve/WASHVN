# Orchestrator Agent Spec

> Role: **Orchestrator** | Domain: **Execution** | Design: **Contract**
> Source: `orchestrator-agent-spec.md` (full) (clean/)

## Agent definition

```yaml
name: "micro-skill-orchestrator"
role: "Coordinate micro-skill bundle automatically"
trigger: "SCS >= 3.0 AND orchestration-plan.md exists"
```

## Responsibilities

- Read `orchestration-plan.md` from Context Bus
- Check `_state.yaml` status — if `degraded`, activate defensive mode
- Decompose into N independent micro-tasks with clear boundaries
- Spawn N Micro-Skill Builder subagents in parallel
- Manage SSP (State & Signal Protocol) between micro-skills
- Validate data contracts across micro-skill outputs
- Coordinate DAG execution order
- Collect results, trigger Integration Assembler
- Update `_state.yaml` with each micro-skill status

## Must / Must Not

**Must:**
- Generate `orchestrate.py` when SCS >= 3.0
- Every micro-skill must have SSP contract
- In degraded mode: tighten SSP + defensive code
- Validate schema matching between micro-skill output/input
- Spawn builders in parallel when no dependency

**Must not:**
- Write micro-skill code (only coordinate)
- Bypass data contracts between micro-skills
- Run micro-skills sequentially when parallel possible
- Skip SSP validation
- Self-certify PASS — must run mechanical tests

## Orchestrator Sequence

```mermaid
sequenceDiagram
    participant O as Orchestrator
    participant CB as Context Bus
    participant B1 as Builder 1
    participant B2 as Builder 2
    participant B3 as Builder 3
    participant IA as Integration Assembler

    O->>CB: Đọc orchestration-plan.md
    O->>CB: Đọc hydrated-context.yaml
    O->>O: Phân rã N micro-tasks + SSP contracts
    par Spawn song song
        O->>B1: Micro-task 1 (OTP validation)
        O->>B2: Micro-task 2 (Payment gateway)
        O->>B3: Micro-task 3 (Webhook handler)
    end
    B1->>B1: Build micro-skill 1 (5 Phase)
    B2->>B2: Build micro-skill 2 (5 Phase)
    B3->>B3: Build micro-skill 3 (5 Phase)
    B1-->>O: OUTPUT_READY (OTP_VALIDATED)
    B2-->>O: OUTPUT_READY (PAYMENT_COMPLETED)
    B3-->>O: OUTPUT_READY (WEBHOOK_HANDLED)
    O->>O: Validate SSP contracts
    O->>IA: Handoff N micro-skills + SSP map
    IA->>IA: Merge + sinh orchestrate.py + test
    IA-->>O: integration-test-report.md
    O->>CB: Ghi micro-skill-bundle/ + orchestrate.py
```

> See `branch-b-sequence.md` for full Branch B pipeline sequence
