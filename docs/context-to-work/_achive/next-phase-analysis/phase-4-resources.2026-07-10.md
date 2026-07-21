# Phase 4 — Resource Mapping & Schema Specifications

**Date**: 2026-07-10
**Status**: Initial
**Purpose**: Tổng hợp toàn bộ tài nguyên hiện có để xây dựng Phase 4 (Schemas & DRC Contracts)
**Skill**: context-before-fix v1.0.0

---

## §1: Tổng Quan Phase 4

**Phase 4**: Xây dựng foundation contracts cho Master Skill Suite:
1. **14 YAML/JSON schemas** — machine-parseable cho mỗi artifact type
2. **2 validators** (schema_validator.py, artifact_lifecycle.py) — CLI scripts
3. **3 templates** (DRC contract, skill skeleton, skill README)
4. **1 artifact registry** (`artifact_registry.yaml` — 14 entries)
5. **1 DRC resolver** (`drc_resolver.py`)
6. **28 test fixtures** (2 per schema)
7. **1 knowledge doc** (`karpathy-standards.md`)

**Path**: `skills/ver-3/_shared/` (nơi lưu tất cả deliverables)
**Dependency**: Phase 0 (✅ done — scaffold + suite_config.yaml)
**Downstream**: Phase 5 (BA Skills), Phase 6 (Main Pipeline), Phase 7 (Sandbox+Indexer)

---

## §2: Tài Nguyên Hiện Có — Full Mapping

### 2.1 Spec Architects (Temps/spec/architects/)

Đây là tài liệu thiết kế kiến trúc **5-Layer Pipeline**, là nguồn tham chiếu chính để định nghĩa schemas. Có **45+ files** trong 8 thư mục P0-P7 + shared + indexes.

| Thư mục | Phase | Files | Schema Relevance |
|:---------|:------|:------|:-----------------|
| `P0-context-bus-and-state/` | Foundation | 7 files | **Core**: context-bus-schema, artifact-registry, state-yaml-protocol, context-bus-rules |
| `P1-scs-router-and-gatekeeper/` | Routing | 5 files | **SCS/META schemas**: scs-routing, meta-criteria, spec-gatekeeper |
| `P2-context-hydrator/` | Hydration | 5 files | **Hydration schemas**: hydration-schema, thought-cache-check |
| `P3-drift-detector-and-plan-gate/` | Drift | 5 files | **Plan schemas**: plan-quality-gate, drift-detection, semantic-sampling-audit |
| `P4-orchestrator-and-assembler/` | Orchestration | 7 files | **Orchestration schemas**: SSP-protocol, parallel-builders, orchestrator-agent-spec |
| `P5-fallback-and-escalation/` | Fallback | 5 files | **Fallback schemas**: fallback-matrix-full, escalation-protocol, yaml-resilience-layer |
| `P6-deconstructor-and-miner/` | Migration | 5 files | **Miner schemas**: miner-analyzer, dual-mode, adapters |
| `P7-delta-planning-and-builder/` | Execution | 5 files | **Build schemas**: delta-planning, in-place-builder, token-budget-soft-gate |
| `shared/` | Cross-cutting | 4 files | **Architecture/Quality**: architecture-overview, glossary, pipeline-flowchart, quality-gates-reference |
| `indexes/` | Tra cứu | 3 files | by-role, by-domain, by-design |

### 2.2 Roadmap Source (skills/ver-3/roadmaps/)

| File | Phase | Lines | Content |
|:-----|:------|:-----:|:--------|
| `04-skill-pipeline-scaffold.md` | 4 | 501 | **Chính**: 12 tasks, 14 schemas, 7 AC code, DRC template |
| `05-skill-build-ba-pipeline.md` | 5 | 642 | Consumer của Phase 4 schemas |
| `06-skill-build-main-pipeline.md` | 6 | 678 | Consumer (8 skills) |
| `07-skill-build-sandbox-indexer.md` | 7 | 492 | Consumer (sandbox+indexer) |
| `08-integration-tests-hardening.md` | 8 | 467 | Integration |

### 2.3 Knowledge Docs (`.claude/knowledge/agents/`)

