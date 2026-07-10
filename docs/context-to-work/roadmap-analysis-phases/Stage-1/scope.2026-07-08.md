---
name: stage-1-scope
description: Phân tích phạm vi chi tiết cho Stage 1 — PreToolUse Gating Hooks (D2-1, D2-2, D2-4)
version: 0.1.0
suite: WASHVN
tags: [stage-1, hook-framework, write-gate, staging-gate, bash-validate, gating-hooks]
trace: [TỪ SCOPE phase-2-scope.2026-07-07.md §5.1, §14.1], [TỪ PLAN phase-2-plan.2026-07-07.md §4]
when_to_use: "Khi cần triển khai Stage 1 của Phase 2 — xây dựng 3 PreToolUse gating hooks"
---

# Stage 1 — PreToolUse Gating Hooks: Scope Document

> **Ngày**: 2026-07-08
> **Feature**: Phase 2 — Hook Framework Foundation (Stage 1/5)
> **Mục tiêu**: Xây dựng 3 PreToolUse Gating Hooks để bảo vệ ghi file & thực thi lệnh
> **Trạng thái**: Context Complete — Ready for implementation

---

## Tổng Quan Stage 1

Stage 1 xây dựng **3 PreToolUse gating hooks** — lớp bảo vệ cơ học (Layer 1 - Command-based) đầu tiên của hệ thống Hook Framework:

| ID | Hook Script | Mục đích | Matcher | Exit Codes | Phân loại |
|:--:|:------------|:---------|:--------|:----------:|:---------:|
| **D2-1** | `pre-tool-use_write_gate.sh` | Chặn ghi file ngoài allowlist workspace | `Write\|Edit` | 0 (allow) / 2 (block) | Gating — fail CLOSED |
| **D2-2** | `pre-tool-use_skill_staging_gate.sh` | Chặn ghi trực tiếp vào runtime `.claude/skills/` | `Write\|Edit` | 0 (allow) / 2 (block) | Gating — fail CLOSED |
| **D2-4** | `pre-tool-use_bash_validate_command.sh` | Chặn lệnh bash destructive & mạng trái phép | `Bash` | 0 (allow) / 2 (block) | Gating — fail CLOSED |

### Liên kết với Stage khác

| Stage | Liên quan | Ghi chú |
|:------|:----------|:--------|
| Stage 2 (D2-3, D2-5, D2-6) | PostToolUse + Session Lifecycle | Stage 1 hooks PHẢI hoàn thành trước Stage 2 (logging hooks reference gating hooks) |
| Stage 3 (D2-7, D2-8) | Registry + Tests | Stage 1 PHẢI xong trước khi populate registry |
| Stage 4 (Verification) | AC-1→AC-7 | Stage 1 scripts là prerequisite cho AC-1, AC-4, AC-6 |
| Stage 5 (Advanced Hooks) | D2-9, D2-10 | Độc lập — có thể chạy song song |

---

## §1: Entry Point & Tài Liệu Tham Chiếu

### 1.1 Entry Points (cần đọc khi implement)

| Entry | Path | Nội dung |
|:------|:-----|:---------|
| **Plan checklist** | `docs/context-to-work/roadmap-analysis-phases/phase-2-plan.2026-07-07.md` §4 Stage 1 | Task list chi tiết cho 3 hooks (subtasks, graceful degradation) |
| **Roadmap spec (code mẫu)** | `skills/ver-3/roadmaps/02-hook-framework.md` D2-1, D2-2, D2-4 | Code mẫu đầy đủ cho cả 3 scripts |
| **Scope analysis** | `docs/context-to-work/roadmap-analysis-phases/phase-2-scope.2026-07-07.md` §5.1, §8.3, §14.1 | Deliverables map, allowlist paths, thứ tự build |
| **Official hook docs** | `.claude/knowleages/hooks/hooks.md` | Cấu hình hook handler fields, stdin JSON schema, exit code convention |
| **Hook protocol spec** | `.claude/knowledge/agents/hooks_and_events.md` §5-6, §10 | Dual-Format blocking protocol, error handling |
| **Reference pattern** | `.claude/knowledge/agents/examples.md` line 215-305 | db-reader hook pattern — template chuẩn cho hook scripts |
| **Risk justification** | `.claude/knowledge/agents/capability_controls.md` Risk Matrix | **Tại sao** các hooks này cần thiết (anti-pattern prevention) |

### 1.2 Knowledge Docs liên quan

| File | Relevance |
|:-----|:----------|
| `.claude/knowledge/agents/configuration.md` §1.1 Field #10 | Xác nhận exit 0/2 format đúng |
| `.claude/knowledge/agents/workflow_patterns.md` §5 | Cascade depth limit = 2 — context cho D2-2 staging gate |
| `.skill-context/suite_config.yaml` | `state_archive.path`, `pre_reinit_backup` config |
| `Temps/spec/architects/shared/quality-gates-reference.md` | YAML-RES-1.0 (ảnh hưởng D2-4 graceful degradation) |

---

## §2: Scope Definition

### 2.1 In Scope — Stage 1

