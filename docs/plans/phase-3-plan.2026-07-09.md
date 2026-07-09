# Phase 3 — Agent Foundation Build Plan

**Date**: 2026-07-09
**Status**: Ready for execution
**Source docs**: [phase-3-context](./context-to-work/phase-3/phase-3-context.2026-07-08.md) | [agent-architecture](./context-to-work/phase-3/agent-architecture.md) | [roadmap](../../Temps/spec/roadmaps/03-agent-foundation.md)

---

## Overview

Build **7 mandatory + 1 optional specialized agents** using subagent-forge design pattern. Each agent is a single `.md` file with YAML frontmatter + 8-section system prompt. Process per agent: **design → stage → 4-evaluate → deploy**.

## Build Order

| Priority | Agent | Model | Est. Effort | Dependencies |
|:---------|:------|:-----:|:-----------|:-------------|
| **P1** | pipeline-orchestrator | sonnet | 1 session | None (backbone) |
| **P2a** | design-validator | sonnet | 0.5 session | P1 (runtime) |
| **P2b** | quality-scorer | opus | 0.5 session | P1 (runtime) |
| **P3** | external-code-reviewer | sonnet | 0.5 session | P1 (runtime) |
| **P4a** | ba-pipeline-runner | opus | 0.5 session | P1 (runtime) |
| **P4b** | drift-detector | sonnet | 0.5 session | P1 (runtime) |
| **P5** | user-knowledge-ingestor | opus | 0.5 session | P1 (runtime) |
| **Optional** | branch-orchestrator | opus | 0.5 session | P1 (runtime) |

**Note**: Build dependencies are RUNTIME only — all agent FILES can be built in parallel.

## Agent Design Specs (per roadmap 03-agent-foundation.md)

Each agent file requires:
1. **YAML frontmatter**: name, description, model, justification, tools, permissionMode, skills, hooks (PreToolUse + PostToolUse)
2. **8-section system prompt**: identity, safety-contract, workflow-phases, knowledge-anchors, input-contract, output-contract, examples, failure-modes
3. **Knowledge doc references**: All 7 docs under `.claude/knowledge/agents/` via `<retrieved_docs>` tag
4. **Inline hooks**: `exit 2` blocking patterns per agent role
5. **Output contract**: `<output_contract>` section with concrete artifact paths

### Knowledge Docs (mandatory per agent)
- `.claude/knowledge/agents/configuration.md` — frontmatter schema
- `.claude/knowledge/agents/capability_controls.md` — tool scoping
- `.claude/knowledge/agents/examples.md` — reference patterns
- `.claude/knowledge/agents/forks.md` — fork semantics (orchestrators only)
- `.claude/knowledge/agents/hooks_and_events.md` — hook protocol
- `.claude/knowledge/agents/workflow_patterns.md` — runtime patterns
- `.claude/knowledge/agents/xml_tags_standards.yaml` — XML tag usage

## Verification (AC-1 → AC-8)

| AC | Check | How |
|:---|:------|:----|
| AC-1 | 7 agent files exist in `_staging/` | `test -f` |
| AC-2 | Frontmatter YAML parses + has required fields | python3 yaml parse |
| AC-3 | Each agent references ≥7 knowledge docs | `grep -c` |
| AC-4 | Each agent has `exit 2` blocking hooks | `grep -q "exit 2"` |
| AC-5 | subagent-forge 4-evaluator passes | invoke per agent |
| AC-6 | `<output_contract>` section exists | `grep -q` |
| AC-7 | Skills referenced exist (or WARNING) | python3 dir check |
| AC-8 | No `bypassPermissions` mode | `grep -q` |

## Execution Strategy

For maximum throughput, build agents in **3 parallel waves**:

**Wave 1 (3 agents in parallel)**:
- pipeline-orchestrator (backbone)
- design-validator (schema gate)
- external-code-reviewer (Γ-1 fix)

**Wave 2 (3 agents in parallel)**:
- quality-scorer (META scoring)
- ba-pipeline-runner (BA chain)
- drift-detector (alignment check)

**Wave 3 (1 agent)**:
- user-knowledge-ingestor (NEW)
- branch-orchestrator (optional, can defer)

**Finalization**:
- Run AC-1 → AC-8
- Deploy all agents
- Update workspce_tree.md
- Write summary doc

## Output Paths

| Artifact | Staging | Runtime |
|:---------|:--------|:--------|
| pipeline-orchestrator | `_staging/pipeline-orchestrator.md` | `.claude/agents/pipeline-orchestrator.md` |
| design-validator | `_staging/design-validator.md` | `.claude/agents/design-validator.md` |
| quality-scorer | `_staging/quality-scorer.md` | `.claude/agents/quality-scorer.md` |
| ba-pipeline-runner | `_staging/ba-pipeline-runner.md` | `.claude/agents/ba-pipeline-runner.md` |
| external-code-reviewer | `_staging/external-code-reviewer.md` | `.claude/agents/external-code-reviewer.md` |
| drift-detector | `_staging/drift-detector.md` | `.claude/agents/drift-detector.md` |
| user-knowledge-ingestor | `_staging/user-knowledge-ingestor.md` | `.claude/agents/user-knowledge-ingestor.md` |
| branch-orchestrator (opt) | `_staging/branch-orchestrator.md` | `.claude/agents/branch-orchestrator.md` |
