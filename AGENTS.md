# AGENTS.md — Deep Work by Steve

> **Version:** 2.1 | **Updated:** 2026-05-27
> **Scope:** Root agent guide — L0 anchor rules + L1 working policy.
> Đọc file này đầu tiên. Tra cứu chi tiết tại Working Map bên dưới.

<instructions>
Luôn ưu tiên thay đổi an toàn. Workspace này là Personal AI Skill Lab — không phải production runtime codebase.
KHÔNG sửa trực tiếp `.hermes/skills/` — edit ở `skills/rebuild/` rồi sync qua skill-sync.
KHÔNG xóa skill context artifacts mà không archive.
KHÔNG di chuyển file mà không cập nhật routing maps.
</instructions>

---

## 1. Project Overview

**Đây là gì:** Personal AI Skill Lab + Knowledge Base để xây dựng và duy trì **Master Skill Suite** — bộ công cụ tạo, nâng cấp, quản lý và bảo trì Agent Skills cho Claude Code / AI agents.

**Mục tiêu:**
1. Tích lũy tri thức cá nhân → chuyển hóa thành Agent Skill chất lượng cao, reusable, production-ready
2. Phát triển 8-Stage pipeline: Explorer (Stage 0) → Knowledge Miner (Stage 0.5) → Architect (Stage 1) → Quality Gatekeeper (Stage 1.5) → Planner (Stage 2) → Builder (Stage 3) → Google Code Reviewer (Stage 3.5) → Sandbox Tester (Stage 4) → Indexer (Stage 5)
3. Quản lý vòng đời skill: `raw → designed → planned → built → verified → installed`
4. Áp dụng CASE System (Confidence-Aware Skill Execution) để kiểm soát chất lượng

