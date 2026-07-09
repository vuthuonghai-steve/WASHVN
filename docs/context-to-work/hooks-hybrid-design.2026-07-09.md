# Design Doc — Hooks Hybrid Model (script + prompt)

**Date**: 2026-07-09
**Status**: Implemented
**Scope**: `WASHVN/.claude/settings.json` + 7 hook scripts (unchanged)
**Decision basis**: analyst report on `knowleages/hooks/hooks.md` (3101 dòng, official Claude Code docs)

---

## §1. Mục tiêu

Nâng cấp hệ thống hooks từ **script-only (hard gate)** sang **hybrid (script + prompt)**:
- Giữ `command` scripts làm preventive gate (deterministic, rẻ, always-on).
- Thêm `prompt` hook làm **semantic advisory layer** — bắt các lỗi script regex/bash không thể phát hiện (placeholder ẩn, 7-Zone violation, broken cross-refs, token-limit drift).
- Không hard-deny qua prompt (advisory only) → tránh false-positive gián đoạn luồng build.

---

## §2. Evidence từ tài liệu chính thức

- `prompt` hook type được hỗ trợ ở **cả PreToolUse, PostToolUse, Stop** (hooks.md dòng 2749-2763). Chỉ `SessionEnd` + `SessionStart`/`Setup` là KHÔNG có prompt.
- `prompt` = model call (mặc định fast/Haiku), timeout 30s, **KHÔNG async** → mỗi fire phải chờ.
- `PostToolUse` `ok:false` **KHÔNG block** (tool đã chạy) → chỉ warning / `additionalContext`. `continueOnBlock: true` → feed reason vào turn tiếp theo.
- `PreToolUse` `ok:false` = **deny** tool call. → Vi phạm advisory-only → KHÔNG dùng PreToolUse prompt.
- Prompt hook tốn token mỗi fire → thu hẹp bằng `matcher` (Write|Edit), không gắn Bash (fire quá frequent).

---

## §3. Hook Types khả dụng (5 loại) — đã khai thác / chưa

| Type | Trạng thái | Tiềm năng tương lai |
|:-----|:----------|:-------------------|
| `command` | ✅ dùng (4 scripts) | Hard gate — giữ nguyên |
| `prompt` | ✅ dùng (Stop + mới PostToolUse) | Semantic advisory |
| `http` | ❌ chưa | Gửi JSON sang validator service riêng (kiểm soát quota/model) |
| `mcp_tool` | ❌ chưa | Gọi MCP tool validate schema/YAML (deterministic hơn prompt) |
| `agent` | ❌ chưa | Spawn subagent đa-turn review (experimental) |

**Fields chưa khai thác (có thể dùng sau):**
- `if` — scoping hẹp hơn matcher: `"Edit(*.ts)"`, `"Bash(git *)"`.
- `hookSpecificOutput.additionalContext` — feedback mềm (đã dùng qua prompt continueOnBlock).
- `hookSpecificOutput.updatedToolOutput` — PostToolUse auto-repair output (vd: sửa YAML hỏng).
- `hookSpecificOutput.permissionDecision: defer/ask` — PreToolUse defer thay deny/allow.
- `async` — chỉ `command` hỗ trợ; hook dài (log_artifact) có thể chạy async.

---

## §4. Cấu trúc hybrid cuối cùng

```
PreToolUse (Write|Edit):
  ├─ command: pre-tool-use_write_gate.sh        [HARD GATE] block ngoài workspace
  └─ command: pre-tool-use_skill_staging_gate.sh [HARD GATE] block ghi runtime .claude/skills/

PreToolUse (Bash):
  └─ command: pre-tool-use_bash_validate_command.sh [HARD GATE] block rm -rf/sudo/network

PostToolUse (Write|Edit):
  ├─ command: post-tool-use_log_artifact.sh      [LOG, non-block]
  ├─ command: validate-state-ledger.sh           [VERIFY _state_ledger.yaml, block nếu hỏng]
  └─ prompt:  semantic-quality-reviewer          [ADVISORY] additionalContext feedback

Stop:
  ├─ command: stop_session_log_state.sh          [LOG + backup _state.yaml hỏng]
  └─ prompt:  structural-completeness-check       [ADVISORY] JSON {ok, reason}
```

---

## §5. Prompt PostToolUse (mới)

```json
{
  "type": "prompt",
  "prompt": "You are a quality reviewer for the WASHVN skill/agent lab. A file was just written or edited. Input JSON: $ARGUMENTS. Review the written file for: (1) YAML frontmatter completeness — for .md agent/skill files require name, version, suite, tags; (2) dangling placeholders (TODO/FIXME/mock/pass #) that are real (ignore prose mentioning them); (3) if SKILL.md, token count <=700; (4) well-formed Markdown (no broken tables, no unterminated code fences). Return JSON {\"ok\": true, \"reason\": \"...\"} if clean, or {\"ok\": false, \"reason\": \"<concise list of issues>\"}. This is advisory — do NOT block; surface findings as guidance.",
  "timeout": 30,
  "continueOnBlock": true
}
```

**Behavior:** mỗi Write|Edit → 1 model call → nếu có issue, reason được feed vào conversation như `additionalContext` (không block, không deny). Claude tự điều chỉnh.

---

## §6. Tradeoffs & Rủi ro

- **Latency:** mỗi Write|Edit chờ ~model call (30s timeout). Chấp nhận (user: không quản quota).
- **Token cost:** prompt fire mỗi artifact write. Thu hẹp Write|Edit (không Bash) để giảm.
- **False-positive advisory:** prompt có thể báo sai → chỉ advisory, không block → an toàn.
- **Không async:** prompt tuần tự. Nếu muốn parallel, chuyển sang `command` gọi LLM API riêng (http/mcp_tool).

---

## §7. Verification

- [x] settings.json valid JSON (parse bằng `jq`)
- [x] PostToolUse prompt added với continueOnBlock:true
- [x] 4 command scripts unchanged (hard gate intact)
- [ ] Thực tế fire 1 Write → quan sát additionalContext xuất hiện trong chat
- [ ] Stop prompt vẫn trả JSON {ok, reason} đúng schema

---

## §8. Future (không implement hôm nay)

1. PreToolUse `prompt` nếu cần hard-deny semantic (vi phạm advisory-only hiện tại).
2. `mcp_tool` validator thay prompt để deterministic + rẻ hơn.
3. `updatedToolOutput` auto-repair YAML hỏng ở PostToolUse.
4. `if` scoping cho staging gate (chỉ check `Edit(*.md)` trong skills/).
