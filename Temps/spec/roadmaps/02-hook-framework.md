# Phase 2 — Hook Framework Foundation

> **Order:** 3rd phase | **Estimated effort:** M (medium) | **Predicted duration:** 1-2 sessions
> **Depends on:** Phase 0, Phase 1
> **Downstream:** Phase 3 (Agents), Phase 5/6/7 (Skills)
> **Architectural defects addressed:** Γ-7 (escalation recursion), Γ-1 (self-referential blindness — chèn ground-truth validator bằng hook bảo vệ critical writes)

## Mục đích

Phase 2 xây dụng hệ thống **standalone hook framework** tại `.claude/hooks/` — chuyển từ "inline hooks only" (hiện subagent-forge có 2 biến inline) sang hệ thống hooks rõ rời, có registry, có unit test cho từng event.

Hooks là **thành phần bị nhìn nhận là third pillar** của workflow tích hợp Skills + Agents + Hooks:
- Skills = nội dung / tri thức
- Agents = trình thực thi
Phase 2 address architectural defect Γ-1 (LLM self-audit không thể đảm bảo chất lượng) bằng cách thêm máy dịch chuyển ra LLM — shell exits với `exit 2` để block.

> ⚠️ **Quyết định Thiết kế (Hook Format Gap)**: Mặc dù tài liệu `hooks_and_events.md` (Phase 1) mô tả cả hai định dạng block (Format A: stdout JSON `permissionDecision` và Format B: exit code 2), Phase 2 sẽ **thống nhất sử dụng Format B (exit code 2)** cho toàn bộ 6 hooks đầu tiên để đảm bảo tính đơn giản và tối giản (YAGNI). Việc đối khớp và migrate sang cấu trúc JSON stdout (Format A) để phục vụ cho việc chain hooks sẽ được thực hiện tại Phase 8.

---

## Prerequisites

```yaml
prerequisites:
  - Phase 0 done
  - Phase 1 done (hooks_and_events.md là contract spec)
  - jq CLI có sẵn trên PATH
  - bash ≥ 4.0 hoặc zsh có sẵn
  - Hooks phải là shell scripts, không dùng Python (vì hook chạy mỗi tool call — phải nhanh < 100ms)
```

---

## Design principle cho hooks

```yaml
hook_design_principles:
  - "Hooks là cơ học, không semantic — Hook không 'hiểu' agent output, chỉ verify cấu trúc/exit code"
  - "Hooks phải < 50 dòng, < 100ms execution time"
  - "Hooks không bao giờ spawn sub-task (trigger agent); chỉ verify deny/allow decision"
  - "Hooks phải fail-safe: nếu input malformed, default = allow phase (loose enforcement) → post-tool verify catch-up"
  - "Hooks không write file (trừ audit logs); chỉ read state"
  - "Standalone preferred over inline — cho reuse cross-agent"
```

---

## Deliverables (file-by-file)

### D2-1: `.claude/hooks/events/pre-tool-use_write_gate.sh`

Hook dùng PreToolUse matcher `Write|Edit` để block writes ngoài sandbox paths.

```bash
#!/usr/bin/env bash
# Gate: Write|Edit tool — block writes outside allowlisted paths
# Piped JSON stdin: { tool_name, tool_input: { file_path, content } }
# Exit 0 = allow, Exit 2 = block

INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')

# Fail-safe: if no file_path extracted (e.g., Bash tool), allow
[ -z "$FILE_PATH" ] && exit 0

# Canonical allowlist (canonical paths, never modify without commit review)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
ALLOWLIST_REGEX="^${WORKSPACE_ROOT}/(\.claude/|skills/ver-3/|\.skill-context/|docs/context-to-work/|Temps/spec/)"

if [[ ! "$FILE_PATH" =~ $ALLOWLIST_REGEX ]]; then
  echo "BLOCKED: write target outside WASHVN workspace: $FILE_PATH" >&2
  echo "Allowed prefixes: .claude/, skills/ver-3/, .skill-context/, docs/, Temps/spec/" >&2
  exit 2
fi

exit 0
```

