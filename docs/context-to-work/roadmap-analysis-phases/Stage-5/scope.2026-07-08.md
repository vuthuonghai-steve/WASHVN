---
name: stage-5-scope
description: Scope document cho Stage 5 — Advanced Hooks Research & Evaluation (Phase 2: Hook Framework Foundation)
version: 0.1.0
suite: WASHVN
tags: [roadmap, phase-2, stage-5, advanced-hooks, prompt-hook, d2-9, d2-10, research, experimental, hook-heal, self-healing]
trace: [TỪ phase-2-plan.2026-07-07.md §4], [TỪ advanced-hooks-capability.2026-07-07.md], [TỪ phase-2-scope.2026-07-07.md §22-24], [TỪ 02-hook-framework.md §Design Principles], [TỪ hooks.md prompt-hook-fields], [TỪ BA GAP-5 metrics]
when_to_use: "Khi cần hiểu phạm vi, yêu cầu và rủi ro của Stage 5 — Advanced Hooks Research trước khi triển khai"
---

# Scope Document — Stage 5: Advanced Hooks Research & Evaluation

> **Phase:** Phase 2 — Hook Framework Foundation
> **Stage:** 5/5
> **Date:** 2026-07-08
> **Status:** Initial — Context Complete
> **Feature:** Prompt-based Hook Experiment (D2-9) + Advanced Hook Evaluation Report (D2-10)
> **Nature:** ⚠️ **EXPERIMENTAL — Research deliverable, không phải production**
> **Dependency:** Stage 1-4 có thể chạy song song — Stage 5 không block core deliverables

---

## §1: Tổng Quan Stage 5

### 1.1 Vị Trí Trong Phase 2

Phase 2 bao gồm 5 Stages, trong đó Stage 1-4 xây dựng **Layer 1 — Command-based hooks** (cơ học, bash+jq, <100ms, exit 2 blocking) và Stage 5 là **Layer 2 — Prompt/Agent-based hooks** (thông minh, LLM evaluation, self-healing với `continueOnBlock: true`).

| Stage | Focus | Layer | Nature |
|:-----:|:------|:-----:|:-------|
| Stage 1 | PreToolUse Gating Hooks (D2-1, D2-2, D2-4) | Layer 1 | Production |
| Stage 2 | Logging & Lifecycle Hooks (D2-3, D2-5, D2-6) | Layer 1 | Production |
| Stage 3 | Registry & Unit Tests (D2-7, D2-8) | Layer 1 | Production |
| Stage 4 | Verification (AC-1→AC-7) | Layer 1 | Production |
| **Stage 5** | **Advanced Hooks Research (D2-9, D2-10)** | **Layer 2** | **🧪 Experimental** |

### 1.2 Two-Layer Hook Design Principle

Kiến trúc hooks trong WASHVN được thiết kế theo hai lớp, như định nghĩa trong `02-hook-framework.md §Design principles`:

```yaml
layer_1_command_based:
  description: "Cơ học, phi ngữ nghĩa, tối giản — chốt chặn deterministic"
  characteristics:
    - "bash + jq"
    - "< 50 dòng code"
    - "< 100ms execution"
    - "Format B: exit 2 blocking"
    - "Chạy synchronous mỗi tool call (PreToolUse)"
    - "Không phụ thuộc LLM — không risk timeout/hallucination"
  deliverables:
    - "D2-1 → D2-6 (6 command hooks)"
    - "D2-7 registry.yaml"
    - "D2-8 test scripts (7 scripts)"

layer_2_prompt_agent_based:
  description: "Thông minh, suy luận ngữ nghĩa, self-healing — dùng LLM để đánh giá chất lượng"
  characteristics:
    - "LLM evaluation (Haiku/Sonnet)"
    - "30-120s timeout (chậm hơn nhiều so với Layer 1)"
    - "continueOnBlock: true (cơ chế self-healing)"
    - "Chỉ chạy ở mốc thưa thớt: Stop, SessionStart, TaskCompleted"
    - "output schema: {\"ok\": boolean, \"reason\": string}"
  deliverables:
    - "D2-9: Prompt Hook Experiment (Stop event — self-healing)"
    - "D2-10: Evaluation Report (feasibility + metrics)"
    - "3 test fixture files"
```

**Nguyên tắc thiết kế cốt lõi**:
- Layer 1 là **mandatory** — deterministic gate không thể bypass, bảo vệ cơ học
- Layer 2 là **optional** — semantic check cho quality assurance, không block pipeline nếu fail
- Cả 2 layer hoạt động **độc lập** — không blocking nhau
- Layer 2 chỉ dùng ở **Stop event** (thưa thớt) — **không dùng ở PreToolUse** (mỗi tool call)
- **Fail-safe**: Layer 2 fail → degrade gracefully, không block session

### 1.3 Stage 5 = Layer 2 Experiment

Stage 5 là bước đầu tiên đưa Layer 2 vào thực tế. Mục tiêu:

1. **Thiết lập** môi trường thử nghiệm Prompt-based Hook (D2-9) tại Stop event
2. **Đo lường** hiệu năng thực tế (latency, accuracy, self-healing) qua 60 cycles
3. **Đánh giá** feasibility của Agent-based hooks (HOOK-AUDIT-2.0) cho Phase 8
4. **Quyết định** có mở rộng Layer 2 cho PreToolUse trong tương lai hay không

### 1.4 Mối Quan Hệ Với Quality Gates

| Quality Gate | Liên Quan Stage 5 | Mô Tả |
|:-------------|:------------------|:------|
| **HOOK-HEAL-1.0** | ✅ D2-9 triển khai | Native Prompt-based Hook với continueOnBlock: true trên Stop event. Tự động audit MD format + YAML syntax, prompt agent tự sửa lỗi trước khi session kết thúc. |
| **HOOK-AUDIT-2.0** | 🔬 D2-10 đánh giá feasibility | Agent-based Hook trên Stop/TaskCompleted để chạy test suite. Chưa implement — D2-10 quyết định có triển khai Phase 8 không. |
| **YAML-RES-1.0** | 🔗 rule_9 last-mile verification | D2-9 là last-mile verification gate — phát hiện uncommitted/corrupted YAML state trước khi session exit. Kết hợp với D2-5 (L1 Syntax check). |
| **Γ-7** | 🔗 Gián tiếp | D2-9 self-healing loop có thể phát hiện và sửa corrupt state mà D2-5 chỉ backup. |

---

## §2: Entry Point & Tài Liệu Tham Chiếu

### 2.1 Entry Points

| Entry | Path | Ghi Chú |
|:------|:-----|:--------|
| Phase 2 Plan §4 Stage 5 | `docs/context-to-work/roadmap-analysis-phases/phase-2-plan.2026-07-07.md` | Task checklist D2-9 & D2-10 (line 311-358) |
| Advanced Hooks Capability | `docs/context-to-work/roadmap-analysis-phases/advanced-hooks-capability.2026-07-07.md` | Research doc — 145 dòng về Prompt/Agent hooks |
| Phase 2 Scope §22-24 | `docs/context-to-work/roadmap-analysis-phases/phase-2-scope.2026-07-07.md` | Cross-cutting context (Quality Gates, YAML Resilience, Design Principles) |
| Roadmap Spec | `skills/ver-3/roadmaps/02-hook-framework.md` | Task list item 10 (line 432-433), Design principles (line 34-44) |
| Official Hooks Doc | `.claude/knowleages/hooks/hooks.md` | Prompt hook fields (line 468-475), Settings locations (line 170-185), Stop event (line 2122-2221) |
| Quality Gates Ref | `Temps/spec/architects/shared/quality-gates-reference.md` | HOOK-HEAL-1.0 spec, YAML-RES-1.0 spec |
| YAML Resilience Layer | `Temps/spec/architects/P5-fallback-and-escalation/yaml-resilience-layer.md` | rule_9 last-mile verification, 3-level pre-check |
| BA Analysis | `docs/context-to-work/roadmap-analysis-phases/business-analysis-phase2-hook-framework.2026-07-07.md` | GAP-5 metrics quantification, Mâu thuẫn #3 continueOnBlock |
| Settings State | `.claude/settings.json` | Current state — chỉ có permissions block, chưa có hooks key |
| Gitignore | `.claude/.gitignore` | Hiện tại chỉ ignore `context-before-fix` và `knowleages` — chưa có `settings.local.json` |

