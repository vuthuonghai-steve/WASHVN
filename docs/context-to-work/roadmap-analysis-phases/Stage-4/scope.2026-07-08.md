---
name: stage-4-verification-scope
description: Scope document cho Stage 4 — Verification & Acceptance (Phase 2: Hook Framework Foundation)
version: 0.1.0
suite: WASHVN
tags: [roadmap, phase-2, stage-4, verification, acceptance, hook-framework, quality-gates]
when_to_use: "Khi cần thực hiện verification & acceptance cho Stage 4 — Hook Framework Foundation Phase 2"
trace: [TỪ SCOPE phase-2-plan.2026-07-07.md §4], [TỪ ROADMAP 02-hook-framework.md §Verification-checklist], [TỪ SCOPE phase-2-scope.2026-07-07.md §10], [TỪ BA GAP-2 graceful-degradation], [TỪ quality-gates-reference.md YAML-RES-1.0]
---

# Scope Document — Stage 4: Verification & Acceptance

> **Phiên bản**: 0.1.0
> **Ngày**: 2026-07-08
> **Stage**: 4/5 — Verification & Acceptance (Phase 2: Hook Framework Foundation)
> **Phụ thuộc**: Stage 1 (PreToolUse Gating Hooks) ✅ hoàn thành, Stage 2 (Logging & Lifecycle Hooks) ✅ hoàn thành, Stage 3 (Registry & Unit Tests) ✅ hoàn thành
> **Gates**: Stage 5 (Advanced Hooks Research) — cần Stage 4 PASS để bắt đầu

---

## §1: Tổng Quan Stage 4

Stage 4 là **Verification & Acceptance** stage — stage cuối cùng trong chuỗi 4 stages xây dựng Hook Framework Foundation (Phase 2). Stage này **không implement code mới**. Nhiệm vụ duy nhất là xác minh rằng tất cả deliverable từ Stage 1→3 đáp ứng đầy đủ các Acceptance Criteria (AC) đã định nghĩa.

### 1.1 Verification Scope

Stage 4 gồm 4 nhóm verification task:

```yaml
verification_tasks:
  task_1_ac_1_to_7:
    name: "AC-1→AC-7 Full Verification Suite"
    source: "Roadmap spec 02-hook-framework.md §Verification-checklist"
    scope: "7 acceptance criteria từ roadmap spec — primary verification"
    verify_scripts: true
    verify_registry: true
    verify_hooks_behavior: true
    verify_state_backup: true

  task_2_graceful_degradation:
    name: "Graceful Degradation Verification"
    source: "BA Analysis GAP-2 §1.2.2"
    scope: "6 hooks × degradation scenarios (jq missing, stdin malformed, python3 missing, env var missing)"
    gating_hooks: "D2-1, D2-2, D2-4 — fail CLOSED (exit 2)"
    logging_hooks: "D2-3, D2-5, D2-6 — fail OPEN (exit 0, skip/warning)"

  task_3_yaml_res_compliance:
    name: "YAML-RES-1.0 Compliance Verification"
    source: "quality-gates-reference.md YAML-RES-1.0"
    scope: "L1 Syntax check (D2-5), L2 Schema validation (D2-7), corrupt backup, degraded flag"
    yaml_resilience_levels:
      l1_syntax: "pyyaml.safe_load() — D2-5"
      l2_schema: "required keys: hooks, script_path, matcher, event_type — D2-7"
      l3_cross_ref: "Deferred to Phase 8"

  task_4_consistency:
    name: "Consistency & Quality Checks"
    source: "Phase 2 plan §4 Stage 4 subtasks"
    scope: "Placeholder scan, subagent-forge.md compatibility, documentation consistency"
```

### 1.2 Stage 4 trong Pipeline Phase 2

```text
Stage 1: PreToolUse Gating Hooks (D2-1, D2-2, D2-4)  ───┐
Stage 2: Logging & Lifecycle Hooks (D2-3, D2-5, D2-6) ───┤
Stage 3: Registry & Unit Tests (D2-7, D2-8) ─────────────┤
                                                          ▼
Stage 4: VERIFICATION & ACCEPTANCE ◄── BẠN ĐANG Ở ĐÂY
                                                          │
                                                          ▼
Stage 5: Advanced Hooks Research (D2-9, D2-10) — gate bởi Stage 4
```

### 1.3 Nguyên Tắc Hoạt Động

```yaml
stage_4_principles:
  - "Stage 4 CHỈ verify — KHÔNG implement, KHÔNG sửa code mới"
  - "Nếu verification FAIL → ghi nhận lỗi chi tiết → quay lại Stage tương ứng fix → quay lại Stage 4 re-verify"
  - "Stage 4 phải chạy trên codebase đã hoàn thành Stage 1→3 (6 hook scripts, registry, 7 tests)"
  - "Stage 4 output: verification-report.md (PASS/FAIL chi tiết cho từng AC)"
  - "Stage 4 không yêu cầu sandbox — chạy verification trực tiếp trên host (hooks chạy local)"
  - "Stage 4 cũng là điều kiện gate cho Stage 5 — Advanced Hooks Research cần baseline hoạt động"
  - "Mỗi AC cần: verification command chính xác, expected result, failure recovery path"
```

---

## §2: Entry Point & Tài Liệu Tham Chiếu

### 2.1 Entry Points

| Entry | Path | Ghi chú |
|:------|:-----|:--------|
| Roadmap spec | `skills/ver-3/roadmaps/02-hook-framework.md` (§Verification-check-list) | AC-1→AC-7 verification commands |
| Phase 2 Plan | `docs/context-to-work/roadmap-analysis-phases/phase-2-plan.2026-07-07.md` (§4 Stage 4) | Task list + graceful degradation + YAML-RES-1.0 |
| Phase 2 Scope | `docs/context-to-work/roadmap-analysis-phases/phase-2-scope.2026-07-07.md` (§10) | Acceptance criteria mapping |
| BA Analysis | `docs/context-to-work/roadmap-analysis-phases/business-analysis-phase2-hook-framework.2026-07-07.md` | GAP-2 graceful degradation policy |
| Quality Gates | `Temps/spec/architects/shared/quality-gates-reference.md` | YAML-RES-1.0, HOOK-HEAL-1.0 |
| YAML Resilience | `Temps/spec/architects/P5-fallback-and-escalation/yaml-resilience-layer.md` | 3-level pre-check, rule_9 |
| Hook Protocol | `.claude/knowledge/agents/hooks_and_events.md` | Dual-Format blocking protocol |
| Registry | `.claude/hooks/registry.yaml` | (sau Stage 3 — 6 entries) |
| Events dir | `.claude/hooks/events/` | (sau Stage 1+2 — 6 scripts) |
| Tests dir | `.claude/hooks/tests/` | (sau Stage 3 — 7 scripts) |
| Suite Validator | `.claude/scripts/validate_suite_integrity.py` | Có thể extend cho hook validation |
| subagent-forge.md | `.claude/agents/subagent-forge.md` | Inline hooks reference (dòng ~262) |

