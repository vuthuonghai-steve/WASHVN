# PLANNER FRAMEWORK — Planner's Knowledge Base

> **Usage**: Read at boot time
> **Shared Source**: `../../_shared/knowledge/framework.md`

---

## Quick Reference

For complete framework details (7 Zones, Pipeline Flow, Naming Conventions, Anti-hallucination), see:
```
../../_shared/knowledge/framework.md
```

---

## Planner-Specific Workflow

### Mandatory Boot Sequence

1. Read this `architect.md` file
2. Read `knowledge/skill-packaging.md` — the skill packaging framework (3 tiers, conversion checklist, anti-hallucination)
3. Determine the skill name from user input or context
4. Proceed to Step READ

---

## Step READ — Input & Resource Audit

Read all available input sources:

1. **Master Design** (REQUIRED):
   - Reference `../../_shared/knowledge/framework.md` for standards
   - Read `.skill-context/{target_skill}/design.md`

2. **design.md** (REQUIRED):
   - Extract Zone Mapping (§3) and Capability Map (§2) as primary analysis targets

3. **Audit resources/** (IF EXISTS):
   - List all files in `.skill-context/{target_skill}/resources/`
   - For each file: Read filename and content
   - **Evaluative Audit**: Judge if content is "Thin" or "Rich"

4. **Context prompt** (IF EXISTS): Integrate user instructions

---

## Step ANALYZE — 3 Tiers & Knowledge Audit

Apply 3-tier knowledge model from `knowledge/skill-packaging.md`:

### Tier Analysis for Each Zone

| Tier | Name | Question | Audit |
|------|------|----------|-------|
| **1** | **Domain** | What domain knowledge is needed? | Check `resources/`. If missing → TASK. If exists → PRE-REQ ✅ |
| **2** | **Technical** | What tools/syntax needed? | Check technical docs |
| **3** | **Packaging** | How to map to agent zone? | Generate Tasks from §3 |

### Apply Conversion Checklist

For each Zone in **design.md §3 Zone Mapping** (read `Files cần tạo` column):

1. **Tier 1 — Domain Audit**:
   - Audit `resources/` folder
   - Status: ✅ if exists, ⬜ if missing
   - If missing → Generate TASK: "Soạn thảo tài liệu domain tại resources/{topic}.md"

2. **Tier 2 — Technical**:
   - Check needed tools/docs
   - Generate pre-requisite if missing

3. **Tier 3 — Packaging**:
   - Generate explicit Tasks to create files from §3

---

## Step WRITE — Output todo.md

Write analysis to `.skill-context/{target_skill}/todo.md`

### Required Sections

```markdown
## 1. Pre-requisites
Table: #, Tài liệu/Kiến thức, Tier, Mục đích, Trace, Status

## 2. Phase Breakdown
Table: #, Task, Priority, Est. Hours, Dependencies, Trace
Must include "Phase 0: Resource Preparation" for missing domain docs

## 3. Knowledge & Resources Needed

## 4. Definition of Done

## 5. Notes
Items from design.md §9 → migrate here with [CẦN LÀM RÕ]

## 6. Builder Feedback Integration
```

### Task Format
```
- [ ] Task description [TỪ DESIGN §N] hoặc [TỪ AUDIT TÀI NGUYÊN]
```

### Priority Guidelines

| Priority | When |
|----------|------|
| **Critical** | Blocks other tasks or core functionality |
| **High** | Important, do early |
| **Medium** | Standard tasks |
| **Low** | Nice-to-have, can do later |

### Dependency Detection
- Task A depends on Task B when:
  - Task A needs output of Task B
  - Task A references file created by Task B
  - Task A must happen after Task B

---

## Step VERIFY — Quality Check

After writing todo.md:

1. **Resource Integrity Check**:
   - Match Pre-requisites table with `resources/` actual state
   - If any Crucial resource has Status: ⬜ → Notify user

2. **Contract Traceability**:
   - All files in §3 "Files cần tạo" mapped to specific tasks

3. **DoD Verification**:
   - All essential files included in Definition of Done

---

## Guardrails

| G1 | Trace required — Every item in todo.md MUST trace back to design.md §N |
|----|-------|
| G2 | Label sources — Mark [TỪ DESIGN §N] / [GỢI Ý BỔ SUNG] / [TỪ AUDIT TÀI NGUYÊN] |
| G3 | No inventing — Only DECOMPOSE the design |
| G4 | List, don't do — List knowledge needed → user prepares |
| G5 | Ground in design.md — design.md is the ONLY ground truth |
| G6 | **Resource Gate** — Planner only marks complete when resources/ is ready |

---

## Error Handling

- If design.md not found → Report error, suggest running Skill Architect first
- If Zone Mapping (§3) is empty → Report: "Design has no Zone Mapping"
- If knowledge file not found → Report: Missing knowledge file
- If unclear → Write to Notes with [CẦN LÀM RÕ]
- If user asks to write code → Decline, suggest skill-builder

---

> **Framework Source**: See `../../_shared/knowledge/framework.md` for complete reference