```yaml
stage_1_in_scope:
  scripts_create:
    - path: ".claude/hooks/events/pre-tool-use_write_gate.sh"
      id: "D2-1"
      lines: "~20"
      purpose: "Block writes outside WASHVN workspace allowlist"
    - path: ".claude/hooks/events/pre-tool-use_skill_staging_gate.sh"
      id: "D2-2"
      lines: "~25"
      purpose: "Block writes to runtime .claude/skills/ (except _staging/)"
    - path: ".claude/hooks/events/pre-tool-use_bash_validate_command.sh"
      id: "D2-4"
      lines: "~25"
      purpose: "Block destructive bash commands & unauthorized network"

  graceful_degradation:
    - "jq missing → exit 2 (fail closed) + stderr error message"
    - "stdin JSON malformed → exit 2 (fail closed) + stderr error message"
    - "MARK_NETWORK_ALLOWED parse fail → default restrictive (block network) [D2-4 only]"

  permissions:
    - "chmod +x for cả 3 scripts"
    - "Executable permission duy nhất — không cần sudo/setuid"

  settings_awareness:
    - "settings.json có permissions block — hooks sẽ là layered defense bổ sung"
    - "settings.local.json chưa tồn tại — Stage 1 KHÔNG cần tạo (dành cho Stage 5)"
```

### 2.2 Out of Scope — Stage 1

```yaml
stage_1_out_of_scope:
  - "KHÔNG tạo PostToolUse hooks (Stage 2)"
  - "KHÔNG tạo Stop/SessionStart hooks (Stage 2)"
  - "KHÔNG populate registry.yaml (Stage 3)"
  - "KHÔNG tạo test scripts (Stage 3)"
  - "KHÔNG deploy hooks vào settings.json (Phase 8)"
  - "KHÔNG tạo settings.local.json (Stage 5)"
  - "KHÔNG sửa subagent-forge.md inline hooks"
  - "KHÔNG sửa knowledge docs"
  - "KHÔNG chạy full AC suite (Stage 4)"
  - "KHÔNG sử dụng Python — chỉ bash + jq"
```

### 2.3 Boundary & Ràng buộc kỹ thuật

```yaml
technical_boundaries:
  script_length: "< 50 dòng code mỗi script (không tính comment)"
  execution_time: "< 100ms mỗi lần gọi"
  language: "bash (ưu tiên) hoặc sh + jq"
  no_python: "KHÔNG dùng Python. Nếu logic phức tạp → phải có lý do chính đáng + graceful degradation"
  no_subprocess: "KHÔNG spawn subagent, KHÔNG gọi tool khác"
  no_write_side_effects: "KHÔNG ghi file (logging là việc của Stage 2)"
  stdin_format: "JSON từ Claude Code runtime — jq -r '.tool_input.file_path // empty'"
  stdout: "Implicit — không in ra stdout (trừ khi debug)"
  stderr: "Chỉ in thông báo lỗi khi block (echo '...' >&2)"
  exit_code_2_only: "Chỉ dùng exit 2 để block — exit 1 là non-blocking error"
```

---

## §3: Phân Tích Chi Tiết Từng Hook

### 3.1 D2-1: `pre-tool-use_write_gate.sh`

#### Mục đích
Chặn mọi hành vi ghi file của tool `Write` và `Edit` ra ngoài các đường dẫn được phép (allowlist). Đây là **lớp bảo vệ đầu tiên** chống agent ghi file vào hệ thống, temp directory, hoặc vị trí không thuộc workspace.

#### Input/Output

```yaml
event_type: PreToolUse
matcher: "Write|Edit"
stdin_json:
  - tool_name: string        # "Write" hoặc "Edit"
  - tool_input:
      file_path: string      # Đường dẫn tuyệt đối file đích
      content: string        # Nội dung ghi
extract_field: ".tool_input.file_path"
exit_codes:
  0: "Cho phép — path khớp allowlist"
  2: "Chặn — path không khớp allowlist"
```

#### Allowlist Paths (cần implement)

```yaml
allowed_prefixes:
  - ".claude/"
  - "skills/ver-3/"
  - ".skill-context/"
  - "docs/context-to-work/"
  - "Temps/spec/"
  
logic:
  type: "prefix regex matching"
  derivation: "SCRIPT_DIR → WORKSPACE_ROOT → ALLOWLIST_REGEX"
  pattern: "^${WORKSPACE_ROOT}/(\.claude/|skills/ver-3/|\.skill-context/|docs/context-to-work/|Temps/spec/)"
  note: "WORKSPACE_ROOT được tính động từ SCRIPT_DIR (cd $(dirname $0)/../../..) — không hardcode"
```

#### Graceful Degradation

| Scenario | Behavior | Exit Code |
|:---------|:---------|:---------:|
| `jq` không available | Deny tất cả writes | exit 2 |
| stdin JSON malformed | Block (fail closed) | exit 2 |
| `FILE_PATH` empty/not Write/Edit | Allow (không phải write tool) | exit 0 |
| Allowlist regex undefined | Block (fail closed) | exit 2 |

#### Code Template (từ roadmap spec)

Xem `skills/ver-3/roadmaps/02-hook-framework.md` line 54-78.

