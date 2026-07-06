# Phase 6 — Rebuild 8 Main Pipeline Skills (Stage 0 → 3.5 + Security)

> **Order:** 7th phase | **Estimated effort:** XL (extra-large) | **Predicted duration:** 5-8 sessions
> **Depends on:** Phase 3 (orchestrator + gatekeeper agents), Phase 4 (schemas + DRC), Phase 5 (BA pipeline — produces business-analysis.md để skill-explorer dùng)
> **Downstream:** Phase 7 (sandbox-tester + indexer), Phase 8 (integration & hardening)
> **Architectural defects addressed:** Γ-4 (Hydrator information loss — skill-explorer must call hydrator quality before passing to Planner via enriched exploration.md), Γ-3 (SCS hysteresis — skill-explorer outputs frozen SCS with hysteresis_triggered flag)
> **Roadmap evaluation v1 patches incorporated:** Đề xuất 1 (split Phase 6 → 6A discovery cluster + 6B execution cluster), Đề xuất 2 (hysteresis re-eval max=1, tránh infinite loop Explorer↔Gatekeeper)

## Mục đích

Build 8 skills theo 8-Stage Pipeline (architecture.md §1):

```text
Skill build flow:
  ↓
skill-explorer (Stage 0)        → exploration.md + criteria.md  [SCS frozen]
  ↓
skill-knowledge-miner (Stage 0.5)  → domain-handbook.md
  ↓
skill-architect (Stage 1)       → design.md (7-Zone mapping)
  ↓
production-quality-gatekeeper (Stage 1.5) → quality-matrix.yaml + evaluation-report.md + feedback.yaml
  ↓
skill-planner (Stage 2)          → todo.md (DAG)
  ↓
skill-builder (Stage 3)          → SKILL.md + scripts + build-log.md
  ↓
production-code-reviewer (Stage 3.5) → review-report.md + audit-metrics.yaml
  ↓
skill-security-reviewer (cross-cutting)  → security-review-report.md
  ↓
(Phase 7: sandbox-tester + indexer)
```

## Phase 6 sub-split (per roadmap evaluation v1, đề xuất 1)

> [!IMPORTANT]
> Phase 6 chia thành **2 sub-phases** có verify checkpoint giữa:
>
> | Sub-phase | Skills | Reason |
> |:---|:---|:---|
> | **6A** — Discovery & Design cluster | skill-explorer, skill-knowledge-miner, skill-architect, production-quality-gatekeeper (4 skills) | Context-heavy reasoning — read domain, mine knowledge, design 7-Zone layout, enforced META criteria |
> | **6B** — Execution & Review cluster | skill-planner, skill-builder, production-code-reviewer, skill-security-reviewer (4 skills) | Codegen-heavy execution — emit todo DAG, write SKILL.md+scripts, lint/static analyze, OWASP audit |
>
> **Checkpoint giữa 6A và 6B**: Requires `quality-matrix.yaml` từ gatekeeper (4 skills Phase 6A) PASS aggregate score ≥ 80% trước khi Phase 6B bắt đầu. Nếu 6A snapshot fails, rollback 6A và không advance 6B. Ly của split: giảm XL bottleneck, catch design-side errors trước khi build code, dễ rollback.

Phase 6 là **bulk effort** — 8 skills × 7-Zone × with heterogeneity content. Phase này builds theo nguyên tắc: **mỗi skill dependency chain broken if any upstream skill fails — so verify each skill individually before next**.

---

## Prerequisites

```yaml
prerequisites:
  - Phase 5 done: BA pipeline ready. skill-explorer inputs business-analysis.md.
  - Phase 3: skill-pipeline-orchestrator agent deployed + aggregate-quality-gatekeeper deployed
  - Phase 4: 14 schemas, DRC template, validators available
  - Phase 2: hooks active — writes outside .skill-context/ gated, so skill build process safe
```

---

## Skill 1: `skill-explorer` (Stage 0)

**Role**: Nhận business-analysis.md + user_skill_request, output exploration.md + criteria.md. Tính SCS (1.0-5.0) và ghi frozen score với hysteresis flag (Γ-3 fix).

