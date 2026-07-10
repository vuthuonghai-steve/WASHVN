# Scope Document — Phase 2: Hook Framework Foundation

**Date**: 2026-07-07
**Status**: Initial
**Feature**: Hook Framework Foundation (Phase 2 — 8-Phase Roadmap)

---

## §1: Problem Summary

Phase 2 là phase thứ 3 trong lộ trình Master Skill Suite Rebuild, sau Phase 0 (Foundation Bootstrap — ✅ done) và Phase 1 (Knowledge Base Authoring — ✅ done). Phase này xây dựng **standalone hook framework** tại `.claude/hooks/` — chuyển từ inline hooks-only (hiện tại subagent-forge có 2 inline hooks) sang hệ thống hooks rõ rời, có registry, có unit test cho từng event.

**Tại sao Phase 2 quan trọng:**
- Hooks là **third pillar** của hệ thống Skills + Agents + Hooks
- Skills = nội dung / tri thức
- Agents = trình thực thi
- Hooks = **chốt chặn cơ học** đảm bảo agent tôn trọng luật (không phụ thuộc "self-discipline" của LLM)
- Address architectural defects: **Γ-7** (escalation recursion), **Γ-1** (self-referential blindness)

---

## §2: Entry Point

| Entry | Path | Ghi chú |
|:------|:-----|:--------|
| Roadmap source | `Temps/spec/roadmaps/02-hook-framework.md` | 458 dòng — spec đầy đủ 6 hooks + 7 tests |
| Index roadmap | `Temps/spec/roadmaps/index.md` | Dependency: P0 → P1 → P2 |
| Plan checklist | `docs/context-to-work/roadmap-analysis-phases/plan-checklist.2026-07-07.md` | §7: Phase 2 checklist |
| Hook protocol spec | `.claude/knowledge/agents/hooks_and_events.md` | 551 dòng — Dual-Format blocking, matchers |
| Registry stub | `.claude/hooks/registry.yaml` | Stub hiện tại (13 dòng, chưa có hooks entries) |
| Events dir | `.claude/hooks/events/` | Hiện chỉ có `.gitkeep` — chưa có hook script nào |
| Tests dir | `.claude/hooks/tests/` | Hiện chỉ có `.gitkeep` — chưa có test script nào |
| Suite config | `.skill-context/suite_config.yaml` | Γ-7 fix placeholder, max_history_entries: 20 |

---

## §3: Scope Definition

### 3.1 In Scope

```yaml
in_scope:
  - 6 standalone hook scripts tại .claude/hooks/events/
  - 1 registry.yaml hoàn chỉnh (6 entries)
  - 7 test scripts tại .claude/hooks/tests/
  - D2-9: Advanced Hook experiment (Prompt-based hook cho Stop event — self-healing test)
  - D2-10: Evaluation report cho advanced hook feasibility (prompt vs agent type)
  - Content từ hooks_and_events.md knowledge doc + quality-gates-reference.md
  - Exit code convention: 0 = allow, 2 = block
  - Audit log directory .skill-context/_state-archive/
  - Γ-7 fix: corrupt _state.yaml backup trong stop hook
  - Quality gates cross-cutting: HOOK-HEAL-1.0, HOOK-AUDIT-2.0, YAML-RES-1.0
  - YAML Resilience Layer rule_9 (last-mile verification trên Stop event)
```

### 3.2 Out of Scope

```yaml
out_of_scope:
  - KHÔNG build skill, agent, schema
  - KHÔNG sửa knowledge docs (Phase 1 đã done)
  - KHÔNG deploy hooks vào runtime settings (cần Phase 8 integration)
  - KHÔNG reconcile hook format gap (exit 2 vs stdout JSON) — deferred to Phase 8
  - KHÔNG modify subagent-forge.md inline hooks
  - KHÔNG sửa architecture.md, suite_config.yaml
```

### 3.3 Boundary

- Giới hạn trong `.claude/hooks/` directory
- Hook scripts phải < 50 dòng, < 100ms execution . hạn chế những script có kích thước lớn và tốn thời gian thực thi . ưu tiên giải quyết được vấn đề trực tiếp và ngắn gọn clean nhất có thể  .
- Hook scripts dùng bash (ưu tiên) hoặc sh , có thể dùng thêm jq . hạn chế dùng python , nếu bắt buộc phải dùng python thì cần phải có lý do rõ ràng . và phải đảm bảo python được cài đặt trên hệ thống , khi shell script không thể giải quyết được vấn đề thì mới được phép sử dụng python .
- Không spawn sub-task, không write file (trừ audit logs)
- Advanced Hook experiment (D2-9): dùng settings.local.json — **không sửa** settings.json chính
- Advanced Hook chỉ thử nghiệm ở Stop event (không ảnh hưởng PreToolUse gates)
- D2-9/10 không block Phase 2 core deliverables — research parallel

---

## §4: Impact Analysis

### 4.1 Direct Impact

```yaml
direct_impact:
  files:
    - path: ".claude/hooks/events/pre-tool-use_write_gate.sh"
      status: "need_create"
      description: "Gate writes outside WASHVN workspace"
    - path: ".claude/hooks/events/pre-tool-use_skill_staging_gate.sh"
      status: "need_create"
      description: "Gate writes to runtime .claude/skills/"
    - path: ".claude/hooks/events/pre-tool-use_bash_validate_command.sh"
      status: "need_create"
      description: "Block destructive bash commands"
    - path: ".claude/hooks/events/post-tool-use_log_artifact.sh"
      status: "need_create"
      description: "Audit-log artifact writes"
    - path: ".claude/hooks/events/stop_session_log_state.sh"
      status: "need_create"
      description: "Log session stop, backup corrupt state (Γ-7)"
    - path: ".claude/hooks/events/session-start_record_metadata.sh"
      status: "need_create"
      description: "Record boot metadata"
    - path: ".claude/hooks/registry.yaml"
      status: "need_update"
      description: "Populate 6 hook entries từ stub"
    - path: ".claude/hooks/tests/*"
      status: "need_create"
      description: "7 test scripts: 2 write_gate + 2 staging_gate + 3 bash_validate"
```

### 4.2 Indirect Impact

```yaml
indirect_impact:
  phases_downstream:
    - "Phase 3 — Agents (dependency: hooks active trước khi agents build)"
    - "Phase 5 — BA Skills (hooks gate writes trong skill build)"
    - "Phase 6 — Main Pipeline (hooks protect .skill-context/)"
    - "Phase 8 — Integration (hook format gap reconcile + external validator hook)"
  
  knowledge_docs:
    - path: ".claude/knowledge/agents/hooks_and_events.md"
      impact: "Reference cho hook convention — cần verify consistency với spec"
  
  suite_config:
    - path: ".skill-context/suite_config.yaml"
      impact: "yaml_resilience.max_history_entries: 20 — Γ-7 placeholder trong stop hook"
  
  agents:
    - path: ".claude/agents/subagent-forge.md"
      impact: "Inline hooks vẫn tồn tại song song — cần verify không conflict"
```

---

## §5: Deliverables Map

### 5.1 6 Hook Scripts + 1 Registry + 7 Tests

| ID | Deliverable | Lines | Purpose | Event Type | Matcher | Exit Codes |
|:--:|:------------|:-----:|:--------|:-----------|:--------|:----------:|
| D2-1 | `pre-tool-use_write_gate.sh` | ~20 | Block writes outside WASHVN workspace | PreToolUse | Write\|Edit | 0/2 |
| D2-2 | `pre-tool-use_skill_staging_gate.sh` | ~25 | Block writes to runtime `.claude/skills/` | PreToolUse | Write\|Edit | 0/2 |
| D2-3 | `post-tool-use_log_artifact.sh` | ~15 | Audit-log mọi artifact write | PostToolUse | Write\|Edit | 0 |
| D2-4 | `pre-tool-use_bash_validate_command.sh` | ~25 | Block destructive bash (rm -rf, sudo, dd) | PreToolUse | Bash | 0/2 |
| D2-5 | `stop_session_log_state.sh` | ~35 | Log stop + backup corrupt _state.yaml (Γ-7) | Stop | .* | 0 |
| D2-6 | `session-start_record_metadata.sh` | ~20 | Record boot metadata | SessionStart | .* | 0 |
| D2-7 | `registry.yaml` | ~40 | Registry đầy đủ 6 hooks | — | — | — |
| D2-8 | 7 test scripts | ~15 ea | Hook unit tests | — | — | — |
| D2-9 | Prompt Hook Experiment | ~15 | Prompt-based hook: self-healing on Stop event — `continueOnBlock: true` | Stop | .* | ok: true/false |
| D2-10 | Advanced Hook Eval Report | ~N/A | Feasibility report: prompt vs agent hooks, latency, self-healing | — | — | — |

### 5.2 Test Scripts Matrix

