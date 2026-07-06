# Phase 3 — Agent Foundation Build

> **Order:** 4th phase | **Estimated effort:** M-L (medium-large) | **Predicted duration:** 2-3 sessions
> **Depends on:** Phase 0, Phase 1, Phase 2
> **Downstream:** Phase 5, 6, 7 (Skills), Phase 8 (Integration)
> **Architectural defects addressed:** Γ-1 (self-referential blindness — agents cần external validator), Γ-7 (escalation recursion — giới hạn depth)

## Mục địch

Phase 3 xây dụng **4 production agents** tại `.claude/agents/` bằng cách dụng subagent-forge làm reference pattern. Đây là infrastructure layer cho Phase 5-7 — khi skills build, các agents này sẽ act là:
- **Orchestrator** cho skill build pipeline
- **Aggregate quality gatekeeper** (như spec Phase P1 yêu cầu)
- **BA-pipeline runner** tự kích 3 BA skills nối tiếp nhau
- **Production code reviewer agent** (external ground-truth cho Γ-1)

Phase 3 là tới vị trí bắt buộc đã có Phase 1 (knowledge docs) để subagent-forge reference đầy đủ.

---

## Prerequisites

```yaml
prerequisites:
  - Phase 0, 1, 2 done
  - subagent-forge agent invokeable và tạo được agent mới (verify bằng cách thử invoke nó)
  - 7 knowledge docs được refresh authored Phase 1
  - subagent-forge references không còn dangling paths
```

---

## Design Principle

```yaml
agent_design_principles:
  - "Mỗi agent phải tuân chặt subagent-forge 4-evaluator pipeline ≥ APPROVED_FOR_REVIEW"
  - "Mỗi agent phải reference tất cả 7 knowledge docs via retrieved_docs tag"
  - "Mỗi agent phải có ≥ 3 inline hooks (PreToolUse + PostToolUse) trừ trường hợp justify standalone"
  - "Mỗi agent chỉ có phụ thuộc skills-phase-5-7-không-built-yet được declare trong frontmatter `skills:` field nhưng phải NOT CIRCULAR-DEPENDENCY skillPhase (e.g., agent ba-pipeline-runner dependent trên skill ba-elicitor — cần phase 5 build skill trước)"
  - "Output contract của mỗi agent phải khai báo artifact paths trong .skill-context/"
```

---

## Deliverables (4 agents)

### D3-1: `.claude/agents/_staging/skill-pipeline-orchestrator.md`

Agent orchestration cho skill build pipeline — nhận user request, chạy 8-stage pipeline.

**Frontmatter keys**:
```yaml
name: skill-pipeline-orchestrator
description: "Use PROACTIVELY khi user yêu cầu build, rebuild, hoặc maintain một skill. Trigger phrases: 'build skill <name>', 'rebuild skill <name>', 'maintain skill'. Orchestrate 11 skills theo 8-Stage pipeline (Phase P0-P7 từ spec)."
model: opus
tools: [Read, Write, Glob, Grep, Task, TodoWrite]
permissionMode: default
skills: []   # Phase 5-7 sẽ thêm skills)
mcpServers: []
hooks:
  PreToolUse:
    - matcher: "Write|Edit"
      hook: |
        # Block writes outside _staging/ + .skill-context/
        INPUT=$(cat)
        FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')
        [ -z "$FILE_PATH" ] && exit 0
        if [[ ! "$FILE_PATH" =~ \.claude/agents/_staging/|\.skill-context/|Temps/spec/roadmaps/|docs/context-to-work/ ]] && [[ "$FILE_PATH" =~ \.claude/ ]]; then
          echo "BLOCKED: orchestrator chỉ được phép viết vào _staging/, .skill-context/, roadmaps/, docs/" >&2
          exit 2
        fi
    - matcher: "Task"
      hook: |
        # Block recursive orchestrator spawn (max depth = 1)
        INPUT=$(cat)
        SUB_TYPE=$(echo "$INPUT" | jq -r '.tool_input.subagent_type // empty')
        if [ "$SUB_TYPE" = "skill-pipeline-orchestrator" ]; then
          echo "BLOCKED: recursive orchestrator spawn forbidden (max depth = 1)" >&2
          exit 2
        fi
```

