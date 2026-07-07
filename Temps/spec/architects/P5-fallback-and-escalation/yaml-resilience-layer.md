# YAML Resilience Layer

> Role: **Validator** | Domain: **Resilience** | Design: **Architecture**
> Source: `protocols-and-state-spec.md §11` (clean/)

## Purpose

Cross-cutting middleware that validates YAML artifacts before Context Bus commit. Not a separate stage — an interceptor on every write.

## Pre-check pipeline (3 Levels)

| Level | Check | Fail action |
|:---|:---|:---|
| **L1 Syntax** | `yaml.safe_load()` parse | Auto-repair (max 2 attempts) |
| **L2 Schema** | Required keys + types + constraints | Auto-repair (max 2 attempts) |
| **L3 Cross-ref** | File paths exist + non-empty | Graceful degradation |

## Auto-repair protocol

- Max 2 repair attempts per artifact
- Repair subagent fixes (indentation, nesting) — preserves semantics
- After 2 fails → trigger fallback for source stage to regenerate

## Graceful degradation (Level 3)

**Critical refs** (design.md, hydrated-context.yaml, todo.md, orchestration-plan.md):
- Hard Halt — pipeline cannot proceed
- Fallback to source stage

**Non-critical refs** (domain-handbook.md, quality-matrix.yaml, criteria.md):
- Warning only → `_state.yaml.status = "degraded"`
- Pipeline continues in defensive mode
- Downstream agents auto-activate safety defaults

## Integration

```yaml
integration_rules:
  rule_1: "Every YAML artifact write calls yaml_resilience.pre_check()"
  rule_2: "PASS → commit proceeds normally"
  rule_3: "Level 1 FAIL → auto-repair (max 2)"
  rule_4: "Level 2 FAIL → auto-repair (max 2)"
  rule_5: "Level 3 FAIL: Critical → Hard Halt; Non-critical → degraded"
  rule_6: "Repair 2nd fail → trigger fallback to source stage"
  rule_7: "All repair events → `_state.yaml.yaml_repair_history`"
  rule_8: "All grace warnings → `_state.yaml.graceful_warnings`"
  rule_9: "HOOK-HEAL-1.0 acts as a last-mile verification gate on Stop/SubagentStop events to catch any uncommitted or corrupted YAML state (_state.yaml) or formatting defects, feeding back errors to the agent context for self-healing before session exit."
```

> See `shared/quality-gates-reference.md` for YAML-RES-1.0 and HOOK-HEAL-1.0