### D2-2: `.claude/hooks/events/pre-tool-use_skill_staging_gate.sh`

Hook bảo vệ `.claude/skills/` runtime — chỉ cho phép Phase 8 canonical deploy; tất cả skill build phải stage tại `skills/ver-3/<name>/` trước.

```bash
#!/usr/bin/env bash
# Block writes to runtime .claude/skills/ unless explicit deploy_run

INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')
[ -z "$FILE_PATH" ] && exit 0

# Block pattern: writes to .claude/skills/<any>/ except for git.staging/
if [[ "$FILE_PATH" =~ \.claude/skills/ ]] && [[ ! "$FILE_PATH" =~ \.claude/skills/_staging/ ]]; then
  # Unless DEPLOY_PHASE_ACTIVE env var is set (reserved for deployflow)
  if [ -z "$WASHVN_DEPLOY_PHASE_ACTIVE" ]; then
    echo "BLOCKED: writes to runtime .claude/skills/ gated. Edit at skills/ver-3/<name>/ then deploy via 'deploy-skill <name>'." >&2
    exit 2
  fi
fi

exit 0
```

### D2-3: `.claude/hooks/events/post-tool-use_log_artifact.sh`

Hook PostToolUse matcher `Write|Edit` — log mọi artifact write tới audit log.

```bash
#!/usr/bin/env bash
# Audit-logs every artifact write (no enforcement, just side-effect)
# Input: { tool_name, tool_input, tool_output }
# Exit 0 = allow output

INPUT=$(cat)
TOOL=$(echo "$INPUT" | jq -r '.tool_name // empty')
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')

[ -z "$FILE_PATH" ] && exit 0

# Audit log path
LOG=".skill-context/_state-archive/tool-audit-$(date +%Y-%m-%d).log"
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
AGENT="${CLAUDE_AGENT_NAME:-parent}"
PID_CP="${$}"

printf '%s\t%s\tpid=%s\tagent=%s\ttool=%s\tpath=%s\n' \
  "$TIMESTAMP" "WRITE" "$PID_CP" "$AGENT" "$TOOL" "$FILE_PATH" >> "$LOG"

exit 0
```

### D2-4: `.claude/hooks/events/pre-tool-use_bash_validate_command.sh`

Gate Bash tool — block destructive commands và commands cấm.

```bash
#!/usr/bin/env bash
# Block destructive bash patterns: rm -rf, truncate, dd of=, mv over, sudo, ...

INPUT=$(cat)
CMD=$(echo "$INPUT" | jq -r '.tool_input.command // empty')

[ -z "$CMD" ] && exit 0

# Pattern blocklist
if echo "$CMD" | grep -qE "(rm -rf|sudo |truncate -s 0|dd of=/dev/|chmod -R|chown -R .* /|> */dev/)"; then
  echo "BLOCKED: destructive pattern detected in Bash command" >&2
  echo "Command snippet: $(echo "$CMD" | head -c 200)" >&2
  exit 2
fi

# Phase-specific gate:阻止 running external network from skill scripts not trong allowlist
if echo "$CMD" | grep -qE "(curl|wget|nc )"; then
  # Only allowed if env MARK_NETWORK_ALLOWED set (e.g., inside sandbox-tester)
  if [ -z "$MARK_NETWORK_ALLOWED" ]; then
    echo "BLOCKED: network access requires MARK_NETWORK_ALLOWED env var (sandbox-tester only)" >&2
    exit 2
  fi
fi

exit 0
```

### D2-5: `.claude/hooks/events/stop_session_log_state.sh`

Stop hook — log session end state.

