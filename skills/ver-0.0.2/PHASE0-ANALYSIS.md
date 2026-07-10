# Phase 0 Analysis — `skills/ver-0.0.2`

> **Scope:** Pre-flight gate verification cho skills suite phiên bản 0.0.2
> **Ngày phân tích:** 2026-06-17
> **Tổng effort ước tính:** ~0.9h (55 phút)
> **Gate Status tổng:** 🔴 **FAIL** (3/4 sub-gates fail)

---

## 1. Executive Summary

- 🔴 **3/4 sub-gates FAIL** — Phase 0 chưa đạt acceptance, cần remediation trước khi sync runtime.
- 🔴 **P0.1 (Hardcoded Paths):** 3 paths `/home/steve/Work-space/` còn nằm trong `ROADMAP.md` (lines 4, 5, 141) — vi phạm portability rule, chặn acceptance 0-hit.
- 🔴 **P0.2 (AGENTS.md):** File tồn tại nhưng rỗng (0 bytes / 0 lines) — thiếu L0 routing anchor cho `skills/` subzone, vi phạm Crucial Rule từ `skills/CLAUDE.md`.
- 🔴 **P0.3 (CASE Duplication):** `case-system.md` trùng lặp đồng nhất (SHA1 `b71ca178ea5b...`, 7372 bytes) giữa `_shared/knowledge/` và `skill-planner/knowledge/` — drift risk cao.
- 🟢 **P0.4 (File Links):** 3/3 file links resolve thành công — không có broken link, gate PASS.

---

## 2. Bảng tổng hợp 4 Task

| Task | Tên | Trạng thái | Severity | Effort | Blocking? |
|------|-----|------------|----------|--------|-----------|
| P0.1 | Hardcoded Paths Scan | 🔴 FAIL | Low | 20 min | Có |
| P0.2 | AGENTS.md Status | 🔴 FAIL | Medium | 15 min | Có |
| P0.3 | CASE System Duplication | 🔴 FAIL | Medium | 5 min | Có |
| P0.4 | File Links Integrity | 🟢 PASS | None | 0 min | Không |

---

## 3. Chi tiết từng Task

### 3.1 🔴 P0.1 — Hardcoded Paths Scan

**Hiện trạng:** 9 hits phát hiện tổng cộng, phân bổ như sau:

| Loại | Số lượng | File | Trạng thái |
|------|----------|------|------------|
| Hardcoded path thực sự | **3** | `ROADMAP.md` (lines 4, 5, 141) | 🔴 Cần fix |
| Anti-pattern documentation | 2 | `dev-standards.md` (line 46), `quality-matrix.yaml` (line 288) | 🟢 Acceptable |
| Session metadata (cwd cũ) | 1 | `.omc/state/sessions/7bfedfd1.../session-started.json` (line 4) | 🟢 Auto-generated |
| Self-referential ROADMAP | 2 | `ROADMAP.md` (lines 93, 107) | 🟢 Meta-reference |
| Runtime variable (không hardcode) | 1 | `init_context.py` (line 254) | 🟢 `{exploration_path.resolve()}` |

**Vị trí cần fix (blocking):**

```yaml
# /home/stveve/Documents/washvn/WASHVN/skills/ver-0.0.2/ROADMAP.md
# Line 4:
- [Source of Truth](file:///home/steve/Work-space/WASHVN/skills/ver-0.0.2)  # ❌ hardcoded

# Line 5:
- [architecture.md](file:///home/steve/Work-space/WASHVN/architecture.md)  # ❌ hardcoded
- [standards.md](file:///home/steve/Work-space/WASHVN/standards.md)        # ❌ hardcoded

# Line 141:
- [standards.md](file:///home/steve/Work-space/WASHVN/standards.md)         # ❌ hardcoded
```

**Acceptance criterion:** `grep -r '/home/steve/Work-space' skills/ver-0.0.2/ returns 0` → hiện tại trả 3.

---

### 3.2 🔴 P0.2 — AGENTS.md Status

**Hiện trạng:**

```yaml
file: /home/stveve/Documents/washvn/WASHVN/skills/AGENTS.md  # (parent)
exists: true
size: 0 bytes
lines: 0
preview: ""
```

**Gap analysis:**

- `skills/CLAUDE.md` định nghĩa routing guide cho `skills/` directory với các thành phần quan trọng:
  1. **Crucial Rule** — bắt buộc cập nhật `skills-registry.json` khi thêm/bớt skill thuộc version chính thức
  2. **Folder structure mapping** — `ver-0.0.1` baseline + `ver-0.0.2` upgrade
  3. **Add/Remove skill workflow** — 7-Zone init + metadata + routing map update

- `AGENTS.md` cần mirror/duplicate `CLAUDE.md` content (hoặc tối thiểu L0 pointer dẫn về `CLAUDE.md` + `skills-registry.json` + `workspce_tree.md`).

