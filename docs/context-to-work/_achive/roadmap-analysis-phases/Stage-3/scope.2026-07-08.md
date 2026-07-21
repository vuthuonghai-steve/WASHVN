---
name: scope-stage-3
description: Scope document cho Stage 3 — Registry Configuration & Unit Tests (Phase 2: Hook Framework Foundation)
version: 0.1.0
suite: WASHVN
tags: [scope, stage-3, registry, unit-tests, hook-framework, phase-2, yaml-resilience]
when_to_use: "Khi cần phân tích scope xây dựng registry.yaml và test scripts cho Hook Framework Foundation"
trace: [TỪ SCOPE phase-2-scope §5.1 D2-7/D2-8], [TỪ PLAN phase-2-plan §4 Stage 3], [TỪ ROADMAP 02-hook-framework D2-7/D2-8]
---

# Scope Document — Stage 3: Registry Configuration & Unit Tests

> **Phase**: Phase 2 — Hook Framework Foundation
> **Stage**: Stage 3 / 5
> **Deliverables**: D2-7 (registry.yaml) + D2-8 (7 test scripts)
> **Ngày**: 2026-07-08
> **Trạng thái**: Initial — Context Complete

---

## §1: Tổng Quan Stage 3

Stage 3 là stage thứ ba trong Phase 2 (Hook Framework Foundation), tập trung vào 2 deliverables cuối cùng của core hook framework trước khi bước vào Verification (Stage 4) và Advanced Hooks Research (Stage 5).

### 1.1 Hai Deliverables Chính

| ID | Deliverable | Path | Loại | Mục Đích |
|:--:|:------------|:-----|:----:|:---------|
| **D2-7** | `registry.yaml` | `.claude/hooks/registry.yaml` | UPDATE (stub→full) | Compile registry 6 hook entries — WASHVN tracking convention |
| **D2-8** | 7 test scripts | `.claude/hooks/tests/test_*.sh` | CREATE (7 files) | Unit test cho 3 gating hooks — verify allow/block behavior |

### 1.2 Mối Quan Hệ Với Các Stage Khác

```text
Phase 2 Pipeline:

Stage 1: PreToolUse Gating Hooks (D2-1, D2-2, D2-4)
  │  Xây dựng 3 hook scripts: write_gate, staging_gate, bash_validate
  │  Cần cho Stage 3 để populate registry paths + test pipe JSON
  │
  ├──→ Stage 3: Registry & Tests (D2-7, D2-8)
  │     D2-7 registry.yaml cần Stage 1 + Stage 2 hooks paths
  │     D2-8 test scripts chỉ cần Stage 1 hooks (D2-1, D2-2, D2-4)
  │     Có thể implement song song với Stage 2
  │
  ├──→ Stage 2: Logging & Lifecycle Hooks (D2-3, D2-5, D2-6)
  │     Registry cần Stage 2 entries cho footer completeness
  │     Test KHÔNG test Stage 2 hooks (chỉ gating hooks)
  │
  ├──→ Stage 4: Verification (AC-1→AC-8)
  │     Chạy toàn bộ test suite + verify registry parse
  │
  └──→ Stage 5: Advanced Hooks (D2-9, D2-10)
        Research parallel — không phụ thuộc Stage 3
```

### 1.3 Vai Trò Trong Hệ Thống

```yaml
registry_yaml:
  - "Single source of truth cho tất cả hooks trong WASHVN"
  - "WASHVN tracking convention — KHÔNG phải format Claude Code runtime đọc"
  - "Bridge mapping đến settings.json (F4) sẽ thực hiện tại Phase 8"
test_scripts:
  - "Primary verification mechanism cho gating hooks (D2-1, D2-2, D2-4)"
  - "Standalone — pipe mock JSON vào hook script, verify exit code"
  - "Mỗi test script độc lập — không phụ thuộc lẫn nhau"
  - "Không cần Claude Code runtime hay settings.json active"
```

---

## §2: Entry Point & Tài Liệu Tham Chiếu

### 2.1 Entry Points

| Entry | Path | Ghi chú |
|:------|:-----|:--------|
| Registry stub (hiện tại) | `.claude/hooks/registry.yaml` | 13 dòng — header + hooks trống + version footer |
| Roadmap spec code | `skills/ver-3/roadmaps/02-hook-framework.md` | D2-7 full code (L228-282), D2-8 code mẫu (L284-317) |
| Phase 2 plan tasks | `docs/context-to-work/roadmap-analysis-phases/phase-2-plan.2026-07-07.md` | §4 Stage 3 — checklist 2 tasks |
| Phase 2 scope | `docs/context-to-work/roadmap-analysis-phases/phase-2-scope.2026-07-07.md` | §5.1 Deliverables, §5.2 Test Matrix, §9 Components |
| Events dir | `.claude/hooks/events/` | `.gitkeep` — chưa có hook script nào |
| Tests dir | `.claude/hooks/tests/` | `.gitkeep` — chưa có test script nào |
| Subagent-forge | `.claude/agents/subagent-forge.md` | Dòng 262 "Hook self-test fails" — abort safety pattern |
| Quality gates ref | `Temps/spec/architects/shared/quality-gates-reference.md` | YAML-RES-1.0 L2 Schema validation |
| YAML Resilience | `Temps/spec/architects/P5-fallback-and-escalation/yaml-resilience-layer.md` | 3-level pre-check — rule_9 context |
| Advanced hooks | `docs/context-to-work/roadmap-analysis-phases/advanced-hooks-capability.2026-07-07.md` | §4 Format Landscape F1/F2/F3/F4 |
| Settings runtime | `.claude/settings.json` | Chỉ permissions block — không hooks key |