```bash
#!/usr/bin/env bash
# Stop hook: log session termination status to audit
# Input: { stop_hook_active }
# Exit 0 = allow stop

INPUT=$(cat)
STOP_ACTIVE=$(echo "$INPUT" | jq -r '.stop_hook_active // false')

LOG=".skill-context/_state-archive/session-$(date +%Y-%m-%d).log"
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

# Log session stop
printf '%s\tSTOP\tstop_hook_active=%s\n' "$TIMESTAMP" "$STOP_ACTIVE" >> "$LOG"

# CRITICAL — Phase 0 failsafe: preinit backup if pipeline state corrupt (Γ-7 fix)
STATE_FILE=".skill-context/_state.yaml"
if [ -f "$STATE_FILE" ]; then
  if ! python3 -c "import yaml; yaml.safe_load(open('$STATE_FILE'))" 2>/dev/null; then
    # _state.yaml corrupt — create backup before any re-init
    BACKUP=".skill-context/_state-archive/_state-${TIMESTAMP}-corrupt.yaml"
    cp "$STATE_FILE" "$BACKUP"
    echo "STATE CORRUPT: backed up to $BACKUP before any re-init" >> "$LOG"
  fi
fi

exit 0
```

### D2-6: `.claude/hooks/events/session-start_record_metadata.sh`

SessionStart hook — record boot metadata.

```bash
#!/usr/bin/env bash
# SessionStart hook: record session metadata
# Input: { cwd, pid, boot_id, session_id }
# Exit 0 = allow session to start

INPUT=$(cat)

CWD=$(echo "$INPUT" | jq -r '.cwd // empty')
PID=$(echo "$INPUT" | jq -r '.pid // empty')
BOOT_ID=$(echo "$INPUT" | jq -r '.boot_id // empty')
SESSION_ID=$(echo "$INPUT" | jq -r '.session_id // empty')

LOG=".skill-context/_state-archive/session-start.log"
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

printf '%s\tSTART\tsession=%s\tpid=%s\tboot=%s\tcwd=%s\n' \
  "$TIMESTAMP" "$SESSION_ID" "$PID" "$BOOT_ID" "$CWD" >> "$LOG"

# Optional: Create session-tracking.json entry nếu exists under OMC
TRACKING=".claude/skills/.omc/state/session-started.json"
# (Let OMC manage this if present; nếu không có, ghi vào log)

exit 0
```

### D2-7: `.claude/hooks/registry.yaml` (full)

Compile registry đầy đủ:

```yaml
hooks:
  - name: pre-write-workspace-gate
    event_type: PreToolUse
    matcher: "Write|Edit"
    script: .claude/hooks/events/pre-tool-use_write_gate.sh
    description: "Block writes outside WASHVN workspace allowlist"
    exit_allow: 0
    exit_block: 2
  
  - name: pre-skill-staging-gate
    event_type: PreToolUse
    matcher: "Write|Edit"
    script: .claude/hooks/events/pre-tool-use_skill_staging_gate.sh
    description: "Block writes to runtime .claude/skills/ unless explicit deploy phase active"
    exit_allow: 0
    exit_block: 2
  
  - name: pre-bash-validate-command
    event_type: PreToolUse
    matcher: "Bash"
    script: .claude/hooks/events/pre-tool-use_bash_validate_command.sh
    description: "Block destructive bash patterns (rm -rf, sudo, truncate, dd of=)"
    exit_allow: 0
    exit_block: 2
  
  - name: post-write-audit-log
    event_type: PostToolUse
    matcher: "Write|Edit"
    script: .claude/hooks/events/post-tool-use_log_artifact.sh
    description: "Audit-log every artifact write to daily log file"
    exit_allow: 0
  
  - name: stop-session-state-archive
    event_type: Stop
    matcher: ".*"
    script: .claude/hooks/events/stop_session_log_state.sh
    description: "Log session stop + backup corrupt _state.yaml before any re-init (Γ-7 fix)"
    exit_allow: 0
  
  - name: session-start-record
    event_type: SessionStart
    matcher: ".*"
    script: .claude/hooks/events/session-start_record_metadata.sh
    description: "Record session metadata on boot"
    exit_allow: 0

version: 1.0.0
suite: WASHVN
last_updated: 2026-07-04
maintainer: steve
```