| File | Lines | Schema Reference |
|:-----|:-----:|:----------------|
| `configuration.md` | 280 | **Agent frontmatter schema** — pattern cho YAML field definitions |
| `capability_controls.md` | 352 | Tool/MCP/skills scoping patterns |
| `examples.md` | 308 | 4 reference agent patterns — mẫu cho fixtures |
| `forks.md` | 289 | Fork semantics |
| `hooks_and_events.md` | 626 | Hook protocol — Dual-Format (exit 2 vs stdout JSON) |
| `workflow_patterns.md` | 407 | 6 runtime workflows |
| `xml_tags_standards.yaml` | 422 | **9-tag XML whitelist** — pattern cho schema constraint definitions |

### 2.4 Config Files Existing

| File | Content | Schema Relevance |
|:-----|:--------|:-----------------|
| `.skill-context/suite_config.yaml` | Suite config — SCS hysteresis zone, resilience params | **Pattern cho YAML schema thiết kế** |
| `.claude/settings.json` | Claude settings | **Pattern cho JSON schema** |
| `.claude/hooks/registry.yaml` | Hook registry (6 hooks) | **Pattern cho artifact_registry.yaml** |

### 2.5 Đã Có Từ Phase 0

| Resource | Status | Note |
|:---------|:-------|:-----|
| `skills/ver-3/_shared/schemas/` (14 files) | ⬜ Stub | `# schema stub — Phase 4 fill` |
| `skills/ver-3/_shared/validators/` | ⬜ Empty | Chỉ `.gitkeep` |
| `skills/ver-3/_shared/scripts/` | ⬜ Empty | Chỉ `.gitkeep` |
| `skills/ver-3/_shared/templates/` | ⬜ Empty | Chỉ `.gitkeep` |
| `skills/ver-3/_shared/knowledge/` | ⬜ Empty | Chỉ `.gitkeep` |
| `skills/ver-3/_shared/data/` | ⬜ Empty | Chỉ `.gitkeep` |

---

## §3: Schema Specifications Chi Tiết

### 3.1 Schema Format Rules (Áp dụng cho tất cả 14 schemas)

```yaml
format_rules:
  draft: "JSON Schema draft-07"
  style: "YAML (except criteria.schema.json là JSON thuần)"
  required_fields:
    - $schema: "https://json-schema.org/draft-07/schema#"
    - $id: "washvn://schemas/<schema-name>"
    - title: "<Human-readable title>"
    - description: "<Purpose description>"
    - type: "object"
    - required: ["<field1>", "<field2>", ...]
    - properties: { <field definitions> }
    - additionalProperties: false
  field_conventions:
    - Mỗi property có: type, description, minimum/maximum nếu numeric
    - Enum fields: enum: [val1, val2]
    - String fields: pattern regex nếu cần format specific
    - Array fields: items + minItems
    - Optional fields: không nằm trong required
  schema_size: "≥ 30 dòng mỗi schema (roadmap yêu cầu)"
```

### 3.2 Schema #1 — exploration.schema.yaml

**Mục đích**: Validate exploration.md (Stage 0 — skill-explorer output)
**$id**: `washvn://schemas/exploration`
**Source spec**: `roadmaps/04-skill-pipeline-scaffold.md` D4-1 + `Temps/spec/architects/P0/artifact-registry.md`

**Fields cần có**:
```yaml
required:
  - skill_name          # string, pattern: ^[a-z][a-z0-9-]*$
  - scs_score           # number, min 1.0, max 5.0
  - exploration_summary # string, minLength: 100
  - identified_zones    # array, items enum: [core, knowledge, scripts, templates, data, loop, assets], minItems: 4
  - routing_decision    # object: branch (A|B), scs_at_routing, hysteresis_triggered (bool)

optional:
  - domain_anchors      # array of strings — domain terms from handbook
  - stakeholder_list    # array of objects: role, goals, pain_points
  - risk_flags          # array of strings
  - thought_cache_ref   # string — path to thought-cache.yaml
```

### 3.3 Schema #2 — criteria.schema.json (JSON format)

**Mục đích**: Validate criteria.md (Stage 0 — skill-explorer output)
**$id**: `washvn://schemas/criteria`
**Format**: JSON (theo roadmap chỉ định)
**Source spec**: `roadmaps/04` D4-1 + `Temps/spec/architects/P1/meta-criteria.md`

**Fields cần có**:
```yaml
required:
  - skill_name          # string
  - acceptance_criteria # array, minItems: 5 — META-1 yêu cầu ≥5 criteria
  - test_cases          # array, minItems: 2
    - each: { name, description, expected_result, type: [pass|fail] }

optional:
  - quality_gates       # array of gate references (BA-1→4, SCS-1→2, etc.)
  - meta_criteria_ref   # reference to META-1→3 criteria applied
  - edge_cases          # array of strings
```

