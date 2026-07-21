# Scope Document — Phase 3: Agent Foundation Build

**Date**: 2026-07-08
**Status**: Initial — Context Analysis Complete
**Language**: Tiếng Việt

---

## §1: Problem Summary

Phase 3 là phase thứ 4 trong lộ trình 8-phase Master Skill Suite Rebuild, với nhiệm vụ xây dựng **8 specialized agents** (từ thiết kế 4-agent concentrated gốc) tại `.claude/agents/` bằng cách sử dụng `subagent-forge` làm reference pattern, theo nguyên tắc **1-role-per-agent**. Đây là infrastructure layer cho Phase 5-7.

**Vai trò của Phase 3 trong toàn lộ trình:**
- Cung cấp orchestrator + drift detector cho skill build pipeline (Phase 5-7)
- Cung cấp external validator + quality scorer giải quyết architectural defect Γ-1 (self-referential blindness)
- Cung cấp BA pipeline runner tự động kích hoạt 3 BA skills (Phase 5)
- Cung cấp design validator cho schema compliance (mechanical validation)
- Cung cấp user-knowledge-ingestor để nhận tài liệu từ user suốt build (MỚI)
- Cung cấp code reviewer độc lập (ground-truth cho Γ-1)

**Vấn đề cần giải quyết:**
- Hiện tại `.claude/agents/_staging/` trống (chỉ có `.gitkeep`)
- Chưa có agent orchestration cho pipeline build
- Chưa có external quality validator (Γ-1)
- Chưa có BA pipeline tự động

---

## §2: Entry Point

### 2.1 Entry Points Chính

| Entry Point | Path | Vai trò |
|:------------|:-----|:--------|
| Roadmap gốc | `Temps/spec/roadmaps/03-agent-foundation.md` (383 dòng) | Spec đầy đủ: deliverables, AC, tasks, DoD |
| Checklist tracking | `docs/context-to-work/roadmap-analysis-phases/plan-checklist.2026-07-07.md` §8 | Status + task list + AC tracking |
| Subagent-forge | `.claude/agents/subagent-forge.md` (292 dòng) | Công cụ tạo agent — đã deploy sẵn |
| Spec Architects P3 | `Temps/spec/architects/P3-drift-detector-and-plan-gate/` (5 files) | Design concept cho Drift Detection + Plan Gate (reference) |
| Knowledge base | `.claude/knowledge/agents/` (7 canonical docs) | Reference bắt buộc cho mọi agent |

### 2.2 Prerequisites Status

| Prerequisite | Status | Ghi chú |
|:-------------|:------:|:--------|
| Phase 0 — Foundation Bootstrap | ✅ done | 10/10 tasks, 8/8 AC, 9/9 DoD |
| Phase 1 — Knowledge Base Authoring | ✅ done | 10/10 tasks, 7/7 AC, 7 canonical docs |
| Phase 2 — Hook Framework Foundation | ✅ done | 9/9 tasks, 7/7 AC, 6 hook scripts |
| subagent-forge invokeable | ✅ sẵn sàng | Tồn tại tại `.claude/agents/subagent-forge.md` |
| 7 knowledge docs authored | ✅ sẵn sàng | Tại `.claude/knowledge/agents/` |
| subagent-forge references valid | ✅ | Không còn dangling paths |

---

## §3: Scope Definition

### 3.1 In Scope