### 2.2 Tài Liệu Tham Chiếu Chính

```yaml
reference_docs:
  phase_2_plan:
    path: "docs/context-to-work/roadmap-analysis-phases/phase-2-plan.2026-07-07.md"
    relevant_sections:
      - "§4: Stage 5 tasks chi tiết (line 311-358)"
      - "§9: settings.local.json configuration (line 506-555)"
      - "§10: BA Recommendations (GAP-5 metrics)"
  
  advanced_hooks_capability:
    path: "docs/context-to-work/roadmap-analysis-phases/advanced-hooks-capability.2026-07-07.md"
    relevant_sections:
      - "§2: Prompt-based hooks spec (type: prompt)"
      - "§3: Agent-based hooks spec (type: agent)"
      - "§4: ok:false behavior per event type"
      - "§5 Kịch Bản 1: Self-healing Stop hook"
      - "§6: Integration plan vào Phase 2"
  
  phase_2_scope:
    path: "docs/context-to-work/roadmap-analysis-phases/phase-2-scope.2026-07-07.md"
    relevant_sections:
      - "§22: Quality Gates — HOOK-HEAL-1.0, HOOK-AUDIT-2.0, YAML-RES-1.0"
      - "§23: YAML Resilience Layer — rule_9 mapping"
      - "§24: Two-layer design + D2-9/D2-10 detail"
      - "§14.2 note 7: Two-layer principle"
  
  official_hooks_doc:
    path: ".claude/knowleages/hooks/hooks.md"
    relevant_sections:
      - "line 170-185: Settings locations (5-level priority)"
      - "line 468-475: Prompt/agent hook fields"
      - "line 2122-2221: Stop event — input, decision control, continueOnBlock"
      - "line 591-635: Input JSON schema"
  
  roadmap_spec:
    path: "skills/ver-3/roadmaps/02-hook-framework.md"
    relevant_sections:
      - "line 34-44: Design principles — two-layer gating"
      - "line 432-433: Task 10 — Advanced Hooks Research"
      - "line 437-452: Definition of done (prompt-based hook experiment)"
```

---

## §3: Scope Definition

### 3.1 In Scope

```yaml
in_scope:
  deliverables:
    - "D2-9: Prompt-based Hook Experiment (HOOK-HEAL-1.0) — Stop event, self-healing"
    - "D2-10: Advanced Hook Evaluation Report — metrics, feasibility, recommendations"
    - "3 test fixture files tại .claude/hooks/tests/fixtures/"
    - "Test harness cho experiment execution (shell script)"
    - "1 evaluation report tại docs/context-to-work/roadmap-analysis-phases/"
  
  configuration:
    - "Thiết lập .claude/settings.local.json với hooks config (Stop event, type: prompt)"
    - "Bổ sung settings.local.json vào .claude/.gitignore"
    - "Xác nhận merge behavior: settings.local.json → shallow merge hooks object"
  
  experimental_design:
    - "3 fixtures × 2 models (Haiku + Sonnet) × 10 cycles = 60 evaluations"
    - "Self-healing loop test: block → reason → repair → re-evaluate"
    - "continueOnBlock: true behavior verification"
    - "Max 2 self-healing cycles per evaluation"
  
  metrics_collection:
    - "Latency: P50/P95/P99 cho Haiku vs Sonnet"
    - "Accuracy: overall rate per model"
    - "False positive rate: block legitimate doc"
    - "False negative rate: miss corrupt doc"
    - "Self-healing: success rate, avg cycles, avg cycle time"
  
  documentation:
    - "Scope document này (docs/Stage-5/scope.2026-07-08.md)"
    - "D2-10 evaluation report output"
```

### 3.2 Out of Scope

```yaml
out_of_scope:
  - "KHÔNG implement Agent-based hooks (type: agent) — chỉ research, defer Phase 8"
  - "KHÔNG implement Prompt-based hooks ở PreToolUse event — chỉ Stop event"
  - "KHÔNG sửa .claude/settings.json — chỉ dùng settings.local.json"
  - "KHÔNG deploy hooks vào runtime settings của Claude Code"
  - "KHÔNG reconcile hook format gap (exit 2 vs stdout JSON) — defer Phase 8"
  - "KHÔNG modify subagent-forge.md inline hooks"
  - "KHÔNG modify registry.yaml (D2-7 là Stage 3 deliverable)"
  - "KHÔNG modify suite_config.yaml, architecture.md"
  - "KHÔNG tạo skill, agent, schema mới"
  - "KHÔNG sửa knowledge docs"
  - "KHÔNG build production tooling từ kết quả — chỉ research và báo cáo"
  - "KHÔNG xóa file hiện có"
```

### 3.3 Boundary & Constraints

```yaml
boundary:
  event: "Stop event only — không PreToolUse, PostToolUse, SessionStart"
  config_file: ".claude/settings.local.json — KHÔNG settings.json"
  hook_type: "type: prompt — không type: agent, không type: command"
  execution: "Research parallel — không block Stage 1-4 core deliverables"
  output: "Evaluation report — không production tooling"
  
constraints:
  - "Prompt hook timeout: mặc định 30s, D2-9 set 45s"
  - "Agent hook timeout: mặc định 60s — không dùng trong Stage 5"
  - "continueOnBlock: true — non-blocking, session không bị block"
  - "Haiku (fast model) dùng cho experiment chính"
  - "Sonnet dùng cho comparison benchmark"
  - "Token cost: mỗi prompt hook call tốn token (Haiku rẻ, Sonnet đắt hơn)"
  - "Stop event không support matcher — luôn fire"
```

---

## §4: D2-9 — Prompt-based Hook Experiment (HOOK-HEAL-1.0)

### 4.1 Tổng Quan

D2-9 là thử nghiệm Prompt-based Hook tại Stop event, nhằm kiểm tra khả năng **self-healing** của Claude Code: LLM đánh giá cấu trúc documentation, phát hiện lỗi, và feed reason ngược lại agent để tự sửa trước khi session kết thúc.

**Mã hiệu quality gate**: HOOK-HEAL-1.0
**Tên**: D2-9: Prompt-based self-healing hook — verify MD/YAML structural completeness on Stop event
**Event**: `Stop`
**Handler type**: `"prompt"`
**Model mặc định**: `claude-3-5-haiku` (fast model)
**Timeout**: 45 giây
**continueOnBlock**: `true`

### 4.2 File Configuration: `.claude/settings.local.json`

**Vị trí**: `.claude/settings.local.json` (project-local, gitignored)

Cấu hình mẫu đầy đủ:

```json
{
  "hooks": {
    "Stop": [
      {
        "handlers": [
          {
            "type": "prompt",
            "prompt": "Evaluate the structural completeness of workspace documentation before session closure. Event context: $ARGUMENTS. Check for: (1) valid YAML frontmatter with all required fields (name, version, suite, tags), (2) well-formed Markdown structure (no broken tables, no unterminated code fences), (3) no dangling TODO or placeholder patterns in documentation files. Return JSON matching this schema: {\"ok\": boolean, \"reason\": string}",
            "model": "claude-3-5-haiku",
            "timeout": 45,
            "continueOnBlock": true,
            "description": "D2-9: Prompt-based self-healing hook — verify MD/YAML structural completeness on Stop event (HOOK-HEAL-1.0)"
          }
        ]
      }
    ]
  }
}
```

### 4.3 Prompt Content — 3 Check Categories

Prompt gửi tới LLM yêu cầu kiểm tra 3 categories:

#### Category 1: YAML Frontmatter Completeness

| Check | Mô Tả | File Targets |
|:------|:------|:-------------|
| C1.1 | YAML frontmatter tồn tại (bắt đầu bằng `---`) | `.md` files |
| C1.2 | Required fields present: `name`, `version` (pattern: `\d+\.\d+\.\d+`), `suite` (value: WASHVN), `tags` (non-empty array) | SKILL.md, scope documents |
| C1.3 | YAML syntax valid (no unterminated strings, no tab indentation) | All `.md` + `.yaml` files |
| C1.4 | `version` field matches semver format (X.Y.Z) | SKILL.md, design.md |
| C1.5 | `when_to_use` field present và không rỗng (nếu là skill) | SKILL.md |

#### Category 2: Markdown Structure Validity