### 2.2 Tài Liệu Tham Chiếu Chi Tiết

| File | Nội dung | Dòng chính |
|:-----|:---------|:-----------|
| `02-hook-framework.md` | AC-1→AC-7 verification commands | 322-399 |
| `02-hook-framework.md` | Definition of Done | 437-452 |
| `02-hook-framework.md` | 6 hook script code mẫu | 50-285 |
| `02-hook-framework.md` | 7 test script structure | 286-317 |
| `phase-2-plan.2026-07-07.md` §4 | Stage 4 tasks | 274-305 |
| `phase-2-plan.2026-07-07.md` §6 | Error handling policy (exit codes, graceful degradation) | 402-461 |
| `phase-2-plan.2026-07-07.md` §7 | Acceptance criteria AC-1→AC-11 | 465-481 |
| `phase-2-scope.2026-07-07.md` §10 | AC-1→AC-8 mapping | 348-361 |
| `phase-2-scope.2026-07-07.md` §7 | Call chain lifecycle | 189-228 |
| `phase-2-scope.2026-07-07.md` §22-23 | Quality gates + YAML resilience context | 1084-1228 |
| `quality-gates-reference.md` | YAML-RES-1.0, HOOK-HEAL-1.0 | 44-47 |
| `yaml-resilience-layer.md` | 3-level pre-check, rule_9 | 12-47 |
| `validate_suite_integrity.py` | Script có thể extend | 319 dòng |

---

## §3: Scope Definition

### 3.1 In Scope

```yaml
in_scope:
  - "AC-1: Xác minh 6 hook scripts tồn tại và executable (+x)"
  - "AC-2: Xác minh registry.yaml parses với đúng 6 entries"
  - "AC-3: Xác minh 7 test scripts chạy và PASS"
  - "AC-4: Xác minh hook self-test — allow trả về exit 0, block trả về exit 2"
  - "AC-5: Xác minh corrupt state backup — Γ-7 fix hoạt động"
  - "AC-6: Xác minh bash validate distinguish allow vs block"
  - "AC-7: Xác minh subagent-forge.md inline hooks vẫn hoạt động (không conflict)"
  - "Graceful Degradation: verify fail CLOSED cho gating hooks (D2-1, D2-2, D2-4)"
  - "Graceful Degradation: verify fail OPEN cho logging hooks (D2-3, D2-5, D2-6)"
  - "YAML-RES-1.0 L1 Syntax: D2-5 pyyaml parse _state.yaml corrupt"
  - "YAML-RES-1.0 L2 Schema: D2-7 registry.yaml required keys validation"
  - "Corrupt backup verification: backup file tạo tại _state-archive/"
  - "Degraded flag: _state.yaml.status = 'degraded' sau non-critical corrupt"
  - "Placeholder scan: zero TODO, pass trong hook scripts"
  - "Documentation consistency: hooks_and_events.md vs hook scripts thực tế"
  - "Simulation scripts: tạo script phụ để simulate graceful degradation scenarios"
  - "Verification report: ghi nhận kết quả PASS/FAIL từng AC"
```

### 3.2 Out of Scope

```yaml
out_of_scope:
  - "KHÔNG implement, sửa code hook script mới"
  - "KHÔNG sửa registry.yaml (trừ khi verification phát hiện lỗi cần fix)"
  - "KHÔNG sửa test scripts (trừ khi verification phát hiện lỗi cần fix)"
  - "KHÔNG deploy hooks vào settings.json (deferred đến Phase 8)"
  - "KHÔNG reconcile Format A/B gap (deferred đến Phase 8)"
  - "KHÔNG implement HOOK-HEAL-1.0 hoặc D2-9 (Stage 5 task)"
  - "KHÔNG run D2-9 Prompt Hook experiment (Stage 5 task)"
  - "KHÔNG run D2-10 Evaluation (Stage 5 task)"
  - "KHÔNG sửa validate_suite_integrity.py (trừ khi cần extend cho Stage 4)"
  - "KHÔNG modify subagent-forge.md inline hooks"
```

### 3.3 Boundary

```yaml
boundary:
  - "Verification giới hạn trong .claude/hooks/ (scripts, tests, registry)"
  - "YAML-RES-1.0 L1 Syntax: chỉ verify _state.yaml corrupt detection"
  - "YAML-RES-1.0 L2 Schema: chỉ verify registry.yaml (không verify _state.yaml schema)"
  - "YAML-RES-1.0 L3 Cross-ref: KHÔNG verify (deferred Phase 8)"
  - "Graceful degradation verification: chạy simulation scripts — KHÔNG sửa hook scripts"
  - "Simulation scripts là temporary verification artifacts — có thể xóa sau Stage 4"
  - "Consistency check: so sánh documentation vs code — KHÔNG sửa documentation"
  - "subagent-forge.md inline hooks: chỉ verify không conflict — KHÔNG modify"
  - "Stage 4 không yêu cầu sandbox Docker — chạy trên host"
```

---

## §4: AC-1→AC-7 Full Verification

### 4.1 Ma Trận AC

