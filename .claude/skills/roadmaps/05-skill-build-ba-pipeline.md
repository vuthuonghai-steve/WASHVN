# Phase 5 — Rebuild 3 BA Skills (Elicitor → Analyst → Synthesizer)

> **Order:** 6th phase | **Estimated effort:** L (large) | **Predicted duration:** 3-4 sessions
> **Depends on:** Phase 3 (ba-pipeline-runner agent ready), Phase 4 (schemas + DRC)
> **Downstream:** Phase 6 (main skill pipeline inputs from business-analysis.md từ synthesizer)
> **Architectural defects addressed:** Γ-1 (self-referential SAUDIT — BA skills phải have thought-cache schema validated)
> **Sequence importance:** BA pipeline MUST complete before Phase 6 — main skills depend on `business-analysis.md`

## Mục đích

Build 3 BA skills theo 7-Zone prep pattern architectural spec 8-stage pipeline:

```text
User business request
  ↓
ba-elicitor (Stage BA-1)        → elicitation-report.md   [thought-cache created]
  ↓
ba-analyst (Stage BA-0.5)       → analyst-output.md      [NFR quantified]
  ↓
ba-synthesizer (Stage BA-0.2)   → business-analysis.md    [synthesized, cross-validated]
  ↓
(fed vào skill-explorer Stage 0 in Phase 6)
```

Phase 5 build từng skill theo Workflow:

```text
For each skill (3 vòng lặp):
  1. Tác giả SKILL.md + frontmatter from skeleton Phase 4
  2. Tác giả knowledge/ files (domain knowledge)
  3. Tác giả templates/ artifact templates
  4. Tác giả scripts/ validator scripts (cho BA-elicitor cần empathy/constraints extraction)
  5. Tác giả loop/ kiểm soát chất lượng checklist
  6. Tác giả DRC YAML contract file
  7. Invoke quality-scorer agent (Phase 3) để audit
  8. Fix findings → re-audit until ≥80% quality score
  9. Test invoke skill với mock user request
  10. Deploy (move file từ skills/ver-3/ sang .claude/skills/ via deploy script)
```

---

## Prerequisites

```yaml
prerequisites:
  - Phase 0: skills/ver-3/ba-elicitor/, ba-analyst/, ba-synthesizer/ 7-Zone dirs tồn tại
  - Phase 3: ba-pipeline-runner agent deployed, able to invoke skills
  - Phase 4: schemas elicitation/analysis/synthesis schemas + DRC template + validator scripts available
  - subagent-forge not broken (Phase 1 fixed knowledge references)
  - Benchmark skill `context-before-fix` available as reference pattern
```

---

## 1. ba-elicitor Skill (Stage BA-1)

> Skill đầu tiên — **most important** — establishes thought-cache pattern

### D5-1-1: `skills/ver-3/ba-elicitor/SKILL.md`

Frontmatter theo skill_skeleton.md template:

```yaml
---
name: ba-elicitor
description: "Skill Stage BA-1. Trigger khi user yêu cầu elicite business requirements. Input: raw user requirements (text). Output: elicitation-report.md với thought blocks (business_thought_process, stakeholder_empathy, reverse_questions, defensive_reasoning) ≥200 tokens each. Quantifies NFR basics."
suite: WASHVN
version: 0.0.1
category: hierarchical-micro-skill
stage: "BA Stage -1"
target_variable: feature_name
tags: [ba, elicitation, business-analysis, requirement-gathering]
when_to_use: "User initially states business need without technical structure → invoke this skill to elicite. Example: 'tôi cần buildfeature tính toán giá trên mobile' → elicite to concrete requirements."
last_updated: 2026-07-04
output_contract: ".skill-context/{feature_name}/ba-elicitor/drc.yaml"
---
```

Body SKILL.md ≤ 700 tokens (L0 anchor) per CLAUDE.md rule:

```markdown
<instructions>
You are ba-elicitor skill — Stage BA-1 in Master Skill Suite. Elicit business requirements from raw user input to structured elicitation-report.md.
</instructions>

<safety_contract>
must:
  - Generate thought-cache.yaml with 5 fields per spec P2/hydration-schema
  - Ensure each thought block > 200 tokens (META-2.1 depth)
  - Include ≥4 reverse questions in reverse_questions field (META-2.2)
  - Identify ≥2 stakeholders with goals + pain points for each
must_not:
  - Generate bare minimum placeholder content ("user wants X")
  - Skip empathy sections
  - Quote user verbatim without paraphrasing
</safety_contract>

<knowledge_anchors>
- .claude/knowledge/agents/configuration.md
- .claude/knowledge/agents/capability_controls.md
- skills/ver-3/_shared/knowledge/karpathy-standards.md
- skills/ver-3/_shared/schemas/elicitation.schema.yaml
</knowledge_anchors>

<workflow_phases>
1. Read user_requirements (text)
2. <phase_intake>: Parse intent, identify domain hints
3. <phase_empathic_appreciation>: Generate stakeholder_empathy for each role identified
4. <phase_reverse_probing>: For each ambiguous requirement, generate ≥4 reverse questions per aspect (technical, business, user, constraint)
5. <phase_defensive_reasoning>: For each requirement, identify edge cases, failure modes
6. <phase_semantic_anchoring>: Map domain-specific terms to glossary array
7. <phase_emit_artifacts>: Write elicitation-report.md + thought-cache.yaml
</workflow_phases>

<input_contract>
- name: user_business_requirements
  format: text
  description: "Raw user request, e.g., 'I need an e-commerce skill' "
</input_contract>

<output_contract>
- file_id: elicitation_report
  path: .skill-context/{feature_name}/ba-elicitor/elicitation-report.md
  schema: skills/ver-3/_shared/schemas/elicitation.schema.yaml
- file_id: thought_cache
  path: .skill-context/{feature_name}/thought-cache.yaml
  schema: inline (5 fields per spec P2/thought-cache-check.md)
</output_contract>

<acceptance_criteria>
- elicitation-report.md has YAML frontmatter với feature_name, stakeholder_count, reverse_questions_count
- thought-cache.yaml có 5 sections: business_thought_process, stakeholder_empathy, reverse_questions, defensive_reasoning, semantic_anchors
- Each thought block > 200 tokens (validate bằng wc -c)
- ≥4 reverse questions documented in reverse_questions
- ≥2 stakeholders with goals + pain points
- zero placeholder elements
</acceptance_criteria>

<failure_modes>
- F16: business_thought_process missing → trigger user fallback for clarification
- F17: stakeholder_empathy or reverse_questions missing → notify ba-pipeline-runner, request user clarification
- F19: META-2.1 depth signals not all met → re-run ba-elicitor
</failure_modes>

See full docs: knowledge/, templates/, loop/.
```

### D5-1-2: `skills/ver-3/ba-elicitor/knowledge/elicitation_patterns.md`

Knowledge doc - 4 elicitation patterns reference:

```markdown
# Elicitation Patterns Reference

## Pattern 1: 5-Whys Ladder
...

## Pattern 2: Stakeholder Empathy Matrix
...

## Pattern 3: Reverse Probing Framework (4 aspects)
aspects:
  - technical: "{aspect}"
  - business: "{aspect}"
  - user: "{aspect}"
  - constraint: "{aspect}"

## Pattern 4: Defensive Reasoning Guards
- Failure mode list
- Edge case enumeration
- Confidence anchoring
```

### D5-1-3: `skills/ver-3/ba-elicitor/templates/elicitation_report.template.md`

Markdown template cho elicitation-report output:

```markdown
---
feature_name: {feature_name}
elicited_at: {timestamp}
stakeholder_count: {n}
reverse_questions_count: {n}
summary: {one_sentence}
glossary_terms: [...]
---

# {feature_name} — Elicitation Report

## Domain & Problem
{domain_summary}

## Stakeholders
For each stakeholder:
- Role: {role}
- Goals: {goals}
- Pain Points: {pain_points}

## Reverse Questions
For each ambiguous requirement:
- Topic: {topic}
- Aspect Technical: {question_t}
- Aspect Business: {question_b}
- Aspect User: {question_u}
- Aspect Constraint: {question_c}

## Defensive Reasoning
For each high-risk aspect:
- Aspect: {aspect}
- Failure Mode: {failure}
- Mitigation: {mitigation}

## Glossary
{terms with definitions}
```