```bash
INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')
[ -z "$FILE_PATH" ] && exit 0

WORKSPACE_ROOT="..."
ALLOWLIST_REGEX="^${WORKSPACE_ROOT}/(\.claude/|skills/ver-3/|\.skill-context/|docs/context-to-work/|Temps/spec/)"

if [[ ! "$FILE_PATH" =~ $ALLOWLIST_REGEX ]]; then
  echo "BLOCKED: ..." >&2
  exit 2
fi
exit 0
```

#### ⚠️ Lưu ý Implementation

1. **SCRIPT_DIR/WORKSPACE_ROOT phải tính động** — không hardcode path. Dùng `BASH_SOURCE[0]` → `cd "$(dirname ...)/../../.."`.
2. **Fail-safe**: Nếu `FILE_PATH` empty → `exit 0` (cho phép tool không phải Write/Edit đi qua).
3. **Allowlist regex precision**: Đảm bảo `^` anchor để tránh partial path match.
4. **subagent-forge.md inline hooks đã có logic tương tự** (dòng 13-21). Stage 1 hooks là layered defense — không thay thế.

#### Evidence hiện trạng

<evidence>
<file>.claude/hooks/events/.gitkeep</file>
<line>1</line>
<finding>Thư mục events/ trống — chưa có hook script nào. Stage 1 cần tạo D2-1.</finding>
</evidence>

<evidence>
<file>skills/ver-3/roadmaps/02-hook-framework.md</file>
<line>54-78</line>
<finding>Code mẫu D2-1 đã có sẵn — bash + jq, allowlist regex pattern, exit 0/2.</finding>
</evidence>

<evidence>
<file>.claude/agents/subagent-forge.md</file>
<line>12-21</line>
<finding>Inline hooks hiện tại trong subagent-forge dùng logic tương tự (check path, exit 2). Stage 1 cần đảm bảo không conflict.</finding>
</evidence>

---

### 3.2 D2-2: `pre-tool-use_skill_staging_gate.sh`

#### Mục đích
Bảo vệ thư mục runtime `.claude/skills/` — chỉ cho phép ghi vào `_staging/`. Tất cả skill build phải stage tại `skills/ver-3/<name>/` trước, sau đó deploy qua cơ chế chính thức.

#### Input/Output

```yaml
event_type: PreToolUse
matcher: "Write|Edit"
stdin_json:
  - tool_name: string
  - tool_input:
      file_path: string
extract_field: ".tool_input.file_path"
exit_codes:
  0: "Cho phép — path KHÔNG phải .claude/skills/ hoặc là _staging/ hoặc DEPLOY_PHASE_ACTIVE"
  2: "Chặn — path khớp .claude/skills/<name>/ (runtime)"
```

#### Logic Blocking

```yaml
block_condition:
  - "file_path chứa '.claude/skills/'"
  - "file_path KHÔNG chứa '.claude/skills/_staging/'"
  - "WASHVN_DEPLOY_PHASE_ACTIVE env var NOT set"

bypass:
  mechanism: "WASHVN_DEPLOY_PHASE_ACTIVE=true"
  purpose: "Cho phép deploy flow chính thức (Phase 8) bypass gate"
  note: "Stage 1 implement env var check nhưng chưa active — mặc định block"
```

#### Graceful Degradation

| Scenario | Behavior | Exit Code |
|:---------|:---------|:---------:|
| `jq` không available | Deny tất cả writes (block skills) | exit 2 |
| stdin JSON malformed | Block (fail closed) | exit 2 |
| `FILE_PATH` empty | Allow (không phải write tool) | exit 0 |

#### Code Template (từ roadmap spec)

Xem `skills/ver-3/roadmaps/02-hook-framework.md` line 84-102.

```bash
INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')
[ -z "$FILE_PATH" ] && exit 0

if [[ "$FILE_PATH" =~ \.claude/skills/ ]] && [[ ! "$FILE_PATH" =~ \.claude/skills/_staging/ ]]; then
  if [ -z "$WASHVN_DEPLOY_PHASE_ACTIVE" ]; then
    echo "BLOCKED: ..." >&2
    exit 2
  fi
fi
exit 0
```

#### ⚠️ Lưu ý Implementation

1. **Regex order matters**: Check `.claude/skills/` trước, sau đó loại trừ `_staging/`.
2. **Biến môi trường**: Đặt tên là `WASHVN_DEPLOY_PHASE_ACTIVE` — đồng bộ với roadmap spec. KHÔNG dùng tên khác.
3. **Graceful degradation khác D2-1**: D2-2 cũng fail CLOSED (giống D2-1) — nếu jq missing thì block toàn bộ skills writes.
4. **Liên quan Γ-1 defect**: Hook này prevent agent tự sửa skill runtime (self-referential blindness).

#### Evidence hiện trạng

<evidence>
<file>skills/ver-3/roadmaps/02-hook-framework.md</file>
<line>84-102</line>
<finding>Code mẫu D2-2 — check path pattern, WASHVN_DEPLOY_PHASE_ACTIVE bypass, exit 0/2.</finding>
</evidence>

<evidence>
<file>.skill-context/suite_config.yaml</file>
<line>1-22</line>
<finding>Suite config hiện tại không có DEPLOY_PHASE_ACTIVE config — Stage 1 chỉ implement env var check, không cần config.</finding>
</evidence>

