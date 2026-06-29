# Delta Planning

> Role: **Planner** | Domain: **Execution** | Design: **Contract**
> Source: `skill-migration-spec.md §13.6` (clean/)

## Purpose

In UPDATE mode, Planner generates ONLY the delta tasks — changes needed — rather than a full plan from scratch.

## Input

- `deconstructed_context` from Context Bus (P6 output)
- Current `design.md` vN (existing)
- New `design.md` vN+1 (provided by Architect)

## Delta analysis

Compare old vs new design to identify:

| Change type | Example | Action |
|:---|:---|:---|
| **Added** | New zone, new contract | Create new files |
| **Modified** | Updated persona, changed rules | Patch existing files |
| **Deleted** | Deprecated zones, removed contracts | Remove files |
| **Unchanged** | Same content | Skip (no action) |

## Output: Delta todo.md

```yaml
tasks:
  - id: "D001"
    type: "modify"
    target: "SKILL.md"
    change: "Update persona to include payment-gateway domain"
    zone: "core"
  - id: "D002"
    type: "create"
    target: "knowledge/payment-rules.md"
    content: "Payment validation rules from design.md §2"
    zone: "knowledge"
```

## Benefits

- Minimizes token usage (only changed parts)
- Preserves old skill's working functionality
- Reduces hallucination risk (less code regenerated)
- Faster pipeline for small updates