| Test Script | Input | Expected Exit |
|:------------|:------|:-------------:|
| `test_write_gate_allow.sh` | Workspace path: `skills/ver-3/test/SKILL.md` | 0 |
| `test_write_gate_block.sh` | Outside path: `/tmp/test.txt` | 2 |
| `test_skill_staging_allow_staging.sh` | Staging path: `.claude/skills/_staging/test.md` | 0 |
| `test_skill_staging_block_runtime.sh` | Runtime path: `.claude/skills/foo/SKILL.md` | 2 |
| `test_bash_validate_allow.sh` | Normal cmd: `ls -la` | 0 |
| `test_bash_validate_block_destructive.sh` | Destructive: `rm -rf /home` | 2 |
| `test_bash_validate_block_network.sh` | Network: `curl https://example.com` | 2 |

---

## §6: Hook Format Gap — Dual-Format Blocking Protocol

> ⚠️ **ISSUE CẦN LƯU Ý**: hooks_and_events.md (Phase 1) đã document **2 formats**:
> - **Format A**: stdout JSON `{"permissionDecision": "deny"}` → exit 0
> - **Format B**: exit code 2 (stderr message)
>
> Trong khi roadmap Phase 2 spec (từ Temps/spec/roadmaps/02-hook-framework.md) chỉ dùng **Format B** (exit 2).
>
> **Tác động**:
> - hooks_and_events.md §6 khuyến nghị Format A cho multiple hooks chain, Format B cho standalone
> - Roadmap spec D2-1→D2-6 dùng `exit 2` thuần túy
> - Quyết định: **giữ Format B cho Phase 2** (roadmap spec), **defer reconcile đến Phase 8** hoặc khi cần chain hooks
>
> **Evidence**:
> - File: `.claude/knowledge/agents/hooks_and_events.md` (lines 266-342)
> - File: `Temps/spec/roadmaps/02-hook-framework.md` (lines 58-76 — D2-1 dùng exit 2)
> - File: `plan-checklist.2026-07-07.md` (line 1098 — Open Question #3)

---

## §7: Call Chain

### 7.1 Hook Lifecycle trong Claude Code

```text
Session Start
  └── SessionStart event
       └── D2-6: session-start_record_metadata.sh → log metadata → exit 0

Per-Turn Loop (mỗi tool call)
  ├── PreToolUse (Write|Edit)
  │    ├── D2-1: write_gate.sh → check path allowlist → exit 0|2
  │    └── D2-2: skill_staging_gate.sh → check runtime path → exit 0|2
  │
  ├── PreToolUse (Bash)
  │    └── D2-4: bash_validate_command.sh → check destructive patterns → exit 0|2
  │
  └── PostToolUse (Write|Edit)
       └── D2-3: log_artifact.sh → append to audit log → exit 0

Session End (Ctrl-C / /stop / error)
  └── Stop event
       └── D2-5: stop_session_log_state.sh
            ├── log session stop to audit
            └── check _state.yaml corrupt → backup if corrupt (Γ-7) → exit 0
```

### 7.2 Dependencies

```yaml
prerequisites:
  - "Phase 0 done: scaffold dirs tồn tại (.claude/hooks/events/, .claude/hooks/tests/)"
  - "Phase 1 done: hooks_and_events.md knowledge doc available (551 dòng)"
  - "jq CLI installed (đã verify tại Phase 0)"
  - "bash >= 4.0 hoặc zsh"
  
output_dependencies:
  - "Phase 3: agents reference hooks (inline + standalone)"
  - "Phase 5/6/7: hooks gate skill writes"
  - "Phase 8: reconcile format gap, add external_validator hook"
```

---

## §8: Data Flow

### 8.1 Input Format (stdin JSON mỗi hook)

```yaml
pre_tool_use_input:
  format: "stdin JSON"
  fields:
    - tool_name: string        # "Write", "Edit", "Bash"
    - tool_input:
        file_path: string      # Write/Edit target
        command: string        # Bash command
        content: string        # Write content

stop_input:
  format: "stdin JSON"
  fields:
    - stop_hook_active: bool

session_start_input:
  format: "stdin JSON"
  fields:
    - cwd: string
    - pid: number
    - boot_id: string
    - session_id: string

post_tool_use_input:
  format: "stdin JSON"
  fields:
    - tool_name: string
    - tool_input: object
    - tool_output: object
```

### 8.2 Output (side effects)

```yaml
audit_logs:
  - path: ".skill-context/_state-archive/tool-audit-{YYYY-MM-DD}.log"
    format: "TSV: timestamp\ttool\tpid\tagent\tpath"
    created_by: "D2-3 post-tool-use_log_artifact.sh"
  
  - path: ".skill-context/_state-archive/session-{YYYY-MM-DD}.log"
    format: "TSV: timestamp\tSTOP\tstop_hook_active=bool"
    created_by: "D2-5 stop_session_log_state.sh"
  
  - path: ".skill-context/_state-archive/session-start.log"
    format: "TSV: timestamp\tSTART\tsession=id\tpid=num\tboot=id\tcwd=path"
    created_by: "D2-6 session-start_record_metadata.sh"

backup:
  - path: ".skill-context/_state-archive/_state-{timestamp}-corrupt.yaml"
    condition: "_state.yaml corrupt (YAML parse fail)"
    created_by: "D2-5 stop hook (Γ-7 fix)"
```

### 8.3 Allowlist Paths (Write Gate)

```yaml
allowed_prefixes:
  - ".claude/"
  - "skills/ver-3/"
  - ".skill-context/"
  - "docs/context-to-work/"
  - "Temps/spec/"
  
blocked_patterns:
  - ".claude/skills/<any>/"           # skill_staging_gate
  - "/tmp/"                           # outside workspace
  - "/etc/"                           # system files
```

---

## §9: Affected Components

### 9.1 Files Created

```text
.claude/hooks/events/
├── pre-tool-use_write_gate.sh          (NEW)
├── pre-tool-use_skill_staging_gate.sh  (NEW)
├── pre-tool-use_bash_validate_command.sh (NEW)
├── post-tool-use_log_artifact.sh       (NEW)
├── stop_session_log_state.sh           (NEW)
└── session-start_record_metadata.sh    (NEW)

.claude/hooks/registry.yaml             (UPDATE — từ stub lên full)
.claude/hooks/tests/
├── test_write_gate_allow.sh            (NEW)
├── test_write_gate_block.sh            (NEW)
├── test_skill_staging_allow_staging.sh (NEW)
├── test_skill_staging_block_runtime.sh (NEW)
├── test_bash_validate_allow.sh         (NEW)
├── test_bash_validate_block_destructive.sh (NEW)
└── test_bash_validate_block_network.sh (NEW)
```

### 9.2 Files Modified

```text
.claude/hooks/registry.yaml             # Phase 0 stub → populate 6 entries
```

### 9.3 Files Reference (Read-Only)

```text
.claude/knowledge/agents/hooks_and_events.md   # Hook protocol spec
.claude/knowledge/agents/configuration.md      # Frontmatter reference
.skill-context/suite_config.yaml               # yaml_resilience config
```

---

## §10: Acceptance Criteria Check

| AC | Mô tả | Verification Command | Dự kiến PASS |
|:--:|:------|:---------------------|:------------:|
| AC-1 | 6 hook scripts tồn tại + executable | `for hook in ...; do test -f + test -x` | ✅ |
| AC-2 | Registry parses + 6 entries | `python3 -c "yaml.safe_load; assert len(hooks)==6"` | ✅ |
| AC-3 | Hook tests pass (7 scripts) | `for test in ...; do bash $test` | ✅ |
| AC-4 | Hook self-test (allow 0, block 2) | Pipe JSON → verify exit code | ✅ |
| AC-5 | Corrupt state backup (Γ-7) | Simulate corrupt YAML → verify backup | ✅ |
| AC-6 | Bash validate distinguish | `ls -la` exit 0, `rm -rf /home` exit 2 | ✅ |
| AC-7 | subagent-forge.md inline hooks validated | `grep "PreToolUse" subagent-forge.md` | ✅ |
| AC-8 | Prompt-based Hook experiment hoạt động: Claude Code nhận decision ok:false + hiển thị reason + tiếp tục turn | Verify settings.local.json config + test run with corrupt doc | ✅ |

**Total AC: 8** | **Total Tasks: 11** | **Total Files: 16**

---

## §11: Evidence

<evidence>
<file>Temps/spec/roadmaps/02-hook-framework.md</file>
<line>1-458</line>
<finding>Full Phase 2 spec — 6 hooks, 7 tests, AC-1 đến AC-7, DoD</finding>
</evidence>

<evidence>
<file>.claude/knowledge/agents/hooks_and_events.md</file>
<line>266-342</line>
<finding>Dual-Format Blocking Protocol — Format A (stdout JSON) vs Format B (exit 2). Phase 2 dùng Format B.</finding>
</evidence>

<evidence>
<file>.claude/hooks/registry.yaml</file>
<line>1-13</line>
<finding>Registry stub hiện tại — chỉ có header, chưa có hooks entries. Phase 2 cần populate.</finding>
</evidence>

<evidence>
<file>.claude/hooks/events/</file>
<line>1</line>
<finding>Chỉ có .gitkeep — chưa có hook script nào. Phase 2 cần tạo 6 files.</finding>
</evidence>

<evidence>
<file>.claude/hooks/tests/</file>
<line>1</line>
<finding>Chỉ có .gitkeep — chưa có test script nào. Phase 2 cần tạo 7 files.</finding>
</evidence>

<evidence>
<file>docs/context-to-work/roadmap-analysis-phases/plan-checklist.2026-07-07.md</file>
<line>279-338</line>
<finding>Phase 2 checklist — 9 tasks, 7 AC, DoD, progress dashboard</finding>
</evidence>

<evidence>
<file>.skill-context/suite_config.yaml</file>
<line>15</line>
<finding>yaml_resilience.max_history_entries: 20 — Γ-7 placeholder cho stop hook corrupt state check</finding>
</evidence>

<evidence>
<file>Temps/spec/roadmaps/08-integration-tests-hardening.md</file>
<line>38-55</line>
<finding>A1 — Phase 8 sẽ add external_validator hook (hook thứ 7), cần verify registry có thể extend</finding>
</evidence>

---

## §12: Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|:-----|:----------:|:------:|:-----------|
| Hook script chậm >100ms ảnh hưởng UX | Low | Medium | Giới hạn <50 dòng, dùng bash+jq, không spawn subprocess |
| Format A vs Format B conflict khi chain hooks | Medium | High | Phase 2 dùng Format B thuần — format gap note để Phase 8 reconcile |
| jq không có sẵn trên PATH | Low | High | Verify jq tại Phase 0 prereq; fallback dùng python3 -c "import json" |
| _state.yaml corrupt detection không chính xác | Medium | Medium | Stop hook dùng pyyaml để parse; nếu không có python3, skip check |
| Hook block nhầm legitimate writes | Medium | High | Allowlist regex phải chính xác; test kỹ allow cases |
| Registry không khớp Claude Code runtime expectation | Medium | High | Claude Code hooks cần settings.json + registry.yaml — Phase 8 integration sẽ verify |

---

## §13: Tài Liệu Tham Khảo Chi Tiết

### 13.1 Source Spec (Roadmap)

| File | Nội dung | Dòng chính |
|:-----|:---------|:-----------|
| `Temps/spec/roadmaps/02-hook-framework.md` | Phase 2 spec hoàn chỉnh | Line 34-48: design principles |
| | | Line 50-285: 6 hook scripts code + registry |
| | | Line 286-317: 7 test scripts |
| | | Line 322-399: AC-1 đến AC-7 verification commands |
| | | Line 403-458: Task list + DoD |

### 13.2 Knowledge Docs (Phase 1 — Đã có)

| File | Nội dung | Dòng chính |
|:-----|:---------|:-----------|
| `hooks_and_events.md` | Hook protocol spec | Line 57-114: hook config schema |
| | | Line 151-193: matcher syntax |
| | | Line 197-261: core events (4 events) |
| | | Line 266-342: Dual-Format Blocking Protocol |
| | | Line 520-551: error handling + cross-refs |

### 13.3 Checklist Tracking

| File | Nội dung |
|:-----|:---------|
| `plan-checklist.2026-07-07.md` §7 | Phase 2 checklist (9 tasks, 7 AC, DoD) |
| `plan-checklist.2026-07-07.md` §15 | Cross-phase metrics dashboard |
| `plan-checklist.2026-07-07.md` §16 | Status tracking protocol |

### 13.4 Quality & Resilience References (New — Cross-Cutting)

| File | Nội dung | Liên quan Phase 2 |
|:-----|:---------|:------------------|
| `Temps/spec/architects/shared/quality-gates-reference.md` | Quality gates cross-cutting — HOOK-HEAL-1.0, HOOK-AUDIT-2.0, YAML-RES-1.0 | HOOK-HEAL-1.0 → D2-9 Prompt Hook Experiment |
| | | YAML-RES-1.0 → D2-5 Γ-7 fix (YAML pre-check) |
| | | HOOK-AUDIT-2.0 → Future Phase 8 integration |
| `Temps/spec/architects/P5-fallback-and-escalation/yaml-resilience-layer.md` | YAML Resilience Layer spec — 3-level pre-check, auto-repair protocol, rule_9 | rule_9: last-mile verification on Stop — direct mapping to D2-5 + D2-9 |
| | | L1 Syntax check (pyyaml) — D2-5 corrupt state detection |
| | | Auto-repair (max 2 attempts) — context cho graceful degradation |

### 13.5 Context-to-Work Docs (Đã có — Reference)

| File | Mục đích |
|:-----|:---------|
| `scope.2026-07-07.md` | Scope analysis tổng thể — xác định Phase 0 priority |
| `phase-0-implementation-plan.md` | Phase 0 detailed plan (10 tasks, 27 files) |
| `tai-lieu-ho-tro-phase-0.md` | Supporting docs từ knowledge base hiện có |
| `phase-2-plan.2026-07-07.md` | Implementation plan — Stage 5 Advanced Hooks Research, AC-8 |
| `advanced-hooks-capability.2026-07-07.md` | Research doc về Prompt/Agent-based hooks capabilities |

---

## §14: Recommendations cho Implementation

### 14.1 Thứ tự build khuyến nghị

```text
Step 1: D2-1 → write_gate.sh           (basic gate — dễ test nhất)
Step 2: D2-4 → bash_validate.sh         (second gate — pattern blocking)
Step 3: D2-2 → skill_staging_gate.sh    (third gate — DEPLOY_PHASE_ACTIVE pattern)
Step 4: D2-3 → log_artifact.sh          (audit — no block logic, pure log)
Step 5: D2-6 → session-start.sh         (metadata recording)
Step 6: D2-5 → stop_log_state.sh        (Γ-7 — corrupt backup logic, cần python3)
Step 7: D2-7 → registry.yaml            (compile all 6 entries)
Step 8: D2-8 → 7 test scripts           (per hook allow/block pairs)
Step 9: Run AC-1 đến AC-7               (full verification)
Step 10: D2-9 → Prompt Hook Experiment  (Stop event self-healing — settings.local.json)
Step 11: D2-10 → Advanced Hook Eval Report (feasibility analysis for Phase 8)
```

### 14.2 Lưu ý đặc biệt

1. **Format gap**: hooks_and_events.md khuyến nghị Format A cho chain hooks, roadmap dùng Format B. Phase 2 **giữ Format B**. Nếu cần chain nhiều hooks trong tương lai, Phase 8 sẽ migrate.

2. **Γ-7 corrupt backup** (D2-5): Cần `python3` để parse YAML. Nếu python3 không available → skip corrupt check (graceful degradation). Dòng 183-192 trong roadmap spec code mẫu đã handle.

3. **DEPLOY_PHASE_ACTIVE** (D2-2): Env var pattern cho phép bypass staging gate khi deploy chính thức. Phase 2 không deploy nên mặc định block.

4. **Audit log path**: `".skill-context/_state-archive/"` — đã được Phase 0 tạo. Mỗi hook script xác định log file khác nhau (tool-audit, session, session-start).

5. **Network block** (D2-4): Dùng `MARK_NETWORK_ALLOWED` env var để cho phép sandbox-tester (Phase 7) bypass network restriction.

6. **subagent-forge.md inline hooks vẫn tồn tại**: Standalone hooks Phase 2 là layered defense, không replace inline hooks. Cả 2 cùng hoạt động.

7. **Two-Layer Hook Design Principle** (02-hook-framework.md §Design principles):
   - **Layer 1 — Command-based (Mechanical)**: D2-1→D2-6 — bash+jq, <50 dòng, <100ms, exit 2 blocking. Fast, deterministic.
   - **Layer 2 — Prompt/Agent-based (Semantic)**: D2-9 experiment — LLM evaluation, self-healing với `continueOnBlock: true`. Slow (>30s) nhưng thông minh.
   - Layer 2 chỉ dùng ở Stop/SessionStart (thưa thớt) — không dùng ở PreToolUse (mỗi tool call).

8. **YAML Resilience Layer Integration**: D2-5 stop hook implement L1 Syntax check (pyyaml parse) của YAML Resilience Layer spec. rule_9 của yaml-resilience-layer.md yêu cầu HOOK-HEAL-1.0 (Prompt-based hook) làm last-mile verification — đây chính là D2-9 experiment. Phase 2 hooks là runtime implementation của architectural resilience design.

---

## §15: Confidence Assessment

```yaml
overall_confidence: 90%

breakdown:
  spec_completeness: 95%         # Roadmap spec rất chi tiết (458 dòng)
  code_readiness: 90%            # Code mẫu đã có sẵn trong spec
  test_coverage: 85%             # 7 test scripts cover allow/block pairs
  dependency_ready: 100%         # Phase 0 + Phase 1 đều done
  format_gap_awareness: 80%      # Format A/B gap đã identify, defer đến Phase 8
  risk_mitigation: 85%           # All risks have mitigation plans

uncertainty_flags:
  - "Hook format gap: Đã thống nhất giữ Format B (exit 2) cho Phase 2, reconcile ở Phase 8"
  - "Claude Code runtime có tôn trọng registry.yaml format hiện tại? Cần test thực tế tại Phase 8"
  - "stop hook corrupt YAML detection dùng python3 — nếu python3 không available thì skip"
```

---

## §16: Open Questions

| # | Question | Priority | Status |
|--:|:---------|:--------:|:------:|
| 1 | Hook format reconcile: exit 2 (roadmap) vs stdout JSON (Claude Code) — khi nào reconcile? | High | Resolved (Keep B for P2, reconcile in P8) |
| 2 | jq CLI có sẵn trên PATH? (prerequisite cho hook scripts) | High | Assumed (Phase 0 ghi prereq) |
| 3 | Claude Code settings.json có cần update để active hooks? | Medium | Need test tại Phase 8 |
| 4 | Corrupt YAML detection — python3 có luôn available? | Medium | Fallback: skip check |
| 5 | `DEPLOY_PHASE_ACTIVE` env var mechanism — ai set? khi nào? | Low | Defer đến deploy decision |

---

## §17: Phase 2 Task Breakdown (9 tasks)

| Task | Deliverable | Files | Effort | AC |
|:----:|:------------|:-----:|:------:|:--:|
| 1 | D2-1: write_gate.sh | 1 script | Small | AC-1,4 |
| 2 | D2-2: skill_staging_gate.sh | 1 script | Small | AC-1,4 |
| 3 | D2-4: bash_validate.sh | 1 script | Small | AC-1,4,6 |
| 4 | D2-3: log_artifact.sh | 1 script | Small | AC-1 |
| 5 | D2-5: stop_log_state.sh | 1 script | Small | AC-1,5 |
| 6 | D2-6: session-start.sh | 1 script | Small | AC-1 |
| 7 | D2-7: registry.yaml | 1 file | Small | AC-2 |
| 8 | D2-8: 7 test scripts | 7 scripts | Medium | AC-3,4 |
| 9 | Run AC-1→AC-7 | — | Small | AC-1→7 |
| 10 | D2-9: Prompt Hook Experiment (Stop event, self-healing) | 1 config + 1 test | Small | AC-8 |
| 11 | D2-10: Advanced Hook Eval Report | 1 report | Small | AC-8 |

**Total: 16 files | ~260 dòng code | Estimated: 1-2 sessions**

---

## §18: Quality Checklist

```yaml
pre_delivery_check:
  entry_point_identified: true        # Temps/spec/roadmaps/02-hook-framework.md
  all_related_files_searched: true    # 26 files read
  impact_map_direct: true             # 14 files (8 create + 1 update + 5 reference)
  impact_map_indirect: true           # 4 phases downstream + 3 knowledge areas
  evidence_specific: true             # 7 evidence blocks with file:line
  confidence_assessment_done: true    # 90%
  document_written_in_vietnamese: true
  document_saved_correct_path: true   # docs/context-to-work/roadmap-analysis-phases/phase-2-scope.2026-07-07.md
  no_code_changes_made: true          # Document only
```

---

**Document Status**: Context Complete — Ready for Phase 2 Implementation
**NO Code Changes Made** — Document only per context-before-fix skill guardrails

```
✓ Problem Summary — Phase 2 mission, importance, architectural defects addressed
✓ Entry Point — 7 entry points mapped with ghi chú
✓ Scope Definition — in scope (14 files) + out of scope + boundary
✓ Impact Analysis — direct (14 files) + indirect (4 phases, 3 knowledge areas)
✓ Deliverables Map — 6 hooks + 1 registry + 7 tests with line counts
✓ Hook Format Gap — Format A vs B documented with defer decision
✓ Call Chain — lifecycle flow + dependency graph
✓ Data Flow — input format (stdin JSON) + output (logs) + allowlist
✓ Affected Components — created vs modified vs reference files
✓ Acceptance Criteria — 7 AC mapped
✓ Evidence — 7 evidence blocks with file:line
✓ Risk Assessment — 6 risks with mitigation
✓ Reference Documents — all source specs + knowledge docs mapped
✓ Recommendations — build order + 6 special notes
✓ Confidence Assessment — 90% với uncertainty flags
✓ Open Questions — 5 questions tracked
```

---

---

## §19: Official Claude Code Hooks Documentation — Findings

> **Nguồn**: `.claude/knowleages/hooks/hooks.md` (official Anthropic docs) + `.claude/knowleages/agents/agent.md`
> **Phát hiện ngày**: 2026-07-07

### 19.1 Cấu trúc Hook Configuration (Official)

Theo official docs, hooks được cấu hình trong **JSON settings files** (`settings.json`), **không phải** YAML registry:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PROJECT_DIR}/.claude/hooks/pre-tool-use_write_gate.sh",
            "args": []
          }
        ]
      }
    ]
  }
}
```

Cấu trúc 3 levels:
1. **Hook event**: `PreToolUse`, `PostToolUse`, `Stop`, `SessionStart`, ...
2. **Matcher group**: Lọc theo tool name (`"Bash"`, `"Write|Edit"`, `"mcp__.*"`)
3. **Hook handler**: Shell command, HTTP endpoint, MCP tool, prompt, agent

### 19.2 ⚠️ Format Gap — Roadmap Spec vs Official Reality

Phát hiện **3 inconsistencies** giữa roadmap spec và official hooks documentation:

| Aspect | Roadmap Spec (Phase 2) | Phase 1 Knowledge Doc | Official Claude Code Docs |
|:-------|:----------------------|:---------------------|:--------------------------|
| **Blocking format** | Format B: `exit 2` | Format A: `{"permissionDecision": "deny"}` | `{ hookSpecificOutput: { hookEventName, permissionDecision, permissionDecisionReason } }` |
| **Config format** | `registry.yaml` (YAML) | — | `settings.json` (JSON) |
| **Input JSON** | `{ tool_name, tool_input }` | `{ tool, params }` | `{ session_id, tool_name, tool_input, cwd, permission_mode, hook_event_name }` |

### 19.3 Input JSON Schema Chi Tiết (Official)

PreToolUse hook nhận stdin:

```json
{
  "session_id": "abc123",
  "prompt_id": "550e8400-e29b-41d4-a716-446655440000",
  "transcript_path": "/home/user/.claude/projects/.../transcript.jsonl",
  "cwd": "/home/user/my-project",
  "permission_mode": "default",
  "hook_event_name": "PreToolUse",
  "tool_name": "Bash",
  "tool_input": {
    "command": "npm test"
  }
}
```

### 19.4 Permission Decision Format (Official)

Khi muốn block:

```bash
#!/bin/bash
# Format: exit 0 + stdout JSON (official)
command=$(jq -r '.tool_input.command' < /dev/stdin)
if [[ "$command" == rm* ]]; then
  jq -n '{
    hookSpecificOutput: {
      hookEventName: "PreToolUse",
      permissionDecision: "deny",
      permissionDecisionReason: "Destructive command blocked"
    }
  }'
  exit 0