```yaml
in_scope:
  deliverables:
    - "7+1 agent files tại .claude/agents/_staging/ (7 mandatory + 1 optional branch-orchestrator)"
    - "7+1 evaluator reports tại .skill-context/_subagent-staging/<name>/eval-report.md"
    - "7+1 deployed agents tại .claude/agents/"
    - "Updated workspce_tree.md với new entries"
    - "Phase 3 summary doc"
  
  agents_cần_build:
    - name: pipeline-orchestrator
      model: sonnet  # [v0.0.2] downgrade opus→sonnet — mechanical dispatch
      role: "Orchestrate 8-stage pipeline — dispatch via handoff manifest"
      note: "Decomposed from skill-pipeline-orchestrator gốc (giữ orchestration ONLY)"
    
    - name: design-validator
      model: sonnet
      role: "Schema/contract validation — mechanical check design.md 7-Zone completeness"
      note: "Split từ aggregate-quality-gatekeeper gốc (gatekeeper cũ = 2+ role)"
    
    - name: quality-scorer
      model: opus
      role: "META-1→3 scoring — semantic depth, reverse Q, multi-stakeholder"
      note: "Split từ aggregate-quality-gatekeeper gốc. Upgrade sonnet→opus per Λ-10 fix"
    
    - name: ba-pipeline-runner
      model: opus
      role: "Orchestrate 3 BA skills sequentially"
    
    - name: external-code-reviewer
      model: sonnet
      role: "Fresh-eyes reviewer (Γ-1 fix) — static analysis only, NOT biết design.md"
    
    - name: user-knowledge-ingestor
      model: opus
      role: "Elicit + parse + ingest tài liệu/knowledge từ user cung cấp suốt build"
      note: "MỚI — không có trong thiết kế 4-agent gốc. Khai thác tài nguyên từ user."
    
    - name: drift-detector
      model: sonnet
      role: "Stage 2.5 plan-design alignment drift check — back-link + contract alignment"
      note: "MỚI — Stage 2.5 bị bỏ sót trong thiết kế 4-agent gốc"
    
    - name: branch-orchestrator (TÙY CHỌN)
      model: opus
      role: "Branch B parallel coordination — spawn builders + SSP contract validate"
      note: "Optional — defer sang Phase 8 nếu scope Phase 3 quá rộng"
  
  process:
    - "Invoke subagent-forge để design từng agent"
    - "Review subagent-forge output (≥ APPROVED_FOR_REVIEW)"
    - "Deploy agent từ staging sang runtime"
    - "Run full AC-1 → AC-8"
```

### 3.2 Out of Scope

```yaml
out_of_scope:
  - "Không build skills (Phase 5-7)"
  - "Không build hooks mới (Phase 2 đã xong)"
  - "Không modify knowledge docs (Phase 1 đã xong)"
  - "Không design chi tiết Drift Detection (đã có Temps/spec/architects/P3/)"
  - "Không chạy E2E pipeline test (Phase 8)"
```

### 3.3 Boundary

- **Workspace zone**: `.claude/agents/` (runtime) + `.claude/agents/_staging/` (staging)
- **State zone**: `.skill-context/_subagent-staging/` (eval reports)
- **Doc zone**: `docs/context-to-work/foundation-bootstrap/phase-3-summary.*.md`
- **GIỚI HẠN**: subagent-forge chỉ được write vào `_staging/` (enforced by hooks)

---

## §4: Impact Analysis

### 4.1 Direct Impact

| Component | Impact | Mức độ |
|:----------|:-------|:------:|
| `.claude/agents/` | +8 agents deployed (7 mandatory + 1 optional branch-orchestrator) | 🔴 Cao |
| `.claude/agents/_staging/` | 8 staging files created (7 mandatory + 1 optional) | 🟡 Trung |
| `.skill-context/_subagent-staging/` | 4+ eval reports generated | 🟢 Thấp |
| `workspce_tree.md` | +4 entries (typo "workspce" giữ nguyên) | 🟢 Thấp |
| `.claude/agents/subagent-forge.md` | Sẽ được invoke 4 lần | 🟡 Trung |

### 4.2 Indirect Impact

| Component | Impact | Reason |
|:----------|:-------|:-------|
| **Phase 5 (BA Skills)** | Phụ thuộc agents để chạy pipeline | Phải chờ Phase 3 deploy runners |
| **Phase 6 (Main Pipeline)** | Phụ thuộc pipeline-orchestrator | Không có orchestrator → không build skills |
| **Phase 8 (Integration)** | Phụ thuộc external-code-reviewer cho Γ-1 fix | Code review quality phụ thuộc agent |
| **Architecture defect Γ-1** | Được address bởi 3 agents | quality-scorer + external-code-reviewer + design-validator |
| **Architecture defect Γ-7** | Được address bởi orchestrator | Block recursive spawn (max depth = 1) |

### 4.3 Architectural Defects Resolution

| Defect | Phase 3 Role | Agent giải quyết | Cơ chế |
|:-------|:-------------|:-----------------|:--------|
| Γ-1 Self-Referential Blindness | 🔴 Primary fix | `quality-scorer` + `external-code-reviewer` + `design-validator` | External LLM validator không cùng context với builder. design-validator schema check + quality-scorer META scoring + external-code-reviewer fresh-eyes |
| Γ-7 Escalation Recursion | 🟡 Partial fix | `pipeline-orchestrator` | Hooks block recursive spawn, max depth = 1 |