### 2.2 Tài Liệu Tham Chiếu Chi Tiết

| File | Nội dung | Dòng chính |
|:-----|:---------|:-----------|
| `02-hook-framework.md` | D2-7 registry.yaml full code mẫu | 228-282 |
| `02-hook-framework.md` | D2-8 test scripts matrix + code mẫu | 284-317 |
| `02-hook-framework.md` | AC verification commands | 322-399 |
| `phase-2-plan.md` | Stage 3 tasks checklist | 246-269 |
| `phase-2-plan.md` | Configuration Architecture — 4 Format Landscape | 363-399 |
| `phase-2-plan.md` | Bridge mapping registry.yaml → settings.json | 378-388 |
| `phase-2-scope.md` | Deliverables Map (D2-7, D2-8) | §5.1 |
| `phase-2-scope.md` | Test Scripts Matrix | §5.2 |
| `phase-2-scope.md` | Official Claude Code Hooks Documentation — Format gap findings | §19 |
| `advanced-hooks-capability.md` | Format Landscape — F1/F2/F3/F4 distinction | §4 |
| `subagent-forge.md` | "Hook self-test fails" pattern | 262-264 |

---

## §3: Scope Definition

### 3.1 In Scope

```yaml
d2_7_registry:
  - "Populate 6 hook entries từ stub lên full registry"
  - "Mỗi entry: name, event_type, matcher, script, description, exit_allow, exit_block"
  - "Footer: version 1.0.0, suite WASHVN, last_updated 2026-07-08, maintainer steve"
  - "YAML-RES-1.0 L2 Schema compliance: required keys hooks, script_path, matcher, event_type"
d2_8_test_scripts:
  - "7 test scripts tại .claude/hooks/tests/ — mỗi script pipe stdin JSON → run hook → verify exit code"
  - "Test coverage: D2-1 write_gate (2 tests), D2-2 staging_gate (2 tests), D2-4 bash_validate (3 tests)"
  - "Tất cả test scripts được chmod +x"
  - "Code template dựa trên roadmap spec D2-8 code mẫu (L304-317)"
format:
  - "F1 (WASHVN Registry): populate registry.yaml đầy đủ"
  - "F4 (Claude Code settings.json): bridge mapping documentation (Phase 8 sẽ implement)"
```

### 3.2 Out of Scope

```yaml
- "KHÔNG tạo hook scripts (Stage 1 và 2)"
- "KHÔNG deploy hooks vào settings.json runtime (Phase 8)"
- "KHÔNG reconcile Format A vs Format B blocking protocol (Phase 8)"
- "KHÔNG tạo test cho D2-3, D2-5, D2-6 (logging/lifecycle hooks — Stage 2)"
- "KHÔNG graceful degradation test cases (recommended bổ sung extra, không bắt buộc)"
- "KHÔNG sửa settings.json permissions block"
- "KHÔNG tạo settings.local.json (D2-9 — Stage 5)"
- "KHÔNG bridge registry.yaml → settings.json (Phase 8)"
- "KHÔNG modify subagent-forge.md inline hooks"
- "KHÔNG modify knowledge docs"
```

### 3.3 Boundary

```yaml
file_boundary: "Chỉ sửa .claude/hooks/registry.yaml; chỉ tạo .claude/hooks/tests/test_*.sh"
dependency:    "Cần Stage 1 hooks (D2-1, D2-2, D2-4) tồn tại để test pipe JSON"
parallel:      "Có thể chạy song song với Stage 2"
test_method:   "Pipe mock JSON vào hook script — không cần Claude Code runtime hay settings.json"
isolation:     "Mỗi test script chạy độc lập — không shared state, không order dependency"
```

---

## §4: D2-7 — Phân Tích Registry.yaml

### 4.1 Cấu Trúc Hiện Tại (Stub — 13 dòng)

```yaml
# Hook Registry — Phase 2 sẽ fill với danh sách đầy đủ
# Cấu trúc mỗi entry:
#   event_type: PreToolUse | PostToolUse | Stop | SessionStart
#   matcher: regex string cho tool_name hoặc event pattern
#   script: path tới shell script trong .claude/hooks/events/
#   exit_allow: exit code = allow (default 0)
#   exit_block: exit code = block (default 2)

hooks:
  # Phase 2 sẽ populate
version: 0.0.1
suite: WASHVN
last_updated: 2026-07-04
```