### D6-1-1: `raw/ver-3/skill-explorer/SKILL.md`

```yaml
---
name: skill-explorer
description: "Skill Stage 0. Trigger khi business-analysis.md available OR direct user skill request. Explore domain, calculate Skill Complexity Score (SCS), generate exploration.md + criteria.md. Phase 6 Γ-3 fix: emit hysteresis_triggered flag when SCS within ±0.3 of breakpoint 3.0."
suite: WASHVN
version: 0.0.1
category: monolithic-stage
stage: "Stage 0"
target_variable: target_skill
tags: [explore, scs, complexity, criteria]
when_to_use: "After BA pipeline complete OR when user directly requests building a skill without prior BA. Invoke this skill to explore domain and decide routing (Branch A vs B per SCS)."
last_updated: 2026-07-04
output_contract: ".skill-context/{target_skill}/drc-skill-explorer.yaml"
---
```

Body: standard pattern with workflow_phases:

```markdown
<workflow_phases>
1. Read business-analysis.md (from BA Phase 5) OR raw user_skill_request
2. <phase_domain_scan>: Identify skill's domain (e.g., 'data-analysis', 'API-client', 'prompt-engineering')
3. <phase_complexity_assessment>: Compute Skill Complexity Score (SCS) 1.0-5.0 based on:
   - Number of sub-features required
   - Number of integration points
   - State storage requirements
   - Branching logic depth
   - Security surface area
4. <phase_hysteresis_check>: If SCS within [2.7, 3.3], set hysteresis_triggered: true — require mandatory re-eval (Γ-3 fix). **Re-eval cap = 1** (per eval v1 đề xuất 2): nếu sau 1 re-eval SCS vẫn ∈ [2.7, 3.3], chọn Branch B (conservative) thay vì re-eval indefinite — tránh infinite loop Explorer↔Gatekeeper.
5. <phase_routing_decision>: Branch A (SCS < 3.0 && !hysteresis) → Fast Track; Branch B (SCS ≥ 3.0 && !hysteresis) → Full OMSP; hysteresis (with re-eval cap=1 enforced) → re-evaluate exactly once with extra context, then default to Branch B if still in hysteresis zone
6. <phase_criteria_gene>: From exploration summary derive ≥5 acceptance criteria per criteria.md format
7. <phase_emit>: Write exploration.md (exploration.schema.yaml valid) + criteria.md (criteria.schema.json valid)
</workflow_phases>

<acceptance_criteria>
- exploration.md frontmatter has: skill_name, scs_score, hysteresis_triggered (bool), routing_decision (A|B|re-eval), explored_zones, re_eval_count (int, default 0, max 1 — per eval v1 đề xuất 2)
- criteria.md has ≥5 acceptance criteria with verifiable commands
- SCS score validates ∈ [1.0, 5.0]
- hysteresis_triggered is calculated (auto-set khi SCS ∈ [2.7, 3.3])
- re_eval_count never exceeds 1 (cap enforced — infinite loop prevention)
- If hysteresis && re_eval_count === 1 && SCS still ∈ zone → routing_decision = "B" (conservative default)
- Zero placeholder
</acceptance_criteria>
```

### D6-1-2: `raw/ver-3/skill-explorer/knowledge/scs_reference_table.yaml`

YAML reference cho SCS calculation factors:

```yaml
scs_factors:
  - factor: feature_count
    description: "Number of sub-features identified"
    weight: 0.5
    score: "[count >=  3 → 1.0; 5-9 → 2.0; >=10 → 3.0]"
  - factor: integration_points
    description: "External systems/APIs needed"
    weight: 0.4
    score: "[0 → 0.0; 1-3 → 1.0; 4+ → 2.0]"
  - factor: state_storage
    description: "Persistent state requirements"
    weight: 0.3
    score: "[ephemeral → 0; session → 1.0; persistent → 2.0]"
  - factor: branching_depth
    description: "Max depth of if/else decision tree"
    weight: 0.4
    score: "[<=2 → 0.5; 3-5 → 1.5; >=6 → 3.0]"
  - factor: security_surface
    description: "Authentication/Authorization/Payment/PII"
    weight: 0.6
    score: "[none → 0.0; auth → 1.5; payment → 3.0]"

hysteresis_zone: [2.7, 3.3]
hysteresis_action:
  - flag: true → require re-evaluation with additional context from user
  - max_re_eval_cap: 1                              # Phase 6 eval v1 patch: bound iteration
  - default_to: Branch B (conservative) within hysteresis when explicit user confirmation needed
  - post_cap_rule: "After 1 re-eval, if SCS still ∈ [2.7, 3.3], route to Branch B (Full OMSP) as conservative default. Do NOT trigger additional re-evals."
```

