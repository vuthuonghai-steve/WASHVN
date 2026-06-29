# In-place Builder

> Role: **Builder** | Domain: **Execution** | Design: **Integration**
> Source: `skill-migration-spec.md §13.6` (clean/)

## Purpose

In UPDATE mode, Builder applies changes directly to existing skill files instead of recreating from scratch.

## Process

```
Delta todo.md
      │
      ▼
For each delta task:
  ├── type: "create"   → Write new file at target path
  ├── type: "modify"   → Read file → apply patch → verify
  └── type: "delete"   → Remove file + update registry
      │
      ▼
Verify modified skill still works:
  - Structural integrity (7-zone completeness)
  - Existing functionality unchanged
  - New changes applied correctly
```

## Builder 5 phases (modified for in-place)

| Phase | Delta adaptation |
|:---|:---|
| P0 Intake Verification | Verify target skill path exists and readable |
| P1 Context Hydration | Dual Context + old state understanding |
| P2 Clarification Gate | Check if delta plan aligns with constraints |
| P3 Contract Implementation | **In-place** edits (patches, not full writes) |
| P4 Verification & Security | Verify old functionality preserved |
| P5 Physical Delivery | Update build-log + _state.yaml |

## Quality gates

- BUILD-1.1: Zone Contract — files modified in correct zones
- BUILD-2.1: Placeholder Density — zero new placeholders (soft gate)
- BUILD-4.1: Executable — skill still runs after modifications