**Phân tích gaps:**
- `hooks:` key tồn tại nhưng list rỗng — 0 entries
- `version: 0.0.1` cần bump lên `1.0.0` (roadmap spec dùng 1.0.0)
- Thiếu `maintainer` field
- `last_updated` cần update lên 2026-07-08
- Comment header 7 dòng chiếm hơn 50% file

### 4.2 Schema Yêu Cầu Mỗi Entry

```yaml
required_keys:
  - name: string              # Unique identifier, kebab-case
  - event_type: string        # PreToolUse | PostToolUse | Stop | SessionStart
  - matcher: string           # Regex: "Write|Edit", "Bash", ".*"
  - script: string            # Path relative to workspace root
  - description: string       # Mục đích hook (max 200 chars)
optional_keys:
  - exit_allow: integer       # Default: 0
  - exit_block: integer       # Default: 2 (chỉ gating hooks)
footer_keys:
  - version: string           # Semantic version x.y.z
  - suite: string             # "WASHVN"
  - last_updated: string      # ISO date YYYY-MM-DD
  - maintainer: string        # Owner name
```

### 4.3 6 Hook Entries Chi Tiết

| # | name | event_type | matcher | script | exit_allow | exit_block |
|:-:|:-----|:-----------|:--------|:-------|:----------:|:----------:|
| 1 | `pre-write-workspace-gate` | PreToolUse | Write\|Edit | `events/pre-tool-use_write_gate.sh` | 0 | 2 |
| 2 | `pre-skill-staging-gate` | PreToolUse | Write\|Edit | `events/pre-tool-use_skill_staging_gate.sh` | 0 | 2 |
| 3 | `pre-bash-validate-command` | PreToolUse | Bash | `events/pre-tool-use_bash_validate_command.sh` | 0 | 2 |
| 4 | `post-write-audit-log` | PostToolUse | Write\|Edit | `events/post-tool-use_log_artifact.sh` | 0 | — |
| 5 | `stop-session-state-archive` | Stop | .* | `events/stop_session_log_state.sh` | 0 | — |
| 6 | `session-start-record` | SessionStart | .* | `events/session-start_record_metadata.sh` | 0 | — |

**Phân loại:**
- **Entry 1-3 (PreToolUse)**: Gating hooks — có cả `exit_allow` (0) và `exit_block` (2). Block tool call nếu vi phạm.
- **Entry 4-6 (PostToolUse, Stop, SessionStart)**: Non-gating hooks — chỉ có `exit_allow` (0). Không block, chỉ log/side-effect.
- **Matcher**: Entry 1-2 dùng `Write\|Edit` (cùng event type PreToolUse — chạy sequential). Entry 5-6 dùng `.*` (global — match mọi sự kiện).

### 4.4 Cấu Trúc Mục Tiêu (Roadmap Spec)

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
    description: "Block writes to runtime .claude/skills/ unless deploy phase active"
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
    description: "Log session stop + backup corrupt _state.yaml (Γ-7 fix)"
    exit_allow: 0

  - name: session-start-record
    event_type: SessionStart
    matcher: ".*"
    script: .claude/hooks/events/session-start_record_metadata.sh
    description: "Record session metadata on boot"
    exit_allow: 0

