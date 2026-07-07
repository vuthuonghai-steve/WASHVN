# `_state.yaml` Protocol

> Role: **Registry** | Domain: **Protocol** | Design: **Architecture**
> Source: `protocols-and-state-spec.md §9` (clean/)

## Schema

```yaml
pipeline_state:
  version: "2.0"
  run_id: "run_001"
  created_at: "2026-06-25T10:00:00Z"
  
  execution_mode: "UPDATE"          # CREATE | UPDATE | REBUILD
  source_skill_ref: "/path/to/old-skill"
  
  current_stage: "stage_2_planner"
  previous_stage: "stage_1_7_hydrator"
  status: "in_progress"            # in_progress | completed | blocked | failed | escalated | degraded
  iteration_count: 1
  max_iterations: 3
  
  scs_score: 3.5
  branch: "branch_b_micro_skill"   # branch_a_single | branch_b_micro_skill
  routing_mode: "Full-Track OMSP"
  
  context_bus_ref: ".skill-context/{target}/context-bus.yaml"
  
  artifacts: {design_md: {path,status,version}, todo_md: {...}}
  fallback_history: []             # Append-only
  stage_status: {}                 # Per-stage tracking
  micro_skill_tracking: {}         # Branch B only
  escalation: {triggered, reason, escalated_to, depth, last_triggered_at, last_failure_summary}
```

## State transitions

```
in_progress → completed | blocked | failed | escalated | degraded
```

## Escalation protocol

- Triggered when iteration_count > max_iterations (3)
- Escalate to: oracle | user
- Pipeline halts until resolution

> See `state-diagram.md` for visual state machine
> See `P5-fallback-and-escalation/` for full fallback/escalation details
