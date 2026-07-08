---
name: stage-2-scope
description: Phân tích phạm vi chi tiết cho Stage 2 — Logging & Session Lifecycle Hooks (D2-3, D2-5, D2-6)
version: 0.2.0
suite: WASHVN
tags: [stage-2, hook-framework, logging, audit, session-lifecycle, yaml-resilience, gamma-7]
trace: [TỪ SCOPE phase-2-scope.2026-07-07.md §5.1, §8.2, §14.2], [TỪ PLAN phase-2-plan.2026-07-07.md §4, §6]
when_to_use: "Khi cần triển khai Stage 2 của Phase 2 — xây dựng logging hooks & session lifecycle hooks"
---

# Stage 2 — Logging & Session Lifecycle Hooks: Scope Document

> **Ngày**: 2026-07-08 | **Feature**: Phase 2 — Hook Framework Foundation (Stage 2/5)
> **Mục tiêu**: Xây dựng 3 hooks PostToolUse audit log (D2-3) + Stop session log Γ-7 fix YAML-RES-1.0 (D2-5) + SessionStart metadata (D2-6)
> **Trạng thái**: Context Complete — Ready for implementation

---

## Tổng Quan Stage 2

Stage 2 xây dựng **3 logging/session lifecycle hooks** (Layer 1 — Command-based). Khác Stage 1 (gating fail CLOSED), Stage 2 là **non-blocking fail OPEN**:

| ID | Hook Script | Mục đích | Event | Matcher | Exit | Phân loại |
|:--:|:------------|:---------|:------|:--------|:----:|:---------:|
| **D2-3** | `post-tool-use_log_artifact.sh` | Audit-log mọi artifact write | PostToolUse | Write\|Edit | 0 | Logging — fail OPEN |
| **D2-5** | `stop_session_log_state.sh` | Log stop + Γ-7 corrupt backup + YAML-RES-1.0 L1 | Stop | .* | 0 | Logging — fail OPEN (YAML optional) |
| **D2-6** | `session-start_record_metadata.sh` | Record boot metadata (cwd, pid, boot_id, session_id) | SessionStart | .* | 0 | Logging — fail OPEN |

### So sánh Stage 1 vs Stage 2

| Tiêu chí | Stage 1 (Gating) | Stage 2 (Logging) |
|:---------|:-----------------|:------------------|
| **Fail behavior** | FAIL CLOSED — exit 2 khi lỗi | FAIL OPEN — exit 0, skip log |
| **Side effect** | Không ghi file | Ghi audit logs TSV vào `_state-archive/` |
| **Block tool call?** | Có (exit 2) | Không (exit 0 always) |
| **Python policy** | Không dùng Python | D2-5 được phép (YAML parsing) |
| **Complexity** | D2-4 trung bình (regex) | D2-5 trung bình-cao (YAML + backup) |
| **Dependency** | jq bắt buộc | jq optional (fail OPEN skip) |

### Liên kết Stage

| Stage | Liên quan | Ghi chú |
|:------|:----------|:--------|
| Stage 1 (D2-1, D2-2, D2-4) | PreToolUse gates | **Độc lập** — có thể build song song |
| Stage 3 (D2-7 registry) | Populate registry | Stage 2 paths cần có trước |
| Stage 4 (Verification) | AC-1, AC-5 | Prerequisite cho AC-1 (6 hooks), AC-5 (Γ-7 fix) |
| Stage 5 (D2-9) | Prompt hook on Stop | D2-5 → D2-9 chain trên Stop event |

---

## §1: Entry Point & Tài Liệu Tham Chiếu

| Entry | Path | Nội dung |
|:------|:-----|:---------|
| **Plan checklist** | `phase-2-plan.2026-07-07.md` §4 Stage 2 | Task list 3 hooks + graceful degradation subtasks |
| **Roadmap spec (code mẫu)** | `skills/ver-3/roadmaps/02-hook-framework.md` D2-3, D2-5, D2-6 | Code mẫu đầy đủ cho cả 3 scripts |
| **Scope tổng thể** | `phase-2-scope.2026-07-07.md` §5.1, §8.2, §14.2 | Deliverables map, audit log format, Γ-7 fix |
| **YAML Resilience Layer** | `Temps/spec/architects/P5-fallback-and-escalation/yaml-resilience-layer.md` | rule_9 last-mile, 3-level pre-check |
| **Quality Gates** | `Temps/spec/architects/shared/quality-gates-reference.md` | YAML-RES-1.0 (L1 Syntax → D2-5) |
| **Suite config** | `.skill-context/suite_config.yaml` | state_archive.path, pre_reinit_backup |
| **Official hook docs** | `.claude/knowleages/hooks/hooks.md` line 591-715 | stdin JSON schema, exit code convention |
| **Hook protocol** | `.claude/knowledge/agents/hooks_and_events.md` §5-6, §10 | Dual-Format protocol, error handling |
| **Reference pattern** | `.claude/knowledge/agents/examples.md` line 215-305 | db-reader hook template |

