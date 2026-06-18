---
# [TỪ DESIGN §3 references zone, §10.1 versioning, BA §6 KG-10, R-10, RES-01..RES-08]
# ver-0.0.3 — KG-10 P1: Migration guide from 0.0.2 to 0.0.3.
# Lists all 7 breaking changes (C1-C7) with upgrade steps.
artifact_type: "migration-guide"
from_version: "0.0.2"
to_version: "0.0.3"
zone: "references"
---

# Migration Guide: skill-builder 0.0.2 → 0.0.3

> **Audience**: Maintainers of skills that depend on skill-builder, or teams running skill-builder ver-0.0.2 with plans to upgrade.

---

## Breaking Changes Summary (7 items: C1-C7)

| # | Change | Type | Severity | Affected Files |
|---|--------|------|----------|----------------|
| C1 | Version bump 0.0.1 → 0.0.3 (SKILL.md); spec_version 3.0.0 → 3.1.0 (SPEC.md) | Semver | P1 | `SKILL.md`, `SPEC.md` |
| C2 | Placeholder threshold unified `<5 PASS / 5-9 WARNING / >=10 FAIL` | Behavior | P1 | `SKILL.md`, `loop/build-checklist.yaml`, `policy/skill-builder.yaml`, `SPEC.md` |
| C3 | `skills-registry.json` `src_path` canonicalized to `skills/ver-0.0.2/skill-builder` | Routing | P0 | `skills-registry.json`, `workspce_tree.md` |
| C4 | 4 missing zones added: `policy/`, `templates/`, `data/`, `examples/`, `references/` | Structure | P0 | New zones |
| C5 | `disable-model-invocation: true` kept (sibling consistency); auto-trigger deferred | Behavior | P1 | `SKILL.md` |
| C6 | 8-stage pipeline documented in `SPEC.md` §8 (0, 0.5, 1, 1.5, 2, 3, 3.5, 4, 5) | Documentation | P1 | `SPEC.md` |
| C7 | Validator regex refactored: `^## 3\.\s+` section-number pattern (was literal `"## 3. Zone Mapping"`) | Code | P0 | `scripts/validate_skill.py` |

---

## C1 — Version Bump (P1)

### Before (0.0.2)

```yaml
# SKILL.md
name: skill-builder
version: 0.0.1
```

```yaml
# SPEC.md
spec_version: "3.0.0"
```

### After (0.0.3)

```yaml
# SKILL.md
name: skill-builder
version: 0.0.3
suite: WASHVN
stage: 3
```

```yaml
# SPEC.md
spec_version: "3.1.0"
```

### Migration

```bash
# Update frontmatter
sed -i 's/version: 0.0.1/version: 0.0.3/' skills/ver-0.0.2/skill-builder/SKILL.md
sed -i 's/spec_version: "3.0.0"/spec_version: "3.1.0"/' skills/ver-0.0.2/skill-builder/SPEC.md
```

---

## C2 — Placeholder Threshold Unification (P1)

### Before (0.0.2) — INCONSISTENT

| File | Threshold | Issue |
|------|-----------|-------|
| `SKILL.md` line 30 | `placeholder density > 9` | Inconsistent |
| `SKILL.md` line 225 (Phase 4) | `<5 / 5-9 / 10+` | Different boundary |
| `loop/build-checklist.yaml` | `<5 / 5-9 / >=10` | Different from SKILL.md line 30 |
| `SPEC.md` §4 | `<5 / 5-9 / 10+` | Different boundary |

### After (0.0.3) — UNIFIED

All 4 locations now read: `<5 PASS / 5-9 WARNING / >=10 FAIL` — single canonical threshold.

### Migration

Verify all 4 locations read the same threshold. Validator `check_placeholder_density` enforces the unified rule.

---

## C3 — Routing Path Canonicalization (P0)

### Before (0.0.2)

```json
// skills-registry.json line 168
{
  "name": "skill-builder",
  "src_path": "raw/ver-3/skill-builder"  // ❌ Stale path
}
```