| Check | Mô Tả |
|:------|:------|
| C2.1 | Code fences có matching closing (`` ``` `` hoặc ` ``` ``) |
| C2.2 | Tables có đúng số cột (header align row khớp với separator row) |
| C2.3 | Headers không bị broken (có space sau `#`, không empty header) |
| C2.4 | Unclosed HTML tags (nếu dùng) |
| C2.5 | Lists (numbered/bullet) có indent nhất quán |
| C2.6 | Clickable links không bị wrap trong backticks (lỗi LLM phổ biến) |

#### Category 3: Placeholder Detection

| Check | Mô Tả |
|:------|:------|
| C3.1 | Dangling `TODO:` / `FIXME:` / `HACK:` patterns |
| C3.2 | `pass` statements (Python stubs) |
| C3.3 | `// TODO` comments trong code blocks |
| C3.4 | Empty `{}` objects hoặc `[]` arrays không có comment giải thích |
| C3.5 | Mock implementations (`mock()`, `stub`, `placeholder`) |

### 4.4 Response Schema

LLM bắt buộc phải trả về JSON với schema sau:

```json
{
  "ok": true,
  "reason": "All documentation files pass structural checks. No issues found."
}
```

Hoặc khi phát hiện lỗi:

```json
{
  "ok": false,
  "reason": "Found 3 issues: (1) docs/example.md: missing YAML frontmatter 'name' field; (2) docs/guide.md: unterminated code fence at line 45; (3) SKILL.md: contains TODO placeholder at line 12."
}
```

**Chi tiết schema**:

| Field | Type | Required | Mô Tả |
|:------|:-----|:--------:|:------|
| `ok` | boolean | ✅ | `true` = documentation clean, `false` = cần sửa |
| `reason` | string | ✅ (khi `ok: false`) | Mô tả chi tiết lỗi, vị trí file:line, gợi ý sửa |
| `issues` | array | Optional | Array of issue objects (mỗi issue có file, line, type, description) |
| `issues[].file` | string | Optional | File path chứa lỗi |
| `issues[].line` | number | Optional | Line number |
| `issues[].type` | string | Optional | `yaml`, `md_structure`, `placeholder` |
| `issues[].description` | string | Optional | Mô tả lỗi |

> **Lưu ý**: Claude Code runtime chỉ xử lý `ok` và `reason`. Các field phụ (`issues[]`) không được runtime sử dụng nhưng có ích cho D2-10 evaluation.

### 4.5 `continueOnBlock` Behavior

`continueOnBlock: true` là cơ chế self-healing cốt lõi của HOOK-HEAL-1.0:

```yaml
continueOnBlock_behavior:
  value: true
  
  flow:
    - "1. Stop event fires — prompt hook gửi prompt tới LLM"
    - "2. LLM trả về {\"ok\": false, \"reason\": \"...\"}"
    - "3. Claude Code runtime đọc reason string"
    - "4. Runtime FEED reason vào context của agent (turn tiếp theo)"
    - "5. Agent NHÌN thấy reason và TỰ ĐỘNG sửa lỗi"
    - "6. Sau khi sửa, Stop event fire lại (stop_hook_active: true)"
    - "7. Prompt hook chạy lại — nếu ok: true → session kết thúc"
    - "8. Nếu vẫn ok: false → lặp lại (max 2 cycles)"
  
  max_cycles: 2
  # Sau 2 cycles liên tiếp ok:false, runtime force-close session
  
  safety:
    - "8 consecutive blocks max — Claude Code override và kết thúc turn"
    - "stop_hook_active: true sau lần block đầu — tránh infinite loop"
    - "continueOnBlock: true KHÔNG block session — non-blocking by design"
  
  khác_voi_continueOnBlock_false:
    - "false: block reason logged → session continues WITHOUT action"
    - "true: block reason fed back → agent tự sửa → retry completion"
```

### 4.6 Merge Behavior (Settings Resolution)

**CẢNH BÁO**: Shallow merge tại object key level. Nếu `settings.json` sau này có `hooks` key, `settings.local.json`'s `hooks` sẽ **replace hoàn toàn** — không deep-merge handler-level.

```yaml
settings_resolution:
  priority_levels:
    - level: 1 (lowest)
      file: "~/.claude/settings.json"
      scope: "User-wide"
      behavior: "Overridden by project-level"
    
    - level: 2
      file: ".claude/settings.json"
      scope: "Project base"
      behavior: "Overridden by settings.local.json"
    
    - level: 3
      file: ".claude/settings.local.json"
      scope: "Project local"
      behavior: "WINS on same key — hooks object REPLACE hoàn toàn"
    
    - level: 4
      file: "Plugin hooks (hooks/hooks.json)"
      scope: "Plugin-scoped"
      behavior: "Overrides local"
    
    - level: 5 (highest)
      file: "Skill/Agent frontmatter"
      scope: "Per-component"
      behavior: "Highest priority"
  
  merge_warning:
    - "settings.local.json hooks → REPLACE settings.json hooks object"
    - "Không merge từng handler — nếu settings.json có PreToolUse hooks"
    - "và settings.local.json chỉ có Stop hooks → settings.json PreToolUse hooks"
    - "sẽ bị MẤT khi settings.local.json active"
    - "Trong Phase 2, settings.json chưa có hooks key → không ảnh hưởng"
```

### 4.7 Các Tham Số Cấu Hình Chi Tiết

| Field | Required | Value cho D2-9 | Ghi Chú |
|:------|:--------:|:---------------|:--------|
| `type` | ✅ Required | `"prompt"` | Loại handler |
| `prompt` | ✅ Required | LLM instruction với 3 check categories + $ARGUMENTS | Xem §4.3 cho nội dung đầy đủ |
| `model` | ❌ Optional | `"claude-3-5-haiku"` | Omit = default model (cũng là fast model) |
| `timeout` | ❌ Optional (default: 30s) | `45` | Tăng từ 30s lên 45s do prompt dài 3 categories |
| `continueOnBlock` | ❌ Optional (default: false) | `true` | Self-healing enabled |
| `description` | ⭐ Strongly recommended | Diagnostic label cho `/hooks` menu | Hiển thị trong hook browser |
| `event` | Implied by parent key | Omitted | Key `"Stop"` xác định event |
| `matcher` | Optional (Stop không hỗ trợ) | Omitted | Stop event không support matcher |

### 4.8 3 Test Fixture Files

Tạo 3 test fixture files tại `.claude/hooks/tests/fixtures/` để mô phỏng các kịch bản:

#### Fixture 1: `test-SKILL-valid.md`

**Mục đích**: File hợp lệ — frontmatter đầy đủ, MD structure đúng, không placeholder

```yaml
---
name: test-skill-valid
description: A valid test skill with complete frontmatter
version: 1.0.0
suite: WASHVN
tags: [test, valid]
when_to_use: "Use for testing valid markdown parsing"
---
```

Nội dung MD hợp lệ:

~~~markdown
# Test Skill Valid

This is a valid skill file for testing.

## Installation

Run the following command:

`bash
npm install test-skill-valid
`

## Usage

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `option`  | bool | `false` | Enable feature |
| `name`    | str  | `"world"` | Greeting target |

> **Note**: This is a valid blockquote.
~~~

**Dự kiến kết quả**: `ok: true`

#### Fixture 2: `test-SKILL-corrupt.md`

**Mục đích**: File corrupt — YAML syntax lỗi + MD structure lỗi

```yaml
---
name: test-skill-corrupt
description: "Corrupt test file with multiple issues
version: 1.0.0   # Thiếu dấu " đóng ở description
suite: WASHVN
tags: [test, corrupt
when_to_use: "Use for testing corrupt file detection"
```

Nội dung MD corrupt:

~~~markdown
# Test Skill Corrupt

This file has multiple structural issues.

## Unclosed Code Fence

`python
def hello():
    print("hello")
`  <!-- Thiếu closing mark -->

## Broken Table

| Header 1 | Header 2 |
|----------|----------|
| Cell 1  | Cell 2
| Cell 3  | Cell 4 |  <!-- Thiếu pipe ở row 1 -->

## TODO Placeholder

TODO: implement this section
~~~

**Dự kiến kết quả**: `ok: false, reason: "..."` — phát hiện ít nhất:
- YAML syntax error (unterminated string)
- Unterminated code fence
- Broken table
- TODO placeholder

#### Fixture 3: `test-SKILL-nofrontmatter.md`

**Mục đích**: Zero metadata — valid MD body nhưng không có YAML frontmatter

~~~markdown
# Test Skill No Frontmatter

This file has valid markdown structure but ZERO metadata.

## Features

- Clean markdown
- Proper code fences
`bash
echo "valid"
`
- Proper tables

| Col A | Col B |
|-------|-------|
| Data  | Data  |

> Clean blockquote.

## No Placeholders

All content is properly written.
~~~

**Dự kiến kết quả**: `ok: false, reason: "Missing YAML frontmatter — required fields: name, version, suite, tags"`

### 4.9 Test Harness Design

Script test harness: `.claude/hooks/tests/run-hook-experiment.sh`

**Mô tả**: Shell script tự động chạy experiment bằng cách pipe fixture content vào mô phỏng Stop event context và capture output.

**Logic xử lý**:

```
for each model in [haiku, sonnet]:
  for each fixture in [valid, corrupt, nofrontmatter]:
    for cycle in 1..10:
      1. Tạo mock Stop event JSON với fixture content
      2. Ghi vào stdin của prompt hook (mô phỏng)
         (Trong thực tế, cần chạy Claude Code session thật hoặc dùng API)
      3. Bắt đầu timer
      4. Ghi nhận response {ok, reason}
      5. Dừng timer → latency
      6. So sánh result với expected
      7. Ghi metrics vào CSV
```

> **⚠️ Hạn chế kỹ thuật**: Prompt hooks (`type: "prompt"`) chỉ chạy trong Claude Code runtime — không thể test bằng pipe stdin như command hooks. Test harness cần:
> - Cách 1 (khuyến nghị): Tạo Claude Code session thật với settings.local.json active → mở/ghi fixture → Stop event → capture output
> - Cách 2 (fallback): Dùng Anthropic API trực tiếp để mô phỏng LLM call với cùng prompt
> - Cách 3 (minimum): Verify cấu hình settings.local.json đúng format bằng Claude Code `/hooks` menu

**Output metrics file**: `.claude/hooks/tests/experiment-results.csv`

```
model,fixture,cycle,latency_ms,ok,expected_ok,match,self_heal_cycles,notes
haiku,valid,1,5234,true,true,true,0,clean pass
haiku,corrupt,1,7123,false,false,true,1,self-healed after 1 cycle
haiku,nofrontmatter,1,6891,false,false,true,1,self-healed after 1 cycle
sonnet,valid,1,12345,true,true,true,0,clean pass
sonnet,corrupt,1,15678,false,false,true,1,self-healed after 1 cycle
sonnet,nofrontmatter,1,14234,false,false,true,1,self-healed after 1 cycle
...
```

### 4.10 60-Cycle Evaluation Plan

```yaml
evaluation_plan:
  total_cycles: 60
  
  breakdown:
    - model: "claude-3-5-haiku"
      cycles_per_fixture: 10
      fixtures: [valid, corrupt, nofrontmatter]
      total: 30
      
    - model: "claude-sonnet-4"  # hoặc phiên bản mới nhất
      cycles_per_fixture: 10
      fixtures: [valid, corrupt, nofrontmatter]
      total: 30
  
  rationale:
    - "10 cycles per (model, fixture) pair → đủ để tính P50/P95/P99"
    - "2 models → so sánh Haiku (fast+cheap) vs Sonnet (accurate+expensive)"
    - "3 fixtures → valid + corrupt + nofrontmatter = full coverage"
  
  expected_duration:
    estimated: "~45-90 phút (tùy model và queue)"
    per_cycle_haiku: "~5-20s (P50 8s, P99 20s)"
    per_cycle_sonnet: "~10-28s (P50 15s, P99 28s)"
    self_healing_cycle: "~30-120s (block → repair → re-eval)"
  
  cost_estimate:
    haiku_30_cycles: "~$0.03-0.15 (rất rẻ)"
    sonnet_30_cycles: "~$0.30-1.50 (đắt hơn 10x)"
    total: "~$0.33-1.65 (không đáng kể)"
```

---

## §5: D2-10 — Evaluation Report Structure

### 5.1 Tổng Quan

**Output path**: `docs/context-to-work/roadmap-analysis-phases/advanced-hooks-evaluation.2026-07-08.md`

**Mục đích**: Báo cáo đánh giá toàn diện về Prompt-based Hook experiment, bao gồm metrics hiệu năng, self-healing performance, và feasibility assessment cho Agent-based hooks (HOOK-AUDIT-2.0) trong Phase 8.

### 5.2 Metrics Table — Latency

**Target thresholds**:

| Metric | Model | P50 Target | P95 Target | P99 Target | Unit |
|:-------|:------|:----------:|:----------:|:----------:|:----:|
| Response time | Haiku | ≤8 | ≤15 | ≤20 | seconds |
| Response time | Sonnet | ≤15 | ≤22 | ≤28 | seconds |
| Self-heal cycle | Haiku | ≤30 | ≤45 | ≤60 | seconds |
| Self-heal cycle | Sonnet | ≤45 | ≤60 | ≤90 | seconds |

**Bảng latency mẫu** (cần điền từ kết quả experiment):

| Fixture | Model | P50 | P95 | P99 | Mean | Min | Max | StdDev |
|:--------|:------|:---:|:---:|:---:|:----:|:---:|:---:|:------:|
| valid | Haiku | — | — | — | — | — | — | — |
| corrupt | Haiku | — | — | — | — | — | — | — |
| nofrontmatter | Haiku | — | — | — | — | — | — | — |
| valid | Sonnet | — | — | — | — | — | — | — |
| corrupt | Sonnet | — | — | — | — | — | — | — |
| nofrontmatter | Sonnet | — | — | — | — | — | — | — |

### 5.3 Metrics — Accuracy

**Target thresholds**:

| Metric | Haiku Target | Sonnet Target |
|:-------|:------------:|:-------------:|
| Overall Accuracy | ≥80% | ≥92% |
| S1 — Valid doc (expected ok: true) | ≥90% | ≥98% |
| S2 — Corrupt doc (expected ok: false) | ≥75% | ≥90% |
| S3 — No frontmatter (expected ok: false) | ≥75% | ≥88% |
| False Positive Rate | <10% | <5% |
| False Negative Rate | <15% | <8% |

**Confusion matrix mẫu** (cần điền):

| Actual → Predicted ↓ | Valid (ok) | Corrupt (!ok) | NoFront (!ok) |
|:---------------------|:----------:|:-------------:|:-------------:|
| Predicted ok: true | TP — | FP — | FP — |
| Predicted ok: false | FN — | TN — | TN — |

### 5.4 Metrics — Self-Healing Performance

**Target thresholds**:

| Metric | Target | Notes |
|:-------|:------:|:------|
| Self-healing success rate | ≥70% | % lần block được self-heal thành công (PASS sau ≤2 cycles) |
| Avg repair cycles | ≤2 | Số cycle trung bình để self-heal |
| Max repair cycles | 2 | Hard limit — force close sau 2 failures |
| Avg cycle time | ≤60s | Tổng thời gian block → repair → re-eval |
| Self-healing false recovery | <10% | % lần "healed" nhưng thực tế vẫn còn lỗi |

**Bảng self-healing mẫu**:

| Fixture | Model | Success Rate | Avg Cycles | Avg Time (s) | False Recovery |
|:--------|:------|:------------:|:----------:|:------------:|:--------------:|
| corrupt | Haiku | — | — | — | — |
| corrupt | Sonnet | — | — | — | — |
| nofrontmatter | Haiku | — | — | — | — |
| nofrontmatter | Sonnet | — | — | — | — |

### 5.5 Feasibility Assessment for Agent-based Hooks

D2-10 cần đánh giá feasibility của Agent-based hooks (HOOK-AUDIT-2.0) cho Phase 8:

```yaml
feasibility_assessment:
  agent_hook_type: "type: agent"
  target_event: "Stop hoặc TaskCompleted"
  use_case: "Chạy test suite sandbox + đọc logs + quyết định PASS/FAIL"
  
  evaluation_criteria:
    - "Latency: Agent hook timeout mặc định 60s (có thể config) — có chấp nhận được không?"
    - "Cost: Agent spawn subagent với 50 turns — token cost cao hơn prompt hook nhiều lần"
    - "Reliability: Agent hook experimental — behavior có thể thay đổi"
    - "Complexity: Agent cần Read/Grep files, chạy test commands — phức tạp hơn prompt nhiều"
    - "Integration: Cần bridge registry.yaml → settings.json (Phase 8 scope)"
  
  recommendations:
    proceed_phase_8: "Khuyến nghị: CÓ/KHÔNG — dựa trên kết quả D2-9 + assessment"
    conditions:
      - "Haiku accuracy ≥80% → đủ cho self-healing phase 8"
      - "Haiku accuracy <70% → cần Sonnet hoặc cải thiện prompt"
      - "Self-healing success <50% → không đáng tin cậy, cần thiết kế lại"
    notes:
      - "Agent hooks mạnh hơn nhưng đắt hơn và chậm hơn"
      - "Phase 8 nên ưu tiên prompt hooks expansion trước, agent hooks sau"
      - "PreToolUse prompt hooks KHÔNG khuyến nghị — latency không chấp nhận được"
```

### 5.6 Recommendations Section

Các recommendations cần có trong D2-10:

1. **Có mở rộng Layer 2 cho PreToolUse không?**
   - Khuyến nghị: **KHÔNG** — defer đến Phase 8 nếu cần
   - Lý do: latency >30s không chấp nhận được cho mỗi tool call

2. **Có implement Agent-based hooks trong Phase 8 không?**
   - Phụ thuộc vào D2-9 kết quả
   - Nếu Haiku accuracy ≥80% → đủ foundation
   - Nếu Sonnet accuracy ≥92% → có thể skip Haiku cho critical gates

3. **Cần optimize prompt không?**
   - Phân tích false positive/negative để tinh chỉnh prompt
   - Thêm few-shot examples nếu cần

4. **Cost-benefit analysis**
   - Haiku: rẻ, nhanh, accuracy thấp hơn
   - Sonnet: đắt hơn 10x, chậm hơn 2x, accuracy cao hơn
   - Khuyến nghị model dựa trên use case criticality

---

## §6: Settings Resolution Architecture

### 6.1 5-Level Priority

Theo official Claude Code hooks documentation (`hooks.md` line 170-185), settings được resolve theo 5 levels:

| Priority | File | Scope | Git? | Ví dụ |
|:--------:|:-----|:------|:----:|:------|
| 1 (thấp) | `~/.claude/settings.json` | User-wide | Local | Cấu hình cá nhân |
| 2 | `.claude/settings.json` | Project base | ✅ Commit | Cấu hình team |
| 3 | **`.claude/settings.local.json`** | **Project local** | ❌ Gitignore | **D2-9 config** |
| 4 | Plugin `hooks/hooks.json` | Plugin-scoped | ✅ | Plugin hooks |
| 5 (cao) | Skill/Agent frontmatter | Per-component | ✅ | Per-skill hooks |

### 6.2 Merge Behavior Warning

```yaml
merge_behavior:
  type: "Shallow merge — key-level, không deep-merge"
  
  example:
    - "settings.json có: {hooks: {PreToolUse: [...], PostToolUse: [...]}}"
    - "settings.local.json có: {hooks: {Stop: [...]}}"
    - "Kết quả: CHỈ Stop hooks active — PreToolUse và PostToolUse hooks MẤT"
  
  implication_cho_phase_2:
    - "settings.json HIỆN TẠI chưa có hooks key (chỉ permissions block)"
    - "settings.local.json sẽ tạo hooks.Stop — không conflict"
    - "Sau này nếu settings.json có hooks key, cần merge thủ công"
  
  best_practice:
    - "Luôn copy settings.json hooks sang settings.local.json khi cần cả 2"
    - "Hoặc dùng plugin hooks để tránh conflict"
    - "Hoặc dùng skill/agent frontmatter (cao nhất) cho per-skill hooks"
```

### 6.3 `.claude/settings.json` Current State

File hiện tại `.claude/settings.json` chỉ có permissions block, chưa có hooks key:

```json
{
  "permissions": {
    "allow": [
      "Read",
      "Glob",
      "Grep",
      "Bash(validate_suite_integrity.py)"
    ],
    "deny": [
      "Bash(rm -rf *)"
    ]
  }
}
```

**Kết luận**: Hiện tại không conflict — settings.local.json có thể safely tạo `hooks.Stop` key.

### 6.4 `.claude/.gitignore` Check

Hiện tại `.claude/.gitignore` chỉ ignore:

```
context-before-fix
knowleages
```

**Cần bổ sung**: `settings.local.json` — mặc dù Claude Code tự động gitignore file này khi tạo, cần verify.

---

## §7: Impact Analysis

### 7.1 Files Created

```yaml
files_created:
  - path: ".claude/settings.local.json"
    description: "D2-9: Prompt Hook experiment config (Stop event, type:prompt, continueOnBlock:true)"
    format: "JSON"
    estimated_size: "~25 dòng"
    
  - path: ".claude/hooks/tests/fixtures/test-SKILL-valid.md"
    description: "Test fixture — valid frontmatter + MD structure"
    format: "Markdown + YAML frontmatter"
    estimated_size: "~40 dòng"
    
  - path: ".claude/hooks/tests/fixtures/test-SKILL-corrupt.md"
    description: "Test fixture — corrupt YAML + MD errors"
    format: "Markdown + YAML frontmatter (intentionally broken)"
    estimated_size: "~40 dòng"
    
  - path: ".claude/hooks/tests/fixtures/test-SKILL-nofrontmatter.md"
    description: "Test fixture — no frontmatter, valid MD body"
    format: "Markdown (no YAML)"
    estimated_size: "~30 dòng"
    
  - path: ".claude/hooks/tests/run-hook-experiment.sh"
    description: "Test harness — script chạy 60-cycle experiment và collect metrics"
    format: "Shell script"
    estimated_size: "~80 dòng"
    
  - path: "docs/context-to-work/roadmap-analysis-phases/advanced-hooks-evaluation.2026-07-08.md"
    description: "D2-10: Evaluation report — latency, accuracy, self-healing, feasibility"
    format: "Markdown + YAML + tables"
    estimated_size: "~200-300 dòng"
```

### 7.2 Files Modified

```yaml
files_modified:
  - path: ".claude/.gitignore"
    description: "Bổ sung 'settings.local.json' để đảm bảo gitignore"
    change: "Append line: settings.local.json"
```

### 7.3 Files Referenced (Read-Only)

```yaml
files_referenced:
  - path: ".claude/settings.json"
    reason: "Check current state — không có hooks key, không conflict"
  - path: ".claude/knowleages/hooks/hooks.md"
    reason: "Reference cho prompt hook fields, settings resolution, Stop event"
  - path: "skills/ver-3/roadmaps/02-hook-framework.md"
    reason: "Design principles, task list item 10"
  - path: "Temps/spec/architects/shared/quality-gates-reference.md"
    reason: "HOOK-HEAL-1.0, HOOK-AUDIT-2.0 spec"
  - path: "Temps/spec/architects/P5-fallback-and-escalation/yaml-resilience-layer.md"
    reason: "rule_9 last-mile verification context"
```

### 7.4 Không Ảnh Hưởng

```yaml
not_affected:
  - ".claude/hooks/events/*"          # Stage 1-2 deliverables — không sửa
  - ".claude/hooks/registry.yaml"     # Stage 3 — không sửa
  - ".claude/hooks/tests/test_*.sh"   # Stage 3 — không sửa (tạo mới fixtures/ riêng)
  - ".claude/knowledge/*"             # Phase 1 — không sửa
  - ".skill-context/*"                # State — không sửa
  - "raw/ver-3/*"                     # Skills — không sửa
  - "docs/context-to-work/*"          # Các scope docs khác — không sửa
```

---

## §8: Risk Assessment

| # | Rủi Ro | Khả Năng | Ảnh Hưởng | Biện Pháp Giảm Thiểu |
|:-:|:-------|:--------:|:----------:|:---------------------|
| R1 | **LLM timeout** — Prompt hook vượt 45s timeout | Trung bình | Thấp | `continueOnBlock: true` → session không bị block. Timeout fallback cho phép session kết thúc bình thường. |
| R2 | **False positive** — LLM block khi doc thực sự ok | Cao | Thấp | `continueOnBlock: true` → agent kiểm tra lại, nếu thực sự ok thì bỏ qua. Chỉ mất thêm 1 cycle. |
| R3 | **False negative** — LLM bỏ qua lỗi thực sự | Cao | Cao | D2-10 benchmark sẽ quantify rate. Nếu FN > 15%, cần Sonnet thay Haiku. Layer 1 (D2-5) vẫn detect corrupt YAML. |
| R4 | **Self-healing loop infinite** — agent không thể sửa lỗi | Thấp | Trung bình | Hard limit 2 cycles + 8 consecutive blocks cap từ Claude Code runtime. |
| R5 | **Token cost** — Haiku rẻ nhưng Sonnet đắt hơn 10x | Thấp | Thấp | 60 cycles = ~$0.33-1.65 — không đáng kể. Production nếu dùng Sonnet mỗi Stop = ~$0.01-0.05/call. |
| R6 | **settings.local.json merge conflict** — nếu settings.json có hooks key | Thấp | Cao | Hiện tại settings.json không có hooks key. Cần document merge behavior warning. |
| R7 | **Claude Code update thay đổi prompt hook behavior** | Thấp | Trung bình | Stage 5 là research — không production dependency. D2-10 sẽ capture version info. |
| R8 | **Prompt parsing lỗi** — LLM không trả về đúng JSON schema | Trung bình | Thấp | Claude Code runtime tự động xử lý JSON parse fail. Non-blocking error. |
| R9 | **Stop event không fire** — nếu user dùng Ctrl-C thay vì `/stop` | Thấp | Thấp | Official docs: Stop không fire khi user interrupt. Self-healing chỉ chạy khi session kết thúc bình thường. |
| R10 | **Experiment bias** — 3 fixtures không đại diện cho reality | Trung bình | Thấp | Fixtures design based on thực tế lỗi thường gặp. D2-10 sẽ note limitation. |

---

## §9: Acceptance Criteria (Stage 5 Specific)

| Mã AC | Tiêu Chí | Phương Pháp Xác Minh | Dự Kiến |
|:-----:|:---------|:---------------------|:-------:|
| **AC-5.1** | `.claude/settings.local.json` tồn tại với cấu hình hooks.Stop hợp lệ | `python3 -c "import json; c=json.load(open('.claude/settings.local.json')); assert 'hooks' in c and 'Stop' in c['hooks']"` | ✅ PASS |
| **AC-5.2** | settings.local.json có type: prompt, model: claude-3-5-haiku, timeout: 45, continueOnBlock: true | `python3 -c "import json; c=json.load(open('.claude/settings.local.json')); h=c['hooks']['Stop'][0]['handlers'][0]; assert h['type']=='prompt' and h['continueOnBlock']==True"` | ✅ PASS |
| **AC-5.3** | settings.local.json được gitignore | `grep 'settings.local.json' .claude/.gitignore` | ✅ PASS (sau khi thêm) |
| **AC-5.4** | 3 test fixtures tồn tại tại `.claude/hooks/tests/fixtures/` | `ls .claude/hooks/tests/fixtures/test-SKILL-*.md` | ✅ PASS |
| **AC-5.5** | Claude Code `/hooks` menu hiển thị hook với source "Local" | Chạy `/hooks` trong Claude Code session — verify có "Local" label | 🧪 Cần test |
| **AC-5.6** | Prompt-based Hook trả về ok:true cho valid fixture | Mô phỏng Stop event với valid doc → response.ok = true | 🧪 Cần test |
| **AC-5.7** | Prompt-based Hook trả về ok:false + reason cho corrupt fixture | Mô phỏng Stop event với corrupt doc → response.ok = false + reason có nội dung | 🧪 Cần test |
| **AC-5.8** | continueOnBlock: true feed reason vào agent context | Chạy thực tế → agent nhận reason và tự sửa lỗi | 🧪 Cần test |
| **AC-5.9** | Hoàn thành 60-cycle experiment | Kiểm tra experiment-results.csv có 60 rows + metrics | ✅ PASS |
| **AC-5.10** | D2-10 Evaluation Report published | File tồn tại tại docs/.../advanced-hooks-evaluation.*.md | ✅ PASS |
| **AC-5.11** | Feasibility assessment cho Agent-based hooks completed | Report có section feasibility + recommendation | ✅ PASS |
| **AC-5.12** | Token cost analysis included | Report có cost estimate per model per call | ✅ PASS |

---

## §10: Thứ Tự Build Khuyến Nghị

Stage 5 có thể chạy **độc lập và song song** với Stage 1-4. Các bước build:

```text
Step 1: Tạo 3 test fixtures
  → .claude/hooks/tests/fixtures/test-SKILL-valid.md
  → .claude/hooks/tests/fixtures/test-SKILL-corrupt.md
  → .claude/hooks/tests/fixtures/test-SKILL-nofrontmatter.md
  → Verify: content đúng format, có thể parse

Step 2: Bổ sung gitignore
  → Thêm 'settings.local.json' vào .claude/.gitignore
  → Verify: git check-ignore settings.local.json → yes

Step 3: Tạo settings.local.json
  → .claude/settings.local.json với hooks.Stop config
  → Verify: python3 parse → valid JSON
  → Verify: Claude Code /hooks menu show "Local" label

Step 4: Create test harness script
  → .claude/hooks/tests/run-hook-experiment.sh
  → Script mô phỏng experiment flow
  → Ghi metrics CSV

Step 5: Chạy 60-cycle experiment
  → 3 fixtures × 2 models × 10 cycles
  → Thu thập latency, accuracy, self-healing metrics
  → Ghi vào experiment-results.csv

Step 6: Phân tích kết quả
  → Tính P50/P95/P99 per (model, fixture)
  → Tính accuracy, FP rate, FN rate
  → Tính self-healing success rate, avg cycles

Step 7: Viết D2-10 Evaluation Report
  → Điền tất cả metrics tables
  → Feasibility assessment cho Agent-based hooks
  → Recommendations

Step 8: Review + kết luận
  → Verify tất cả AC-5.x đạt
  → Quyết định expand Layer 2 cho Phase 8
  → Archive kết quả
```

### Mối Quan Hệ Với Stage 1-4

```text
Timeline:
Stage 1: ████████░░░░░░░░░░░░  (PreToolUse gates)
Stage 2: ██████████░░░░░░░░░░  (Logging hooks)
Stage 3: ░░░░████████░░░░░░░░  (Registry + Tests)
Stage 4: ░░░░░░░░██████░░░░░░  (Verification)
Stage 5: ░░░░░░░░░░░░████████  (Research — parallel, không blocking)
         ↑ Phase 2 Start       ↑ Phase 2 End
```

- Stage 5 **không phụ thuộc** vào Stage 1-4 kết quả
- Stage 5 **có thể chạy song song** — không chờ Stage 1-4
- Stage 5 output (D2-10) là **input cho Phase 8 decision**, không phải Phase 2 completion

---

## §11: Experimental Nature Warning

> ⚠️ **CẢNH BÁO QUAN TRỌNG**: Stage 5 là RESEARCH — không phải production deliverable.

### 11.1 Những Điều Cần Hiểu Rõ

```yaml
experimental_nature:
  nature: "Research & Evaluation — không phải feature build"
  
  implications:
    - "Kết quả KHÔNG đảm bảo sẽ được dùng trong production"
    - "Metrics có thể dưới threshold — cần iteration ở Phase 8"
    - "Prompt-based hooks có behavioral changes qua Claude Code updates"
    - "Agent-based hooks (type: agent) là experimental — official docs ghi rõ 'may change'"
  
  success_criteria:
    minimum: "D2-10 report completed with all metrics collected"
    good: "Haiku accuracy ≥80%, self-healing ≥70%"
    excellent: "Sonnet accuracy ≥92%, recommend Phase 8 expansion"
  
  failure_modes:
    - "Accuracy <70% → prompt cần redesign"
    - "Self-healing <50% → continueOnBlock không hiệu quả"
    - "Latency >30s P50 → không practical cho bất kỳ use case nào"
    - "TOKEN cost >$0.10/call (Sonnet) → cần Haiku optimization"
```

### 11.2 Non-Blocking Guarantee

Stage 5 được thiết kế để **KHÔNG block** bất kỳ deliverable nào:

- KHÔNG block Phase 2 completion (Stage 1-4 là core deliverables)
- KHÔNG block Claude Code sessions (`continueOnBlock: true` là non-blocking)
- KHÔNG block user workflow (Stop event — thưa thớt, cuối session)
- KHÔNG require production deployment

### 11.3 Rollback Plan

Nếu D2-9 gây ra vấn đề:

```yaml
rollback:
  step_1: "Xóa .claude/settings.local.json"
  step_2: "Không cần restart — Claude Code tự động detect config change"
  step_3: "D2-10 report vẫn valid — đã capture metrics trước khi rollback"
  
  recovery_time: "< 1 phút"
  impact: "Không ảnh hưởng sessions khác — chỉ local config"
```

---

## §12: Các Vấn Đề Cần Lưu Ý (Open Questions)

| # | Question | Priority | Status | Được Trả Lời Bởi |
|:-:|:---------|:--------:|:------:|:-----------------|
| Q1 | **continueOnBlock có hoạt động đúng với Claude Code runtime hiện tại?** | High | 🔴 Cần test | AC-5.8 |
| Q2 | **Prompt có quá dài (3 categories)? Có cần split thành nhiều hooks?** | Medium | 🟡 Design review | D2-10 latency analysis |
| Q3 | **Sonnet accuracy có justify được cost cao hơn 10x không?** | Medium | 🟡 Cần data | D2-10 cost-benefit |
| Q4 | **Stop event có fire đủ thường xuyên để self-healing có ý nghĩa?** | Low | 🟢 Assumed | Official docs: fires mỗi turn |
| Q5 | **Agent-based hooks (type: agent) có stable trong Claude Code version hiện tại?** | High | 🔴 Experimental | Official docs: "Agent hooks are experimental and may change" |
| Q6 | **Token cost tracking — làm sao đo token consumption per hook call?** | Medium | 🟡 Chưa rõ | Cần dùng Anthropic API hoặc Claude Code logs |
| Q7 | **settings.local.json có cần thêm matcher? (Stop không support matcher)** | Low | 🟢 Resolved | Không cần — Stop luôn fire |
| Q8 | **Fixture files có cần nằm trong git tracking?** | Low | 🟢 Resolved | Có — test fixtures không chứa secrets. Nhưng settings.local.json thì không |
| Q9 | **Kết quả experiment có reproduce được không?** | Trung bình | 🟡 LLM nondeterministic | LLM response có thể khác nhau giữa các lần chạy. D2-10 cần note nondeterministic nature. |
| Q10 | **Có cần Auto Mode (bypassPermissions) testing riêng cho prompt hooks?** | Thấp | 🟢 Defer | Stop event không bị ảnh hưởng bởi permission mode. |
| Q11 | **MessageDisplay hook — có nên test thêm cho visual feedback?** | Thấp | 🟢 Ngoài scope | Stage 5 chỉ Stop event. MessageDisplay là optional research. |
| Q12 | **Cần bao nhiêu cycles để có statistical significance?** | Trung bình | 🟡 10 cycles/ pair | 10 cycles cho rough estimate. 30+ cycles cho statistical significance. Trade-off: time vs accuracy. |

---

## §13: Confidence Assessment

```yaml
overall_confidence: 75%

breakdown:
  config_readiness: 90%
    note: "Config schema rõ ràng từ official docs và phase-2-plan. settings.local.json format đã verified."
    
  experiment_design: 85%
    note: "3 fixtures × 2 models × 10 cycles = sound design. Prompt content có 3 categories rõ ràng."
    
  metrics_completeness: 80%
    note: "Latency, accuracy, FP, FN, self-healing đều có threshold. Token cost tracking chưa rõ."
    
  self_healing_feasibility: 70%
    note: "continueOnBlock behavior chưa được verify trên Claude Code runtime. Phụ thuộc LLM nondeterministic."
    
  agent_hook_feasibility: 50%
    note: "Agent hooks experimental — official docs ghi 'may change'. Không đủ data để đánh giá."
    
  risk_mitigation: 85%
    note: "All risks identified + mitigation plans. Non-blocking guarantee."
    
  dependency_ready: 100%
    note: "Không phụ thuộc Stage 1-4. Có thể chạy song song."

uncertainty_flags:
  - "continueOnBlock behavior CHƯA được verify trên Claude Code runtime cụ thể — cần test thực tế"
  - "Agent hooks (type: agent) là experimental — behavior có thể thay đổi bất kỳ lúc nào"
  - "LLM nondeterministic — kết quả experiment có variance giữa các lần chạy"
  - "Token tracking method chưa rõ — cần xác định cách đo"
  - "settings.local.json merge behavior warning — cần document rõ cho developer"
```

---

## §14: Tổng Kết

### 14.1 Stage 5 Summary

| Aspect | Detail |
|:-------|:-------|
| **Mục tiêu** | Nghiên cứu và đánh giá Layer 2 Prompt/Agent-based hooks cho WASHVN |
| **Layer** | Layer 2 — Semantic, LLM-based, self-healing |
| **Event** | Stop (chỉ event này) |
| **Deliverables** | D2-9 (experiment) + D2-10 (report) + 3 fixtures + harness |
| **Files created** | 5-6 files (~215 dòng code) |
| **Effort** | Small-Medium — 1 session |
| **Nature** | 🧪 **EXPERIMENTAL** — không production |
| **Blocking?** | ❌ KHÔNG — chạy song song Stage 1-4 |
| **Quality Gate** | HOOK-HEAL-1.0 (D2-9), HOOK-AUDIT-2.0 feasibility (D2-10) |
| **Phase 8 Input** | D2-10 quyết định có mở rộng Agent-based hooks không |

### 14.2 Decision Tree

Kết quả D2-10 quyết định hướng đi cho Phase 8:

```text
D2-10 Evaluation
│
├─ Haiku accuracy ≥80% AND self-healing ≥70%?
│  ├─ YES → Prompt hooks đủ tốt cho Phase 8
│  │  ├─ Mở rộng: thêm PreToolUse prompt hooks? → NO (latency)
│  │  └─ Agent hooks feasibility?
│  │     ├─ Dùng Agent hooks cho HOOK-AUDIT-2.0 test runner
│  │     └─ Cost-benefit acceptable? → Phase 8 decision
│  │
│  └─ NO → Cần optimize
│     ├─ Optimize prompt (few-shot examples, stricter instructions)
│     ├─ Dùng Sonnet thay Haiku (accuracy ≥92% target)
│     └─ Nếu vẫn <70% → redesign approach
│
└─ Document all findings + recommendations
```

### 14.3 Key Decisions Made

1. **Stop event only** — không PreToolUse (latency không chấp nhận được)
2. **type: prompt** — không type: agent (experimental, defer Phase 8)
3. **settings.local.json** — không sửa settings.json (gitignored, an toàn)
4. **continueOnBlock: true** — self-healing enabled, non-blocking
5. **Haiku primary, Sonnet comparison** — cost-effective experiment design
6. **10 cycles per pair** — trade-off: đủ cho rough estimate, không đủ cho statistical significance
7. **3 fixtures** — valid + corrupt + nofrontmatter = full coverage
8. **Non-blocking** — Stage 5 không block Phase 2 core deliverables
9. **Parallel execution** — có thể chạy cùng lúc với Stage 1-4

### 14.4 Cost-Benefit Tổng Quan

```yaml
cost:
  experiment_execution:
    haiku_30_cycles: "~$0.03-0.15"
    sonnet_30_cycles: "~$0.30-1.50"
    total_api_cost: "~$0.33-1.65"
  
  development_time:
    estimated: "1 session (~2-4 hours)"
    files_created: "5-6 files"
    lines_of_code: "~215 dòng"
  
  production_cost_per_stop_event:
    haiku_per_call: "~$0.001-0.005"
    sonnet_per_call: "~$0.01-0.05"

benefit:
  - "Phát hiện lỗi documentation trước khi commit"
  - "Tự động sửa lỗi MD/YAML không cần manual review"
  - "Foundation cho HOOK-AUDIT-2.0 agent-based test runner"
  - "Data-driven decision cho Phase 8 architecture"
  - "Zero risk to production — research only"
```

### 14.5 Final Notes

1. **Stage 5 là RESEARCH** — kết quả không đảm bảo sẽ vào production
2. **continueOnBlock: true** là cơ chế self-healing mạnh nhưng nondeterministic
3. **Agent-based hooks** còn experimental — official docs khuyến cáo thận trọng
4. **Cost consideration** — Haiku rẻ, Sonnet đắt hơn 10x, chọn model dựa trên criticality
5. **Merge behavior warning** — settings.local.json hooks REPLACE hoàn toàn hooks object từ settings.json
6. **Layer 1 vẫn là primary defense** — Layer 2 chỉ là semantic overlay
7. **Phase 8 sẽ quyết định** có mở rộng Layer 2 dựa trên D2-10 recommendations

---

**Document**: `docs/context-to-work/roadmap-analysis-phases/Stage-5/scope.2026-07-08.md`
**Generated by**: Sisyphus-Junior — context-before-fix pattern
**Language**: Tiếng Việt
**Version**: 0.1.0
**Date**: 2026-07-08
**Status**: Context Complete — Ready for Stage 5 Implementation

```
✓ §1: Tổng Quan Stage 5 — Two-Layer Design Principle, mối quan hệ quality gates
✓ §2: Entry Point & Tài Liệu Tham Chiếu — 8 entry points mapped
✓ §3: Scope Definition — in scope (8 items) + out of scope (11 items) + boundary
✓ §4: D2-9 — Prompt Hook Experiment — config, prompt, schema, fixtures, harness, 60-cycle plan
✓ §5: D2-10 — Evaluation Report Structure — metrics, feasibility, recommendations
✓ §6: Settings Resolution Architecture — 5-level priority, merge warning
✓ §7: Impact Analysis — files created (6), modified (1), referenced (5)
✓ §8: Risk Assessment — 10 risks với mitigation
✓ §9: Acceptance Criteria — 12 AC (AC-5.1 → AC-5.12)
✓ §10: Build Order — 8 steps, parallel execution confirmed
✓ §11: Experimental Nature Warning — non-blocking guarantee, rollback plan
✓ §12: Open Questions — 12 questions tracked
✓ §13: Confidence Assessment — 75% với uncertainty flags
✓ §14: Tổng Kết — decision tree, cost-benefit, final notes
```

**NO Code Changes Made** — Document only per context-before-fix guardrails
