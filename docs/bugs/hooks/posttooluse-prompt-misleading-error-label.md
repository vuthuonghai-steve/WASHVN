# BUG-001: PostToolUse `prompt` hook `ok:false` mislabeled as "Error writing file" / "blocking error"

**Date**: 2026-07-09
**Severity**: Medium (UX/UX-trust, not data-loss)
**Component**: Claude Code hook surface (PostToolUse `prompt` type) + WASHVN settings.json
**Status**: Open — observed, not yet reported upstream

---

## §1. Symptom

Khi một `prompt` hook ở event `PostToolUse` (matcher `Write|Edit`) trả về:

```json
{ "ok": false, "reason": "<findings>" }
```

Claude Code hiển thị banner:

```
Error writing file
PostToolUse:Write hook returned blocking error
[<prompt text>]: <reason>
```

Người dùng **hiểu lầm file ghi THẤT BẠI** (do nhãn "Error writing file" + "blocking error").

## §2. Actual behavior (verified)

- File **ĐÃ ĐƯỢC GHI THÀNH CÔNG**. PostToolUse chạy *sau* tool hoàn tất, nên output đã flush xuống disk.
- Evidence từ test 2026-07-09: Write tool trả `"File created successfully at ..."`, và file có thể `rm` ngay sau đó → tồn tại trên disk.
- Theo tài liệu chính thức (`knowleages/hooks/hooks.md` dòng 685): *PostToolUse exit 2 / ok:false KHÔNG block* (tool đã chạy rồi). Chỉ `PreToolUse` ok:false mới deny tool call.

→ **Hook logic ĐÚNG. Chỉ nhãn UI sai.** Đây là misleading label, không phải hook hiểu sai nội dung.

## §3. Root cause

- `prompt` hook `ok:false` tại PostToolUse được Claude Code surface render với cùng code path như lỗi block thực sự (PreToolUse deny / command exit 2).
- Không có phân biệt giữa "advisory feedback" (continueOnBlock:true) và "hard block" → UI gộp chung thành "Error writing file" + "blocking error".
- `continueOnBlock: true` chỉ ảnh hưởng luồng tiếp tục (turn không dừng), KHÔNG ảnh hưởng cách banner hiển thị.

## §4. Impact

- Người dùng tưởng write fail → có thể retry ghi, tạo duplicate/orphan file.
- Mất trust vào hook system (tưởng hook broken trong khi hoạt động đúng).
- Ở WASHVN: prompt hook được set advisory-only (continueOnBlock:true) theo design doc `hooks-hybrid-design.2026-07-09.md` → mọi Write có issue đều hiện banner "Error" dù file OK.

## §5. Reproduction

1. settings.json có PostToolUse `prompt` hook (Write|Edit) với `continueOnBlock: true`.
2. Write một file có lỗi (vd: thiếu `tags` trong frontmatter, có `TODO` thật).
3. Quan sát: banner "Error writing file" + "blocking error" hiện ra.
4. Kiểm tra disk: file vẫn tồn tại → confirm false-negative label.

Test thực tế 2026-07-09:
```
INPUT file: .claude/agents/_staging/test-prompt-hook.md (thiếu tags, có TODO + mock())
OUTPUT banner: "Error writing file / PostToolUse:Write hook returned blocking error"
                 "Frontmatter missing tags. Dangling placeholders: 'TODO: fix this later', 'mock()'."
DISK: file created successfully, removable afterward → write actually succeeded
```

## §6. Expected vs Actual

| | Expected | Actual |
|:--|:--|:--|
| File on disk | written | written (OK) |
| Banner | "Advisory: issues found" / non-error tone | "Error writing file" + "blocking error" |
| Turn continues | yes (continueOnBlock) | yes (continueOnBlock) |

## §7. Workarounds (current)

1. **Nhận thức:** hiểu "Error writing file" ở PostToolUse = advisory, không phải write fail. Kiểm tra disk để confirm.
2. **Giảm noise:** thu hẹp prompt chỉ check nghiêm trọng (vd: chỉ SKILL.md ≤700 token), bỏ tags/placeholder.
3. **Hard-block instead:** bỏ `continueOnBlock` → ok:false sẽ deny (nhưng mất tính advisory, vi phạm design decision).

## §8. Suggested upstream fix

Claude Code nên phân biệt banner:
- PreToolUse `ok:false` / command exit 2 → "blocked" (đúng).
- PostToolUse `ok:false` + `continueOnBlock` → "advisory / warning" tone, KHÔNG "Error writing file".

Hoặc: thêm field `severity: advisory|block` trong prompt JSON để UI render đúng tone.

## §9. Related

- `docs/context-to-work/hooks-hybrid-design.2026-07-09.md` — thiết kế hybrid, giải thích tại sao prompt advisory-only.
- `.claude/knowleages/hooks/hooks.md` dòng 685 — PostToolUse ok:false không block (evidence). **[FIXED 2026-07-09]** path gốc thiếu prefix `.claude/`.
- `.claude/knowleages/hooks/hooks.md` dòng 2839-2848 — behavior ok:false per event.

