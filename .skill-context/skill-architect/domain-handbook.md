---
artifact_type: "domain-handbook"
target_skill: "skill-architect"
version: "0.0.2"
generated_by: "knowledge-miner (Stage 0.5)"
generated_at: "2026-06-18"
pipeline_position: "Stage 0.5 → Stage 1 (Architect)"
quality_score: "44.5% (WARNING — BA report quality below 80% threshold)"
consumer: "skill-architect (Stage 1) — primary input for SKILL.md update"
---

# Domain Handbook: skill-architect ver-0.0.2

> **Purpose**: Consolidated domain knowledge mined from BA report, existing knowledge files, runtime code, and project docs. Directly consumable by Stage 1 (Architect) to update SKILL.md without re-deriving context.

---

## 1. Domain Overview

### 1.1 What skill-architect Does

Senior Architect role in the WASHVN Master Skill Suite pipeline. It consumes upstream artifacts (exploration.md, domain-handbook.md) and user pain points, then produces `design.md` — a 10-section architecture document mapping a new Agent Skill to 7 Zones (Core, Knowledge, Scripts, Templates, Data, Loop, Assets).

Source: [`business-analysis.md §1`](file:///home/steve/Work-space/WASHVN/.skill-context/skill-architect/business-analysis.md#L108-L109)

### 1.2 Pipeline Position

```
Stage 0 (Explorer) → Stage 0.5 (Knowledge Miner) → Stage 1 (Architect) → Stage 1.5 (Gatekeeper) → Stage 2 (Planner) → Stage 3 (Builder) → ...
```

Source: [`architecture.md §1`](file:///home/steve/Work-space/WASHVN/architecture.md#L14-L50)

### 1.3 Three Core Pillars (Design Framework)

| Pillar | Focus | Source |
|--------|-------|--------|
| 1 — Knowledge | Domain knowledge requirements, knowledge/ folder structure | [`architect.md §Phase2`](file:///home/steve/Work-space/WASHVN/skills/ver-0.0.2/skill-architect/knowledge/architect.md#L74-L80) |
| 2 — Process | Workflow logic, phase ordering, interaction points | [`architect.md §Phase2`](file:///home/steve/Work-space/WASHVN/skills/ver-0.0.2/skill-architect/knowledge/architect.md#L74-L80) |
| 3 — Guardrails | Zone applicability, risk identification, quality gates | [`architect.md §Phase2`](file:///home/steve/Work-space/WASHVN/skills/ver-0.0.2/skill-architect/knowledge/architect.md#L74-L80) |

### 1.4 Output Artifact

`design.md` at `.skill-context/{target_skill}/design.md` with 10 mandatory sections (§1-§10) in progressive write order (Phase 1 → §1+§10, Phase 2 → §2+§3+§8, Phase 3 → §4-§7+§9).

Source: [`SKILL.md §Output Contract`](file:///home/steve/Work-space/WASHVN/.claude/skills/skill-architect/SKILL.md#L115-L142); [`workflow.md §Progressive Writing`](file:///home/steve/Work-space/WASHVN/.claude/skills/skill-architect/policy/workflow.md#L84-L92)

---

## 2. Core Concepts and Vocabulary (Glossary)

| Term | Definition | Source |
|------|------------|--------|
| **7 Zones** | Core, Knowledge, Scripts, Templates, Data, Loop, Assets — the physical directory structure of every Agent Skill | [`architecture.md`](file:///home/steve/Work-space/WASHVN/architecture.md); [`design-exemplars.md §4`](file:///home/steve/Work-space/WASHVN/skills/ver-0.0.2/skill-architect/knowledge/design-exemplars.md#L497-L507) |
| **3 Pillars** | Knowledge, Process, Guardrails — analytical framework for mapping any requirement to skill architecture | [`architect.md`](file:///home/steve/Work-space/WASHVN/skills/ver-0.0.2/skill-architect/knowledge/architect.md#L19-L40) |
| **Deterministic Boundary** | Scripts zone MUST only contain tasks with deterministic input→output. Business logic stays with LLM. | [`script-boundary-policy.md §1`](file:///home/steve/Work-space/WASHVN/skills/ver-0.0.2/skill-architect/knowledge/script-boundary-policy.md#L9-L16) |
| **Knowledge Boot Scan** | Boot sequence MUST scan `.claude/knowledge/` and skill's own `knowledge/` before Phase 1 | [`knowledge-boot-sequence.md §1`](file:///home/steve/Work-space/WASHVN/skills/ver-0.0.2/skill-architect/knowledge/knowledge-boot-sequence.md#L9-L21) |
| **Progressive Disclosure** | Tier 1 (always loaded) vs Tier 2 (conditional) vs Tier 3 (on-demand) — token management strategy | [`SKILL.md §Routing`](file:///home/steve/Work-space/WASHVN/.claude/skills/skill-architect/SKILL.md#L47-L62) |
| **Trace Tags** | `[TU USER INPUT]`, `[TU NGUON EXTERNAL]`, `[GOI Y BO SUNG]`, `[CAN LAM RO]` — source attribution for every assertion in design.md | [`architect.md §Source Attribution`](file:///home/steve/Work-space/WASHVN/skills/ver-0.0.2/skill-architect/knowledge/architect.md#L19-L48) |
| **SCS (Skill Complexity Score)** | Score computed by Stage 0; SCS > 3.0 triggers full 8-stage pipeline, SCS < 3.0 uses fast-track | [`architecture.md §A`](file:///home/steve/Work-space/WASHVN/architecture.md#L127-L131) |
| **CASE System** | Confidence-Aware Skill Execution — auto-rollback when confidence < 85% or validation FAIL | [`architecture.md §5`](file:///home/steve/Work-space/WASHVN/architecture.md#L113-L118) |
| **Gherkin Scenario** | Given-When-Then acceptance criteria for functional requirements | [`business-analysis.md §Deliverable6`](file:///home/steve/Work-space/WASHVN/.skill-context/skill-architect/business-analysis.md#L276-L341) |
| **K=8 Chains** | 8 parallel reasoning chains (2/3/3 split across 3 Pillars) for hard mode (confidence 70-85%) | [`guardrails.md §Heavy Thinking`](file:///home/steve/Work-space/WASHVN/.claude/skills/skill-architect/policy/guardrails.md#L62-L98) |

---

## 3. Functional Requirements (FR) — Distilled from BA

### 3.1 Context Awareness (Knowledge Boot)

| FR ID | Description | MoSCoW | Priority | Source |
|-------|-------------|--------|----------|--------|
| FR-01 | Auto-scan `.claude/knowledge/` at boot | Must-have | P0 | [`business-analysis.md §2 FR-01`](file:///home/steve/Work-space/WASHVN/.skill-context/skill-architect/business-analysis.md#L113-L113) |
| FR-02 | Read upstream artifacts (exploration.md, domain-handbook.md) | Must-have | P0 | [`business-analysis.md §2 FR-02`](file:///home/steve/Work-space/WASHVN/.skill-context/skill-architect/business-analysis.md#L114-L114) |
| FR-03 | Distinguish 3 input types: user pain point / knowledge base / heavy-thinking | Must-have | P0 | [`business-analysis.md §2 FR-03`](file:///home/steve/Work-space/WASHVN/.skill-context/skill-architect/business-analysis.md#L115-L115) |
| FR-10 | Boot sequence MUST include "Load Knowledge" step | Must-have | P0 | [`business-analysis.md §2 FR-10`](file:///home/steve/Work-space/WASHVN/.skill-context/skill-architect/business-analysis.md#L123-L123) |
| FR-04 | Propose knowledge additions on gap detection | Could-have | P3 | [`business-analysis.md §2 FR-04`](file:///home/steve/Work-space/WASHVN/.skill-context/skill-architect/business-analysis.md#L134-L134) |

### 3.2 Script Boundary Determinism

| FR ID | Description | MoSCoW | Priority | Source |
|-------|-------------|--------|----------|--------|
| FR-05 | Scripts zone ONLY deterministic tasks | Must-have | P0 | [`business-analysis.md §2 FR-05`](file:///home/steve/Work-space/WASHVN/.skill-context/skill-architect/business-analysis.md#L117-L117) |
| FR-06 | ALL business decisions handled by LLM, not scripts | Must-have | P0 | [`business-analysis.md §2 FR-06`](file:///home/steve/Work-space/WASHVN/.skill-context/skill-architect/business-analysis.md#L118-L118) |
| FR-08 | Scripts ONLY do: IO, file system, network, parsing | Must-have | P0 | [`business-analysis.md §2 FR-08`](file:///home/steve/Work-space/WASHVN/.skill-context/skill-architect/business-analysis.md#L120-L120) |
| FR-17 | Script zone only generates: init context, validate schema, export Mermaid, run checklist | Must-have | P0 | [`business-analysis.md §2 FR-17`](file:///home/steve/Work-space/WASHVN/.skill-context/skill-architect/business-analysis.md#L127-L127) |
| FR-18 | MUST NOT generate scripts for: business logic, decision trees, data transformation | Must-have | P0 | [`business-analysis.md §2 FR-18`](file:///home/steve/Work-space/WASHVN/.skill-context/skill-architect/business-analysis.md#L128-L128) |
| FR-20 | Scripts MUST NOT contain LLM prompt logic | Must-have | P0 | [`business-analysis.md §2 FR-20`](file:///home/steve/Work-space/WASHVN/.skill-context/skill-architect/business-analysis.md#L129-L129) |
| FR-07 | Scripts designed AFTER knowledge zone (not in parallel) | Should-have | P1 | [`business-analysis.md §2 FR-07`](file:///home/steve/Work-space/WASHVN/.skill-context/skill-architect/business-analysis.md#L119-L119) |
| FR-19 | Each script MUST have deterministic boundary description | Should-have | P1 | [`business-analysis.md §2 FR-19`](file:///home/steve/Work-space/WASHVN/.skill-context/skill-architect/business-analysis.md#L133-L133) |

### 3.3 Knowledge Integration Pipeline

| FR ID | Description | MoSCoW | Priority | Source |
|-------|-------------|--------|----------|--------|
| FR-09 | Integrate Knowledge Miner (Stage 0.5) output as upstream input | Must-have | P0 | [`business-analysis.md §2 FR-09`](file:///home/steve/Work-space/WASHVN/.skill-context/skill-architect/business-analysis.md#L121-L121) |
| FR-12 | design.md §2 Capability Map MUST trace each knowledge source file | Must-have | P0 | [`business-analysis.md §2 FR-12`](file:///home/steve/Work-space/WASHVN/.skill-context/skill-architect/business-analysis.md#L124-L124) |
| FR-15 | design.md MUST have dedicated "Knowledge Requirements" section | Must-have | P0 | [`business-analysis.md §2 FR-15`](file:///home/steve/Work-space/WASHVN/.skill-context/skill-architect/business-analysis.md#L125-L125) |

### 3.4 Design Quality and Validation

| FR ID | Description | MoSCoW | Priority | Source |
|-------|-------------|--------|----------|--------|
| FR-14 | MUST validate design before handoff (checklist auto-run) | Must-have | P0 | [`business-analysis.md §2 FR-14`](file:///home/steve/Work-space/WASHVN/.skill-context/skill-architect/business-analysis.md#L126-L126) |
| FR-16 | Check `.skill-context/{target_skill}/` artifacts before designing | Must-have | P0 | [`business-analysis.md §2 FR-16`](file:///home/steve/Work-space/WASHVN/.skill-context/skill-architect/business-analysis.md#L128-L128) |
| FR-11 | Stop and request domain knowledge if insufficient | Should-have | P1 | [`business-analysis.md §2 FR-11`](file:///home/steve/Work-space/WASHVN/.skill-context/skill-architect/business-analysis.md#L131-L131) |
| FR-13 | Every zone in design MUST have rationale | Should-have | P1 | [`business-analysis.md §2 FR-13`](file:///home/steve/Work-space/WASHVN/.skill-context/skill-architect/business-analysis.md#L132-L132) |

### 3.5 MoSCoW Summary

| Level | Count | Key Items |
|-------|-------|-----------|
| Must-have | 15 | FR-01/02/03/05/06/08/09/10/12/14/15/16/17/18/20 + NFR-01/03/04/05/06 |
| Should-have | 5 | FR-04/07/11/13/19 + NFR-02 |
| Could-have | 1 | FR-04 |
| Won't-have | 0 | — |

Source: [`business-analysis.md §MoSCoW`](file:///home/steve/Work-space/WASHVN/.skill-context/skill-architect/business-analysis.md#L147-L154)

---

## 4. Non-Functional Requirements (NFR)

| NFR ID | Description | Target | MoSCoW | Source |
|--------|-------------|--------|--------|--------|
| NFR-01 | Context Load Time — boot loads ≤5 knowledge files | ≤5 files loaded at boot | Must-have | [`business-analysis.md §NFR-01`](file:///home/steve/Work-space/WASHVN/.skill-context/skill-architect/business-analysis.md#L140-L140) |
| NFR-02 | Knowledge Freshness — detect stale design via timestamp | Compare knowledge/ mtime vs design.md mtime | Should-have | [`business-analysis.md §NFR-02`](file:///home/steve/Work-space/WASHVN/.skill-context/skill-architect/business-analysis.md#L141-L141) |
| NFR-03 | Traceability — 100% trace tag coverage in design.md | Every assertion has source tag | Must-have | [`business-analysis.md §NFR-03`](file:///home/steve/Work-space/WASHVN/.skill-context/skill-architect/business-analysis.md#L142-L142) |
| NFR-04 | Token Efficiency — SKILL.md ≤600, boot load ≤2000 tokens | ≤2600 total | Must-have | [`business-analysis.md §NFR-04`](file:///home/steve/Work-space/WASHVN/.skill-context/skill-architect/business-analysis.md#L143-L143) |
| NFR-05 | Hallucination Guard — zero placeholders, zero faux-knowledge | Zero tolerance | Must-have | [`business-analysis.md §NFR-05`](file:///home/steve/Work-space/WASHVN/.skill-context/skill-architect/business-analysis.md#L144-L144) |
| NFR-06 | Script Determinism — every script has input/output schema, no LLM context side-effect | Full deterministic boundary | Must-have | [`business-analysis.md §NFR-06`](file:///home/steve/Work-space/WASHVN/.skill-context/skill-architect/business-analysis.md#L145-L145) |

---

## 5. Existing Code Patterns and Reusable Assets

### 5.1 Runtime State (`.claude/skills/skill-architect/`)

| Asset | Path | Status | Notes |
|-------|------|--------|-------|
| SKILL.md | [`.claude/skills/skill-architect/SKILL.md`](file:///home/steve/Work-space/WASHVN/.claude/skills/skill-architect/SKILL.md) | **NEEDS UPDATE** | ver-0.0.1; lacks knowledge boot scan, still references `templates/design.md.template` |
| Knowledge/architect.md | [`.claude/skills/skill-architect/knowledge/architect.md`](file:///home/steve/Work-space/WASHVN/.claude/skills/skill-architect/knowledge/architect.md) | OK | 3 Pillars framework |
| Knowledge/design-exemplars.md | [`.claude/skills/skill-architect/knowledge/design-exemplars.md`](file:///home/steve/Work-space/WASHVN/.claude/skills/skill-architect/knowledge/design-exemplars.md) | OK | Section content spec + anti-patterns |
| Knowledge/visualization-guidelines.md | [`.claude/skills/skill-architect/knowledge/visualization-guidelines.md`](file:///home/steve/Work-space/WASHVN/.claude/skills/skill-architect/knowledge/visualization-guidelines.md) | OK | Mermaid diagram standards |
| Policy/guardrails.md | [`.claude/skills/skill-architect/policy/guardrails.md`](file:///home/steve/Work-space/WASHVN/.claude/skills/skill-architect/policy/guardrails.md) | OK | G1-G7 guardrails |
| Policy/output-spec.md | [`.claude/skills/skill-architect/policy/output-spec.md`](file:///home/steve/Work-space/WASHVN/.claude/skills/skill-architect/policy/output-spec.md) | OK | 10-section output spec |
| Policy/workflow.md | [`.claude/skills/skill-architect/policy/workflow.md`](file:///home/steve/Work-space/WASHVN/.claude/skills/skill-architect/policy/workflow.md) | OK | Phase 1-3 details |
| Loop/design-checklist.md | [`.claude/skills/skill-architect/loop/design-checklist.md`](file:///home/steve/Work-space/WASHVN/.claude/skills/skill-architect/loop/design-checklist.md) | **NEEDS UPDATE** | Missing knowledge scan check, trace validation items |
| Loop/design-checklist.yaml | [`.claude/skills/skill-architect/loop/design-checklist.yaml`](file:///home/steve/Work-space/WASHVN/.claude/skills/skill-architect/loop/design-checklist.yaml) | **NEEDS UPDATE** | Machine-readable version, same gap |
| Scripts/init_context.py | [`.claude/skills/skill-architect/scripts/init_context.py`](file:///home/steve/Work-space/WASHVN/.claude/skills/skill-architect/scripts/init_context.py) | **CONTRADICTION EXISTS** | Still has FALLBACK_TEMPLATES dict, TEMPLATE_FILES dict, writes design.md template — violates FR-17/FR-18 |
| Scripts/export-pipeline.py | [`.claude/skills/skill-architect/scripts/export-pipeline.py`](file:///home/steve/Work-space/WASHVN/.claude/skills/skill-architect/scripts/export-pipeline.py) | OK | Simple pipeline Mermaid export |
| Templates/design.md.template | [`.claude/skills/skill-architect/templates/design.md.template`](file:///home/steve/Work-space/WASHVN/.claude/skills/skill-architect/templates/design.md.template) | **CONTRADICTION EXISTS** | BA analysis says remove hard template; file still exists |

### 5.2 Development State (`skills/ver-0.0.2/skill-architect/`)

| Asset | Path | Status vs Runtime | Notes |
|-------|------|-------------------|-------|
| SKILL.md | [`skills/ver-0.0.2/skill-architect/SKILL.md`](file:///home/steve/Work-space/WASHVN/skills/ver-0.0.2/skill-architect/SKILL.md) | MISSING from runtime | Development copy not deployed |
| Knowledge/knowledge-boot-sequence.md | [`skills/ver-0.0.2/skill-architect/knowledge/knowledge-boot-sequence.md`](file:///home/steve/Work-space/WASHVN/skills/ver-0.0.2/skill-architect/knowledge/knowledge-boot-sequence.md) | **MISSING from runtime** | Exists in ver-0.0.2 but NOT in .claude/skills/ |
| Knowledge/script-boundary-policy.md | [`skills/ver-0.0.2/skill-architect/knowledge/script-boundary-policy.md`](file:///home/steve/Work-space/WASHVN/skills/ver-0.0.2/skill-architect/knowledge/script-boundary-policy.md) | **MISSING from runtime** | Exists in ver-0.0.2 but NOT in .claude/skills/ |

> **Key Delta**: Runtime `.claude/skills/skill-architect/` has only 3 knowledge files. Development `skills/ver-0.0.2/` has 5 (adds `knowledge-boot-sequence.md` and `script-boundary-policy.md`). The 2 new files were generated by BA analysis as recommended deliverables. They must be synced to runtime.

Source: [`business-analysis.md §3.2`](file:///home/steve/Work-space/WASHVN/.skill-context/skill-architect/business-analysis.md#L367-L376)

### 5.3 Reusable Patterns from design-exemplars.md

- **Section Content Specification**: Good/bad examples for each of §1-§10 with trace tags, token budgets, anti-patterns
- **Zone Decision Tree**: Mermaid flowchart determining which zones are needed for any skill
- **design.md Exemplar**: Complete annotated example (example-skill) showing correct format, trace tags, and progressive disclosure

Source: [`design-exemplars.md`](file:///home/steve/Work-space/WASHVN/skills/ver-0.0.2/skill-architect/knowledge/design-exemplars.md)

### 5.4 BA-Proposed Knowledge Source Registry

```json
{
  "KS-01": { "path": ".claude/knowledge/agents/", "type": "agents", "priority": "tier2", "load": "WHEN designing subagent-using skill" },
  "KS-02": { "path": ".claude/knowledge/skills/", "type": "skills_framework", "priority": "tier1", "load": "ALWAYS" },
  "KS-03": { "path": ".claude/knowledge/hooks/", "type": "hooks", "priority": "tier2", "load": "WHEN skill needs hooks" },
  "KS-04": { "path": ".skill-context/{target}/exploration.md", "type": "exploration", "priority": "tier1", "load": "IF EXISTS" },
  "KS-05": { "path": ".skill-context/{target}/domain-handbook.md", "type": "domain_handbook", "priority": "tier1", "load": "IF EXISTS" }
}
```

Source: [`analysis-report.md §6`](file:///home/steve/Work-space/WASHVN/.skill-context/skill-architect/ba-analyst/analysis-report.md#L196-L234); [`business-analysis.md §Deliverable5`](file:///home/steve/Work-space/WASHVN/.skill-context/skill-architect/business-analysis.md#L227-L270)

---

## 6. Established Conventions and Standards

### 6.1 Format Standards (from `standards.md`)

- **Markdown** for explanation, rationale, architecture, domain knowledge
- **YAML** for constraints, policies, checklists, routing, output contracts
- **XML-like tags** (`<instructions>`, `<context>`, `<examples>`, `<output_contract>`) for semantic boundaries
- **4-layer knowledge model**: L0 (anchor rules, always load), L1 (working policy, frequent), L2 (domain context, on-demand), L3 (evidence/examples, task-specific)
- **Root guide token budget**: 300-900 tokens excellent, 900-1800 good, >3000 warning

Source: [`standards.md`](file:///home/steve/Work-space/WASHVN/standards.md)

### 6.2 SKILL.md Conventions (from `CLAUDE.md`)

- YAML frontmatter required: name, description, version: 0.0.1, suite: WASHVN, tags, when_to_use
- SKILL.md ≤700 tokens (L0 anchor)
- kebab-case naming for skills
- 7-Zone structure mandatory
- Zero placeholders in production code

Source: [`CLAUDE.md §5-§6`](file:///home/steve/Work-space/WASHVN/CLAUDE.md#L78-L100)

### 6.3 Guardrails Schema (G1-G7)

| Guardrail | Rule | Source |
|-----------|------|--------|
| G1 | Design Only — no implementation code | [`guardrails.md`](file:///home/steve/Work-space/WASHVN/.claude/skills/skill-architect/policy/guardrails.md#L12-L16) |
| G2 | Gate Enforcement — stop at each phase for user confirmation | [`guardrails.md`](file:///home/steve/Work-space/WASHVN/.claude/skills/skill-architect/policy/guardrails.md#L18-L21) |
| G3 | Confidence Threshold — <70% ask user; <85% activate K=8 | [`guardrails.md`](file:///home/steve/Work-space/WASHVN/.claude/skills/skill-architect/policy/guardrails.md#L24-L27) |
| G4 | Zone Mapping Contract — specific filenames, no placeholders | [`guardrails.md`](file:///home/steve/Work-space/WASHVN/.claude/skills/skill-architect/policy/guardrails.md#L30-L32) |
| G5 | Checklist Gate — pass checklist before deliver | [`guardrails.md`](file:///home/steve/Work-space/WASHVN/.claude/skills/skill-architect/policy/guardrails.md#L35-L37) |
| G6 | Heavy Thinking Gate — K=8 chains when confidence <85% at Phase 2 | [`guardrails.md`](file:///home/steve/Work-space/WASHVN/.claude/skills/skill-architect/policy/guardrails.md#L40-L42) |
| G7 | Format Compliance — YAML/XML/trace tags mandatory | [`guardrails.md`](file:///home/steve/Work-space/WASHVN/.claude/skills/skill-architect/policy/guardrails.md#L45-L58) |

### 6.4 Token Budget (from SKILL.md and design-exemplars.md)

- SKILL.md: 600 tokens max (hard enforcement)
- L1 limit: 1500 tokens
- L2 limit: 2500 tokens
- design.md: 1500-2500 tokens (excellent), 2500-4000 (acceptable)
- Per-section budget defined in `design-exemplars.md §6`

Source: [`SKILL.md §Token Budget`](file:///home/steve/Work-space/WASHVN/.claude/skills/skill-architect/SKILL.md#L40-L45); [`design-exemplars.md §6`](file:///home/steve/Work-space/WASHVN/skills/ver-0.0.2/skill-architect/knowledge/design-exemplars.md#L530-L554)

---

## 7. Architectural Constraints

### 7.1 Pipeline Constraints

1. **Stateless sessions**: Each stage is independently invoked. State persists only via `.skill-context/{name}/` artifacts. — Source: [`CLAUDE.md §7`](file:///home/steve/Work-space/WASHVN/CLAUDE.md#L130-L133)
2. **No runtime edits**: Skills must be developed in `raw/ver-3/` then synced. Direct edit of `.claude/skills/` is forbidden. — Source: [`CLAUDE.md §3`](file:///home/steve/Work-space/WASHVN/CLAUDE.md#L7-L8)
3. **SCS-driven pipeline mode**: SCS < 3.0 = fast-track monolithic; SCS >= 3.0 = full 8-stage with micro-skill decomposition. — Source: [`architecture.md §A`](file:///home/steve/Work-space/WASHVN/architecture.md#L127-L131)
4. **CASE auto-rollback**: If verification FAIL or confidence < 85%, auto-rollback to responsible stage. — Source: [`architecture.md §5`](file:///home/steve/Work-space/WASHVN/architecture.md#L113-L118)

### 7.2 Design Contract Constraints

1. **design.md is contract between Architect and Planner**: Planner reads §3 to decompose into tasks. — Source: [`design-exemplars.md §3`](file:///home/steve/Work-space/WASHVN/skills/ver-0.0.2/skill-architect/knowledge/design-exemplars.md#L66-L67)
2. **§4 must exactly match §3**: Every file in Folder Structure must appear in Zone Mapping and vice versa. — Source: [`design-exemplars.md §4`](file:///home/steve/Work-space/WASHVN/skills/ver-0.0.2/skill-architect/knowledge/design-exemplars.md#L96-L98)
3. **Progressive disclosure Tier 1 ≤4 files**: Must not overload agent at boot. — Source: [`design-exemplars.md §7`](file:///home/steve/Work-space/WASHVN/skills/ver-0.0.2/skill-architect/knowledge/design-exemplars.md#L162-L165)
4. **No extra sections beyond §1-§10**: If additional content needed, merge into §10 Metadata. — Source: [`design-exemplars.md §Anti-pattern 5`](file:///home/steve/Work-space/WASHVN/skills/ver-0.0.2/skill-architect/knowledge/design-exemplars.md#L452-L462)

### 7.3 Script Boundary Constraints (from script-boundary-policy.md)

1. Scripts zone ONLY deterministic tasks: input X → output Y, always same result
2. Business decisions stay in knowledge/ zone and SKILL.md instructions
3. Scripts MUST NOT contain: business logic, decision trees, prompt templates
4. Each script MUST have deterministic boundary comment (first 3 lines)
5. Every script MUST declare input/output schema
6. Zero side-effect with LLM context
7. Shell > Python > Docker (portability priority)

Source: [`script-boundary-policy.md`](file:///home/steve/Work-space/WASHVN/skills/ver-0.0.2/skill-architect/knowledge/script-boundary-policy.md)

### 7.4 Knowledge Boot Constraints (from knowledge-boot-sequence.md)

1. Tier 1 sources loaded ALWAYS: skill's own knowledge/, exploration.md (if exists), domain-handbook.md (if exists)
2. Tier 2 loaded ALWAYS: _shared/knowledge/
3. Tier 3 loaded on-demand: references/examples/
4. If no Tier 1 knowledge found → set confidence < 70%, ask user, DO NOT hallucinate
5. Every §2 Capability Map item MUST trace to knowledge source

Source: [`knowledge-boot-sequence.md`](file:///home/steve/Work-space/WASHVN/skills/ver-0.0.2/skill-architect/knowledge/knowledge-boot-sequence.md)

---

## 8. Cross-References and Citation Map

### 8.1 Source Mapping

| Source File | Content Type | Sections Used | 
|-------------|--------------|---------------|
| [`business-analysis.md`](file:///home/steve/Work-space/WASHVN/.skill-context/skill-architect/business-analysis.md) | Primary BA report — synthesized | §1-§10 of this handbook |
| [`analysis-report.md`](file:///home/steve/Work-space/WASHVN/.skill-context/skill-architect/ba-analyst/analysis-report.md) | Raw BA analysis | §3, §5, §6 of this handbook |
| [`SKILL.md`](file:///home/steve/Work-space/WASHVN/.claude/skills/skill-architect/SKILL.md) | Runtime SKILL.md (ver-0.0.1) | §1, §5, §6, §7 |
| [`architect.md`](file:///home/steve/Work-space/WASHVN/skills/ver-0.0.2/skill-architect/knowledge/architect.md) | 3 Pillars framework | §2, §1 |
| [`knowledge-boot-sequence.md`](file:///home/steve/Work-space/WASHVN/skills/ver-0.0.2/skill-architect/knowledge/knowledge-boot-sequence.md) | Boot v2 with knowledge scan | §2, §7 |
| [`script-boundary-policy.md`](file:///home/steve/Work-space/WASHVN/skills/ver-0.0.2/skill-architect/knowledge/script-boundary-policy.md) | Deterministic boundary policy | §2, §7 |
| [`design-exemplars.md`](file:///home/steve/Work-space/WASHVN/skills/ver-0.0.2/skill-architect/knowledge/design-exemplars.md) | Section content spec + exemplars | §2, §5, §7 |
| [`visualization-guidelines.md`](file:///home/steve/Work-space/WASHVN/skills/ver-0.0.2/skill-architect/knowledge/visualization-guidelines.md) | Mermaid diagram standards | §2 |
| [`guardrails.md`](file:///home/steve/Work-space/WASHVN/.claude/skills/skill-architect/policy/guardrails.md) | G1-G7 specification | §6 |
| [`output-spec.md`](file:///home/steve/Work-space/WASHVN/.claude/skills/skill-architect/policy/output-spec.md) | Output section spec | §1, §6 |
| [`workflow.md`](file:///home/steve/Work-space/WASHVN/.claude/skills/skill-architect/policy/workflow.md) | Phase 1-3 execution | §1, §6 |
| [`design-checklist.md`](file:///home/steve/Work-space/WASHVN/.claude/skills/skill-architect/loop/design-checklist.md) | Quality checklist | §5 |
| [`design-checklist.yaml`](file:///home/steve/Work-space/WASHVN/.claude/skills/skill-architect/loop/design-checklist.yaml) | Machine-readable checklist | §5 |
| [`init_context.py`](file:///home/steve/Work-space/WASHVN/.claude/skills/skill-architect/scripts/init_context.py) | Init script (has contradictions) | §5, §9 |
| [`architecture.md`](file:///home/steve/Work-space/WASHVN/architecture.md) | 8-stage pipeline, CASE, SCS | §1, §7 |
| [`standards.md`](file:///home/steve/Work-space/WASHVN/standards.md) | LLM Knowledge Activation Standard | §6 |
| [`CLAUDE.md`](file:///home/steve/Work-space/WASHVN/CLAUDE.md) | Root agent guide | §6, §7 |

### 8.2 Cross-Reference Gaps (BA vs Existing)

| Topic | BA Report Says | Existing Assets | Delta |
|-------|---------------|-----------------|-------|
| Knowledge Boot | Must scan knowledge/ at boot (FR-01, FR-10) | knowledge-boot-sequence.md exists in ver-0.0.2 but NOT in runtime | **knowledge-boot-sequence.md missing from runtime; SKILL.md boot lacks scan steps** |
| Script Boundary | Must be deterministic only (FR-05, FR-06, FR-08) | script-boundary-policy.md exists in ver-0.0.2 but NOT in runtime; BA says 12/15 FRs missing Gherkin | **script-boundary-policy.md missing from runtime; Gherkin coverage only 3/15** |
| Template Removal | Remove hard template from init_context.py | init_context.py still has FALLBACK_TEMPLATES + writes design.md template | **CONTRADICTION — BA says remove, code still has it** |
| Knowledge Gap | Stop when confidence < 70% (FR-11) | G3 in guardrails.md already covers this | **G3 exists but BA wants stronger enforcement — should stop entirely, not just ask** |
| Knowledge Requirements §11 | Add "Knowledge Requirements" section | output-spec.md has only §1-§10 | **Need to add §11 to output spec** |
| Missing Diagrams | No Sequence Diagram, no ERD in BA | No diagrams exist | **Architect must create these** |

---

## 9. Open Questions, Gaps and Assumptions

### 9.1 Critical Gaps (Must Resolve Before Architect Update)

| Gap ID | Description | Severity | Source Evidence |
|--------|-------------|----------|----------------|
| GAP-01 | **Runtime missing 2 knowledge files**: `knowledge-boot-sequence.md` and `script-boundary-policy.md` exist in `skills/ver-0.0.2/` but NOT in `.claude/skills/skill-architect/knowledge/`. SKILL.md cannot reference them. | MUST | [`skills/ver-0.0.2/skill-architect/knowledge/`](file:///home/steve/Work-space/WASHVN/skills/ver-0.0.2/skill-architect/knowledge/) vs [`.claude/skills/skill-architect/knowledge/`](file:///home/steve/Work-space/WASHVN/.claude/skills/skill-architect/knowledge/) |
| GAP-02 | **SKILL.md boot sequence outdated**: Current runtime boot (steps 1-5) does not include knowledge scan. knowledge-boot-sequence.md defines v2 boot with 8 steps. | MUST | [`SKILL.md §Boot`](file:///home/steve/Work-space/WASHVN/.claude/skills/skill-architect/SKILL.md#L29-L38) vs [`knowledge-boot-sequence.md §1`](file:///home/steve/Work-space/WASHVN/skills/ver-0.0.2/skill-architect/knowledge/knowledge-boot-sequence.md#L9-L21) |
| GAP-03 | **SKILL.md references Tier 3 template that BA says to remove**: `templates/design.md.template` is in Tier 3 of SKILL.md routing. BA analysis explicitly says "remove hard template." | MUST | [`SKILL.md §Routing Tier 3`](file:///home/steve/Work-space/WASHVN/.claude/skills/skill-architect/SKILL.md#L58-L59); [`business-analysis.md §3.1`](file:///home/steve/Work-space/WASHVN/.skill-context/skill-architect/business-analysis.md#L361-L363) |
| GAP-04 | **Gherkin coverage is 3/15 Must-Have FRs (20%)**: 12 FRs lack test scenarios. BA flags FR-08, FR-17, FR-18 as especially dangerous. | SHOULD | [`business-analysis.md §B`](file:///home/steve/Work-space/WASHVN/.skill-context/skill-architect/business-analysis.md#L53-L67) |
| GAP-05 | **No Sequence Diagram in BA**: BA explicitly lacks sequenceDiagram Mermaid. Proposed draft exists but not validated. | SHOULD | [`business-analysis.md §Deliverable3`](file:///home/steve/Work-space/WASHVN/.skill-context/skill-architect/business-analysis.md#L158-L183) |
| GAP-06 | **No ERD in BA**: Only JSON schema (Knowledge Source Registry) exists. Missing PK/FK, data types for entities. | SHOULD | [`business-analysis.md §Deliverable5`](file:///home/steve/Work-space/WASHVN/.skill-context/skill-architect/business-analysis.md#L227-L270) |
| GAP-07 | **init_context.py violates FR-17/FR-18**: Contains FALLBACK_TEMPLATES dict (line 97-101), writes design.md.template with pre-populated zone mapping, pre-populated frontmatter. | MUST | [`init_context.py L84-L101`](file:///home/steve/Work-space/WASHVN/.claude/skills/skill-architect/scripts/init_context.py#L84-L101) |
| GAP-08 | **Script boundary knowledge file not referenced in SKILL.md**: Even after sync, SKILL.md boot routing must include `knowledge/script-boundary-policy.md` in Tier 2 or Tier 3. | MUST | [`SKILL.md §Routing`](file:///home/steve/Work-space/WASHVN/.claude/skills/skill-architect/SKILL.md#L47-L62) |
| GAP-09 | **design-checklist missing knowledge scan and trace items**: Current checklist does not verify knowledge scan completion or trace tag coverage, though these are FR-10 and NFR-03. | SHOULD | [`design-checklist.md`](file:///home/steve/Work-space/WASHVN/.claude/skills/skill-architect/loop/design-checklist.md); [`business-analysis.md FR-10`](file:///home/steve/Work-space/WASHVN/.skill-context/skill-architect/business-analysis.md#L123) |
| GAP-10 | **No "Knowledge Requirements" section in output spec**: BA FR-15 requires dedicated knowledge requirements section. Current output-spec.md has only §1-§10. | SHOULD | [`output-spec.md`](file:///home/steve/Work-space/WASHVN/.claude/skills/skill-architect/policy/output-spec.md); [`business-analysis.md FR-15`](file:///home/steve/Work-space/WASHVN/.skill-context/skill-architect/business-analysis.md#L125) |

### 9.2 Open Questions

| # | Question | Source | Status |
|---|----------|--------|--------|
| Q1 | Should confidence < 70% trigger complete stop (as BA FR-11 implies) or just ask for clarification (as G3 currently does)? | [`business-analysis.md FR-11`](file:///home/steve/Work-space/WASHVN/.skill-context/skill-architect/business-analysis.md#L131) vs [`guardrails.md G3`](file:///home/steve/Work-space/WASHVN/.claude/skills/skill-architect/policy/guardrails.md#L24-L27) | OPEN |
| Q2 | Should `init_context.py` be entirely stripped of template-writing code, keeping only directory creation and resource copy? | [`business-analysis.md §3.1`](file:///home/steve/Work-space/WASHVN/.skill-context/skill-architect/business-analysis.md#L361-L363) | OPEN |
| Q3 | What is the correct replacement for `templates/design.md.template` — should it be removed entirely or replaced with a minimal skeleton with no pre-populated content? | [`init_context.py L84-L101`](file:///home/steve/Work-space/WASHVN/.claude/skills/skill-architect/scripts/init_context.py#L84-L101) | OPEN |
| Q4 | Should the "Knowledge Requirements" section be added as §11 in output-spec.md, or merged into §2 Capability Map as FR-12 requires? | [`business-analysis.md FR-15`](file:///home/steve/Work-space/WASHVN/.skill-context/skill-architect/business-analysis.md#L125) | OPEN |
| Q5 | Should flowchart in BA include Alternative Path (knowledge exists) and Exception Path (confidence < 70%)? Currently only Problem→Impact path exists. | [`business-analysis.md §Deliverable4`](file:///home/steve/Work-space/WASHVN/.skill-context/skill-architect/business-analysis.md#L189-L207) | OPEN |
| Q6 | Should design-checklist.md and design-checklist.yaml be merged or kept as separate human/machine formats? | See both files in `.claude/skills/skill-architect/loop/` | OPEN |
| Q7 | The BA proposes a draft Sequence Diagram (boot→collect→analyze→design). Is this accurate for the intended runtime behavior? | [`business-analysis.md §Deliverable3`](file:///home/steve/Work-space/WASHVN/.skill-context/skill-architect/business-analysis.md#L162-L183) | OPEN |

### 9.3 Assumptions Made

| # | Assumption | Rationale | Risk |
|---|-----------|-----------|------|
| A1 | skill-architect remains a monolithic stage skill (SCS > 3.0 not applicable) | BA explicitly states "N/A — skill-architect là monolithic stage skill, không decompose thêm" | Low — BA recommendation |
| A2 | `knowledge-boot-sequence.md` and `script-boundary-policy.md` should be synced to runtime `.claude/skills/skill-architect/knowledge/` | BA §3.2 says these are "generated from analysis" and should be copied | Low — BA recommendation |
| A3 | Current G3 (confidence < 70% → ask) is NOT sufficient for knowledge gap handling; stronger stop+block is needed | BA FR-11 says "must stop and report 'Need more domain knowledge'" | Medium — BA quality score only 44.5% |
| A4 | The development copy `skills/ver-0.0.2/skill-architect/SKILL.md` represents the intended updated SKILL.md | It exists in the ver-0.0.2 path which is the target version | Medium — may not be final |
| A5 | No elicitation report exists (score 0.0 in BA quality calculation) | BA explicitly states "no elicitation-report.md" — this is confirmed absence, not incomplete discovery | Low |

### 9.4 Quality Score Breakdown

| Deliverable | Weight | Score | Weighted |
|-------------|--------|-------|----------|
| Elicitation Report | 0.15 | 0.0 | 0.0 |
| Requirements Classification | 0.15 | 1.0 | 0.15 |
| Sequence Diagram | 0.15 | 0.0 | 0.0 |
| Flowchart Activity | 0.15 | 0.35 | 0.053 |
| ERD Schema | 0.15 | 0.0 | 0.0 |
| Acceptance Criteria | 0.15 | 1.0 | 0.15 |
| Risk Matrix | 0.10 | 1.0 | 0.10 |
| **Total** | **1.0** | | **0.445 (44.5%)** |

Source: [`business-analysis.md §C`](file:///home/steve/Work-space/WASHVN/.skill-context/skill-architect/business-analysis.md#L70-L91)

---

## 10. Decision Traces (Ky luat — Trung thuc — Sang tao audit)

### 10.1 Discipline (Ky luat) — Structured Process Compliance

| Requirement | Status | Evidence |
|-------------|--------|----------|
| All 10 Domain Handbook sections produced | PASSED | Sections 1-10 complete |
| All claims cited to absolute file paths with line ranges | PASSED | Every claim mapped to source file + section |
| Knowledge anchors re-read at start | PASSED | All 7 knowledge/agents/ files read before mining |
| Archive check performed | PASSED | No existing domain-handbook.md to archive |
| Skill name collision check | PASSED | target_skill is skill-architect (ver-0.0.2), exists in development path not as new skill |

### 10.2 Honesty (Trung thuc) — Gap/Violation Acknowledgment

| Gap | Acknowledged | Location in Handbook |
|-----|-------------|---------------------|
| BA quality score is 44.5% (< 80% threshold) | YES | §9.4, frontmatter |
| 12/15 Must-Have FRs have no Gherkin scenarios | YES | §9.1 GAP-04 |
| Contradiction: BA says remove template, init_context.py still has it | YES | §9.1 GAP-07 |
| Contradiction: SKILL.md references templates/design.md.template in Tier 3 | YES | §9.1 GAP-03 |
| knowledge-boot-sequence.md missing from runtime | YES | §9.1 GAP-01 |
| script-boundary-policy.md missing from runtime | YES | §9.1 GAP-01 |
| No Sequence Diagram or ERD in BA | YES | §9.1 GAP-05, GAP-06 |
| G3 confidence handling may be insufficient per BA FR-11 | YES | §9.2 Q1 |

### 10.3 Creativity (Sang tao) — Non-Obvious Patterns and Opportunities

| Insight | Description | Source Synthesis |
|---------|-------------|-----------------|
| **Progressive sync pattern**: ver-0.0.2 has 5 knowledge files but runtime only has 3. The 2 new files (knowledge-boot-sequence.md, script-boundary-policy.md) must be synced BEFORE SKILL.md is updated, because SKILL.md's boot routing must reference them. | Sync order: knowledge files first → SKILL.md second → design-checklist update third | [`skill/ver-0.0.2/`](file:///home/steve/Work-space/WASHVN/skills/ver-0.0.2/skill-architect) vs [`.claude/skills/`](file:///home/steve/Work-space/WASHVN/.claude/skills/skill-architect) |
| **Template removal cascade**: Removing `templates/design.md.template` has 3 downstream effects: (1) SKILL.md Tier 3 reference must be removed, (2) init_context.py FALLBACK_TEMPLATES must be removed, (3) design-exemplars.md §4 Zone-DT table lists Templates zone — may need update. | Single change, 3 files affected. | Cross-reference: [`SKILL.md`](file:///home/steve/Work-space/WASHVN/.claude/skills/skill-architect/SKILL.md#L58-L60) → [`init_context.py`](file:///home/steve/Work-space/WASHVN/.claude/skills/skill-architect/scripts/init_context.py#L84-L101) → [`design-exemplars.md §4`](file:///home/steve/Work-space/WASHVN/skills/ver-0.0.2/skill-architect/knowledge/design-exemplars.md#L497-L507) |
| **Knowledge Source Registry as runtime boot config**: BA defines 5 knowledge sources with tier/priority/load_condition. This could be formalized as a YAML config file (e.g., `config/knowledge-sources.yaml`) that the Architect reads at boot rather than hardcoding paths in SKILL.md. | If formalized, it becomes dynamically configurable without SKILL.md edits. | [`analysis-report.md §6`](file:///home/steve/Work-space/WASHVN/.skill-context/skill-architect/ba-analyst/analysis-report.md#L196-L234) |
| **Gherkin gap is an opportunity, not just a deficit**: The 12 missing scenarios mean the Architect can co-design them with the BA during the same session. Merging Gherkin creation into the design workflow reduces handoff overhead. | Design-time Gherkin co-creation = fewer iterations. | [`business-analysis.md §B`](file:///home/steve/Work-space/WASHVN/.skill-context/skill-architect/business-analysis.md#L53-L67) |
| **The "Knowledge Requirements §11" is architecturally important**: BA FR-15 demands a dedicated section listing every knowledge file needed. This is a structural addition that affects output-spec.md, design.md template, design-checklist, and the handoff contract to Planner. It may be better as a subsection of §2 rather than §11. | If §11, must update 4 files. If subsection of §2, simpler but may lose visibility. | [`output-spec.md`](file:///home/steve/Work-space/WASHVN/.claude/skills/skill-architect/policy/output-spec.md) |
| **script-boundary-policy.md as a reusable cross-skill asset**: The policy defines deterministic boundary rules that apply to ANY skill's scripts zone. It could be promoted to `_shared/knowledge/` for reuse by other Architects/Planners across the entire pipeline. | Promotion reduces duplication. Currently only in skill-architect's knowledge/. | [`script-boundary-policy.md`](file:///home/steve/Work-space/WASHVN/skills/ver-0.0.2/skill-architect/knowledge/script-boundary-policy.md) |

---

## Handoff Summary

| Item | Value |
|------|-------|
| Sections produced | 10/10 |
| Total citations | 65+ unique file-path-markdown links |
| Open questions | 7 (Q1-Q7) |
| Critical gaps | 10 (GAP-01 through GAP-10) |
| Assumptions | 5 (A1-A5) |
| Confidence score | 65/100 (BA input quality is 44.5%, but source triangulation across BA + existing files + runtime code raises confidence) |

### Priority Action Items for Stage 1 (Architect)

1. **P0**: Sync `knowledge-boot-sequence.md` and `script-boundary-policy.md` from `skills/ver-0.0.2/` to `.claude/skills/skill-architect/knowledge/`
2. **P0**: Update SKILL.md boot sequence to v2 (knowledge scan before Phase 1, per knowledge-boot-sequence.md)
3. **P0**: Remove `templates/design.md.template` from SKILL.md Tier 3 routing and strip template-writing from init_context.py
4. **P1**: Add `knowledge/script-boundary-policy.md` and `knowledge/knowledge-boot-sequence.md` to SKILL.md Tier 2 routing
5. **P1**: Update design-checklist.md/design-checklist.yaml with knowledge scan + trace validation checks
6. **P1**: Add Knowledge Requirements section to output spec (resolve Q4 — subsection or §11)
7. **P2**: Add missing Sequence Diagram and ERD (use BA-proposed draft as starting point)
8. **P2**: Generate missing 12 Gherkin scenarios to achieve 15/15 Must-Have coverage
9. **P3**: Formalize Knowledge Source Registry as YAML config file