version: 1.0.0
suite: WASHVN
last_updated: 2026-07-08
maintainer: steve
```

### 4.5 Format Landscape — F1 vs F4 Distinction

⚠️ **ĐÂY LÀ ĐIỂM QUAN TRỌNG NHẤT CẦN HIỂU**: registry.yaml là WASHVN convention — CLAUDE CODE KHÔNG ĐỌC file này.

Có 4 định dạng cấu hình hook khác nhau trong hệ thống:

| # | Tên | File | Format | Mục đích | Claude Code đọc? |
|:-:|:----|:-----|:-------|:---------|:----------------:|
| **F1** | WASHVN Registry | `.claude/hooks/registry.yaml` | YAML flat list | WASHVN tracking & documentation | ❌ Không |
| **F2** | Knowledge §2.4 | `hooks_and_events.md` | JSON array `[{matcher, handlers}]` | Schema mô tả (sai format) | ❌ Không |
| **F3** | Knowledge §7.4.1 | `hooks_and_events.md` | JSON object `{Event: [{handlers}]}` | Prompt hook config (đúng format) | ✅ Có |
| **F4** | Official Claude Code | `settings.json` | JSON object `hooks: {Event: [{hooks: [{type, command}]}]}` | Runtime activation | ✅ **Có — chính thức** |

Claude Code hooks config được đặt trong `settings.json` (JSON format). Phase 8 sẽ bridge registry.yaml → settings.json.

### 4.6 Bridge Mapping: registry.yaml (F1) → settings.json (F4)

| registry.yaml field | settings.json location | Transformation |
|:--------------------|:-----------------------|:---------------|
| `event_type: PreToolUse` | `"hooks": {"PreToolUse": [...]}` | Flat field → object key |
| `matcher: "Write\|Edit"` | `...{"matcher": "Write\|Edit", ...}` | **Direct 1:1 mapping** |
| `script: "events/gate.sh"` | `...{"command": "\${CLAUDE_PROJECT_DIR}/.claude/hooks/events/gate.sh"}` | Relative → absolute with `${CLAUDE_PROJECT_DIR}` |
| `exit_allow: 0` | N/A — implicit runtime behavior | Use `exit 0` in scripts |
| `exit_block: 2` | N/A — implicit runtime behavior | Use `exit 2` in scripts |
| `description` | Optional `description` field | Can preserve |
| `version/suite/last_updated` | No equivalent | WASHVN-only metadata |

**settings.json hiện tại (chỉ permissions block):**
```json
{
  "permissions": {
    "allow": ["Read", "Glob", "Grep", "Bash(validate_suite_integrity.py)"],
    "deny": ["Bash(rm -rf *)"]
  }
}
```
**Hiện không có hooks key.** Phase 8 sẽ thêm hooks object.

### 4.7 YAML-RES-1.0 L2 Schema Validation

YAML Resilience Layer định nghĩa 3 cấp độ validation:

| Level | Check | Áp dụng registry.yaml | Status |
|:------|:------|:----------------------|:-------|
| **L1 Syntax** | `yaml.safe_load()` parse | File parse thành công | ✅ Dùng python3 |
| **L2 Schema** | Required keys + types + constraints | 6 entries + footer đủ keys | **Cần implement** |
| **L3 Cross-ref** | File paths exist + non-empty | script path → file tồn tại | Defer Phase 8 |

**8 L2 Rules:**

| Rule | Check | Severity | Implementation |
|:-----|:------|:---------|:---------------|
| L2-001 | `hooks` key tồn tại và là list | blocking | `isinstance(data.get('hooks'), list)` |
| L2-002 | hooks list có ≥ 6 entries | blocking | `len(data['hooks']) >= 6` |
| L2-003 | Mỗi entry có: name, event_type, matcher, script, description | blocking | `all(k in h for k in [...])` |
| L2-004 | event_type ∈ enum allowed values | blocking | `h['event_type'] in ['PreToolUse', ...]` |
| L2-005 | script path bắt đầu bằng `.claude/hooks/events/` | warning | `h['script'].startswith(...)` |
| L2-006 | Footer có: version, suite, last_updated, maintainer | blocking | `all(k in data for k in [...])` |
| L2-007 | version format x.y.z | warning | `re.match(r'^\d+\.\d+\.\d+$', v)` |
| L2-008 | suite = WASHVN | warning | `data['suite'] == 'WASHVN'` |

**Verification command:**
```bash
python3 -c "
import yaml, sys, re
d = yaml.safe_load(open('.claude/hooks/registry.yaml'))
assert 'hooks' in d and isinstance(d['hooks'], list), 'L2-001'
assert len(d['hooks']) >= 6, f'L2-002: {len(d[\"hooks\"])}'
for i,h in enumerate(d['hooks']):
    for k in ['name','event_type','matcher','script','description']:
        assert k in h, f'L2-003: hook {i} missing {k}'
    assert h['event_type'] in ['PreToolUse','PostToolUse','Stop','SessionStart'], f'L2-004'
    assert h['script'].startswith('.claude/hooks/events/'), f'L2-005'
for k in ['version','suite','last_updated','maintainer']:
    assert k in d, f'L2-006: missing {k}'
