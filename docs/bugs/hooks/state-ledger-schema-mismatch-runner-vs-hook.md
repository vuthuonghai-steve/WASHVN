# Bug Report — State Ledger: Schema Mismatch giữa Agent Contract vs validate-state-ledger.sh

- **Date:** 2026-07-11
- **Severity:** Medium (validation dead zone — không block pipeline, nhưng mất protection)
- **Status:** Resolved — verified on-disk 2026-07-11 (runner writes canonical `_state_ledger.yaml` with 6 required fields; ledger path whitelisted in PreToolUse gate L32-35)
- **Component:** `.claude/agents/ba-pipeline-runner.md` ↔ `.claude/hooks/validate-state-ledger.sh`
- **Branch:** `feat/architect-v1`
- **Phát hiện qua:** Phase 5 test — agent ghi `_ba_pipeline_state.yaml` (legacy) thay vì `_state_ledger.yaml` (canonical)

---

## 1. Symptom

`validate-state-ledger.sh` (PostToolUse hook) **không bao giờ kiểm tra** state file của BA pipeline.

Dù state file tồn tại và có YAML well-formed, hook bỏ qua vì:
- Hook chỉ match `_state_ledger.yaml`
- BA pipeline ghi `_ba_pipeline_state.yaml` (legacy naming)

→ Validation dead zone: malformed YAML / thiếu field trong BA state file không bị phát hiện → Λ-9 stage state leakage risk.

---

## 2. Root Cause

### 2a — File name mismatch

`validate-state-ledger.sh` dòng 17:
```bash
[[ "$FILE_PATH" =~ _state_ledger\.yaml$ ]]
```

Nhưng `ba-pipeline-runner` (cho đến commit fix hôm nay) ghi:
```
.skill-context/user-auth/_ba_pipeline_state.yaml
```

Hai tên khác nhau → hook skip → không validate.

### 2b — Schema field mismatch (kể cả khi tên file đúng)

Khi file tên đúng (`_state_ledger.yaml`), hook yêu cầu 6 required fields (`schema_validator.py` section):

```python
required = ["schema_version", "skill_name", "mode", "current_stage", "stage_status", "artifacts"]
```

Trong khi `ba-pipeline-runner` contract định nghĩa schema khác:

```yaml
# runner schema (task section)
feature_name: string
stages:
  elicitor: {status, artifact}
  analyst: {status, artifact}
  synthesizer: {status, artifact}
current_stage: string
status: string
```

| Field | Hook required | Runner schema |
|:------|:-------------|:--------------|
| `schema_version` | ✅ required | ❌ missing |
| `skill_name` | ✅ required | ❌ missing |
| `mode` | ✅ required | ❌ missing |
| `current_stage` | ✅ required | ✅ has |
| `stage_status` | ✅ required | ❌ missing (runner dùng `status`) |
| `artifacts` | ✅ required | ❌ missing (runner dùng `stages`) |
| `feature_name` | ❌ not required | ✅ has |
| `status` | ❌ not required | ✅ has |

→ **3/6 required fields missing** — hook sẽ block nếu file name đúng.

---

## 3. Impact

| Component | File name | Validator runs? | Would pass? |
|:----------|:----------|:---------------:|:-----------:|
| ba-pipeline-runner | `_ba_pipeline_state.yaml` | ❌ Skip (name) | ❌ Would fail (schema) |
| branch-orchestrator (Branch B) | `_state_ledger.yaml` | ✅ Match | ✅ Likely pass |
| pipeline-orchestrator | `_state_ledger.yaml` | ✅ Match | ⚠️ Cần verify |

---

## 4. Design Decision Required

Cần chọn 1 trong 2 hướng:

### Option A — Align runner → hook (recommended)

Runner áp dụng canonical schema (6 fields hook yêu cầu) + ghi file tên `_state_ledger.yaml`.

**Ưu:** Một schema duy nhất cho mọi pipeline. Hook hoạt động đồng nhất.
**Nhược:** Runner state ledger mất field `feature_name` và `stages/` — nhưng `feature_name` có thể ghi vào `artifacts` metadata, và `stages` trùng với `stage_status`.

**Runner schema mới:**
```yaml
schema_version: "1.0"
skill_name: ba-pipeline-runner
mode: ba-sub-pipeline
feature_name: user-auth        # extra field vẫn OK (hook chỉ check required)
current_stage: synthesizer
stage_status: completed
artifacts:
  elicitor: .skill-context/user-auth/ba-elicitor/elicitation-report.md
  analyst: .skill-context/user-auth/ba-analyst/analyst-output.md
  synthesizer: .skill-context/user-auth/ba-synthesizer/business-analysis.md
status: completed
```

### Option B — Mở rộng hook cho multiple schemas

Cho phép hook match nhiều tên file + nhiều schema per pipeline type.

**Ư:** Flexible, mỗi pipeline có schema riêng.
**Nhược:** Phức tạp, tăng technical debt. Hook không còn là single-source-of-truth.

---

## 5. Proposed Fix

### 5a — File name align

`ba-pipeline-runner.md` output_contract: ghi `_state_ledger.yaml` (đã fix trong bản rewrite).

`validate-state-ledger.sh`: thêm fallback cho legacy name (backward compat):

```bash
# BEFORE
[[ "$FILE_PATH" =~ _state_ledger\.yaml$ ]] || exit 0

# AFTER
[[ "$FILE_PATH" =~ _state_ledger\.yaml$ ]] || [[ "$FILE_PATH" =~ _ba_pipeline_state\.yaml$ ]] || exit 0
```

### 5b — Schema align

Áp dụng Option A: runner ghi đủ 6 required fields + extra fields tùy chọn.

Dùng YAML anchor pattern để tránh schema duplication giữa contract và runtime:
```yaml
# anchor
x-state-ledger-base: &state_ledger_base
  schema_version: "1.0"
  skill_name: ""
  mode: ""
  current_stage: ""
  stage_status: ""
  artifacts: {}

# concrete
schema_version: "1.0"
skill_name: ba-pipeline-runner
mode: ba-sub-pipeline
feature_name: user-auth
current_stage: synthesizer
stage_status: completed
artifacts:
  elicitor: .skill-context/user-auth/ba-elicitor/elicitation-report.md
  analyst: .skill-context/user-auth/ba-analyst/analyst-output.md
  synthesizer: .skill-context/user-auth/ba-synthesizer/business-analysis.md
status: completed
```

---

## 6. Verification

1. Run BA pipeline cho user-auth
2. Assert `_state_ledger.yaml` tồn tại và parse được
3. Run `validate-state-ledger.sh` inject: `FILE_PATH=.skill-context/user-auth/_state_ledger.yaml` → exit 0
4. Malformed inject (thiếu field): → block + reason message
5. Legacy file `_ba_pipeline_state.yaml` vẫn được hook check (backward compat)

---

## 7. Related

- **Bug linked:** `ba-pipeline-runner-state-write-conflict.md` (cùng component — state write block)
- **Λ-9 architectural defect:** Stage state leakage — hook được design để fix, nhưng validation dead zone làm fix vô hiệu
- **Cross-ref:** `validate-state-ledger.sh` là PostToolUse hook duy nhất compute-bound (parse YAML), token cost ≈ 0

---

*Phát hiện qua Phase 5 test — 3 artifacts PASS schema validation riêng lẻ, nhưng state ledger không được validate bởi hook.*
