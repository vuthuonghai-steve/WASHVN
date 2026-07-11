# Bug Report — user-knowledge-ingestor: Write Hook Regex Chứa Literal `{skill}` Thay vì Wildcard

- **Date:** 2026-07-11
- **Severity:** High (block mọi domain ingest hợp lệ)
- **Status:** Open — fix chưa apply
- **Component:** `.claude/agents/user-knowledge-ingestor.md` — PreToolUse `Write` hook (dòng 20)
- **Branch:** `feat/architect-v1`
- **Phát hiện qua:** Phase 5 code review — cross-check hook regex với actual path pattern

---

## 1. Symptom

Mọi lệnh ingest domain knowledge từ user đều bị block:

```
BLOCKED: ingestor chỉ write .skill-context/{skill}/user-contrib*
```

Hook **không bao giờ match** đường dẫn thực tế → `exit 2` trên mọi Write cố gắng, kể cả write hợp lệ.

---

## 2. Root Cause

`user-knowledge-ingestor.md` dòng 20:

```bash
# BEFORE (BROKEN) — literal string
if [[ ! "$FILE_PATH" =~ \.skill-context/{skill}/user-contrib ]]; then
  echo "BLOCKED: ..." >&2
  exit 2
fi
```

`{skill}` là **placeholder notation** (ý đồ template để thay bằng tên skill thực tế), nhưng trong shell regex context nó là **literal string**.

**Path thực tế khi ingest:** `payment-gateway` skill:

```
.skill-context/payment-gateway/user-contrib/user-contributed-knowledge.md
```

Regex đang match:
```
\.skill-context/{skill}/user-contrib
```

Phải match:
```
\.skill-context/payment-gateway/user-contrib
```

`{skill}` literal khớp với `{skill}` — không khớp với `payment-gateway` → **không bao giờ match** → block mọi write.

---

## 3. Impact

| Scenario | Expected | Actual |
|:---------|:---------|:-------|
| `ingest docs/domain-spec.pdf for skill payment-gateway` | Writes .skill-context/payment-gateway/user-contrib/... | ❌ Blocked — no artifact created |
| `analyze src/legacy/ for skill inventory-migration` | Writes .skill-context/inventory-migration/user-contrib/... | ❌ Blocked |
| `ingest README.md for skill test-skill` | Writes ingest-log.md (status=skipped) | ❌ Blocked |
| Bất kỳ ingest nào tạo artifact | Write vào zone hợp lệ | ❌ Đều bị block |

**Tất cả phiên ingest đều silent-fail** — hook block trước khi agent kịp ghi bất kỳ output nào.

---

## 4. Fix

**Surgical — một dòng duy nhất:**

```bash
# AFTER (FIXED) — wildcard path segment
if [[ ! "$FILE_PATH" =~ \.skill-context/[^/]+/user-contrib ]]; then
  echo "BLOCKED: ingestor chỉ write .skill-context/{skill}/user-contrib* (vd .skill-context/payment-gateway/user-contrib/)" >&2
  exit 2
fi
```

Thay đổi:
- `{skill}` → `[^/]+` (wildcard match 1 path segment)
- Message báo lỗi thêm ví dụ cụ thể để dễ debug

Logic giữ nguyên: **chỉ** match `.skill-context/<skill-name>/user-contrib*`. Bảo vệ zone isolation không đổi.

---

## 5. Verification (Post-Fix)

1. Write `.skill-context/payment-gateway/user-contrib/ingest-log.md` → allowed (exit 0)
2. Write `.skill-context/inventory-migration/user-contrib/glossary-supplement.yaml` → allowed (exit 0)
3. Write `.skill-context/payment-gateway/ba-elicitor/elicitation-report.md` → blocked (đúng — zone khác)
4. Write `.claude/agents/user-knowledge-ingestor.md` → blocked (đúng — runtime)

---

## 6. Related

- **Pattern sibling:** ba-pipeline-runner hook dòng 20 dùng `.*` đúng — không mắc lỗi này:
  ```bash
  if [[ ! "$FILE_PATH" =~ \.skill-context/.*/ba-(elicitor|analyst|synthesizer)/ ]] && ...
  ```
- **Root cause class:** Template variable (`{skill}`) leak vào production regex — common LLM coding mistake (see CLAUDE.md §11 — Karpathy).

---

*Phát hiện qua code review Phase 5 (ba-pipeline-runner rewrite). Bug ngăn cản toàn bộ chức năng ingest — recommend fix trước Phase 6.*