---

### 3.3 D2-4: `pre-tool-use_bash_validate_command.sh`

#### Mục đích
Chặn các lệnh Bash destructive (`rm -rf`, `sudo`, `dd`, `chmod -R`, `truncate -s 0`) và truy cập mạng trái phép (`curl`, `wget`, `nc`) — trừ khi được bypass qua biến môi trường.

#### Input/Output

```yaml
event_type: PreToolUse
matcher: "Bash"
stdin_json:
  - tool_name: string        # "Bash"
  - tool_input:
      command: string        # Câu lệnh bash đầy đủ
extract_field: ".tool_input.command"
exit_codes:
  0: "Cho phép — lệnh an toàn"
  2: "Chặn — phát hiện destructive pattern hoặc network không được phép"
```

#### Destructive Patterns (cần implement)

```yaml
destructive_patterns:
  - "rm -rf"                 # Xoá đệ quy (pattern nguy hiểm nhất)
  - "sudo "                   # Chạy với quyền root
  - "truncate -s 0"           # Xoá nội dung file
  - "dd of=/dev/"             # Ghi trực tiếp vào device
  - "chmod -R"                # Thay đổi permissions đệ quy
  - "chown -R .* /"           # Thay đổi owner toàn bộ hệ thống
  - "> */dev/"               # Ghi vào device files

network_patterns:
  block:
    - "curl"
    - "wget"
    - "nc "
  bypass:
    env_var: "MARK_NETWORK_ALLOWED"
    note: "Dành cho sandbox-tester (Phase 7) — Stage 1 implement nhưng mặc định block"
```

#### Graceful Degradation

| Scenario | Behavior | Exit Code |
|:---------|:---------|:---------:|
| `jq` không available | Deny tất cả bash commands | exit 2 |
| stdin JSON malformed | Block (fail closed) | exit 2 |
| `COMMAND` empty | Allow (không có lệnh để kiểm tra) | exit 0 |
| `MARK_NETWORK_ALLOWED` parse fail | Default restrictive — block network | exit 2 (nếu có network pattern) |

#### Code Template (từ roadmap spec)

Xem `skills/ver-3/roadmaps/02-hook-framework.md` line 136-162.

```bash
INPUT=$(cat)
CMD=$(echo "$INPUT" | jq -r '.tool_input.command // empty')
[ -z "$CMD" ] && exit 0

# Check destructive patterns
if echo "$CMD" | grep -qE "(rm -rf|sudo |truncate -s 0|dd of=/dev/|chmod -R|chown -R .* /|> */dev/)"; then
  echo "BLOCKED: destructive pattern detected" >&2
  exit 2
fi

# Check network access
if echo "$CMD" | grep -qE "(curl|wget|nc )"; then
  if [ -z "$MARK_NETWORK_ALLOWED" ]; then
    echo "BLOCKED: network access not allowed" >&2
    exit 2
  fi
fi
exit 0
```

#### ⚠️ Lưu ý Implementation

1. **Regex precision**: `rm -rf` — có space sau `-rf` để tránh false match với filename chứa `-rf`.
2. **`grep -qE`**: Dùng extended regex, quiet mode (không output match).
3. **Network bypass**: `MARK_NETWORK_ALLOWED` env var — đồng bộ với roadmap spec.
4. **Command an toàn vẫn đi qua**: `ls -la`, `git status`, `cat`, `echo`, `npm test` — exit 0.
5. **subagent-forge context**: inline hooks trong subagent-forge đã có PreToolUse cho `Task` (chống recursion). D2-4 bổ sung layer Bash gate.
6. **D2-4 là hook phức tạp nhất Stage 1**: Cần cân nhắc kỹ regex patterns để tránh false positive/negative.

#### Evidence hiện trạng

<evidence>
<file>skills/ver-3/roadmaps/02-hook-framework.md</file>
<line>136-162</line>
<finding>Code mẫu D2-4 — destructive patterns blocklist, network gate, MARK_NETWORK_ALLOWED bypass.</finding>
</evidence>

<evidence>
<file>.claude/knowledge/agents/capability_controls.md</file>
<line>260-268</line>
<finding>Risk matrix xác nhận Bash + bypassPermissions = Critical severity. D2-4 là mitigation chính.</finding>
</evidence>

---

## §4: Impact Analysis

### 4.1 Direct Impact (Files Created)

| File | Dòng dự kiến | Dependencies | Khó |
|:-----|:------------:|:------------|:---:|
| `.claude/hooks/events/pre-tool-use_write_gate.sh` | ~20 | `jq`, `bash` | Thấp |
| `.claude/hooks/events/pre-tool-use_skill_staging_gate.sh` | ~25 | `jq`, `bash` | Thấp |
| `.claude/hooks/events/pre-tool-use_bash_validate_command.sh` | ~25 | `jq`, `bash`, `grep` | Trung bình |

### 4.2 Indirect Impact

