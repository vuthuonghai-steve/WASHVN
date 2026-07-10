# 📋 Phạm vi: Đồng bộ & Thống nhất Kiến trúc Skill Suite

> **Generated**: 2026-06-07
> **Target**: `skills/ver-3/` — 12 skills + `_shared/`
> **Type**: Architecture sync scope analysis
> **Status**: 🔍 Discovery complete — ready for fix phase

---

## 1. Problem Summary

Lượng skill lớn (12 skills) phát triển qua nhiều phiên bản → **không đồng bộ về**:
- Cấu trúc thư mục (7-Zones)
- Format conventions (YAML/Markdown/XML)
- Trace tags standard
- Pipeline stage numbering
- Policy layer (`policy/` vs inlined)
- Zone boundary (`data/`, `policy/`, `knowledge/`)
- SPEC.md existence

---

## 2. Entry Points

| # | Entry | File | Vấn đề |
|---|-------|------|--------|
| EP1 | Pipeline Stage Conflict | `_shared/knowledge/framework.md` §5 vs `skill-planner/SKILL.md` §Pipeline | Stage numbering lệch nhau |
| EP2 | Format-standards duplication | `_shared/knowledge/format-standards.md` + 3 local copies | 4 copies, khác nhau nội dung |
| EP3 | Trace Tags inconsistency | `format-standards.md` §5 vs `framework.md` §7 vs BA skills | 3 format khác nhau |
| EP4 | 7-Zone non-compliance | Nhiều skills thiếu zones | Không skill nào follow đúng 7-Zones |
| EP5 | `policy/` zone undefined | 7-Zones table không có `policy/` nhưng 2 skills dùng | Zone contract bị vi phạm |

---

## 3. Scope Definition

### 3.1 Affected Area
```
skills/ver-3/
├── _shared/                          # 🔴 Trung tâm — sửa 1 ảnh hưởng toàn bộ
│   ├── knowledge/framework.md        # Stage numbering, trace tags, 7-Zones
│   ├── knowledge/format-standards.md # Trace tags, format rules
│   └── schemas/                      # Schema alignment
├── skill-architect/                   # 🟡 policy/ zone, format-standards copy
├── skill-explorer/                    # 🟡 policy/ zone, format-standards missing
├── skill-planner/                     # 🟡 Stage order=2 vs framework, SPEC.md
├── skill-builder/                     # 🟡 SPEC.md, missing templates/, data/
├── skill-knowledge-miner/             # 🟢 Thiếu zones
├── production-code-reviewer/          # 🟢 data/ vs policy/ confusion
├── production-quality-gatekeeper/     # 🟢 data/ vs policy/ confusion
├── skill-security-reviewer/           # 🟢 Minimal structure
├── ba-analyst/                        # 🔴 Không theo 7-Zones
├── ba-elicitor/                       # 🔴 Không theo 7-Zones
├── ba-synthesizer/                    # 🔴 Không theo 7-Zones
└── scripts/                           # 🟢 validate_suite_integrity.py
```

### 3.2 Analysis Dimensions

| Dimension | Skills affected | Severity |
|-----------|----------------|----------|
| Pipeline Stage numbering | skill-planner, skill-builder, framework.md | 🔴 HIGH |
| Trace Tags standard | ALL skills + _shared | 🔴 HIGH |
| 7-Zones structure | ALL skills (0% compliant) | 🔴 HIGH |
| Format-standards duplication | skill-architect, skill-planner, skill-builder | 🟡 MEDIUM |
| policy/ zone undefined | skill-architect, skill-explorer | 🟡 MEDIUM |
| data/ vs policy/ confusion | production-*, skill-planner | 🟡 MEDIUM |
| SPEC.md inconsistency | skill-planner, skill-builder have; others don't | 🟢 LOW |
| BA skills structural gap | ba-analyst, ba-elicitor, ba-synthesizer | 🔴 HIGH |
| Script naming fragmentation | ALL skills | 🟢 LOW |