assert re.match(r'^\d+\.\d+\.\d+$', d['version']), 'L2-007'
assert d['suite'] == 'WASHVN', 'L2-008'
print('L2 Schema: PASS')
" && echo 'registry.yaml VALID'
```

### 4.8 Quy Trình Cập Nhật registry.yaml

```text
Bước 1: Mở file .claude/hooks/registry.yaml hiện tại
Bước 2: Xóa comment header 7 dòng (hoặc giữ lại — cần decision)
Bước 3: Populate hooks list với 6 entries (PreToolUse trước, PostToolUse, Stop, SessionStart)
Bước 4: Gating hooks (entry 1-3): thêm exit_allow (0) + exit_block (2)
Bước 5: Non-gating hooks (entry 4-6): chỉ exit_allow (0)
Bước 6: Update footer: version → 1.0.0, last_updated → 2026-07-08, thêm maintainer: steve
Bước 7: Verify: python3 yaml.safe_load() + L2 Schema script
```

---

## §5: D2-8 — Phân Tích Test Scripts

### 5.1 7 Test Scripts Matrix

| # | Test Script | Input (stdin JSON) | Expected Exit | Hook Tested | Category |
|:-:|:------------|:--------------------|:-------------:|:------------|:---------|
| 1 | `test_write_gate_allow.sh` | `{"tool_name":"Write","tool_input":{"file_path":"<ws>/skills/ver-3/test/SKILL.md"}}` | **0** | D2-1 write_gate | Allow |
| 2 | `test_write_gate_block.sh` | `{"tool_name":"Write","tool_input":{"file_path":"/tmp/test.txt"}}` | **2** | D2-1 write_gate | Block |
| 3 | `test_skill_staging_allow_staging.sh` | `{"tool_name":"Write","tool_input":{"file_path":"<ws>/.claude/skills/_staging/test.md"}}` | **0** | D2-2 staging_gate | Allow |
| 4 | `test_skill_staging_block_runtime.sh` | `{"tool_name":"Write","tool_input":{"file_path":"<ws>/.claude/skills/foo/SKILL.md"}}` | **2** | D2-2 staging_gate | Block |
| 5 | `test_bash_validate_allow.sh` | `{"tool_name":"Bash","tool_input":{"command":"ls -la"}}` | **0** | D2-4 bash_validate | Allow |
| 6 | `test_bash_validate_block_destructive.sh` | `{"tool_name":"Bash","tool_input":{"command":"rm -rf /home"}}` | **2** | D2-4 bash_validate | Block |
| 7 | `test_bash_validate_block_network.sh` | `{"tool_name":"Bash","tool_input":{"command":"curl https://example.com"}}` | **2** | D2-4 bash_validate | Block |

### 5.2 Code Template Chung

**Allow test template** (expect exit 0):
```bash
#!/usr/bin/env bash
set -e
WORKSPACE_ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
JSON='{"tool_name":"<Tool>","tool_input":{<fields>}}'
EXIT=0
echo "$JSON" | bash "$WORKSPACE_ROOT/.claude/hooks/events/<script>.sh" 2>&1 || EXIT=$?
[ "$EXIT" = "0" ] || { echo "FAIL: expected exit 0, got $EXIT"; exit 1; }
echo "PASS: <description>"
```

**Block test template** (expect exit 2):
```bash
#!/usr/bin/env bash
set -e
WORKSPACE_ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
JSON='{"tool_name":"<Tool>","tool_input":{<fields>}}'
EXIT=0
echo "$JSON" | bash "$WORKSPACE_ROOT/.claude/hooks/events/<script>.sh" 2>&1 || EXIT=$?
[ "$EXIT" = "2" ] || { echo "FAIL: expected exit 2, got $EXIT"; exit 1; }
echo "PASS: <description>"
```

**Path resolution:** `$(dirname "$0")/../../..` từ `.claude/hooks/tests/` → workspace root. Portable giữa các máy.

### 5.3 Ví dụ Test Script Cụ Thể

**test_write_gate_block.sh** (block test):
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

**test_bash_validate_block_destructive.sh** (block test):
```bash
#!/usr/bin/env bash
# Test: pre-tool-use_bash_validate_command.sh blocks destructive command
set -e
JSON='{"tool_name":"Bash","tool_input":{"command":"rm -rf /home"}}'
EXIT=0
echo "$JSON" | bash .claude/hooks/events/pre-tool-use_bash_validate_command.sh 2>&1 || EXIT=$?
[ "$EXIT" = "2" ] || { echo "FAIL: expected exit 2, got $EXIT"; exit 1; }
echo "PASS: hook blocks rm -rf"
```

### 5.4 Graceful Degradation Tests (Khuyến Nghị Bổ Sung)

Ngoài 7 test scripts chính, các graceful degradation test cases sau được khuyến nghị để verify behavior khi dependencies thiếu:

| # | Test Script | Scenario | Expected Exit | Ghi chú |
|:-:|:------------|:---------|:-------------:|:--------|
| GD-1 | `test_write_gate_jq_missing.sh` | jq không trên PATH → gating hook | **2** (fail closed) | Cần mock PATH không có jq |
| GD-2 | `test_write_gate_malformed_json.sh` | stdin JSON malformed → gating hook | **2** (fail closed) | Pipe raw string thay vì JSON |
| GD-3 | `test_write_gate_empty_path.sh` | file_path rỗng → should allow | **0** | Path rỗng = no-op (không block) |
| GD-4 | `test_bash_validate_empty_cmd.sh` | command rỗng → should allow | **0** | Command rỗng = no-op |

**Nguồn tham khảo:** `.claude/agents/subagent-forge.md` dòng 262: "Hook self-test fails: abort with 'SAFETY HOOK NOT ENFORCING...' Cannot run subagent-forge safely."

Các test này **không bắt buộc** cho Stage 3 core deliverables nhưng được khuyến nghị để đảm bảo robustness.

### 5.5 Phạm Vi Test Coverage

```yaml
hooks_tested:
  - "D2-1 write_gate: 2 tests (allow workspace + block /tmp)"
  - "D2-2 staging_gate: 2 tests (allow _staging/ + block runtime skills/)"
  - "D2-4 bash_validate: 3 tests (allow safe cmd + block destructive + block network)"

hooks_NOT_tested:
  - "D2-3 log_artifact: logging hook — non-blocking, pure side-effect"
  - "D2-5 stop_log_state: lifecycle hook — cần simulation phức tạp (StateStop)"
  - "D2-6 session_start: lifecycle hook — cần Claude Code runtime"

coverage_ratio: "50% hooks (3/6). 100% gating hooks (3/3) have tests."

independence:
  - "Mỗi test script chạy độc lập — không shared state"
  - "Không phụ thuộc thứ tự chạy"
  - "Không cần cleanup giữa các tests"
  - "Không cần Claude Code runtime active"