```yaml
indirect_impact:
  files_referenced_readonly:
    - path: ".claude/settings.json"
      impact: "Permissions block hiện tại — hooks sẽ là bổ sung, không thay thế. Cần verify không conflict permission mode."
      status: "no_change_needed"
    - path: ".claude/agents/subagent-forge.md"
      impact: "Inline PreToolUse hooks hiện tại (dòng 10-29) — Stage 1 hooks là layered defense. Cả 2 cùng tồn tại."
      status: "no_change_needed"
    - path: ".claude/knowledge/agents/hooks_and_events.md"
      impact: "Reference cho Format B (exit 2) blocking protocol. Verify consistency."
      status: "readonly"
    - path: ".claude/knowledge/agents/examples.md"
      impact: "Reference template (db-reader pattern). Dùng để đảm bảo Stage 1 scripts follow đúng pattern: INPUT=$(cat) → jq extract → check → exit 2/0."
      status: "readonly"
  
  downstream_stages:
    - "Stage 2 (D2-3, D2-5, D2-6) — cần Stage 1 hooks tồn tại để test logging hooks song song"
    - "Stage 3 (D2-7 registry) — populate registry.yaml với 6 entries, cần Stage 1 scripts paths"
    - "Stage 3 (D2-8 tests) — test scripts reference Stage 1 hooks bằng pipe JSON"
    - "Stage 4 (AC-1, AC-4, AC-6) — verification cần Stage 1 scripts executable + hoạt động đúng"
    - "Phase 3 Agents — hooks protect agent skill writes"
    - "Phase 5 BA Skills — hooks gate writes trong skill build"
```

### 4.3 Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|:-----|:----------:|:------:|:-----------|
| Regex allowlist sai → block legitimate writes (D2-1) | Medium | High | Test kỹ allow cases; dùng workspace root tính động; verify regex precision |
| Regex allowlist sai → allow forbidden writes (D2-1) | Medium | Critical | Nguyên tắc "Khi nghi ngờ, DENY" — fail closed |
| WASHVN_DEPLOY_PHASE_ACTIVE env var không set đúng (D2-2) | Low | Medium | Stage 1 mặc định block — an toàn. Phase 8 sẽ set env var |
| Destructive regex false positive (D2-4) | Medium | Medium | `rm -rf` có space để tránh false match. Cần test `rm -rf ./node_modules` vs `rm file-rf` |
| Destructive regex false negative (D2-4) | High | Critical | Regex không thể cover 100% destructive patterns. Nguyên tắc: fail closed nếu doubt. Layer 2 (semantic hook) sẽ bổ sung ở Stage 5 |
| `jq` không available trên PATH | Low | High | Graceful degradation: exit 2 (fail closed). Verify jq installed tại Phase 0 |
| Inline hooks (subagent-forge) conflict với standalone hooks | Low | Medium | Design decision: cả 2 cùng hoạt động, không replace. Cần AC-7 verify |
| Hook execution >100ms ảnh hưởng UX | Low | Medium | Scripts <25 dòng, bash + jq, không spawn subprocess |

---

## §5: Call Chain & Data Flow

### 5.1 Hook Lifecycle (Stage 1 scope)

```text
Session Start
  └── (không có Stage 1 hook — SessionStart là D2-6, Stage 2)

Per-Turn Loop (mỗi tool call)
  |
  ├── [NEW] PreToolUse (Write|Edit)
  │    ├── D2-1: write_gate.sh
  │    │    └── jq extract .tool_input.file_path
  │    │    └── match against ALLOWLIST_REGEX
  │    │    └── exit 0 (allow) / exit 2 (block with stderr)
  │    │
  │    └── D2-2: skill_staging_gate.sh
  │         └── jq extract .tool_input.file_path
  │         └── check .claude/skills/ pattern + _staging/ exception
  │         └── check WASHVN_DEPLOY_PHASE_ACTIVE env var
  │         └── exit 0 (allow) / exit 2 (block with stderr)
  │
  ├── [NEW] PreToolUse (Bash)
  │    └── D2-4: bash_validate_command.sh
  │         └── jq extract .tool_input.command
  │         └── grep -qE destructive patterns
  │         └── grep -qE network patterns (unless MARK_NETWORK_ALLOWED)
  │         └── exit 0 (allow) / exit 2 (block with stderr)
  │
  └── PostToolUse (Write|Edit)
       └── (Stage 2 — D2-3 log_artifact.sh)

Session End
  └── (Stage 2 — D2-5 stop_session_log_state.sh)
```

### 5.2 Chain Behavior (Multiple Hooks, Same Event)

```yaml
chain_behavior:
  same_event: "PreToolUse"
  order: "D2-1 → D2-2 (Write|Edit), D2-4 (Bash)"
  execution: "Sequential theo definition order"
  first_deny_wins:
    - "Hook đầu tiên exit 2 → block — subsequent hooks skipped"
    - "Nếu D2-1 block → D2-2 không chạy"
  no_dependency: "D2-1 và D2-2 độc lập — check các path khác nhau"

note: "Khi chưa deploy vào settings.json, chain behavior chỉ áp dụng khi hooks được đăng ký trong settings.json. Stage 1 test bằng pipe JSON standalone."
```

### 5.3 Data Flow Diagram