---

## 4. Impact Analysis

### 4.1 Direct Impact

| Feature | Impact | Reason |
|---------|--------|--------|
| Pipeline execution | ❌ BROKEN | Stage numbering conflict → agent nhầm thứ tự |
| Skill handoff | ⚠️ RISK | Trace tags khác format → handoff contract break |
| Quality Gates | ⚠️ RISK | Gate checklists reference wrong sections |
| Validation scripts | ⚠️ RISK | Script path/naming inconsistency |
| Schema validation | ⚠️ RISK | 4 schemas in _shared but skills reference none |

### 4.2 Indirect Impact

| Feature | Impact | Reason |
|---------|--------|--------|
| LLM context loading | ⚠️ RISK | PD tiers reference files may not exist |
| Cross-skill debugging | ⚠️ RISK | No consistent zone structure |
| New skill creation | ⚠️ RISK | Template không consistent |
| BA → pipeline integration | ❌ BROKEN | BA skills don't follow 7-Zones → cannot plug into pipeline |

### 4.3 Data Flow Affected

```
[skill-explorer] → exploration.md → [skill-architect] → design.md → [skill-planner] → todo.md → [skill-builder]
       ↓                            ↓                            ↓                            ↓
  7-Golden Standards           Zone Mapping                  Trace Tags                  Zone Contract
  (OK)                        (OK)                          ❌ INCONSISTENT               ❌ policy/ vs knowledge/
```

### 4.4 API Contracts Broken

| Contract | Source | Destination | Status |
|----------|--------|-------------|--------|
| `exploration.md §6 → design.md §3` | skill-explorer | skill-architect | ✅ OK |
| `design.md §3 → todo.md tasks` | skill-architect | skill-planner | ⚠️ Trace tags not aligned |
| `quality-matrix.yaml` | production-quality-gatekeeper | skill-planner | ⚠️ Stage numbering off |
| `todo.md → skill files` | skill-planner | skill-builder | ⚠️ policy/ zone undefined |
| `BA skills output → pipeline` | BA skills | skill-architect | ❌ No contract defined |

---

## 5. Call Chain

```
Pipeline Flow (THEORETICAL — theo framework.md):
  Explorer (S0) → Miner (S0.5) → Architect (S1) → Gatekeeper (S2) → SecurityReview → Planner (S3) → HumanGate → Builder (S4)

Pipeline Flow (ACTUAL — theo skill SKILL.md):
  skill-explorer (stage 0)
  skill-knowledge-miner (stage 0.5)
  skill-architect (stage 1)
  production-quality-gatekeeper (stage 2)  ← skill-planner SKILL.md says stage_order: 2
  skill-planner (stage 2)                   ← framework.md §5 says Stage 3 = Planner
  skill-builder (stage 3)                   ← framework.md §5 says Stage 4 = Builder
  production-code-reviewer (stage 4)        ← framework.md §5 says stage 4 = Builder!

CONFLICT: stage numbering lệch 1 ở mọi chỗ!
```

---

## 6. Data Flow Mismatches

### 6.1 Trace Tags — 3 Standards

| Standard | Source | Tags |
|----------|--------|------|
| **A** | `_shared/knowledge/framework.md` §7 | `[TỪ DESIGN §N]`, `[GỢI Ý BỔ SUNG]`, `[TỪ AUDIT TÀI NGUYÊN]`, `[CẦN LÀM RÕ]` |
| **B** | `_shared/knowledge/format-standards.md` §5 | `[TỪ USER INPUT]`, `[TỪ DESIGN §N]`, `[TỪ NGUỒN EXTERNAL]`, `[GỢI Ý BỔ SUNG]`, `[CẦN LÀM RÕ]` |
| **C** | BA skills | `[TỪ INPUT]`, `[SUY LUẬN]`, `[CẦN LÀM RÕ]` |