---

## §2: Scope Definition

### 2.1 In Scope

```yaml
scripts_create:
  - id: D2-3; path: "post-tool-use_log_artifact.sh"; lines: ~15
    purpose: "Audit-log Write|Edit vào tool-audit-{date}.log TSV"
  - id: D2-5; path: "stop_session_log_state.sh"; lines: ~35
    purpose: "Log stop + Γ-7 corrupt backup + YAML-RES-1.0 L1 Syntax check"
  - id: D2-6; path: "session-start_record_metadata.sh"; lines: ~20
    purpose: "Record boot metadata (cwd, pid, boot_id, session_id) vào session-start.log"

audit_logs:
  - "tool-audit-{YYYY-MM-DD}.log — TSV: timestamp\\tWRITE\\tpid=N\\tagent=N\\ttool=T\\tpath=P"
  - "session-{YYYY-MM-DD}.log — TSV: timestamp\\tSTOP\\tstop_hook_active=bool"
  - "session-start.log — TSV: timestamp\\tSTART\\tsession=ID\\tpid=N\\tboot=ID\\tcwd=P"

yaml_resilience:
  d2_5: ["L1 Syntax: pyyaml yaml.safe_load()", "Γ-7: backup corrupt → _state-{ts}-corrupt.yaml"]
  deferred: ["L2 Schema", "L3 Cross-ref", "Auto-repair", "degraded flag", "rule_7 repair_history"]

graceful_degradation:
  d2_3_d2_6: ["jq missing → exit 0 skip", "stdin malformed → exit 0", "log dir missing → mkdir -p → exit 0"]
  d2_5: ["python3 unavailable → exit 0 + WARNING", "_state.yaml not exist/empty → skip",
         "backup cp fail → WARNING", "state file missing → exit 0"]
```

### 2.2 Out of Scope

- KHÔNG tạo PreToolUse gating hooks (Stage 1)
- KHÔNG populate registry.yaml / test scripts (Stage 3)
- KHÔNG implement Prompt-based hook (Stage 5)
- KHÔNG set `_state.yaml.status = 'degraded'` — chỉ backup
- KHÔNG auto-repair YAML (Phase 8)
- KHÔNG dùng Python cho D2-3, D2-6
- KHÔNG log content file — privacy
- KHÔNG implement log rotation/retention policy

### 2.3 Boundary

- Script < 50 dòng, execution < 100ms (D2-5 python < 500ms)
- Ngôn ngữ: bash + jq. D2-5 thêm python3 optional
- Chỉ ghi audit logs tại `_state-archive/` — không ghi file khác
- Mọi lỗi exit 0 — fail OPEN
- TSV dùng `printf` với `\t` — không `echo`

---

## §3: Phân Tích Chi Tiết Từng Hook

### 3.1 D2-3: `post-tool-use_log_artifact.sh`

#### Mục đích
Ghi nhận mọi Write/Edit thành công vào audit log. Non-blocking — exit 0.

#### Input / Output

```yaml
event: PostToolUse | matcher: "Write|Edit"
stdin: { tool_name, tool_input: { file_path, content }, tool_response, duration_ms }
extract: ".tool_input.file_path" + ".tool_name"
log_file: ".skill-context/_state-archive/tool-audit-{YYYY-MM-DD}.log"
log_format: "TSV 6 columns: timestamp, WRITE, pid=$$, agent=$CLAUDE_AGENT_NAME, tool, path"
```

**stdin JSON mẫu**:
```json
{
  "session_id": "ses_abc123", "cwd": "/home/user/WASHVN",
  "hook_event_name": "PostToolUse", "tool_name": "Write",
  "tool_input": {"file_path": "/home/user/WASHVN/test.md", "content": "..."},
  "tool_response": {"success": true}, "duration_ms": 150
}
```