### D5-1-4: `skills/ver-3/ba-elicitor/templates/thought_cache_template.yaml`

```yaml
# thought-cache.yaml template
reflection_cache:
  business_thought_process:
    - block_id: bp-001
      block: >- 
        {Thể hiện chain-of-thought về intent người dùng, >200 tokens}
  stakeholder_empathy:
    - role: {role_name}
      goals: [...]
      pain_points: [...]
  reverse_questions:
    - topic: {topic}
      technical_question: {question}
      business_question: {question}
      user_question: {question}
      constraint_question: {question}
  defensive_reasoning:
    - aspect: {aspect}
      failure_mode: {description}
      mitigation: {description}
  semantic_anchors:
    {term}: { definition within domain }
```

### D5-1-5: `skills/ver-3/ba-elicitor/loop/scoping_checklist.md`

Checklist cho self-verification:

```yaml
post_run_checklist:
  - "elicitation-report.md frontmatter có feature_name?"
  - "thought-cache.yaml có 5 sections?"
  - "Each thought block > 200 tokens? (wc -c check)"
  - "≥4 reverse questions?"
  - "≥2 stakeholders?"
  - "Zero placeholder strings (TODO, FIXME, mock)?"
  - "Glossary có ≥3 domain terms?"
  - "YAML frontmatter elicit-report parses?"
```

### D5-1-6: `skills/ver-3/ba-elicitor/scripts/validate_outputs.py`

Script Python local validator:

```python
#!/usr/bin/env python3
"""ba-elicitor output validator.

Reads elicitation-report.md + thought-cache.yaml at .skill-context/{feature}/ba-elicitor/ and .skill-context/{feature}/thought-cache.yaml
Validates 8 criteria per checklist.
"""
# Implementation: parse markdown frontmatter, parse YAML, check 5 thought block token counts via simple wc heuristic
```

### D5-1-7: `skills/ver-3/ba-elicitor/data/drc.yaml`

DRC contract file (copy template D4-4, fill concrete paths):

```yaml
skill_name: ba-elicitor
skill_version: 0.0.1
suite: WASHVN
last_updated: 2026-07-04

inputs:
  - name: user_business_requirements
    path_template: "TEXT INPUT from user/invoke"
    format: text
    required: true

outputs:
  - file_id: elicitation_report
    path_template: ".skill-context/{feature_name}/ba-elicitor/elicitation-report.md"
    format: markdown
    schema: skills/ver-3/_shared/schemas/elicitation.schema.yaml
    lifecycle: WORM
    consumed_by: [ba-analyst]
    downstream_phase: "BA Stage -0.5"
  - file_id: thought_cache
    path_template: ".skill-context/{feature_name}/thought-cache.yaml"
    format: yaml
    schema: inline (per spec P2/thought-cache-check.md)
    lifecycle: append-only-by-stage-1.5-only
    consumed_by: [ba-analyst, ba-synthesizer, architect, builder]
    downstream_phase: "Multiple"

routing:
  upstream_skills: []
  downstream_skills: [ba-analyst]
  fallback_targets:
    - trigger: F16
      target_skill: ba-elicitor
      target_stage: "BA Stage -1"
    - trigger: F17
      target_skill: ba-elicitor
      target_stage: "BA Stage -1"
    - trigger: F19
      target_skill: ba-elicitor
      target_stage: "BA Stage -1"
```

### D5-1-8: Empty placeholders (`skills/ver-3/ba-elicitor/assets/`)

Thêm 1 `.gitkeep` file để maintain dir. Assets sẽ fill nếu cần diagrams sau.

---

## 2. ba-analyst Skill (Stage BA-0.5)

> Skill thứ 2 — consumes elicitation-report, outputs analyst-output

### D5-2-1: `skills/ver-3/ba-analyst/SKILL.md`

Frontmatter:

```yaml
---
name: ba-analyst
description: "Skill Stage BA-0.5. Trigger khi elicitation-report.md từ ba-elicitor ready. Phân tích elicitation, structure thành technical spec, classify FR/NFR, quantify metrics."
suite: WASHVN
version: 0.0.1
category: hierarchical-micro-skill
stage: "BA Stage -0.5"
target_variable: feature_name
tags: [ba, analysis, technical-spec, fr-nfr]
when_to_use: "After ba-elicitor produces elicitation-report.md → invoke ba-analyst to convert to structured technical analysis."
last_updated: 2026-07-04
output_contract: ".skill-context/{feature_name}/ba-analyst/drc.yaml"
---
```