→ `framework.md` và `format-standards.md` (cùng _shared/) đã conflict với nhau!

### 6.2 Format-standards — 4 Copies

| File | Sync Status |
|------|-------------|
| `_shared/knowledge/format-standards.md` | 🟢 Master |
| `skill-architect/knowledge/format-standards.md` | ❌ Local copy — không rõ sync policy |
| `skill-planner/knowledge/format-standards.md` | ❌ Local copy — không rõ sync policy |
| `skill-builder/knowledge/format-standards.md` | ❌ Local copy — không rõ sync policy |

### 6.3 `policy/` zone — Undefined in 7-Zones

- 7-Zones table (`framework.md` §1): Core, Knowledge, Scripts, Templates, Data, Loop, Assets
- Reality: `skill-architect` và `skill-explorer` có `policy/` zone
- `policy/` chứa L1 content (guardrails, output-spec, workflow)
- `policy/` là de-facto standard cho 2 skills nhưng không được document

---

## 7. Affected Components

### 7.1 Files cần sửa (HIGH priority)

| File | Issue | Type |
|------|-------|------|
| `_shared/knowledge/framework.md` §5 | Stage numbering sai | 🔴 Contract |
| `_shared/knowledge/framework.md` §1 | Thiếu `policy/` zone | 🔴 Contract |
| `_shared/knowledge/framework.md` §7 | Inconsistent trace tags | 🔴 Contract |
| `_shared/knowledge/format-standards.md` §5 | Inconsistent trace tags | 🔴 Contract |
| `skill-planner/SKILL.md` §Pipeline | Stage order = 2 (must be 3) | 🔴 Logic |
| `ba-analyst/SKILL.md` | Missing 7-Zones, wrong trace tags | 🔴 Structure |
| `ba-elicitor/SKILL.md` | Missing 7-Zones, wrong trace tags | 🔴 Structure |
| `ba-synthesizer/SKILL.md` | Missing 7-Zones, wrong trace tags | 🔴 Structure |

### 7.2 Files cần align (MEDIUM priority)

| File | Issue |
|------|-------|
| `skill-architect/knowledge/format-standards.md` | Duplicate — remove or point to _shared |
| `skill-planner/knowledge/format-standards.md` | Duplicate — remove or point to _shared |
| `skill-builder/knowledge/format-standards.md` | Duplicate — remove or point to _shared |
| `skill-architect/policy/` (3 files) | policy/ zone needs formal definition |
| `skill-explorer/policy/` (3 files) | policy/ zone needs formal definition |
| `skill-builder/` | Thiếu templates/, data/ theo 7-Zones |
| `skill-knowledge-miner/` | Thiếu templates/, data/, scripts/ |
| `skill-security-reviewer/` | Thiếu templates/, scripts/ |
| `production-code-reviewer/data/review-rules.yaml` | Move to policy/? |
| `production-quality-gatekeeper/data/quality-matrix.yaml` | Move to policy/? |

### 7.3 Files cần thêm (LOW priority)

| Skill | Missing Zone | Notes |
|-------|-------------|-------|
| skill-builder | `templates/` | Per 7-Zones contract |
| skill-builder | `data/` | Per 7-Zones contract |
| skill-architect | `SPEC.md` | Conventions: planner & builder have it |
| skill-explorer | `SPEC.md` | Conventions: planner & builder have it |
| production-code-reviewer | `SPEC.md` | Nếu cần |
| production-quality-gatekeeper | `SPEC.md` | Nếu cần |
| BA skills | `scripts/`, more zones | Cần restructure lớn |

---

## 8. Evidence