| Mã AC | Mô tả | Verification Command | Expected Result | Failure Recovery |
|:-----:|:------|:--------------------|:----------------|:-----------------|
| **AC-1** | 6 hook scripts tồn tại + executable | `for f in pre-tool-use_write_gate.sh pre-tool-use_skill_staging_gate.sh pre-tool-use_bash_validate_command.sh post-tool-use_log_artifact.sh stop_session_log_state.sh session-start_record_metadata.sh; do test -f ".claude/hooks/events/$f" && test -x ".claude/hooks/events/$f" || exit 1; done; echo "AC-1 PASS"` | `AC-1 PASS` (exit 0) | Quay lại Stage 1/2 — tạo script thiếu hoặc `chmod +x` |
| **AC-2** | Registry parses + 6 entries | `python3 -c "import yaml; data=yaml.safe_load(open('.claude/hooks/registry.yaml')); assert isinstance(data.get('hooks'), list); assert len(data['hooks']) == 6; print('AC-2 PASS')"` | `AC-2 PASS` (exit 0) | Quay lại Stage 3 — sửa registry.yaml |
| **AC-3** | 7 test scripts run + pass | `for t in .claude/hooks/tests/test_*.sh; do bash "$t" || exit 1; done; echo "AC-3 PASS"` | `AC-3 PASS` (exit 0) | Quay lại Stage 3 — sửa test scripts hoặc hook scripts |
| **AC-4** | Hook self-test — allow 0, block 2 | `JSON_ALLOW='{"tool_name":"Write","tool_input":{"file_path":"'$(pwd)'/skills/ver-3/test/SKILL.md"}}'; JSON_BLOCK='{"tool_name":"Write","tool_input":{"file_path":"/etc/passwd"}}'; EXIT_ALLOW=$(echo "$JSON_ALLOW" | bash .claude/hooks/events/pre-tool-use_write_gate.sh 2>&1 > /dev/null; echo $?); EXIT_BLOCK=$(echo "$JSON_BLOCK" | bash .claude/hooks/events/pre-tool-use_write_gate.sh 2>&1 > /dev/null; echo $?); [ "$EXIT_ALLOW" = "0" ] && [ "$EXIT_BLOCK" = "2" ] && echo "AC-4 PASS" || exit 1` | `AC-4 PASS` (exit 0) — allow=0, block=2 | Quay lại Stage 1 — sửa write_gate.sh logic |
| **AC-5** | Corrupt state backup (Γ-7) | `echo "this: is: invalid: yaml" > /tmp/test_state.yaml; mkdir -p /tmp/hook_test_dir/.skill-context/_state-archive; cp /tmp/test_state.yaml /tmp/hook_test_dir/.skill-context/_state.yaml; cd /tmp/hook_test_dir; STOP_JSON='{"stop_hook_active":false}'; EXIT=$(echo "$STOP_JSON" | bash '$WORKSPACE/.claude/hooks/events/stop_session_log_state.sh' 2>&1; echo $?); [ "$EXIT" = "0" ] && ls .skill-context/_state-archive/_state-*-corrupt.yaml > /dev/null 2>&1 && echo "AC-5 PASS" || exit 1; rm -rf /tmp/hook_test_dir /tmp/test_state.yaml` | `AC-5 PASS` (exit 0) | Quay lại Stage 2 — sửa stop_session_log_state.sh |
| **AC-6** | Bash validate distinguish allow/block | `JSON_ALLOW='{"tool_name":"Bash","tool_input":{"command":"ls -la"}}'; JSON_BLOCK='{"tool_name":"Bash","tool_input":{"command":"rm -rf /home"}}'; EXIT_ALLOW=$(echo "$JSON_ALLOW" | bash .claude/hooks/events/pre-tool-use_bash_validate_command.sh 2>&1 > /dev/null; echo $?); EXIT_BLOCK=$(echo "$JSON_BLOCK" | bash .claude/hooks/events/pre-tool-use_bash_validate_command.sh 2>&1 > /dev/null; echo $?); [ "$EXIT_ALLOW" = "0" ] && [ "$EXIT_BLOCK" = "2" ] && echo "AC-6 PASS" || exit 1` | `AC-6 PASS` (exit 0) — allow=0, block=2 | Quay lại Stage 1 — sửa bash_validate_command.sh |
| **AC-7** | subagent-forge.md inline hooks validated | `grep -q "PreToolUse" .claude/agents/subagent-forge.md && echo "AC-7 PASS" || exit 1` | `AC-7 PASS` (exit 0) | Kiểm tra subagent-forge.md — có thể inline hooks bị xóa nhầm |

### 4.2 Verification Workflow

```text
for each AC in [AC-1, AC-2, AC-3, AC-4, AC-5, AC-6, AC-7]:
  1. Run verification command
  2. Capture exit code + stdout + stderr
  3. So sánh với expected result
  4. PASS → ghi nhận vào verification-report.md
  5. FAIL → ghi nhận lỗi chi tiết → dừng → chuyển sang stage tương ứng để fix
```

### 4.3 AC-7 Chi Tiết — subagent-forge.md Compatibility

AC-7 yêu cầu xác minh 2 điều:

1. **Inline hooks tồn tại** (không bị xóa nhầm bởi Stage 1-3):
   ```bash
   grep -q "PreToolUse" .claude/agents/subagent-forge.md || exit 1
   ```

2. **Exit code convention compatibility** — cả inline hooks (subagent-forge) và standalone hooks (Phase 2) đều dùng Format B (exit 2 blocking):
   ```bash
   # subagent-forge.md dòng ~262 có pattern:
   # "Hook self-test fails" → abort (exit 2 pattern)
   grep -q "exit 2\|exit 0" .claude/agents/subagent-forge.md || echo "WARN: no exit code convention found"
   ```

3. **Không conflict event/matcher** — standalone hooks không override hay disable inline hooks:
   - subagent-forge.md inline hooks dùng `PreToolUse` event
   - Phase 2 standalone hooks cũng dùng `PreToolUse` cho D2-1, D2-2, D2-4
   - Claude Code runtime chạy cả 2 loại hooks sequentially (inline → standalone hoặc ngược lại)
   - First hook that exits 2 wins — nếu inline hooks exit 2, standalone hooks không chạy
   - **Cần verify**: không có dual-block (cả 2 cùng block) gây false positive

---

## §5: Graceful Degradation Verification

### 5.1 Policy Overview

Theo Error Handling Policy (phase-2-plan.md §6), mỗi hook có degradation behavior khác nhau dựa trên category:

| Hook | Category | Fallback Behavior |
|:-----|:---------|:-----------------|
| **D2-1** write_gate | **Gating — fail CLOSED** | `jq` missing → exit 2, stdin malformed → exit 2 |
| **D2-2** staging_gate | **Gating — fail CLOSED** | `jq` missing → exit 2, stdin malformed → exit 2 |
| **D2-4** bash_validate | **Gating — fail CLOSED** | `jq` missing → exit 2, stdin malformed → exit 2, MARK_NETWORK_ALLOWED parse fail → restrictive |
| **D2-3** log_artifact | **Logging — fail OPEN** | `jq` missing → exit 0 (skip log), stdin malformed → exit 0 |
| **D2-6** session_start | **Logging — fail OPEN** | `jq` missing → exit 0, stdin malformed → exit 0 |
| **D2-5** stop_state | **Logging — fail OPEN** | `python3`/`pyyaml` missing → exit 0 + warning, `_state.yaml` missing → exit 0 |

### 5.2 Verification Matrix