- File hiện tại: **rỗng hoàn toàn** → vi phạm `Crucial Rule` vì thiếu routing anchor cho `skills/` subzone.

**Acceptance criterion:** File ≥ 200 bytes content → hiện tại 0 bytes.

**Sections bắt buộc phải có:**

```yaml
required_sections:
  - Header / Scope declaration (version, scope=skills/ directory)
  - Crucial Rule — Ecosystem Registry update mandate
  - Exceptions clause (non-versioned / experimental skills excluded)
  - Folder structure map (ver-0.0.1, ver-0.0.2, registry pointer)
  - Add Skill workflow (7-Zone init + metadata + routing map update)
  - Remove Skill workflow (delete dir + registry entry + routing map)
  - Pointer to skills-registry.json and workspce_tree.md
```

---

### 3.3 🔴 P0.3 — CASE System Duplication

**Hiện trạng:** 2 file trùng lặp đồng nhất 100%:

| File | Size | SHA1 (first 12 chars) | Skill |
|------|------|------------------------|-------|
| `_shared/knowledge/case-system.md` | 7372 bytes | `b71ca178ea5b` | shared |
| `skill-planner/knowledge/case-system.md` | 7372 bytes | `b71ca178ea5b` | skill-planner |

**Verification (re-checked 2026-06-17):** Identical SHA1 = `b71ca178ea5bb075e384face0cefac1e69e2274b` (rtk sha1sum) + identical size (7372 bytes) + identical first 20 lines. ✅

**Impact:**

```yaml
risks:
  - skill-planner pulls from _shared via knowledge/ symlink/copy instead of referencing it
  - versioning/routing inconsistencies between ver-0.0.1 and ver-0.0.2 baseline
  - drift risk — future edits to _shared copy will not propagate to skill-planner copy
```

**Recommendation:** Delete `skill-planner/knowledge/case-system.md` → archive tại `skill-planner/knowledge/.archive/case-system.md` → reference `_shared/knowledge/case-system.md` qua include hoặc symlink.

**Cross-references cần update sau dedup:**

- `skill-planner/SPEC.md` line 247 (tham chiếu local copy)
- `skill-planner/knowledge/case-system.md` line 61 (self-reference)

**Acceptance criterion:** `find -name 'case-system.md' returns 1 result` → hiện tại 2.

---

### 3.4 🟢 P0.4 — File Links Integrity

**Hiện trạng:** 3/3 links resolve thành công.

| File | Line | Link | Status |
|------|------|------|--------|
| `ROADMAP.md` | 4 | `file:///home/stveve/Documents/washvn/WASHVN/skills/ver-0.0.2` | 🟢 OK (self-link) |
| `ROADMAP.md` | 5 | `file:///home/stveve/Documents/washvn/WASHVN/architecture.md` | 🟢 OK |
| `ROADMAP.md` | 5 | `file:///home/stveve/Documents/washvn/WASHVN/standards.md` | 🟢 OK |
| `ROADMAP.md` | 141 | `file:///home/stveve/Documents/washvn/WASHVN/standards.md` | 🟢 OK |

**Note:** Self-link ở line 4 kỹ thuật valid nhưng kém thẩm mỹ — cân nhắc bỏ.

---

## 4. Gate P0 Status

```yaml
gate_status:
  P0.1: 🔴 FAIL  # 3 hardcoded /home/steve/Work-space/ paths còn trong ROADMAP.md
  P0.2: 🔴 FAIL  # AGENTS.md = 0 bytes (yêu cầu ≥200 bytes)
  P0.3: 🔴 FAIL  # case-system.md duplicate (yêu cầu 1 file)
  P0.4: 🟢 PASS  # 3/3 links OK
  overall: 🔴 FAIL
```

**Lý do fail từng gate:**

| Gate | Acceptance | Hiện tại | Kết luận |
|------|------------|----------|----------|
| P0.1 | 0 grep hit cho `/home/steve/Work-space` | 3 hits | 🔴 FAIL |
| P0.2 | AGENTS.md ≥ 200 bytes | 0 bytes | 🔴 FAIL |
| P0.3 | 1 file `case-system.md` duy nhất | 2 files identical | 🔴 FAIL |
| P0.4 | Tất cả file:// links resolve | 3/3 OK | 🟢 PASS |

---

## 5. Blocking Issues & Risk

### 5.1 Blocking Issues

