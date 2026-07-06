# Phase 4 — Skill Pipeline Scaffold (Schemas + Validators + DRC Contracts)

> **Order:** 5th phase | **Estimated effort:** L (large) | **Predicted duration:** 2-3 sessions
> **Depends on:** Phase 0 (đã scaffold `_shared/` skeleton)
> **Downstream:** Phase 5 (BA skills), Phase 6 (main pipeline skills), Phase 7 (sandbox+indexer)
> **Architectural defects addressed:** Schema-as-prose (extract spec from markdown code blocks → `.schema.yaml` machine-parseable), Drift detection boundary là condensed context (sửa bằng schema versioning trong DRC)

## Mục đích

Phase 4 build **foundation contracts** cho skills:
1. **YAML schemas** машину-parseable cho mỗi artifact type (12 schemas)
2. **Validator script** chạy được từ CLI
3. **DRC (Dynamic Routing Contract)** template — output contract cho mỗi Phase 5/6 skill
4. **Artifact-registry template** — single source of truth về paths

Phase này là cơ sở để Phase 5-7 build skills mỗi skill có output contract hợp lệ, schema validate được.

**Quan trọng**: Phase 4 KHÔNG build skills, chỉ build **scaffolding** cho skills. Skills Phase 5-7 sẽ reference scaff + populate SKILL.md với `output_contract` field pointing tới schemas tại `raw/ver-3/_shared/schemas/`.

---

## Prerequisites

```yaml
prerequisites:
  - Phase 0 done (skeleton dirs tại raw/ver-3/_shared/schemas/)
  - Python pyyaml, jsonschema installed
  - Phase 1 knowledge docs can be referenced (xml_tags_standards.yaml etc.)
```

---

## Deliverables

### D4-1: 14 YAML/JSON schemas trong `raw/ver-3/_shared/schemas/`

Mỗi file đặc tả cấu trúc JSON-schema hoặc YAML-schema:

| File | Mục đích | Format |
|:---|:---|:---|
| `exploration.schema.yaml` | Schema exploration.md frontmatter + structure | YAML |
| `criteria.schema.json` | Schema criteria.md (≥5 tiêu chí + ≥2 test cases) | JSON |
| `design.schema.yaml` | design.md (7-Zone mapping) | YAML |
| `quality-matrix.schema.yaml` | quality-matrix.yaml (META-1→3 scores) | YAML |
| `todo.schema.yaml` | todo.md (DAG task structure) | YAML |
| `build-log.schema.yaml` | build-log.md | YAML |
| `review-report.schema.yaml` | review-report.md (audit findings) | YAML |
| `audit-metrics.schema.yaml` | audit-metrics.yaml | YAML |
| `verification.schema.yaml` | verification.md (Sandbox PASS/FAIL) | YAML |
| `security-review.schema.yaml` | security-review.md (OWASP check) | YAML |
| `elicitation.schema.yaml` | elicitation-report.md (BA output) | YAML |
| `analysis.schema.yaml` | analysis-report.md (BA output) | YAML |
| `synthesis.schema.yaml` | business-analysis.md (BA synthesized) | YAML |
| `domain-handbook.schema.yaml` | domain-handbook.md (Miner output) | YAML |

Mỗi schema có cấu trúc (JSON Schema draft-07 style, viết dưới dạng YAML):

```yaml
# exploration.schema.yaml
$schema: "https://json-schema.org/draft-07/schema#"
$id: "washvn://schemas/exploration"
title: "Exploration Report"
type: object
required: [skill_name, scs_score, exploration_summary, identified_zones, routing_decision]
properties:
  skill_name:
    type: string
    description: "Target skill name (kebab-case)"
    pattern: "^[a-z][a-z0-9-]*$"
  scs_score:
    type: number
    minimum: 1.0
    maximum: 5.0
  exploration_summary:
    type: string
    minLength: 100
    description: "Domain exploration summary"
  identified_zones:
    type: array
    items:
      type: string
      enum: [core, knowledge, scripts, templates, data, loop, assets]
    minItems: 4
  routing_decision:
    type: object
    required: [branch, scs_at_routing]
    properties:
      branch:
        type: string
        enum: [A, B]
      scs_at_routing:
        type: number
        description: "Frozen SCS score at route-time"
      # Hysteresis tracking (Γ-3 fix):
      hysteresis_triggered:
        type: boolean
        description: "True if score within ±0.3 of boundary — mandatory re-eval required"
additionalProperties: false
```

Mỗi schema phải:
- Dùng `$schema: json-schema.org/draft-07`
- Có `$id` unique (`washvn://...`)
- Có `title`, `description`
- Có `required` array rõ ràng
- Có `additionalProperties: false` unless deliberately extendable
- Document `description` cho mỗi field