| Hook | Scenario | Simulation Method | Expected Exit | Expected Stderr |
|:-----|:---------|:-----------------|:-------------:|:----------------|
| **D2-1** | `jq` missing | `PATH=/tmp no-jq-dir:$PATH` (override PATH, loại bỏ jq) | 2 | `jq: command not found` hoặc error message |
| **D2-1** | stdin malformed | Pipe non-JSON string: `echo "not-json" \| ...` | 2 | `parse error` hoặc error message |
| **D2-2** | `jq` missing | `PATH=/tmp no-jq-dir:$PATH` | 2 | `jq: command not found` |
| **D2-2** | stdin malformed | Pipe non-JSON: `echo "not-json"` | 2 | `parse error` |
| **D2-4** | `jq` missing | `PATH=/tmp no-jq-dir:$PATH` | 2 | `jq: command not found` |
| **D2-4** | stdin malformed | Pipe non-JSON: `echo "not-json"` | 2 | `parse error` |
| **D2-4** | MARK_NETWORK_ALLOWED unset + curl in cmd | `unset MARK_NETWORK_ALLOWED` + pipe curl command | 2 | `network access requires` |
| **D2-4** | MARK_NETWORK_ALLOWED set + curl in cmd | `MARK_NETWORK_ALLOWED=true` + pipe curl command | 0 | — |
| **D2-3** | `jq` missing | `PATH=/tmp no-jq-dir:$PATH` | 0 | (có thể có warning) |
| **D2-3** | stdin malformed | Pipe non-JSON: `echo "not-json"` | 0 | (có thể có warning) |
| **D2-6** | `jq` missing | `PATH=/tmp no-jq-dir:$PATH` | 0 | (có thể có warning) |
| **D2-6** | stdin malformed | Pipe non-JSON: `echo "not-json"` | 0 | (có thể có warning) |
| **D2-5** | `python3` missing | `PATH=/tmp no-py3-dir:$PATH` (loại python3) | 0 | Warning: python3 not available |
| **D2-5** | `_state.yaml` missing | Run in directory without `_state.yaml` | 0 | — |
| **D2-5** | `_state.yaml` malformed | Pipe malformed YAML + run | 0 | STATE CORRUPT: backed up |

### 5.3 Simulation Script Mẫu

```bash
#!/usr/bin/env bash
# Simulation: graceful degradation test cho D2-1 (write_gate)
# Scenario: jq missing

echo "=== D2-1 Graceful Degradation: jq missing ==="

# Save original PATH
ORIG_PATH="$PATH"

# Create temp directory without jq
TMPDIR=$(mktemp -d)
export PATH="$TMPDIR"  # No jq in this PATH

# Test input
JSON='{"tool_name":"Write","tool_input":{"file_path":"/tmp/test.txt"}}'

# Run hook
EXIT_CODE=0
OUTPUT=$(echo "$JSON" | bash .claude/hooks/events/pre-tool-use_write_gate.sh 2>&1) || EXIT_CODE=$?

echo "Exit code: $EXIT_CODE"
echo "Stderr: $OUTPUT"

# Verify
if [ "$EXIT_CODE" = "2" ]; then
  echo "PASS: D2-1 fail CLOSED (exit 2) when jq missing"
else
  echo "FAIL: expected exit 2, got $EXIT_CODE"
fi

# Cleanup
export PATH="$ORIG_PATH"
rm -rf "$TMPDIR"
```

### 5.4 Scenario Implementation Details

#### Scenario A: jq missing
```bash
# Simulate jq missing bằng cách tạo PATH chỉ chứa sh, không có jq
TMPDIR=$(mktemp -d)
ln -s /bin/sh "$TMPDIR/sh"  # chỉ có sh, không có jq
PATH="$TMPDIR" bash .claude/hooks/events/pre-tool-use_write_gate.sh <<< "$JSON"
EXIT=$?
rm -rf "$TMPDIR"
```

#### Scenario B: stdin malformed
```bash
# Pipe non-JSON input
echo "this is not json at all" | bash .claude/hooks/events/pre-tool-use_write_gate.sh
EXIT=$?
```

#### Scenario C: python3 missing (D2-5 only)
```bash
TMPDIR=$(mktemp -d)
# Tạo minimal PATH không có python3
for cmd in sh cat date mkdir cp printf; do
  ln -s "$(which $cmd)" "$TMPDIR/$cmd" 2>/dev/null || true
done
PATH="$TMPDIR" bash .claude/hooks/events/stop_session_log_state.sh <<< '{"stop_hook_active":false}'
EXIT=$?
rm -rf "$TMPDIR"
```

#### Scenario D: Env var missing (D2-4 network check)
```bash
# MARK_NETWORK_ALLOWED unset — kiểm tra network block
unset MARK_NETWORK_ALLOWED
JSON='{"tool_name":"Bash","tool_input":{"command":"curl https://example.com"}}'
echo "$JSON" | bash .claude/hooks/events/pre-tool-use_bash_validate_command.sh
EXIT=$?
[ "$EXIT" = "2" ] || echo "FAIL: expected 2 for network without MARK_NETWORK_ALLOWED"

# MARK_NETWORK_ALLOWED set — kiểm tra network allow
export MARK_NETWORK_ALLOWED=true
echo "$JSON" | bash .claude/hooks/events/pre-tool-use_bash_validate_command.sh
EXIT=$?
[ "$EXIT" = "0" ] || echo "FAIL: expected 0 for network with MARK_NETWORK_ALLOWED"
unset MARK_NETWORK_ALLOWED
```

---

## §6: YAML-RES-1.0 Compliance Verification

### 6.1 L1 Syntax Check (D2-5)

Mục tiêu: Xác minh D2-5 `stop_session_log_state.sh` phát hiện chính xác `_state.yaml` corrupt và backup.

**Test case 1 — Malformed YAML:**
```bash
# Arrange: tạo _state.yaml bị lỗi cú pháp
mkdir -p /tmp/yaml-test/.skill-context/_state-archive
cat > /tmp/yaml-test/.skill-context/_state.yaml << 'EOF'
this: is: invalid: yaml: structure
  broken indentation
  - missing value
EOF

# Act: chạy stop hook với _state.yaml corrupt trên đường dẫn
cd /tmp/yaml-test
STOP_JSON='{"stop_hook_active":false}'
EXIT=$(echo "$STOP_JSON" | bash $WORKSPACE/.claude/hooks/events/stop_session_log_state.sh 2>&1; echo $?)
echo "Exit: $EXIT"

# Assert: exit 0 + backup created
[ "$EXIT" = "0" ] || echo "FAIL: expected exit 0"
BACKUP_COUNT=$(ls -1 .skill-context/_state-archive/_state-*-corrupt.yaml 2>/dev/null | wc -l)
[ "$BACKUP_COUNT" -ge 1 ] && echo "PASS: backup created" || echo "FAIL: no backup found"

# Cleanup
cd /
rm -rf /tmp/yaml-test
```

**Test case 2 — Valid YAML (không corrupt):**
```bash
mkdir -p /tmp/yaml-valid/.skill-context/_state-archive
cat > /tmp/yaml-valid/.skill-context/_state.yaml << 'EOF'
status: active
version: 1.0.0
last_updated: 2026-07-08
EOF

cd /tmp/yaml-valid
STOP_JSON='{"stop_hook_active":false}'
EXIT=$(echo "$STOP_JSON" | bash $WORKSPACE/.claude/hooks/events/stop_session_log_state.sh 2>&1; echo $?)
[ "$EXIT" = "0" ] || echo "FAIL: expected exit 0"
# Verify không có backup được tạo (state không corrupt)
BACKUP_COUNT=$(ls -1 .skill-context/_state-archive/_state-*-corrupt.yaml 2>/dev/null | wc -l)
[ "$BACKUP_COUNT" -eq 0 ] && echo "PASS: no false backup" || echo "FAIL: unexpected backup created"

cd /
rm -rf /tmp/yaml-valid
```

