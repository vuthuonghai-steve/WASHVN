# Phase 3 — Agent Foundation Build

> **Order:** 4th phase | **Estimated effort:** M-L (medium-large) | **Predicted duration:** 2-3 sessions
> **Depends on:** Phase 0, Phase 1, Phase 2
> **Downstream:** Phase 5, 6, 7 (Skills), Phase 8 (Integration)
> **Architectural defects addressed:** Γ-1 (self-referential blindness — agents cần external validator), Γ-7 (escalation recursion — giới hạn depth)

## Mục địch

Phase 3 xây dụng **8 specialized agents** (từ thiết kế concentrated 4-agent gốc) tại `.claude/agents/` bằng cách dụng subagent-forge làm reference pattern, theo nguyên tắc **1-role-per-agent** để tránh LLM overload (Λ-1 Role Confation). Đây là infrastructure layer cho Phase 5-7 — khi skills build, các agents này sẽ act là:
- **Orchestrator** (pipeline) cho skill build pipeline — giữ orchestration only
- **Design validator** + **Quality scorer** (tách từ aggregate gatekeeper) — schema check + META scoring riêng
- **BA-pipeline runner** — tự kích 3 BA skills nối tiếp nhau
- **External code reviewer** — external ground-truth cho Γ-1
- **User-knowledge-ingestor** (MỚI) — nhận + parse tài liệu từ user suốt build
- **Drift detector** — Stage 2.5 plan-design alignment, bị bỏ sót trong thiết kế gốc
- **Branch orchestrator** (TÙY CHỌN) — Branch B parallel coordination

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
  - "1-role-per-agent (architecture doc §1 role_invariant): mỗi agent có ĐÚNG 1 primary_responsibility, không dồn nhiều role → tránh Λ-1 Role Overload"
  - "Mỗi agent phải tuân chặt subagent-forge 4-evaluator pipeline ≥ APPROVED_FOR_REVIEW"
  - "Mỗi agent phải reference tất cả 7 knowledge docs via retrieved_docs tag"
  - "Mỗi agent phải có ≥ 3 inline hooks (PreToolUse + PostToolUse) trừ trường hợp justify standalone"
  - "Mỗi agent chỉ có phụ thuộc skills-phase-5-7-không-built-yet được declare trong frontmatter `skills:` field nhưng phải NOT CIRCULAR-DEPENDENCY skillPhase (e.g., agent ba-pipeline-runner dependent trên skill ba-elicitor — cần phase 5 build skill trước)"
  - "Output contract của mỗi agent phải khai báo artifact paths trong .skill-context/"
  - "Model tier justify theo task complexity (architecture doc §5 Λ-10 fix): opus=deep reasoning, sonnet=operational, haiku=classification-only"
  - "Agent có state_ledger_validation_hook=true bắt buộc PostToolUse hook validate YAML schema (architecture doc §3-bis)"
```

---

## Deliverables (8 agents)

### D3-1: `.claude/agents/_staging/pipeline-orchestrator.md`

Agent orchestration cho skill build pipeline — nhận user request, chạy 8-stage pipeline. **Điều phối (orchestration) only — không thực thi nội dung nghiệp vụ.** [revised per Λ-10 fix: model opus→sonnet vì orchestration là mechanical task]

**Frontmatter keys**:
```yaml
name: pipeline-orchestrator
description: "Use PROACTIVELY khi user yêu cầu build, rebuild, hoặc maintain một skill. Trigger phrases: 'build skill <name>', 'rebuild skill <name>', 'maintain skill'. Orchestrate 8-stage pipeline — dispatch stage executors via handoff manifest. NOT responsible for quality scoring, design validation, or BA elicitation."
model: sonnet  # [v0.0.2] orchestration là mechanical dispatch — opus gây Λ-10 lãng phí deep-reasoning cho mechanical task
justification: "Orchestration = đọc state ledger + dispatch agent next + kiểm handoff manifest. Sonnet pattern matching đủ xử lý, opus lãng phí latency + token budget."
tools: [Read, Task, TodoWrite]
permissionMode: default
skills: []   # Phase 5-7 sẽ thêm skills
mcpServers: []
state_ledger_validation_hook: true  # §3-bis architecture doc
hooks:
  PreToolUse:
    - matcher: "Write|Edit"
      hook: |
        # Block writes outside designated zones
        INPUT=$(cat)
        FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')
        [ -z "$FILE_PATH" ] && exit 0
        if [[ "$FILE_PATH" =~ \.claude/agents/ ]] && [[ ! "$FILE_PATH" =~ \.claude/agents/_staging/ ]] && [[ ! "$FILE_PATH" =~ \.skill-context/.*_state_ledger ]]; then
          echo "BLOCKED: orchestrator chỉ write _staging/ + _state_ledger.yaml" >&2
          exit 2
        fi
    - matcher: "Task"
      hook: |
        # Block recursive orchestrator spawn (max depth = 1)
        INPUT=$(cat)
        SUB_TYPE=$(echo "$INPUT" | jq -r '.tool_input.subagent_type // empty')
        if [ "$SUB_TYPE" = "pipeline-orchestrator" ]; then
          echo "BLOCKED: recursive orchestrator spawn forbidden (max depth = 1)" >&2
          exit 2
        fi
  PostToolUse:
    - matcher: "Write|Edit"
      hook: ".claude/hooks/validate-state-ledger.sh"  # validate schema + YAML parse