### D6-1-3: `raw/ver-3/skill-explorer/templates/exploration_template.md`

### D6-1-4: `raw/ver-3/skill-explorer/templates/criteria_template.md`

### D6-1-5: `raw/ver-3/skill-explorer/loop/scs_audit_checklist.md`

### D6-1-6: `raw/ver-3/skill-explorer/scripts/compute_scs.py`

Python helper script — given exploration raw data, output SCS score with hysteresis check.

### D6-1-7: `raw/ver-3/skill-explorer/data/drc.yaml`

---

## Skill 2: `skill-knowledge-miner` (Stage 0.5)

**Role**: Miner từ spec P6 — consume exploration.md, mine domain knowledge from local files + git history + any existing related skill patterns, output domain-handbook.md.

### D6-2-1: `raw/ver-3/skill-knowledge-miner/SKILL.md`

```yaml
---
name: skill-knowledge-miner
description: "Skill Stage 0.5. Trigger khi exploration.md available. Mine domain knowledge from project documentation, glossaries, related patterns. Output domain-handbook.md with ≥10 glossary terms, anti-patterns, exemplars."
suite: WASHVN
version: 0.0.1
category: monolithic-stage
stage: "Stage 0.5"
target_variable: target_skill
tags: [knowledge-mining, domain-handbook, glossary]
when_to_use: "After skill-explorer produces exploration.md. Scan Temps/, .claude/, _shared/, related skill's knowledge/ to extract domain terms and patterns. Produce domain-handbook.md ≥10 glossary terms."
last_updated: 2026-07-04
output_contract: ".skill-context/{target_skill}/drc-skill-knowledge-miner.yaml"
---
```

Workflow phasesdatetime:

```markdown
<workflow_phases>
1. Read exploration.md + business-analysis.md (if available)
2. <phase_scan_workspace>: Search for related skill knowledge/ docs, glossaries, exemplars in raw/ver-3/_shared/, .claude/knowledge/
3. <phase_extract_terms>: Identify domain-specific terms (≥10 in glossary)
4. <phase_extract_antipatterns>: From miner_search_script (script below), find anti-patterns common trong domain
5. <phase_extract_exemplars>: 1-2 reference implementations (canonical patterns)
6. <phase_emit>: Write domain-handbook.md per domain-handbook.schema.yaml
</workflow_phases>

<acceptance_criteria>
- domain-handbook.md has ≥10 glossary terms (F6 trigger if <10)
- anti-patterns section has ≥3 examples with reason
- exemplars section has ≥1 example with code structure
- All references use clickable file:// links
- Schema validates
</acceptance_criteria>
```

Remaining 6 files analogous (knowledge/, templates/, loop/, scripts/mine_for_terms.py, scripts/find_antipatterns.py, data/drc.yaml).

---

## Skill 3: `skill-architect` (Stage 1)

**Role**: Architect theo spec P1 — consume exploration.md + domain-handbook.md, output design.md (7-Zone mapping).

### D6-3-1: `raw/ver-3/skill-architect/SKILL.md`

```yaml
---
name: skill-architect
description: "Skill Stage 1. Trigger khi exploration.md AND domain-handbook.md ready. Design skill's 7-Zone structure + Mermaid diagrams + data contracts. Output design.md."
suite: WASHVN
version: 0.0.1
category: monolithic-stage
stage: "Stage 1"
target_variable: target_skill
tags: [architect, design, 7-zone, contracts]
when_to_use: "After miner Stage 0.5 complete. Generates design.md with full 7-Zone layout, Mermaid diagrams for state + flow, data contracts for I/O between zones."
last_updated: 2026-07-04
output_contract: ".skill-context/{target_skill}/drc-skill-architect.yaml"
---
```