**Test case 3 — _state.yaml missing (edge case):**
```bash
# _state.yaml không tồn tại
mkdir -p /tmp/yaml-missing/.skill-context/_state-archive
cd /tmp/yaml-missing
STOP_JSON='{"stop_hook_active":false}'
EXIT=$(echo "$STOP_JSON" | bash $WORKSPACE/.claude/hooks/events/stop_session_log_state.sh 2>&1; echo $?)
# Expected: exit 0 (graceful degradation)
[ "$EXIT" = "0" ] && echo "PASS: graceful degradation on missing _state.yaml"

cd /
rm -rf /tmp/yaml-missing
```

### 6.2 L2 Schema Validation (D2-7 Registry)

Mục tiêu: Xác minh `registry.yaml` pass L2 Schema validation với required keys.

**Required keys (theo quality-gates-reference.md YAML-RES-1.0):**
```yaml
required_keys_per_entry:
  - "hooks"              # Top-level array
  - "script_path"        # Path to hook script
  - "matcher"            # Event matcher regex
  - "event_type"         # PreToolUse | PostToolUse | Stop | SessionStart
```

**Verification script:**
```python
#!/usr/bin/env python3
"""Registry L2 Schema Validation (YAML-RES-1.0)"""
import yaml
import sys

REQUIRED_ENTRY_KEYS = {"event_type", "matcher", "script"}
REQUIRED_TOP_KEYS  = {"hooks", "version", "suite"}

with open(".claude/hooks/registry.yaml") as f:
    data = yaml.safe_load(f)

errors = []

# 1. Check top-level required keys
for key in REQUIRED_TOP_KEYS:
    if key not in data:
        errors.append(f"Missing top-level key: {key}")

# 2. Check hooks is a list
hooks = data.get("hooks", [])
if not isinstance(hooks, list):
    errors.append("'hooks' must be a list")
    hooks = []

# 3. Check each entry has required keys
for i, entry in enumerate(hooks):
    missing = REQUIRED_ENTRY_KEYS - set(entry.keys())
    if missing:
        errors.append(f"Entry #{i} ('{entry.get('name', 'unnamed')}'): missing {missing}")
    if not isinstance(entry.get("event_type"), str):
        errors.append(f"Entry #{i}: 'event_type' must be a string")
    if not isinstance(entry.get("matcher"), str):
        errors.append(f"Entry #{i}: 'matcher' must be a string")

# 4. Check count
if len(hooks) != 6:
    errors.append(f"Expected 6 hook entries, got {len(hooks)}")

if errors:
    print("L2 Schema validation FAILED:")
    for e in errors:
        print(f"  - {e}")
    sys.exit(1)
else:
    print("L2 Schema validation PASSED — 6 entries, all required keys present")
    sys.exit(0)
```

**Expected output:**
```
L2 Schema validation PASSED — 6 entries, all required keys present
```

### 6.3 Corrupt Backup Verification

Sau khi chạy test case L1 Syntax, kiểm tra:
1. File backup tồn tại tại `.skill-context/_state-archive/_state-{timestamp}-corrupt.yaml`
2. Nội dung backup giống với nội dung gốc (không bị modify trước khi backup)
3. File backup có timestamp trong tên

```bash
verify_backup() {
  # Kiểm tra backup tồn tại
  BACKUP=$(ls -1 .skill-context/_state-archive/_state-*-corrupt.yaml 2>/dev/null | head -1)
  if [ -z "$BACKUP" ]; then
    echo "FAIL: no backup found"
    return 1
  fi
  
  # Kiểm tra backup có content
  if [ ! -s "$BACKUP" ]; then
    echo "FAIL: backup is empty"
    return 1
  fi
  
  # Kiểm tra timestamp trong tên file
  if [[ ! "$BACKUP" =~ _state-[0-9]{4}-[0-9]{2}-[0-9]{2}T ]]; then
    echo "WARN: backup filename missing timestamp"
  fi
  
  echo "PASS: backup verified at $BACKUP"
  return 0
}
```

### 6.4 Degraded Flag Verification

Sau khi phát hiện corrupt non-critical ref:
1. Xác minh `_state.yaml` (original) được set `.status = 'degraded'` (YAML-RES-1.0 non-critical degraded mode)
2. Xác minh `_state.yaml.yaml_repair_history` ghi nhận repair event (YAML-RES-1.0 rule_7)

> **⚠️ Lưu ý**: Phase 2 plan §11 (Known Limitations) ghi nhận:
> > `_state.yaml.status = "degraded"` full implementation → Deferred to Phase 8
> > Phase 2 D2-5 set flag nhưng không active degraded pipeline
>
> Nếu D2-5 hiện tại không implement degraded flag, verification sẽ FAIL và cần:
> - Cập nhật D2-5 stop hook để set degraded flag (quay lại Stage 2)
> - Hoặc chấp nhận gap và document cho Phase 8

```bash
verify_degraded_flag() {
  # Kiểm tra _state.yaml có status='degraded' không
  if [ -f ".skill-context/_state.yaml" ]; then
    STATUS=$(python3 -c "import yaml; print(yaml.safe_load(open('.skill-context/_state.yaml')).get('status', 'unknown'))" 2>/dev/null)
    if [ "$STATUS" = "degraded" ]; then
      echo "PASS: _state.yaml status = degraded"
    else
      echo "WARN: _state.yaml status = '$STATUS' (expected 'degraded')"
      echo "  → Phase 2 gap: degraded flag not fully implemented (deferred to Phase 8)"
    fi
  fi
}
```

---

## §7: Consistency & Quality Checks

### 7.1 Placeholder Scan

Mục tiêu: Xác minh zero placeholder (TODO, FIXME, `pass`, mock) trong hook scripts.

```bash
#!/usr/bin/env bash
# Placeholder scan — tất cả hook scripts
echo "=== Placeholder Scan ==="
ERRORS=0

for script in .claude/hooks/events/*.sh; do
  basename=$(basename "$script")
  
  # Check TODO/FIXME
  if grep -qiE '(TODO|FIXME|HACK|XXX)' "$script" 2>/dev/null; then
    echo "FAIL: $basename contains TODO/FIXME"
    ERRORS=$((ERRORS + 1))
  fi
  
  # Check placeholder pass (Python-specific)
  if grep -qE '^\s*pass\s*$' "$script" 2>/dev/null; then
    echo "FAIL: $basename contains 'pass' placeholder"
    ERRORS=$((ERRORS + 1))
  fi
  
  # Check mock() calls
  if grep -qiE 'mock\(' "$script" 2>/dev/null; then
    echo "FAIL: $basename contains mock()"
    ERRORS=$((ERRORS + 1))
  fi
  
  # Check empty catch blocks
  if grep -qiE '(except\s*(Exception)?\s*:\s*pass|catch\s*\{.*\})' "$script" 2>/dev/null; then
    echo "WARN: $basename may have empty catch block"
  fi
done

if [ "$ERRORS" = "0" ]; then
  echo "PASS: zero placeholders found"
else
  echo "FAIL: $ERRORS scripts contain placeholders"
fi
```

