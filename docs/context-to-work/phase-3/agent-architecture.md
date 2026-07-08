---
name: agent-architecture
version: 0.0.2
last_updated: 2026-07-09
status: revised
revision_history:
  - "0.0.2 (2026-07-09): downgrade pipeline-orchestrator opus→sonnet per user review (Λ-10 fix); add §3-bis State Ledger Validation Hook; add AS-11 (state ledger validation hook mandatory) + AS-12 (model-tier justification per task complexity) per user review II.1+II.2"
  - "0.0.1 (2026-07-09): initial architecture document — 4 concentrated → 8 specialized agents"
suite: WASHVN
target_consumer: phase-3-builder
description: "Re-architecture Phase 3 Agent Build — chuyển từ concentrated 4-agent sang modular agent-per-role với role taxonomy đầy đủ cho toàn ecosystem, I/O contract chuẩn hóa, tam phân gate pattern, và LLM-specific failure mode catalog."
tags: [architecture, agent, phase-3, role-taxonomy, handoff-contract, llm-failure-modes]
---

# Agent Architecture — Phase 3 Re-Architecture

> [!IMPORTANT]
> Tài liệu này tái kiến trúc Phase 3 Agent Build dự án WASHVN. Từ **4 concentrated agents** (skill-pipeline-orchestrator, aggregate-quality-gatekeeper, ba-pipeline-runner, external-code-reviewer) chuyển sang **8 specialized agents** với `1-role-per-agent` principle. Taxonomy framework đầy đủ cho cả ecosystem (orchestration + stage-executor + gate + validator + knowledge-ingestion + infrastructure), Phase 3 build subset tối thiểu.

