# Phase 0 — Foundation Bootstrap

> **Order:** 1st phase | **Estimated effort:** S (small) | **Predicted duration:** 1 session
> **Depends on:** None
> **Downstream:** Phase 1 (Knowledge base), Phase 2 (Hooks), Phase 3 (Agents), Phase 4 (Schemas)
> **Architectural defects addressed:** Γ-7 (re-init destroys state — fix bằng checkpoint archive bootstrap)
> **Roadmap evaluation v1 patches incorporated:** Đề xuất 3 — Docker Diagnostics AC-8 (early env check, tránh late discovery tại Phase 7)

## Mục đích

Phase 0 trả lời câu hỏi: "Trước khi xây bất kỳ thứ gì, ta cần scaffolding directory nào, naming convention nào, và những 'puzzle pieces' cơ bản tồn tại mà chưa được khởi tạo?"

Phase này KHÔNG build skill, agent, hay hook logic. Phase này chỉ tạo **scaffold** (dir, paths, stubs, registry templates) để Phase 1-4 có chỗ để đi vào.

---

## Prerequisites

```yaml
prerequisites:
  - git repo đã commit clean (chạy `git status` clean)
  - Python 3.10+ có sẵn
  - `pyyaml` package đã cài
  - Docker CLI có sẵn (chỉ để verify path, không chạy tại Phase 0)
  - Unix shell (zsh hoặc bash)
  - jq CLI (đã install sẵn — subagent-forge.md cần nó)
```

---

## Deliverables (file-by-file)

### D1 — Canonical directory structure

Tạo cây thư mục runtime đầy đủ:

```text
.claude/
├── knowledge/              ← Phase 1 sẽ fill (had reference trong subagent-forge nhưng chưa tồn tại)
│   ├── agents/              ← 7 kiến thức docs cho agents sẽ đặt đây
│   ├── skills/              ← Kiến thức docs về skill format
│   └── hooks/                ← Kiến thức docs về hook conventions
├── skills/
│   ├── context-before-fix/  ← Đã tồn tại, giữ nguyên Phase 0
│   └── (11 skill dirs sẽ tạo rỗng Phase 0 — Phase 5/6/7 fill)
├── agents/
│   ├── subagent-forge.md    ← Đã tồn tại, giữ nguyên Phase 0
│   ├── _staging/             ← Guard path của subagent-forge
│   └── _archive/             ← Mới trong Phase 0: archived agent versions
├── hooks/
│   ├── events/               ← Standalone hook scripts (Phase 2)
│   └── registry.yaml         ← Hook → event mapping
├── scripts/
│   └── validate_suite_integrity.py   ← Canonical integrity check
├── rules/                    ← Đã tồn tại rỗng, để DHCP default rules Phase 0
└── settings.json             ← Tạo Phase 0 nếu không tồn tại

raw/ver-3/                    ← Tái tạo (đã mất trong baseline)
├── _shared/
│   ├── schemas/              ← Phase 4 fill với YAML schemas
│   ├── validators/            ← Phase 4 fill với scripts
│   ├── templates/             ← Phase 4 fill với artifact templates
│   ├── knowledge/             ← shared knowledge docs (e.g., karpathy-standards)
│   └── fixtures/               ← shared test fixtures
├── skill-explorer/           ← dir sẽ populate Phase 6
├── skill-knowledge-miner/
├── skill-architect/
├── production-quality-gatekeeper/
├── skill-planner/
├── skill-builder/
├── production-code-reviewer/
├── skill-security-reviewer/
├── sandbox-tester/            ← Phase 7
├── indexer/                   ← Phase 7
├── ba-elicitor/               ← Phase 5
├── ba-analyst/
└── ba-synthesizer/

.skill-context/
├── registry/                  ← Lifecycle status tracking cho mỗi skill
└── suite_config.yaml         ← Dynamic Configuration Overlay (theo §6 architecture.md)

docs/context-to-work/foundation-bootstrap/
└── scope.2026-07-04.md       ← Phập Phase 0 scope document (theo context-before-fix pattern)
```