```markdown
<!-- workspce_tree.md Stage 3 row -->
| Stage 3 | `raw/ver-3/skill-builder/` | ... | ❌ Stale path
```

### After (0.0.3)

```json
{
  "name": "skill-builder",
  "version": "0.0.3",
  "src_path": "skills/ver-0.0.2/skill-builder"  // ✅ Canonical
}
```

```markdown
| Stage 3 | `skills/ver-0.0.2/skill-builder/` | `SKILL.md` | Xây dựng skill | ✅ Synced
```

### Migration

```bash
# 1. Update skills-registry.json
jq '.skills[] | select(.name=="skill-builder") | .src_path = "skills/ver-0.0.2/skill-builder"' skills-registry.json > /tmp/sr.json && mv /tmp/sr.json skills-registry.json

# 2. Update workspce_tree.md Stage 3 row
sed -i 's|raw/ver-3/skill-builder|skills/ver-0.0.2/skill-builder|g' workspce_tree.md
```

---

## C4 — 4 Missing Zones Added (P0)

### Before (0.0.2) — 4 zones

```
skill-builder/
├── SKILL.md
├── knowledge/
├── scripts/
└── loop/
```

### After (0.0.3) — 9 zones

```
skill-builder/
├── SKILL.md
├── knowledge/         (existing, 3 files refactored + 3 new = 6 files)
├── scripts/           (existing, 1 file refactored)
├── loop/              (existing, 3 files refactored)
├── policy/            (NEW — 4 files: skill-builder.yaml, workflow.md, guardrails.md, output-spec.md)
├── templates/         (NEW — 1 file: build-log.md.template)
├── data/              (NEW — 1 file: builder-knowledge-sources.yaml)
├── examples/          (NEW — 1 file: build-exemplars.md; +1 optional fidelity-checks.md deferred)
└── docs/              (NEW — 1 file: MIGRATION-0.0.2-to-0.0.3.md, this file)
```

### Migration

No action needed for consumers — new zones are additive. For skill-builder self: cp -r the 8 new files (5 policy/templates/data + 1 examples + 1 docs) into the skill dir.

---

## C5 — disable-model-invocation Consistency (P1)

### Before / After

Both 0.0.2 and 0.0.3 have `disable-model-invocation: true` (consistent with sibling `skill-architect`).

### Why kept

- Sibling consistency (skill-architect also `true`)
- Manual trigger via parent orchestrator = explicit
- Auto-trigger deferred to ver-0.0.4

### When to change to `false`

If Steve wants Builder to auto-trigger in autopilot/ralph workflows, bump ver-0.0.4 + change to `false`. See `design.md §9 Q1 DEFERRED`.

---

## C6 — 8-Stage Pipeline Documentation (P1)

### Before (0.0.2) — 6 stages in SPEC.md §8

```yaml
# SPEC.md §8
pipeline:
  stage_order: 3
  predecessor: "skill-planner"
  successor: null  # ❌ Stale
```

### After (0.0.3) — 8 stages

```yaml
# SPEC.md §8
pipeline:
  stage_order: 3
  predecessor: "skill-planner"  # Stage 2
  successor: "production-code-reviewer"  # Stage 3.5
  full_8_stage_pipeline:
    - 0    # Explorer
    - 0.5  # Knowledge Miner
    - 1    # Architect
    - 1.5  # Quality Gatekeeper
    - 2    # Planner
    - 3    # Builder (this skill)
    - 3.5  # Code Reviewer
    - 4    # Sandbox Tester
    - 5    # Indexer
```

### Migration

Update SPEC.md §8 to list all 8 stages. See `architecture.md §1` for canonical pipeline.

---

## C7 — Validator Regex Refactor (P0)

### Before (0.0.2) — brittle literal match

```python
# scripts/validate_skill.py line 153
if '## 3. Zone Mapping' in line:
    in_zone_mapping = True
```

→ Fails on heading variations like "## 3 Zone Mapping", "## 3. Zones".

### After (0.0.3) — robust section-number pattern