### D2-8: Test scripts (one per hook)

Tạo `.claude/hooks/tests/` directory với một test file per hook để verify nó hoạt động chính xác.

```text
.claude/hooks/tests/
├── test_write_gate_allow.sh
├── test_write_gate_block.sh
├── test_skill_staging_allow_staging.sh
├── test_skill_staging_block_runtime.sh
├── test_bash_validate_allow.sh
├── test_bash_validate_block_destructive.sh
└── test_bash_validate_block_network.sh
```

Mỗi test script:
- Pipe một stdin JSON vào hook script
- Verify exit code (0 or 2)
- Verify stderr output matches expected pattern

Ví dụ `test_write_gate_block.sh`:

```bash
#!/usr/bin/env bash
# Test: pre-tool-use_write_gate.sh blocks non-workspace writes

set -e
JSON='{"tool_name":"Write","tool_input":{"file_path":"/tmp/test.txt"}}'
EXIT=0
echo "$JSON" | bash .claude/hooks/events/pre-tool-use_write_gate.sh 2>&1 || EXIT=$?

[ "$EXIT" = "2" ] || { echo "FAIL: expected exit 2, got $EXIT"; exit 1; }
echo "PASS: hook blocks /tmp write"
```

---

## Verification checklist (cơ học)

### AC-1 — 6 hook scripts tồn tại và executable
```bash
for hook in pre-tool-use_write_gate.sh pre-tool-use_skill_staging_gate.sh pre-tool-use_bash_validate_command.sh post-tool-use_log_artifact.sh stop_session_log_state.sh session-start_record_metadata.sh; do
  test -f .claude/hooks/events/$hook
  test -x .claude/hooks/events/$hook
done
echo "AC-1 PASS"
```

### AC-2 — Registry parses
```bash
python3 -c "import yaml; data = yaml.safe_load(open('.claude/hooks/registry.yaml')); assert len(data['hooks']) == 6"
echo "AC-2 PASS"
```

### AC-3 — Hook tests run + pass
```bash
for test in .claude/hooks/tests/test_*.sh; do
  bash $test || exit 1
done
echo "AC-3 PASS"
```

### AC-4 — Hook self-test (reverse direction)
```bash
# Test allow case:
WORKSPACE_ROOT="$(pwd)"
JSON_INSIDE="{\"tool_name\":\"Write\",\"tool_input\":{\"file_path\":\"\${WORKSPACE_ROOT}/skills/ver-3/test/SKILL.md\"}}"
EXIT=$(echo "$JSON_INSIDE" | bash .claude/hooks/events/pre-tool-use_write_gate.sh 2>&1; echo $?)
[ "$EXIT" = "0" ] || exit 1

# Test block case:
JSON_OUTSIDE='{"tool_name":"Write","tool_input":{"file_path":"/etc/passwd"}}'
EXIT=$(echo "$JSON_OUTSIDE" | bash .claude/hooks/events/pre-tool-use_write_gate.sh 2>&1; echo $?)
[ "$EXIT" = "2" ] || exit 1
echo "AC-4 PASS"
```

### AC-5 — Corrupt state backup trigger works (Γ-7 fix at hook level)
```bash
# Simulate corrupt _state.yaml:
echo "this: is: invalid: yaml" > /tmp/test_state.yaml
mkdir -p /tmp/hook_test_dir
cd /tmp/hook_test_dir
ln -sf /tmp/test_state.yaml .skill-context/_state.yaml 2>/dev/null || \
  mkdir -p .skill-context/_state-archive && cp /tmp/test_state.yaml .skill-context/_state.yaml

# Run stop hook:
STOP_JSON='{"stop_hook_active":false}'
EXIT=$(echo "$STOP_JSON" | bash .claude/hooks/events/stop_session_log_state.sh 2>&1; echo $?)
[ "$EXIT" = "0" ] || exit 1

# Verify backed up
ls .skill-context/_state-archive/_state-*-corrupt.yaml > /dev/null || exit 1
echo "AC-5 PASS"
# Cleanup:
rm -rf /tmp/hook_test_dir /tmp/test_state.yaml
```