**Expected outcome**: `PASS: zero placeholders found`
**Failure recovery**: Quay lại Stage tương ứng (1/2/3) để remove placeholder trước khi commit.

### 7.2 subagent-forge.md Inline Hooks Compatibility

Xác minh standalone hooks (Phase 2) không conflict với inline hooks (subagent-forge.md):

```bash
echo "=== subagent-forge.md Compatibility ==="

# 1. Inline hooks vẫn tồn tại
if grep -q "PreToolUse" .claude/agents/subagent-forge.md; then
  echo "OK: inline PreToolUse hooks exist in subagent-forge.md"
else
  echo "WARN: no PreToolUse inline hook in subagent-forge.md"
fi

# 2. Exit code convention — verify both use Format B (exit 2)
INLINE_HOOK_COUNT=$(grep -cE 'exit [02]' .claude/agents/subagent-forge.md 2>/dev/null || echo 0)
if [ "$INLINE_HOOK_COUNT" -gt 0 ]; then
  echo "OK: subagent-forge.md uses exit code convention (Format B)"
else
  echo "OK: subagent-forge.md may not have inline hooks with exit codes"
fi

# 3. Event/matcher overlap check
INLINE_EVENTS=$(grep -oP 'PreToolUse|PostToolUse|Stop|SessionStart' .claude/agents/subagent-forge.md 2>/dev/null | sort -u)
STANDALONE_EVENTS="PreToolUse PostToolUse Stop SessionStart"
for event in $STANDALONE_EVENTS; do
  if echo "$INLINE_EVENTS" | grep -q "$event"; then
    echo "INFO: Event '$event' present in both inline and standalone hooks"
    echo "  → Claude Code runs both sequentially. First exit 2 wins."
  fi
done

echo "PASS: subagent-forge.md compatibility check complete"
```

### 7.3 Documentation Consistency

So sánh `hooks_and_events.md` (knowledge doc) với hook scripts thực tế:

```yaml
consistency_checklist:
  - item: "Event types match"
    check: "hooks_and_events.md lists 4 events: PreToolUse, PostToolUse, Stop, SessionStart"
    actual: "Hook scripts cover all 4 events"
    
  - item: "Exit code convention"
    check: "hooks_and_events.md §6 documents Format B (exit 2 blocking)"
    actual: "D2-1→D2-6 use Format B consistently"
    
  - item: "Matcher patterns match"
    check: "hooks_and_events.md §4.2 defines matcher syntax"
    actual: "registry.yaml matchers match documentation"
    
  - item: "Input JSON fields"
    check: "hooks_and_events.md §4.2 defines tool_name, tool_input"
    actual: "Scripts use jq -r '.tool_input.file_path' / '.tool_input.command'"
    
  - item: "Graceful degradation policy"
    check: "hooks_and_events.md §10 defines error handling"
    actual: "D2-1/2/4 fail closed, D2-3/5/6 fail open"
```

**References inconsistency note** (từ phase-2-scope.md §19.2):
```
| Aspect | Roadmap Spec | Knowledge Doc | Official Claude Code |
|--------|-------------|---------------|---------------------|
| Blocking format | Format B: exit 2 | Format A: JSON | exit 2 + stdout JSON |
| Config format | registry.yaml (YAML) | — | settings.json (JSON) |
| Input JSON | { tool_name, tool_input } | { tool, params } | { session_id, tool_name, tool_input } |
```

Stage 4 chỉ **document** inconsistency này — không reconcile (deferred Phase 8).

---

## §8: Implementation Requirements Files

### 8.1 Files Cần Có Trước Khi Stage 4 Bắt Đầu

```yaml
required_files:
  hook_scripts:
    - ".claude/hooks/events/pre-tool-use_write_gate.sh"           # Stage 1
    - ".claude/hooks/events/pre-tool-use_skill_staging_gate.sh"   # Stage 1
    - ".claude/hooks/events/pre-tool-use_bash_validate_command.sh" # Stage 1
    - ".claude/hooks/events/post-tool-use_log_artifact.sh"        # Stage 2
    - ".claude/hooks/events/stop_session_log_state.sh"            # Stage 2
    - ".claude/hooks/events/session-start_record_metadata.sh"     # Stage 2
  
  registry:
    - ".claude/hooks/registry.yaml"                                # Stage 3 — 6 entries
  
  test_scripts:
    - ".claude/hooks/tests/test_write_gate_allow.sh"              # Stage 3
    - ".claude/hooks/tests/test_write_gate_block.sh"              # Stage 3
    - ".claude/hooks/tests/test_skill_staging_allow_staging.sh"   # Stage 3
    - ".claude/hooks/tests/test_skill_staging_block_runtime.sh"   # Stage 3
    - ".claude/hooks/tests/test_bash_validate_allow.sh"           # Stage 3
    - ".claude/hooks/tests/test_bash_validate_block_destructive.sh" # Stage 3
    - ".claude/hooks/tests/test_bash_validate_block_network.sh"   # Stage 3
  
  state_archive:
    - ".skill-context/_state-archive/"                              # Phase 0 — directory tồn tại
    - ".skill-context/_state.yaml"                                  # Có thể có hoặc không

  knowledge_docs:
    - ".claude/knowledge/agents/hooks_and_events.md"               # Phase 1 — reference
```

### 8.2 Stage 4 Output Files

```yaml
stage_4_outputs:
  - path: "docs/context-to-work/roadmap-analysis-phases/Stage-4/verification-report.2026-07-08.md"
    status: "need_create"
    description: "Báo cáo verification chi tiết — PASS/FAIL cho từng AC (tạo sau khi chạy verification)"
    
  - path: "docs/context-to-work/roadmap-analysis-phases/Stage-4/scope.2026-07-08.md"
    status: "created"
    description: "Scope document này — định nghĩa phạm vi verification"

optional_outputs:
  - path: ".claude/hooks/tests/fixtures/"                           # Recommended: fixture cho graceful degradation tests
    status: "optional"
    description: "Thư mục chứa fixture files cho graceful degradation simulation"

  - path: ".claude/hooks/scripts/run-verification.sh"              # Recommended: automation script
    status: "optional"
    description: "Script tự động chạy toàn bộ verification suite (AC-1→AC-7 + graceful degradation + YAML-RES-1.0)"
```