### 3.4 Schema #3 — design.schema.yaml

**Mục đích**: Validate design.md (Stage 1 — skill-architect output)
**$id**: `washvn://schemas/design`
**Source spec**: `roadmaps/04` D4-1 + `Temps/spec/architects/P1/spec-gatekeeper.md` + `P3/drift-detection.md`

**Fields cần có**:
```yaml
required:
  - skill_name          # string
  - target_variable     # string — target skill/feature
  - zone_mapping        # object — 7-Zone mapping
    - zones: [core, knowledge, scripts, templates, data, loop, assets]
    - each zone: { purpose, files, constraints }
  - data_contracts      # array, minItems: 1
    - each: { contract_id, description, input_schema, output_schema }
  - state_machine       # object — pipeline state transitions
  - must_not_rules      # array, minItems: 5 — META-2 S1 yêu cầu ≥5 per phase

optional:
  - semantic_anchors    # array — domain anchor table
  - phase_deconstruction # array — 3-5 phases with I/O contracts (META-1.2)
  - quality_gates       # array — ARCH-1→4 gate references
```

### 3.5 Schema #4 — quality-matrix.schema.yaml

**Mục đích**: Validate quality-matrix.yaml (Stage 1.5 — Spec Gatekeeper output)
**$id**: `washvn://schemas/quality-matrix`
**Source spec**: `roadmaps/04` D4-1 + `Temps/spec/architects/P1/meta-criteria.md`

**Fields cần có**:
```yaml
required:
  - skill_name          # string
  - meta_scores         # object
    - META-1: { score: number 0-100, structural_integrity, domain_anchoring }
    - META-2: { score: number 0-100, semantic_depth, reverse_q }
    - META-3: { score: number 0-100, mechanical, negative_space, sandbox }
  - overall_score       # number 0-100
  - verdict             # string enum: [PASS, FAIL, PASS_WITH_WARNING]

optional:
  - signal_details      # object — S1-S4 signal pass/fail (META-2.1)
  - criteria_ref        # string — path to criteria.md
  - gate_results        # array — per-gate pass/fail detail
```

### 3.6 Schema #5 — todo.schema.yaml

**Mục đích**: Validate todo.md (Stage 2 — skill-planner output)
**$id**: `washvn://schemas/todo`
**Source spec**: `roadmaps/04` D4-1 + `Temps/spec/architects/P3/plan-quality-gate.md` + `P3/drift-detection.md`

**Fields cần có**:
```yaml
required:
  - skill_name          # string
  - tasks               # array, minItems: 1
    - each: { task_id, description, zone, priority: [high|medium|low],
              input_schema, output_schema, verification_cmd, must_not }
  - dag_dependencies    # array of { from, to } — task dependency graph
  - total_tasks         # integer

optional:
  - plan_verification   # object — PLAN-1→5 check results
  - token_budget        # object — estimated tokens per section
  - fallback_task_map   # array — F-code to task_id mapping
```

### 3.7 Schema #6 — build-log.schema.yaml

**Mục đích**: Validate build-log.md (Stage 3 — skill-builder output)
**$id**: `washvn://schemas/build-log`
**Source spec**: `roadmaps/04` D4-1 + `Temps/spec/architects/P7/token-budget-soft-gate.md`

**Fields cần có**:
```yaml
required:
  - skill_name          # string
  - build_status        # string enum: [in_progress, completed, failed]
  - build_phases        # array — log of build steps
    - each: { phase, start_time, end_time, status, artifacts }
  - warnings            # array — soft gate warnings (placeholder, token budget)

optional:
  - soft_gates          # object — BUILD-2.1, BUILD-3.1 pass/warning
  - token_budget        # object — actual vs limit
  - refactor_triggered  # boolean — REV-3.0 trigger flag
```

### 3.8 Schema #7 — review-report.schema.yaml

**Mục đích**: Validate review-report.md (Stage 3.5 — Code Reviewer output)
**$id**: `washvn://schemas/review-report`
**Source spec**: `roadmaps/04` D4-1 + `Temps/spec/architects/shared/quality-gates-reference.md`

**Fields cần có**:
```yaml
required:
  - skill_name          # string
  - review_verdict      # string enum: [PASS, FAIL, REFACTOR_REQUIRED]
  - gate_results        # array — REV-1→3 results
    - each: { gate_id, status: [pass|fail|warning], finding }
  - findings            # array — audit findings with severity
    - each: { severity: [critical|major|minor|info], file, line, description }

optional:
  - external_validator_invoked  # boolean — Γ-1 fix check
  - refactor_recommendations    # array — strings
```