> [!WARNING]
> Đây là architecture document, không phải implementation. Concrete agent file build sẽ thực hiện qua [subagent-forge](file:///home/stveve/Documents/workspace/build-workflow/WASHVN/.claude/agents/subagent-forge.md) theo §2 Roster.

> [!NOTE]
> Tham chiếu trực tiếp: [architecture.md](file:///home/stveve/Documents/workspace/build-workflow/WASHVN/architecture.md) (5-Layer Pipeline), [standards.md](file:///home/stveve/Documents/workspace/build-workflow/WASHVN/standards.md) (format), [configuration.md](file:///home/stveve/Documents/workspace/build-workflow/WASHVN/.claude/knowledge/agents/configuration.md) (frontmatter 16-field), [workflow_patterns.md](file:///home/stveve/Documents/workspace/build-workflow/WASHVN/.claude/knowledge/agents/workflow_patterns.md) (cascading max depth = 2), [03-agent-foundation.md](file:///home/stveve/Documents/workspace/build-workflow/WASHVN/Temps/spec/roadmaps/03-agent-foundation.md) (roadmap gốc).

---

## §1. Agent Role Taxonomy (Ecosystem Framework)

```yaml
# [traced-to: architecture.md §1 5-Layer Pipeline + §5 Quality Gates]
# [traced-to: 03-agent-foundation.md §45-104 (4 agents gốc) + §5.3 runtime chain (10 entities)]

role_layers:
  L0_orchestration:
    primary: "Điều phối luồng, không thực thi nội dung nghiệp vụ"
    agents:
      - pipeline-orchestrator      # main 8-stage DAG coordinator
      - ba-pipeline-runner          # BA elicitor→analyst→synthesizer sub-chain
      - branch-orchestrator         # Branch B parallel micro-skill coordination (SCS >= 3.0)

  L1_knowledge_ingestion:
    primary: "Tiếp nhận, parse, curate tài liệu/knowledge từ user trong suốt build"
    agents:
      - user-knowledge-ingestor    # NEW: elicit+ingest user resource (PDF/MD/code domain docs)

  L2_stage_executor:
    primary: "Thực thi 1 stage nghiệp vụ cụ thể — Phase 5-7 build dưới dạng SKILL"
    note: "Phase 3 không build agents lớp này. Role template chuẩn cho skill design."
    skills_not_agents:
      - skill-explorer              # Stage 0
      - skill-knowledge-miner       # Stage 0.7
      - skill-architect             # Stage 1
      - skill-planner               # Stage 2
      - skill-builder               # Stage 3
      - production-code-reviewer    # Stage 3.5a (skill)
      - skill-security-reviewer     # Stage 3.5b (skill)
      - sandbox-tester              # Stage 4
      - indexer                      # Stage 5

  L3_gate:
    primary: "Đảm nhiệm 1 trong 3 gate role: validation | quality | handoff"
    agents:
      - design-validator           # sonnet, schema/contract validation gate
      - quality-scorer              # opus, META-1→3 scoring gate
      - drift-detector              # plan-design alignment drift gate (Stage 2.5)

  L4_external_validator:
    primary: "Fresh-eyes reviewer không cùng context với builder — fix Γ-1"
    agents:
      - external-code-reviewer      # static analysis only, NOT biết design.md

  L5_infrastructure:
    primary: "Công cụ vận hành, không thuộc pipeline runtime"
    agents:
      - subagent-forge              # agent creation tool — đã tồn tại
      - scs-router                   # SCS routing decision (Stage 0.5) — optional Phase 3+
```

### Nguyên tắc 1-role-per-agent

```yaml
# [proposed — address Λ-1 Role Confation]

role_invariant:
  principle: "Mỗi agent có ĐÚNG 1 primary_responsibility"
  cannot_have: "agent vừa orchestrate vừa validate vừa gate"
  cross_cutting: "block recursion (γ-7) và write zone gating KHÔNG tính là role — là safety bounded trên mọi agent"

  per_role_required_fields:
    primary_responsibility: "string ≤ 30 từ — chính xác 1 hành động"
    not_responsible_for:    "list — ranh giới rõ với role khác"
    input_artifacts:        "list[YAML contract]"
    output_artifacts:       "list[YAML contract]"
    gate_role:              "validation | quality | handoff | none"
    model_tier:             "haiku | sonnet | opus (justify)"
    write_zone:             "path pattern exact"
```

---

## §2. Phase 3 Agent Roster (Concrete Build)

> [!IMPORTANT]
> 8 agents Phase 3 sẽ build. Thứ tự phản ánh dependency. Branch-orchestrator có thể defer Phase 8 nếu scope quá rộng.

```yaml
# [proposed — decomposition từ 4 agents concentrate sang 8 specialized]

phase_3_agents:
  1_user_knowledge_ingestor:
    primary_responsibility: "Elicit + parse + ingest tài liệu/knowledge từ user cung cấp trong suốt build"
    not_responsible_for:
      - "Orchestrate pipeline stages"
      - "Validate design quality"
      - "Score META criteria"
    input_artifacts: ["user_resource_path (PDF/MD/code/codebase dir)"]
    output_artifacts:
      - ".skill-context/{skill}/user-contributed-knowledge.md"
      - ".skill-context/{skill}/glossary-supplement.yaml"
      - ".skill-context/{skill}/ingest-log.md"
    gate_role: "validation (input artifact supply)"
    model: opus
    justification: "Elicitation deep reasoning, cần maintain context đa modal qua nhiều turn"
    tools: [Read, Glob, Grep]
    write_zone: ".skill-context/{skill}/user-contrib*"
    new_role: true  # Không có trong 4-agents gốc, bổ sung theo user intent "khai thác tài liệu từ user"
    traces_to_user_intent: "User cung cấp tài liệu domain/thiết kế đặc thù trong quá trình build"

  2_pipeline_orchestrator:
    primary_responsibility: "Điều phối tuần tự 8-stage pipeline, không thực thi nội dung"
    not_responsible_for:
      - "Quality scoring (đã có quality-scorer)"
      - "Write gating logic (chỉ safety hook, không logic nghiệp vụ)"
      - "BA elicitation (đã có ba-pipeline-runner)"
    input_artifacts: ["user_request: {skill_name, mode: build|rebuild|maintain}"]
    output_artifacts:
      - ".skill-context/{skill}/_orchestration_log.md"
      - ".skill-context/{skill}/_state_ledger.yaml"
    gate_role: "handoff (chuyển giao giữa stages)"
    model: sonnet  # [revised 2026-07-09 per user review] — downgrade opus→sonnet
    justification: "Orchestration là mechanical task — đọc state ledger + dispatch agent tiếp theo. Opus gây Λ-10 ngược: deep-reasoning model bị lãng phí cho mechanical dispatch, tăng latency mà không có quality gain. Sonnet đủ tốc độ + pattern matching cho manifest-driven orchestration."
    tools: [Read, Task, TodoWrite]
    write_zone: ".skill-context/{skill}/_*log* | .skill-context/{skill}/_state*"
    state_ledger_validation_hook: true  # [added 2026-07-09] — see §3-bis
    decomposition_from: "skill-pipeline-orchestrator (gốc dồn orchestration + write gate + recursion block → giữ orchestration ONLY)"

  3_ba_pipeline_runner:
    primary_responsibility: "Điều phối BA sub-pipeline elicitor→analyst→synthesizer"
    not_responsible_for: ["Main pipeline orchestration", "META scoring"]
    input_artifacts: ["feature_request: {feature_name, business_context}"]
    output_artifacts:
      - ".skill-context/{feature}/ba-elicitor/elicitation-report.md"
      - ".skill-context/{feature}/ba-analyst/analysis-report.md"
      - ".skill-context/{feature}/ba-synthesizer/business-analysis.md"
    gate_role: "handoff"
    model: opus
    tools: [Read, Task]
    write_zone: ".skill-context/{feature}/ba-*"
    decomposition_from: "ba-pipeline-runner (gốc dồn orchestration + write gate → giữ BA orchestration ONLY)"

  4_design_validator:
    primary_responsibility: "Schema/contract validation — kiểm design.md có đủ 7-Zone, data contracts, semantic anchors không"
    not_responsible_for: ["META scoring (đã có quality-scorer)", "Plan drift check"]
    input_artifacts: ["design.md", "criteria.md"]
    output_artifacts:
      - ".skill-context/{skill}/design-validation-report.yaml"
    gate_role: "validation (input gate cho Planner)"
    model: sonnet
    tools: [Read, Glob, Grep]
    write_zone: ".skill-context/{skill}/design-valid*"
    decomposition_from: "aggregate-quality-gatekeeper (gốc dồn validate+score+gate → tách validation)"

  5_quality_scorer:
    primary_responsibility: "META-1→3 scoring — semantic depth, reverse Q, multi-stakeholder, mechanical verify"
    not_responsible_for: ["Schema validation (đã có design-validator)", "Code review (đã có external reviewer)"]
    input_artifacts: ["design.md", "criteria.md", "design-validation-report.yaml"]
    output_artifacts:
      - ".skill-context/{skill}/quality-matrix.yaml"
      - ".skill-context/{skill}/evaluation-report.md"
    gate_role: "quality (output gate cho Architect handoff)"
    model: opus
    tools: [Read, Glob, Grep]
    write_zone: ".skill-context/{skill}/quality-*"
    decomposition_from: "aggregate-quality-gatekeeper (gốc dồn validate+score+gate → tách scoring)"
    justification: "META scoring là deep reasoning task — sonnet có thể shallow. Upgrade sonnet→opus."

  6_drift_detector:
    primary_responsibility: "Phát hiện sai lệch design↔plan — Stage 2.5 back-link + contract alignment check"
    not_responsible_for: ["Quality scoring (đã có quality-scorer)", "Code review"]
    input_artifacts: ["todo.md", "design.md", "criteria.md"]
    output_artifacts:
      - ".skill-context/{skill}/drift-report.md"
      - ".skill-context/{skill}/audit-fail-report.md"  # 仅 khi FAIL
    gate_role: "validation (gate cho Builder)"
    model: sonnet
    tools: [Read, Glob, Grep]
    write_zone: ".skill-context/{skill}/drift* | .skill-context/{skill}/audit-*"
    new_role: true  # Roadmap gốc không có agent — Stage 2.5 bị fold vào orchestrator
    traces_to: "architecture.md §1 (Stage 2.5 Drift Detector) bị bỏ sót trong 4-agent Phase 3"

  7_external_code_reviewer:
    primary_responsibility: "Fresh-eyes static analysis — NOT biết design.md context, fix Γ-1 self-referential blindness"
    not_responsible_for: ["META scoring", "Plan drift check"]
    input_artifacts: ["raw/ver-3/{skill}/ artifacts"]
    output_artifacts:
      - ".skill-context/{skill}/external-review-report.md"
      - ".skill-context/{skill}/external-audit-metrics.yaml"
    gate_role: "quality (independent validation gate)"
    model: sonnet
    tools: [Read, Bash, Grep, Glob]
    write_zone: ".skill-context/{skill}/external-*"
    decomposition_from: "external-code-reviewer (gần giữ nguyên, sharpen contract)"

  8_branch_orchestrator:
    primary_responsibility: "Branch B parallel coordination — spawn parallel builders + SSP contract validate"
    not_responsible_for: ["Main pipeline DAG (đã có pipeline-orchestrator)", "BA orchestration"]
    input_artifacts: ["orchestration-plan.md", "hydrated-context"]
    output_artifacts:
      - ".skill-context/{skill}/branch-b/{micro1,micro2,micro3}/"
      - ".skill-context/{skill}/branch-b/integration-test-report.md"
    gate_role: "handoff (parallel skill coordination)"
    model: opus
    tools: [Read, Task, Write]
    write_zone: ".skill-context/{skill}/branch-b/*"
    new_role: true  # Optional — defer Phase 8 nếu Phase 3 scope balloon
    traces_to: "architecture.md §2 (Branch B SCS >= 3.0)"
```

### Build Order & Dependency

```text
Priority 1: pipeline-orchestrator       (backbone, mọi agent khác invoke qua đây)
Priority 2: quality-scorer               (γ-1 fix critical, cần trước stage executor)
Priority 3: design-validator             (Sanh đôi với quality-scorer)
Priority 4: external-code-reviewer      (γ-1 independent path)
Priority 5: drift-detector               (Stage 2.5, cần trước Builder stage)
Priority 6: ba-pipeline-runner           (BA sub-chain, độc lập)
Priority 7: user-knowledge-ingestor      (NEW — cần design input elicitation interface)
Priority 8: branch-orchestrator          (OPTIONAL — defer nếu scope quá lớn)
```

---

## §3. I/O Contract Granularity & Hand-off Manifest

### Granularity Pattern

```yaml
# [proposed — address Λ-4 Hidden Token Tax + Λ-5 Hallucinated Handoffs]

contract_granularity:
  single_artifact:
    use_for: ["gate agents (validator, scorer)", "external reviewer", "drift detector"]
    rationale: "Closed-context validation, không cần state ledger"
    shape: { input: "1 file path", output: "1 report path" }

  artifact_bundle:
    use_for: ["orchestration agents (pipeline, ba, branch)"]
    rationale: "Cần big-picture, nhưng phải externalize state ledger"
    shape: { input: "user_request + state_ledger_path", output: "next_action + updated_state_ledger" }

  stateless_executor:
    use_for: ["stage-executor skills (Phase 5-7)"]
    rationale: "Mỗi skill invoke độc lập, không carry state"
    shape: { input: "input_contract + bus_ref", output: "output_artifact + bus_ref updates" }
```

### Hand-off Manifest Schema (YAML)

```yaml
# [proposed — chuẩn hóa transfer giữa 2 agents bất kỳ]

handoff_manifest:
  schema_version: "0.0.1"
  source_agent: "<agent-role-name>"
  target_agent: "<agent-role-name>"
  skill_context: "{skill-name|feature-name}"
  trigger: "<gate_verdict | user_command | orchestrator_dispatch>"

  artifact_paths:
    required:
      - path: ".skill-context/{skill}/<artifact>"
        schema: "<schema-name or inline>"
        checksum: "sha256:<hash>"
    optional:
      - path: ".skill-context/{skill}/<artifact>"
        note: "<when-needed>"

  state_ledger_ref:
    path: ".skill-context/{skill}/_state_ledger.yaml"
    version: "<semver of state>"

  constraints:
    must:
      - "target_agent phải validate artifact_paths.required trước khi execute"
      - "source_agent cam kết output_artifacts xuất hiện trước khi emit manifest"
    must_not:
      - "target_agent không modify artifact của source_agent"
      - "source_agent không invoke target_agent (max depth = 2 cascade)"

  gate_results:
    - gate_name: "<validation|quality|handoff>"
      verdict: "PASS | FAIL | WARNING"
      evidence: "<path to gate report or inline summary>"

  next_action:
    on_pass: "invoke target_agent"
    on_fail: "rollback to <previous_agent> per F<id> matrix"
    on_warning: "escalate to user OR continue with caveat"
```

---

## §3-bis. State Ledger Validation Hook (Crit-ial Infrastructure)

> [!IMPORTANT]
> `state_ledger_ref` trong handoff_manifest (§3) là **single point of coordination** cho toàn pipeline. Bất kỳ YAML parse error hay schema violation nào cũng tê liệt pipeline → cần **schema validation hook** tích hợp sẵn, phát hiện lỗi ngay khi agent vừa ghi xong trước khi agent kế tiếp đọc file hỏng.

> [!NOTE]
> Tham chiếu hook protocol: [hooks.md](file:///home/stveve/Documents/workspace/build-workflow/WASHVN/.claude/knowleages/hooks/hooks.md) §PostToolUse (line 1657-1726). Hook script nhận JSON stdin, tham chiếu `tool_input.file_path`, trả JSON với `decision: "block"` + `reason` khi validation FAIL.

### State Ledger Schema (target cho validation)

```yaml
# [proposed — schema chốt cho `.skill-context/{skill}/_state_ledger.yaml`]

state_ledger_schema:
  schema_version: "0.0.1"
  skill_name: "<kebab-case required>"
  mode: "build | rebuild | maintain (required)"
  
  current_stage: "<enum: S0 | S0.5 | S0.7 | S1 | S1.5 | S1.7 | S2 | S2.5 | S3 | S3.5 | S4 | S5>"
  stage_status: "<enum: pending | in_progress | passed | failed | rolled_back>"
  
  artifacts:
    - stage: "S0"
      path: ".skill-context/{skill}/exploration.md"
      checksum: "sha256:<hash>"
      exists: true
  
  handoff_history:
    - from_agent: "skill-explorer"
      to_agent: "skill-knowledge-miner"
      manifest_path: ".skill-context/{skill}/_handoffs/S0-to-S0.5.yaml"
      timestamp: "ISO-8601"
      verdict: "PASS"
  
  fallback_count: 0  # integer, max 3 per F-matrix
  
  required_fields:
    - schema_version
    - skill_name
    - mode
    - current_stage
    - stage_status
    - artifacts
```

### PostToolUse Validation Hook Script

```bash
# [traced-to: hooks.md §PostToolUse (line 1657-1726)]
# Path: .claude/hooks/validate-state-ledger.sh
# Trigger: PostToolUse trên Write|Edit match `_state_ledger.yaml`

#!/usr/bin/env bash
# Đọc JSON stdin, kiểm nếu file_path là state_ledger → validate YAML + schema
set -euo pipefail

INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')

# Bỏ qua nếu không phải state_ledger
[[ "$FILE_PATH" =~ _state_ledger\.yaml$ ]] || exit 0

# 1) YAML parse check
if ! python3 -c "import yaml, sys; yaml.safe_load(open(sys.argv[1]))" "$FILE_PATH" 2>/dev/null; then
  cat <<EOF
{
  "hookSpecificOutput": {
    "hookEventName": "PostToolUse",
    "decision": "block",
    "reason": "State Ledger YAML PARSE FAIL tại $FILE_PATH. Agent ghi file phải auto-repair ngay trong turn tiếp theo — không để agent kế tiếp đọc file hỏng (Λ-9 stage state leakage)."
  }
}
EOF
  exit 0
fi

# 2) Schema required-fields check
MISSING=$(python3 <<PYEOF
import yaml, sys
with open("$FILE_PATH") as f: data = yaml.safe_load(f)
required = ["schema_version", "skill_name", "mode", "current_stage", "stage_status", "artifacts"]
missing = [r for r in required if r not in data]
print(",".join(missing))
PYEOF
)

if [[ -n "$MISSING" ]]; then
  cat <<EOF
{
  "hookSpecificOutput": {
    "hookEventName": "PostToolUse",
    "decision": "block",
    "reason": "State Ledger SCHEMA FAIL — thiếu fields: $MISSING. Mọi agent có state_ledger_validation_hook=true phải re-Write với đầy đủ required_fields."
  }
}
EOF
  exit 0
fi

# 3) Pass — không can thiệp
exit 0
```

### Hợp đồng giữa Orchestrator và Validation Hook

```yaml
# [proposed — address §II.2 reviewer critique about state ledger sync risk]

hook_binding_contract:
  applicable_to_agents:
    - pipeline-orchestrator       # primary state ledger writer
    - ba-pipeline-runner          # sub-state-ledger for BA sub-pipeline
    - branch-orchestrator         # sub-state-ledger for Branch B parallel coord
    - user-knowledge-ingestor     # glossary-supplement.yaml (cùng schema family)
  
  hook_event: "PostToolUse"
  matcher: "Write|Edit"
  trigger_path_pattern: "_state_ledger\\.yaml$"
  
  on_pass: "Agent tiếp tục workflow — không can thiệp"
  on_fail_yaml_parse: "decision=block + reason → agent ghi phải auto-repair loop (≤3 lần per AGENTS.md §6)"
  on_fail_schema: "decision=block + reason → agent ghi phải re-Write với đầy đủ required_fields"
  
  failure_escalation:
    "Sau 3 lần auto-repair FAIL → escalate lên user (per AGENTS.md §6 iterative fallbacks, max 3 iterations)"
  
  cost_model: "free — pure bash+python script, không tốn model token"
  
  integration_with_Λ:
    - "addresses Λ-2 Silent Semantic Override (hook priority rõ — validation hook không xung đột gate agent)"
    - "addresses Λ-5 Hallucinated Handoffs (state_ledger valid → manifest reference đáng tin)"
    - "addresses reviewer risk về YAML corruption — phát hiện synchronously, không để error lan truyền"
```

### Auto-Repair Loop Sequence

```text
Agent Write state_ledger.yaml
  ↓
PostToolUse hook fires (validate-state-ledger.sh)
  ↓
  ├─ PASS → exit 0 → agent continue workflow
  └─ FAIL → JSON decision:block + reason
        ↓
        Agent nhận reason trong context tool_result
        ↓
        Agent thực hiện auto-repair (re-Write với đúng schema)
        ↓
        Hook fires lại trên re-Write
        ↓
        Loop max 3 lần → nếu vẫn FAIL, agent exit + escalate user
```

> [!WARNING]
> Hook script Reference path phải được declare trong frontmatter `hooks.PostToolUse` của mỗi agent ROSTER (§2 — field `state_ledger_validation_hook: true`). subagent-forge sẽ embed hook script vào agent file khi build phase khởi động. KHÔNG hardcode hook trong từng agent — extract script ra `.claude/hooks/validate-state-ledger.sh` và reference qua relative path.

---

## §4. Tam Phân Gate Pattern

> [!IMPORTANT]
> Mỗi transition N→N+1 cần CHỈ 1 gate role active. Tránh gate chồng gate → Λ-2 Silent Semantic Override.

```yaml
# [proposed — address Λ-2 Hook Conflict + Λ-7 Cascading Hook Failure]

gate_triple:
  validation_gate:  # INPUT
    role: "Kiểm artifact đầu vào có đủ field, đúng schema, không missing không"
    owner: "design-validator (Stage 1.5a) | drift-detector (Stage 2.5)"
    verdict_shape: "PASS | FAIL_with_missing_fields"
    on_fail: "Reject invoke, return to upstream agent"
    cost_model: "sonnet — mechanical check"

  quality_gate:  # OUTPUT
    role: "Kiểm artifact đầu ra đạt META criteria hoặc domain metric không"
    owner: "quality-scorer (Stage 1.5b) | external-code-reviewer (Stage 3.5)"
    verdict_shape: "score >= threshold | PASS | FAIL_with_evidence"
    on_fail: "Block handoff, return to producer agent"
    cost_model: "opus — deep reasoning"

  handoff_gate:  # TRANSFER
    role: "Kiểm target agent ready, contract compatible, không recursion depth issue"
    owner: "pipeline-orchestrator (between all stages)"
    verdict_shape: "READY | NOT_READY_with_reason"
    on_fail: "Halt pipeline, escalate OR fallback per F-matrix"
    cost_model: "free — pure orchestration check"

  resolution:
    "Khi > 1 gate cùng active, priority: validation > quality > handoff"
    "Gate hooks từ subagent (PreToolUse exit 2) là SAFETY, không phải gate — không tính."
```

---

## §5. LLM-Specific Failure Modes (Λ-1 → Λ-10)

```yaml
# [proposed — mở rộng Γ-1/Γ-7 existing với LLM-specific patterns]

llm_failure_modes:
  Λ-1_role_confation_overload:
    mechanism: "LLM attention fragmented khi 1 prompt phải handle nhiều role khác nhau"
    affected_in_old_design: "Cả 4 agents (orchestrator 3 roles, gatekeeper 3 roles)"
    mitigation: "1-role-per-agent (§1 role_invariant)"

  Λ-2_silent_semantic_override:
    mechanism: "Hook của agent A block action mà agent B cần — LLM confused về priority"
    affected_in_old_design: "orchestrator + gatekeeper đều block writes ra .skill-context/"
    mitigation: "Hook priority table + §4 gate resolution"

  Λ-3_context_window_fragmentation:
    mechanism: "System prompt đa role phình to, ít room cho task context"
    affected_in_old_design: "8-section prompts per subagent-forge output contract"
    mitigation: "Section agent prompt ≤ 4 sections (identity, safety, workflow, output_contract)"

  Λ-4_hidden_token_tax_orchestration:
    mechanism: "Orchestrator track 10 stage states trong context → ~30-50% token budget lost"
    affected_in_old_design: "skill-pipeline-orchestrator không có state externalization"
    mitigation: "§3 state_ledger_ref — orchestrator chỉ giữ next_action pointer"

  Λ-5_hallucinated_handoffs:
    mechanism: "Narrative 'here's context from stage 1' → target hallucinates non-existent artifacts"
    affected_in_old_design: "Implicit via pipeline call, no manifest"
    mitigation: "§3 handoff_manifest với checksum + required paths"

  Λ-6_description_drift:
    mechanism: "Agent description outdated vs actual tools → routing fail"
    affected_in_old_design: "subagent-forge sinh fresh nhưng không periodic re-validate"
    mitigation: "Build phase: subagent-forge 4-evaluator validate description↔tools"

  Λ-7_cascading_hook_failure:
    mechanism: "Hook từ parent agent block tool call của child → silent failure"
    mitigation: "Hook isolation per agent level — child agent không inherit parent's PreToolUse block"

  Λ-8_circular_delegation:
    mechanism: "A→B→A qua description matching"
    mitigation: "Per-type recursion block (đã address γ-7) — extend cho tất cả agents Ph3"

  Λ-9_stage_state_leakage:
    mechanism: "Output Stage 1 bleed vào Stage 2 reasoning → incorrect independence"
    mitigation: "Stage executors stateless — chỉ đọc artifact paths qua manifest, không read narrative"

  Λ-10_model_selection_mismatch:
    mechanism: "Model tier mismatch với task complexity → 2 hướng fail: (a) shallow khi deep-cần, (b) lãng phí khi mechanical-only"
    affected_in_old_design:
      - "aggregate-quality-gatekeeper dùng sonnet cho META scoring (deep-reasoning task) → shallow"
      - "skill-pipeline-orchestrator dùng opus cho mechanical dispatch → lãng phí + latency cao"
    mitigation_v0_0_2:
      - "§2 quality-scorer: upgrade sonnet→opus (deep reasoning META scoring)"
      - "§2 pipeline-orchestrator: downgrade opus→sonnet (mechanical orchestration)"
      - "§2 user-knowledge-ingestor: giữ opus (deep elicitation đa modal)"
      - "§2 ba-pipeline-runner: giữ opus (BA elicitation cần deep reasoning, không thuần dispatch)"
      - "Model-tier mapping rule: model chọn theo task complexity, KHÔNG theo 'prestige' role"
```

---

## §6. Composition Rules & Extensibility Axes

### Composition Rules

```yaml
# [traced-to: workflow_patterns.md §5 Cascading Agents depth=2]

composition:
  max_cascade_depth: 2   # root → child → grandchild

  allowed_patterns:
    sequential_handoff:  "A → manifest → B → manifest → C (synthetic)"
    parallel_spawn:       "pivotator spawn [A, B, C] async, gather → D"
    cascade_validate:     "builder → validator → if FAIL back to builder"

  forbidden_patterns:
    - "A → A (recursion)            # blocked via γ-7 hook"
    - "A → B → A (cycle depth 2)    # cycle detection trong manifest"
    - "Validator → Producer         # gate không thể produce"

  token_cost_per_pattern:
    sequential_3_stage: "~15k-30k tokens (3× single invoke)"
    parallel_3_child:    "~25k-50k tokens (concurrent window)"
    cascade_depth_2:     "~25k-50k tokens (full chain)"
```

### Extensibility Axes

```yaml
# [proposed]

extensibility_axes:
  new_stage:
    how: "Thêm role vào L2_stage_executor §1 → plasma role §2 (nếu là agent) hoặc skill spec"
    impact: "Pipeline-orchestrator workflow_phases section append 1 line"
    backward_compat: "Yes — stage thêm không break stage hiện có"

  new_lifecycle_phase:  # e.g., Phase 9 monitoring
    how: "Thêm agent vào L0_orchestration hoặc L4_external_validator"
    impact: "Phase routing update — phase-3-build sẽ mở rộng phase-9-build"
    constraint: "新增 phase phải tuân §1 role_invariant (1 role/agent)"

  new_domain_package:  # e.g., thêm dữ liệu healthcare domain
    how: "user-knowledge-ingestor prompt template + glossary-supplement schema mở rộng"
    impact: "0 — agent role boundary không đổi, chỉ input data"

  new_model:  # e.g., thêm Claude 5 Opus release
    how: "Update configuration.md §6.2 model aliases → role-to-model mapping table §2 update if re-tier"
    impact: "Per-role justified — NOT pipeline-wide"
    backward_compat: "Yes — model alias trừu tượng hóa version cụ thể"

  new_gate_type:  # e.g., thêm accessibility gate
    how: "Thêm role vào L3_gate với gate_role xác định"
    impact: "§4 Tam Phân Gate cần verify không overlap với gate hiện có"
    constraint: "Gate mới phải không trùng verdict của ≥1 gate khác"
```

---

## §7. Phase 3 Re-mapping Table & Anti-Slop Ruleset

### Re-mapping (4 concentrated → 8 specialized)

```yaml
# [traced-to: 03-agent-foundation.md §45-236 (4 agents gốc)]

remapping:
  skill-pipeline-orchestrator:
    decomposes_to:
      - pipeline-orchestrator       # orchestration only
      - branch-orchestrator         # Branch B parallel (NEW, optional)
    removed_role: "write gate logic → chuyển sang per-agent inline hook (safety, không phải role)"

  aggregate-quality-gatekeeper:
    decomposes_to:
      - design-validator            # schema/contract check (sonnet)
      - quality-scorer              # META scoring (opus)
      - drift-detector              # plan-design alignment (NEW, Stage 2.5)
    removed_role: "Nhầm quality scoring với schema validation"

  ba-pipeline-runner:
    decomposes_to:
      - ba-pipeline-runner          # orchestration only (clean contract)
    removed_role: "write zone gating inline (safety)"

  external-code-reviewer:
    decomposes_to:
      - external-code-reviewer      # giữ nguyên, sharpen I/O contract
    new: "user-knowledge-ingestor — full NEW role, không từ agent nào"

  new_total: 8  # 7 mandatory + 1 optional (branch-orchestrator)
```

### Anti-Slop Ruleset (YAML-checkable)

```yaml
# [proposed]

anti_slop_rules:
  AS-1:
    rule: "Mọi agent role phải có primary_responsibility ≤ 30 từ"
    check: "yaml parse + count words ≥ 1 and ≤ 30"
    on_violation: "REJECT — role confation"

  AS-2:
    rule: "Mọi agent phải khai báo not_responsible_for ≥ 2 mục"
    check: "list length ≥ 2"
    on_violation: "REJECT — thiếu boundary"

  AS-3:
    rule: "write_zone phải là exact path pattern, không glob broad"
    check: "không match /^(\\.skill-context\\/.+|_staging\\/)$/ — phải cụ thể hơn"
    on_violation: "REJECT — broad scope"

  AS-4:
    rule: "model tier justify: opus → 'deep reasoning task'; sonnet → 'operational check'; haiku → 'classification only'"
    check: "regex match justification"
    on_violation: "WARN — verify model-role fit"

  AS-5:
    rule: "Description của agent phải chứa ≥1 trigger phrase đánh thức auto-routing"
    check: "contains 'trigger:' string OR imperative action verb"
    on_violation: "REJECT — routing fail risk (Λ-6)"

  AS-6:
    rule: "Không mask generic software patterns làm LLM-specific failure"
    check: "Λ-* failure phải reference LLM mechanism (attention/context/token/hallucination)"
    on_violation: "WARN — generic failure pattern"

  AS-7:
    rule: "Mọi design decision phải có trace tag: [traced-to] | [proposed] | [confirmed]"
    check: "regex tag at line end"
    on_violation: "WARN — unlogged assertion"

  AS-8:
    rule: "Architecture doc toàn bộ ≤ 4000 tokens — dài hơn split"
    check: "wc -w or tokenizer count"
    on_violation: "REJECT — split document"

  AS-9:
    rule: "Không placeholder strings (TODO, FIXME, mock, 'TBD' not bound to τι)" 
    check: "regex `(TODO|FIXME|mock\\(|pass$)` fail"
    on_violation: "REJECT — incomplete spec"

  AS-10:
    rule: "Tất cả file reference phải dùng clickable link `[name](file:///abs/path)` per standards.md §3.1"
    check: "markdown link regex file://"
    on_violation: "WARN — unreachable reference"

  AS-11:
    rule: "Mọi agent có `state_ledger_validation_hook: true` (§2 Roster) phải có PostToolUse hook reference tới `.claude/hooks/validate-state-ledger.sh` trigger path pattern `_state_ledger\\.yaml$`"
    check: "grep frontmatter `hooks.PostToolUse.*validate-state-ledger`"
    on_violation: "REJECT — bỏ sơ phí bảo vệ single-source-of-truth state ledger"
    traces_to: "§3-bis State Ledger Validation Hook + hooks.md §PostToolUse"
    added_in_version: "0.0.2"
    addresses: "Reviewer critique II.2 — State Ledger sync risk có thể tê liệt pipeline"

  AS-12:
    rule: "Model-tier selection phải justify theo task complexity KHÔNG theo role prestige — opus chỉ cho deep reasoning tasks (META scoring, elicitation, BA chain), sonnet cho operational/dispatch tasks, haiku cho classification-only"
    check: "frontmatter `justification:` regex match (deep reasoning | operational | classification)"
    on_violation: "REJECT — Λ-10 model selection mismatch"
    added_in_version: "0.0.2"
    addresses: "Reviewer critique II.1 — Lạm dụng Opus cho orchestration"
```

---

## Definition of Done (Architecture Document)

```yaml
# [traced-to: standards.md §12 Definition of Done cho tài liệu AI-first]

dod_architecture_doc:
  source_fidelity:
    - "Tất cả 4 agents gốc được remap — no orphans"
    - "Mọi trace tag reference đến file thật tồn tại"
    - "Phase 3 roster ≤ 8 agents với justification per role"

  structure:
    - "7 sections — exceeded only khi user explicitly approve"
    - "Markdown cho explanation + YAML cho contract/schema + tables cho comparison"
    - "GitHub alerts [!NOTE] [!IMPORTANT] [!WARNING] dùng đúng ngữ nghĩa"

  agent_usability:
    - "Mỗi role role có 6 required fields: primary_responsibility, not_responsible_for, input_artifacts, output_artifacts, gate_role, model_tier"
    - "Tam phân gate pattern declared rõ"
    - "Hand-off manifest schema concrete (YAML parseable)"

  token_awareness:
    - "Document total ≤ 4000 tokens (L2 domain context warning zone)"
    - "Mỗi section ≤ 800 tokens — split khi vượt"
    - "Mermaid tối thiểu, không repeat prose"

  maintainability:
    - "Mỗi section có rõ scope, không mix information types"
    - "trace tag nhất quán [traced-to] [proposed] [confirmed]"
    - "Remapping table không introduce ambiguity về agent cũ/mới"
```

---

**Document Status**: Architecture Complete — No Code Changes Made

```text
✓ Entry point identified (phase-3-context.md, 03-agent-foundation.md, architecture.md)
✓ Anti-patterns verified từ codebase (AP-1 → AP-6)
✓ LLM-specific failure mode catalog (Λ-1 → Λ-10)
✓ Role taxonomy ecosystem (6 layers)
✓ Phase 3 roster — 8 specialized agents with 1-role-per-agent
✓ TAM phân gate pattern — validation | quality | handoff
✓ Hand-off manifest schema — concrete YAML
✓ Re-mapping table — 4 concentrated → 8 specialized
✓ Composition rules + extensibility axes
✓ Anti-slop ruleset — 10 rules YAML-checkable
✓ Definition of Done — 5 categories per standards.md
```

**Document**: `docs/context-to-work/phase-3/agent-architecture.md`
**Generated by**: Sisyphus + Metis (pre-plan consultant) + context-before-fix pattern (extended)
**Language**: Vietnamese
**NO Code Changes Made** — Architecture document only, awaiting user approval before agent build phase