```

**System prompt structure (8 sections per subagent-forge output contract)**:

1. `<instructions>` — identity statement (~80 words): "You are pipeline-orchestrator, agent cho Skill Lab WASHVN. Bạn read user request, parse features, invoke appropriate stage executors via handoff manifest theo 8-stage pipeline (from source architecture.md), aggregate outputs từ .skill-context/. Bạn không write skill content — chỉ orchestrate skills via Task dispatch."
2. `<safety_contract>` — non-negotiable:
   - Chỉ invoke skills via `Task` calls — không trực tiếp write skill content
   - Tuân thủ_CAT protocol Phase 0-7 sequence
   - Block recursion (block on `subagent_type: pipeline-orchestrator`)
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

### D3-2: `.claude/agents/_staging/design-validator.md`

Agent schema/contract validation — kiểm tra design.md có đủ 7-Zone, data contracts, semantic anchors. **Mechanical validation only — không chấm META quality.**

```yaml
name: design-validator
description: "Use PROACTIVELY bởi pipeline-orchestrator hoặc user request. Validate design.md schema completeness: 7-Zone, data contracts, semantic anchors. NOT META scoring (chuyển quality-scorer)."
model: sonnet
justification: "Schema validation = pattern matching + checklist. Sonnet đủ tốc độ, không cần opus."
tools: [Read, Glob, Grep]
permissionMode: default
skills: []
hooks:
  PreToolUse:
    - matcher: "Write"
      hook: |
        INPUT=$(cat)
        FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')
        [ -z "$FILE_PATH" ] && exit 0
        if [[ ! "$FILE_PATH" =~ \.skill-context/{skill}/design-valid ]]; then
          echo "BLOCKED: design-validator chỉ write .skill-context/{skill}/design-valid*" >&2
          exit 2
        fi
```

**System prompt sections**:
1. Identity: schema/contract validator — NOT quality scorer
2. Safety contract: chỉ mechanical check, không opine về design quality
3. Workflow: Read design.md → validate 7-Zone completeness → check data contracts → emit design-validation-report.yaml
4. Retrieved_docs: 7 knowledge docs
5. Input contract: `design.md`, `criteria.md`
6. Output contract: `.skill-context/{skill}/design-validation-report.yaml` (PASS/FAIL schema checklist)
7. Failure modes: criteria.md missing → PASS with warning

### D3-3: `.claude/agents/_staging/quality-scorer.md`

Agent META-1→3 scoring — semantic depth, reverse Q, multi-stakeholder, mechanical verify. **Deep reasoning task — dùng opus.** [split từ aggregate-gatekeeper gốc với Λ-10 fix: upgrade sonnet→opus cho META scoring]

```yaml
name: quality-scorer
description: "Use PROACTIVELY bởi pipeline-orchestrator sau khi design-validator PASS. Score design quality theo META-1→3 criteria: META-1.1 domain anchor, META-2.1 semantic depth, META-3.1 mechanical. Output quality-matrix.yaml."
model: opus
justification: "META scoring cần deep reasoning (reverse Q, multi-stakeholder, negation density) — sonnet gây shallow validation (Λ-10). Opus bắt buộc."
tools: [Read, Glob, Grep]
permissionMode: default
skills: [production-quality-gatekeeper]  # Phase 6 build — skill reference
hooks:
  PreToolUse:
    - matcher: "Write"
      hook: |
        INPUT=$(cat)
        FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')
        [ -z "$FILE_PATH" ] && exit 0
        if [[ ! "$FILE_PATH" =~ \.skill-context/{skill}/quality- ]]; then
          echo "BLOCKED: quality-scorer chỉ write .skill-context/{skill}/quality-*" >&2
          exit 2
        fi