| Evidence | File:Line | Detail |
|----------|-----------|--------|
| Stage conflict | `skills/ver-3/_shared/knowledge/framework.md:100-109` | Pipeline table: Stage 2 = Gatekeeper, Stage 3 = Planner, Stage 4 = Builder |
| Stage conflict | `skills/ver-3/skill-planner/SKILL.md:47` | `stage_order: 2` (should be 3 theo framework) |
| Stage conflict | `skills/ver-3/skill-builder/SKILL.md:43` | `stage_order: 3` (should be 4 theo framework) |
| Trace tag A | `skills/ver-3/_shared/knowledge/framework.md:200-205` | 4 standard tags |
| Trace tag B | `skills/ver-3/_shared/knowledge/format-standards.md:65-70` | 5 different tags (incl. `[TỪ USER INPUT]`, `[TỪ NGUỒN EXTERNAL]`) |
| Trace tag C | `skills/ver-3/ba-elicitor/SKILL.md:20-22` | `[TỪ INPUT]`, `[SUY LUẬN]` |
| 7-Zones table | `skills/ver-3/_shared/knowledge/framework.md:14-23` | No `policy/` zone listed |
| policy/ exists | `skills/ver-3/skill-architect/policy/` | 3 policy files |
| policy/ exists | `skills/ver-3/skill-explorer/policy/` | 3 policy files |
| Format dup | `skills/ver-3/skill-architect/knowledge/format-standards.md` | Local copy |
| Format dup | `skills/ver-3/skill-planner/knowledge/format-standards.md` | Local copy |
| Format dup | `skills/ver-3/skill-builder/knowledge/format-standards.md` | Local copy |
| SPEC.md | `skills/ver-3/skill-planner/SPEC.md` | Exists |
| SPEC.md | `skills/ver-3/skill-builder/SPEC.md` | Exists |
| No SPEC.md | `skills/ver-3/skill-architect/` | Missing |
| BA structure | `skills/ver-3/ba-analyst/` | No scripts/, no data/, no 7-Zones alignment |

---

## 9. Confidence Assessment

```yaml
confidence: 92%
flags:
  - "BA skills integration path với pipeline chưa được document trong framework.md"
  - "policy/ zone có thể là intentional design choice — cần user confirm"
  - "format-standards duplication có intentional reason không rõ"
```

---

## 10. Open Questions

| # | Question | Importance | Suggested Resolution |
|---|----------|------------|---------------------|
| Q1 | `policy/` zone có nên được formalize vào 7-Zones hay move hết content vào knowledge/? | HIGH | Nếu policy/ là L1 content, nên formalize |
| Q2 | Trace tags: chọn standard A (framework.md) hay B (format-standards.md)? | HIGH | Thống nhất 1 standard cho toàn bộ |
| Q3 | BA skills có nên được restructure theo 7-Zones hay giữ nguyên micro-skill format? | HIGH | Nếu BA skills là micro-skills tách rời, có thể không cần 7-Zones |
| Q4 | Stage numbering: framework.md hay skill SKILL.md là truth? | HIGH | framework.md là shared truth — update skills |
| Q5 | format-standards.md local copies: remove hay soft-link? | MEDIUM | Remove local, reference _shared |
| Q6 | data/ vs policy/: run rõ boundary hay merged? | MEDIUM | data/ = static config, policy/ = behavioral rules |

---

## Summary

```
Total issues found: 12
  🔴 HIGH: 5 (Stage numbering, Trace tags, 7-Zones, BA structure, policy/ undefined)
  🟡 MEDIUM: 4 (Format dup, data/ confusion, policy/ migration, missing zones)
  🟢 LOW: 3 (SPEC.md, script naming, BA micro details)

Root causes:
  1. Không có single source of truth được enforce
  2. _shared/ documents tự conflict (framework.md vs format-standards.md)
  3. 7-Zones contract outdated — không reflect policy/ zone
  4. BA skills developed independently from pipeline
  5. Stage numbering never synced after hybrid pipeline change
```

---

> **NO CODE CHANGES** — Context ready for fix phase.
> **Path**: `docs/context-to-work/arch-sync/scope.2026-06-07.md`
> **Next**: Proceed to fix plan — thống nhất 1 source of truth, align all skills.