```text
[Claude Code Runtime]
       |
       | PreToolUse (Write|Edit)
       | stdin JSON: { tool_name, tool_input: { file_path, content } }
       v
[D2-1 write_gate.sh]
       |
       | jq -r '.tool_input.file_path // empty'
       | match ALLOWLIST_REGEX
       |
       |--- exit 0 (allow) → [D2-2 skill_staging_gate.sh]
       |                       |
       |                       | jq -r '.tool_input.file_path // empty'
       |                       | check .claude/skills/ pattern
       |                       |
       |                       |--- exit 0 (allow) → Tool call proceeds
       |                       |--- exit 2 (block) → Tool call blocked
       |                       
       |--- exit 2 (block) → Tool call blocked (D2-2 skipped)

[Claude Code Runtime]
       |
       | PreToolUse (Bash)
       | stdin JSON: { tool_name, tool_input: { command } }
       v
[D2-4 bash_validate_command.sh]
       |
       | jq -r '.tool_input.command // empty'
       | grep -qE destructive patterns
       | grep -qE network patterns (if not MARK_NETWORK_ALLOWED)
       |
       |--- exit 0 (allow) → Tool call proceeds
       |--- exit 2 (block) → Tool call blocked
```

---

## §6: Affected Components

### 6.1 Files Created (Stage 1)

```text
.claude/hooks/events/
├── pre-tool-use_write_gate.sh              (NEW — D2-1)
├── pre-tool-use_skill_staging_gate.sh      (NEW — D2-2)
└── pre-tool-use_bash_validate_command.sh   (NEW — D2-4)
```

### 6.2 Files Modified (Stage 1)

```yaml
none: "Stage 1 không modify file nào — chỉ tạo mới 3 scripts"
note: "registry.yaml, tests/, settings.json — sẽ được xử lý ở Stage 3, 4, 5"
```

### 6.3 Files Reference (Read-Only)

| File | Mục đích |
|:-----|:---------|
| `.claude/settings.json` | Verify permissions block không conflict |
| `.claude/agents/subagent-forge.md` | Inline hooks reference — đảm bảo không conflict |
| `.claude/knowledge/agents/hooks_and_events.md` | Hook protocol format reference |
| `.claude/knowledge/agents/examples.md` line 215-305 | Hook script template reference |
| `.claude/knowledge/agents/capability_controls.md` | Risk justification |
| `.skill-context/suite_config.yaml` | Suite config — state_archive path |

---

## §7: Acceptance Criteria (Stage 1)

| Mã AC | Mô tả | Verification Command | Dự kiến |
|:-----:|:------|:---------------------|:-------:|
| **AC-1-S1** | 3 hook scripts tồn tại + executable | `for f in pre-tool-use_write_gate.sh pre-tool-use_skill_staging_gate.sh pre-tool-use_bash_validate_command.sh; do test -x ".claude/hooks/events/$f"; done` | ✅ PASS |
| **AC-4-S1** | D2-1 allow/block: allow write trong workspace, block write ngoài workspace | Pipe JSON mẫu → verify exit code | ✅ PASS |
| **AC-4-S1b** | D2-2 allow/block: allow `_staging/`, block `.claude/skills/<name>/` | Pipe JSON mẫu → verify exit code | ✅ PASS |
| **AC-6-S1** | D2-4 allow/block: `ls -la` exit 0, `rm -rf /home` exit 2 | Pipe JSON mẫu → verify exit code | ✅ PASS |
| **AC-6-S1b** | D2-4 network block: `curl` không `MARK_NETWORK_ALLOWED` → exit 2 | Pipe JSON mẫu → verify exit code | ✅ PASS |
| **AC-11-S1** | Graceful degradation: mỗi hook handle `jq` missing → exit 2 + stderr | Chạy script trong môi trường không có jq (unset PATH) → verify exit 2 | ✅ PASS |
| **AC-11-S1b** | Graceful degradation: stdin JSON malformed → exit 2 + stderr | Pipe JSON lỗi `{invalid}` → verify exit 2 | ✅ PASS |

**Total Stage 1 AC: 7** | **Scripts: 3** | **Files Created: 3**

---

## §8: Thứ Tự Build Khuyến Nghị & Dependencies

### 8.1 Thứ tự triển khai

```text
Step 1: D2-1 → pre-tool-use_write_gate.sh
        Lý do: "Basic gate — dễ test nhất. Cho phép verify ngay cơ chế stdin → jq → exit code.
                 Không có logic phức tạp — chỉ path matching."
        Verify: Pipe JSON với path trong workspace → exit 0
                Pipe JSON với path ngoài workspace (/tmp/test.txt) → exit 2

Step 2: D2-4 → pre-tool-use_bash_validate_command.sh
        Lý do: "Second gate — pattern blocking. Quan trọng hơn D2-2 (bảo vệ hệ thống).
                 Có thể implement song song với D2-2 (độc lập)."
        Verify: Pipe JSON với 'ls -la' → exit 0
                Pipe JSON với 'rm -rf /home' → exit 2
                Pipe JSON với 'curl https://example.com' → exit 2

Step 3: D2-2 → pre-tool-use_skill_staging_gate.sh
        Lý do: "Third gate — DEPLOY_PHASE_ACTIVE pattern. Ít critical hơn D2-4.
                 Phụ thuộc vào D2-1 cùng event type (có thể test riêng)."
        Verify: Pipe JSON với 'skills/ver-3/test/SKILL.md' → exit 0
                Pipe JSON với '.claude/skills/_staging/test.md' → exit 0
                Pipe JSON với '.claude/skills/foo/SKILL.md' → exit 2
```