fi
exit 0
```

Hoặc đơn giản hơn (Format B):

```bash
#!/bin/bash
# Format: exit 2 + stderr (simpler)
command=$(jq -r '.tool_input.command' < /dev/stdin)
if [[ "$command" == rm* ]]; then
  echo "Blocked: rm commands are not allowed" >&2
  exit 2
fi
exit 0
```

### 19.5 Exit Code Behavior

| Exit Code | Meaning | JSON processed? |
|:---------:|:--------|:---------------:|
| 0 | Success — allow (nếu không có permissionDecision) | ✅ Yes |
| 2 | Blocking error — block tool call | ❌ No (stdout ignored) |
| Other | Non-blocking error — allow + log | ❌ No |

> ⚠️ **Warning from official docs**: Only exit code 2 blocks. Exit code 1 is treated as non-blocking error and proceeds!

### 19.6 Matcher Pattern Rules

| Pattern type | Characters | Example |
|:-------------|:-----------|:--------|
| Exact match | letters, digits, `_`, `-`, spaces, `,`, `\|` | `"Bash"`, `"Write\|Edit"` |
| Regex match | contains any other chars | `"^mcp__memory__.*"` |

### 19.7 Hook Handler Types

| Type | Description | Use case |
|:-----|:------------|:---------|
| `command` | Run shell script | Phase 2 hooks (bash + jq) |
| `http` | HTTP POST to endpoint | Remote validation |
| `mcp_tool` | Call MCP server tool | Validate với external tool |
| `prompt` | LLM prompt (single-turn) | AI-based decision |
| `agent` | Spawn subagent | Complex verification |

### 19.8 Key Differences: `settings.json` vs `registry.yaml`

Official docs sử dụng `settings.json` để cấu hình hooks:

| Location | Scope | Priority |
|:---------|:------|:--------:|
| `~/.claude/settings.json` | User-wide | Low |
| `.claude/settings.json` | Project | Medium |
| `.claude/settings.local.json` | Project local | Medium |
| Managed policy | Org-wide | High |
| Plugin `hooks/hooks.json` | Plugin-scoped | Medium |
| Skill/Agent frontmatter | Per-component | High |

**registry.yaml** trong roadmap spec là convention riêng của WASHVN để tracking, **không phải** format Claude Code đọc. Phase 8 integration cần bridge registry.yaml → settings.json.

### 19.9 Additional Context Feature

Official hooks có thể inject context vào conversation:

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PostToolUse",
    "additionalContext": "This file is generated. Edit src/schema.ts instead."
  }
}
```