---

## §5: Call Chain

### 5.1 Phase 3 Execution Flow (Build 8 Agents: 7 mandatory + 1 optional)

```mermaid
flowchart TD
    A[Start Phase 3] --> B[Task 1: Invoke subagent-forge<br/>→ pipeline-orchestrator]
    B --> C[Task 2: Review subagent-forge output<br/>≥ APPROVED_FOR_REVIEW?]
    C -->|Yes| D[Task 3: Deploy orchestrator]
    C -->|No| B
    
    D --> E[Task 4: Invoke subagent-forge<br/>→ design-validator — tách từ aggregate-gatekeeper]
    E --> F[Task 5: Review + deploy gatekeeper]
    
    F --> G[Task 6: Invoke subagent-forge<br/>→ ba-pipeline-runner]
    G --> H[Task 7: Review + deploy runner]
    
    H --> I[Task 8: Invoke subagent-forge<br/>→ external-code-reviewer]
    I --> J[Task 9: Review + deploy reviewer]
    
    J --> K[Task 10: Run AC-1 → AC-8]
    K --> L{All AC PASS?}
    L -->|Yes| M[Task 11: Update workspce_tree.md]
    L -->|No| N[Fix failures → re-run AC]
    N --> L
    M --> O[Task 12: Author Phase 3 summary doc]
    O --> P[Phase 3 COMPLETE ✅]
```

### 5.2 Subagent-forge Invocation Chain (per agent)

```mermaid
flowchart LR
    A[subagent-forge invoke] --> B[subagent-forge<br/>reads 7 knowledge docs]
    B --> C[subagent-forge<br/>writes to _staging/<name>.md]
    C --> D[4-Evaluator Pipeline]
    D --> E[Eval 1: Oracle<br/>Goal Verification]
    D --> F[Eval 2: Security<br/>Reviewer]
    D --> G[Eval 3: Code<br/>Reviewer]
    D --> H[Eval 4: Quality<br/>Gatekeeper]
    E --> I{Aggregate<br/>Verdict}
    F --> I
    G --> I
    H --> I
    I -->|≥ APPROVED_FOR_REVIEW| J[Present for deploy]
    I -->|< APPROVED_FOR_REVIEW| K[Fix → re-evaluate]
    K --> C
```

### 5.3 Agent Deployment Call Chain (Runtime)

```
[User request] → subagent-forge → _staging/<agent>.md
    → 4-evaluator PASS → user "deploy <name>" → .claude/agents/<agent>.md
    
[Runtime] → pipeline-orchestrator invoked (dispatch via handoff manifest)
    → invokes skill-explorer (Stage 0)
    → invokes skill-knowledge-miner (Stage 0.5)
    → invokes skill-architect (Stage 1)
    → invokes production-quality-gatekeeper (Stage 1.5)
    → invokes skill-planner (Stage 2)
    → invokes skill-builder (Stage 3)
    → invokes production-code-reviewer + skill-security-reviewer (Stage 3.5)
    → invokes sandbox-tester (Stage 4)
    → invokes indexer (Stage 5)
```

---

## §6: Data Flow

### 6.1 Input (Phase 3 Build Phase)

```
[Input từ roadmap 03-agent-foundation.md]
  ├── Agent specs (YAML frontmatter)
  ├── Workflow requirements (8 sections)
  ├── Hooks design (PreToolUse matchers)
  └── AC/DoD definitions

[Input từ subagent-forge]
  ├── 7 knowledge docs (.claude/knowledge/agents/)
  ├── Agent design template
  └── 4-evaluator pipeline

[Input từ knowledge base hiện có]
  ├── configuration.md — frontmatter schema (16 fields)
  ├── capability_controls.md — tool/MCP/skills scoping
  ├── examples.md — 4 reference patterns
  ├── hooks_and_events.md — hook protocol (Dual-Format)
  └── workflow_patterns.md — runtime workflows
```

### 6.2 Output (Phase 3 Artifacts)