```

**System prompt sections**:
1. Identity: META quality scorer — external validator (Γ-1 fix)
2. Safety contract: CHỈ đánh giá quality, không sửa design
3. Workflow:
   - Phase A: read design.md, criteria.md, design-validation-report.yaml (đã PASS)
   - Phase B: META-2.1 signal checks (S1 must_not ≥ 5, S2 reverse Q ≥ 4-aspect, S3 multi-stakeholder, S4 constraint anchoring)
   - Phase C: META-1.1 domain anchor + META-1.2 phase deconstruct
   - Phase D: aggregate score → quality-matrix.yaml + evaluation-report.md
4. Retrieved_docs: 7 knowledge docs
5. Input contract: `design.md`, `criteria.md`, `design-validation-report.yaml`
6. Output contract: `.skill-context/{skill}/quality-matrix.yaml`, `.skill-context/{skill}/evaluation-report.md`
7. Failure modes: criteria files missing → exit with error, don't fabricate

### D3-4: `.claude/agents/_staging/ba-pipeline-runner.md`

Agent chuyên nghiệp cho BA pipeline (elicitor → analyst → synthesizer): điều phối BA sub-pipeline, không main pipeline orchestration.

> [revised per 1-role-per-agent: giữ nguyên role, clean contract — không dồn orchestration chính vào agent này]

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

### D3-5: `.claude/agents/_staging/external-code-reviewer.md`

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

### D3-6: `.claude/agents/_staging/user-knowledge-ingestor.md`

Agent tiếp nhận, parse, ingest tài liệu/knowledge từ user cung cấp trong suốt build. **MỚI — không có trong thiết kế 4-agent gốc.** Đảm nhiệm khâu khai thác tài nguyên từ user.

```yaml
name: user-knowledge-ingestor
description: "Use PROACTIVELY khi user cung cấp tài liệu domain (PDF, MD, code, mockup) trong quá trình build. Elicit + parse + ingest knowledge. Output: phần bổ sung cho context bus."
model: opus  # elicitation deep reasoning, multi-modal context
justification: "Elicitation từ user resource cần deep reasoning để extract implicit domain knowledge. Model conversation multi-turn."
tools: [Read, Glob, Grep]
permissionMode: default
skills: []
hooks:
  PreToolUse:
    - matcher: "Write"
      hook: |
        INPUT=$(cat)
        FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')
        [ -z "$FILE_PATH" ] && exit 0
        if [[ ! "$FILE_PATH" =~ \.skill-context/{skill}/user-contrib ]]; then
          echo "BLOCKED: ingestor chỉ write .skill-context/{skill}/user-contrib*" >&2
          exit 2
        fi
```

### D3-7: `.claude/agents/_staging/drift-detector.md`

Agent Stage 2.5 — phát hiện sai lệch design↔plan trước khi Builder nhận handoff. **MỚI — Stage 2.5 bị bỏ sót trong 4-agent gốc.**

```yaml
name: drift-detector
description: "Use PROACTIVELY bởi pipeline-orchestrator sau Planner. Check back-link fidelity, contract alignment, zone alignment before Builder handoff."
model: sonnet
justification: "Drift detection = mechanical comparison (todo.md vs design.md). Pattern match, không cần deep reasoning."
tools: [Read, Glob, Grep]
permissionMode: default
skills: []
hooks:
  PreToolUse:
    - matcher: "Write"
      hook: |
        INPUT=$(cat)
        FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')
        [ -z "$FILE_PATH" ] && exit 0
        if [[ ! "$FILE_PATH" =~ \.skill-context/{skill}/drift|audit ]]; then
          echo "BLOCKED: drift-detector chỉ write .skill-context/{skill}/drift* | audit-*" >&2
          exit 2
        fi