**Người dùng:** Steve (Steve-claw#7410) + AI coding agents (Claude Code, Codex, Hermes, Antigravity)

---

## 2. Tech Stack

```yaml
tech_stack:
  primary_languages: [Markdown, YAML, Python, Bash]
  agent_runtimes:
    - Claude Code (.claude/skills)
    - Antigravity (.agents/skills)
    - Hermes agent (.hermes/skills/)
    - OMC/OMX agents (.omc/, .omx/)
  documentation_format: "Hybrid Markdown + YAML + XML-like tags (per standards.md)"
  knowledge_format: "LLM Knowledge Activation Standard (standards.md)"
  skill_format: "7-Zone structure (SKILL.md + knowledge/ + scripts/ + templates/ + data/ + loop/ + assets/)"
  versioning: "Semantic versioning per skill (YAML frontmatter)"
  validation: "schema_validator.py + Docker/gVisor sandbox"
```

---

## 3. Folder Structure

```text
WASHVN/                      ← Root workspace
├── AGENTS.md                ← [L0] Root agent guide (general rules + policy - file này)
├── CLAUDE.md                ← [L0] Root agent rules for Claude Code
├── architecture.md          ← Master Skill Suite architecture — 8 stages, CASE system, SCS Switcher
├── standards.md             ← LLM Knowledge Activation Standard — format rules
├── .gitignore               ← Configures ignored paths (.claude, .agents, raw)
│
├── .claude/                 ← Claude Code active workspace directory
│   ├── settings.json        ← Configures default permissions to bypassPermissions & active agent teams
│   ├── skills/              ← Active runtime skills (synced with raw/ver-3/)
│   └── knowledge/           ← High-fidelity documentation on Claude Code capabilities & custom skills
│
└── raw/
    └── ver-3/               ← Canonical ver-3 physical micro-skills source
        ├── _shared/         ← Shared schemas, validators, templates, fixtures
        ├── skill-explorer/
        ├── skill-knowledge-miner/
        ├── skill-architect/
        ├── production-quality-gatekeeper/
        ├── skill-planner/
        ├── skill-builder/
        ├── production-code-reviewer/
        ├── skill-security-reviewer/
        └── scripts/         ← Programmatic validation & suite integrity scripts
```

> **Routing nhanh:** Xem `architecture.md` để nắm cấu trúc 5 Layer / 8 Stage.

---

## 4. Commands

```yaml
commands:
  sync_skill:
    run: "cp -r raw/ver-3/* .claude/skills/"
    desc: "Sync các skills từ raw/ver-3 vào runtime .claude/skills/"

  validate_suite:
    run: "python3 .claude/scripts/validate_suite_integrity.py"
    desc: "Chạy script kiểm tra tính toàn vẹn của Master Skill Suite"

  view_architecture:
    run: "cat architecture.md"
    desc: "Xem 8-stage pipeline + CASE recovery + Acceptance Matrix"

  view_standards:
    run: "cat standards.md"
    desc: "Xem LLM Knowledge Activation format rules"
```

---

## 5. Code Style & Conventions

```yaml
conventions:
  skill_naming: "kebab-case (ví dụ: skill-architect, prompt-cleaner)"
  frontmatter: "YAML frontmatter bắt buộc: name, description, version: 0.0.1, suite: WASHVN, tags, when_to_use"
  language_in_instructions: "Imperative (Do X, Never Y — không dùng passive voice)"
  skill_file_limit: "SKILL.md tối đa 700 tokens (L0 anchor) — chi tiết chuyển sang knowledge/ hoặc policy/"
  format_rules:
    markdown: "Dùng cho explanation, architecture, rationale, onboarding"
    yaml: "Dùng cho constraints, policies, checklists, output_contract"
    xml_tags: "Dùng cho semantic boundaries (instructions, context, examples)"
  trace_tags: "Mọi task trong todo.md phải có trace: [TỪ DESIGN §N] hoặc [TỪ AUDIT TÀI NGUYÊN]"
  placeholder_rule: "ZERO placeholder trong production code (// TODO, pass, mock() = FAIL)"
```

---

## 6. Do's & Don'ts

```yaml
must:
  - Đọc CLAUDE.md và architecture.md để xác định đúng zone cần làm việc
  - Phát triển và edit skill ở raw/ver-3/ — KHÔNG sửa trực tiếp .claude/skills/
  - Chạy validate_suite_integrity.py trước khi đồng bộ hóa sang runtime
  - Viết YAML frontmatter đầy đủ cho mọi SKILL.md mới (gồm version: 0.0.1 và suite: WASHVN)
  - Xác định đầu ra động qua Dynamic Routing Contract (DRC) dưới .skill-context/ thay vì chạy script khởi tạo thủ công
  - Cập nhật danh sách đăng ký trong skills-registry.json mỗi khi bổ sung hoặc loại bỏ một skill thuộc về các phiên bản chính thức (bỏ qua các skill thử nghiệm bên ngoài)
  - Archive context artifacts trước khi xóa hoặc overwrite
  - Đảm bảo các thay đổi cấu trúc được cập nhật chính xác trong tài liệu kiến trúc và tệp đăng ký
  - Báo cáo summary_of_changes + zones_affected sau mỗi task

must_not:
  - Sửa trực tiếp các runtime skills trong .claude/skills/ — sử dụng workflow phát triển ở raw/ver-3/ rồi sync
  - Nhồi domain context vào AGENTS.md (file này) — chuyển sang docs/ hoặc knowledge/
  - Dùng placeholder (TODO, mock, pass) trong production skill code
  - Di chuyển file mà không cập nhật routing maps
  - Xóa .skill-context/ artifacts mà không archive evidence
  - Tạo skill mới mà không có design.md và criteria.md trước
```

---

## 7. Architecture Notes

> Chi tiết đầy đủ tại `architecture.md`. Dưới đây là quyết định cốt lõi đã được confirm — KHÔNG tranh luận lại.

**8-Stage Pipeline (Master Skill Suite ver-3.0.0):**

```text
Stage 0 Explorer  → sinh exploration.md + criteria.md
Stage 0.5 Miner   → khai thác tri thức đặc thù dự án
Stage 1 Architect → sinh design.md (7-Zone mapping, Mermaid diagrams)
Stage 1.5 Gatekeeper → chấm điểm & thẩm định thiết kế, sinh quality-matrix.yaml
Stage 2 Planner   → sinh todo.md (trace tags, DAG blocker map)
Stage 3 Builder   → build SKILL.md + src code (zero placeholder)
Stage 3.5 Reviewer → phân tích tĩnh code, sinh review-report.md
Stage 4 Tester    → chạy sandbox Docker/gVisor → sinh verification.md (PASS/FAIL)
Stage 5 Indexer   → sinh README.md + đăng ký vào llms.txt
```

**State Ledger:** `.skill-context/{skill-name}/` là persistent state giữa các stage stateless.

**CASE System:** Rollback tự động khi confidence < 85% hoặc validation FAIL → tạo `rollback_request.yaml`, archive state, notify developer.

**Staleness Policy:**
- < 7 ngày: tiếp tục từ checkpoint
- 7-30 ngày: cảnh báo, review todo.md trước
- > 30 ngày: force restart từ Stage 0

---

## 8. Testing Standards

```yaml
testing:
  framework: "Docker/gVisor sandbox (Stage 4 Tester)"
  minimum_test_cases: 2 kịch bản test cụ thể trong criteria.md
  placeholder_density: "Phải = 0 để PASS"
  validator: "schema_validator.py đối chiếu exploration.schema.yaml"
  evidence: "verification.md với kết quả PASS/FAIL rõ ràng"
  sandbox_isolation: "Mọi script kiểm thử chạy trong Docker biệt lập — KHÔNG chạy trực tiếp trên host"
  acceptance_gate:
    bad: "AI tự xác nhận Pass mà không chạy script thực tế"
    good: "100% kịch bản test từ criteria.md pass trong sandbox"
    premium: "Tích hợp kiểm thử hiệu năng + prompt injection defense"
```

---

## 9. Known Constraints & Limitations

```yaml
constraints:
  runtime_sync_required:
    desc: "Các custom skills của Claude Code hoạt động trong .claude/skills/ cần đồng bộ định kỳ"
    workaround: "Chỉnh sửa tại raw/ver-3/ rồi chạy cp -r raw/ver-3/* .claude/skills/"

  stateless_sessions:
    desc: "Mỗi agent stage là một session độc lập (stateless)"
    workaround: "Dùng .skill-context/{name}/ làm persistent state ledger"

  token_budget_l0:
    desc: "SKILL.md không được vượt 700 tokens (L0 anchor rule)"
    workaround: "Tách chi tiết sang knowledge/, policy/, scripts/"

  architure_typo:
    desc: "Lỗi typo tên file architecture.md"
    note: "Đã rename thành công file architure.md sang architecture.md"
    status: "Resolved (architecture.md is standardized)"

  raw_skills_unverified:
    desc: "raw/ver-3/ chứa các skills chưa kiểm chứng tự động toàn diện"
    workaround: "Chạy validate_suite_integrity.py định kỳ trước khi deploy"

  omx_unclear:
    desc: ".omx/ directory purpose chưa được document đầy đủ"
    status: "Open — chờ Steve clarify"
```

---

## 10. Quality Gates

```yaml
quality_gates:
  skill_production_checklist:
    - "YAML frontmatter đầy đủ: name, description, version: 0.0.1, suite: WASHVN, tags, when_to_use"
    - "SKILL.md ≤ 700 tokens (L0 anchor)"
    - "Có sections: Limitations + When not to use"
    - "Zero placeholders trong code/scripts"
    - "criteria.md có ≥ 5 tiêu chí nghiệm thu + ≥ 2 kịch bản test case"
    - "verification.md PASS từ sandbox"
    - "Đăng ký vào llms.txt sau khi verified"
    - "Cập nhật đăng ký trong skills-registry.json khi thêm/bớt skill thuộc các phiên bản chính thức"
    - "Update .skill-context/registry/README.md với lifecycle status"
    - "Thiết lập output_contract dạng YAML tuân thủ chuẩn Dynamic Routing Contract (DRC)"

  progressive_disclosure:
    - "SKILL.md chỉ chứa L0 anchor (instructions + routing map)"
    - "Chi tiết ở knowledge/, policy/, scripts/ — nạp on-demand"
    - "Root guide không làm kho tri thức"

  modularity:
    - "Mỗi skill có cấu trúc 7 Zones: core, knowledge, scripts, templates, data, loop, assets"
    - "Skill phải reusable độc lập với project cụ thể"

  versioning:
    - "Mọi skill bắt buộc có version: 0.0.1 và suite: WASHVN trong YAML frontmatter"
    - "Breaking changes phải có migration notes"
```

---

## Working Map

```yaml
load_when_needed:
  skill_framework_architecture: "architecture.md"
  documentation_format_standard: "standards.md"
  shared_schemas_validators: "raw/ver-3/_shared/"
  knowledge_base_index: ".claude/knowledge/README.md"
```

---

## Interaction Protocol

```yaml
agent_protocol:
  before_any_task:
    - Đọc CLAUDE.md và architecture.md để xác định đúng Zone cần làm việc
    - Xác định skill đang ở lifecycle phase nào (raw / designed / planned / built / verified / installed)
  before_editing_skill:
    - Nếu runtime (.claude/skills/): edit raw/ver-3/ → sync
    - Nếu new: tạo design.md + criteria.md trong .skill-context/{name}/
  during_editing:
    - Preserve SKILL.md contract (frontmatter, sections, 7 Zones structure)
    - Document build evidence trong build-log.md
    - Zero placeholder — nếu chưa implement được, dừng và notify
  before_final_response:
    - Verify routing map updated nếu có thay đổi structure
    - Report: summary_of_changes + zones_affected + lifecycle_phase_changed
```

---

## 11. Karpathy-Inspired Coding Guidelines

Behavioral guidelines to reduce common LLM coding mistakes (caution over speed):

### 1. Think Before Coding
- **Don't assume. Don't hide confusion. Surface tradeoffs.**
- State assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them — don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop. Name what's confusing. Ask.

### 2. Simplicity First
- **Minimum code that solves the problem. Nothing speculative.**
- No features/abstractions beyond what was asked. No speculative configurability.
- If you write 200 lines and it could be 50, rewrite it.
- Ask: "Would a senior engineer say this is overcomplicated?" If yes, simplify.

### 3. Surgical Changes
- **Touch only what you must. Clean up only your own mess.**
- Don't "improve" adjacent code, comments, or formatting. Don't refactor things that aren't broken.
- Match existing style, even if you'd do it differently.
- Remove imports/variables/functions that YOUR changes made unused. Don't touch pre-existing dead code unless asked.
- Every changed line should trace directly to the user's request.

### 4. Goal-Driven Execution
- **Define success criteria. Loop until verified.**
- Transform tasks into verifiable goals (e.g., write/run tests to reproduce bug first).
- For multi-step tasks, state a brief plan with verification checks for each step:
  ```
  1. [Step] → verify: [check]
  2. [Step] → verify: [check]
  ```
- Strong success criteria let you loop independently.