| Artifact | Path | Format | Consumer |
|:---------|:-----|:-------|:---------|
| Staging files (4) | `.claude/agents/_staging/<name>.md` | Markdown + YAML | User review |
| Eval reports (4+) | `.skill-context/_subagent-staging/<name>/eval-report.md` | Markdown | User decision |
| Deployed agents (4) | `.claude/agents/<name>.md` | Markdown + YAML | Claude Code runtime |
| Updated routing map | `workspce_tree.md` | Markdown | Developer navigation |
| Phase 3 summary | `docs/context-to-work/foundation-bootstrap/phase-3-summary.*.md` | Markdown | Context archive |

### 6.3 Dependencies

```yaml
dependencies:
  requires_from_phase_0:
    - "Directory structure: .claude/agents/_staging/, _archive/"
    - "subagent-forge.md scaffold"
  
  requires_from_phase_1:
    - "7 canonical knowledge docs (configuration.md, capability_controls.md, examples.md, forks.md, hooks_and_events.md, workflow_patterns.md, xml_tags_standards.yaml)"
  
  requires_from_phase_2:
    - "PreToolUse hooks: write_gate, staging_gate"
  
  produces_for_phase_5:
    - "pipeline-orchestrator — orchestrates skill build (dispatch pipeline)"
    - "ba-pipeline-runner — runs BA skills chain"
    - "user-knowledge-ingestor — ingest user resources for BA elicitation"
  
  produces_for_phase_6:
    - "pipeline-orchestrator — orchestrates main pipeline"
    - "quality-scorer — META-1→3 scoring external validator"
    - "design-validator — schema/contract validation"
    - "drift-detector — plan-design alignment checkpoint"
  
  produces_for_phase_7:
    - "pipeline-orchestrator — orchestrates sandbox/indexer stages"
  
  produces_for_phase_8:
    - "external-code-reviewer — Γ-1 ground truth validator"
    - "quality-scorer — quality gate (META scoring)"
    - "design-validator — design gate (schema compliance)"
```

---

## §7: Affected Components

### 7.1 Files

| File | Action | Mức độ |
|:-----|:-------|:------:|
| `.claude/agents/subagent-forge.md` | Invoked 7+ lần (read-only) | 🟢 Không đổi |
| `.claude/agents/_staging/pipeline-orchestrator.md` | **CREATE** | 🔴 New file |
| `.claude/agents/_staging/design-validator.md` | **CREATE** | 🔴 New file |
| `.claude/agents/_staging/quality-scorer.md` | **CREATE** | 🔴 New file |
| `.claude/agents/_staging/ba-pipeline-runner.md` | **CREATE** | 🔴 New file |
| `.claude/agents/_staging/external-code-reviewer.md` | **CREATE** | 🔴 New file |
| `.claude/agents/_staging/user-knowledge-ingestor.md` | **CREATE** | 🔴 New file |
| `.claude/agents/_staging/drift-detector.md` | **CREATE** | 🔴 New file |
| `.claude/agents/_staging/branch-orchestrator.md` | **CREATE** (optional) | 🟡 Tùy chọn |
| `.claude/agents/pipeline-orchestrator.md` | **CREATE** (deploy) | 🔴 New file |
| `.claude/agents/design-validator.md` | **CREATE** (deploy) | 🔴 New file |
| `.claude/agents/quality-scorer.md` | **CREATE** (deploy) | 🔴 New file |
| `.claude/agents/ba-pipeline-runner.md` | **CREATE** (deploy) | 🔴 New file |
| `.claude/agents/external-code-reviewer.md` | **CREATE** (deploy) | 🔴 New file |
| `.claude/agents/user-knowledge-ingestor.md` | **CREATE** (deploy) | 🔴 New file |
| `.claude/agents/drift-detector.md` | **CREATE** (deploy) | 🔴 New file |
| `.claude/agents/branch-orchestrator.md` | **CREATE** (deploy, optional) | 🟡 Tùy chọn |
| `workspce_tree.md` | **UPDATE** entries | 🟡 Modified |
| `.skill-context/_subagent-staging/<name>/eval-report.md` | **CREATE** (7+ files) | 🟡 New artifacts |
| `docs/context-to-work/foundation-bootstrap/phase-3-summary.*.md` | **CREATE** | 🟢 Summary doc |

### 7.2 Functions/APIs