Body sections tương tự ba-elicitor structure (identity, safety, knowledge_anchors, workflow, input/output contracts, acceptance, failure modes). Quan trọng:

```markdown
<workflow_phases>
1. Read elicitation-report.md
2. <phase_classify>: Phân loại requirements: Functional Requirements (FR) vs Non-Functional (NFR)
3. <phase_quantify_nfrs>: Convert qualitative NFRs → measurable metrics (e.g., "fast response" → "<200ms latency at 95th percentile")
4. <phase_interlock>: Cross-reference stakeholder goals vs NFRs (ensure each main goal has ≥1 NFR)
5. <phase_emit_analysis>: Write analyst-output.md
</workflow_phases>

<input_contract>
- name: elicitation_report
  path: .skill-context/{feature_name}/ba-elicitor/elicitation-report.md
  required: true
- name: thought_cache
  path: .skill-context/{feature_name}/thought-cache.yaml
  required: true
  usage: "Note: Analyst may read thought-cache nhưng optional — designed per spec P2 dual-context-ingestion.md"
</input_contract>

<output_contract>
- file_id: analysis_report
  path: .skill-context/{feature_name}/ba-analyst/analyst-output.md
  schema: skills/ver-3/_shared/schemas/analysis.schema.yaml
</output_contract>

<acceptance_criteria>
- Each FR has unique ID (FR-001, FR-002, ...)
- Each NFR has quantifiable metric + unit
- Cross-reference table: stakeholder goals ↔ NFRs ≥ 80% coverage
- glossary expansion vs elicitation ≥ 30% (knowledge growth)
- Zero placeholder strings
</acceptance_criteria>
```

### D5-2-2: `skills/ver-3/ba-analyst/knowledge/fr_nfr_taxonomy.md`

Knowledge doc với FR/NFR classification framework.

### D5-2-3: `skills/ver-3/ba-analyst/templates/analysis_report.template.md`

### D5-2-4: `skills/ver-3/ba-analyst/loop/interlock_checklist.md`

### D5-2-5: `skills/ver-3/ba-analyst/scripts/validate_metrics.py`

Script check NFR quantification (regex detect number + unit).

### D5-2-6: `skills/ver-3/ba-analyst/data/drc.yaml`

---

## 3. ba-synthesizer Skill (Stage BA-0.2)

> Skill thứ 3 — consumes both elicitation + analysis, outputs business-analysis.md (input cho Phase 6 skill-explorer)

### D5-3-1: `skills/ver-3/ba-synthesizer/SKILL.md`

```yaml
---
name: ba-synthesizer
description: "Skill Stage BA-0.2. Trigger khi elicitation-report.md AND analyst-output.md available. Synthesize 2 artifacts thành business-analysis.md (single source of truth cho downstream pipeline). Cross-validate congruence between elicitation nuance và analysis structure."
suite: WASHVN
version: 0.0.1
category: hierarchical-micro-skill
stage: "BA Stage -0.2"
target_variable: feature_name
tags: [ba, synthesis, business-analysis, cross-validation]
when_to_use: "After ba-analyst produces analyst-output.md → invoke để synthesize final business-analysis.md. Skill final trong BA pipeline. Output feeds vào skill-explorer Stage 0."
last_updated: 2026-07-04
output_contract: ".skill-context/{feature_name}/ba-synthesizer/drc.yaml"
---
```

Quan trọng workflow phases:

```markdown
<workflow_phases>
1. Read elicitation-report.md AND analyst-output.md AND thought-cache.yaml
2. <phase_cross_validate>:
   - Check every stakeholder goal in elicitation có ≥1 FR/NFR trong analysis
   - Check every reverse question addressed
   - Check every defensive reason point có mitigation trong analysis
3. <phase_resolve_gaps>:
   - Nếu elicitation có goal không có FR/NFR tương ứng → flag gap, add implicit FR
   - Nếu reverse question không được address trong analysis → annotate
4. <phase_synthesize>: Merge 2 artifacts với narrative thread
5. <phase_emit>: Write business-analysis.md
</workflow_phases>

<input_contract>
- name: elicitation_report
  path: .skill-context/{feature_name}/ba-elicitor/elicitation-report.md
  required: true
- name: analysis_report
  path: .skill-context/{feature_name}/ba-analyst/analyst-output.md
  required: true
- name: thought_cache
  path: .skill-context/{feature_name}/thought-cache.yaml
  required: true
  usage: "Read stakeholder_empathy + reverse_questions to verify congruence"
</input_contract>

<output_contract>
- file_id: synthesized_business_analysis
  path: .skill-context/{feature_name}/business-analysis.md
  schema: skills/ver-3/_shared/schemas/synthesis.schema.yaml
  consumed_by: [skill-explorer]
  downstream_phase: "Stage 0"
</output_contract>

<acceptance_criteria>
- business-analysis.md has unified narrative (single source)
- All elicitation nuance preserved (no information loss vs elicit+analysis)
- Cross-validation table > 90% alignment (not perfect because synthesis adds context)
- Zero unresolved reverse questions
- Glossary ≥5 terms (mine from elicitation)
- frontmatter có: feature_name, complexity_hint, downstream_skill_recommendation
</acceptance_criteria>
```

### D5-3-2 to D5-3-6: analogous files

Pattern:
- knowledge/cross_validation_strategies.md
- templates/business_analysis_template.md
- loop/congruence_checklist.md
- scripts/check_congruence.py (script compareselicitation vs analysis artifacts)
- data/drc.yaml

---

## Verification checklist (cơ học)

### AC-1 — 3 skills deploy tại `.claude/skills/`
```bash
for skill in ba-elicitor ba-analyst ba-synthesizer; do
  test -f .claude/skills/$skill/SKILL.md || exit 1
done
echo "AC-1 PASS"
```

### AC-2 — Each skill frontmatter hợp lệ
```bash
python3 << 'EOF'
import yaml
for s in ['ba-elicitor', 'ba-analyst', 'ba-synthesizer']:
    with open(f'.claude/skills/{s}/SKILL.md') as f:
        c = f.read()
    fm = c.split('---')[1]
    d = yaml.safe_load(fm)
    for f_name in ['name', 'description', 'suite', 'version', 'category', 'stage', 'target_variable', 'tags', 'when_to_use', 'output_contract']:
        assert f_name in d, f"{s} missing {f_name}"
    assert d['suite'] == 'WASHVN'
    assert d['name'] == s
print("AC-2 PASS")
EOF
```

### AC-3 — SKILL.md ≤ 700 tokens (L0 anchor rule per CLAUDE.md)
```bash
for skill in ba-elicitor ba-analyst ba-synthesizer; do
  wc -w .claude/skills/$skill/SKILL.md | awk '$1 > 800 { exit 1 } END { print "  - pass"}'
done
echo "AC-3 PASS"
```

### AC-4 — 7-Zone structure populate ≥4 zones
```bash
for skill in ba-elicitor ba-analyst ba-synthesizer; do
  populated=0
  for zone in knowledge scripts templates loop data; do
    [ -d .claude/skills/$skill/$zone ] && ls .claude/skills/$skill/$zone/*.md 2>/dev/null && populated=$((populated+1))
  done
  # Allow 4/5 zones (assets optional)
  test "$populated" -ge 4 || exit 1
done
echo "AC-4 PASS"
```

### AC-5 — DRC files parse + reference existing schemas
```bash
for skill in ba-elicitor ba-analyst ba-synthesizer; do
  python3 -c "import yaml; yaml.safe_load(open('.claude/skills/$skill/data/drc.yaml'))"
done
echo "AC-5 PASS"
```