**System prompt structure (8 sections per subagent-forge output contract)**:

1. `<instructions>` — identity statement (~80 words): "You are skill-pipeline-orchestrator, agent cho Skill Lab WASHVN. Bạn read user request, parse features, invoke appropriate 8-stage skills theo 8-stage pipeline (from spec architecture.md), aggregate outputs từ .skill-context/. Bạn không write skill content — chỉ orchestrate skills."
2. `<safety_contract>` — non-negotiable:
   - Chỉ invoke skills via `Task` calls — không trực tiếp write skill content
   - Tuân thủ_CAT protocol Phase 0-7 sequence
   - Block recursion (block on `subagent_type: skill-pipeline-orchestrator`)
3. `<workflow_phases>` — 8 phases correspond tới 8 stages:
   - Stage 0 → invoke `skill-explorer`
   - Stage 0.5 → invoke `skill-knowledge-miner`
   - Stage 1 → invoke `skill-architect`
   - Stage 1.5 → invoke `production-quality-gatekeeper`
   - Stage 2 → invoke `skill-planner`
   - Stage 3 → invoke `skill-builder`
   - Stage 3.5 → invoke `production-code-reviewer` + `skill-security-reviewer`
   - Stage 4 → invoke `sandbox-tester`
   - Stage 5 → invoke `indexer`
4. `<knowledge_anchors>` — `<retrieved_docs>` reference 7 knowledge docs (data:/phase 1 authored)
5. `<input_contract>` — nhận từ user: `{skill_name, query_tipo: build|rebuild|maintain}`
6. `<output_contract>` — `.skill-context/{skill_name}/_orchestration_log.md` với timeline, gate results
7. `<examples>` — trivial skill "hello-world" đi qua pipeline (mock example)
8. `<failure_modes>` — fallback paths F1-F9 với brief description

### D3-2: `.claude/agents/_staging/aggregate-quality-gatekeeper.md`

Agent quality aggregator — nhận design.md + criteria.md từ Skill Pipeline, chấm điểm theo META-1→3 criteria, sinh quality-matrix.yaml.

特质 khác biệt với skill `production-quality-gatekeeper` (Phase 6 build):
- Skill = pure verification algorithm (đọc design.md, compare với criteria, chấm)
- Agent = external validator (gọi tới skills+cyan+, không phụ thuộc standard flow)

```yaml
name: aggregate-quality-gatekeeper
description: "Use khi user yêu cầu hoặc skill-pipeline-orchestrator invokes để quality check a skill design. Trigger: 'evaluate design for <skill>', aggregate META-1 to 3 criteria. Architectural defect Γ-1 fix: external LLM validator thay vì self-audit."
model: sonnet   # Opus thiết quá nhiều tokens cho quality check
tools: [Read, Glob, Grep, Task]
permissionMode: default
skills: [production-quality-gatekeeper]  # Phase 6 sẽ build
hooks:
  PreToolUse:
    - matcher: "Write"
      hook: |
        # Chỉ Write vào .skill-context/
        INPUT=$(cat)
        FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')
        [ -z "$FILE_PATH" ] && exit 0
        if [[ ! "$FILE_PATH" =~ \.skill-context/ ]]; then
          echo "BLOCKED: gatekeeper chỉ write vào .skill-context/" >&2
          exit 2
        fi
```

**System prompt sections**:

1. Identity: external quality validator
2. Safety contract: chỉ verify, không modify design
3. Workflow:
   - Phase A: read design.md + criteria.md
   - Phase B: run 4 META-2.1 signal checks (S1 must_not ≥ 5, S2 reverse Q ≥ 4-aspect, S3 multi-stakeholder, S4 constraint anchoring)
   - Phase C: run META-1.1 domain anchor + META-1.2 phase deconstruct checks
   - Phase D: aggregate score → emit quality-matrix.yaml + evaluation-report.md