```python
# scripts/validate_skill.py
_ZONE_SECTION_PATTERN = re.compile(r"^##\s+3\.\s+", re.MULTILINE)

def _parse_zone_mapping(design_path: str, version: int = 2) -> List[Dict[str, str]]:
    """R1 fix: section-number pattern matches all variations."""
    ...
```

→ Matches `## 3. Zone Mapping`, `## 3 Zone Mapping`, `## 3. Zones`, etc.

### Migration

```bash
# Validator refactored automatically in 0.0.3. No user action needed.
# For backward compat, use --zone-mapping-version 1 (legacy literal match).
python3 scripts/validate_skill.py <path> --zone-mapping-version 1  # legacy
python3 scripts/validate_skill.py <path> --zone-mapping-version 2  # default (section-number)
```

---

## Upgrade Steps (Step-by-step)

```bash
# 1. Backup current skill-builder
cp -r skills/ver-0.0.2/skill-builder/ /tmp/skill-builder-v0.0.2-backup/

# 2. Apply migration (assume new files already exist from Stage 3 build)
# C1: version bump (manual edit or sed)
# C2: threshold unified (already done in this build)
# C3: update registry + tree (T9.4 + T9.5)
# C4: copy 5 new zone files into skill dir
# C5: no action
# C6: update SPEC.md §8
# C7: validator refactored (R1+R2)

# 3. Run validator
python3 skills/ver-0.0.2/skill-builder/scripts/validate_skill.py \
    skills/ver-0.0.2/skill-builder/ \
    --design .skill-context/skill-builder/design.md \
    --todo .skill-context/skill-builder/todo.md \
    --strict-context
# Expect: Exit 0

# 4. Run build-checklist v2.0.0
# (manual or via Stage 4 sandbox-validator)

# 5. Sync runtime
cp -r skills/ver-0.0.2/skill-builder/* .claude/skills/skill-builder/

# 6. Verify
python3 .claude/skills/skill-builder/scripts/validate_skill.py \
    .claude/skills/skill-builder/ \
    --design .skill-context/skill-builder/design.md
# Expect: Exit 0
```

---

## Rollback Procedure

If 0.0.3 breaks your pipeline:

```bash
# 1. Restore from backup
rm -rf skills/ver-0.0.2/skill-builder/
cp -r /tmp/skill-builder-v0.0.2-backup/ skills/ver-0.0.2/skill-builder/

# 2. Restore registry
git checkout skills-registry.json

# 3. Restore workspce_tree
git checkout workspce_tree.md

# 4. Sync runtime
cp -r skills/ver-0.0.2/skill-builder/* .claude/skills/skill-builder/
```

---

## Deferred to ver-0.0.4 (P2)

| # | Item | Reason | Timeline |
|---|------|--------|----------|
| KG-3 | `knowledge/build-visualization-guidelines.md` (Mermaid standards) | Optional per design §3 | ver-0.0.4 |
| KG-9 | `examples/fidelity-checks.md` (3 case studies) | Optional per design §3 | ver-0.0.4 |
| Q1 | `disable-model-invocation: false` for auto-trigger | Awaiting Steve sign-off | TBD |
| Q2 | `--sandbox` flag for validate_skill.py | Awaiting Stage 4 sandbox-validator | TBD |
| R11 | Recursive sub-skill validation in Docker/gVisor | Awaiting Stage 4 | TBD |
| R12 | Idempotency 3-run byte-identical benchmark | Awaiting Stage 4 acceptance criteria | TBD |
| NFR-01 | Build time p95 benchmark | Awaiting Stage 4 sandbox-validator | TBD |

---

## References

- `design.md` — Stage 1 architecture
- `quality-matrix.yaml` — Stage 1.5 quality gate
- `todo.md` — Stage 2 execution plan
- `architecture.md` — 8-Stage pipeline + CASE recovery
- `CLAUDE.md` — Project rules + routing
- `workspce_tree.md` — Routing map (Stage 3 row updated)
- `skills-registry.json` — Skill registry (src_path canonicalized)

---

> **Migration Status**: ✅ Complete for ver-0.0.3 (8 new files + 5 refactored + 1 deferred).
> **Next**: Stage 3.5 (production-code-reviewer) will validate the build.
