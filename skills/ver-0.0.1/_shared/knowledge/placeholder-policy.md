---
name: placeholder-policy
description: "Canonical policy cho placeholder density — giải quyết mâu thuẫn giữa 6 giá trị hiện tại trong suite. Status: PROPOSAL (chưa enforce)."
type: rfc
status: proposed
version: "0.1.0-draft"
proposed_value: "0 (zero tolerance)"
scope: ver-3 Master Skill Suite
last_updated: "2026-06-02"
maintained_by: "Steve Void Team"
related_issues:
  - I4_placeholder_threshold_mismatch
---

# Placeholder Density Policy — Canonical RFC

> **Status:** 🟡 PROPOSAL (chưa enforce — đang chờ Steve review & quyết)
> **Mục đích:** Giải quyết mâu thuẫn 6 giá trị placeholder threshold đang tồn tại rải rác trong suite
> **Scope:** Tất cả production skills trong ver-3
> **Migration path:** Sau khi được approve, 6 file dưới sẽ được update để reference policy này

---

## 1. Vấn đề hiện tại (Problem Statement)

Suite ver-3 hiện có **6 quy tắc khác nhau** về placeholder density rải rác ở các file:

| # | Source | Quy định | Loại |
|---|--------|----------|------|
| 1 | `AGENTS.md §5` (root policy) | `placeholder_density: Phải = 0 để PASS` | HARD |
| 2 | `_shared/knowledge/framework.md §[BLD-09]` | `Mật độ placeholder < 5` | SOFT |
| 3 | `skill-builder/SKILL.md:71` (mission) | `placeholder count gate (< 5)` | SOFT |
| 4 | `skill-builder/SKILL.md:28` (must_not) | `leave placeholder density > 9` (tức OK 0-9) | SOFT |
| 5 | `_shared/schemas/verification.schema.json:93` | `semantic_placeholder_density == 0.0` | HARD |
| 6 | `skill-knowledge-miner/SKILL.md:83` | `100% không chứa placeholder` | HARD |

**Hệ quả:**
- Builder (`skill-builder`) không biết nên nghe quy tắc nào
- Validator (`schema_validator`, `check_status`) check threshold nào?
- Stakeholder review khó replicate được vì mỗi nơi đọc ra 1 giá trị khác
- Drift giữa docs (3) ↔ code contracts (1, 5) — root cause của I4

---

## 2. Đề xuất (Proposal)

### 2.1. Giá trị duy nhất: **Zero tolerance**

```yaml
canonical_threshold:
  value: 0
  unit: "semantic placeholders (TODO, FIXME, mock(), NotImplementedError, pass # placeholder)"
  enforcement: hard
  rationale: |
    - Đồng bộ với root policy (AGENTS.md §5) — single source of truth
    - Đồng bộ với verification schema (== 0.0) — production code phải clean
    - Phù hợp với "personal AI skill lab" — không phải production runtime
    - Tránh case-by-case judgement (mập mờ 0 vs 5 vs 9)
```

### 2.2. Tại sao KHÔNG chọn `< 5` hoặc `< 9`?

| Threshold | Ưu | Nhược |
|-----------|-----|-------|
| **0** (chọn) | Strict, dễ enforce, đồng bộ root | Có thể quá rigid cho edge case |
| **< 5** | Lenient, chừa buffer | Drift với root policy + schema |
| **< 9** | Hợp với skill-builder dual-rule | Tạo cảm giác "OK để có 5-9 placeholders" — không khuyến khích clean code |
| **Tri-tier 0/5/9** | Nuance | Phức tạp, khó test, dễ inconsistent |

### 2.3. Cơ chế phát hiện (Detection)

```yaml
placeholder_patterns:
  semantic:
    - "TODO"
    - "FIXME"
    - "XXX"
    - "TBD"
    - "// PLACEHOLDER"
    - "pass  # .*placeholder"
    - "mock\\(\\)"
    - "raise NotImplementedError"
  lexical:
    - "\\.\\.\\.\\s*$"            # dòng kết thúc bằng "..."
    - "xxxxxxxx+"                  # chuỗi x lặp
  measurement: "count per skill, NOT ratio"
  reason: "Ratio misleading với file ngắn — count tuyệt đối thì an toàn hơn"
```