### D4-2: `raw/ver-3/_shared/validators/schema_validator.py`

Script Python validator:

```python
#!/usr/bin/env python3
"""Schema Validator for WASHVN Skill Suite.

Usage:
  python3 schema_validator.py --all                  # Validate mọi artifact trong .skill-context/ tìm hence schemas
  python3 schema_validator.py --artifact exploration --path .skill-context/test-skill/exploration.md
  python3 schema_validator.py --skills-registry     # Cross-check registry declared paths tồn tại

Exit codes:
  0 = all checks pass
  1 = validation error (schema mismatch)
  2 = path resolution error
  3 = configuration error (missing schema file)
"""

# Implementation principles:
# 1. Parse markdown frontmatter (YAML between --- lines)
# 2. Apply schema via jsonschema library
# 3. Report errors with file:line context
# 4. Output JSON: {valid: bool, errors: [...], file: str, schema: str}
# 5. Aggregate multiple file checks into final exit code
```

Refperiments: `jsonschema`, `pyyaml`, `click` (CLI).

### D4-3: `raw/ver-3/_shared/validators/artifact_lifecycle.py`

Script Python kiểm tra artifact lifecycle:
- Dir tồn tại (per skill)
- File artifact exist nếu stage ran
- File artifact có creation timestamp
- Artifact version pinned (v1, v2 if regenerated)
- Drift detection: file mtime vs upstream artifact mtimes (mới nhất vs stage ran)

### D4-4: `raw/ver-3/_shared/templates/drc_contract_template.yaml`

Dynamic Routing Contract template — mỗi skill phải emit output_contract theo template này:

```yaml
# DRC Template — Dynamic Routing Contract
# Mỗi skill phải save one copy với concrete paths in SKILL.md frontmatter

skill_name: <placeholder-replace>
skill_version: 0.0.1
suite: WASHVN
last_updated: <YYYY-MM-DD>

inputs:
  - name: <input_artifact_id>
    path_template: ".skill-context/{target_skill}/<filename>.<ext>"
    format: <markdown|yaml|json|python>
    schema: "raw/ver-3/_shared/schemas/<input_schema_file>"
    required: <true|false>
    consumed_by: <consuming skill name>
    downstream_phase: <stage number naming>

outputs:
  - file_id: <output_id>
    path_template: ".skill-context/{target_skill}/<filename>.<ext>"
    format: <markdown|yaml|json|python>
    schema: "raw/ver-3/_shared/schemas/<output_schema_file>"
    lifecycle_status: <draft|final|superseded>
    versioning: <WORM|append-only|versioned>

routing:
  upstream_skills: [<previous skill name>, ...]
  downstream_skills: [<next skill name>, ...]
  fallback_targets:
    - trigger: <failure code, e.g., F5>
      target_skill: <fallback skill name>
      target_stage: <stage number>

state_persistence:
  context_bus_write: <true|false>
  state_yaml_write: <true|false>
  fields_to_write: [<field names>]
```

### D4-5: `raw/ver-3/_shared/templates/skill_readme_template.md`

Skill README template — mỗi SKILL.md phải reference canonic template:

```markdown
# {Skill Name}

> **Stage:** {Stage number}
> **Suite:** WASHVN
> **Version:** {Skill version}
> **Last Updated:** {YYYY-MM-DD}

## Role

{1-2 câu mô tả vai trò}

## 7-Zone Architecture

- **/SKILL.md** — bạn đang đọc
- **/knowledge/** — domain knowledge
- **/scripts/** — Python/Bash scripts
- **/templates/** — artifact templates
- **/data/** — schema files, YAML configs
- **/loop/** — checklist, validation loops
- **/assets/** — biểu đồ, tài liệu phụ

## Inputs

{Table input contracts}

## Outputs

{Table output contracts}

## Quality Gates

{Questions/LIST META-*, PLAN-*, BUILD-* gates applied}

## Fallbacks

{List fallback codes F1-F19 applicable}

## Activation Patterns

{Trigger phrases và invocation conditions}
```

### D4-6: `raw/ver-3/_shared/templates/skill_skeleton.md`

Skill skeleton markdown — template cho tác giả SKILL.md trong Phase 5-7:

```markdown
---
name: <skill-name>                          # kebab-case, unique
description: <trigger phrases + description> # ≥100 chars, contains trigger patterns
suite: WASHVN
version: 0.0.1
category: <monolithic-stage | hierarchical-micro-skill>
stage: <"Stage 0", "BA Stage -1", etc.>
target_variable: <target_skill|feature_name>
tags: [<list of tags>]
when_to_use: <criteria for invocation>
last_updated: <YYYY-MM-DD>
output_contract: ".skill-context/{target}/drc-<skill-name>.yaml"
---

<instructions>
{Name} skill — {1 sentence identity}
</instructions>

<safety_contract>
{must / must_not rules per architectural spec}
</safety_contract>

<knowledge_anchors>
{References to .claude/knowledge/agents/, raw/ver-3/_shared/knowledge/}
</knowledge_anchors>

<workflow_phases>
{Task-by-task execution phases}
</workflow_phases>

<input_contract>
{Inputs from upstream skills per DRC}
</input_contract>

<output_contract>
{Outputs to downstream skills per DRC}
</output_contract>

<acceptance_criteria>
{Verifiable success criteria}
</acceptance_criteria>

<failure_modes>
{Fallback codes and recovery actions}
</failure_modes>
```

### D4-7: `raw/ver-3/_shared/artifact_registry.yaml`

 bảng tổng hợp artifact registry (machine-parseable theo spec P0):

```yaml
# Canonical artifact registry — định nghĩa mỗi artifact: creator, consumer, schema
suite: WASHVN
version: 1.0
last_updated: 2026-07-04

artifacts:
  - artifact_id: exploration_report
    file_name: exploration.md
    path_template: ".skill-context/{target_skill}/exploration.md"
    format: markdown
    created_by: skill-explorer
    consumed_by: [skill-knowledge-miner, skill-architect, production-quality-gatekeeper]
    schema: raw/ver-3/_shared/schemas/exploration.schema.yaml
    lifecycle: WORM  # Write-Once-Read-Many — versioning by re-firing skill

  - artifact_id: test_criteria
    file_name: criteria.md
    path_template: ".skill-context/{target_skill}/criteria.md"
    format: markdown
    created_by: skill-explorer
    consumed_by: [skill-architect, skill-planner, sandbox-tester]
    schema: raw/ver-3/_shared/schemas/criteria.schema.json
    lifecycle: WORM

  # ... 14 artifacts per D4-1 schemas
  # Mỗi artifact entry cần:
  # artifact_id, file_name, path_template, format, created_by, consumed_by, schema, lifecycle
```

### D4-8: `raw/ver-3/_shared/scripts/drc_resolver.py`

Script Python resolve DRC — verify that each skill frontmatter `output_contract` field references existing schemas + path templates:

```python
"""DRC Resolver — Verify skill output_contract consistency.

Usage:
  python3 drc_resolver.py --skill <skill-name>     # Verify a single skill's DRC
  python3 drc_resolver.py --all                     # Verify all skills

Exit 0 = PASS
Exit 1 = DRC mismatch (path/schema mismatch)
"""
```

### D4-9: `raw/ver-3/_shared/test_fixtures/` directory

Test fixtures cho validators — 1 valid + 1 broken example per schema:

```text
test_fixtures/
├── exploration_valid.md
├── exploration_broken_scs_invalid.md
├── design_valid.md
├── design_broken_missing_zones.md
├── quality_matrix_valid.yaml
├── quality_matrix_broken_low_meta_score.yaml
└── ... (2 fixtures per schema, total ~28 files)
```

### D4-10: `raw/ver-3/_shared/knowledge/karpathy-standards.md` (backfill)

Nếu Phase 0 không tìm thấy, Phase 4 phải backfill từ git history hoặc compose từ standards.md condensed:

```bash
# Recover từ git log nếu đã tồn tại trong archived commits:
git log --all --oneline --diff-filter=A -- 'raw/ver-3/_shared/knowledge/karpathy-standards.md' | head -5
```

Nếu không recover, seed file condensed từ `standards.md` §5 (4-layer knowledge model) — extract ~150 dòng condensed content.

---

## Verification checklist (cơ học)

### AC-1 — All 14 schemas parse
```bash
python3 << 'EOF'
import yaml, os
schemas = ['exploration.schema.yaml', 'design.schema.yaml', 'quality-matrix.schema.yaml',
           'todo.schema.yaml', 'build-log.schema.yaml', 'review-report.schema.yaml',
           'audit-metrics.schema.yaml', 'verification.schema.yaml', 'security-review.schema.yaml',
           'elicitation.schema.yaml', 'analysis.schema.yaml', 'synthesis.schema.yaml',
           'domain-handbook.schema.yaml']
import json
for s in schemas:
    p = f'raw/ver-3/_shared/schemas/{s}'
    if p.endswith('.json'):
        with open(p) as f: json.load(f)
    else:
        with open(p) as f: yaml.safe_load(f)
print("AC-1 PASS")
EOF
```