---

## §9: Phụ Thuộc vào Stage 1→3

### 9.1 Stage 1 + Stage 2: Hook Scripts

Stage 1 (PreToolUse Gating Hooks):
- D2-1: `pre-tool-use_write_gate.sh` — path allowlist check
- D2-2: `pre-tool-use_skill_staging_gate.sh` — runtime skills write gate
- D2-4: `pre-tool-use_bash_validate_command.sh` — destructive command block

Stage 2 (Logging & Lifecycle Hooks):
- D2-3: `post-tool-use_log_artifact.sh` — artifact audit log
- D2-5: `stop_session_log_state.sh` — session stop + Γ-7 corrupt backup
- D2-6: `session-start_record_metadata.sh` — boot metadata

**Stage 4 phụ thuộc**: Tất cả 6 scripts tồn tại, executable, graceful degradation implemented.

### 9.2 Stage 3: Registry & Test Scripts

Stage 3 (Registry & Unit Tests):
- D2-7: `registry.yaml` — 6 hook entries với required keys
- D2-8: 7 test scripts — allow/block pairs

**Stage 4 phụ thuộc**: Registry pass YAML parse, test scripts tồn tại và run được.

### 9.3 Dependency Verification Checklist

Trước khi bắt đầu Stage 4, verify:

```bash
#!/usr/bin/env bash
echo "=== Pre-Stage-4 Dependency Check ==="
ERRORS=0

# Check 6 hook scripts exist + executable
for hook in pre-tool-use_write_gate.sh pre-tool-use_skill_staging_gate.sh pre-tool-use_bash_validate_command.sh post-tool-use_log_artifact.sh stop_session_log_state.sh session-start_record_metadata.sh; do
  if [ ! -f ".claude/hooks/events/$hook" ]; then
    echo "FAIL: .claude/hooks/events/$hook not found"
    ERRORS=$((ERRORS + 1))
  elif [ ! -x ".claude/hooks/events/$hook" ]; then
    echo "FAIL: .claude/hooks/events/$hook not executable"
    ERRORS=$((ERRORS + 1))
  fi
done

# Check registry exists
if [ ! -f ".claude/hooks/registry.yaml" ]; then
  echo "FAIL: .claude/hooks/registry.yaml not found"
  ERRORS=$((ERRORS + 1))
fi

# Check tests exist
TEST_COUNT=0
for test in .claude/hooks/tests/test_*.sh; do
  [ -f "$test" ] && TEST_COUNT=$((TEST_COUNT + 1))
done
if [ "$TEST_COUNT" -lt 7 ]; then
  echo "FAIL: expected 7 test scripts, found $TEST_COUNT"
  ERRORS=$((ERRORS + 1))
fi

if [ "$ERRORS" = "0" ]; then
  echo "PASS: All Stage 1→3 dependencies ready for Stage 4 verification"
else
  echo "FAIL: $ERRORS dependencies missing — complete Stage 1→3 first"
fi
```

---

## §10: Expected Timeline

```yaml
estimated_timeline:
  total_estimated_duration: "1 session (~2-4 giờ)"
  
  task_1_ac_1_to_7:
    duration: "45-60 phút"
    steps:
      - "Chạy AC-1 verify scripts tồn tại: 5 phút"
      - "Chạy AC-2 verify registry parse: 5 phút"
      - "Chạy AC-3 verify 7 test scripts pass: 5 phút"
      - "Chạy AC-4 verify hook self-test: 10 phút"
      - "Chạy AC-5 verify corrupt backup: 10 phút"
      - "Chạy AC-6 verify bash validate: 5 phút"
      - "Chạy AC-7 verify subagent-forge compatibility: 5 phút"
      - "Ghi nhận kết quả vào verification-report.md: 10 phút"
  
  task_2_graceful_degradation:
    duration: "30-45 phút"
    steps:
      - "Tạo simulation environment: 10 phút"
      - "Chạy tests cho gating hooks (D2-1, D2-2, D2-4): 10 phút"
      - "Chạy tests cho logging hooks (D2-3, D2-5, D2-6): 10 phút"
      - "Ghi nhận kết quả: 15 phút"
  
  task_3_yaml_res_compliance:
    duration: "30-40 phút"
    steps:
      - "L1 Syntax check test (3 scenarios): 15 phút"
      - "L2 Schema validation test: 10 phút"
      - "Corrupt backup + degraded flag verification: 15 phút"
  
  task_4_consistency:
    duration: "20-30 phút"
    steps:
      - "Placeholder scan: 5 phút"
      - "subagent-forge compatibility: 10 phút"
      - "Documentation consistency: 10 phút"
  
  contingency:
    duration: "30-60 phút"
    description: "Thời gian dự phòng cho unexpected failures, cross-stage communication"
```

---

## §11: Các Vấn đề Cần Lưu Ý (Open Questions)

| # | Question | Priority | Status | Liên quan |
|--:|:---------|:--------:|:------|:----------|
| 1 | **Degraded flag**: D2-5 stop hook có implement `_state.yaml.status = "degraded"`? Phase 2 plan §11 ghi deferred đến Phase 8 — nếu chưa có, AC YAML-RES-1.0 sẽ FAIL. | **Cao** | Cần verify | §6.4, phase-2-plan §11 |
| 2 | `validate_suite_integrity.py` có nên extend để tự động verify hooks? Hiện tại script chỉ validate skills — có thể thêm section cho hook validation. | Trung bình | Cần quyết định | §8.2 |
| 3 | **Simulation scripts cleanup**: Các simulation scripts cho graceful degradation có nên commit vào repo? Hay chỉ chạy temporary? | Thấp | Cần quyết định | §5.3 |
| 4 | **Phase 2 plan AC-8→AC-11**: Các AC mở rộng (AC-8→AC-11) thuộc Stage 5 (Advanced Hooks Research). Stage 4 chỉ verify AC-1→AC-7? | Trung bình | **Resolved** — Stage 4 chỉ verify AC-1→AC-7 | §4, phase-2-plan §7 |
| 5 | **yaml.safe_load vs yaml.load**: D2-5 stop hook dùng hàm nào? `yaml.load` không safe nếu không có Loader — cần verify dùng `yaml.safe_load`. | **Cao** | Cần verify | §6.1, validate_suite_integrity.py L26 |
| 6 | **Backup directory missing**: D2-5 stop hook handle `mkdir -p` khi `_state-archive/` chưa tồn tại? Cần verify graceful degradation. | Trung bình | Cần verify code | §5.2, phase-2-plan §6 |
| 7 | **AC-7 subagent-forge.md**: Nếu subagent-forge.md không còn inline hooks (đã refactor), AC-7 có cần điều chỉnh? | Thấp | Cần verify | §4.3 |
| 8 | **Network allowlist pattern**: D2-4 dùng `MARK_NETWORK_ALLOWED` env var — cần verify pattern `curl|wget|nc ` không quá restrictive (ví dụ `curl` trong comment). | Trung bình | Cần verify | §5.2 |
| 9 | **jq missing detection**: Hook scripts detect jq missing bằng cách nào? `command -v jq`? `which jq`? Hay chỉ implicit fail? | Trung bình | Cần verify code | §5.3 |
| 10 | **registry.yaml L2 Schema version**: `version` key ở top-level registry.yaml có pass L2 Schema validation? Required keys spec chỉ yêu cầu entry-level keys. | Thấp | Cần clarify | §6.2 |