### D2 — `.claude/scripts/validate_suite_integrity.py`

Script Python kiểm tra tính toàn vẹn của bộ skill suite. Chạy được từ anywhere:

```python
#!/usr/bin/env python3
"""Validate Suite Integrity — Phase 0 minimal version.

Exit codes:
  0 = all checks pass
  1 = structural checks fail (missing dirs/files)
  2 = schema validity fail (yaml parse error or missing required keys)
  3 = registry consistency fail (skills-registry.json mismatch với filesystem)
"""
# Cần import yaml, sys, os, json
# Checks (detailed spec trong Phase 0 Acceptance Criteria §AC-3)
```

**Lưu ý**: Script phải parse `skills-registry.json`, duyệt mỗi `src_path` declared, kiểm tra:
- (i) Dir tồn tại
- (ii) `SKILL.md` tồn tại
- (iii) YAML frontmatter hợp lệ
- (iv) `name` field matches dir name
- (v) `version` field present và semantic version format
- (vi) `suite` field == "WASHVN"

Exit 1first failure → print reason to stderr. Exit 0 → print "OK: 0/N skills valid" (Phase 0 expect 0/N vì dirs rỗng).

### D3 — `.claude/settings.json`

Nếu chưa tồn tại, tạo với minimal permissions:

```json
{
  "permissions": {
    "allow": ["Read", "Glob", "Grep", "Bash(validate_suite_integrity.py)"],
    "deny": ["Bash(rm -rf *)"]
  }
}
```

### D4 — `_state.yaml` checkpoint archive protocol (address Γ-7)

Tạo `.skill-context/_state-archive/` directory và stub `.skill-context/suite_config.yaml`:

```yaml
# suite_config.yaml — Dynamic Configuration Overlay (per §6 architecture.md)
suite: WASHVN
version: 3.0.0
runtime_target:
  claude_code: .claude/skills/
  antigravity: .agents/skills/
  hermes: .hermes/skills/

state_archive:
  path: .skill-context/_state-archive/
  retention_policy: keep_last_3_per_run_id
  pre_reinit_backup: required    # CRITICAL: fix architectural defect Γ-7

yaml_resilience:
  max_repair_attempts_per_artifact: 2
  translation_history: append_only
  max_history_entries: 20          # fix architectural defect: unbounded state ledger

feature_flags:
  enable_docker_sandbox: true
  enable_branch_b_orchestration: true
  hysteresis_zone_scs: [2.7, 3.3]  # architectural defect Γ-3 fix placeholder
```

### D5 — 7 knowledge-doc stubs (Phase 1 sẽ fill content)

Tạo 7 file stub tại `.claude/knowledge/agents/` được subagent-forge.md reference:

```text
.claude/knowledge/agents/
├── configuration.md          ← Phase 1 fill: 16-field frontmatter schema
├── capability_controls.md    ← Phase 1 fill: tool allow/deny, permissionMode, MCP scoping
├── examples.md               ← Phase 1 fill: 4 reference patterns (code-reviewer, debugger, data-scientist, db-reader)
├── forks.md                  ← Phase 1 fill: experimental fork semantics
├── hooks_and_events.md       ← Phase 1 fill: hook protocol spec
├── workflow_patterns.md      ← Phase 1 fill: invocation, foreground/background, resume
└── xml_tags_standards.yaml   ← Phase 1 fill: 9 XML tags whitelist
```

Mỗi stub có ribbon placeholder:

```markdown
---
phase_to_author: 1
status: stub
estimated_lines: 100-150
last_updated: 2026-07-04
---

# <TITLE>

> [!WARNING]
> STUB FILE — Phase 1 will populate this document.
> Do NOT consume this content yet; subagent-forge.md must fall back to inline hook contract until Phase 1 complete.

(to be authored in Phase 1)
```

