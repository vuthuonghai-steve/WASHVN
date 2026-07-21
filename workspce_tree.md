# WASHVN Workspace Directory Tree Mapping

> **Updated:** 2026-07-16 | **Audit:** Full structural sync from actual filesystem.

A comprehensive routing map and layout guide for the WASHVN Master Skill Suite repository.
All paths relative to `/home/stveve/Documents/workspace/build-workflow/WASHVN/`.

## Layout Overview

```
WASHVN/
├── AGENTS.md                          # L0 Root Agent Guide & Behavior Sync
├── CLAUDE.md                          # Claude Code Active Rules (v3.0.0)
├── architecture.md                    # Master Skill Suite 5-Layer / 8-Stage Pipeline Architecture
├── standards.md                       # LLM Knowledge Activation Standards
├── workspce_tree.md                   # Workspace Tree Map (This File)
│
├── skills-registry.json               # Global skill registry (all versions)
├── llms.txt                           # LLM knowledge index
│
├── 7-llm-principles-mapping-analysis.md
├── synthesis-llm-principles.md
├── system-prompt-workflow.md
│
├── .gitignore
│
├── .claude/                           # [RUNTIME] Claude Code — primary agent
│   ├── settings.json                  # Custom settings & permission bounds
│   ├── settings.local.json            # Local overrides
│   ├── agents/                        # Agent templates (pipeline orchestrators)
│   │   ├── _staging/                  # Quarantine/staging for generated agents
│   │   ├── _archive/                  # Historic agent versions
│   │   │   ├── 2026-07-09_phase-3-deploy/
│   │   │   └── 2026-07-11_remove-ba-subagents/
│   │   ├── subagent-forge.md
│   │   ├── pipeline-orchestrator.md
│   │   ├── design-validator.md
│   │   ├── quality-scorer.md
│   │   ├── ba-pipeline-runner.md
│   │   ├── external-code-reviewer.md
│   │   ├── drift-detector.md
│   │   ├── user-knowledge-ingestor.md
│   │   └── branch-orchestrator.md
│   ├── skills/                        # Runtime skills (synced from skills/ver-3/)
│   │   ├── _shared/
│   │   ├── .omc/
│   │   ├── ba-analyst/
│   │   ├── ba-elicitor/
│   │   ├── ba-synthesizer/
│   │   ├── claude-code-hooks-designer/
│   │   ├── context-before-fix/
│   │   ├── indexer/
│   │   ├── production-code-reviewer/
│   │   ├── production-quality-gatekeeper/
│   │   ├── roadmaps/
│   │   ├── sandbox-tester/
│   │   ├── skill-architect/
│   │   ├── skill-builder/
│   │   ├── skill-explorer/
│   │   ├── skill-knowledge-miner/
│   │   ├── skill-planner/
│   │   └── skill-security-reviewer/
│   ├── knowledge/                     # Agent knowledge base
│   │   ├── agents/                    # Agent lifecycle docs
│   │   │   ├── configuration.md
│   │   │   ├── capability_controls.md
│   │   │   ├── examples.md
│   │   │   ├── forks.md
│   │   │   ├── agent_hooks.md
│   │   │   ├── workflow_patterns.md
│   │   │   ├── xml_tags_standards.yaml
│   │   │   └── README.md
│   │   ├── hooks/                     # Hook implementation guides
│   │   │   ├── hooks-and-events.md
│   │   │   ├── hooks-implementation.md
│   │   │   └── hooks-reference.md
│   │   └── skills/                    # Skill docs (placeholder)
│   ├── knowleages/                    # [DUAL] Alternate knowledge tree (typo-origin)
│   │   ├── agents/agent.md
│   │   ├── hooks/hooks.md
│   │   ├── memorys/agent.md
│   │   └── skills/                    # (empty)
│   ├── hooks/                         # Active hook system
│   │   ├── registry.yaml              # Event-to-hook registry mapping
│   │   ├── validate-state-ledger.sh
│   │   ├── events/                    # Shell hook scripts
│   │   │   ├── pre-tool-use_bash_validate_command.sh
│   │   │   ├── pre-tool-use_skill_staging_gate.sh
│   │   │   ├── pre-tool-use_write_gate.sh
│   │   │   ├── post-tool-use_log_artifact.sh
│   │   │   ├── session-start_record_metadata.sh
│   │   │   └── stop_session_log_state.sh
│   │   └── tests/                     # Hook test suite
│   │       ├── fixtures/
│   │       ├── run_self_healing_tests.sh
│   │       ├── run-hook-experiment.py / .sh
│   │       ├── test_bash_validate_allow.sh
│   │       ├── test_bash_validate_block_destructive.sh
│   │       ├── test_bash_validate_block_network.sh
│   │       ├── test_skill_staging_allow_staging.sh
│   │       ├── test_skill_staging_block_runtime.sh
│   │       ├── test_write_gate_allow.sh
│   │       └── test_write_gate_block.sh
│   ├── scripts/
│   │   └── validate_suite_integrity.py
│   └── rules/                         # (empty — reserved for LSP/rules)
│
├── .agents/                           # [RUNTIME] Antigravity agent
│   ├── agents/
│   │   └── subagent-forge.md
│   └── skills/                        # Skills compiled for Antigravity
│       ├── _shared/                   # Shared schemas, knowledge, templates
│       │   ├── fixtures/
│       │   ├── knowledge/
│       │   ├── rules/
│       │   ├── schemas/
│       │   ├── templates/
│       │   └── validators/
│       ├── .omc/
│       ├── ba-analyst/
│       ├── ba-analyst copy/
│       ├── ba-elicitor/
│       ├── ba-elicitor copy/
│       ├── ba-synthesizer/
│       ├── ba-synthesizer copy/
│       ├── context-before-fix/
│       ├── html-diagram/
│       ├── html-plan/
│       ├── production-code-reviewer/
│       ├── production-quality-gatekeeper/
│       ├── scripts/
│       ├── skill-architect/
│       ├── skill-builder/
│       ├── skill-explorer/
│       ├── skill-knowledge-miner/
│       ├── skill-planner/
│       ├── skill-security-reviewer/
│       └── skills-registry.json
│
├── .hermes/                           # [RUNTIME] Hermes agent
│   └── analysis-architecture-prompt-standards.md
│
├── .omc/                              # [RUNTIME] OMC/OMX state
│   ├── handoffs/
│   │   ├── team-exec-to-verify.md
│   │   └── team-plan-to-exec.md
│   └── state/
│       ├── hud-stdin-cache.json
│       └── sessions/
│
├── .omo/                              # [RUNTIME] OMO continuation cache
│   └── run-continuation/              # Session continuation JSONs (97 files)
│
├── .codegraph/                        # CodeGraph AST index (auto-generated)
│   ├── codegraph.db / .db-shm / .db-wal
│   ├── daemon.log / .pid / .sock
│   └── .gitignore
│
├── .skill-context/                    # [STATE] Persistent state ledger
│   ├── suite_config.yaml              # Dynamic configuration overlay
│   ├── _state.yaml                    # Current pipeline state
│   ├── _sample/                       # Template state: ba-analyst/
│   ├── _subagent-staging/             # Staged subagent designs
│   │   ├── design-validator/
│   │   ├── pipeline-orchestrator/
│   │   └── quality-scorer/
│   ├── _state-archive/                # Archived state snapshots (33 entries)
│   │   ├── session-*.log
│   │   ├── tool-audit-*.log
│   │   ├── escalation_report.yaml
│   │   └── feature archives (auth-feature/, upvote-board/, etc.)
│   ├── registry/                      # Lifecycle status tracking
│   ├── skill-explorer-main-build/     # Active skill build context
│   │   ├── design.md
│   │   ├── domain-handbook.md
│   │   ├── zone-map.yaml
│   │   ├── data-contracts.yaml
│   │   ├── _ba_pipeline_state.yaml
│   │   ├── scope.2026-07-11.md
│   │   ├── ba-elicitor/ / ba-analyst/ / ba-synthesizer/
│   │   ├── architect-requirements-analysis.md
│   │   └── resources/                 # 13 resource documents
│   └── skill-knowledge-miner/         # Active miner build context
│       ├── domain-handbook.md
│       ├── exploration.md
│       ├── hydrated-context.yaml
│       ├── thought-cache.yaml
│       ├── ba-elicitor/elicitation-report.md
│       ├── ba-analyst/analyst-output.md
│       ├── ba-synthesizer/business-analysis.md
│       └── reports/quality_review_report.md
│
├── skills/                            # [SOURCE] All skill versions
│   ├── AGENTS.md
│   ├── CLAUDE.md
│   │
│   ├── ver-0.0.1/                     # Legacy v0.0.1 (14 skills)
│   │   ├── _shared/  .omc/
│   │   ├── ba-analyst/  ba-elicitor/  ba-synthesizer/
│   │   ├── production-code-reviewer/  production-quality-gatekeeper/
│   │   ├── scripts/
│   │   ├── skill-architect/  skill-builder/  skill-explorer/
│   │   ├── skill-knowledge-miner/  skill-planner/
│   │   └── skill-security-reviewer/
│   │
│   ├── ver-0.0.2/                     # Legacy v0.0.2 (14 skills + meta)
│   │   ├── _shared/  .omc/  .skill-context/
│   │   ├── ba-analyst/  ba-elicitor/  ba-synthesizer/
│   │   ├── production-code-reviewer/  production-quality-gatekeeper/
│   │   ├── scripts/
│   │   ├── skill-architect/  skill-builder/  skill-explorer/
│   │   ├── skill-knowledge-miner/  skill-planner/
│   │   ├── skill-security-reviewer/
│   │   ├── ECOSYSTEM-STATUS.md  PHASE0-ANALYSIS.md  ROADMAP.md
│   │   └── skills-registry.json
│   │
│   └── ver-3/                         # [ACTIVE] v3.0.0 Development (15 skills)
│       ├── _shared/                   # Shared infrastructure
│       │   ├── schemas/               # 15 YAML/JSON validation schemas
│       │   ├── validators/            # schema_validator.py, artifact_lifecycle.py
│       │   ├── scripts/               # drc_resolver.py, run_tests.sh
│       │   ├── templates/             # skill_readme_template.md, skill_skeleton.md, drc_contract_template.yaml
│       │   ├── knowledge/             # karpathy-standards.md
│       │   └── fixtures/              # 28 test fixtures (valid/broken pairs)
│       ├── roadmaps/                  # Development roadmaps
│       ├── ba-elicitor/   ba-analyst/   ba-synthesizer/
│       ├── indexer/
│       ├── production-code-reviewer/  production-quality-gatekeeper/
│       ├── sandbox-tester/
│       ├── skill-architect/  skill-builder/  skill-explorer/
│       ├── skill-knowledge-miner/  skill-planner/
│       └── skill-security-reviewer/
│
├── docs/                              # [ARTIFACTS] Documentation
│   ├── bugs/hooks/                    # Bug reports — hooks subsystem
│   ├── context-to-work/               # Context analysis documents (19 entries)
│   │   ├── arch-sync/
│   │   ├── architecture-crossref/
│   │   ├── architecture-sync/
│   │   ├── foundation-bootstrap/
│   │   ├── hooks-hybrid-design.2026-07-09.md
│   │   ├── next-phase-analysis/
│   │   ├── phase-1/  phase-3/  phase-4-audit/
│   │   ├── phase-5-audit/  phase-5-ba-pipeline/  phase-5-remaining-scope/
│   │   ├── phase-6-main-pipeline-skills/  phase-6-post-explorer/
│   │   ├── roadmap-analysis-phases/
│   │   ├── skill-explorer-main-build/
│   │   ├── skill-knowledge-miner-deploy/
│   │   ├── skill-output-alignment/
│   │   └── spec-split-prep/
│   ├── plans/                         # Work plans
│   │   ├── phase-3-plan.2026-07-09.md
│   │   └── plan-checklist.2026-07-07.md
│   └── Prompts/                       # Reusable prompt templates
│       └── architect-skill-explorer-v1.md
│
├── Temps/                             # [SCRATCH] Temporary artifacts
│   ├── clean/                         # Cleaned/processed temp docs
│   │   ├── architecture-design.md
│   │   ├── orchestrator-agent-spec.md
│   │   ├── protocols-and-state-spec.md
│   │   ├── quality-gates-matrix.md
│   │   ├── scope.washvn-v2-critique.2026-06-26.md
│   │   ├── skill-migration-spec.md
│   │   ├── supplements/
│   │   ├── .skill-context/
│   │   └── .gitignore
│   ├── raw/                           # Raw/scratch notes
│   │   ├── build-stage-standards.md
│   │   ├── design_analysis_and_framework.md
│   │   ├── meta-criteria.md
│   │   ├── note.md
│   │   ├── planner_analysis_and_criteria.md
│   │   ├── temps.md
│   │   └── temps2.md
│   ├── isuse/                         # Issue analyses
│   │   ├── architecture_critique.md
│   │   └── isuse1.md
│   ├── spec/                          # Spec drafts
│   │   ├── architects/                # P0-P7 architecture specs + shared/
│   │   ├── roadmaps/                  # 9 roadmap documents + index
│   │   └── README.md
│   └── prompt-idea-to-product.md
│
└── scratch/                           # Isolated test scripts
    └── test_bash_validator_boundaries.py
```