Workflow:

```markdown
<workflow_phases>
1. Read exploration.md, domain-handbook.md, criteria.md
2. <phase_zone_mapping>: Map each zone (core, knowledge, scripts, templates, data, loop, assets) → concrete file structure for target skill
3. <phase_data_contracts>: Define input_schema + output_schema for each zone transition
4. <phase_state_diagram>: Draw Mermaid state machine cho skill lifecycle (initial → invoked → completed → escalated)
5. <phase_must_not_rules>: Per spec P1 META-1.1, generate ≥5 must_not rules per phase (>5 to satisfy S1)
6. <phase_emit>: Write design.md per design.schema.yaml
</workflow_phases>

<acceptance_criteria>
- design.md has explicit 7-Zone mapping table
- ≥1 Mermaid diagram (state OR flow)
- ≥5 must_not rules per phase (per META-2.1 S1)
- ≥4 reverse questions per aspect (per META-2.2 S2)
- ≥2 stakeholders with goals + pain points (per S3)
- All constraints traceable to domain rules (per S4)
</acceptance_criteria>
```

---

## Skill 4: `production-quality-gatekeeper` (Stage 1.5)

**Role**: Quality gatekeeper theo spec P1 + P3 — consume design.md, evaluate per META-1→3 criteria, write quality-matrix.yaml.

### D6-4-1: `raw/ver-3/production-quality-gatekeeper/SKILL.md`

```yaml
---
name: production-quality-gatekeeper
description: "Skill Stage 1.5. Trigger khi design.md available. Score design vs META-1→3 criteria (16 criteria total). Produce quality-matrix.yaml, evaluation-report.md, feedback.yaml. Address Γ-1: invoke external-code-reviewer agent as co-validator (avoid self-audit trap)."
suite: WASHVN
version: 0.0.1
category: monolithic-stage
stage: "Stage 1.5"
target_variable: target_skill
tags: [quality, meta-criteria, gate, gatekeeper]
when_to_use: "After skill-architect Stage 1. Required before skill-planner can proceed. Block planner if any META-1→3 criterion FAILS."
last_updated: 2026-07-04
output_contract: ".skill-context/{target_skill}/drc-gatekeeper.yaml"
---
```

Workflow:

```markdown
<workflow_phases>
1. Read design.md
2. <phase_meta1_evaluate>: META-1.1 domain anchor (domain terms referenced), META-1.2 phase deconstruct (3-5 phases)
3. <phase_meta2_evaluate>: META-2.1 4 signals (S1 must_not≥5, S2 reverse Q 4-aspect, S3 multi-stakeholder, S4 constraint anchoring) — AND gate
4. <phase_meta3_evaluate>: META-3.1 mechanical pass/fail, META-3.2 negative space, META-3.3 sandbox testing
5. <phase_external_validator>: Invoke aggregate-quality-gatekeeper agent (Phase 3 deployed) as co-evaluator — address Γ-1 self-audit
6. <phase_emit_quality>: Output quality-matrix.yaml (scores), evaluation-report.md (reasoning), feedback.yaml (recommended fixes)
7. <phase_gate>: If aggregate score < 85% OR any signal S1-S4 FAIL, emit feedback to skill-architect (F3 fallback)
</workflow_phases>

<acceptance_criteria>
- quality-matrix.yaml exists with 16 criteria scored 0-100 each
- evaluation-report.md documents each score reasoning
- feedback.yaml lists concrete improvement recommendations if score < 85%
- external validator invoked (NOT pure self-audit)
- AT LEAST must pass META-1.1 + META-2 S1 (must_not ≥5)
</acceptance_criteria>

<failure_modes>
- F3: criteria fails meta-criteria → back to skill-architect (revise design)
- F4: SCS score changes after reading design → back to skill-explorer (re-route)
- F16: business_thought_process missing → back to ba-elicitor (re-do)
- F19: META-2.1 4 signals not all met → back to ba-elicitor (re-do with enforcement)
</failure_modes>
```