#### Code Template

```bash
#!/usr/bin/env bash
INPUT=$(cat); TOOL=$(echo "$INPUT" | jq -r '.tool_name // empty')
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')
[ -z "$FILE_PATH" ] && exit 0
mkdir -p ".skill-context/_state-archive"
LOG=".skill-context/_state-archive/tool-audit-$(date +%Y-%m-%d).log"
TS=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
printf '%s\tWRITE\tpid=%s\tagent=%s\ttool=%s\tpath=%s\n' \
  "$TS" "$$" "${CLAUDE_AGENT_NAME:-parent}" "$TOOL" "$FILE_PATH" >> "$LOG"
exit 0
```

#### Graceful Degradation

| Scenario | Exit | Ghi chú |
|:---------|:----:|:--------|
| jq missing | 0 | Skip log entry |
| stdin malformed | 0 | Skip |
| Log dir missing | 0 | mkdir -p, nếu fail skip |
| Log write fails | 0 | Silent skip |

#### ⚠️ Lưu ý

1. `printf` với `\t` — không dùng `echo`
2. Log path relative — script cần CWD = workspace root
3. `>>` append atomic trên Linux (O_APPEND)
4. Không log `content` — privacy concern

**Evidence**: `roadmap spec line 108-130` — code mẫu; `hooks.md line 685` — PostToolUse không block được.

---

### 3.2 D2-6: `session-start_record_metadata.sh`

#### Mục đích
Ghi boot metadata khi Claude Code khởi động session. Non-blocking — exit 0.

#### Input / Output

```yaml
event: SessionStart | matcher: ".*"
stdin: { session_id, cwd, hook_event_name, source, model }
extract: [".cwd // empty", ".session_id // empty", ".pid // empty", ".boot_id // empty"]
log_file: ".skill-context/_state-archive/session-start.log"
log_format: "TSV 6 columns: timestamp, START, session=ID, pid=N, boot=ID, cwd=PATH"
```

> Official docs không guarantee `pid`/`boot_id` — dùng `// empty` fallback.

#### Code Template

```bash
#!/usr/bin/env bash
INPUT=$(cat)
CWD=$(echo "$INPUT" | jq -r '.cwd // empty')
PID=$(echo "$INPUT" | jq -r '.pid // empty')
BOOT_ID=$(echo "$INPUT" | jq -r '.boot_id // empty')
SESSION_ID=$(echo "$INPUT" | jq -r '.session_id // empty')
mkdir -p ".skill-context/_state-archive"
printf '%s\tSTART\tsession=%s\tpid=%s\tboot=%s\tcwd=%s\n' \
  "$(date -u +'%Y-%m-%dT%H:%M:%SZ')" "$SESSION_ID" "$PID" "$BOOT_ID" "$CWD" \
  >> ".skill-context/_state-archive/session-start.log"
exit 0
```

#### Graceful Degradation: jq missing→0, stdin malformed→0, log write fails→0

**Evidence**: `roadmap spec line 200-225` — code mẫu; `hooks.md line 691` — SessionStart exit 2 không block.

---

### 3.3 D2-5: `stop_session_log_state.sh` (Γ-7 + YAML-RES-1.0)

#### Mục đích
**Hook phức tạp nhất trong Phase 2**. 3 nhiệm vụ: (1) log session stop, (2) Γ-7 corrupt backup, (3) YAML-RES-1.0 L1 Syntax check.

#### Input / Output

```yaml
event: Stop | matcher: ".*"
stdin: { session_id, cwd, hook_event_name, stop_hook_active, last_assistant_message, background_tasks }
extract: ".stop_hook_active // false"
log_file: ".skill-context/_state-archive/session-{YYYY-MM-DD}.log"
log_format: "TSV 3 cols: timestamp, STOP, stop_hook_active=bool"
```

#### 3-Step Logic

```yaml
step_1_log_stop:
  always_run: true
  output: "session-{YYYY-MM-DD}.log — timestamp\\tSTOP\\tstop_hook_active=bool"

step_2_yaml_l1 (YAML-RES-1.0):
  prerequisites: ["_state.yaml exists && -s", "python3 available"]
  command: "python3 -c 'import yaml; yaml.safe_load(open(\".skill-context/_state.yaml\"))'"
  on_corrupt:
    - "cp _state.yaml → _state-archive/_state-{ts}-corrupt.yaml"
    - "log 'STATE CORRUPT: backed up to ...' vào session log (Γ-7: backup TRƯỚC re-init)"
  on_python_missing: "WARNING → skip → exit 0"
  on_state_not_exist/empty: "skip → exit 0"

step_3_degraded_flag:
  status: "DEFERRED — Phase 8. Lý do: corrupt state không thể ghi thêm key."
```