```

---

## §6: Impact Analysis

### 6.1 Direct Impact (8 files)

| File | Status | From | To | Lines |
|:-----|:-------|:-----|:---|:-----:|
| `.claude/hooks/registry.yaml` | UPDATE | stub (13 dòng) | full 6 entries + footer | ~45 |
| `.claude/hooks/tests/test_write_gate_allow.sh` | CREATE | — | allow test | ~12 |
| `.claude/hooks/tests/test_write_gate_block.sh` | CREATE | — | block test | ~12 |
| `.claude/hooks/tests/test_skill_staging_allow_staging.sh` | CREATE | — | allow test | ~12 |
| `.claude/hooks/tests/test_skill_staging_block_runtime.sh` | CREATE | — | block test | ~12 |
| `.claude/hooks/tests/test_bash_validate_allow.sh` | CREATE | — | allow test | ~12 |
| `.claude/hooks/tests/test_bash_validate_block_destructive.sh` | CREATE | — | block test | ~12 |
| `.claude/hooks/tests/test_bash_validate_block_network.sh` | CREATE | — | block test | ~12 |

### 6.2 Indirect Impact

```yaml
stages_downstream:
  - "Stage 4 — Verification: chạy 7 test scripts + verify registry parse + L2 Schema"
  - "Phase 8 — Integration: bridge registry.yaml → settings.json runtime activation"
quality_gates:
  - "YAML-RES-1.0 L2 Schema: registry.yaml phải pass 8 rules (L2-001→L2-008)"
  - "HOOK-AUDIT-2.0: test scripts pattern có thể mở rộng thành Agent-based test suite (Phase 8)"
subagent_forge:
  - ".claude/agents/subagent-forge.md dòng 262: 'Hook self-test fails' pattern"
  - "Test scripts verify hooks hoạt động — prevent false sense of security khi build subagent"
documentation:
  - "hooks_and_events.md: cần update §2.4 format nếu registry schema thay đổi (Phase 8)"
  - "skills-registry.json: có thể cần update nếu test scripts path được reference"
```

### 6.3 Files Reference (Read-Only)

```text
.claude/hooks/events/                                    # Hook scripts dir (Stage 1&2)
.claude/hooks/events/pre-tool-use_write_gate.sh          # D2-1 — test target
.claude/hooks/events/pre-tool-use_skill_staging_gate.sh  # D2-2 — test target
.claude/hooks/events/pre-tool-use_bash_validate_command.sh # D2-4 — test target
.claude/settings.json                                     # Claude Code runtime — không sửa
.skill-context/_state-archive/                            # Audit log dir — side effect target
```

---

## §7: Acceptance Criteria

| Mã AC | Tiêu Chí | Verification Command | Dự kiến |
|:-----:|:---------|:---------------------|:-------:|
| **AC-2a** | registry.yaml YAML syntax hợp lệ | `python3 -c "import yaml; yaml.safe_load(open('.claude/hooks/registry.yaml'))"` | ✅ |
| **AC-2b** | registry.yaml có đúng 6 hook entries | `python3 -c "import yaml; d=yaml.safe_load(open('...')); assert len(d['hooks'])==6"` | ✅ |
| **AC-2c** | registry.yaml pass L2 Schema validation | `python3 -c "import yaml; d=yaml.safe_load(open('...')); [assert all(k in h for k in ['name','event_type','matcher','script','description']) for h in d['hooks']]"` | ✅ |
| **AC-2d** | Footer đầy đủ (version, suite, last_updated, maintainer) | `python3 -c "import yaml; d=yaml.safe_load(open('...')); assert all(k in d for k in ['version','suite','last_updated','maintainer'])"` | ✅ |
| **AC-3a** | 7 test scripts tồn tại | `for t in test_write_gate_allow test_write_gate_block test_skill_staging_allow_staging test_skill_staging_block_runtime test_bash_validate_allow test_bash_validate_block_destructive test_bash_validate_block_network; do test -f ".claude/hooks/tests/$t.sh"; done` | ✅ |
| **AC-3b** | 7 test scripts executable | `for t in .claude/hooks/tests/test_*.sh; do test -x "$t"; done` | ✅ |
| **AC-3c** | 7 test scripts đều đạt PASS | `for t in .claude/hooks/tests/test_*.sh; do bash "$t" || exit 1; done` | ✅ |
| **AC-4** | Hook self-test: allow→exit 0, block→exit 2 | Pipe JSON mẫu vào từng hook → verify exit code | ✅ |
| **AC-6** | Bash validate phân biệt allow/block | `ls -la` exit 0, `rm -rf /home` exit 2 | ✅ |

**Total Stage 3 AC: 9 checks | 8 files (1 update + 7 create)**

---

## §8: Thứ Tự Build Khuyến Nghị

### 8.1 Dependency Graph

```text
Stage 1 (D2-1, D2-2, D2-4) xong
  │
  ├──→ D2-8 (7 test scripts)
  │     Chỉ cần Stage 1 hooks tồn tại
  │     Có thể làm NGAY sau Stage 1 — không cần đợi Stage 2
  │     Bước 1-7: tạo từng test script → chmod +x → chạy suite
  │
  └──→ D2-7 (registry.yaml)
        Cần Stage 1 + Stage 2 hooks paths cho 6 entries đầy đủ
        Nếu Stage 2 chưa xong: có thể populate 3 PreToolUse entries trước