| Function/API | Component | Impact |
|:-------------|:----------|:-------|
| `subagent-forge` invoke (via Task) | 7+ agents | Được gọi 7+ lần (mỗi agent 1 lần) |
| `deploy` command (manual) | User action | Move staging → runtime |
| PreToolUse hooks (Phase 2) | write_gate, staging_gate | Gate agent writes |
| AC verification scripts | bash/python | 8 AC checks |

### 7.3 Knowledge Docs được Reference (bắt buộc ≥7 per agent)

| Doc | Agent tham chiếu |
|:----|:-----------------|
| `configuration.md` | Cả 7+ agents (frontmatter schema) |
| `capability_controls.md` | Cả 7+ agents (tool scoping) |
| `examples.md` | Cả 7+ agents (reference patterns) |
| `forks.md` | Orchestrator, Runner (fork semantics) |
| `hooks_and_events.md` | Cả 7+ agents (hook design, state_ledger_validation_hook) |
| `workflow_patterns.md` | Orchestrator, Runner, branch-orchestrator (runtime patterns) |
| `xml_tags_standards.yaml` | Cả 7+ agents (8-section prompt structure) |

---

## §8: Evidence

<evidence>
<file>/home/stveve/Documents/workspace/build-workflow/WASHVN/Temps/spec/roadmaps/03-agent-foundation.md</file>
<line>1-383</line>
<finding>Roadmap gốc Phase 3: 4 agents, 12 tasks, 8 AC, DoD, design principle, execution flow đầy đủ</finding>
</evidence>

<evidence>
<file>/home/stveve/Documents/workspace/build-workflow/docs/context-to-work/roadmap-analysis-phases/plan-checklist.2026-07-07.md</file>
<line>351-412</line>
<finding>Phase 3 tracking: status pending, 0/12 tasks, 0/8 AC, 4 agents xác định rõ</finding>
</evidence>

<evidence>
<file>/home/stveve/Documents/workspace/build-workflow/WASHVN/.claude/agents/subagent-forge.md</file>
<line>1-60</line>
<finding>subagent-forge đã sẵn sàng: PreToolUse hooks gate staging writes, 4-evaluator pipeline, skills: [skill-security-reviewer]</finding>
</evidence>

<evidence>
<file>/home/stveve/Documents/workspace/build-workflow/WASHVN/.claude/agents/_staging/</file>
<line>1</line>
<finding>Staging directory trống (chỉ .gitkeep) — chưa có agent nào được tạo</finding>
</evidence>

<evidence>
<file>/home/stveve/Documents/workspace/build-workflow/WASHVN/.claude/knowledge/agents/README.md</file>
<line>19-29</line>
<finding>7 canonical knowledge docs sẵn sàng: configuration.md (273), capability_controls.md (356), examples.md (302), forks.md (296), hooks_and_events.md (547), workflow_patterns.md (408), xml_tags_standards.yaml (420)</finding>
</evidence>

<evidence>
<file>/home/stveve/Documents/workspace/build-workflow/WASHVN/Temps/spec/architects/P3-drift-detector-and-plan-gate/README.md</file>
<line>1-26</line>
<finding>Spec Architects P3 (Drift Detector + Plan Gate) cung cấp design reference cho external-code-reviewer và quality gatekeeper — khác với roadmap Phase 3 Agent Build</finding>
</evidence>

<evidence>
<file>/home/stveve/Documents/workspace/build-workflow/WASHVN/Temps/spec/architects/shared/architecture-overview.md</file>
<line>7-14</line>
<finding>5-Layer Pipeline: L0 (Intake) → L1 (Knowledge) → L2 (Design) → L3 (Planing & Verification) → L4 (Implementation). Phase 3 agents nằm ở L3-L4</finding>
</evidence>

<evidence>
<file>/home/stveve/Documents/workspace/build-workflow/WASHVN/Temps/spec/roadmaps/03-agent-foundation.md</file>
<line>22-28</line>
<finding>Prerequisites list: Phase 0,1,2 done; subagent-forge invokeable; 7 knowledge docs; non-dangling paths — tất cả đã satisfied</finding>
</evidence>

<evidence>
<file>/home/stveve/Documents/workspace/build-workflow/WASHVN/Temps/spec/roadmaps/03-agent-foundation.md</file>
<line>83-104</line>
<finding>skill-pipeline-orchestrator spec: 8-section system prompt, hooks block recursive spawn + write outside _staging/, 8-stage pipeline orchestration</finding>
</evidence>