### 2.4. Enforcement (khi policy được DECIDED)

```yaml
gate:
  pre_commit: "skill-builder must_not allow build nếu density > 0"
  pre_sync: "scripts/test_suite_workflow.py sẽ FAIL nếu phát hiện > 0"
  review: "production-code-reviewer sẽ block PR có placeholder"

exception_process:
  must: "Ghi rõ lý do trong exceptions.yaml với expiry date"
  must_not: "Exception vĩnh viễn"
```

---

## 3. Migration Plan (khi approve)

```yaml
migration_steps:
  step_1:
    file: "_shared/knowledge/placeholder-policy.md" (file này)
    action: "Đổi status: proposed → decided"
    
  step_2:
    files:
      - "skill-builder/SKILL.md:28"
      - "skill-builder/SKILL.md:71"
    action: "Đổi '> 9' → '> 0' và '< 5' → '≤ 0'; thêm link tới canonical"
    
  step_3:
    file: "_shared/knowledge/framework.md"
    action: "Thêm NOTE: 'Xem placeholder-policy.md cho canonical threshold'"
    
  step_4:
    file: "AGENTS.md §5"
    action: "Đã đúng (= 0) — chỉ thêm link tới canonical"
    
  step_5:
    file: "_shared/schemas/verification.schema.json"
    action: "Đã đúng (== 0.0) — chỉ thêm description reference"
    
  step_6:
    file: "skill-knowledge-miner/SKILL.md:83"
    action: "Đã đúng (100% no placeholder) — chỉ thêm link tới canonical"

verify_after_each_step: "python3 scripts/test_suite_workflow.py"
rollback: "Dùng .bak files; revert 1 step nếu fail"
```

---

## 4. Out of Scope (không xử lý ở RFC này)

```yaml
out_of_scope:
  - "Auto-fix tool (đề xuất thay thế placeholder thành real code) — RFC riêng"
  - "Per-domain threshold (vd: skill-explorer có thể cho phép < 5 vì exploratory work) — cần data"
  - "Test code placeholders (`# placeholder for test`) — cần làm rõ test vs prod boundary"
  - "Doc placeholder (`<placeholder-name>` template) — không phải semantic placeholder"
```

---

## 5. Acceptance Criteria (cho bản DECIDED)

```yaml
acceptance:
  - "Status changed: proposed → decided"
  - "Tất cả 6 file dưới đã reference canonical này"
  - "scripts/test_suite_workflow.py P7 PASS (đo count = 0 trên toàn suite)"
  - "Steve đã sign-off trong comment hoặc commit message"
```

---

## 6. References

```yaml
related:
  - "[[I4-placeholder-threshold-mismatch]]" # bug report
  - "[[AGENTS.md §5]]" # root policy
  - "[[framework.md §[BLD-09]]]" # framework rule
  - "[[verification.schema.json]]" # schema contract
  - "[[skill-builder/SKILL.md]]" # builder rules
  - "[[skill-knowledge-miner/SKILL.md]]" # miner rules
  - "[[scripts/test_suite_workflow.py]]" # P7 test
```

---

## 7. Decision Log

```yaml
decisions:
  - date: "2026-06-02"
    who: "Steve"
    decision: "Defer I4 — chỉ fix bugs trong ver-3"
    why: "Tách policy work khỏi bug fix work"
    next: "Tạo canonical RFC (file này) để giải quyết sau"
```

---

> **TL;DR:** Tôi đề xuất **0 placeholder** làm canonical, sẽ được apply sau khi bạn duyệt. Hiện tại không enforce — bạn có thể tự do sửa 6 file nếu muốn theo bất kỳ threshold nào, hoặc đợi quyết định policy rồi migrate một lần.