```yaml
blocking:
  - id: P0.1
    desc: "3 hardcoded /home/steve/Work-space/ paths remain in skills/ver-0.0.2/ROADMAP.md (lines 4, 5, 141). Acceptance criterion requires 0 grep hits."
    fix_effort: 20 min

  - id: P0.2
    desc: "skills/AGENTS.md exists but is 0 bytes / 0 lines. Acceptance requires ≥200 bytes content. Empty file violates Crucial Rule from skills/CLAUDE.md."
    fix_effort: 15 min

  - id: P0.3
    desc: "case-system.md exists in 2 locations with identical SHA1 (b71ca178ea5b...) and 7.2K size — _shared/knowledge/case-system.md AND skill-planner/knowledge/case-system.md."
    fix_effort: 5 min
```

### 5.2 Risk Assessment

🟢 **Low risk overall.** Toàn bộ 3 failures là content/path issues, không phải architectural:

- Không thay đổi script logic
- Không thay đổi skill contract
- Fix hoàn toàn mechanical: text replacement (P0.1), file write (P0.2), file move+archive (P0.3)
- Drift risk trên CASE dedup đã mitigate vì `SKILL.md` đã point sang `_shared/` canonical path
- Hardcoded paths trong `ROADMAP.md` là documentation-only, không ảnh hưởng runtime behavior

### 5.3 Nice-to-haves (không blocking)

```yaml
nice:
  - "P0.4 self-link trên ROADMAP.md line 4 (file:///.../ver-0.0.2 pointing to its own dir) kỹ thuật valid nhưng kém thẩm mỹ — cân nhắc bỏ."
  - "dev-standards.md line 46 + quality-matrix.yaml line 288 dùng /home/steve/ làm anti-pattern example — acceptable nhưng cân nhắc sanitize thành /home/<user>/ cho portability."
  - "init_context.py line 254 dùng {exploration_path.resolve()} — runtime variable, không hardcode, nhưng cần verify không có string literal ở chỗ khác."
  - "skill-planner/SPEC.md line 247 + knowledge/case-system.md line 61 reference local copy paths — cần update sau dedup để point sang _shared/."
```

---

## 6. Action Plan (theo thứ tự ưu tiên)

### Step 1 — Dedup CASE System (5 min) 🔴

**Rationale:** Quick context-preserving fix — move duplicate vào `.archive/` trước khi remove để registry/SPEC.md links còn resolve được evidence.

```bash
# 1. Archive duplicate
mv /home/stveve/Documents/washvn/WASHVN/skills/ver-0.0.2/skill-planner/knowledge/case-system.md \
   /home/stveve/Documents/washvn/WASHVN/skills/ver-0.0.2/skill-planner/knowledge/.archive/case-system.md

# 2. Update cross-references
# skill-planner/SPEC.md line 247: ../_shared/knowledge/case-system.md
# skill-planner/knowledge/case-system.md line 61: ../_shared/knowledge/case-system.md

# 3. Verify
find /home/stveve/Documents/washvn/WASHVN/skills/ver-0.0.2 -name 'case-system.md'  # expect 1 result
```

### Step 2 — Create `skills/AGENTS.md` (15 min) 🔴

**Rationale:** Compliance với Crucial Rule trong `CLAUDE.md` + đạt gate P0.2 acceptance (≥200 bytes).

**Nội dung tối thiểu:**

```yaml
# skills/AGENTS.md — L0 Routing Anchor
- Header: Skills Directory Agent Guide vX.Y.Z
- Crucial Rule: skills-registry.json sync on add/remove
- Exceptions: non-versioned / experimental skills excluded
- Folder structure map: ver-0.0.1, ver-0.0.2, _shared
- Add/Remove workflow summary
- Links: skills/CLAUDE.md + skills-registry.json + workspce_tree.md
```

### Step 3 — Replace Hardcoded Paths (20 min) 🔴

**Rationale:** Low severity nhưng chặn gate P0.1 acceptance (0 hits required). 3 hits tất cả trong `ROADMAP.md` — anti-pattern docs ở `dev-standards/quality-matrix` là acceptable.

```bash
# Replace trong ROADMAP.md
/home/steve/Work-space/WASHVN/skills/ver-0.0.2  →  ./  (relative)
/home/steve/Work-space/WASHVN/architecture.md  →  ../../architecture.md
/home/steve/Work-space/WASHVN/standards.md     →  ../../standards.md

# Verify
grep -r '/home/steve/Work-space' /home/stveve/Documents/washvn/WASHVN/skills/ver-0.0.2/  # expect 0
```

### Step 4 — Update Phase 0 Evidence (10 min) ⬜

**Rationale:** Audit hardcoded paths + collect evidence cho 4 gates.

**File cần update:** `/home/stveve/Documents/washvn/WASHVN/.skill-context/ver-0.0.2/phase0-gate-report.md`

**Evidence cần thu thập:**