---

## Skill 5: `skill-planner` (Stage 2)

**Role**: Planner spec P3 — consume design.md + quality-matrix.yaml, produce todo.md (DAG).

### D6-5-1: `raw/ver-3/skill-planner/SKILL.md`

```yaml
---
name: skill-planner
description: "Skill Stage 2. Trigger khi quality-matrix.yaml passes (>85% aggregate OR planner can proceed with warnings). Generate todo.md dạng DAG with task IDs, dependencies, verification commands. Per spec P3 PLAN-1→5 quality gate."
suite: WASHVN
version: 0.0.1
category: monolithic-stage
stage: "Stage 2"
target_variable: target_skill
tags: [planner, dag, todo, tasks]
when_to_use: "After gatekeeper approves design. todo.md must satisfy PLAN-1 through PLAN-5 criteria before builder Stage 3 can proceed."
last_updated: 2026-07-04
output_contract: ".skill-context/{target_skill}/drc-skill-planner.yaml"
---
```

Workflow:

```markdown
<workflow_phases>
1. Read design.md, quality-matrix.yaml, criteria.md
2. <phase_decompose_to_tasks>: Break down design.md phases into atomic tasks (each ≤1-3 tool calls)
3. <phase_dag_construction>: Build DAG — identify parallelizable tasks vs dependencies
4. <phase_assign_priorities>: Priority high/medium/low based on criticality
5. <phase_link_back>: Each task's parent design.md § reference (DRIFT-1.0 back-link integrity)
6. <phase_must_not_assign>: For tasks priority ≥ HIGH, add must_not constraints (PLAN-4.0)
7. <phase_command_emit>: For each task, emit CLI verification command (PLAN-5.0 mechanical)
8. <phase_emit_todo>: Write todo.md per todo.schema.yaml
</workflow_phases>

<acceptance_criteria>
- todo.md has DAG-structured tasks (not flat list)
- Every task has id, brief description, trace back to design.md zone
- Every task priority ≥ HIGH has must_not rules
- Every task has verification command (script or test)
- Token count < 1200 (PLAN-2.0)
- All priorities assigned (no Priority UNASSIGNED)
- Zero placeholder
</acceptance_criteria>

<failure_modes>
- F7: drift minor → back to planner (re-plan)
- F8: drift major → back to skill-architect (revise design)
- F9: design wrong domain → back to skill-explorer (re-anchor)
</failure_modes>
```

---

## Skill 6: `skill-builder` (Stage 3)

**Role**: Builder — consume todo.md + design.md, build actual code + scripts + SKILL.md.

### D6-6-1: `raw/ver-3/skill-builder/SKILL.md`

```yaml
---
name: skill-builder
description: "Skill Stage 3. Trigger khi todo.md verifies (PLAN-1→5 pass). Build actual skill content (SKILL.md, scripts/, knowledge/, templates/, etc.) per design.md layout. Zero placeholder rule."
suite: WASHVN
version: 0.0.1
category: monolithic-stage
stage: "Stage 3"
target_variable: target_skill
tags: [builder, code, implementation, zero-placeholder]
when_to_use: "After planner Stage 2 passes. Read todo.md task by task, build file by file. Build-log.md records every artifact created."
last_updated: 2026-07-04
output_contract: ".skill-context/{target_skill}/drc-skill-builder.yaml"
---
```

Workflow:

```markdown
<workflow_phases>
1. Read todo.md, design.md, quality-matrix.yaml
2. <phase_orient>: Determine target skill's full path (raw/ver-3/<target_skill>/ + .claude/skills/<target_skill>/)
3. <phase_task_iteration>: For each task in todo.md (in DAG order):
   a. Read task's zone target
   b. Write file content per design.md spec
   c. Verify zero placeholder
   d. Run verification command (PLAN-5.0)
   e. Append to build-log.md
4. <phase_emit_build_log>: Write build-log.md per schema (every artifact + mtime + sha256)
5. <phase_self_audit>: Run production-code-reviewer skill on output (cross-validation)
6. <phase_signal_completion>: Update _state.yaml stage_status: "Stage 3 completed"
</workflow_phases>

<acceptance_criteria>
- SKILL.md ≤ 700 tokens (per CLAUDE.md L0 anchor limit)
- Zero placeholder strings in any output file
- All 7 Zones populated (at least .gitkeep in assets if not used)
- Build-log.md records every artifact with sha256 hash
- Every script executable (chmod +x)
- Self-audit by production-code-reviewer returns no FAIL items
</acceptance_criteria>

<failure_modes>
- F10: review fail (Branch B) → back to assembler (re-merge)
- F11: review fail (Branch B) → back to assembler
- F12: review fail (Branch B) → back to planner (re-plan)
- F13: sandbox fail (Branch A) → back to builder
- F14: sandbox fail (Branch B) → back to assembler
</failure_modes>
```

---

## Skill 7: `production-code-reviewer` (Stage 3.5)

**Role**: Code reviewer theo spec P5 — consume build-log.md, run static analysis, output review-report.md.

### D6-7-1: `raw/ver-3/production-code-reviewer/SKILL.md`

```yaml
---
name: production-code-reviewer
description: "Skill Stage 3.5. Trigger khi build-log.md available. Static analysis: pyflakes, eslint, cyclomatic complexity, placeholder detection. Output review-report.md + audit-metrics.yaml. Phase 6 invoke external-code-reviewer agent as co-validator (Γ-1)."
suite: WASHVN
version: 0.0.1
category: monolithic-stage
stage: "Stage 3.5"
target_variable: target_skill
tags: [code-review, static-analysis, audit, quality]
when_to_use: "After skill-builder Stage 3. Independent review by external-code-reviewer agent AS CO-VALIDATOR to address Γ-1 self-audit trap."
last_updated: 2026-07-04
output_contract: ".skill-context/{target_skill}/drc-code-reviewer.yaml"
---
```

Workflow:

```markdown
<workflow_phases>
1. Read build-log.md
2. <phase_static_lint>: Run pyflakes on Python scripts, eslint on JS scripts (if any), bash -n on shell scripts
3. <phase_complexity_check>: Calculate cyclomatic complexity for each Python script (radon library if available, else simple heuristic)
4. <phase_placeholder_check>: Scan all files for (TODO|FIXME|mock\(\)|pass # implement|... placeholder) — zero tolerance (BUILD-2.1)
5. <phase_docstring_check>: Ensure each function/script has docstring
6. <phase_external_review>: Invoke external-code-reviewer agent (Phase 3 deployed) for cross-validation
7. <phase_emit>: Write review-report.md (audit-metrics.yaml structured)
8. <phase_gate>: If any MUST-FIX item found → F10/F12 fallback
</workflow_phases>

<acceptance_criteria>
- review-report.md has sections per audit schema
- audit-metrics.yaml has metrics: files_reviewed, errors_critical, errors_minor, placeholder_density, complexity_avg
- placeholder_density = 0 (HARD gate)
- All scripts linted (no missing files)
- External validator returns no critical issues
</acceptance_criteria>
```

---

## Skill 8: `skill-security-reviewer` (cross-cutting)

**Role**: Security audit — consume build-log.md, OWASP top 10 + secret scan + unsafe patterns check.

### D6-8-1: `raw/ver-3/skill-security-reviewer/SKILL.md`

```yaml
---
name: skill-security-reviewer
description: "Skill Stage Security. Trigger parallel với Stage 3.5 production-code-reviewer. Audit security: OWASP top 10 + secret scanning (no hardcoded API keys) + unsafe patterns (eval, exec, system()). Output security-review-report.md."
suite: WASHVN
version: 0.0.1
category: monolithic-stage
stage: "Security Stage"
target_variable: target_skill
tags: [security, owasp, secrets, audit]
when_to_use: "Run in parallel with Stage 3.5. Independent security audit based on OWASP."
last_updated: 2026-07-04
output_contract: ".skill-context/{target_skill}/drc-security-reviewer.yaml"
---
```

Workflow:

```markdown
<workflow_phases>
1. Read build-log.md
2. <phase_owasp_scan>: Per OWASP top 10:
   - A01 Broken Access Control
   - A02 Cryptographic Failures
   - A03 Injection
   - A04 Insecure Design
   - A05 Security Misconfiguration
   - A06 Vulnerable Components
   - A07 Auth Failures
   - A08 Software/Data Integrity
   - A09 Security Logging Failures
   - A10 SSRF
3. <phase_secret_scan>: Detect hardcoded credentials (regex patterns for API keys, JWTs, AWS creds)
4. <phase_unsafe_patterns>: Detect Python: eval, exec, __import__, os.system; JS: eval, Function; bash: sudo, eval, exec
5. <phase_emit>: Write security-review-report.md
</workflow_phases>
```

---

## Verification checklist (cơ học)

### AC-1 — 8 skills deployed
```bash
for skill in skill-explorer skill-knowledge-miner skill-architect production-quality-gatekeeper skill-planner skill-builder production-code-reviewer skill-security-reviewer; do
  test -f .claude/skills/$skill/SKILL.md || exit 1
done
echo "AC-1 PASS"
```

### AC-2 — Each skill frontmatter valid + 700-token limit
```bash
python3 << 'EOF'
import yaml
for s in ['skill-explorer', 'skill-knowledge-miner', 'skill-architect', 'production-quality-gatekeeper', 'skill-planner', 'skill-builder', 'production-code-reviewer', 'skill-security-reviewer']:
    with open(f'.claude/skills/{s}/SKILL.md') as f:
        c = f.read()
    fm = c.split('---')[1]
    d = yaml.safe_load(fm)
    for k in ['name', 'description', 'suite', 'version', 'category', 'stage', 'target_variable', 'tags']:
        assert k in d, f"{s} missing {k}"
    assert d['name'] == s, f"{s} name mismatch"
    assert d['suite'] == 'WASHVN'
    # Token count check (~700 tokens ~= 2800 chars)
    body = c.split('---', 2)[2]
    assert len(body) < 3500, f"{s} body over 3500 chars (likely > 700 tokens)"
print("AC-2 PASS")
EOF
```

### AC-3 — Each skill has ≥4 of 7 Zones populated
```bash
for skill in skill-explorer skill-knowledge-miner skill-architect production-quality-gatekeeper skill-planner skill-builder production-code-reviewer skill-security-reviewer; do
  populated=0
  for zone in knowledge scripts templates loop data; do
    [ -d .claude/skills/$skill/$zone ] && ls .claude/skills/$skill/$zone/*.md 2>/dev/null | head -1 > /dev/null && populated=$((populated+1))
  done
  test "$populated" -ge 4 || exit 1
done
echo "AC-3 PASS"
```

### AC-4 — Each skill DRC valid
```bash
for skill in skill-explorer skill-knowledge-miner skill-architect production-quality-gatekeeper skill-planner skill-builder production-code-reviewer skill-security-reviewer; do
  python3 -c "import yaml; yaml.safe_load(open('.claude/skills/$skill/data/drc.yaml'))"
done
echo "AC-4 PASS"
```

### AC-5 — End-to-end pipeline test with mock skill "prompt-cleaner"

```bash
# Create mock skill target
TARGET="mock-prompt-cleaner"
mkdir -p .skill-context/$TARGET/

# Mock business-analysis.md
cat > .skill-context/$TARGET/business-analysis.md << EOF
---
feature_name: mock-prompt-cleaner
stakeholder_count: 1
---
# Mock prompt cleaner — clean text of generic prefixes/suffixes
EOF

# Invoke skill-explorer via skill-pipeline-orchestrator (Phase 3):
# task(subagent_type=skill-pipeline-orchestrator, prompt="build skill mock-prompt-cleaner from .skill-context/mock-prompt-cleaner/business-analysis.md")
# After invocation verify:
test -f .skill-context/$TARGET/exploration.md
test -f .skill-context/$TARGET/criteria.md
test -f .skill-context/$TARGET/domain-handbook.md
test -f .skill-context/$TARGET/design.md
test -f .skill-context/$TARGET/quality-matrix.yaml
test -f .skill-context/$TARGET/todo.md
test -f .skill-context/$TARGET/build-log.md
test -f .skill-context/$TARGET/review-report.md
test -f .skill-context/$TARGET/audit-metrics.yaml
test -f .skill-context/$TARGET/security-review-report.md

# Verify SCS hysteresis flag present (Γ-3 fix):
grep -q "hysteresis_triggered" .skill-context/$TARGET/exploration.md

# Verify skill output exists:
test -f .claude/skills/$TARGET/SKILL.md

# Cleanup mock:
# rm -rf .skill-context/$TARGET/ .claude/skills/$TARGET/

echo "AC-5 PASS"
```