<evidence>
<file>/home/stveve/Documents/workspace/build-workflow/WASHVN/Temps/spec/roadmaps/03-agent-foundation.md</file>
<line>106-148</line>
<finding>aggregate-quality-gatekeeper spec: sonnet model, META-1→3 scoring, external validator (Γ-1 fix), chỉ write .skill-context/</finding>
</evidence>

<evidence>
<file>/home/stveve/Documents/workspace/build-workflow/WASHVN/Temps/spec/roadmaps/03-agent-foundation.md</file>
<line>150-188</line>
<finding>ba-pipeline-runner spec: opus model, 3 BA skills (elicitor → analyst → synthesizer), block recursive spawn, chỉ write ba-* dirs</finding>
</evidence>

<evidence>
<file>/home/stveve/Documents/workspace/build-workflow/WASHVN/Temps/spec/roadmaps/03-agent-foundation.md</file>
<line>190-236</line>
<finding>external-code-reviewer spec: Γ-1 ground truth, sonnet model, static analysis only (pyflakes/eslint), NOT biết design.md context</finding>
</evidence>

<evidence>
<file>/home/stveve/Documents/workspace/build-workflow/WASHVN/Temps/spec/roadmaps/03-agent-foundation.md</file>
<line>240-329</line>
<finding>AC-1 đến AC-8 verification scripts: test -f, YAML parse, grep knowledge refs, grep exit 2, subagent-forge 4-evaluator, grep output_contract, skills check, bypassPermissions ban</finding>
</evidence>

<evidence>
<file>/home/stveve/Documents/workspace/build-workflow/docs/context-to-work/roadmap-analysis-phases/plan-checklist.2026-07-07.md</file>
<line>961-973</line>
<finding>Defects tracker: Γ-1 pending (Phase 3 address), Γ-7 pending (Phase 3 address via orchestrator hooks)</finding>
</evidence>

<evidence>
<file>/home/stveve/Documents/workspace/build-workflow/docs/context-to-work/roadmap-analysis-phases/plan-checklist.2026-07-07.md</file>
<line>1093-1098</line>
<finding>Uncertainty flags: AC-5 Phase 3 (subagent-forge 4-evaluator) đánh dấu NEEDED_MANUAL — cần invoke thực tế</finding>
</evidence>

---

## §9: Confidence Assessment

```yaml
overall_confidence: 92%  # [v0.0.2 sync] tăng từ 88% sau khi re-architecture + document đồng bộ

breakdown:
  roadmap_understanding: 95%
    - "03-agent-foundation.md spec rõ ràng, đầy đủ 383 dòng"
    - "plan-checklist.md tracking chi tiết 12 tasks + 8 AC"
  
  prerequisites_verification: 95%
    - "Phase 0,1,2 đều done (verified từ checklist)"
    - "subagent-forge sẵn sàng (verified từ file content)"
    - "7 knowledge docs sẵn sàng (verified từ directory listing)"
  
  agent_design_understanding: 95%  # [v0.0.2] tăng từ 90% sau re-architecture
    - "8 agents có spec rõ ràng trong roadmap + architecture doc v0.0.2"
    - "1-role-per-agent principle applied, Λ-1→Λ-10 mapped"
    - "8-section prompt structure chi tiết chưa được viết (subagent-forge sẽ sinh)"
  
  architectural_impact: 85%
    - "Γ-1 address chính xác bằng external validator"
    - "Γ-7 address bằng block recursion hooks"
    - "AC-5 (subagent-forge 4-evaluator) chưa rõ automation level"
  
  evidence_verification: 88%
    - "Tất cả evidence traced đến file:line cụ thể"
    - "Staging trống đã verify trực tiếp"
    - "subagent-forge hooks đã verify"

uncertainty_flags:
  - "AC-5: subagent-forge 4-evaluator cần invoke thực tế — không thể verify passive"
  - "Agent design details (8-section prompts) sẽ do subagent-forge sinh — chưa thể pre-verify"
  - "Skill dependencies (ba-elicitor, ba-analyst, ba-synthesizer) chưa build — AC-7 sẽ WARNING"
  - "Hook interaction: Phase 2 hooks (write_gate, staging_gate) + agent inline hooks — cần test integration"
```