Phase 2 có thể ignore feature này (Phase 8 integration sẽ dùng).

### 19.10 Implications cho Phase 2

```yaml
implications:
  hook_scripts:
    - "Scripts trong roadmap spec (Format B: exit 2) vẫn compatible với official runtime"
    - "Không cần thay đổi code — roadmap spec dùng format đơn giản hơn nhưng đúng"
  
  config_format:
    - "registry.yaml là WASHVN tracking convention — cần bridge sang settings.json tại Phase 8"
    - "Phase 2 chỉ populate registry.yaml như roadmap spec"
  
  input_json:
    - "Roadmap spec giả định input đơn giản hơn reality"
    - "Scripts dùng `jq -r '.tool_input.command'` vẫn work (field tồn tại trong cả 2 format)"
    - "Cần verify thêm field path: official dùng `.tool_input.file_path` (roadmap dùng `.tool_input.file_path` — giống nhau)"
  
  format_gap_resolution:
    - "Quyết định: giữ Format B (exit 2) cho Phase 2 — đơn giản, đúng spec"
    - "Phase 8 integration sẽ migrate lên official format nếu cần chain hooks"
```

### 19.11 Evidence

<evidence>
<file>.claude/knowleages/hooks/hooks.md</file>
<line>591-635</line>
<finding>Official input JSON schema — PreToolUse nhận session_id, tool_name, tool_input với command field</finding>
</evidence>