#### Code Template

```bash
#!/usr/bin/env bash
INPUT=$(cat); STOP_ACTIVE=$(echo "$INPUT" | jq -r '.stop_hook_active // false')
mkdir -p ".skill-context/_state-archive"
LOG=".skill-context/_state-archive/session-$(date +%Y-%m-%d).log"
TS=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
printf '%s\tSTOP\tstop_hook_active=%s\n' "$TS" "$STOP_ACTIVE" >> "$LOG"

STATE_FILE=".skill-context/_state.yaml"
if [ -f "$STATE_FILE" ] && [ -s "$STATE_FILE" ] && command -v python3 &>/dev/null; then
  if ! python3 -c "import yaml; yaml.safe_load(open('$STATE_FILE'))" 2>/dev/null; then
    BACKUP=".skill-context/_state-archive/_state-${TS}-corrupt.yaml"
    cp "$STATE_FILE" "$BACKUP" 2>/dev/null \
      && echo "STATE CORRUPT: backed up to $BACKUP" >> "$LOG" \
      || echo "WARNING: backup corrupt _state.yaml failed" >> "$LOG"
  fi
elif ! command -v python3 &>/dev/null && [ -f "$STATE_FILE" ]; then
  echo "WARNING: python3 not available — skip YAML check" >> "$LOG"
fi
exit 0
```

#### Graceful Degradation

| Scenario | Behavior | Exit |
|:---------|:---------|:----:|
| jq missing | Skip log | 0 |
| stdin malformed | Skip all | 0 |
| Log dir missing | mkdir -p, skip | 0 |
| python3 unavailable | WARNING, skip check | 0 |
| pyyaml not installed | Import fail → skip | 0 |
| _state.yaml not exist | Skip | 0 |
| _state.yaml empty | Skip (-s check) | 0 |
| _state.yaml corrupt | Backup + log corrupt event | 0 |
| Backup cp fails | WARNING | 0 |

#### ⚠️ Lưu ý

1. **Python policy**: D2-5 là hook DUY NHẤT Phase 2 dùng Python — vì YAML parsing không feasible với bash thuần
2. **Γ-7 timing**: Backup TRƯỚC khi bất kỳ re-init nào — đây là primary fix cho architectural defect Γ-7
3. **Exit code**: python3 detect corrupt exit 1, nhưng bash script exit 0 (non-blocking)
4. **Không xóa state gốc**: Chỉ backup, không xóa _state.yaml dù corrupt
5. **Stop chain**: D2-5 chạy TRƯỚC D2-9 (Stage 5) trên cùng Stop event

**Evidence**: `roadmap spec line 168-195` — code mẫu; `yaml-resilience-layer.md line 12-17` — L1 Syntax; `suite_config.yaml line 9-12` — pre_reinit_backup; `hooks.md line 678` — Stop event.

---

## §4: Impact Analysis

### Direct Impact

| File | Dòng | Deps | Khó |
|:-----|:----:|:-----|:---:|
| `post-tool-use_log_artifact.sh` | ~15 | jq, bash | Thấp |
| `stop_session_log_state.sh` | ~35 | jq, bash, python3 opt | TB |
| `session-start_record_metadata.sh` | ~20 | jq, bash | Thấp |

### Indirect Impact

- **Read-only**: `suite_config.yaml` (archive path), `_state.yaml` (check target), `_state-archive/` (log dir)
- **Runtime**: tool-audit-{date}.log, session-{date}.log, session-start.log, _state-{ts}-corrupt.yaml (conditional)
- **Downstream**: Stage 3 registry, Stage 4 verification, Stage 5 Stop chain, Phase 8 YAML-RES L2/L3

### Risk Assessment