```

### D3-8: `.claude/agents/_staging/branch-orchestrator.md` (TÙY CHỌN)

Agent Branch B parallel coordination — spawn parallel builders + SSP contract validate. **Chỉ build nếu Phase 3 scope còn dư. Có thể defer sang Phase 8.**

```yaml
name: branch-orchestrator
description: "Orchestrate Branch B micro-skill bundle — parallel builders + SSP contract validation. Trigger: pipeline-orchestrator khi SCS >= 3.0."
model: opus
justification: "Branch B coordination cần state management qua nhiều parallel session — opus cho orchestration planning."
tools: [Read, Task, Write]
permissionMode: default
skills: []
state_ledger_validation_hook: true
hooks:
  PreToolUse:
    - matcher: "Task"
      hook: |
        # Block recursive spawn
        INPUT=$(cat)
        SUB_TYPE=$(echo "$INPUT" | jq -r '.tool_input.subagent_type // empty')
        if [ "$SUB_TYPE" = "branch-orchestrator" ]; then
          echo "BLOCKED: recursive branch-orchestrator forbidden" >&2
          exit 2
        fi
  PostToolUse:
    - matcher: "Write|Edit"
      hook: ".claude/hooks/validate-state-ledger.sh"
```

---

## Verification checklist (cơ học)

### AC-1 — 8 agent files created at staging area
```bash
for agent in pipeline-orchestrator design-validator quality-scorer ba-pipeline-runner external-code-reviewer user-knowledge-ingestor drift-detector; do
  test -f .claude/agents/_staging/$agent.md || exit 1
done
test -f .claude/agents/_staging/branch-orchestrator.md || echo "WARNING: branch-orchestrator optional, not required for AC-1 PASS"
echo "AC-1 PASS"
```

### AC-2 — Frontmatter YAML parses + has required fields
```bash
python3 << 'EOF'
import yaml
agents = ['pipeline-orchestrator', 'design-validator', 'quality-scorer', 'ba-pipeline-runner', 'external-code-reviewer', 'user-knowledge-ingestor', 'drift-detector']
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
ALLAGENTS="pipeline-orchestrator design-validator quality-scorer ba-pipeline-runner external-code-reviewer user-knowledge-ingestor drift-detector"
for agent in $ALLAGENTS; do
  count=$(grep -c "claude/knowledge/agents/" .claude/agents/_staging/$agent.md)
  test "$count" -ge 7 || exit 1
done
echo "AC-3 PASS"
```
Note: branch-orchestrator (optional) independent check khi nó được build.

### AC-4 — Inline hooks block recursive + gate paths
```bash
ALLAGENTS="pipeline-orchestrator design-validator quality-scorer ba-pipeline-runner external-code-reviewer user-knowledge-ingestor drift-detector"
for agent in $ALLAGENTS; do
  grep -q "exit 2" .claude/agents/_staging/$agent.md || exit 1
done
echo "AC-4 PASS"
```

### AC-5 — Subagent-forge 4-evaluator passes
```bash
# Invoke subagent-forge to evaluate each agent → archive eval-report
# (Thực tế invoke — sẽ chạy 4 parallel Task calls per agent)
ALLAGENTS="pipeline-orchestrator design-validator quality-scorer ba-pipeline-runner external-code-reviewer user-knowledge-ingestor drift-detector"
for agent in $ALLAGENTS; do
  echo "Manual step: invoke subagent-forge evaluate .claude/agents/_staging/$agent.md"
  # invoke: task subagent_type=general-purpose prompt="evaluate .claude/agents/_staging/$agent.md per subagent-forge §Multi-Eval Pipeline"
done
echo "AC-5 NEEDED_MANUAL — invoke subagent-forge on each agent & verify APPROVED_FOR_REVIEW aggregate verdict"
```

### AC-6 — Output contract section exists in each agent
```bash
ALLAGENTS="pipeline-orchestrator design-validator quality-scorer ba-pipeline-runner external-code-reviewer user-knowledge-ingestor drift-detector"
for agent in $ALLAGENTS; do
  grep -q "<output_contract>" .claude/agents/_staging/$agent.md || exit 1