### AC-2 — Schema validator runs on fixtures
```bash
# Validate against valid fixture (expect PASS):
python3 raw/ver-3/_shared/validators/schema_validator.py \
  --artifact exploration \
  --path raw/ver-3/_shared/test_fixtures/exploration_valid.md
# Should exit 0

# Validate against broken fixture (expect FAIL):
python3 raw/ver-3/_shared/validators/schema_validator.py \
  --artifact exploration \
  --path raw/ver-3/_shared/test_fixtures/exploration_broken_scs_invalid.md
# Should exit 1
echo "AC-2 PASS"
```

### AC-3 — DRC template parses + 2-field placeholder replaced
```bash
python3 -c "import yaml; data = yaml.safe_load(open('raw/ver-3/_shared/templates/drc_contract_template.yaml'))"
echo "AC-3 PASS"
```

### AC-4 — Artifact registry parses + every entry has required fields
```bash
python3 << 'EOF'
import yaml
d = yaml.safe_load(open('raw/ver-3/_shared/artifact_registry.yaml'))
assert 'artifacts' in d
for a in d['artifacts']:
    for f in ['artifact_id', 'file_name', 'path_template', 'format', 'created_by', 'consumed_by', 'schema', 'lifecycle']:
        assert f in a, f"missing field {f} in {a.get('artifact_id')}"
print(f"AC-4 PASS ({len(d['artifacts'])} artifacts declared)")
EOF
```

### AC-5 — DRC resolver runs on registry
```bash
python3 raw/ver-3/_shared/scripts/drc_resolver.py --registry-only \
  --registry raw/ver-3/_shared/artifact_registry.yaml
# Should exit 0
echo "AC-5 PASS"
```

### AC-6 — Skill skeleton template parses
```bash
test -f raw/ver-3/_shared/templates/skill_skeleton.md
grep -q "^name:" raw/ver-3/_shared/templates/skill_skeleton.md
grep -q "^suite: WASHVN" raw/ver-3/_shared/templates/skill_skeleton.md
echo "AC-6 PASS"
```

### AC-7 — Karpathy standards exist
```bash
test -f raw/ver-3/_shared/knowledge/karpathy-standards.md
test $(wc -l < raw/ver-3/_shared/knowledge/karpathy-standards.md) -ge 100
echo "AC-7 PASS"
```

---

## Step-by-step task list

1. **Plan Durante**: review lại spec Temps/spec/architects/P0-P7 + skill-explorer để ensure schemas cover all artifacts pipeline needs.

2. **Author 14 schemas** — D4-1. 14 files trong raw/ver-3/_shared/schemas/. Mỗi schema ≥ 30 dòng với full field specs. Commit atomic smith per 3-4 schemas cùng chủ đề: `phase-4: schemas for <group>`

3. **Author schema_validator.py** — D4-2. ~250 dòng. CLI với argparse, support `--all`, `--artifact <name> --path <file>`, `--skills-registry`. Validates frontmatter YAML bằng jsonschema package.

4. **Author artifact_lifecycle.py** — D4-3. ~150 dòng. Check existence + mtime + version pinning.

5. **Author DRC template** — D4-4.

6. **Author skill skeleton + README templates** — D4-6, D4-5.

7. **Author artifact_registry.yaml** — D4-7. Full entries for 14 artifacts per D4-1 schemas. Every artifact trác về spec P0 artifact-registry.md.

8. **Author drc_resolver.py** — D4-8.

9. **Author test fixtures** — D4-9. 2 per schema = 28 fixtures. Author valid fixture là simplest passing case; broken fixture violate 1 schema constraint (e.g., scs_score = 6.0 for exploration_broken_scs_invalid.md).

10. **Backfill karpathy-standards.md** — D4-10.

11. **Run AC-1 đến AC-7**. Fix any failures.

12. **Update skills-registry.json schema field** — when Phase 5-7 build skills, ensure each skill DRC points tới schemas from this phase.

---

## Definition of done (Phase 4)

```yaml
dod:
  - 14 schemas tồn tại, parse được
  - schema_validator.py exit 0 on valid fixtures, exit 1 on broken fixtures
  - 28 test fixtures (2 per schema)
  - DRC template exist + resolves
  - Artifact registry valid YAML với 14 entries
  - drc_resolver.py exit 0 on registry
  - Skill skeleton template contains required frontmatter fields
  - karpathy-standards.md tồn tại ≥ 100 dòng
```

---

## Liên kết

- [Roadmap Index](index.md)
- [Phase 3 trước](03-agent-foundation.md)
- [Phase 5 tiếp](05-skill-build-ba-pipeline.md)
- [Spec architects P0: artifact-registry](file:///home/stveve/Documents/workspace/build-workflow/WASHVN/Temps/spec/architects/P0-context-bus-and-state/artifact-registry.md)
- [Standards (4-layer model §5)](file:///home/stveve/Documents/workspace/build-workflow/WASHVN/standards.md)