### 3.9 Schema #8 — audit-metrics.schema.yaml

**Mục đích**: Validate audit-metrics.yaml (cross-cutting audit data)
**$id**: `washvn://schemas/audit-metrics`
**Source spec**: `roadmaps/04` D4-1 + `Temps/spec/architects/P3/semantic-sampling-audit.md`

**Fields cần có**:
```yaml
required:
  - run_id             # string
  - audit_type         # string enum: [sampling, full, spot]
  - metrics            # object
    - total_artifacts: integer
    - artifacts_sampled: integer
    - pass_rate: number 0-100
    - fail_rate: number 0-100

optional:
  - sampling_rate      # number — adaptive rate
  - audit_log          # array — per-sample results
  - recommendations    # array — strings
```

### 3.10 Schema #9 — verification.schema.yaml

**Mục đích**: Validate verification.md (Stage 4 — Sandbox Tester output)
**$id**: `washvn://schemas/verification`
**Source spec**: `roadmaps/04` D4-1 + `Temps/spec/architects/shared/quality-gates-reference.md` (SAND-1→2)

**Fields cần có**:
```yaml
required:
  - skill_name          # string
  - sandbox_status      # string enum: [PASS, FAIL, PASS_WITH_WARNING]
  - exit_code           # integer — SAND-2.0: 0 = pass
  - test_results        # array
    - each: { test_name, status: [pass|fail], expected, actual }

optional:
  - docker_available    # boolean — AC-8 check
  - sandbox_duration_ms # integer
  - rollback_triggered  # boolean — nếu fail → rollback_request.yaml
  - verification_log    # array — full log lines
```

### 3.11 Schema #10 — security-review.schema.yaml

**Mục đích**: Validate security-review.md (security reviewer output)
**$id**: `washvn://schemas/security-review`
**Source spec**: `roadmaps/04` D4-1 + OWASP Top 10 patterns

**Fields cần có**:
```yaml
required:
  - skill_name          # string
  - owasp_coverage      # array — A01-A10 checked
  - vulnerabilities     # array
    - each: { id, severity: [critical|high|medium|low], category, description, file, line, remediation }
  - secret_scan         # object — { enabled, findings_count }
  - overall_verdict     # string enum: [SAFE, FLAGGED, UNSAFE]

optional:
  - unsafe_patterns     # array — detected anti-patterns
  - remediation_priority # array — ordered fix list
```

### 3.12 Schema #11—14 — BA Output Schemas

Ba schema này validate BA pipeline outputs (Phase 5), tham chiếu từ `Temps/spec/architects/P0/artifact-registry.md` + `P2/thought-cache-check.md`:

#### #11 elicitation.schema.yaml — elicitation-report.md (BA Elicitor)
**$id**: `washvn://schemas/elicitation`
```yaml
required:
  - skill_name
  - domain_ontology       # object — domain terms, relationships
  - stakeholder_analysis  # array — role, goals, pain_points
  - nrfs                 # array — quantified metrics (HYD-2.0)
  - thought_cache        # object — business_thought_process, stakeholder_empathy, reverse_questions (META-2.2)
```

#### #12 analysis.schema.yaml — analysis-report.md (BA Analyst)
**$id**: `washvn://schemas/analysis`
```yaml
required:
  - skill_name
  - criteria_analysis     # array — acceptance criteria với FR/NFR classification
  - metrics               # array — quantified, regex detect number+unit
  - risk_assessment       # array — edge cases, mitigations
```

#### #13 synthesis.schema.yaml — business-analysis.md (BA Synthesizer)
**$id**: `washvn://schemas/synthesis`
```yaml
required:
  - skill_name
  - synthesized_requirements # array — merged from elicitation + analysis
  - congruence_check        # object — cross-validation results
  - pipeline_ready          # boolean — ready for Stage 0.5 SCS Router
```

#### #14 domain-handbook.schema.yaml — domain-handbook.md (Miner output)
**$id**: `washvn://schemas/domain-handbook`
```yaml
required:
  - skill_name
  - glossary              # array, minItems: 10 (MIN-1.0, F6 trigger)
  - anti_patterns         # array, minItems: 3 (MIN-2.0)
  - exemplars             # array (MIN-3.0)
  - domain_anchors        # array — terms for Architect semantic anchoring

optional:
  - success_criteria      # array — binary pass/fail
  - error_boundaries      # array — what NOT to do
  - structural_exemplars  # array — API contracts, sample code
```

