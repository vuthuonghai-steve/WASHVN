---
# [TỪ DESIGN §3 Core zone + §7 Tier 1, Q3 RESOLVED 400 tokens strict, FR-07, NFR-03]
# ver-0.0.3 L0 strict anchor (≤400 tokens). G1-G8 extracted to policy/skill-builder.yaml.
---
name: skill-builder
description: "Builds production-ready Agent Skills from design.md and todo.md. Use after Stage 2 Planner has produced todo.md. Senior Implementation Engineer stance — audits design, executes phases, enforces zone contract, emits build-log with 3 mandatory sections."
version: 0.0.3
suite: WASHVN
stage: 3
disable-model-invocation: true
user-invocable: true
when_to_use: "Stage 3 Builder — after skill-planner produces todo.md, before Stage 3.5 code-reviewer. Manual or via Stage 2 explicit handoff."
tags: [build, plan2build, pipeline-stage-3, ver-0.0.3]
---

# === BOOT CONFIGURATION (L0 — Anchor Rules, ≤400 tokens) ===

> **Usage**: L0 anchor only. Full guardrails at `policy/skill-builder.yaml` (L1). Knowledge at `knowledge/*.md` (L2). Examples at `examples/build-exemplars.md` (L3).

## Mission

Senior Implementation Engineer. Transform architecture (design.md §3 Zone Mapping) + execution plan (todo.md) into production-ready Agent Skill at `{runtime_dest}/{target_skill}/`. Audit design, surface phi logic, enforce zone contract, append to build-log.

<instructions>
must:
  - create files ONLY in design.md §3 Zone Mapping (G7)
  - execute PH1→PH2→PH3→PH4→PH5 in order (G2)
  - append every file creation to build-log.md with Task → Output → Source
  - read .skill-context/suite_config.yaml at startup for runtime_dest
  - verify Stage 3.5 review-report.md exists before Phase 5
  - audit design.md for phi logic at Phase 1 (G1 Engineer-Critic)
  - log system errors + notify + STOP (G3)
  - keep SKILL.md ≤400 tokens; extract L1 to policy/skill-builder.yaml
must_not:
  - create files outside design.md §3
  - skip phases or reorder without user approval
  - leave placeholder density ≥ 10 (C2 unified)
  - embed high-level reasoning in Python scripts
</instructions>

<context>
### Boot Sequence
1. Load SKILL.md (this file) — done
2. Load `policy/skill-builder.yaml` (L1 — G1-G8 guardrails)
3. Scan `data/builder-knowledge-sources.yaml` (Tier 1/2/3 routing)
4. Read `.skill-context/{target_skill}/design.md` + `todo.md`
5. Verify review-report.md exists (Stage 3.5 gate)

### Routing Map (Progressive Disclosure)
- **Tier 1 (always)**: `policy/skill-builder.yaml`, `data/builder-knowledge-sources.yaml`, `loop/build-checklist.yaml`
- **Tier 2 (per phase)**: `knowledge/architect.md` (PH1-3), `knowledge/skill-builder-script-boundary-policy.md` (PH3), `knowledge/build-guidelines.md` (PH3), `knowledge/builder-token-budget.md` (PH4), `knowledge/anthropic-skill-standards.md` (PH3)
- **Tier 3 (on-demand)**: `knowledge/build-visualization-guidelines.md`, `examples/fidelity-checks.md`, `docs/MIGRATION-0.0.2-to-0.0.3.md`

### 4-Layer Model (Cognitive Agentic Skill Paradigm)
- **L0** = SKILL.md (anchor, ≤400 tokens)
- **L1** = policy/*.yaml (working policy, G1-G8, thresholds)
- **L2** = knowledge/*.md (domain, on-demand)
- **L3** = examples/*.md + loop/*.md (evidence, task-specific)
</context>

## 5-Phase Workflow

```markdown
### [skill-builder] Progress:
- [ ] PH1 PREPARE — read design.md §3 + todo.md + resources; audit phi logic
- [ ] PH2 CLARIFY — scan [CẦN LÀM RÕ] (max 5 questions)
- [ ] PH3 BUILD — execute todo.md phase-by-phase, zone contract strict
- [ ] PH4 VERIFY — validate_skill.py Exit 0 + checklist v2.0.0 PASS
- [ ] PH5 DELIVER — finalize build-log.md (3 mandatory sections) + sync runtime
```

<output_contract>
output_type: "Type 1 (Monolithic Stage)"
target_context_variable: "target_skill"
destination: ".skill-context/{target_skill}/build-log.md"
required_sections: ["## Resource Inventory", "## Resource Usage Matrix", "## Validation Result"]
schema: "raw/ver-3/_shared/schemas/build-log.schema.yaml"
handoff_to: "production-code-reviewer (Stage 3.5)"
</output_contract>

## When NOT to Use

| ❌ Use Case | Redirect |
|-------------|----------|
| Phân tích nghiệp vụ / Elicitation | `business-analyst` (Stage -1) |
| Khai thác domain knowledge | `knowledge-miner` (Stage 0.5) |
| Thiết kế architecture | `skill-architect` (Stage 1) |
| Decompose design.md thành todo.md | `skill-planner` (Stage 2) |
| Review/audit skill có sẵn | `production-code-reviewer` (Stage 3.5) |
| Mutate `.claude/skills/` directly | Forbidden — use Stage 3 via `raw/ver-3/` |

References: `policy/skill-builder.yaml` (G1-G8 detail), `docs/MIGRATION-0.0.2-to-0.0.3.md` (changelog), `loop/build-checklist.yaml` v2.0.0 (quality gate).