### D6 — 11 raw/ver-3/ skill directory stubs

Mỗi 11 dirs cần có cấu trúc 7-Zone skeleton:

```text
raw/ver-3/<skill-name>/
├── SKILL.md          ← Phase 5/6/7 fill
├── knowledge/         ← empty
├── scripts/           ← empty
├── templates/         ← empty
├── data/              ← empty
├── loop/              ← empty
└── assets/            ← empty
```

Chỉ cần tạo các dir rỗng (`.gitkeep` trong mỗi dir) — Phase 5/6/7 sẽ fill content.

### D7 — `raw/ver-3/_shared/` skeleton

Tạo skeleton:

```text
raw/ver-3/_shared/
├── schemas/             ← Phase 4 fill với:
│   ├── exploration.schema.yaml
│   ├── criteria.schema.json
│   ├── design.schema.yaml
│   ├── quality-matrix.schema.yaml
│   ├── todo.schema.yaml
│   ├── build-log.schema.yaml
│   ├── review-report.schema.yaml
│   ├── audit-metrics.schema.yaml
│   ├── verification.schema.yaml
│   ├── security-review.schema.yaml
│   ├── elicitation.schema.yaml
│   ├── analysis.schema.yaml
│   ├── synthesis.schema.yaml
│   └── domain-handbook.schema.yaml
├── validators/
│   └── schema_validator.py     ← Phase 4 fill
├── templates/
│   ├── artifact_template.md     ← Phase 4 fill
│   └── drc_contract_template.yaml  ← Phase 4 fill
├── knowledge/
│   └── karpathy-standards.md    ← chống mất (nếu không tồn tại, Phase 0 copy từ Temps/raw/karpathy-standards.md nếu có)
└── fixtures/                    ← test fixtures rỗng
```

### D8 — `.claude/hooks/registry.yaml` stub

```yaml
# Hook Registry — Phase 2 sẽ fill với danh sách đầy đủ
# Cấu trúc mỗi entry:
#   event_type: PreToolUse | PostToolUse | Stop | SessionStart
#   matcher: regex string cho tool_name hoặc event pattern
#   script: path tới shell script trong .claude/hooks/events/
#   exit_allow: exit code = allow (default 0)
#   exit_block: exit code = block (default 2)

hooks:
  # Phase 2 sẽ populate
version: 0.0.1
suite: WASHVN
last_updated: 2026-07-04
```

### D9 — `workspce_tree.md` update (file đã tồn tại)

Cập nhật file này (nếu đã tồn tại) với các entry mới cho directories. Cần xác nhận path của file này trước khi update.

---

## Verification checklist (cơ học)

### AC-1 — Directory structure
```bash
# Chạy:
test -d .claude/knowledge/agents/ && \
test -d .claude/hooks/events/ && \
test -d .claude/scripts/ && \
test -d .claude/agents/_archive/ && \
test -d raw/ver-3/_shared/schemas/ && \
test -d raw/ver-3/_shared/validators/ && \
test -d .skill-context/_state-archive/ && \
test -d .skill-context/registry/ && \
echo "AC-1 PASS"
```

### AC-2 — 11 skill dirs tồn tại với 7-Zone skeleton
```bash
for skill in skill-explorer skill-knowledge-miner skill-architect production-quality-gatekeeper skill-planner skill-builder production-code-reviewer skill-security-reviewer sandbox-tester indexer ba-elicitor ba-analyst ba-synthesizer; do
  for zone in knowledge scripts templates data loop assets; do
    test -d raw/ver-3/$skill/$zone || exit 1
  done
  test -f raw/ver-3/$skill/SKILL.md || echo "$skill SKILL.md chưa fill (OK tại Phase 0)"
done
echo "AC-2 PASS"
```

### AC-3 — `validate_suite_integrity.py` chạy được
```bash
python3 .claude/scripts/validate_suite_integrity.py
# Exit 0 hoặc exit 1 (vì 11 skills chưa populated, doar dir tồn tại)
# Exit 2 hoặc 3 = FAIL (script broken hoặc mismatch)
```