4. Retrieved_docs: 7 knowledge docs
5. Input contract: design.md + criteria.md paths
6. Output contract: `.skill-context/{skill}/quality-matrix.yaml`, `.skill-context/{skill}/evaluation-report.md`, `.skill-context/{skill}/feedback.yaml`
7. Examples: PASS example + FAIL example each ~20 dòng
8. Failure modes: criteria files missing → exit with error, don't fabricate

### D3-3: `.claude/agents/_staging/ba-pipeline-runner.md`

Agent chuyên nghiệp cho BA pipeline (Stage -1 → -0.5 → -0.2): ba-elicitor → ba-analyst → ba-synthesizer.

```yaml
name: ba-pipeline-runner
description: "Use PROACTIVELY khi user cần elicite business requirements cho một feature. Trigger: 'elicit business for <feature>', 'business requirements for <feature>'. Orchestrate 3 BA skills (elicitor → analyst → synthesizer)."
model: opus  # BA elicitation nặng về deep reasoning
tools: [Read, Task, Write]
permissionMode: default
skills: [ba-elicitor, ba-analyst, ba-synthesizer]  # Phase 5 build
hooks:
  PreToolUse:
    - matcher: "Write"
      hook: |
        # Chỉ write vào .skill-context/{feature}/ba-*/
        INPUT=$(cat)
        FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')
        [ -z "$FILE_PATH" ] && exit 0
        if [[ ! "$FILE_PATH" =~ \.skill-context/.*/ba-(elicitor|analyst|synthesizer)/ ]]; then
          echo "BLOCKED: ba-pipeline-runner chỉ write vào .skill-context/{feature}/ba-*" >&2
          exit 2
        fi
    - matcher: "Task"
      hook: |
        # Block recursive spawn + Require block_type matching ba skills
        INPUT=$(cat)
        SUB_TYPE=$(echo "$INPUT" | jq -r '.tool_input.subagent_type // empty')
        if [ "$SUB_TYPE" = "ba-pipeline-runner" ]; then
          echo "BLOCKED: recursive ba-pipeline-runner forbidden" >&2
          exit 2
        fi
```

**Workflow**:
1. Invoke `skill ba-elicitor` (Phase 5 xây) → elicite thông tin user, output `elicitation-report.md`
2. Invoke `skill ba-analyst` → phân tích elicitation report, output `analysis-report.md`
3. Invoke `skill ba-synthesizer` → hợp latest analysis, output `business-analysis.md`
4. Update `.skill-context/{feature}/_ba_pipeline_state.yaml` với lifecycle status

### D3-4: `.claude/agents/_staging/external-code-reviewer.md`

**Đây là external ground-truth validator** address defect Γ-1 — LLM self-audit mặc cả.

Cần một "fresh-eyes" reviewer không cùng context với builder:
- Khác model (e.g., haiku cho cheap check, sonnet cho medium, hoặc invoke Codex CLI.external nếu có)
- Khác system prompt (không biết tri thức tác giả)
- Khác tools (Read-only + Bash chỉ cho static analysis)

```yaml
name: external-code-reviewer
description: "Use POST build để catch 'valid-looking but semantically wrong' code (PASS-form FAIL-meaning). Independent reviewer không same-context như Builder, address LLM self-referential blindness."
model: sonnet
tools: [Read, Bash, Grep, Glob]
permissionMode: default
skills: [production-code-reviewer]  # Use skill's audit-metrics.yaml schema
hooks:
  PreToolUse:
    - matcher: "Write|Edit"
      hook: |
        # External reviewer KHÔNG modify code — chỉ emit review-report.md
        INPUT=$(cat)
        FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')
        [ -z "$FILE_PATH" ] && exit 0
        if [[ "$FILE_PATH" =~ \.claude/skills/|raw/ver-3/ ]] && [[ ! "$FILE_PATH" =~ review-report.md|audit-metrics.yaml ]]; then
          echo "BLOCKED: external reviewer chỉ write review reports, không modify source" >&2
          exit 2
        fi
    - matcher: "Bash"
      hook: |
        # External reviewer Bash chỉ cho static analysis (pyflakes, eslint, complexity)
        INPUT=$(cat)
        CMD=$(echo "$INPUT" | jq -r '.tool_input.command // empty')
        if echo "$CMD" | grep -qE "(run|execute|python|node|cargo)"; then
          echo "BLOCKED: external reviewer không execute code — chỉ static analysis" >&2
          exit 2
        fi
```