### AC-6 — Test invoke skill với mock user request
```bash
# Mock: create a feature dir, simulate user request
mkdir -p .skill-context/mock-ecommerce/
echo "I need an e-commerce skill for selling Vietnamese handcrafted goods internationally" > /tmp/mock_user_req.txt

# Invoke ba-elicitor via skill-pipeline-orchestrator (Phase 3 deployed)
# Or directly via Task call:
# task(subagent_type=skill-pipeline-orchestrator, prompt="invoke ba-elicitor for feature 'mock-ecommerce' with input at /tmp/mock_user_req.txt")

# Manual verification:
test -f .skill-context/mock-ecommerce/ba-elicitor/elicitation-report.md
test -f .skill-context/mock-ecommerce/thought-cache.yaml
test $(wc -c < .skill-context/mock-ecommerce/ba-elicitor/elicitation-report.md) -ge 1000
python3 -c "import yaml; d=yaml.safe_load(open('.skill-context/mock-ecommerce/thought-cache.yaml')); assert 'reflection_cache' in d"
echo "AC-6 PASS"
```

### AC-7 — Mock full BA pipeline
```bash
# Invoke full pipeline: ba-elicitor → ba-analyst → ba-synthesizer
# Then verify:
test -f .skill-context/mock-ecommerce/business-analysis.md
# Cleanup mock:
rm -rf .skill-context/mock-ecommerce/
echo "AC-7 PASS (mock pipeline test)"
```

### AC-8 — Aggregate quality gatekeeper agent (Phase 3) gives ≥70% score
```bash
# Manually invoke quality-scorer on each skill's SKILL.md:
# task(subagent_type=quality-scorer, prompt="evaluate .claude/skills/ba-elicitor/SKILL.md vs META-1→3 criteria")
# Receive evaluation-report.md, ensure quality_score ≥ 70
echo "AC-8 NEEDED_MANUAL"
```

### AC-9 — Pipeline runner agent (Phase 3 ba-pipeline-runner) can chain 3 skills

Should be verified through AC-7 (same test path).

---

## Step-by-step task list

1. **Build ba-elicitor** (D5-1-1 to D5-1-7). Commit per file group:
   - `phase-5: ba-elicitor SKILL.md + DRC`
   - `phase-5: ba-elicitor knowledge + templates`
   - `phase-5: ba-elicitor loop + scripts`

2. **Run local validator** on ba-elicitor scripts/validate_outputs.py.

3. **Invoke quality-scorer** to audit ba-elicitor. Fix findings ≥70% score.

4. **Test invoke skill manually** with a mock user request (e.g., "build an e-commerce skill"). Verify elicitation-report.md + thought-cache.yaml created.

5. **Build ba-analyst** (D5-2-1 to D5-2-6). Commit per group.

6. **Invoke quality-scorer** audit, fix.

7. **Test ba-analyst** with output từ step 4's elicitation-report. Verify analyst-output.md created.

8. **Build ba-synthesizer** (D5-3-1 to D5-3-6). Commit per group.

9. **Invoke quality-scorer** audit, fix.

10. **Test ba-synthesizer** with output từ steps 4 + 7. Verify business-analysis.md created.

11. **Test full pipeline through ba-pipeline-runner agent** (Phase 3):
    - Invoke `ba-pipeline-runner` with mock request
    - Verify `_ba_pipeline_state.yaml` updated
    - Verify all 3 artifacts produced in order

12. **Deploy 3 skills**: move `skills/ver-3/ba-*/` to `.claude/skills/ba-*/` via deploy script.

13. **Update `skills-registry.json`** — verify 3 BA skills already listed.

14. **Update `_state.yaml`** — record phase 5 completion.

15. **Run full AC-1 to AC-9**, fix any failures.

---

## Definition of done (Phase 5)

```yaml
dod:
  - 3 skills deployed .claude/skills/ba-{elicitor,analyst,synthesizer}/
  - All AC-1 to AC-7 PASS (AC-8 and AC-9 pass via gatekeeper validation)
  - Skills-registry.json references valid
  - Full BA pipeline test invocation successful with 1 mock feature
  - business-analysis.md output creates file ready for skill-explorer consumption (Phase 6)
  - Each skill reviewed quality-scorer approved ≥70%
```

---

## Liên kết

- [Roadmap Index](index.md)
- [Phase 4 trước](04-skill-pipeline-scaffold.md)
- [Phase 6 kế tiếp](06-skill-build-main-pipeline.md)
- [Spec P2 dual-context-ingestion](../../../Temps/spec/architects/P2-context-hydrator/dual-context-ingestion.md)
- [Spec P1 re-validation-rule F16-F19](../../../Temps/spec/architects/P1-scs-router-and-gatekeeper/re-validation-rule.md)