---

## §10: Open Questions

| # | Question | Priority | Liên quan | Status |
|:--|:---------|:--------:|:----------|:------:|
| 1 | AC-5 subagent-forge 4-evaluator: automate hay manual invoke? | 🔴 Cao | AC-5 | Open (manual tại Phase 3, P8 automate) |
| 2 | Skill dependencies reference (ba-*, production-*) chưa build: AC-7 PASS hay WARNING? | 🟡 Trung | AC-7 | Roadmap cho phép WARNING |
| 3 | Deploy command: cần script tự động move staging→runtime hay manual `mv`? | 🟡 Trung | Task 3,5,7,9 | Open |
| 4 | Hook interaction test: Phase 2 hooks (workspace gate) + agent inline hooks có conflict? | 🟡 Trung | Integration | Open |
| 5 | `workspce_tree.md` typo "workspce": giữ nguyên hay fix? | 🟢 Thấp | Task 11 | Giữ nguyên per roadmap |
| 6 | Phase 3 summary doc path: `foundation-bootstrap/` (như plan-checklist) hay `roadmap-analysis-phases/`? | 🟢 Thấp | Task 12 | Roadmap ghi `foundation-bootstrap/` |
| 7 | external-code-reviewer: có cần Codex CLI integration cho cross-model review không? | 🟢 Thấp | D3-4 | Roadmap đề xuất nhưng optional |

---

## §11: Task Priority Order (Khuyến nghị)