| Risk | L | I | Mitigation |
|:-----|:-:|:-:|:-----------|
| `>>` race condition tool call song song | Thấp | Thấp | O_APPEND atomic |
| python3 missing → skip YAML check | Thấp | TB | Graceful: WARNING, exit 0 |
| Log file growth | TB | Thấp | Per-day rolling, defer rotation |
| Backup corrupt state fails | Thấp | TB | WARNING, exit 0 |
| Stop event timeout | Thấp | Thấp | D2-5 < 100ms + python < 500ms. Timeout 30s |

---

## §5: Call Chain & Data Flow

### 5.1 Hook Lifecycle

```text
Session Start
  └── SessionStart → D2-6: jq extract → printf TSV >> session-start.log → exit 0

Per-Turn Loop
  ├── PreToolUse (Write|Edit)  ← Stage 1: D2-1 → D2-2 (chain)
  ├── PreToolUse (Bash)        ← Stage 1: D2-4
  └── PostToolUse (Write|Edit) → D2-3: jq extract → printf >> tool-audit-{date}.log → exit 0

Session End
  └── Stop → D2-5:
       ├── Step 1: printf TSV >> session-{date}.log (luôn chạy)
       └── Step 2: if _state.yaml exists + python3 → yaml.safe_load()
            ├── FAIL → cp _state.yaml → _state-{ts}-corrupt.yaml (Γ-7)
            └── PASS/NO_PYTHON/NO_FILE → skip
       └── exit 0
```

### 5.2 Chain Behavior

```yaml
stop: "D2-5 (script) trước → D2-9 (prompt, Stage 5) sau — definition order, cùng Stop event"
post_tool_use: "Chỉ D2-3 — single hook"
session_start: "Chỉ D2-6 — single hook"
note: "Chain chỉ thực sự active khi deploy settings.json (Phase 8). Stage 2 test standalone pipe JSON."
```

### 5.3 Data Flow

```text
[Claude Code]              [.skill-context/_state-archive/]
     |                              |
     | SessionStart                 |
     v                              |
[D2-6] ─── TSV ─────────────────▶ session-start.log
     |                              |
     | PostToolUse (Write|Edit)     |
     v                              |
[D2-3] ─── TSV ─────────────────▶ tool-audit-{date}.log
     |                              |
     | Stop                         |
     v                              |
[D2-5]                             |
     ├── TSV ───────────────────▶ session-{date}.log
     └── [corrupt] cp ─────────▶ _state-{ts}-corrupt.yaml
     exit 0
```

---

## §6: Affected Components

### 6.1 Files Created

```text
.claude/hooks/events/
├── post-tool-use_log_artifact.sh       (D2-3)
├── stop_session_log_state.sh           (D2-5)
└── session-start_record_metadata.sh    (D2-6)
```

### 6.2 Files Modified: None

### 6.3 Files Reference (Read-Only)

`suite_config.yaml` — state_archive path | `_state.yaml` — D2-5 check target | `hooks.md` — stdin schema | `hooks_and_events.md` — protocol | `yaml-resilience-layer.md` — rule_9 | `quality-gates-reference.md` — YAML-RES-1.0

---

## §7: Acceptance Criteria (Stage 2)

| Mã AC | Mô tả | Verification | Dự kiến |
|:-----:|:------|:-------------|:-------:|
| **AC-1-S2** | 3 scripts tồn tại + executable | `test -x .claude/hooks/events/post-tool-use_log_artifact.sh && test -x .claude/hooks/events/stop_session_log_state.sh && test -x .claude/hooks/events/session-start_record_metadata.sh` | ✅ |
| **AC-5-S2** | D2-5 corrupt backup | corrupt _state.yaml → pipe Stop → verify backup created | ✅ |
| **AC-5-S2b** | D2-5 python3 missing → exit 0 | chạy không python3 → exit 0 + warning | ✅ |
| **AC-5-S2c** | D2-5 state not exist → exit 0 | xóa _state.yaml → exit 0 | ✅ |
| **AC-5-S2d** | D2-5 state empty → exit 0 | touch _state.yaml → exit 0 | ✅ |
| **AC-LOG-S2** | D2-3 log đúng TSV | pipe Write JSON → verify 6-column TSV entry | ✅ |
| **AC-LOG-S2b** | D2-6 log đúng TSV | pipe SessionStart JSON → verify 6-column TSV | ✅ |
| **AC-LOG-S2c** | D2-3 jq missing → exit 0 | PATH không jq → exit 0 | ✅ |
| **AC-LOG-S2d** | D2-6 jq missing → exit 0 | PATH không jq → exit 0 | ✅ |
| **AC-LOG-S2e** | D2-5 log đúng format | pipe Stop → verify session-{date}.log | ✅ |
| **AC-11-S2** | stdin malformed → exit 0 (all 3) | pipe `{invalid}` → exit 0 | ✅ |

