# === OUTPUT SPEC — build-log.md schema for skill-builder ver-0.0.3 ===
# [TỪ DESIGN §6 + §7 Tier 3 templates, BA §2.1 FR-05, HANDBOOK §6.5, todo.md §6]
# Full target_skill build scaffold. 3 mandatory sections (Resource Inventory + Resource Usage Matrix + Validation Result).

output_spec:
  version: "2.0"
  target_file: ".skill-context/{target_skill}/build-log.md"
  format: "markdown"
  schema: "raw/ver-3/_shared/schemas/build-log.schema.yaml"

frontmatter:
  required_fields:
    - "skill_schema_version: '3.1.0'"
    - "artifact_type: 'build-log'"
    - "skill_name: '{target_skill}'"
    - "version: '0.0.3'"
    - "generated_by: 'skill-builder'"
    - "generated_at: <ISO8601>"
    - "stage: 'builder'"
    - "status: 'in_progress' | 'build-completed' | 'build-blocked'"
    - "execution_id: <UUID4>"
    - "execution_trace: <array>"

execution_trace:
  description: "Array of per-file events with required fields"
  required_fields:
    - "timestamp: <ISO8601>"
    - "task_id: 'T{N}.{M}'"
    - "phase: 'PH1' | 'PH2' | 'PH3' | 'PH4' | 'PH5'"
    - "action: 'CREATE_FILE' | 'MODIFY_FILE' | 'VALIDATE' | 'RUN_SCRIPT'"
    - "file: <path>"
    - "status: 'success' | 'failed' | 'skipped'"
    - "notes: <string>"
    - "decision: 'CONTINUE' | 'HALT' | 'ROLLBACK'"
    - "trace_tag: '[TỪ TODO #N]'"

# === 3 MANDATORY SECTIONS (FR-05) ===
mandatory_sections:
  - title: "Resource Inventory"
    heading: "## Resource Inventory"
    description: "Liệt kê tất cả input resources consumed during build"
    required_content:
      - "design.md path with version + checksum"
      - "todo.md path with phase count + task count"
      - "quality-matrix.yaml path with score"
      - "resources/* paths (if any) with line counts"
      - "data/* paths (if any) with format + size"
      - "loop/* paths (if any) with checkpoint status"
    template: |
      ## Resource Inventory

      | Resource Path | Type | Version | Status | Notes |
      |---------------|------|---------|--------|-------|
      | `design.md` | Critical | 0.0.3 | READY | 12 sections, 9 zones, 18 files |
      | `todo.md` | Critical | 0.0.3 | READY | 27 tasks, 10 phases |
      | `quality-matrix.yaml` | Critical | 0.0.3 | PASS | 98.2% / 161/161 MUST |
      | `ba-report.md` | Domain | 0.0.3 | READY | 19 FR + 10 NFR |
      | `domain-handbook.md` | Domain | 0.0.3 | READY | 70+ citations |

  - title: "Resource Usage Matrix"
    heading: "## Resource Usage Matrix"
    description: "Critical-resource → Task → Output mapping with evidence"
    required_content:
      - "Every Critical resource MUST have row"
      - "Format: | `Resource` | Priority | Used In Task | Output File(s) | Notes |"
      - "Each row MUST have backticked path"
      - "Notes column MUST cite trace tag"
    template: |
      ## Resource Usage Matrix

      | Resource File | Priority | Used In Task | Output File(s) | Notes |
      |---------------|----------|--------------|----------------|-------|
      | `design.md` | Critical | T0.1, T8.1 | `SKILL.md`, `policy/skill-builder.yaml` | Zone contract source [TỪ DESIGN §3] |
      | `todo.md` | Critical | T1.1-T8.1 | All 18 files | Phase-driven task list [TỪ TODO #N] |
      | `resources/api-spec.md` | Critical | T3.2 | `knowledge/api-patterns.md` | 1:1 fidelity check [TỪ DESIGN §2.1] |

  - title: "Validation Result"
    heading: "## Validation Result"
    description: "Validator + checklist + threshold outcomes"
    required_content:
      - "Validator exit code + error count + warning count"
      - "Build-checklist v2.0.0 MUST check pass/fail summary"
      - "Placeholder density count + threshold band"
      - "Token budget check (SKILL.md count + zone budgets)"
      - "Security review verdict (if security_gate_required)"
      - "Final lifecycle transition status"
    template: |
      ## Validation Result

      ### Validator
      - **Exit Code**: 0 (PASS)
      - **Errors**: 0
      - **Warnings**: 2 (orphan sub-skill files, tier_knowledge_parity partial)

      ### Build-Checklist v2.0.0
      - **Total Checks**: 35
      - **PASS**: 33 / 35
      - **FAIL**: 0
      - **MUST Checks**: 30 / 30 PASS

      ### Placeholder Density
      - **Count**: 0
      - **Threshold**: < 5 PASS

      ### Token Budget
      - **SKILL.md**: 387 tokens (L0 ≤400 target OK)
      - **policy/skill-builder.yaml**: 1100 tokens (L1 ≤1200 OK)

      ### Security Review
      - **Status**: SKIPPED (no auth/payment/upload features)

      ### Lifecycle
      - **Phase**: build-completed
      - **Transition**: designed → built
      - **Timestamp**: 2026-06-18T15:30:00Z

# === FEEDBACK ARRAYS ===
feedback_arrays:
  feedback_to_planner:
    description: "Issues that Planner needs to address in next iteration"
    format: "Array of {id, type, blocks_build, source, issue, action, status}"
    example:
      - "FB-001: TODO_TASKS | yes | todo.md §2 | 2 tasks missing trace tag | Planner add [TỪ DESIGN §3.2] | OPEN"
  feedback_to_architect:
    description: "Design issues that Architect needs to revise"
    format: "Array of {id, type, blocks_build, source, issue, action, status}"
    example:
      - "FB-101: ZONE_MAPPING | no | design.md §3 | Optional zone file_required: false | Architect verify | RESOLVED"

# === STATUS ENUMS ===
status_enums:
  build_status:
    - "READY_FOR_BUILD"
    - "BLOCKED_BY_DESIGN"
    - "BLOCKED_BY_PLAN"
    - "BLOCKED_BY_RESOURCES"
    - "BUILT_WITH_WARNINGS"
    - "COMPLETE"
  file_status:
    - "success"
    - "failed"
    - "skipped"
  action_enum:
    - "CREATE_FILE"
    - "MODIFY_FILE"
    - "VALIDATE"
    - "RUN_SCRIPT"
  decision_enum:
    - "CONTINUE"
    - "HALT"
    - "ROLLBACK"

# === QUALITY METRICS BLOCK ===
quality_metrics:
  required_fields:
    - "placeholder_ratio: <0.0-1.0>"
    - "placeholder_count: <int>"
    - "zone_coverage: <0.0-1.0>"
    - "critical_tasks_done: <bool>"
    - "validator_pass: <bool>"
    - "checklist_pass: <bool>"
    - "blocker_count: <int>"
    - "trace_tag_coverage: <0.0-1.0>"
    - "skill_md_token_count: <int>"

# === EXECUTION_ID + TIMESTAMP NORMALIZATION (R12 idempotency) ===
idempotency:
  execution_id: "<UUID4 generated at Phase 1 start>"
  timestamp_format: "ISO8601 with timezone (e.g., 2026-06-18T15:30:00+07:00)"
  normalization: "Strip execution_id and timestamps before 3-run diff"
  reference: "todo.md §5 Q7 RESOLVED, design.md §8 R12"