### AC-4 — 7 knowledge docs stubs tồn tại
```bash
for doc in configuration.md capability_controls.md examples.md forks.md hooks_and_events.md workflow_patterns.md xml_tags_standards.yaml; do
  test -f .claude/knowledge/agents/$doc || exit 1
done
echo "AC-4 PASS"
```

### AC-5 — subagent-forge.md không broken
```bash
# Verify agent still parse (frontmatter YAML válido):
python3 -c "import yaml; yaml.safe_load(open('.claude/agents/subagent-forge.md').read().split('---')[1])" && echo "AC-5 PASS"
```

### AC-6 — State archive protocol in place (Γ-7 fix)
```bash
test -d .skill-context/_state-archive/
test -f .skill-context/suite_config.yaml
grep -q "pre_reinit_backup: required" .skill-context/suite_config.yaml
echo "AC-6 PASS"
```

### AC-7 — Hook registry stub exists
```bash
test -f .claude/hooks/registry.yaml
python3 -c "import yaml; yaml.safe_load(open('.claude/hooks/registry.yaml'))"
echo "AC-7 PASS"
```

### AC-8 — Docker Diagnostics (added per roadmap evaluation v1, đề xuất 3)

> Early environment check — tránh late discovery tại Phase 7 (sandbox-tester) khi Docker daemon không sẵn sàng hoặc user không có quyền.

```bash
# 1. Docker CLI tồn tại trong PATH
command -v docker > /dev/null || { echo "AC-8 FAIL: docker CLI not in PATH"; exit 1; }

# 2. Docker daemon running + reachable
docker info > /dev/null 2>&1 || { echo "AC-8 FAIL: docker daemon not running. Start with 'sudo systemctl start docker'"; exit 1; }

# 3. User có quyền pull/build/run (không cần sudo)
docker run --rm hello-world > /dev/null 2>&1 || {
  echo "AC-8 WARNING: user not in docker group (docker run cần sudo). Khuyến nghị: 'sudo usermod -aG docker \$USER' rồi re-login."
  echo "AC-8 PASS_WITH_WARNING"
  exit 0
}

# 4. Docker disk còn không gian (≥1GB free)
FREE_GB=$(df -BG --output=avail $(docker info --format '{{.DockerRootDir}}' 2>/dev/null || echo /var/lib/docker) | tail -1 | tr -d 'G' || echo 0)
test "$FREE_GB" -ge 1 || { echo "AC-8 FAIL: docker disk <1GB free"; exit 1; }

# 5. Network access (cần thiết cho Phase 7 pull base images)
# Optional check — không block vì có thể sử dụng cached images:
docker pull python:3.10-slim > /dev/null 2>&1 || echo "AC-8 NOTE: cannot pull python:3.10-slim (network restricted) — Phase 7 needs manual image pre-load"

echo "AC-8 PASS — Docker environment healthy for Phase 7 sandbox"
```

> AC-8 phải PASS (hoặc PASS_WITH_WARNING) trước khi Phase 0 declare done. Nếu FAIL, Phase 7 không thể complete — early discovery tại Phase 0 cho phép either install Docker, request permission, hoặc detect environment trước khi đầu tư vào Phase 1-6.

---

## Step-by-step task list

> Mỗi task phải commit atomic trước khi sang task sau.

1. **Scaffold directories** — chạy `mkdir -p` cho tất cả 11 raw/ver-3/ skill dirs, 7-zone subdirs, .claude/knowledge/agents/, .claude/hooks/events/, .claude/scripts/, .skill-context/_state-archive/, .skill-context/registry/. Tạo `.gitkeep` files. → commit `phase-0: scaffold directory structure`