```

### 8.2 Thứ Tự Khuyến Nghị

```text
Priority 1 (chạy ngay sau Stage 1 — song song Stage 2):
  Step 1:  test_write_gate_allow.sh
  Step 2:  test_write_gate_block.sh
  Step 3:  test_skill_staging_allow_staging.sh
  Step 4:  test_skill_staging_block_runtime.sh
  Step 5:  test_bash_validate_allow.sh
  Step 6:  test_bash_validate_block_destructive.sh
  Step 7:  test_bash_validate_block_network.sh
  Step 8:  chmod +x cho tất cả 7 test scripts
  Step 9:  chạy full suite: for t in tests/test_*.sh; do bash "$t"; done

Priority 2 (sau Stage 1 + Stage 2):
  Step 10: populate registry.yaml với 6 entries
  Step 11: verify YAML syntax + L2 Schema + 6 entries count

Optional:
  Step 12: graceful degradation tests (GD-1→GD-4)
```

### 8.3 Parallel Execution

```yaml
d2_7_vs_d2_8:
  possible: true
  note: "D2-7 và D2-8 không phụ thuộc nhau. Có thể làm song song hoàn toàn."
with_stage_2:
  d2_8: "Song song hoàn toàn — D2-8 chỉ cần Stage 1 hooks"
  d2_7: "Partial — có thể populate 3 PreToolUse entries trước, thêm 3 entries còn lại sau Stage 2"
```

---

## §9: Các Vấn Đề Cần Lưu Ý (Open Questions)

| # | Vấn Đề | Priority | Tác Động | Status |
|--:|:--------|:--------:|:---------|:-------|
| 1 | **registry.yaml là convention — Claude Code không đọc**: Cần ensure developer hiểu rõ F1 vs F4 | **High** | Tránh nhầm lẫn về mục đích file | ✅ Resolved |
| 2 | **Test scripts standalone pipe JSON**: Không cần settings.json active để chạy test | **High** | Test method xác định — không phụ thuộc runtime | ✅ Resolved |
| 3 | **Stage 3 phụ thuộc Stage 1**: Nếu Stage 1 chưa xong, block D2-8 implementation | **Medium** | Block critical path | ⚠️ Theo dõi |
| 4 | **Script path format trong registry**: Dùng relative path (roadmap spec) hay absolute? | **Medium** | D2-7 format consistency | ⚠️ Cần confirm |
| 5 | **Graceful degradation tests**: Có implement GD-1→GD-4 trong Stage 3 hay defer? | **Medium** | Extra scope (không bắt buộc) | ⚠️ Khuyến nghị bổ sung |
| 6 | **version bump 0.0.1 → 1.0.0**: Roadmap spec dùng 1.0.0 — có bump không? | **Low** | D2-7 footer | ✅ Resolved (bump) |
| 7 | **Path resolution portable**: `$(dirname "$0")/../../..` có hoạt động cross-platform? | **Low** | D2-8 template design | ✅ Resolved (Linux/macOS) |
| 8 | **Audit log side effects**: Test scripts pipe JSON vào hook có tạo log entries không? | **Low** | Cleanup policy | ⚠️ Cần quyết định |

---

## §10: Confidence Assessment

```yaml
overall_confidence: 92%

breakdown:
  spec_completeness: 95%
    note: "Roadmap spec D2-7 và D2-8 có code mẫu đầy đủ (L228-282 registry, L284-317 tests)"
    risk: "Comment header trong registry.yaml có thể cần giữ/xóa — chưa có decision"
  
  code_readiness: 95%
    note: "Code mẫu cho registry.yaml và test scripts đã có sẵn trong roadmap spec"
    risk: "Script path format cần confirm (relative vs absolute)"
  
  test_coverage: 85%
    note: "7 test scripts cover 3/3 gating hooks với allow/block pairs"
    risk: "Thiếu graceful degradation tests (jq missing, malformed JSON)"
  
  dependency_ready: 80%
    note: "Stage 3 phụ thuộc Stage 1 hooks tồn tại"
    risk: "Nếu Stage 1 chưa xong, test scripts không thể chạy"
  
  format_gap_awareness: 95%
    note: "Đã xác định rõ F1 (registry.yaml) vs F4 (settings.json)"
    risk: "Developer mới có thể confused về mục đích của registry.yaml"
  
  risk_mitigation: 85%
    note: "All risks identified have mitigation plans"
    risk: "Stage 1 dependency là external risk — không thể mitigate từ Stage 3"

uncertainty_flags:
  - "Script path format trong registry.yaml cần confirm"
  - "Graceful degradation tests: implement trong Stage 3 hay defer?"
  - "Audit log side effects cleanup policy cho test scripts"