**Total: 11 AC | 3 scripts | 3 files**

---

## §8: Thứ Tự Build Khuyến Nghị

```text
Step 1: D2-6 (session-start) — Đơn giản nhất, 4 jq extracts + printf
        Verify: pipe SessionStart JSON → exit 0 + session-start.log entry
        Time: ~10 phút

Step 2: D2-3 (log-artifact) — TSV format, độc lập với D2-6
        Verify: pipe PostToolUse JSON (Write) → exit 0 + tool-audit log entry
        Time: ~10 phút

Step 3: D2-5 (stop-state) — Phức tạp nhất, YAML + conditional backup
        Verify: 5 scenarios (valid state, corrupt, missing, no python3, empty)
        Time: ~25 phút
```

**Ghi chú**: D2-6 và D2-3 độc lập — có thể build song song. Cả 3 độc lập với Stage 1.

---

## §9: Environment Variables

| Variable | Hook | Default | Mục đích |
|:---------|:----:|:--------|:---------|
| `CLAUDE_AGENT_NAME` | D2-3 | `parent` | Agent name trong audit log |

---

## §10: Graceful Degradation Matrix (Stage 2 vs Stage 1)

| Hook | Stage | jq missing | stdin malformed | Log dir missing | python3 missing | Env missing |
|:-----|:-----:|:----------:|:---------------:|:---------------:|:---------------:|:-----------:|
| **D2-1** write_gate | S1 | **exit 2** (block) | **exit 2** (block) | N/A | N/A | N/A |
| **D2-2** staging_gate | S1 | **exit 2** (block) | **exit 2** (block) | N/A | N/A | **exit 2** (block) |
| **D2-4** bash_validate | S1 | **exit 2** (block) | **exit 2** (block) | N/A | N/A | **exit 2** (block net) |
| **D2-3** log_artifact | **S2** | **exit 0** (skip) | **exit 0** (skip) | mkdir →0 | N/A | N/A |
| **D2-6** session_start | **S2** | **exit 0** (skip) | **exit 0** (skip) | mkdir →0 | N/A | **exit 0** |
| **D2-5** stop_state | **S2** | **exit 0** (skip) | **exit 0** (skip) | mkdir →0 | **exit 0** (warn) | N/A |

**Nguyên tắc**: Stage 1 fail CLOSED — bảo vệ filesystem. Stage 2 fail OPEN — observability, mất audit log không block workflow. Mất Γ-7 protection (D2-5) có rủi ro nhưng thấp hơn block session stop.

---

## §11: Cấu trúc Log Files (TSV Formats)

### D2-3: `tool-audit-{YYYY-MM-DD}.log`

```
2026-07-08T10:30:00Z	WRITE	pid=12345	agent=parent	tool=Write	path=/home/.../test.md
```

| Col | Field | Source | Example |
|:---:|:------|:-------|:--------|
| 1 | timestamp | `date -u +'%Y-%m-%dT%H:%M:%SZ'` | `2026-07-08T10:30:00Z` |
| 2 | action | Hardcoded "WRITE" | `WRITE` |
| 3 | pid | `$$` shell PID | `pid=12345` |
| 4 | agent | `$CLAUDE_AGENT_NAME` (fallback "parent") | `agent=parent` |
| 5 | tool | `.tool_name` stdin | `tool=Write` |
| 6 | path | `.tool_input.file_path` stdin | `path=/home/...` |

**Generation**: `printf '%s\tWRITE\tpid=%s\tagent=%s\ttool=%s\tpath=%s\n' "$TS" "$$" "$AGENT" "$TOOL" "$PATH" >> "$LOG"`

### D2-6: `session-start.log`

```
2026-07-08T09:00:00Z	START	session=ses_xyz789	pid=12345	boot=boot_abc	cwd=/home/user/WASHVN
```

| Col | Field | Source |
|:---:|:------|:-------|
| 1 | timestamp | `date -u +'%Y-%m-%dT%H:%M:%SZ'` |
| 2 | event | Hardcoded "START" |
| 3 | session | `.session_id` stdin |
| 4 | pid | `.pid` stdin |
| 5 | boot | `.boot_id` stdin |
| 6 | cwd | `.cwd` stdin |