<evidence>
<file>.claude/knowleages/hooks/hooks.md</file>
<line>640-666</line>
<finding>Exit code behavior: 0 = success (JSON parsed), 2 = block, other = non-blocking error</finding>
</evidence>

<evidence>
<file>.claude/knowleages/hooks/hooks.md</file>
<line>824-896</line>
<finding>Permission decision format: hookSpecificOutput.hookEventName + permissionDecision (khác Format A trong knowledge doc)</finding>
</evidence>

<evidence>
<file>.claude/knowleages/hooks/hooks.md</file>
<line>156-185</line>
<finding>Hook locations: settings.json (JSON), skill/agent frontmatter (YAML) — registry.yaml là WASHVN convention riêng</finding>
</evidence>

<evidence>
<file>.claude/knowleages/agents/agent.md</file>
<line>514-550</line>
<finding>Subagent hooks: PreToolUse hooks in subagent frontmatter, Format B (exit 2) validation example</finding>
</evidence>

---

## §20: Phase 1 Knowledge Docs — Hook-Relevant Context

> **Nguồn**: 7 canonical knowledge docs tại `.claude/knowledge/agents/` (Phase 1 — done)
> **Tổng cộng đã đọc**: 7 files = 2,603 dòng content

### 20.1 `configuration.md` — Hook Field Schema

Field #10 trong 16-field frontmatter schema defines hook configuration:

```yaml
field_10_hooks:
  type: object
  keys: [PreToolUse, PostToolUse, Stop, SessionStart]
  structure: |
    Mỗi key chứa array of hook scripts với `matcher` và `hook` fields
    Hook scripts: stdin JSON → exit 0 = allow, exit 2 = block
  note: "Xác nhận roadmap spec dùng Format B (exit 2) là đúng — official schema hỗ trợ"
```

**Impact Phase 2**: Xác nhận hook field structure trong agent frontmatter hoàn toàn tương thích với standalone hook scripts Phase 2 build.

<evidence>
<file>.claude/knowledge/agents/configuration.md</file>
<line>40-41</line>
<finding>Hook field schema: Keys PreToolUse, PostToolUse, Stop, SessionStart. Scripts stdin JSON, exit 0=allow, exit 2=block.</finding>
</evidence>

---

### 20.2 `capability_controls.md` — Risk Matrix & Anti-Patterns

Tài liệu này document các anti-pattern mà **Phase 2 hooks prevent**:

| Anti-Pattern | Severity | Phase 2 Hook |
|:-------------|:--------:|:-------------|
| Write + acceptEdits without hook — silent file overwrites | **High** | D2-1 write_gate → block writes outside allowlist |
| Nested bypassPermissions agents — cascading permission escalation | **Critical** | D2-2 staging_gate + D2-4 bash_validate |
| Bash + bypassPermissions — unrestricted shell execution | **Critical** | D2-4 bash_validate → block destructive commands |
| Wildcard MCP allow — dangerous filesystem/browser tools | **High** | D2-4 network block (`MARK_NETWORK_ALLOWED`) |
| Agent(agent_type) omitted — unlimited children spawning | **Medium** | D2-2 staging gate prevention |

**Tool Restriction Patterns** cung cấp reference patterns cho subagent tool scoping:

```yaml
# codegen pattern — acceptEdits cần hook review gate
codegen:
  permissionMode: acceptEdits  # cần pairing với hook
  disallowedTools:
    - Bash
```

**Impact Phase 2**: 
- capability_controls.md xác nhận **tại sao** Phase 2 hooks cần thiết — chúng enforce các security constraints
- Risk matrix cung cấp justification cho từng hook
- D2-1 write_gate trực tiếp prevent "Write + acceptEdits without hook" (High severity)

<evidence>
<file>.claude/knowledge/agents/capability_controls.md</file>
<line>260-268</line>
<finding>Risk matrix: Write+acceptEdits without hook = High severity. Phase 2 hooks address this.</finding>
</evidence>

---

### 20.3 `examples.md` — db-reader: Reference Hook Pattern

**Đây là pattern quan trọng nhất cho Phase 2**. examples.md cung cấp 1 reference hook implementation hoàn chỉnh:

**Hook config trong agent frontmatter**:
```yaml
hooks:
  - matcher: "bash"
    handlers:
      - event: PreToolUse
        script: "validate-readonly-query.sh"
        description: "Block write SQL commands before execution"
```

**Hook script implementation**:
```bash
#!/bin/bash
# validate-readonly-query.sh
INPUT=$(cat)
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // empty')

if echo "$COMMAND" | grep -iE '\b(INSERT|UPDATE|DELETE|DROP|CREATE|ALTER|TRUNCATE)\b' > /dev/null; then
  echo "Blocked: Only SELECT queries are allowed" >&2
  exit 2
fi
exit 0
```

**Cấu trúc chuẩn** mà Phase 2 scripts nên follow:
1. `INPUT=$(cat)` — read stdin JSON
2. `jq -r` — extract field
3. `if ...` — check condition
4. `echo "..." >&2` — error message to stderr
5. `exit 2` — block
6. `exit 0` — allow

**Impact Phase 2**: Template này là **reference implementation** cho tất cả 6 hook scripts. Mỗi script Phase 2 nên follow exact pattern:
- D2-1 write_gate: replace SQL check → path allowlist check
- D2-2 staging_gate: replace → `.claude/skills/` runtime check
- D2-4 bash_validate: replace → destructive patterns check

<evidence>
<file>.claude/knowledge/agents/examples.md</file>
<line>215-305</line>
<finding>db-reader pattern: PreToolUse hook + validate-readonly-query.sh script. Reference pattern cho Phase 2 hook scripts.</finding>
</evidence>

---

### 20.4 `hooks_and_events.md` — Dual-Format Protocol (Chi tiết)

Đã document ở §6 và §19. Bổ sung thêm:

**§10 Error Handling** (lines 520-551):
```yaml
hook_error_policy:
  on_script_not_found:
    behavior: "fail closed — block the tool call"
  on_timeout:
    threshold: "30 seconds per handler invocation"
    behavior: "fail closed — block"
  on_parse_error:
    scenario: "Format A script produces invalid JSON"
    behavior: "fall back to Format B exit code evaluation"
  on_non_zero_not_2:
    behavior: "fail open — allow tool call, log error"
  on_chain_break:
    behavior: "first denied decision wins; subsequent hooks skipped"
```

**Impact Phase 2**:
- Cần đảm bảo script path đúng (fail closed nếu script not found)
- Timeout 30s — scripts phải <100ms, không risk timeout
- Nếu script exit code ≠ 0 và ≠ 2 → fail open (tool call vẫn proceed, chỉ log error)
- Chain break: first deny wins — hooks có thể chain