### AC-6 — Bash validate distinguishes allow/block
```bash
JSON_ALLOW='{"tool_name":"Bash","tool_input":{"command":"ls -la"}}'
JSON_BLOCK='{"tool_name":"Bash","tool_input":{"command":"rm -rf /home"}}'
EXIT_ALLOW=$(echo "$JSON_ALLOW" | bash .claude/hooks/events/pre-tool-use_bash_validate_command.sh 2>&1 > /dev/null; echo $?)
EXIT_BLOCK=$(echo "$JSON_BLOCK" | bash .claude/hooks/events/pre-tool-use_bash_validate_command.sh 2>&1 > /dev/null; echo $?)
[ "$EXIT_ALLOW" = "0" ] && [ "$EXIT_BLOCK" = "2" ] || exit 1
echo "AC-6 PASS"
```

### AC-7 — Phase 0 subagent-forge.md inline hooks validated tương tự behavior

```bash
# Verify: subagent-forge.md inline hooks still work alongside standalone hooks.
# (subagent-forge inline hooks không break — chỉ standalone hooks thêm vào layered defense.)
grep -q "PreToolUse" .claude/agents/subagent-forge.md || exit 1
echo "AC-7 PASS"
```

---

## Step-by-step task list

1. **Author .claude/hooks/events/pre-tool-use_write_gate.sh** (D2-1) — ≤ 50 dòng bash. Test allow vs block.
   → commit `phase-2: write gate hook`

2. **Author .claude/hooks/events/pre-tool-use_skill_staging_gate.sh** (D2-2) — block runtime skills write.
   → commit `phase-2: skill staging gate`

3. **Author .claude/hooks/events/pre-tool-use_bash_validate_command.sh** (D2-4) — destructive patterns block.
   → commit `phase-2: bash command validator`

4. **Author post-write-audit-log.sh** (D2-3) — log all writes.
   → commit `phase-2: post-write audit logger`

5. **Author stop_session_log_state.sh** (D2-5) — with corrupt _state.yaml backup logic (Γ-7 fix).
   → commit `phase-2: stop hook + state corruption backup`

6. **Author session-start_record_metadata.sh** (D2-6) — record boot metadata.
   → commit `phase-2: session start metadata recorder`

7. **Author .claude/hooks/registry.yaml** (D2-7) — full registry with 6 hooks.
   → commit `phase-2: hook registry updated`

8. **Author 7 test scripts** trong .claude/hooks/tests/
   → commit `phase-2: hook test suite`

9. **Run full AC-1 to AC-7** — fix any failures.
   → commit `phase-2: acceptance criteria pass`

---

## Definition of done (Phase 2)

```yaml
dod:
  - 6 hook scripts executable, đã test
  - Registry parses thành công với 6 entries
  - 7 test scripts tồn tại, tất cả PASS
  - Hook boundary behaviors tested:
    + Write outside workspace: blocked
    + Write inside workspace: allowed
    + Bash destructive command: blocked
    + Bash normal command: allowed
    + Stop với _state.yaml corrupt: backup created (Γ-7 fix verified at hook level)
  - Audit log directory tồn tại với at least 1 entry sau test run
```

---

## Liên kết

- [Roadmap Index](index.md)
- [Phase 1 trước](01-knowledge-base-authoring.md)
- [Phase 3 kế tiếp](03-agent-foundation.md)
- [Hooks_and_events.md spec](../../../.claude/knowledge/agents/hooks_and_events.md)
- [Reference: subagent-forge.md hooks block](../../../.claude/agents/subagent-forge.md#L9-L30)