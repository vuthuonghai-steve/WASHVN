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
- `knowleages/hooks/hooks.md` dòng 685 — PostToolUse ok:false không block (evidence).
- `knowleages/hooks/hooks.md` dòng 2839-2848 — behavior ok:false per event.