---

## §10. Verification log (2026-07-09)

**Phương pháp:** đọc source thực tế `.claude/knowleages/hooks/hooks.md` (3100 dòng) + `.claude/settings.json` + `.claude/settings.local.json`, đối chiếu với claims trong report.

| Claim trong report | Kết quả | Evidence |
|:--|:--|:--|
| PostToolUse ok:false không block (file đã ghi) | ✅ CONFIRMED | hooks.md:685 — `PostToolUse \| No \| Shows stderr to Claude; the tool already ran` |
| `continueOnBlock:true` feed reason + continue turn | ✅ CONFIRMED | hooks.md:2844 |
| Config trong settings.json khớp mô tả | ✅ CONFIRMED | settings.json:57-62 (prompt + continueOnBlock:true) |
| Banner "Error writing file / blocking error" | ⚠️ UNVERIFIED | Chỉ có 1 observation 2026-07-09, doc mô tả là **"warning line"** chứ không phải "Error writing file". Cần live repro để chụp exact banner string. |
| Path `knowleages/hooks/hooks.md` | ❌ WRONG PATH | Thiếu prefix `.claude/` (file thực tế tại `.claude/knowleages/hooks/hooks.md`) |

**Kết luận:** Cơ chế hook ĐÚNG. Report mechanics xác thực. Nhưng:
1. Citation path sai (đã sửa §9).
2. Headline claim "mislabeled as Error writing file" **chưa được chứng minh** từ docs — doc nói "warning line". Cần live repro trước khi report upstream.
3. §8 `severity` field = upstream feature request, không phải config fix hiện có (prompt hook chỉ trả `ok`+`reason`).

---

## §11. Derived bugs (phát hiện trong lúc verify)

### §11.1 BUG-002: Stop command hook path sai cwd → "No such file"
- **Symptom:** Stop event (chạy từ cwd `build-workflow`) báo `bash: .claude/hooks/events/stop_session_log_state.sh: No such file or directory`.
- **Root cause:** bare `.claude/...` resolve theo **session cwd**, không phải project root. Khi cwd ≠ WASHVN thì miss. hooks.md:479-481 khuyến nghị dùng `${CLAUDE_PROJECT_DIR}`.
- **Fix (đã apply):** settings.json:82 → `bash ${CLAUDE_PROJECT_DIR}/.claude/hooks/events/stop_session_log_state.sh`. JSON valid.
- **Residual:** 5 sibling command hooks (PreToolUse ×3, PostToolUse ×2, SessionStart ×1) vẫn dùng bare `.claude/...` — cùng fragility. Chưa fix (chờ user approve).

### §11.2 BUG-003: Stop prompt hook loop (ok:false on no-doc-change)
- **Symptom:** session không đóng được; Stop prompt hook trả `ok:false` liên tục → hooks.md:2841 (Stop ok:false feed reason back + continue turn) → infinite loop, drain token.
- **Root cause:** prompt yêu cầu trả JSON, nhưng khi không có doc nào đổi, model vẫn trả `ok:false` ("did not evaluate") → tự trigger tiếp turn.
- **Fix (đã apply):** settings.local.json Stop prompt hook thêm directive: nếu không có doc thay đổi → trả `{"ok": true, "reason": "No doc changes to evaluate"}`, NEVER ok:false. JSON valid.
- **Note:** fix chỉ có hiệu lực sau khi **restart session** (settings không hot-reload). Session hiện tại vẫn loop vì hook cũ đã load.

---

## §12. Session handoff (cho restart)

**Tình hình hiện tại (2026-07-09):**
- BUG-001: mechanics verified, headline claim UNVERIFIED (cần live repro).
- BUG-002 (Stop command path): FIXED in settings.json, cần verify sau restart.
- BUG-003 (Stop prompt loop): FIXED in settings.local.json, **chỉ生效 sau restart**.

**Action bắt buộc trước khi tiếp tục:**
1. **RESTART session** để reload `.claude/settings.json` + `.claude/settings.local.json` → chấm dứt Stop-hook loop, kích hoạt path fix.
2. Sau restart: xác nhận Stop event trả `ok:true` ("No doc changes to evaluate") và không loop.

**Open items (chờ user quyết định):**
- [ ] Live repro BUG-001: write temp file thiếu `tags` + real placeholder marker, capture exact banner string.
- [ ] Widen `${CLAUDE_PROJECT_DIR}` tới 5 sibling command hooks.
- [ ] Update BUG-001 report path citation (đã làm §9) — confirm với user.

**Files changed this session:**
- `.claude/settings.json` (Stop command hook path)
- `.claude/settings.local.json` (Stop prompt hook loop guard)
- `docs/bugs/hooks/posttooluse-prompt-misleading-error-label.md` (this update)