Dựa trên dependency graph và spec analysis, thứ tự build khuyến nghị (từ [agent-architecture.md](file:///home/stveve/Documents/workspace/build-workflow/WASHVN/docs/context-to-work/phase-3/agent-architecture.md) §2):

```yaml
build_order:
  priority_1: "pipeline-orchestrator — model: sonnet"
    reason: "Backbone — dispatch 8-stage pipeline, state_ledger_validation_hook"
    estimated_effort: "1 session (orchestration only, nhẹ hơn old design)"
  
  priority_2: "design-validator + quality-scorer (pair)"
    reason: "Tách từ aggregate-gatekeeper gốc. design-validator (sonnet, schema check) trước, quality-scorer (opus, META scoring) sau"
    estimated_effort: "0.5 session mỗi agent"
  
  priority_3: "external-code-reviewer"
    reason: "Γ-1 ground truth — static analysis only, độc lập với quality-scorer"
    estimated_effort: "0.5 session"
  
  priority_4: "ba-pipeline-runner + drift-detector (parallelizable)"
    reason: "Ba-pipeline-runner (opus) orchestrate BA chain; drift-detector (sonnet) Stage 2.5 alignment"
    estimated_effort: "0.5 session mỗi agent"
  
  priority_5: "user-knowledge-ingestor"
    reason: "MỚI — tiếp nhận tài liệu từ user suốt build. Opus model, deep elicitation"
    estimated_effort: "0.5 session"
  
  optional: "branch-orchestrator"
    reason: "Defer Phase 8 nếu scope quá rộng — Branch B parallel coordination"
    estimated_effort: "0.5 session"

  finalization:
    - "Run AC-1 → AC-8 (full verification)"
    - "Update workspce_tree.md"
    - "Author Phase 3 summary doc"
```

**Tổng effort ước tính: 3-4 sessions** (tăng từ 2-3 do số agent tăng, mỗi agent chuyên biệt nên thời gian per agent giảm)

---

## §12: Agent Design Comparison Matrix

| Aspect | pipeline-orchestrator | design-validator | quality-scorer | ba-pipeline-runner | external-code-reviewer | user-knowledge-ingestor | drift-detector | branch-orchestrator |
|:-------|:--------------------:|:----------------:|:--------------:|:------------------:|:----------------------:|:-----------------------:|:--------------:|:-------------------:|
| **Model** | sonnet | sonnet | opus | opus | sonnet | opus | sonnet | opus |
| **Tools** | Read,Task,TodoWrite | Read,Glob,Grep | Read,Glob,Grep | Read,Task | Read,Bash,Grep,Glob | Read,Glob,Grep | Read,Glob,Grep | Read,Task,Write |
| **Permission** | default | default | default | default | default | default | default | default |
| **Skills dep** | [] | [] | [prod-quality-gatkpr] P6 | [ba-*] P5 | [prod-code-review] P6 | [] | [] | [] |
| **Write zone** | _staging/ + state_ledger | .skill-context/{skill}/design-valid* | .skill-context/{skill}/quality-* | .skill-context/{feat}/ba-* | review repos only | .skill-context/{skill}/user-contrib* | .skill-context/{skill}/drift* | .skill-context/{skill}/branch-b/* |
| **Block recursion** | ✅ | N/A | N/A | ✅ | N/A | N/A | N/A | ✅ |
| **Block code exec** | ❌ (dispatch) | ❌ (read-only) | ❌ (read-only) | ❌ (orchestrate) | ✅ (static anal.) | ❌ (read-only) | ❌ (read-only) | ❌ (orchestrate) |
| **Γ-1 fix** | ❌ | ❌ | ✅ External | ❌ | ✅ Fresh-eyes | ❌ | ❌ | ❌ |
| **Γ-7 fix** | ✅ Max depth=1 | ❌ | ❌ | ✅ Max depth=1 | ❌ | ❌ | ❌ | ✅ Max depth=1 |
| **State ledger hook** | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |

---

## §13: Risk Assessment

| Risk | Severity | Likelihood | Mitigation |
|:-----|:--------:|:----------:|:-----------|
| subagent-forge 4-evaluator FAIL cho 1+ agents | 🔴 Cao | 🟡 Medium | Iterate design với subagent-forge cho đến APPROVED |
| Hook conflict: Phase 2 staging_gate blocks agent deploy | 🟡 Trung | 🟢 Low | Deploy command bypass staging_gate (user action) |
| State ledger YAML corruption tê liệt pipeline | 🔴 Cao | 🟢 Low | §3-bis PostToolUse hook validate + auto-repair loop (max 3) |
| Model-tier mismatch — sonnet cho deep reasoning / opus cho mechanical | 🟡 Trung | 🟡 Medium | AS-12 rule enforce justification per agent. Pipeline-orchestrator downgrade opus→sonnet per user review. |
| AC-7 (skills reference) WARNING misinterpreted as FAIL | 🟢 Thấp | 🟡 Medium | Roadmap cho phép WARNING cho Phase 5/6 skills |
| Knowledge docs reference count < 7 per agent | 🟡 Trung | 🟢 Low | AC-3 grep sẽ detect, subagent-forge đảm bảo ≥7 |
| bypassPermissions accidentally included | 🔴 Cao | 🟢 Low | AC-8 grep fail — subagent-forge không generate |
| 8-agent scope làm tăng session count 2-3→3-4 | 🟡 Trung | 🟡 Medium | Mỗi agent chuyên biệt nên build per agent nhanh hơn, compensate |

---

**Document Status**: Context Complete — No Code Changes Made

```
✓ Entry point identified (03-agent-foundation.md, plan-checklist.md)
✓ Prerequisites verified (Phase 0,1,2 all done)
✓ Scope defined (8 agents — 4 cũ decomposed → 8 specialized)
✓ Impact analysis (direct + indirect + defects)
✓ Call chain (build flow + subagent-forge flow + runtime flow)
✓ Data flow (inputs, outputs, dependencies)
✓ Affected components (files, functions, knowledge docs)
✓ Evidence traced to specific files/lines (17 evidence blocks)
✓ Architecture document synced (agent-architecture.md v0.0.2)
✓ Roadmaps synced (Temps + skills/ver-3/roadmaps)
✓ Open questions documented (7 items)
✓ Build order recommended (5 priorities + optional)
✓ Agent comparison matrix (8 rows)
✓ Risk assessment (8 risks, updated per re-arch)
```

---

**Document**: `docs/context-to-work/roadmap-analysis-phases/phase-3-context.2026-07-08.md`
**Generated by**: context-before-fix v1.0.0 + Sisyphus re-architecture
**Language**: Vietnamese
**NO Code Changes Made** — Document update only per skill guardrails
**Last synced with**: [agent-architecture.md v0.0.2](file:///home/stveve/Documents/workspace/build-workflow/WASHVN/docs/context-to-work/phase-3/agent-architecture.md) + [03-agent-foundation.md](file:///home/stveve/Documents/workspace/build-workflow/WASHVN/Temps/spec/roadmaps/03-agent-foundation.md)