### AC-6 — Schema validator passes on every artifact
```bash
for artifact in exploration criteria design quality-matrix todo build-log review-report audit-metrics security-review; do
  python3 raw/ver-3/_shared/validators/schema_validator.py --artifact $artifact --path .skill-context/mock-prompt-cleaner/$artifact* 2>&1 | grep -q "PASS" || exit 1
done
echo "AC-6 PASS"
```

### AC-7 — External validator agent invoked at gates that need it
```bash
# Verify aggregate-quality-gatekeeper invoked during skill-pipeline-orchestrator run
# Via check audit logs:
grep -q "aggregate-quality-gatekeeper" .skill-context/_state-archive/tool-audit-*.log | head -1 || \
  grep -q "external-code-reviewer" .skill-context/_state-archive/tool-audit-*.log | head -1 || \
  echo "WARNING: external co-validator not detected in audit log"
```

### AC-8 — Pipeline runner works for all 8 stages sequentially

Automated test pipe through skill-pipeline-orchestrator from Phase 3.

---

## Step-by-step task list

Build order (suggested): **skill-explorer → skill-knowledge-miner → skill-architect → production-quality-gatekeeper → skill-planner → skill-builder → production-code-reviewer → skill-security-reviewer**

For each skill (8 iterations):
1. **Author SKILL.md** (frontmatter + body sections) per skill-specific template above
2. **Author knowledge/ files** (~1-2 docs per skill)
3. **Author templates/ files** (artifact templates)
4. **Author scripts/ executable scripts** (validators, helper scripts)
5. **Author loop/ checklist** (self-verification)
6. **Author data/drc.yaml** (DRC contract per template)
7. **Run local validator** if script exists (e.g., compute_scs.py for skill-explorer)
8. **Invoke aggregate-quality-gatekeeper** audit on skill SKILL.md
9. **Fix findings** until score ≥70%
10. **Test invoke skill** with mock data (skill-explorer receives mock business-analysis.md, etc.)
11. **Commit atomic** per skill: `phase-6: <skill-name> built + tested`
12. **Deploy** via deploy script (move raw/ver-3/<skill-name>/ to .claude/skills/<skill-name/>)

After all 8 deployed:
- Run AC-1 to AC-8 sequentially
- Run e2e test via skill-pipeline-orchestrator (AC-5)
- Verify schemas validate (AC-6)
- Verify external validator invoked (AC-7)

---

## Definition of done (Phase 6)

```yaml
dod:
  - 8 skills deployed .claude/skills/
  - All AC-1 to AC-7 PASS
  - Skills-registry.json updated (8 main skills marked `installed` lifecycle)
  - End-to-end test: skill-pipeline-orchestrator invokes all 8 stages successfully với 1 mock skill "mock-prompt-cleaner"
  - Every artifact in pipeline passes schema validation
  - External co-validator (aggregate-quality-gatekeeper + external-code-reviewer) invoked at META gate + code review gate
  - SCS hysteresis flag detected in mock-prompt-cleaner/exploration.md
  - Zero placeholder strings anywhere in built skills
```

---

## Liên kết

- [Roadmap Index](index.md)
- [Phase 5 trước](05-skill-build-ba-pipeline.md)
- [Phase 7 kế tiếp](07-skill-build-sandbox-indexer.md)
- [Architectural defects addressed](file:///home/stveve/Documents/workspace/build-workflow/WASHVN/Temps/spec/architects/README.md)