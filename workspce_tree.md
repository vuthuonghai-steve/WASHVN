# 🗺️ Workspace Tree — Routing Quick Reference

> **Version:** 3.0.0 | **Updated:** 2026-06-07
> Mục đích: Bản đồ điều hướng workspace, xác định đúng Zone trước khi làm task.

---

## 📁 Root-Level Files

| File | Vai trò | Ghi chú |
|------|---------|---------|
| `CLAUDE.md` | Root Agent Guide (L0 anchor) | Đọc đầu tiên |
| `architecture.md` | Kiến trúc Master Skill Suite | 8-Stage Pipeline |
| `standards.md` | LLM Knowledge Activation Standard | Format rules |
| `workspce_tree.md` | ⬅️ File này — routing map | Đọc trước mỗi task |

---

## 📦 Master Skill Suite (`raw/ver-3/`)

> **Source of Truth** — Phát triển tại đây, sync ra `.agents/skills/` và `.claude/skills/`

### Pipeline Skills (Core)

| Stage | Skill Directory | SKILL.md | Vai trò |
|-------|----------------|----------|---------|
| Stage 0 | `raw/ver-3/skill-explorer/` | `SKILL.md` | Khảo sát, exploration |
| Stage 0.5 | `raw/ver-3/skill-knowledge-miner/` | `SKILL.md` | Khai thác tri thức |
| Stage 1 | `raw/ver-3/skill-architect/` | `SKILL.md` | Thiết kế kiến trúc |
| Stage 1.5 | `raw/ver-3/production-quality-gatekeeper/` | `SKILL.md` | Thẩm định chất lượng |
| Stage 2 | `raw/ver-3/skill-planner/` | `SKILL.md` | Lập kế hoạch |
| Stage 3 | `raw/ver-3/skill-builder/` | `SKILL.md` | Xây dựng skill |
| Stage 3.5 | `raw/ver-3/production-code-reviewer/` | `SKILL.md` | Review code |
| Stage 4 | `raw/ver-3/sandbox-validator/` | *(planned)* | Kiểm thử sandbox |
| Stage 5 | `raw/ver-3/index-builder/` | *(planned)* | Đăng ký chỉ mục |

### Business Analysis Skills

| Skill | SKILL.md | Vai trò |
|-------|----------|---------|
| `raw/ver-3/ba-analyst/` | `SKILL.md` | Phân tích nghiệp vụ |
| `raw/ver-3/ba-elicitor/` | `SKILL.md` | Khơi gợi yêu cầu |
| `raw/ver-3/ba-synthesizer/` | `SKILL.md` | Hợp nhất BA reports |

### Security Skill

| Skill | SKILL.md | Vai trò |
|-------|----------|---------|
| `raw/ver-3/skill-security-reviewer/` | `SKILL.md` | OWASP security review |

### Shared Infrastructure

| Path | Nội dung | Files |
|------|----------|-------|
| `raw/ver-3/_shared/knowledge/` | Knowledge base | `framework.md`, `case-system.md`, `format-standards.md`, `placeholder-policy.md`, `karpathy-standards.md` |
| `raw/ver-3/_shared/validators/` | Validators | `check_status.py`, `schema_validator.py`, `handoff_validator.py`, `rollback_engine.py`, `trace_validator.py` |
| `raw/ver-3/_shared/schemas/` | JSON/YAML schemas | `exploration.schema.yaml`, `design.schema.yaml`, `todo.schema.yaml`, ... |
| `raw/ver-3/_shared/fixtures/` | Test fixtures | `good/`, `bad/` |

---

## 🚀 Deployment Targets

| Target | Sync command | Mục đích |
|--------|-------------|----------|
| `.agents/skills/` | `cp -r raw/ver-3/* .agents/skills/` | Antigravity runtime |
| `.claude/skills/` | `cp -r raw/ver-3/* .claude/skills/` | Claude Code runtime |

---

## 📚 Other Directories

| Path | Vai trò |
|------|---------|
| `.agents/knowledge/` | Agent knowledge base |
| `.claude/knowledge/` | Claude-specific knowledge |
| `docs/context-to-work/` | Scope analysis documents |
| `.codegraph/` | Codegraph index (auto-generated) |
| `.omc/` | OMC orchestration state |

---

## ✅ Routing Rules

```yaml
routing_rules:
  edit_skill_code:
    - "Làm việc tại raw/ver-3/{skill-name}/"
    - "Không sửa trực tiếp .agents/skills/ hay .claude/skills/"
    - "Sync sau khi hoàn tất: cp -r raw/ver-3/* .agents/skills/"

  create_new_skill:
    - "Tạo design.md + criteria.md trước"
    - "Theo 7-Zone structure"
    - "Đăng ký vào llms.txt sau khi verified"

  run_validator:
    - "Chạy validate_suite_integrity.py trước mỗi sync"
    - "python3 raw/ver-3/scripts/validate_suite_integrity.py"

  add_to_routing_map:
    - "Cập nhật file này khi thay đổi structure"
    - "Đảm bảo file path chính xác"
```