Workflow:
1. Read `raw/ver-3/<skill>/` SKILL.md + scripts/ + knowledge/
2. Run static analysis: `pyflakes`, `eslint` (nếu JS), `--check` complexity metrics
3. Compare with criteria.md và criteria defined trước (NFRs từ exploration.md)
4. Emit `review-report.md` (different from skill's review-report.md produced by production-code-reviewer skill)
5. Output: `audit-metrics.yaml` (reusable structured metrics)

**Anti-pattern / contract**: Agent này phải NOT biết design.md (architect's reasoning). Filter forward refs to validate WITHOUT context bias.

---

## Verification checklist (cơ học)

### AC-1 — 4 agent files created at staging area
```bash
for agent in skill-pipeline-orchestrator aggregate-quality-gatekeeper ba-pipeline-runner external-code-reviewer; do
  test -f .claude/agents/_staging/$agent.md || exit 1
done
echo "AC-1 PASS"
```

### AC-2 — Frontmatter YAML parses + has required fields
```bash
python3 << 'EOF'
import yaml
agents = ['skill-pipeline-orchestrator', 'aggregate-quality-gatekeeper', 'ba-pipeline-runner', 'external-code-reviewer']
for a in agents:
    with open(f'.claude/agents/_staging/{a}.md') as f:
        c = f.read()
    fm = c.split('---')[1]
    data = yaml.safe_load(fm)
    for req in ['name', 'description', 'model', 'tools', 'permissionMode']:
        assert req in data, f"{a} missing {req}"
    assert data['permissionMode'] != 'bypassPermissions', f"{a} dangerous bypassPermissions"
print("AC-2 PASS")
EOF
```

### AC-3 — Reference of 7 knowledge docs exists in each agent
```bash
for agent in skill-pipeline-orchestrator aggregate-quality-gatekeeper ba-pipeline-runner external-code-reviewer; do
  count=$(grep -c "claude/knowledge/agents/" .claude/agents/_staging/$agent.md)
  test "$count" -ge 7 || exit 1
done
echo "AC-3 PASS"
```

### AC-4 — Inline hooks block recursive + gate paths
```bash
# Verify each agent has at least 1 blocker hook referencing exit 2:
for agent in skill-pipeline-orchestrator aggregate-quality-gatekeeper ba-pipeline-runner external-code-reviewer; do
  grep -q "exit 2" .claude/agents/_staging/$agent.md || exit 1
done
echo "AC-4 PASS"
```

### AC-5 — Subagent-forge 4-evaluator passes
```bash
# Invoke subagent-forge to evaluate each agent → archive eval-report
# (Thực tế invoke — sẽ chạy 4 parallel Task calls per agent)
# Manual tại Phase 3:
# invoke: task subagent_type=general-purpose prompt="evaluate .claude/agents/_staging/skill-pipeline-orchestrator.md per subagent-forge §Multi-Eval Pipeline"
# ... check JSON output aggregate verdict
# Currently manual tại phase 3; Phase 8 sẽ automate
echo "AC-5 NEEDED_MANUAL — invoke subagent-forge on each agent & verify APPROVED_FOR_REVIEW aggregate verdict"
```

### AC-6 — Output contract section exists in each agent
```bash
for agent in skill-pipeline-orchestrator aggregate-quality-gatekeeper ba-pipeline-runner external-code-reviewer; do
  grep -q "<output_contract>" .claude/agents/_staging/$agent.md || exit 1
done
echo "AC-6 PASS"
```

### AC-7 — Skills referenced exist (or will exist — Phase 5/6)
```bash
python3 << 'EOF'
import yaml, os
agents = ['skill-pipeline-orchestrator', 'aggregate-quality-gatekeeper', 'ba-pipeline-runner', 'external-code-reviewer']
for a in agents:
    with open(f'.claude/agents/_staging/{a}.md') as f:
        c = f.read()
    fm = c.split('---')[1]
    data = yaml.safe_load(fm)
    skills = data.get('skills', [])
    if skills:
        for s in skills:
            # Phase 5/6 build skills. At runtime, check skill dir exists tại raw/ver-3/
            # At Phase 3, scaffolded only by Phase 0
            if not os.path.isdir(f'raw/ver-3/{s}'):
                print(f"WARNING: {a} skills:{s} not yet built — Phase 5 or 6 must build")
print("AC-7 PASS — no errors")
EOF
```

### AC-8 — No `bypassPermissions` mode

```bash
grep -q "permissionMode: bypassPermissions" .claude/agents/_staging/*.md && exit 1 || echo "AC-8 PASS"
```

---

## Step-by-step task list

1. **Invoke subagent-forge to design skill-pipeline-orchestrator** — pass rich requirements: 8-stage pipeline orchestration, block recursion. subagent-forge will produce staging file + 4-evaluator report. → commit `phase-3: skill-pipeline-orchestrator agent staged`

2. **Review subagent-forge output** — verify APPROVED_FOR_REVIEW aggregate verdict. Fix any NEEDS_FIX items. Iterate until verdict ≥ APPROVED_FOR_REVIEW.

3. **Deploy orchestrator agent** — user types `deploy skill-pipeline-orchestrator` → move staging to runtime. → commit `phase-3: orchestrator agent deployed`

4. **Invoke subagent-forge for aggregate-quality-gatekeeper** — pass requirements: external validator per Γ-1 fix, sonnet model (cheaper), only writes to .skill-context/, references META-1→3 criteria. → commit `phase-3: aggregate-quality-gatekeeper agent staged`

5. **Review + deploy aggregate-quality-gatekeeper** — verify ≥ APPROVED_FOR_REVIEW, deploy via `deploy aggregate-quality-gatekeeper`. → commit `phase-3: gatekeeper agent deployed`

6. **Invoke subagent-forge for ba-pipeline-runner** — requirements: orchestrate 3 BA skills, only writes ba-* dirs, block recursion. → commit `phase-3: ba-pipeline-runner agent staged`

7. **Review + deploy ba-pipeline-runner** — deploy via `deploy ba-pipeline-runner`. → commit `phase-3: ba-pipeline runner agent deployed`

8. **Invoke subagent-forge for external-code-reviewer** — requirements: Γ-1 fix agent, sonnet model, block direct edits to source code, block code execution (static analysis only). → commit `phase-3: external-code-reviewer agent staged`

9. **Review + deploy external-code-reviewer** — deploy via `deploy external-code-reviewer`. → commit `phase-3: external reviewer agent deployed`

10. **Run full AC-1 to AC-8** — fix any failures, re-deploy if needed.

11. **Update subagent-forge workspce_tree.md** — append 4 new entries to file routing map.

12. **Author Phase 3 summary doc** — `docs/context-to-work/foundation-bootstrap/phase-3-summary.2026-07-04.md` documenting all deployed agents, costs, notes.

---

## Definition of done (Phase 3)

```yaml
dod:
  - 4 agents deployed tại .claude/agents/ runtime
  - All 4 agents PASS subagent-forge 4-evaluator aggregate verdict ≥ APPROVED_FOR_REVIEW
  - workspce_tree.md updated với 4 new agent entries
  - Each agent có ≥3 cross-references tới 7 knowledge docs
  - Each agent có ≥1 blocking hook (exit 2)
  - No `permissionMode: bypassPermissions` anywhere
  - Each agent có <output_contract> section with concrete artifact paths
  - Phase 3 summary doc archived per `context-before-fix` pattern
```

---

## Liên kết

- [Roadmap Index](index.md)
- [Phase 2 trước](02-hook-framework.md)
- [Phase 4 kế tiếp](04-skill-pipeline-scaffold.md)
- [Subagent-forge reference](file:///home/stveve/Documents/workspace/build-workflow/WASHVN/.claude/agents/subagent-forge.md)
- [Examples reference doc](file:///home/stveve/Documents/workspace/build-workflow/WASHVN/.claude/knowledge/agents/examples.md)