---

## §4: Validator Specifications

### 4.1 schema_validator.py

**Path**: `skills/ver-3/_shared/validators/schema_validator.py`
**Dependencies**: `pyyaml`, `jsonschema`, `click` (CLI)
**Size**: ~250 dòng
**Exit codes**: 0=pass, 1=validation error, 2=path error, 3=config error

**CLI Interface**:
```bash
python3 schema_validator.py --all                                      # Validate mọi artifact
python3 schema_validator.py --artifact exploration --path <file>       # Validate 1 artifact
python3 schema_validator.py --artifact exploration --path <file> --schema <custom_schema>
python3 schema_validator.py --skills-registry                          # Cross-check registry paths
```

**Implementation notes**:
1. Parse Markdown frontmatter (YAML between `---` delimiters)
2. Map artifact name → schema file path
3. Validate with `jsonschema.validate()`
4. Output JSON: `{valid: bool, errors: [...], file: str, schema: str}`
5. Aggregate multiple file checks → single exit code

**Reference pattern**: Xem `suite_config.yaml` struct + `.claude/settings.json` pattern

### 4.2 artifact_lifecycle.py

**Path**: `skills/ver-3/_shared/validators/artifact_lifecycle.py`
**Size**: ~150 dòng

**Checks**:
1. Directory tồn tại (`.skill-context/{target}/`)
2. File artifact tồn tại nếu stage đã chạy
3. File artifact có `creation_timestamp`
4. Artifact version pinned (`v1`, `v2` nếu regenerated)
5. Drift detection: file mtime vs upstream mtimes

**Reference**: `Temps/spec/architects/P0/context-bus-rules.md` R1 (WORM), R4 (version artifacts)

### 4.3 drc_resolver.py

**Path**: `skills/ver-3/_shared/scripts/drc_resolver.py`
**Size**: ~150 dòng

**CLI Interface**:
```bash
python3 drc_resolver.py --skill <skill-name>   # Verify 1 skill's DRC contracts
python3 drc_resolver.py --all                   # Verify all skills
python3 drc_resolver.py --registry-only --registry <path>  # Verify registry consistency
```

**Checks**:
1. Mỗi skill frontmatter `output_contract` path tồn tại
2. Schema file referenced tồn tại trong `skills/ver-3/_shared/schemas/`
3. Path template resolve được
4. Input/output contracts match artifact_registry.yaml

---

## §5: Template Specifications

### 5.1 DRC Contract Template

**Path**: `skills/ver-3/_shared/templates/drc_contract_template.yaml`
**Format**: YAML
**Source spec**: `roadmaps/04` D4-4 (đã có template mẫu chi tiết)
**Purpose**: Output contract format cho mỗi skill Phase 5-7

**Sections**:
```yaml
skill_name: <placeholder>
skill_version: 0.0.1
suite: WASHVN
last_updated: <YYYY-MM-DD>

inputs:
  - { name, path_template, format, schema, required, consumed_by, downstream_phase }

outputs:
  - { file_id, path_template, format, schema, lifecycle_status, versioning }

routing:
  upstream_skills: [...]
  downstream_skills: [...]
  fallback_targets:
    - { trigger, target_skill, target_stage }

state_persistence:
  context_bus_write: <true|false>
  state_yaml_write: <true|false>
  fields_to_write: [...]
```

**Reference**: `Temps/spec/architects/P4/ssp-protocol.md` (SSP inter-skill protocol)

### 5.2 Skill Skeleton Template

**Path**: `skills/ver-3/_shared/templates/skill_skeleton.md`
**Format**: Markdown + YAML frontmatter
**Source spec**: `roadmaps/04` D4-6 (đã có skeleton mẫu)

**YAML Frontmatter fields**:
```yaml
name, description, suite, version, category, stage, target_variable, tags, when_to_use, output_contract
```

**XML sections**:
```xml
<instructions>, <safety_contract>, <knowledge_anchors>, <workflow_phases>,
<input_contract>, <output_contract>, <acceptance_criteria>, <failure_modes>
```

**Reference**: `.claude/knowledge/agents/configuration.md` (16-field pattern) + `xml_tags_standards.yaml` (9-tag whitelist)

### 5.3 Skill README Template