### D2-5: `session-{YYYY-MM-DD}.log`

**Primary entry**: `2026-07-08T18:30:00Z	STOP	stop_hook_active=true`

**Optional messages** (free-text, append cùng file): `STATE CORRUPT: backed up to ...` / `WARNING: python3 not available — skip YAML check`

### D2-5 Conditional: `_state-{timestamp}-corrupt.yaml`

Copy nguyên bản _state.yaml tại thời điểm corrupt. Giữ indefinitely (theo suite_config retention_policy).

---

## §12: YAML-RES-1.0 & Γ-7 Implementation (D2-5 specific)

### 12.1 YAML-RES-1.0 L1 Syntax Check

```yaml
check: "python3 -c 'import yaml; yaml.safe_load(open(\".skill-context/_state.yaml\"))'"
tool: python3 + pyyaml
target: .skill-context/_state.yaml
behaviors:
  valid YAML: "exit 0 — no action"
  corrupt YAML: "exit 1 (python) → bash cp _state.yaml → _state-{ts}-corrupt.yaml"
  empty file: "skip ( -s check trước khi gọi python )"
  JSON file: "exit 0 — JSON là YAML subset, safe_load parse được"
scope_p2: "L1 Syntax ✅ | L2 Schema ✅ (deferred P8) | L3 Cross-ref ✅ (deferred P8)"
```

### 12.2 Γ-7 Fix — Architectural Defect Remediation

```
Defect: Γ-7 — Escalation recursion do corrupt _state.yaml
  Re-init trên corrupt state → corruption cascade → escalation loop

Fix: D2-5 stop hook kiểm tra _state.yaml TRƯỚC khi session kết thúc
     cp _state.yaml → _state-archive/_state-{ts}-corrupt.yaml
     Backup TRƯỚC bất kỳ re-init nào → session mới start với state sạch

Config: suite_config.yaml line 12 — pre_reinit_backup: required
```

### 12.3 Graceful Degradation Chain (D2-5 Decision Tree)

```
D2-5 entry → [jq?] → [mkdir -p] → [Step 1: STOP log]
  → [_state.yaml exists?]
    ├── NO → exit 0
    └── YES → [-s not empty?]
         ├── NO → exit 0
         └── YES → [python3 available?]
              ├── NO → WARNING → exit 0
              └── YES → [import yaml?]
                   ├── FAIL → treat as unavailable → WARNING → exit 0
                   └── PASS → [yaml.safe_load()]
                        ├── PASS → exit 0
                        └── FAIL → [mkdir -p backup dir] → [cp] → exit 0
```

### 12.4 rule_9 Last-Mile Verification

```yaml
source: "yaml-resilience-layer.md line 47"
phase_2: { d2_5: "L1 Syntax — detect + backup corrupt state ✅", d2_9: "Semantic self-healing 🧪 Stage 5" }
gap: "rule_9 yêu cầu HOOK-HEAL-1.0 full. Phase 2 chỉ implement mechanical part (D2-5)."
```

---

## §13: Python Dependency Rationale

### Tại sao D2-5 cần python3?

```yaml
bash_limitations:
  - "Không có YAML parser built-in trong bash"
  - "YAML spec phức tạp: indentation-sensitive, anchors, tags, multi-line strings"
  - "Dùng regex parse YAML dễ false positive (VD: 'key: value' vs 'key: \"value: nested\"')"

python_pyyaml:
  - "Parser chính thức — handle mọi edge cases (yaml.safe_load)"
  - "import yaml available trên hầu hết Python installations"
  - "Exit code: 0=valid, 1=corrupt — signal trực tiếp"

alternatives_rejected:
  - "Ruby: không phổ biến hơn Python"
  - "Node.js js-yaml: cần node_modules — không reliable"
  - "Docker: overkill cho 1 YAML parse"
  - "yamllint: chỉ lint format, không parse semantics"
```

### Graceful Degradation khi python3 missing

```yaml
detection: "command -v python3 &> /dev/null"
behavior: "WARNING vào session log → skip YAML check → exit 0"
impact: "Mất Γ-7 protection cho session đó — session vẫn kết thúc bình thường"
mitigation: "Phase 0 prereq verify python3 + pyyaml; không block workflow (fail OPEN)"
```