<evidence>
<file>.claude/knowledge/agents/hooks_and_events.md</file>
<line>499-518</line>
<finding>Error handling policy: fail closed on missing script, fail open on unexpected exit code, chain break on first deny.</finding>
</evidence>

---

### 20.5 `workflow_patterns.md` — Context cho Hook Design

Không trực tiếp về hooks, nhưng cung cấp context quan trọng:

**Recursion protection** (Phase 2 D2-2 staging gate cần biết):
```yaml
cascading_agents:
  max_depth: 2
  note: "Root → Subagent (level 1) → Subagent (level 2) — max"
```

**Token cost estimates** — hooks cần lightweight:
| Pattern | Tokens |
|:--------|:------:|
| Foreground Explore | ~5k-10k |
| Background Explore | ~10k-25k |

**Impact Phase 2**: 
- Hooks là synchronous (chạy mỗi tool call) — cần lightweight (<100ms, <50 dòng)
- cascade depth limit = 2 — staging gate D2-2 cần verify không spawn subagent từ hook

<evidence>
<file>.claude/knowledge/agents/workflow_patterns.md</file>
<line>160-191</line>
<finding>Cascading agents max depth = 2. Token costs confirm hooks must be lightweight.</finding>
</evidence>

---

### 20.6 `suite_config.yaml` — Config Parameters cho Phase 2 Hooks

```yaml
state_archive:
  path: ".skill-context/_state-archive/"     # D2-3 audit log, D2-5 backup path
  pre_reinit_backup: required                 # Γ-7 fix — D2-5 stop hook implements

yaml_resilience:
  max_history_entries: 20                     # D2-5 stop hook reference cho history size
  max_repair_attempts_per_artifact: 2         # Recovery context
```

**Impact Phase 2**:
- D2-5 stop hook cần đọc `suite_config.yaml` để biết archive path
- `pre_reinit_backup: required` là Γ-7 fix chính — stop hook phải backup corrupt state
- `_state-archive/` path phải match với D2-3 audit log path

<evidence>
<file>.skill-context/suite_config.yaml</file>
<line>1-22</line>
<finding>state_archive.path, pre_reinit_backup, max_history_entries — config parameters cho Phase 2 hooks</finding>
</evidence>

---

### 20.7 Summary: Knowledge Context → Phase 2 Hooks Mapping

| Phase 1 Knowledge Doc | Nội dung khai thác | Phase 2 Deliverable | Relevance |
|:----------------------|:-------------------|:--------------------|:----------|
| **configuration.md** §1.1 Field #10 | Hook field schema → exit 0/2 | All 6 hooks | Confirm Format B đúng |
| **capability_controls.md** Risk Matrix | Anti-pattern justification | D2-1, D2-2, D2-4 | **Explain WHY** mỗi hook cần thiết |
| **examples.md** db-reader | Reference hook script pattern | All 6 hooks | **Reference template** cho script code |
| **hooks_and_events.md** §5-6 | Dual-Format protocol | D2-1 → D2-6 | Protocol compliance |
| **hooks_and_events.md** §10 | Error handling policy | All hooks | Graceful degradation |
| **workflow_patterns.md** §5 | Cascade depth = 2 | D2-2 staging gate | Recursion prevention context |
| **suite_config.yaml** | state_archive path, Γ-7 config | D2-3, D2-5 | Config file reference |
| **xml_tags_standards.yaml** | (Không liên quan) | — | — |
| **forks.md** | (Không liên quan) | — | — |

---

## §21: Phase 0 Docs — Context cho Phase 2 Build

> **Nguồn**: `docs/context-to-work/roadmap-analysis-phases/phase-0-implementation-plan.md` + `tai-lieu-ho-tro-phase-0.md`

### 21.1 Directory Structure đã có sẵn

Phase 0 đã scaffold:
```text
.claude/hooks/
├── events/                    # ✅ Empty — Phase 2 fills 6 scripts
├── tests/                     # ✅ Empty — Phase 2 fills 7 tests
└── registry.yaml              # ✅ Stub — Phase 2 populates 6 entries
```

### 21.2 Validate Suite Integrity Script

`.claude/scripts/validate_suite_integritity.py` có thể mở rộng để:
- Verify hooks exist + executable
- Verify registry parses
- Verify test scripts run

### 21.3 Hook Format Gap Note

tai-lieu-ho-tro-phase-0.md đã note:
> Hook format gap (exit 2 vs stdout JSON permissionDecision) — đã quyết định giữ Format B cho Phase 2 và reconcile tại Phase 8.

---

**Document**: `docs/context-to-work/roadmap-analysis-phases/phase-2-scope.2026-07-07.md`
**Generated by**: context-before-fix v1.0.0
**Language**: Vietnamese
**Version**: 1.1.0
**Date**: 2026-07-07
**Status**: Updated — added cross-cutting context from quality-gates-reference.md, yaml-resilience-layer.md, phase-2-plan.md

---

## §22: Quality Gates Cross-Cutting Context (Quality-Gates-Reference)

> **Nguồn**: `Temps/spec/architects/shared/quality-gates-reference.md`
> **Phát hiện ngày**: 2026-07-07

### 22.1 HOOK-HEAL-1.0 — Native Prompt-Based Hook (Stop/SubagentStop)

```
HOOK-HEAL-1.0 (Advanced Prompt Gate):
  Native Prompt-based Hook với continueOnBlock: true trên Stop / SubagentStop events.
  Automatically audits markdown format and YAML syntax structure,
  prompting the active agent to self-heal and repair formatting errors
  before closing the session.
```

**Mapping Phase 2**:
- → **D2-9 Prompt Hook Experiment**: Phase 2 sẽ implement thử nghiệm này
- → **D2-5 Stop Hook**: YAML syntax check đã implement (L1), HOOK-HEAL-1.0 bổ sung thêm semantic layer
- `continueOnBlock: true` là cơ chế self-healing — agent được feed reason và tự sửa lỗi

### 22.2 HOOK-AUDIT-2.0 — Agent-Based Verification Hook

```
HOOK-AUDIT-2.0 (Agent-based Verification):
  Native Agent-based Hook on Stop or TaskCompleted events to execute test suites
  and inspect audit logs dynamically inside a sandbox.
```

**Mapping Phase 2**:
- → **Future Phase 8 integration** (không implement trong Phase 2)
- Dùng Agent-based hook (spawn subagent) để chạy test suite
- Liên quan đến Phase 7 Sandbox Tester

### 22.3 YAML-RES-1.0 — YAML Resilience Pre-check

```
YAML-RES-1.0:
  YAML Resilience pre-check on every artifact commit
```

**Mapping Phase 2**:
- → **D2-5 Stop Hook** đã implement L1 Syntax check (pyyaml parse)
- → Cross-cutting: mọi YAML artifact write đều cần pre-check
- Phase 2 hooks là **runtime enforcement** của architectural quality gate

### 22.4 Evidence

<evidence>
<file>Temps/spec/architects/shared/quality-gates-reference.md</file>
<line>44-47</line>
<finding>HOOK-HEAL-1.0: Native Prompt-based Hook on Stop/SubagentStop, continueOnBlock, self-healing. Direct mapping to D2-9.</finding>
</evidence>

<evidence>
<file>Temps/spec/architects/shared/quality-gates-reference.md</file>
<line>46-47</line>
<finding>HOOK-AUDIT-2.0: Agent-based Hook on Stop/TaskCompleted, sandbox test execution. Future Phase 8.</finding>
</evidence>

<evidence>
<file>Temps/spec/architects/shared/quality-gates-reference.md</file>
<line>44</line>
<finding>YAML-RES-1.0: YAML Resilience pre-check on every artifact commit. D2-5 implements L1 Syntax.</finding>
</evidence>

---

## §23: YAML Resilience Layer — Architecture Integration Context

> **Nguồn**: `Temps/spec/architects/P5-fallback-and-escalation/yaml-resilience-layer.md`
> **Phát hiện ngày**: 2026-07-07

### 23.1 3-Level Pre-check Pipeline

YAML Resilience Layer định nghĩa 3 cấp độ pre-check cho mọi YAML artifact write:

| Level | Check | Implementation trong Phase 2 |
|:------|:------|:----------------------------|
| **L1 Syntax** | `yaml.safe_load()` parse | D2-5 stop hook — pyyaml parse `_state.yaml` (đã có) |
| **L2 Schema** | Required keys + types + constraints | Chưa implement — cần Phase 8 hoặc extension |
| **L3 Cross-ref** | File paths exist + non-empty | Chưa implement — graceful degradation |

**Auto-repair protocol**: Max 2 repair attempts per artifact. Phase 2 chưa implement auto-repair — chỉ detect corrupt và backup. Self-healing (auto-repair) sẽ được thử nghiệm qua D2-9 Prompt Hook Experiment.

### 23.2 rule_9 — Last-Mile Verification

