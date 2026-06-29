# REBUILD Workflow

> Role: **Gatekeeper** | Domain: **Migration** | Design: **Architecture**
> Source: `skill-migration-spec.md §14` (clean/)

## When to REBUILD

- External skill being migrated into WASHVN ecosystem
- Existing skill with fundamentally broken architecture
- Skill version jump requiring complete re-think

## Process

1. **External Deconstructor** (P6) → read source, convert to metadata
2. **Miner** → analyze intent + advantages
3. **Architect** → full re-design (preserving original intent)
4. **Planner** → standard full plan (not delta)
5. **Builder** → create fresh directory + files
6. **Reviewer** → check old intent preserved in new design
7. **Sandbox** → full test suite

## Intent preservation

Architect's primary constraint in REBUILD mode:

> "Giữ nguyên ý chí thiết kế cũ" — preserve original design intent

This means:
- Core persona stays the same
- Business rules preserved (even if implementation changes)
- Edge case handling from old skill carried forward
- Must_not rules from old skill merged with new design

## Output

- New skill directory with canonical 7-Zone structure
- `migration-log.md` documenting what changed and why
- Updated `_state.yaml` with execution_mode: "REBUILD"
