# Mining Self-Check Checklist

> Binary quality gates for Stage 0.7 Miner handoff.
> ALL gates must PASS before emitting domain-handbook.md or triggering Architect.

## Phase 1 — Input Integrity
- [ ] exploration.md tồn tại tại `.skill-context/{target_skill}/exploration.md`
- [ ] exploration.md có frontmatter YAML hợp lệ
- [ ] hydrated-context.yaml tồn tại và stage="mining"
- [ ] thought-cache.yaml tồn tại (optional warning nếu thiếu)
- [ ] business-analysis.md tồn tại → parse synthesized_requirements (optional)
- [ ] Input file ≤512000 bytes (NFR-2 cap)

## Phase 2 — Workspace Scan
- [ ] knowledge/ directories scanned
- [ ] Temps/spec/ scanned
- [ ] .claude/agents/ scanned
- [ ] _shared/ scanned
- [ ] Kết quả scan ghi vào resources/ (nếu có)

## Phase 3 — Extraction Gates (HARD)
- [ ] **MIN-1.0: Glossary ≥10 terms**
  - Count: ___
  - Mỗi term có term + definition không rỗng
- [ ] **MIN-2.0: Anti-patterns ≥3 items**
  - Count: ___
  - Mỗi anti-pattern có name + symptom + solution
- [ ] **MIN-3.0: Exemplars ≥1 item**
  - Count: ___
  - Mỗi exemplar có name + description
- [ ] domain_anchors ≥1 anchor

## Phase 4 — Schema Validation (HARD)
- [ ] domain-handbook.md có YAML frontmatter
- [ ] Schema validation PASS:
  ```bash
  python3 skills/ver-3/_shared/validators/schema_validator.py \
    --path .skill-context/{target_skill}/domain-handbook.md \
    --schema skills/ver-3/_shared/schemas/domain-handbook.schema.yaml
  ```

## Phase 5 — Write Confinement & Quality (HARD)
- [ ] **NFR-3**: 100% writes confined dưới `.skill-context/{target_skill}/` — KIỂM TRA: không có file ghi ngoài scope
- [ ] **NFR-4**: Mọi external doc bọc trong `<input>` boundary
- [ ] **NFR-9**: Zero placeholder density — grep TODO/FIXME/mock = 0
- [ ] No dynamic exec từ input (NFR-4 enforced)

## Phase 6 — DRC Contract Verification
- [ ] data/drc.yaml tồn tại
- [ ] drc.yaml skill_name khớp với SKILL.md name
- [ ] Upstream/downstream skills đúng
- [ ] Fallback targets xác định

## Final Gate — Handoff Decision
- [ ] ALL binary gates PASS → Emit domain-handbook.md → Trigger skill-architect
- [ ] glossary<10 → F6: Librarian subagent deep scan in Claude Code TUI
- [ ] anti_patterns<3 → F2: escalate ba-pipeline-runner
- [ ] Schema FAIL → F2: escalate ba-pipeline-runner (NO EMIT)
- [ ] Escalated → manual intervention required