```

---

## §11: Tổng Kết

### 11.1 Stage 3 At a Glance

| Metric | Value |
|:-------|:-----:|
| Deliverables | 2 (D2-7 + D2-8) |
| Files modified | 1 (registry.yaml) |
| Files created | 7 (test scripts) |
| Total files | 8 |
| Estimated total lines | ~140 (45 registry + 95 tests) |
| Dependencies | Stage 1 (PreToolUse hooks) |
| Parallel possible | Stage 2 (logging hooks) |
| Acceptance checks | 9 |
| Confidence | 92% |

### 11.2 Key Decisions

```yaml
registry_is_tracking_not_runtime:
  rationale: "registry.yaml là WASHVN convention — Claude Code không đọc. Phase 8 bridge sang settings.json"
  impact: "Stage 3 chỉ populate registry.yaml — không cần verify với Claude Code runtime"

test_scripts_standalone:
  rationale: "Test scripts dùng pipe mock JSON → run hook → verify exit code. Không cần Claude Code runtime"
  impact: "Test scripts chạy độc lập, không phụ thuộc settings.json hay runtime environment"

coverage_focus_gating:
  rationale: "Chỉ test D2-1, D2-2, D2-4 (PreToolUse gating hooks). D2-3, D2-5, D2-6 không test"
  impact: "7 test scripts cover 3/6 hooks = 50%. Chấp nhận được vì gating hooks là critical path"

parallel_with_stage_2:
  rationale: "D2-8 test scripts chỉ cần Stage 1 hooks. D2-7 registry cần Stage 1+2 cho đủ 6 entries"
  impact: "Có thể start D2-8 ngay sau Stage 1, song song với Stage 2"
```

### 11.3 Downstream Impact

```yaml
stage_4_verification:
  - "Chạy 7 test scripts — expect 100% PASS"
  - "Verify registry.yaml parse + L2 Schema"
  - "Verify registry.yaml consistency với hook scripts thực tế"
phase_8_integration:
  - "Bridge registry.yaml (F1) → settings.json (F4) runtime activation"
  - "Thêm graceful degradation test cases vào test suite"
  - "Mở rộng registry schema nếu cần thêm external_validator hook (hook thứ 7)"
quality_gates:
  - "YAML-RES-1.0 L2 Schema: registry.yaml pass 8 rules"
  - "HOOK-AUDIT-2.0: test scripts pattern có thể mở rộng thành Agent-based test suite"
```

### 11.4 Delivery Checklist

```yaml
d2_7_registry:
  - "[ ] Populate 6 hook entries (name, event_type, matcher, script, description)"
  - "[ ] Gating hooks (entry 1-3): exit_allow=0, exit_block=2"
  - "[ ] Non-gating hooks (entry 4-6): exit_allow=0 (no exit_block)"
  - "[ ] Footer: version 1.0.0, suite WASHVN, last_updated 2026-07-08, maintainer steve"
  - "[ ] Verify YAML syntax: python3 yaml.safe_load()"
  - "[ ] Verify L2 Schema: 8 rules L2-001→L2-008"

d2_8_test_scripts:
  - "[ ] test_write_gate_allow.sh — workspace path → exit 0"
  - "[ ] test_write_gate_block.sh — /tmp path → exit 2"
  - "[ ] test_skill_staging_allow_staging.sh — _staging/ → exit 0"
  - "[ ] test_skill_staging_block_runtime.sh — runtime skills/ → exit 2"
  - "[ ] test_bash_validate_allow.sh — ls -la → exit 0"
  - "[ ] test_bash_validate_block_destructive.sh — rm -rf /home → exit 2"
  - "[ ] test_bash_validate_block_network.sh — curl → exit 2"
  - "[ ] chmod +x cho tất cả 7 test scripts"
  - "[ ] Full suite PASS: for t in tests/test_*.sh; do bash \"$t\"; done"

optional:
  - "[ ] Graceful degradation tests (GD-1→GD-4) — khuyến nghị"
```

---

**Document Status**: Context Complete — Ready for Stage 3 Implementation
**NO Code Changes Made** — Document only per context-before-fix skill guardrails

```
✓ §1 Tổng Quan Stage 3 — deliverables table, pipeline relationships, roles
✓ §2 Entry Point — 10 entry points mapped + 10 reference docs
✓ §3 Scope Definition — in scope (3 areas), out of scope (10 items), boundary (5 rules)
✓ §4 D2-7 Registry — stub analysis, schema, 6 entries table, target structure, Format Landscape (F1-F4), bridge mapping, L2 Schema (8 rules), update procedure
✓ §5 D2-8 Test Scripts — 7-test matrix, code templates, example scripts, graceful degradation (4 extra tests), coverage analysis (50% hooks)
✓ §6 Impact Analysis — 8 direct files, 4 indirect areas, 4 reference files
✓ §7 Acceptance Criteria — 9 AC checks with verification commands
✓ §8 Build Order — priority 1/2 steps, dependency graph, parallel strategy
✓ §9 Open Questions — 8 issues tracked with priority and status
✓ §10 Confidence Assessment — 92%, 6 metrics, 3 uncertainty flags
✓ §11 Tổng Kết — metrics table, 4 key decisions, downstream impact, delivery checklist
```
