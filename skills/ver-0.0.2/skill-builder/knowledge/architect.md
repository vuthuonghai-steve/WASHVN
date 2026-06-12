# BUILDER FRAMEWORK — Builder's Knowledge Base

> **Usage**: Read at boot time
> **Shared Source**: `../../_shared/knowledge/framework.md`

---

## Quick Reference

For complete framework details (7 Zones, Pipeline Flow, Naming Conventions, Anti-hallucination), see:
```
../../_shared/knowledge/framework.md
```

---

## Builder-Specific Workflow

### Phase 1: PREPARE & Evaluate

**Before starting**: Read `knowledge/architect.md` — 7-Zone framework.

Read all inputs and assess feasibility:

- Read `.skill-context/{target_skill}/design.md` (Architecture)
- Read `.skill-context/{target_skill}/todo.md` (Execution Plan)
- Read `.skill-context/{target_skill}/resources/` (Domain Data)
- Read `.skill-context/{target_skill}/data/` if present
- Read `.skill-context/{target_skill}/loop/` if present
- **Context Inventory**: Classify as `Critical` (design.md, todo.md, resources/*, data/*) or `Supportive` (loop/*)
- **The Stance**: Audit design, identify logic flaws, build mental model of phases

---

### Phase 2: CLARIFY (Closing the Loop)

Scan `todo.md` for `[CẦN LÀM RÕ]` or logic flaws. Ask user clarification (Max 5 items). Record answers into design.md §Clarifications.

→ **[⏸️ Gate]**: Wait for user clarification before proceeding

---

### Phase 3: BUILD (Phase-Driven)

**Before starting**: Read:
- `knowledge/build-guidelines.md` — Content writing rules
- `knowledge/anthropic-skill-standards.md` — Required for SKILL.md files

Execute `todo.md` phase by phase:

- **Zone Contract**: Only create files in `design.md §3` (Zone Mapping). No hallucination
- **SKILL.md Writing**: Apply anthropic-skill-standards.md §1-8. YAML frontmatter line 1. Map §7 (PD), §5 (Flow), §6 (Gates). If 3+ phases → add Tracker Checklist. If abstract mappings → reference examples
- **loop/ Writing**: Map `design.md §8` (Risks) into measurable checklist items
- **Fidelity Rule**: 1:1 conceptual mapping. If source has 10 items, target MUST have 10 items
- **Double-Pass**: After each phase, refine to check for information loss
- **Progress Tracking**: Mark tasks done in `todo.md` only after verified
- **Usage Trace**: Append to `.skill-context/{target_skill}/build-log.md` with format: `Task -> Output -> Source files`

---

### Phase 4: VERIFY (The Gatekeeper)

Run quality gates:

- Run validator script if available
- Apply `loop/build-checklist.md`
- **Placeholder Density**: <5 PASS, 5-9 WARNING, 10+ FAIL

---

### Phase 5: DELIVER

Finalize `loop/build-log.md`. Present results in `.skill-context/{target_skill}/build-log.md`. Ensure mandatory sections:

- `## Resource Inventory`
- `## Resource Usage Matrix`
- `## Validation Result`

---

## Context Directory Coverage

```
.skill-context/{target_skill}/
├── design.md              # Architecture source of truth
├── todo.md                # Execution plan source of truth
├── build-log.md           # Evidence + usage matrix + validation log
├── resources/             # Domain references
├── data/                 # Rule configs
└── loop/                 # Prior checks, phase logs
```

### Resource Priority

| Priority | Contents |
|----------|----------|
| **Critical** | design.md, todo.md, all resources/*, all data/* |
| **Supportive** | all loop/*, proof/snapshots |

---

## Guardrails

| ID | Rule |
|----|------|
| G1 | **Kỹ sư Phản biện** — Audit design before build |
| G2 | **Phase-driven Build** — Build by phase, mark-as-done each |
| G3 | **Log-Notify-Stop** — System error → Log → Notify → **STOP** |
| G4 | **Placeholder Scale** — Warning at 5, FAIL at 10+ |
| G5 | **Source Grounding** — Content 100% from design/todo/resources |
| G6 | **PD Tiering** — Follow Tier 1 vs Tier 2 from design.md §7 |
| G7 | **Build-log Mandatory** — Record decisions, evidence |
| G8 | **Context Coverage** — Don't miss critical files |
| G9 | **Knowledge Fidelity** — Don't summarize Critical resources |
| G10 | **Zone Contract Block** — Only create files in design.md §3 |

---

## Error Policy

If critical command fails:
1. Append error to `loop/build-log.md`
2. Use **AskUserQuestion** to notify blockage
3. **STOP** all tasks

---

> **Framework Source**: See `../../_shared/knowledge/framework.md` for complete reference
