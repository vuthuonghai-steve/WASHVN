---
layer: "L2_domain_context"
zone: "knowledge"
skill: "skill-builder"
version: "0.0.3"
trace: "[TỪ DESIGN §3, HANDBOOK §6.4, BA §1.1 S1, R1 close-out]"
last_updated: "2026-06-18"
---

# BUILDER FRAMEWORK — Builder's Knowledge Base

> **Usage**: Read at boot time. Tier 2 — load khi Phase 1-3 (guardrail decisions).
> **Ver-0.0.3 note**: G1-G8 guardrails chi tiết ở `policy/guardrails.md` (L1). File này giữ Builder-specific workflow + 10 guardrails (G1-G10) tổng quan. Section `_parse_zone_mapping` bổ sung cho R1 close-out (validator regex refactor).

---

## Quick Reference

For complete framework details (7 Zones, Pipeline Flow, Naming Conventions, Anti-hallucination), see:
```
../../_shared/knowledge/framework.md
```

For G1-G8 detailed enforcement (severity + actions + tools), see:
- `policy/guardrails.md` (L1)
- `policy/skill-builder.yaml` (L1 root policy)

For knowledge source registry (Tier 1/2/3 routing), see:
- `data/builder-knowledge-sources.yaml`

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

> **Ver-0.0.3**: G1-G8 chi tiết (severity, enforcement tools) chuyển sang `policy/guardrails.md` (L1). Bảng dưới đây là tổng quan 10 guardrails (G1-G10) cho Builder-specific context. Mapping sang L1 policy:

| ID | Rule | L1 Policy Reference |
|----|------|---------------------|
| G1 | **Kỹ sư Phản biện** — Audit design before build | `policy/guardrails.md` §G1 |
| G2 | **Phase-driven Build** — Build by phase, mark-as-done each | `policy/guardrails.md` §G2 |
| G3 | **Log-Notify-Stop** — System error → Log → Notify → **STOP** | `policy/guardrails.md` §G3 |
| G4 | **Placeholder Scale** — Warning at 5, FAIL at 10+ (C2 unified) | `policy/skill-builder.yaml` §placeholder_threshold |
| G5 | **Source Grounding** — Content 100% from design/todo/resources | `policy/guardrails.md` §G4 |
| G6 | **PD Tiering** — Follow Tier 1 vs Tier 2 from `data/builder-knowledge-sources.yaml` | `policy/skill-builder.yaml` §progressive_disclosure |
| G7 | **Build-log Mandatory** — Record decisions, evidence | `policy/guardrails.md` §G5 |
| G8 | **Context Coverage** — Don't miss critical files | `policy/guardrails.md` §G6 |
| G9 | **Knowledge Fidelity** — Don't summarize Critical resources | `policy/skill-builder.yaml` §G7 (zone contract) |
| G10 | **Zone Contract Block** — Only create files in design.md §3 | `policy/guardrails.md` §G7 + `policy/skill-builder.yaml` §zone_contract |

## Cognitive Agentic Skill Paradigm (ver-0.0.3 — dogfooding)

> **Ver-0.0.3 note**: skill-builder 0.0.3 self-applies the paradigm it teaches. See `policy/skill-builder.yaml` for the full L1 split.

The 4-Layer Knowledge Separation is enforced by `policy/skill-builder.yaml` (L1) and consumed by `SKILL.md` (L0):
- **L0** (`SKILL.md`): persona + 5-phase workflow summary + routing map (≤400 tokens)
- **L1** (`policy/skill-builder.yaml`, `policy/workflow.md`, `policy/guardrails.md`, `policy/output-spec.md`): G1-G8 guardrails + must/must_not + thresholds
- **L2** (`knowledge/*.md`): 7 domain knowledge files, loaded on-demand via `data/builder-knowledge-sources.yaml`
- **L3** (`examples/*.md`, `loop/*.md`): concrete builds, fidelity case studies, build-log templates

**`_parse_zone_mapping` helper (R1 close-out)** — applies to `scripts/validate_skill.py` refactor:

```python
import re
from typing import List, Dict

def _parse_zone_mapping(design_path: str) -> List[Dict[str, str]]:
    """
    Parse §3 Zone Mapping from design.md using section-number pattern.
    Supports: '## 3. Zone Mapping', '## 3 Zone Mapping', '## 3. Zones'.
    Shared between check_file_mapping (lines 150-165) and check_todo_cross_reference (lines 349-361).
    """
    with open(design_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Section-number pattern (R1 fix): ^## 3\.\s+ matches "## 3. Zone Mapping", "## 3. Zones", etc.
    SECTION_PATTERN = re.compile(r'^##\s+3\.\s+', re.MULTILINE)
    NEXT_SECTION_PATTERN = re.compile(r'^##\s+\d+\.\s+', re.MULTILINE)

    section_match = SECTION_PATTERN.search(content)
    if not section_match:
        return []

    start = section_match.end()
    next_section = NEXT_SECTION_PATTERN.search(content, start)
    end = next_section.start() if next_section else len(content)
    section_content = content[start:end]

    # Extract file paths from backticks
    files = re.findall(r'`([^`]+)`', section_content)
    return [{"path": f, "tier": "design_spec"} for f in files if "/" in f or "." in f]
```

This helper uses the **section-number pattern** `^## 3\.\s+` (R1 fix) — no longer brittle to heading variations like "## 3. Zones" or "## 3 Zone Mapping". Shared between `check_file_mapping` and `check_todo_cross_reference` to eliminate duplicate parsing logic.

---

## Error Policy

If critical command fails:
1. Append error to `loop/build-log.md`
2. Use **AskUserQuestion** to notify blockage
3. **STOP** all tasks

---

> **Framework Source**: See `../../_shared/knowledge/framework.md` for complete reference
