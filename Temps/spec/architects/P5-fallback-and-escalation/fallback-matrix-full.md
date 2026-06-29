# Fallback Matrix (F1-F19)

> Role: **Gatekeeper** | Domain: **Protocol** | Design: **Fallback**
> Source: `protocols-and-state-spec.md §8` (full) (clean/)

## Fallback Flow

```mermaid
flowchart TD
    S0["Stage 0<br/>BA Elicitor"]
    S05["Stage 0.5<br/>SCS Router"]
    S07["Stage 0.7<br/>Miner"]
    S1["Stage 1<br/>Architect"]
    S15["Stage 1.5<br/>Spec Gatekeeper"]
    S17["Stage 1.7<br/>Context Hydrator"]
    S2["Stage 2<br/>Planner"]
    S25["Stage 2.5<br/>Drift Detector + Plan Gate"]
    S3A["Stage 3<br/>Builder (Branch A)"]
    S3B["Stage 3a-c<br/>Orchestrator+Builders (Branch B)"]
    S35["Stage 3.5<br/>Code Reviewer"]
    S4["Stage 4<br/>Sandbox"]
    S5["Stage 5<br/>Delivery"]

    S0 --> S05 --> S07 --> S1 --> S15 --> S17 --> S2 --> S25
    S25 -->|"Pass"| S3A
    S25 -->|"Pass"| S3B
    S3A --> S35
    S3B --> S35
    S35 --> S4 --> S5

    S05 -.->|"F1: thiếu thông tin SCS"| S0
    S07 -.->|"F2: domain-handbook thiếu"| S0
    S15 -.->|"F3: criteria fail"| S1
    S15 -.->|"F4: SCS thay đổi"| S05
    S17 -.->|"F5: context thiếu"| S1
    S17 -.->|"F6: glossary thiếu"| S07
    S25 -.->|"F7: drift minor"| S2
    S25 -.->|"F8: drift major"| S1
    S25 -.->|"F9: design sai domain"| S05
    S35 -.->|"F10: review fail (A)"| S3A
    S35 -.->|"F11: review fail (B)"| S3B
    S35 -.->|"F12: integration fail"| S2
    S4 -.->|"F13: sandbox fail (A)"| S3A
    S4 -.->|"F14: sandbox fail (B)"| S3B
    S4 -.->|"F15: plan sai"| S2
```

## Full fallback table

| ID | Stage Fail | Cause | Back to | Action |
|:---|:---|:---|:---|:---|
| **F1** | S0.5 SCS Router | Insufficient SCS info | Stage 0 | BA re-elicitation |
| **F2** | S0.7 Miner | Domain-handbook insufficient | Stage 0 | Re-elicitation |
| **F3** | S1.5 Gatekeeper | Criteria fails meta-criteria | Stage 1 | Architect revise design |
| **F4** | S1.5 Gatekeeper | SCS score changed | Stage 0.5 | Re-evaluate SCS, re-route |
| **F5** | S1.7 Hydrator | Context insufficient | Stage 1 | Architect add contracts |
| **F6** | S1.7 Hydrator | Glossary < 10 terms | Stage 0.7 | Miner expand domain-handbook |
| **F7** | S2.5 Drift Detector | Drift minor | Stage 2 | Planner re-plan |
| **F8** | S2.5 Drift Detector | Drift major | Stage 1 | Architect revise design |
| **F8-EXT** | S2.5 Semantic Audit | PASS-form, FAIL-meaning | S1 / S0 | Design revise or re-elicitation |
| **F9** | S2.5 Drift Detector | Design wrong domain | Stage 0.5 | Re-evaluate SCS |
| **F10** | S3.5 Reviewer | Review fail (Branch A) | Stage 3 | Builder re-build |
| **F11** | S3.5 Reviewer | Review fail (Branch B) | Stage 3c | Assembler re-assemble |
| **F12** | S3.5 Reviewer | Integration fail | Stage 2 | Planner revise orchestration-plan |
| **F13** | S4 Sandbox | Sandbox fail (Branch A) | Stage 3 | Builder re-build |
| **F14** | S4 Sandbox | Sandbox fail (Branch B) | Stage 3c | Assembler re-assemble |
| **F15** | S4 Sandbox | Plan wrong (root cause) | Stage 2 | Planner re-plan |
| **F16** | S0 BA | thought-cache missing thought_process | Stage 0 | Re-do elicitation |
| **F17** | S1.5 Gatekeeper | thought-cache missing empathy/questions | Stage 0 | Re-do stakeholder analysis |
| **F18** | S1.7 Hydrator | thought-cache missing/empty | Stage 0 | Depth Recovery |
| **F19** | S0 BA | thought block FAIL META-2.1 | Stage 0 | Deep thinking re-do |

## Common rules

- **Max 3 iterations** per stage → escalate
- **Append-only** `fallback_history` in `_state.yaml`
- **Root cause first**: nearest stage first, repeat → deeper fallback
- **Context Bus preserved** — only append new versions on fallback