done
echo "AC-6 PASS"
```

### AC-7 — Skills referenced exist (or will exist — Phase 5/6)
```bash
python3 << 'EOF'
import yaml, os
agents = ['pipeline-orchestrator', 'design-validator', 'quality-scorer', 'ba-pipeline-runner', 'external-code-reviewer', 'user-knowledge-ingestor', 'drift-detector']
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

### Priority 1 — Backbone (must build first)
1. **Invoke subagent-forge to design pipeline-orchestrator** — model: sonnet, justification: mechanical dispatch, state_ledger_validation_hook: true. 8-stage orchestration only, block recursion. → commit `phase-3: pipeline-orchestrator agent staged`
2. **Review + deploy pipeline-orchestrator** — user types `deploy pipeline-orchestrator` → move staging to runtime.

### Priority 2 — Quality gate (Γ-1 fix critical)
3. **Invoke subagent-forge for design-validator** — model: sonnet, schema/contract validation, write zone `.skill-context/{skill}/design-valid*`. → commit `phase-3: design-validator agent staged`
4. **Review + deploy design-validator** — verify ≥ APPROVED_FOR_REVIEW.
5. **Invoke subagent-forge for quality-scorer** — model: opus, META-1→3 scoring, write zone `.skill-context/{skill}/quality-*`. → commit `phase-3: quality-scorer agent staged`
6. **Review + deploy quality-scorer**.

### Priority 3 — External validation (Γ-1 independent path)
7. **Invoke subagent-forge for external-code-reviewer** — model: sonnet, static analysis only, NOT biết design.md context, block code execution. → commit `phase-3: external-code-reviewer agent staged`
8. **Review + deploy external-code-reviewer**.

### Priority 4 — BA + Drift
9. **Invoke subagent-forge for ba-pipeline-runner** — model: opus, orchestrates 3 BA skills, write zone `.skill-context/{feature}/ba-*`. → commit `phase-3: ba-pipeline-runner agent staged`
10. **Review + deploy ba-pipeline-runner**.
11. **Invoke subagent-forge for drift-detector** — model: sonnet, Stage 2.5 plan-design alignment, write zone `.skill-context/{skill}/drift*`. → commit `phase-3: drift-detector agent staged`
12. **Review + deploy drift-detector**.

### Priority 5 — User resource ingestion (NEW)
13. **Invoke subagent-forge for user-knowledge-ingestor** — model: opus, elicitation+ingest từ user tài liệu, write zone `.skill-context/{skill}/user-contrib*`. → commit `phase-3: user-knowledge-ingestor agent staged`
14. **Review + deploy user-knowledge-ingestor**.

### Finalization
15. **Run full AC-1 to AC-8** — fix any failures, re-deploy if needed.
16. **Update workspce_tree.md** — append 8 new entries (7 mandatory + 1 optional) to file routing map.
17. **Author Phase 3 summary doc** — documenting all deployed agents, costs, notes.

### Optional (defer Phase 8 nếu scope quá rộng)
18. **Invoke subagent-forge for branch-orchestrator** — model: opus, Branch B parallel coordination, SSP contract validate. → commit `phase-3: branch-orchestrator agent staged`
19. **Review + deploy branch-orchestrator**.

---

## Definition of done (Phase 3)

```yaml
dod:
  - 7 mandatory agents deployed tại .claude/agents/ runtime (8 nếu include branch-orchestrator)
  - All agents PASS subagent-forge 4-evaluator aggregate verdict ≥ APPROVED_FOR_REVIEW
  - workspce_tree.md updated với agent entries
  - Each agent có ≥3 cross-references tới 7 knowledge docs
  - Each agent có ≥1 blocking hook (exit 2)
  - Each agent có state_ledger_validation_hook nếu §3-bis yêu cầu
  - No `permissionMode: bypassPermissions` anywhere
  - Each agent có <output_contract> section with concrete artifact paths
  - Model-tier justification match task complexity per Λ-10 fix
  - Phase 3 summary doc archived per `context-before-fix` pattern
```

---

## Liên kết

- [Roadmap Index](index.md)
- [Phase 2 trước](02-hook-framework.md)
- [Phase 4 kế tiếp](04-skill-pipeline-scaffold.md)
- [Subagent-forge reference](../../../.claude/agents/subagent-forge.md)
- [Examples reference doc](../../../.claude/knowledge/agents/examples.md)