```
rule_9: "HOOK-HEAL-1.0 acts as a last-mile verification gate on Stop/SubagentStop events
         to catch any uncommitted or corrupted YAML state (_state.yaml) or formatting defects,
         feeding back errors to the agent context for self-healing before session exit."
```

**Integration với Phase 2**:

```yaml
yaml_resilience_rule_9_mapping:
  component:
    - "D2-5 stop_session_log_state.sh: L1 Syntax check — detect corrupt state, backup"
    - "D2-9 Prompt Hook Experiment: Semantic check — self-healing loop via continueOnBlock"
    - "YAML Resilience Layer: Architectural spec"
  
  flow:
    1: "Stop event fires"
    2: "D2-5 runs: pyyaml parse _state.yaml → corrupt? backup → exit 0"
    3: "HOOK-HEAL-1.0 (D2-9 experiment): Prompt hook → LLM evaluates doc structure"
    4: "If ok: false + continueOnBlock: true → agent self-heals"
    5: "Session ends cleanly"
  
  current_phase_2_coverage:
    - "Step 1-2: ✅ Implemented (D2-5)"
    - "Step 3-4: 🧪 Experimental (D2-9 — research)"
    - "Step 5: ✅ Handled by Claude Code runtime"
```

### 23.3 Graceful Degradation Context

YAML Resilience Layer phân loại:

| Type | Examples | Behavior | Phase 2 Status |
|:-----|:---------|:---------|:---------------|
| **Critical refs** | design.md, hydrated-context.yaml, todo.md, orchestration-plan.md | Hard Halt | N/A (D2-5 chỉ check _state.yaml) |
| **Non-critical refs** | domain-handbook.md, quality-matrix.yaml, criteria.md | Warning → degraded | D2-5 detect và backup nhưng không set degraded flag |

**Gap**: Phase 2 stop hook không set `_state.yaml.status = "degraded"` khi corrupt — chỉ backup. Cần xem xét bổ sung nếu YAML Resilience Layer được active.

### 23.4 Evidence

<evidence>
<file>Temps/spec/architects/P5-fallback-and-escalation/yaml-resilience-layer.md</file>
<line>12-17</line>
<finding>3-level YAML pre-check: L1 Syntax (safe_load), L2 Schema (keys+types), L3 Cross-ref (paths). D2-5 implements L1.</finding>
</evidence>

<evidence>
<file>Temps/spec/architects/P5-fallback-and-escalation/yaml-resilience-layer.md</file>
<line>47</line>
<finding>rule_9: HOOK-HEAL-1.0 last-mile verification on Stop events — self-healing before session exit.</finding>
</evidence>

<evidence>
<file>Temps/spec/architects/P5-fallback-and-escalation/yaml-resilience-layer.md</file>
<line>20-22</line>
<finding>Auto-repair protocol: max 2 attempts per artifact. Phase 2 chưa implement — experimental ở D2-9.</finding>
</evidence>

---

## §24: Roadmap Spec — Design Principles & Advanced Hooks Context

> **Nguồn**: `skills/ver-3/roadmaps/02-hook-framework.md`
> **Phát hiện ngày**: 2026-07-07

### 24.1 Two-Layer Hook Design Principle

Roadmap spec §Design principles định nghĩa kiến trúc phân lớp cho hooks:

```yaml
layer_1_command_based:
  description: "Cơ học, phi ngữ nghĩa, tối giản"
  characteristics:
    - "bash + jq"
    - "< 50 dòng code"
    - "< 100ms execution"
    - "Format B: exit 2 blocking"
    - "Chạy synchronous mỗi tool call (PreToolUse)"
  deliverables:
    - "D2-1 → D2-6 (6 command hooks)"
    - "Chốt chặn deterministic — không phụ thuộc LLM"

layer_2_prompt_agent_based:
  description: "Thông minh, suy luận ngữ nghĩa, self-healing"
  characteristics:
    - "LLM evaluation (Haiku/Sonnet)"
    - "30-120s timeout"
    - "continueOnBlock: true (self-healing)"
    - "Chỉ chạy ở mốc thưa thớt: Stop, SessionStart, TaskCompleted"
  deliverables:
    - "D2-9: Prompt Hook Experiment (Stop event)"
    - "D2-10: Evaluation report"
    - "Không implement ở PreToolUse — tránh latency"

design_rationale:
  - "Layer 1 bắt buộc — deterministic gate không thể bypass"
  - "Layer 2 optional — semantic check cho quality assurance"
  - "Cả 2 layer hoạt động độc lập — không blocking nhau"
  - "Fail-safe: layer 2 fail → degrade gracefully, không block pipeline"
```

**Impact Phase 2**: 
- D2-9 experiment sẽ test Layer 2 trên Stop event với `continueOnBlock: true`
- Kết quả D2-10 sẽ quyết định có mở rộng Layer 2 trong Phase 8 không
- Layer 1 là mandatory — Layer 2 là research

### 24.2 D2-9 / D2-10 Chi Tiết

Từ roadmap spec task list (item 10):

> **D2-9**: Thiết lập cấu hình thử nghiệm Prompt-based Hook tại sự kiện `Stop` trong `.claude/settings.local.json` để kiểm tra khả năng tự sửa lỗi (Self-healing) — `continueOnBlock: true`.

> **D2-10**: Evaluation report ghi nhận:
- Latency benchmark (Haiku vs Sonnet)
- Self-healing success rate
- false positive / false negative rate
- Recommendations for Phase 8 integration

**Config mẫu cho D2-9** (từ hooks_and_events.md §7.4.1):
```json
{
  "hooks": {
    "Stop": [
      {
        "handlers": [
          {
            "type": "prompt",
            "prompt": "Evaluate if the workspace documentation is structurally complete. Event context: $ARGUMENTS. Return JSON in schema: {\"ok\": boolean, \"reason\": string}",
            "model": "claude-3-5-haiku",
            "timeout": 45,
            "continueOnBlock": true,
            "description": "Verify MD layout and YAML frontmatter prior to session end"
          }
        ]
      }
    ]
  }
}
```

### 24.3 Advanced Hooks — Hook Type Support

Từ hooks_and_events.md §7.4, Claude Code hỗ trợ 2 loại advanced hooks:

| Type | Mechanism | Timeout | Use Case cho Phase 2 |
|:-----|:----------|:-------:|:---------------------|
| `prompt` | LLM single-turn (Haiku/Sonnet) | 30s | **D2-9**: Stop event self-healing |
| `agent` | Spawn subagent (50 turns) | 120s | Future: HOOK-AUDIT-2.0 (Phase 8) |

**Output schema** (required for both):
```json
{ "ok": true/false, "reason": "..." }
```

**continueOnBlock behavior**:
- `false` (default): block reason logged → session continues without action
- `true`: block reason fed back to agent → agent tự sửa → retry completion

### 24.4 Evidence

<evidence>
<file>skills/ver-3/roadmaps/02-hook-framework.md</file>
<line>36-44</line>
<finding>Two-layer hook design principle: Layer 1 Command-based (mechanical, exit 2) + Layer 2 Prompt/Agent-based (semantic, continueOnBlock).</finding>
</evidence>

<evidence>
<file>skills/ver-3/roadmaps/02-hook-framework.md</file>
<line>432-433</line>
<finding>D2-9: Advanced Hooks experiment (Prompt-based, Stop event, self-healing). D2-10: Evaluation report.</finding>
</evidence>

<evidence>
<file>.claude/knowledge/agents/hooks_and_events.md</file>
<line>411-470</line>
<finding>Section 7.4: Prompt-based hooks (single-turn LLM, continueOnBlock) và Agent-based hooks (50-turn subagent).</finding>
</evidence>

---

## §25: Phase 2 Plan — Alignment Verification

> **Nguồn**: `docs/context-to-work/roadmap-analysis-phases/phase-2-plan.2026-07-07.md`
> **Phát hiện ngày**: 2026-07-07

### 25.1 Scope Document vs Plan — Coverage Check

| Aspect | Scope Doc (§1-21) | Plan Doc | Status |
|:-------|:------------------|:---------|:-------|
| 6 hook scripts | ✅ §3.1, §5.1 | ✅ Stage 1-2 | ✅ Aligned |
| registry.yaml | ✅ §5.1 D2-7 | ✅ Stage 3 | ✅ Aligned |
| 7 test scripts | ✅ §5.1 D2-8, §5.2 | ✅ Stage 3 | ✅ Aligned |
| AC-1→AC-7 | ✅ §10 | ✅ §5 | ✅ Aligned |
| Advanced Hooks Research | ✅ (New §22-24) | ✅ Stage 5 | ✅ Aligned |
| AC-8 | ✅ (New §10) | ✅ §5 AC-8 | ✅ Aligned |
| D2-9 / D2-10 | ✅ (New §24.2) | ✅ Stage 5 | ✅ Aligned |
| Self-healing (continueOnBlock) | ✅ §24.2-24.3 | ✅ Stage 5 Task 1 | ✅ Aligned |
| Two-layer design principle | ✅ §24.1 | ✅ §2 Mermaid diagram | ✅ Aligned |