---

## Version Context

| Version | Path | Status | Skills Count | Notes |
|---------|------|--------|-------------|-------|
| v0.0.1 | `skills/ver-0.0.1/` | Legacy (archived) | 13 | First skill suite prototype |
| v0.0.2 | `skills/ver-0.0.2/` | Legacy (archived) | 14 + meta docs | Added BA pipeline + ecosystem doc |
| v3.0.0 | `skills/ver-3/` | **Active development** | 14 + roadmaps | Production-ready 8-stage pipeline |

## Agent Runtime Mapping

| Agent | Runtime Directory | Notes |
|-------|------------------|-------|
| Claude Code | `.claude/skills/` | 18 entries (incl. roadmaps, .omc, _shared) |
| Antigravity | `.agents/skills/` | 20 entries (incl. copies, html-diagram, html-plan) |
| Hermes | `.hermes/` | 1 config doc |
| OMC/OMX | `.omc/` | State + handoff cache |
| OMO | `.omo/` | Session continuation cache |

## Key Conventions

- **Edit source** in `skills/ver-3/` -> **sync** to `.claude/skills/` via `cp -r`
- **State persistence** via `.skill-context/{skill-name}/` between pipeline stages
- **Schema validation** against `skills/ver-3/_shared/schemas/*.schema.yaml`
- **Test fixtures** in `skills/ver-3/_shared/fixtures/` (valid/broken pairs per schema)
- **Symlinks**: none -- all directories are real filesystem entries