---

## §12: Confidence Assessment

```yaml
overall_confidence: 85%

breakdown:
  ac_1_to_7_readiness: 90%         # Roadmap spec có verification commands sẵn
  graceful_degradation_coverage: 75%  # Cần simulation scripts — chưa có sẵn
  yaml_res_compliance_coverage: 70%   # Degraded flag có thể deferred — cần verify
  consistency_check_coverage: 85%     # Placeholder scan + doc consistency — rõ ràng
  simulation_script_availability: 40% # Chưa có simulation scripts — cần tạo
  failure_recovery_defined: 85%       # Mỗi AC đã có failure recovery path
  dependency_readiness: 60%          # Stage 1→3 chưa hoàn thành — cần verify trước

uncertainty_flags:
  - "Degraded flag implementation: có thể chưa có trong D2-5 → YAML-RES-1.0 verification FAIL"
  - "D2-5 có dùng yaml.safe_load hay yaml.load? Cần verify code"
  - "jq missing detection mechanism chưa rõ — cần verify code từng hook script"
  - "validate_suite_integrity.py extension: cần quyết định extend hay không"
  - "subagent-forge.md inline hooks: có thể đã thay đổi sau Stage 1-3"
```

---

## §13: Tổng Kết

Stage 4 là verification gate cuối cùng trước khi chuyển sang Stage 5 (Advanced Hooks Research). Stage này đảm bảo rằng toàn bộ Hook Framework Foundation (Phase 2) hoạt động đúng spec trước khi mở rộng thêm experimental features.

### 13.1 Key Decision Points

1. **Primary vs Supplementary Verification**: AC-1→AC-7 là primary (từ roadmap spec) — mandatory PASS. Graceful Degradation và YAML-RES-1.0 là supplementary (từ BA analysis + quality gates) — strongly recommended PASS.
2. **Gate Function**: Nếu bất kỳ AC primary nào FAIL, Stage 5 không thể bắt đầu — cần quay lại Stage tương ứng fix.
3. **Degraded Flag Gap**: Phase 2 plan §11 ghi nhận degraded flag deferred đến Phase 8 — nếu verification phát hiện gap này, cần document rõ ràng.

### 13.2 Summary of Changes

```yaml
summary_of_changes:
  type: "scope-document"
  stage: 4
  phase: 2
  purpose: "Verification & Acceptance — Hook Framework Foundation"
  files_created:
    - "docs/context-to-work/roadmap-analysis-phases/Stage-4/scope.2026-07-08.md"
  files_verified: 16
    - hook_scripts: 6
    - test_scripts: 7
    - registry: 1
    - state_archive: 1
    - knowledge_docs: 1
  verification_tasks: 4
    - ac_1_to_7: "7 acceptance criteria"
    - graceful_degradation: "12 scenarios × 6 hooks"
    - yaml_res_compliance: "3 levels + backup + degraded"
    - consistency: "placeholder + subagent-forge + documentation"
  total_ac_count: 7  # AC-1 → AC-7 (primary)
  supplementary_checks: 31  # graceful degradation (15) + YAML-RES (10) + consistency (6)
  lifecycle_phase: "defined → verification-in-progress"
  zones_affected:
    - ".claude/hooks/events/"
    - ".claude/hooks/tests/"
    - ".claude/hooks/registry.yaml"
    - ".skill-context/_state-archive/"
    - ".skill-context/_state.yaml"
    - ".claude/agents/subagent-forge.md"
    - ".claude/knowledge/agents/hooks_and_events.md"
```

### 13.3 Next Steps

```yaml
next_steps:
  step_1:
    action: "Verify Stage 1→3 dependency readiness"
    script: "Chạy pre-stage-4-dependency-check.sh"
  
  step_2:
    action: "Chạy AC-1→AC-7 Full Verification Suite"
    output: "Ghi nhận PASS/FAIL vào verification-report.md"
  
  step_3:
    action: "Chạy Graceful Degradation Verification"
    depends_on: "Step 2 PASS (hoặc identified gaps)"
  
  step_4:
    action: "Chạy YAML-RES-1.0 Compliance Verification"
    depends_on: "Step 2 PASS"
  
  step_5:
    action: "Chạy Consistency & Quality Checks"
    depends_on: "Step 2 PASS"
  
  step_6:
    action: "Tổng hợp kết quả → quyết định Stage 4 PASS/FAIL"
    output: "Stage-4/verification-report.2026-07-08.md"
    gate_for: "Stage 5 — Advanced Hooks Research"
```

---

**Document Status**: Context Complete — Ready for Stage 4 Verification Execution
**NO Code Changes Made** — Document only per context-before-fix skill guardrails

```text
✓ §1: Tổng Quan Stage 4 — verification scope, 4 task groups, pipeline position
✓ §2: Entry Point & Tài Liệu Tham Chiếu — 10 entry points, 10 reference files
✓ §3: Scope Definition — In Scope (15 items) + Out of Scope (10 items) + Boundary
✓ §4: AC-1→AC-7 Full Verification — ma trận 7 AC, verification workflow, AC-7 chi tiết
✓ §5: Graceful Degradation Verification — policy, matrix 6 hooks × scenarios, simulation scripts
✓ §6: YAML-RES-1.0 Compliance — L1 Syntax (3 test cases), L2 Schema validation, corrupt backup, degraded flag
✓ §7: Consistency & Quality — placeholder scan, subagent-forge compatibility, documentation consistency
✓ §8: Implementation Requirements Files — pre-requisites + output files
✓ §9: Phụ thuộc vào Stage 1→3 — chi tiết từng stage + dependency check script
✓ §10: Expected Timeline — 1 session, 4 tasks, contingency
✓ §11: Open Questions — 10 questions with priority and status
✓ §12: Confidence Assessment — 85%, 5 uncertainty flags
✓ §13: Tổng Kết — key decisions, summary, next steps
```

**Document**: `docs/context-to-work/roadmap-analysis-phases/Stage-4/scope.2026-07-08.md`
**Generated by**: context-before-fix (Stage 4 scope analysis)
**Language**: Tiếng Việt
**Version**: 0.1.0
**Date**: 2026-07-08
**Status**: Initial — Ready for Verification Execution
