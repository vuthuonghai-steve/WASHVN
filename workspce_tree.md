# WASHVN Workspace Directory Tree Mapping

A comprehensive routing map and layout guide for the WASHVN Master Skill Suite repository.

## Layout Overview

- `WASHVN/` (Repository Root)
  - `AGENTS.md` - L0 Root Agent Guide and Policies
  - `CLAUDE.md` - Claude Code Active Rules
  - `architecture.md` - Master Skill Suite Layered Architecture and SCS Calibration
  - `standards.md` - LLM Knowledge Activation Standards
  - `workspce_tree.md` - Workspace Tree Map (This File)
  
  - `.claude/` - Active Claude Code runtime workspace
    - `settings.json` - Custom settings & permission bounds
    - `agents/` - Active agent templates and orchestrators
      - `subagent-forge.md` - Automated agent construction forge
      - `_staging/` - Quarantine/Staging path for generated agents
      - `_archive/` - Historic and deprecated versions of agents
    - `knowledge/` - Repository-scoped structural guides & knowledge bases
      - `agents/` - Machine-readable files for agent lifecycle & configuration
        - `configuration.md`
        - `capability_controls.md`
        - `examples.md`
        - `forks.md`
        - `hooks_and_events.md`
        - `workflow_patterns.md`
        - `xml_tags_standards.yaml`
      - `skills/` - Custom micro-skills runtime documentation
      - `hooks/` - Core hook implementation guide
    - `skills/` - Custom executable micro-skills
      - `context-before-fix/` - Context analysis tool
    - `hooks/` - Active hook scripts and registration configurations
      - `registry.yaml` - Event-to-hook registry mapping
      - `events/` - Active shell hook scripts
      - `tests/` - Acceptance and security test suite for hooks
    - `scripts/` - Script repository for active utilities
      - `validate_suite_integrity.py` - Python suite integrity validator
      
  - `raw/ver-3/` - micro-skills raw development sources (symlink to skills/ver-3)
    - `_shared/` - Shared assets, schemas, templates, and libraries
      - `schemas/` - Validation schemas (YAML/JSON)
      - `validators/` - Validation helpers
      - `templates/` - File templates
      - `knowledge/` - Shared project knowledge documents (e.g. `karpathy-standards.md`)
      - `fixtures/` - Test input fixtures
    - `skill-explorer/` - Stage 0 Exploration skill
    - `skill-knowledge-miner/` - Stage 0.5 Project Knowledge extraction skill
    - `skill-architect/` - Stage 1 7-Zone Design architecture skill
    - `production-quality-gatekeeper/` - Stage 1.5 Peer Review & design gatekeeper skill
    - `skill-planner/` - Stage 2 Executable Task planner skill
    - `skill-builder/` - Stage 3 Zero placeholder code implementation skill
    - `production-code-reviewer/` - Stage 3.5 Senior engineer code reviewer skill
    - `skill-security-reviewer/` - Stage 3.8 OWASP security auditor skill
    - `sandbox-tester/` - Stage 4 Isolation runner and docker validator skill
    - `indexer/` - Stage 5 Installation and registry updates skill
    - `ba-elicitor/` - Elicitation & requirement standardizer skill
    - `ba-analyst/` - Requirement analyst skill
    - `ba-synthesizer/` - Synthesis & interlock checker skill

  - `.skill-context/` - Persistent state ledger for stateless micro-skills execution
    - `suite_config.yaml` - Dynamic configuration overlay & retention policy
    - `_state-archive/` - Archived task and project state ledgers
    - `registry/` - Lifecycle status tracking metadata