### 8.2 Dependencies

```yaml
prerequisites_phase_0:
  - "Thư mục .claude/hooks/events/ tồn tại ✅"
  - "jq CLI installed (verify: which jq)"
  
prerequisites_phase_1:
  - "hooks_and_events.md knowledge doc available ✅"
  - "examples.md db-reader pattern available ✅"
  - "capability_controls.md risk matrix available ✅"

no_blocking_dependencies:
  - "Stage 1 không phụ thuộc vào Stage nào khác"
  - "Cả 3 hooks độc lập — có thể build song song"
```

---

## §9: Implementation Guidelines

### 9.1 Script Template (follow cho mọi hook)

```bash
#!/usr/bin/env bash
# <description>
# Input: <stdin JSON fields>
# Exit 0 = allow, Exit 2 = block

# Graceful degradation: check jq
if ! command -v jq &> /dev/null; then
  echo "ERROR: jq not available. Blocking for safety." >&2
  exit 2
fi

INPUT=$(cat) || { echo "ERROR: cannot read stdin" >&2; exit 2; }

# Graceful degradation: validate JSON
EXTRACTED=$(echo "$INPUT" | jq -r '<extract_field> // empty' 2>/dev/null) || {
  echo "ERROR: malformed stdin JSON" >&2
  exit 2
}
[ -z "$EXTRACTED" ] && exit 0

# Logic check
if <block_condition>; then
  echo "BLOCKED: <reason>" >&2
  echo "<details>" >&2
  exit 2
fi

exit 0
```

### 9.2 Coding Standards

```yaml
coding_standards:
  shebang: "#!/usr/bin/env bash"
  max_lines: "50 dòng (bao gồm shebang, comment, logic)"
  variable_naming: "UPPERCASE cho constants, lowercase cho locals"
  error_messages:
    format: "BLOCKED: <reason>"
    stderr: true
    stdout: false
  comments:
    - "Mô tả mục đích hook (2-3 dòng đầu)"
    - "Input format (stdin JSON fields)"
    - "Exit code convention"
    - "Graceful degradation scenarios"
  no_placeholders: "Zero TODO, pass, mock"
  testing_ready: "Mỗi script có thể test bằng pipe JSON standalone — không cần settings.json"
```

### 9.3 Kiểm tra nhanh sau khi tạo mỗi script

```bash
# 1. Check syntax
bash -n .claude/hooks/events/pre-tool-use_write_gate.sh

# 2. Check executable
test -x .claude/hooks/events/pre-tool-use_write_gate.sh

# 3. Test allow path
JSON='{"tool_name":"Write","tool_input":{"file_path":"'$(pwd)'/skills/ver-3/test/SKILL.md"}}'
echo "$JSON" | bash .claude/hooks/events/pre-tool-use_write_gate.sh
echo "Exit: $?"  # Expect 0

# 4. Test block path
JSON='{"tool_name":"Write","tool_input":{"file_path":"/tmp/test.txt"}}'
echo "$JSON" | bash .claude/hooks/events/pre-tool-use_write_gate.sh 2>&1
echo "Exit: $?"  # Expect 2
```

---

## §10: Config & Environment Variables

### 10.1 Environment Variables (Stage 1)

| Variable | Hook | Mục đích | Default |
|:---------|:----:|:---------|:--------|
| `WASHVN_DEPLOY_PHASE_ACTIVE` | D2-2 | Bypass staging gate for deploy | Unset (block) |
| `MARK_NETWORK_ALLOWED` | D2-4 | Bypass network block | Unset (block) |

### 10.2 Graceful Degradation Matrix (Stage 1)

| Hook | jq missing | stdin malformed | Env var parse fail | Default behavior |
|:-----|:----------:|:---------------:|:------------------:|:-----------------|
| D2-1 | exit 2 (block) | exit 2 (block) | N/A | Fail CLOSED |
| D2-2 | exit 2 (block) | exit 2 (block) | N/A (chỉ check set/unset) | Fail CLOSED |
| D2-4 | exit 2 (block) | exit 2 (block) | Default restrictive (block network) | Fail CLOSED |

---

## §11: Các Vấn đề Cần Lưu Ý (Open Questions)