---

## §14: Open Questions

| # | Question | Pri | Resolution |
|--:|:---------|:---:|:-----------|
| 1 | D2-5 set `_state.yaml.status = "degraded"` khi corrupt? | TB | Defer. State corrupt → không ghi thêm key được. Phase 8 dùng separate flag file. |
| 2 | Ghi `yaml_repair_history` vào _state.yaml? (rule_7) | TB | Ghi vào session log thay vì _state.yaml (state corrupt thì không append được). |
| 3 | Audit log retention policy? | Thấp | Defer Phase 8. Per-day rolling đã giới hạn size. |
| 4 | D2-3 log content? | Thấp | **KHÔNG** — privacy. Chỉ log path. |
| 5 | SessionStart pid/boot_id không guarantee? | TB | `// empty` fallback an toàn. |
| 6 | PostToolUse exit 2 không block? | Thấp | Confirmed. D2-3 exit 0 đúng. |
| 7 | D2-5 + D2-9 chain behavior? | TB | D2-5 script trước, D2-9 prompt sau. Cần verify khi Stage 5 active. |

---

## §15: Confidence Assessment

```yaml
overall: 86%
  spec: 92% | code_ready: 90% | log_format: 95%
  yaml_resilience: 75% | python_dep: 70%
  graceful: 85% | gamma_7: 80% | fail_open: 95%

flags:
  - "D2-5 pyyaml graceful degradation cần test thực tế với corrupt patterns đa dạng"
  - "SessionStart stdout input fields không 100% guarantee — // empty fallback an toàn"
  - "D2-5 và D2-9 chain không implement trong Stage 2 — cần verify khi Stage 5 active"
```

---

## §16: Tổng Kết

### Scope Summary

```
Stage 2 — Logging & Session Lifecycle Hooks
├── Scripts: 3 (D2-3, D2-5, D2-6)
├── Files created: 3
├── Runtime logs: tool-audit-{date}.log, session-{date}.log, session-start.log
├── Conditional backup: _state-{ts}-corrupt.yaml (Γ-7 fix)
├── Total LOC: ~70
├── Acceptance criteria: 11
├── Risk items: 6 (all mitigated — fail OPEN)
├── Python: D2-5 only (pyyaml optional — graceful degradation)
├── Γ-7 fix: ✅ Backup corrupt _state.yaml before re-init
├── YAML-RES-1.0: L1 Syntax ✅ | L2/L3 deferred Phase 8
├── Confidence: 86%
└── Effort: ~45 phút
```

### Deliverable Status

| Hook | Code Template | Graceful Degradation | Python | Độ khó | Lines |
|:-----|:-------------:|:--------------------:|:------:|:------:|:-----:|
| D2-3 log_artifact | ✅ spec 108-130 | ✅ fail OPEN (3 sc.) | ❌ | Thấp | ~15 |
| D2-6 session_start | ✅ spec 200-225 | ✅ fail OPEN (4 sc.) | ❌ | Thấp | ~20 |
| D2-5 stop_state | ✅ spec 168-195 | ✅ fail OPEN (9 sc.) | ✅ pyyaml | TB | ~35 |

### Key Decisions

1. **Fail OPEN**: Stage 2 không block tool call — khác Stage 1 fail CLOSED
2. **Python CHỈ cho YAML parsing**: D2-5 dùng python3 + pyyaml, không dùng cho logic khác
3. **Γ-7 backup TRƯỚC re-init**: Timing quan trọng — backup ngay khi phát hiện corrupt
4. **degraded flag deferred**: State corrupt không thể ghi — Phase 8 dùng separate mechanism
5. **TSV consistent format**: 3 hooks dùng format TSV chung — dễ parse tool sau này

### Next Steps

1. ✅ Scope document complete
2. ⬜ Implement D2-6 (10 phút)
3. ⬜ Implement D2-3 (10 phút)
4. ⬜ Implement D2-5 (25 phút)
5. ⬜ Verify 11 AC (Stage 2)
6. ⬜ Continue Stage 3 (D2-7 registry + D2-8 tests)

---

**Document**: `docs/context-to-work/roadmap-analysis-phases/Stage-2/scope.2026-07-08.md`
**Version**: 0.2.0 | **Date**: 2026-07-08 | **Status**: Context Complete
**NO CODE CHANGES MADE** — Document only per context-before-fix guardrails.