2. **Author `validate_suite_integrity.py`** — viết script Python ~100-150 dòng, parse skills-registry.json, kiểm tra 11 skill dirs, frontmatter hợp lệ. Test với một BROKEN case (e.g., tạo một SKILL.md sai frontmatter tạm thời, verify exit 2). Xóa broken case. → commit `phase-0: integrity validator script`

3. **Tạo `.claude/settings.json`** — minimal permissions ( nếu chưa tồn tại). → commit `phase-0: claude settings bootstrap`

4. **Tạo `.skill-context/suite_config.yaml`** — copy template từ D4. Đặc biệt thêm `pre_reinit_backup: required` cho Γ-7 fix. → commit `phase-0: suite config + state archive bootrap`

5. **Tạo 7 knowledge docs stubs** — copy template từ D5 vào 7 file. → commit `phase-0: knowledge agent doc stubs`

6. **Tạo raw/ver-3/_shared/ skeleton** — tất cả subdirs rỗng + schema files rỗng (chỉ header `# schema stub — Phase 4 fill`). Karpathy-standards.md: copy nếu tìm thấy trong Temps/raw/ hoặc create stub. → commit `phase-0: shared schemas scaffold`

7. **Tạo `.claude/hooks/registry.yaml`** — copy template từ D8. → commit `phase-0: hook registry stub`

8. **Update `workspce_tree.md`** — thêm entries cho tất cả directories mới tạo. → commit `phase-0: routing map updated`

9. **Author scope doc** — `docs/context-to-work/foundation-bootstrap/scope.2026-07-04.md` theo pattern `context-before-fix` skill đang dùng — output schema theo skill output-schema.md. → commit `phase-0: scope doc per context-before-fix pattern`

10. **Run full acceptance criteria** — chạy AC-1 đến AC-8 sequentially (AC-8 added per eval v1). Tất cả PASS → commit `phase-0: acceptance criteria passed`. Tất cả FAIL → log reason, rollback về commit trước task fail, root-cause and fix.

---

## Risks tại Phase 0

| Risk | Mitigation |
|:---|:---|
| `validate_suite_integrity.py` có bug → false negatives blocking mọi phase sau | Tạo FAULT INJECTION test: deliberately broken SKILL.md để verify script catch |
| Karpathy-standards.md không có trong Temps/raw/ | Stub tạo ; Phase 4 sẽ backfill từ git history nếu recover được |
| Thư mục `knowleages` (typo) vs `knowledge` (canonical) — subagent-forge reference `.claude/knowledge/` (sai chính tả vs tên dir `knowleages/`) | Giữ cả 2 dir; symlink `knowleages` → `knowledge` temporarily; Phase 8 sẽ consolidate decision |
| `workspce_tree.md` typo "workspce" không "workspace" | Phase 0 giữ nguyên tên để tôn trọng backward compat; ghi chú để Phase 8 decide rename |

---

## Definition of done (Phase 0)

```yaml
dod:
  - All AC-1 to AC-8 PASS (AC-8 cho phép PASS_WITH_WARNING)
  - Git log có ≥ 9 atomic commits với convention `phase-0: <task>`
  - `validate_suite_integrity.py` exit 0 hoặc exit thông cáo có ý nghĩa
  - Mỗi 7 knowledge stubs file tồn tại với YAML frontmatter (status: stub, phase_to_author: 1)
  - State archive directory tồn tại với `suite_config.yaml` đã có `pre_reinit_backup: required`
  - Hook registry stub tồn tại với valid YAML
  - Skill context `.skill-context/suite_config.yaml` reference được bởi `architecture.md §6` overlay
  - Scope document theo context-before-fix pattern tồn tại
```

Sau khi Phase 0 done → đánh dấu `index.md` "Phase 0" status = `done` và bắt đầu Phase 1.

---

## Liên kết

- [Roadmap Index](index.md)
- [Phase 1 tiếp theo](01-knowledge-base-authoring.md)
- [Architecture critic report](../architects/README.md) — reference source
- [Architecture overview](architecture.md) — pipeline architecture
- [Knowledge format standard](standards.md) — format rules