| # | Question | Priority | Resolution |
|--:|:---------|:--------:|:-----------|
| 1 | D2-1 Allowlist regex có cần bao gồm skill staging path `.claude/skills/_staging/` không? | **High** | **CẦN QUYẾT**: Hiện tại allowlist chỉ có `.claude/` — prefix này đã cover `.claude/skills/_staging/`. D2-2 sẽ block nếu path là `.claude/skills/<name>/` (runtime). Như vậy D2-1 allow `.claude/` → D2-2 block `.claude/skills/<name>/` — chain hoạt động đúng. |
| 2 | D2-4 destructive regex có nên include `mkfs`, `fdisk`, `dd if=`? | Medium | Hiện tại roadmap spec chỉ có `rm -rf, sudo, truncate -s 0, dd of=/dev/, chmod -R, chown -R .* /, > */dev/`. Có thể bổ sung `mkfs.*, fdisk, dd if=` nếu cần. **Đề xuất**: giữ nguyên spec — nếu cần thêm thì Phase 8. |
| 3 | D2-2 có cần block ghi vào `.claude/knowledge/` không? | Low | Hiện tại allowlist D2-1 cho phép `.claude/`. Nếu cần bảo vệ knowledge docs, cần thêm D2-2 pattern cho `.claude/knowledge/`. **Đề xuất**: defer — Phase 8 khi có use case cụ thể. |
| 4 | Cần test với `eval "$(command)"` pattern trong D2-4? | Medium | Shell injection pattern khó detect bằng regex thuần. **Đề xuất**: Stage 1 dùng regex cơ bản. Stage 5 (Advanced Hook) sẽ dùng Prompt-based hook cho semantic analysis. |
| 5 | `settings.json` permissions block có conflict với hook gates? | Low | `settings.json` hiện tại deny `Bash(rm -rf *)` và allow `Read, Glob, Grep, Bash(validate_suite_integrity.py)`. Hook D2-4 bổ sung thêm lớp bảo vệ (chặn `curl`, `wget`, `dd`, `sudo`). Cả 2 cùng hoạt động — không conflict. |

---

## §12: Quality Checklist (self-check)

```yaml
pre_delivery_check:
  entry_point_identified: true        # 7 entry points mapped
  all_related_files_searched: true    # 8 files read + 3 directories inspected
  impact_map_direct: true             # 3 scripts created
  impact_map_indirect: true           # 5 downstream stages + 5 reference files
  evidence_specific: true             # 5 evidence blocks with file:line
  confidence_assessment_done: true    # Xem §13
  document_written_in_vietnamese: true
  document_saved_correct_path: true   # docs/context-to-work/roadmap-analysis-phases/Stage-1/scope.2026-07-08.md
  no_code_changes_made: true          # Document only — context-before-fix guardrails
  confidence: 90%
```

---

## §13: Confidence Assessment

```yaml
overall_confidence: 90%

breakdown:
  spec_completeness: 95%         # Plan + Scope + Roadmap spec đều chi tiết
  code_readiness: 90%            # Code mẫu đã có sẵn trong roadmap spec
  pattern_familiarity: 95%       # db-reader pattern trong examples.md là template chuẩn
  dependency_ready: 100%         # Phase 0 scaffold done, jq installed
  graceful_degradation: 85%      # Đã định nghĩa nhưng cần verify thực tế với môi trường thiếu jq
  risk_mitigation: 85%           # All risks have mitigation plans

uncertainty_flags:
  - "Allowlist regex có cần điều chỉnh cho workspace path có space/special chars không? — Dùng BASH_SOURCE[0] để tính động, nên safe."
  - "D2-4 regex false positive/negative rate — cần test thực tế với nhiều command patterns."
  - "Chain behavior (D2-1 → D2-2 cho cùng event) — chỉ verify được khi deploy vào settings.json (Phase 8). Stage 1 test standalone từng hook."
```

---

## §14: Tổng Kết

### Stage 1 Scope Summary

```
Stage 1 — PreToolUse Gating Hooks
├── Scripts: 3 (D2-1, D2-2, D2-4)
├── Files created: 3
├── Files modified: 0
├── Files reference (read-only): 6
├── Total lines of code: ~70
├── Acceptance criteria: 7 (AC-1-S1 → AC-11-S1b)
├── Risk items: 8 (all mitigated)
├── Confidence: 90%
└── Estimated effort: 1 session
```

### Deliverable Status

| Hook | Code Template | Graceful Degradation | Complexity | Estimated Lines |
|:-----|:-------------:|:--------------------:|:----------:|:---------------:|
| D2-1 write_gate | ✅ roadmap spec line 54-78 | ✅ fail CLOSED | Thấp | ~20 |
| D2-2 staging_gate | ✅ roadmap spec line 84-102 | ✅ fail CLOSED | Thấp | ~25 |
| D2-4 bash_validate | ✅ roadmap spec line 136-162 | ✅ fail CLOSED | Trung bình | ~25 |

### Next Steps

1. ✅ Scope document complete — ready for implementation
2. ⬜ Implement D2-1 → pre-tool-use_write_gate.sh
3. ⬜ Implement D2-2 → pre-tool-use_skill_staging_gate.sh
4. ⬜ Implement D2-4 → pre-tool-use_bash_validate_command.sh
5. ⬜ Verify AC-1-S1: 3 scripts executable
6. ⬜ Verify AC-4-S1, AC-4-S1b: allow/block for each gate
7. ⬜ Verify AC-6-S1, AC-6-S1b: bash validate allow/block
8. ⬜ Verify AC-11-S1, AC-11-S1b: graceful degradation

---

**Document**: `docs/context-to-work/roadmap-analysis-phases/Stage-1/scope.2026-07-08.md`
**Generated by**: context-before-fix v1.0.0
**Language**: Vietnamese
**Date**: 2026-07-08
**Status**: Context Complete — Ready for Implementation Phase

**NO CODE CHANGES MADE** — Document only per context-before-fix skill guardrails.