```yaml
P0.1:
  before: 3 hits trong ROADMAP.md
  after: 0 hits
  cmd: "grep -r '/home/steve/Work-space' skills/ver-0.0.2/"

P0.2:
  before: 0 bytes
  after: ≥200 bytes
  cmd: "wc -c skills/AGENTS.md"

P0.3:
  before: 2 files
  after: 1 file
  cmd: "find skills/ver-0.0.2 -name 'case-system.md'"

P0.4:
  status: 3/3 OK
  cmd: "link-checker hoặc manual verify"
```

### Step 5 — Update Registry & Routing (5 min) ⬜

**Rationale:** Sync skill count delta + case-system dedup metadata nếu version-pinned duplication được giữ intentional.

```yaml
# skills-registry.json — update metadata
ver-0.0.2:
  case-system:
    canonical: "_shared/knowledge/case-system.md"
    duplicates_archived: 1  # skill-planner/knowledge/.archive/

# workspce_tree.md — update routing map
case-system.md: _shared/knowledge/case-system.md  # canonical
```

---

## 7. Acceptance Checklist

| # | Criterion | Gate | Trạng thái | Verification |
|---|-----------|------|------------|--------------|
| 1 | 0 hardcoded `/home/steve/Work-space/` paths trong `skills/ver-0.0.2/` | P0.1 | 🔴 FAIL | `grep -r '/home/steve/Work-space' skills/ver-0.0.2/` |
| 2 | `skills/AGENTS.md` tồn tại với ≥200 bytes content | P0.2 | 🔴 FAIL | `wc -c skills/AGENTS.md` |
| 3 | `AGENTS.md` chứa 7 required sections (header, Crucial Rule, exceptions, folder map, add/remove workflow, links) | P0.2 | 🔴 FAIL | manual review |
| 4 | 1 file `case-system.md` duy nhất (canonical tại `_shared/`) | P0.3 | 🔴 FAIL | `find skills/ver-0.0.2 -name 'case-system.md'` |
| 5 | Archive tồn tại tại `skill-planner/knowledge/.archive/case-system.md` | P0.3 | ⬜ Pending | `ls skill-planner/knowledge/.archive/` |
| 6 | `skill-planner/SPEC.md` line 247 trỏ về `../_shared/knowledge/case-system.md` | P0.3 | ⬜ Pending | manual edit |
| 7 | 100% file:// links trong `ROADMAP.md` resolve thành công | P0.4 | 🟢 PASS | link checker |
| 8 | `phase0-gate-report.md` có evidence cho cả 4 sub-gates | Evidence | ⬜ Pending | file review |
| 9 | `skills-registry.json` metadata cập nhật cho case-system dedup | Registry | ⬜ Pending | JSON diff |
| 10 | `workspce_tree.md` routing map cập nhật canonical path | Routing | ⬜ Pending | file review |

**Tổng kết:** 1/10 PASS, 0/10 FAIL đã fix, 9/10 pending.

---

## 8. Recommended Next Step

🔴 **BLOCKER:** Phase 0 chưa PASS — **KHÔNG sync runtime** (`cp -r skills/ver-3/* .claude/skills/`) cho đến khi 3 blocking gates đạt.

**Sequential execution (ước tính 55 phút):**

1. **Step 1 — Dedup CASE** (5 min) → Verify: `find` trả 1 file
2. **Step 3 — Replace paths** (20 min) → Verify: `grep` trả 0 hits
3. **Step 2 — Create AGENTS.md** (15 min) → Verify: `wc -c` ≥ 200
4. **Step 4 — Update evidence report** (10 min) → Verify: 4/4 gates PASS trong report
5. **Step 5 — Update registry + routing** (5 min) → Verify: JSON diff + tree diff

**Sau khi tất cả 5 steps PASS:**

- Re-run gate verification tự động → expect `overall: PASS`
- Commit với message: `fix(phase0): dedup case-system, sanitize paths, add AGENTS.md anchor`
- Update `.skill-context/ver-0.0.2/` lifecycle status từ `pre-flight` → `gate-passed`
- Proceed to Phase 1 (Architect) hoặc sync runtime nếu đã ở giai đoạn deployment

---

**Report metadata:**

```yaml
generated_by: phase0-analysis-agent
input_sources:
  - P0.1 hardcoded paths scan
  - P0.2 AGENTS.md status check
  - P0.3 case-system dedup detection
  - P0.4 file links integrity check
  - gate verification orchestration
output_format: PHASE0-ANALYSIS.md (Vietnamese + English technical terms)
zones_affected:
  - skills/ver-0.0.2/ROADMAP.md
  - skills/AGENTS.md
  - skills/ver-0.0.2/skill-planner/knowledge/case-system.md
  - skills/ver-0.0.2/skill-planner/SPEC.md
  - skills-registry.json
  - workspce_tree.md
lifecycle_phase: pre-flight (gate verification)
summary_of_changes: "Identified 3 blocking gates (P0.1, P0.2, P0.3) requiring 55min of mechanical fixes before Phase 0 can PASS."
```