### 25.2 Plan Structure Alignment

Phase 2 Plan định nghĩa 5 Stages — scope document now covers all:

| Stage | Focus | Scope Coverage |
|:-----:|:------|:---------------|
| Stage 1 | PreToolUse Gating Hooks (D2-1, D2-2, D2-4) | §5.1, §14.1 |
| Stage 2 | Logging & Lifecycle Hooks (D2-3, D2-5, D2-6) | §5.1, §14.1 |
| Stage 3 | Registry & Unit Tests (D2-7, D2-8) | §5.1, §5.2, §10 |
| Stage 4 | Verification (AC-1→AC-8) | §10, §14.1 |
| Stage 5 | Advanced Hooks Research (D2-9, D2-10) | §14.1, §24 |

### 25.3 Hook Input Field — Minor Schema Note

So sánh giữa các tài liệu về field naming cho stdin JSON:

| Source | Tool Field | Params Field | Notes |
|:-------|:-----------|:-------------|:------|
| Roadmap spec (02-hook-framework.md) | `tool_name` | `tool_input.command` | Dùng trong script code |
| Official Claude Code Docs (§19.3) | `tool_name` | `tool_input.command` | Runtime reality |
| hooks_and_events.md §4.2 | `tool` | `params.command` | Abstract schema description |
| hooks_and_events.md §8.1 (conditions) | `tool.name` | `tool.params.*` | If-condition context vars |

**Assessment**: Không phải inconsistency — `tool`/`params` trong hooks_and_events.md là abstract schema cho mục đích documentation, trong khi runtime JSON dùng `tool_name`/`tool_input`. Condition expressions (§8.1) dùng namespace riêng (`tool.name`, `tool.params.*`). Phase 2 scripts dùng `tool_input.*` (đúng với runtime). **Không cần action**.

### 25.4 Evidence

<evidence>
<file>docs/context-to-work/roadmap-analysis-phases/phase-2-plan.2026-07-07.md</file>
<line>103-239</line>
<finding>Phase 2 Plan định nghĩa 5 Stages, 11 tasks. Stage 5: Advanced Hooks Research (D2-9/D2-10).</finding>
</evidence>

<evidence>
<file>docs/context-to-work/roadmap-analysis-phases/phase-2-plan.2026-07-07.md</file>
<line>256</line>
<finding>AC-8: Prompt-based Hook experiment verification — Claude Code nhận ok:false, self-heal.</finding>
</evidence>

---

## §26: Updated Impact Analysis

### 26.1 New Direct Impact

```yaml
new_direct_impact:
  files:
    - path: ".claude/settings.local.json"
      status: "need_create"
      description: "D2-9: Prompt Hook experiment config (Stop event, continueOnBlock: true)"
    - path: "docs/context-to-work/roadmap-analysis-phases/advanced-hooks-capability.2026-07-07.md"
      status: "reference"
      description: "Existing research doc — reference cho D2-10 evaluation"
    - path: "Temps/spec/architects/shared/quality-gates-reference.md"
      status: "reference"
      description: "HOOK-HEAL-1.0, HOOK-AUDIT-2.0, YAML-RES-1.0 cross-cutting context"
    - path: "Temps/spec/architects/P5-fallback-and-escalation/yaml-resilience-layer.md"
      status: "reference"
      description: "YAML Resilience Layer spec — rule_9 integration context"
```

### 26.2 Updated Deliverables Count

```yaml
updated_totals:
  hook_scripts: 6                          # D2-1 → D2-6 (không đổi)
  registry: 1                              # D2-7 (không đổi)
  test_scripts: 7                          # D2-8 (không đổi)
  advanced_hooks_config: 1                 # D2-9 (NEW: settings.local.json)
  evaluation_report: 1                     # D2-10 (NEW)
  reference_docs: 4                        # quality-gates, yaml-resilience, plan, advanced-hooks
  total_tasks: 11                          # +2 tasks
  total_files_created: 17                  # +2 files
```

---

## §27: Updated Confidence Assessment

```yaml
overall_confidence: 88%                    # Giảm nhẹ từ 90% do thêm advanced hooks research

breakdown:
  spec_completeness: 95%                   # Không đổi
  code_readiness: 90%                      # Không đổi
  test_coverage: 85%                       # Không đổi
  dependency_ready: 100%                   # Không đổi
  format_gap_awareness: 85%                # Tăng nhờ quality-gates-reference context
  risk_mitigation: 85%                     # Không đổi
  quality_gates_integration: 80%           # Mới: cross-cutting context integrated
  advanced_hooks_research: 70%             # Mới: experimental — cần test reality

uncertainty_flags:
  - "Hook format gap: Đã thống nhất giữ Format B (exit 2) cho Phase 2, reconcile ở Phase 8"
  - "Claude Code runtime có tôn trọng registry.yaml format hiện tại? Cần test thực tế tại Phase 8"
  - "stop hook corrupt YAML detection dùng python3 — nếu python3 không available thì skip"
  - "D2-9 Prompt Hook Experiment: continueOnBlock behavior chưa được verify trên Claude Code runtime cụ thể"
  - "HOOK-AUDIT-2.0 (Agent-based hook) không implement trong Phase 2 — defer to Phase 8"
  - "YAML Resilience Layer rule_9 integration cần verify khi settings.local.json active"
```

---

## §28: Updated Open Questions

| # | Question | Priority | Status |
|--:|:---------|:--------:|:------:|
| 1 | Hook format reconcile: exit 2 (roadmap) vs stdout JSON (Claude Code) — khi nào reconcile? | High | Resolved (Keep B for P2, reconcile in P8) |
| 2 | jq CLI có sẵn trên PATH? (prerequisite cho hook scripts) | High | Assumed (Phase 0 ghi prereq) |
| 3 | Claude Code settings.json có cần update để active hooks? | Medium | Need test tại Phase 8 |
| 4 | Corrupt YAML detection — python3 có luôn available? | Medium | Fallback: skip check |
| 5 | `DEPLOY_PHASE_ACTIVE` env var mechanism — ai set? khi nào? | Low | Defer đến deploy decision |
| 6 | **D2-9 Prompt Hook**: continueOnBlock có hoạt động đúng với Claude Code runtime? | Medium | Cần test — thêm vào AC-8 |
| 7 | **YAML Resilience Layer**: Có cần set `_state.yaml.status = "degraded"` trong D2-5 không? | Low | Cần clarify với architect |
| 8 | **Two-layer design**: Layer 2 Prompt hook có cần cho PreToolUse trong tương lai? | Low | Defer đến Phase 8 |

---

## §29: Updated Quality Checklist

```yaml
pre_delivery_check:
  entry_point_identified: true
  all_related_files_searched: true        # 7 docs analyzed (tăng từ 26 files)
  impact_map_direct: true                 # +4 new entries (settings.local.json, references)
  impact_map_indirect: true               # +quality gates +YAML resilience
  evidence_specific: true                 # +7 new evidence blocks (§22-25)
  confidence_assessment_done: true        # 88% (+new metrics)
  document_written_in_vietnamese: true
  document_saved_correct_path: true
  no_code_changes_made: true              # Document only
  cross_references_updated: true          # §13 updated, new §22-29 appended
  plan_alignment_verified: true           # §25: vs phase-2-plan.md
```

---

**Document Status**: Context Complete — Updated with Cross-Cutting Reference Analysis
**NO Code Changes Made** — Document only per context-before-fix skill guardrails

```
✓ In Scope updated — D2-9, D2-10, quality gates, YAML resilience
✓ §5.1 Deliverables Map — +2 rows (D2-9, D2-10)
✓ §10 Acceptance Criteria — AC-8 added, totals updated
✓ §13 References — quality-gates, yaml-resilience, plan added
✓ §14.1 Build Order — steps 10-11 added
✓ §14.2 Special Notes — two-layer design, YAML resilience integration
✓ §17 Task Breakdown — +2 tasks (tasks 10-11)
✓ §22 Quality Gates — HOOK-HEAL-1.0, HOOK-AUDIT-2.0, YAML-RES-1.0 mapped
✓ §23 YAML Resilience Layer — 3-level pipeline, rule_9 mapping
✓ §24 Roadmap Design Principles — two-layer architecture, D2-9/D2-10 detail
✓ §25 Plan Alignment — coverage check vs phase-2-plan.md
✓ §26 Updated Impact — new direct impact + totals
✓ §27 Confidence — 88%, +2 new metrics
✓ §28 Open Questions — +3 questions
✓ §29 Quality Checklist — updated
```

**Document**: `docs/context-to-work/roadmap-analysis-phases/phase-2-scope.2026-07-07.md`
**Generated by**: context-before-fix v1.0.0
**Language**: Vietnamese
**Version**: 1.1.0
**Date**: 2026-07-07
**Status**: Updated