**Path**: `skills/ver-3/_shared/templates/skill_readme_template.md`
**Format**: Markdown
**Source spec**: `roadmaps/04` D4-5 (đã có template mẫu)

**Sections**: Role, 7-Zone Architecture, Inputs, Outputs, Quality Gates, Fallbacks, Activation Patterns

---

## §6: artifact_registry.yaml Specifications

**Path**: `skills/ver-3/_shared/artifact_registry.yaml`
**Format**: YAML
**Entries**: 14 (mapping đến 14 schemas)
**Source spec**: `roadmaps/04` D4-7 + `Temps/spec/architects/P0/artifact-registry.md`

**Entry structure**:
```yaml
artifacts:
  - artifact_id: <unique_id>
    file_name: <filename_with_ext>
    path_template: ".skill-context/{target_skill}/<filename>"
    format: <markdown|yaml|json>
    created_by: <skill/agent name>
    consumed_by: [<skill names>]
    schema: skills/ver-3/_shared/schemas/<schema_file>
    lifecycle: <WORM|append-only|versioned>
```

**Master Artifact Table** (from P0 artifact-registry.md):

| # | artifact_id | file_name | created_by | consumed_by | schema | lifecycle |
|:-:|:-----------|:----------|:-----------|:------------|:-------|:---------|
| 1 | exploration_report | exploration.md | skill-explorer | miner, architect, gatekeeper | exploration.schema.yaml | WORM |
| 2 | test_criteria | criteria.md | skill-explorer | architect, planner, tester | criteria.schema.json | WORM |
| 3 | design_doc | design.md | skill-architect | gatekeeper, hydrator, planner, drift | design.schema.yaml | WORM |
| 4 | quality_matrix | quality-matrix.yaml | gatekeeper | planner, drift, builder | quality-matrix.schema.yaml | WORM |
| 5 | todo_plan | todo.md | skill-planner | builder, drift | todo.schema.yaml | WORM |
| 6 | build_log | build-log.md | skill-builder | reviewer | build-log.schema.yaml | append-only |
| 7 | review_report | review-report.md | code-reviewer | sandbox | review-report.schema.yaml | WORM |
| 8 | audit_metrics | audit-metrics.yaml | drift-detector | cross-cutting | audit-metrics.schema.yaml | append-only |
| 9 | verification_result | verification.md | sandbox-tester | delivery | verification.schema.yaml | WORM |
| 10 | security_review | security-review.md | security-reviewer | delivery | security-review.schema.yaml | WORM |
| 11 | elicitation_report | elicitation-report.md | ba-elicitor | scs-router, miner | elicitation.schema.yaml | WORM |
| 12 | analysis_report | analysis-report.md | ba-analyst | synthesizer | analysis.schema.yaml | WORM |
| 13 | synthesis_report | business-analysis.md | ba-synthesizer | scs-router, architect | synthesis.schema.yaml | WORM |
| 14 | domain_handbook | domain-handbook.md | miner | architect, hydrator | domain-handbook.schema.yaml | WORM |

**Plus cross-cutting artifacts** (thêm vào registry nếu cần):
| 15 | state_yaml | _state.yaml | cross-cutting | cross-cutting | (no schema, free-form) | append-only |
| 16 | context_bus | context-bus.yaml | cross-cutting | cross-cutting | (schema from P0) | versioned |
| 17 | scs_rating | scs-rating.yaml | scs-router | gatekeeper, architect | (no schema) | WORM |
| 18 | hydrated_context | hydrated-context.yaml | hydrator | planner | (schema from P2) | WORM |
| 19 | thought_cache | thought-cache.yaml | ba-elicitor + gatekeeper | hydrator, builder | (schema from P2) | WORM |
| 20 | orchestration_plan | orchestration-plan.md | planner | orchestrator | (no schema) | WORM |
| 21 | plan_verification | plan-verification-report.md | drift-detector | builder | (no schema) | WORM |
| 22 | ssp_contract | ssp-contract.yaml | orchestrator | builders, assembler | (schema from P4) | WORM |

---

## §7: Test Fixture Specifications

**Path**: `skills/ver-3/_shared/test_fixtures/`
**Total**: 28 files (2 per schema: 1 valid + 1 broken)

**Naming convention**:
- Valid: `<schema_name>_valid.<ext>` — simplest passing case
- Broken: `<schema_name>_broken_<violation>.<ext>` — violates 1 constraint

**Fixture patterns** (từ roadmap + config docs):

| Schema | Valid Fixture | Broken Fixture Examples |
|:-------|:-------------|:------------------------|
| exploration | skill_name: "test-skill", scs_score: 2.5, 4+ zones | scs_score: 6.0 (out of range), missing required field |
| criteria | 5 criteria + 2 test cases | Only 1 test case (< 2), criteria < 5 |
| design | 7 zones mapped, 5 must_not rules | Missing zone, must_not < 5 |
| quality-matrix | META-1/2/3 scores ≥70, verdict PASS | META-2 score < 30, missing META-3 |
| todo | 3 tasks with DAG + verification_cmd | Task missing input_schema, circular dependency |
| build-log | Build phases complete, 0 warnings | Empty phases, missing build_status |
| review-report | PASS verdict, all gates pass, 0 critical | Missing gate_results |
| audit-metrics | Rate ≥90%, all metrics present | Negative rate, missing required fields |
| verification | exit_code 0, all tests pass | exit_code 1, missing test_results |
| security-review | SAFE, 0 vulnerabilities, A01-A10 checked | Missing owasp_coverage, UNSAFE with no findings |
| elicitation | Full thought_cache + domain_ontology | Empty thought_cache, missing stakeholder |
| analysis | FR/NFR classified, metrics quantified | No metrics, criteria_analysis empty |
| synthesis | Congruence pass, pipeline_ready true | Missing synthesized_requirements |
| domain-handbook | Glossary 10+, 3+ anti-patterns | Glossary < 10, missing anti_patterns |

---

## §8: Integration Points with Existing Infrastructure

### 8.1 Hook Framework (Phase 2)

Phase 4 schemas được consume bởi hooks:
- `post-tool-use_log_artifact.sh` → artifact_registry.yaml / build-log.schema.yaml
- `stop_session_log_state.sh` → verification.schema.yaml

### 8.2 Agent Framework (Phase 3)

Phase 4 schemas được consume bởi agents:
- `design-validator` → design.schema.yaml, quality-matrix.schema.yaml
- `quality-scorer` → quality-matrix.schema.yaml, meta-criteria
- `drift-detector` → design.schema.yaml, todo.schema.yaml (DRIFT-2→4)
- `external-code-reviewer` → review-report.schema.yaml
- `pipeline-orchestrator` → artifact_registry.yaml, drc_resolver.py

### 8.3 Suite Config (suite_config.yaml)

Các field từ suite_config.yaml tham chiếu trong schemas:
- `hysteresis_zone_scs: [2.7, 3.3]` → exploration.schema.yaml routing_decision
- `max_repair_attempts_per_artifact: 2` → artifact_lifecycle.py
- `max_history_entries: 20` → review-report.schema.yaml

### 8.4 YAML Resilience (P5 spec)

Artifact validation flow khi có YAML Resilience Layer:
```
Stage output → YAML Resilience L1 (syntax) → L2 (schema via our schemas) → L3 (cross-ref)
```

---

## §9: Build Order Khuyến Nghị

Dựa trên dependency giữa các deliverable, thứ tự build tối ưu:

```
Batch 1:  ─── Core Schemas (nhóm foundation)
  ├── exploration.schema.yaml     (#1 — nền tảng)
  ├── criteria.schema.json        (#2 — độc lập)
  ├── design.schema.yaml          (#3 — tham chiếu #1)
  └── test_fixtures batch 1       (4 schemas × 2 = 8 fixtures)

Batch 2:  ─── Quality Schemas
  ├── quality-matrix.schema.yaml  (#4 — tham chiếu #1, #3)
  ├── review-report.schema.yaml   (#7 — tham chiếu #4)
  ├── audit-metrics.schema.yaml   (#8 — độc lập)
  └── test_fixtures batch 2       (3 schemas × 2 = 6 fixtures)

Batch 3:  ─── Execution Schemas
  ├── todo.schema.yaml            (#5 — tham chiếu #3)
  ├── build-log.schema.yaml       (#6 — độc lập)
  ├── verification.schema.yaml    (#9 — độc lập)
  ├── security-review.schema.yaml (#10 — độc lập)
  └── test_fixtures batch 3       (4 schemas × 2 = 8 fixtures)

Batch 4:  ─── BA Pipeline Schemas
  ├── elicitation.schema.yaml     (#11 — độc lập)
  ├── analysis.schema.yaml        (#12 — tham chiếu #11)
  ├── synthesis.schema.yaml       (#13 — tham chiếu #11, #12)
  ├── domain-handbook.schema.yaml (#14 — độc lập)
  └── test_fixtures batch 4       (4 schemas × 2 = 8 fixtures)

Batch 5:  ─── Templates + Registry
  ├── drc_contract_template.yaml
  ├── skill_skeleton.md
  ├── skill_readme_template.md
  ├── artifact_registry.yaml
  └── (28 fixtures tổng thể review)

Batch 6:  ─── Scripts + Validators
  ├── schema_validator.py         (~250 dòng — cần schemas batch 1-4)
  ├── artifact_lifecycle.py       (~150 dòng — cần artifact_registry.yaml)
  └── drc_resolver.py             (~150 dòng — cần artifact_registry.yaml + schemas)

Batch 7:  ─── Knowledge Doc + AC Run
  ├── karpathy-standards.md       (≥100 dòng — từ standards.md §5)
  └── AC-1 đến AC-7 verification
```

---

## §10: Open Questions

| # | Question | Priority | Relevant Spec | Status |
|---|----------|----------|:--------------|:-------|
| 1 | **14 hay 22 schemas?** — Roadmap ghi 14 schemas, nhưng P0 artifact-registry.md định nghĩa 22 artifacts. 8 artifacts không có schema: `_state.yaml, context-bus.yaml, scs-rating.yaml, hydrated-context.yaml, thought-cache.yaml, orchestration-plan.md, plan-verification-report.md, ssp-contract.yaml`. Có nên thêm không? | Medium | P0 | Open |
| 2 | **Schema format**: Roadmap ghi `criteria.schema.json` (JSON) còn lại YAML. Có nhất quán không? JSON Schema có lợi thế ecosystem tools. | Low | 04-roadmap | Open |
| 3 | **Schema field granularity**: Roadmap mẫu (exploration) có ~15 fields. Cần consistent depth cho tất cả hay mỗi schema tự do? | Medium | All schemas | Open |
| 4 | **Naming convention**: `exploration.schema.yaml` vs `criteria.schema.json` — inconsistency nhỏ. Cần normalize? | Low | All schemas | Open |
| 5 | **karpathy-standards.md**: recover từ git history hay compose từ standards.md §5? Standards.md §5 đã rõ (4-layer model). | Low | D4-10 | Open |

---

## §11: Quick Reference Card

```yaml
phase_4_deliverables:
  schemas: 14 files → skills/ver-3/_shared/schemas/
  validators: 2 scripts → skills/ver-3/_shared/validators/
  scripts: 1 resolver → skills/ver-3/_shared/scripts/
  templates: 3 files → skills/ver-3/_shared/templates/
  registry: 1 file → skills/ver-3/_shared/artifact_registry.yaml
  fixtures: 28 files → skills/ver-3/_shared/test_fixtures/
  knowledge: 1 file → skills/ver-3/_shared/knowledge/karpathy-standards.md

key_resources:
  primary_spec: "skills/ver-3/roadmaps/04-skill-pipeline-scaffold.md"
  architecture_ref: "Temps/spec/architects/"
  artifact_registry_ref: "P0-context-bus-and-state/artifact-registry.md"
  quality_gates_ref: "shared/quality-gates-reference.md"
  meta_criteria_ref: "P1-scs-router-and-gatekeeper/meta-criteria.md"
  fallback_ref: "P5-fallback-and-escalation/fallback-matrix-full.md"
  knowledge_ref: ".claude/knowledge/agents/xml_tags_standards.yaml"
  suite_config: ".skill-context/suite_config.yaml"

build_batches: 7 batches (core → schemas → quality → execution → BA → templates → validators → AC)

estimated_files: ~50 files (14 schemas + 3 scripts + 3 templates + 1 registry + 28 fixtures + 1 knowledge)
estimated_effort: L (2-3 sessions)
```

---

**Document Status**: Context Complete — Resource Reference Ready
**NO Code Changes Made**

> Tài liệu này cung cấp **toàn bộ thông tin cần thiết** để build Phase 4:
> - 14 schema specs chi tiết với field definitions
> - 3 validator/script specifications
> - 3 template specifications
> - artifact_registry.yaml master table (22 artifacts)
> - 28 test fixture patterns
> - Build order tối ưu (7 batches)
> - Integration points với các phase khác

---

**Document**: `docs/context-to-work/next-phase-analysis/phase-4-resources.2026-07-10.md`
**Generated by**: context-before-fix v1.0.0
**Language**: Vietnamese
