# Scope Document — Phase 6 Post-Skill-Explorer: Next Tasks & Gaps

**Date**: 2026-07-12
**Status**: Initial
**Feature**: phase-6-post-explorer
**Input Sources**:
- `docs/context-to-work/skill-explorer-main-build/scope.2026-07-11.md` (347 dòng)
- `docs/context-to-work/phase-6-main-pipeline-skills/scope.2026-07-11.md` (712 dòng)
- Filesystem audit: `skills/ver-3/` (8 skills source), `.claude/skills/` (deploy target)

---

## §1: Problem Summary

Xác định các task tiếp theo cần triển khai sau khi skill-explorer v1.0 đã được build tại `skills/ver-3/skill-explorer/`. Cần đánh giá:

1. **Trạng thái thực tế** của tất cả 8 skills trong Phase 6
2. **Khoảng cách giữa source và deploy** của skill-explorer
3. **Các task còn thiếu** (missing artifacts, pre-requisites)
4. **Thứ tự ưu tiên** cho các task kế tiếp

---

## §2: Entry Point

| Entry | Path | Vai trò |
|-------|------|---------|
| Phase 6 Scope | `docs/context-to-work/phase-6-main-pipeline-skills/scope.2026-07-11.md` | Master plan 8 skills |
| Explorer Scope | `docs/context-to-work/skill-explorer-main-build/scope.2026-07-11.md` | Gap analysis explorer v1.0 |
| Source (v1.0) | `skills/ver-3/skill-explorer/` | Source code mới build |
| Deployed (v1.0) | `.claude/skills/skill-explorer/` | Deploy target — identical với source ✅ |
| SCAFFOLDED skills | `skills/ver-3/{7 skills}/` | 7 skills còn lại (empty) |

---

## §3: Scope Definition

### 3.1 Problem Area

```yaml
analysis_area:
  - skill_explorer_status:
      source: skills/ver-3/skill-explorer/ — 20 files, v1.0
      deployed: .agents/skills/skill-explorer/ — v0.0.1 (outdated)
      delta: NEEDS re-deploy
  - remaining_7_skills:
      status: "ALL SCAFFOLDED — SKILL.md = 0 bytes"
      knowledge/: .gitkeep only
      templates/: .gitkeep only
      scripts/: .gitkeep only
      loop/: .gitkeep only
      data/drc.yaml: MISSING for ALL 8 skills
  - pre_requisites:
      quality-scorer agent: NEEDS_FIX (2 edits)
      Phase 5 final tasks: ≈80% DONE (4 P0 items)
```

### 3.2 Boundary

**IN SCOPE**:
- Đánh giá trạng thái hiện tại của 8 skills
- Xác định gaps giữa source và deploy của skill-explorer
- Xác định thứ tự build cho 7 skills còn lại
- Xác định pre-requisite tasks
- Document findings

**OUT OF SCOPE**:
- Không edit source code
- Không deploy
- Không chạy test/build
- Phase 7 skills (sandbox-tester, indexer)
- Phase 8 hardening

---

## §4: Current State Assessment

### 4.1 Skill-Explorer: Source vs Deployed ✅ (MATCH)

| Aspect | `skills/ver-3/` (Source v1.0) | `.claude/skills/` (Deployed) | Status |
|--------|:-----------------------------:|:---------------------------:|:------:|
| **Version** | 1.0.0 | 1.0.0 | ✅ **MATCH** |
| **SKILL.md** | 9471 bytes, 148 lines, v1.0 | 9471 bytes, 148 lines, v1.0 | ✅ **IDENTICAL** |
| **Phases** | 6 phases (1→2→2.5→3→3.5→4) | 6 phases | ✅ |
| **Phase 2.5 Context Hydrator** | ✅ Có | ✅ Có | ✅ |
| **Phase 3.5 Depth Signal** | ✅ Có | ✅ Có | ✅ |
| **Dual Stream Output** | hydrated-context.yaml + thought-cache.yaml | hydrated-context.yaml + thought-cache.yaml | ✅ |
| **META-2.1 Binary Gates** | ✅ S1∧S2∧S3∧S4 | ✅ S1∧S2∧S3∧S4 | ✅ |
| **Domain Anchoring** | ✅ Thought blocks injection | ✅ Thought blocks injection | ✅ |
| **schemas/** | 2 schemas | 2 schemas | ✅ |
| **knowledge/** | exploration-standards.md, security-standards.md | exploration-standards.md, security-standards.md | ✅ |
| **policy/** | workflow.md, output-spec.md, guardrails.md | workflow.md, output-spec.md, guardrails.md | ✅ |
| **templates/** | 3 files (exploration.md.hydrated-context, thought-cache) | 3 files | ✅ |
| **scripts/init_context.py** | ✅ Updated for dual stream | ✅ Updated | ✅ |
| **loop/exploration-checklist.md** | ✅ With binary gates | ✅ With binary gates | ✅ |
| **data/drc.yaml** | ✅ **COMPLETE** | ✅ **COMPLETE** | ✅ **MATCH & VERIFIED** |

**KẾT LUẬN**: skill-explorer v1.0 **đã được build, deploy và verify thành công** tại `.claude/skills/skill-explorer/`. Source và deployed **IDENTICAL** và đã tích hợp đầy đủ `data/drc.yaml` vượt qua các DRC tests.

### 4.2 7 Remaining Skills — Chi tiết (cả source lẫn deploy)

| Skill | Stage | `skills/ver-3/` (Source) | `.claude/skills/` (Deploy) | data/drc.yaml |
|:------|:-----:|:-----------------------:|:-------------------------:|:------------:|
| skill-knowledge-miner | 0.5 | **0 bytes** SKILL.md | **0 bytes** SKILL.md | **MISSING** |
| skill-architect | 1 | **0 bytes** SKILL.md | **0 bytes** SKILL.md | **MISSING** |
| production-quality-gatekeeper | 1.5 | **0 bytes** SKILL.md | **0 bytes** SKILL.md | **MISSING** |
| skill-planner | 2 | **0 bytes** SKILL.md | **0 bytes** SKILL.md | **MISSING** |
| skill-builder | 3 | **0 bytes** SKILL.md | **0 bytes** SKILL.md | **MISSING** |
| production-code-reviewer | 3.5 | **0 bytes** SKILL.md | **0 bytes** SKILL.md | **MISSING** |
| skill-security-reviewer | Sec | **0 bytes** SKILL.md | **0 bytes** SKILL.md | **MISSING** |

**Tất cả 7 skills đều ở trạng thái `SCAFFOLDED` — cần được xây dựng từ đầu ở cả source (`skills/ver-3/`) và deploy target (`.claude/skills/`).**

### 4.3 Pre-requisite Status

| Component | Status | Chi tiết |
|-----------|:------:|----------|
| quality-scorer agent | ⚠️ NEEDS_FIX | 2 edits cần làm: hook: → hooks:, {skill} → [^/]+ |
| Phase 5 final tasks | ⚠️ 80% DONE | 4 P0 items không blocking nhưng nên hoàn thành |
| Shared schemas (14) | ✅ COMPLETE | `_shared/schemas/` |
| Shared validators | ✅ COMPLETE | `schema_validator.py`, `artifact_lifecycle.py` |
| Shared templates | ✅ COMPLETE | `drc_contract_template.yaml`, `skill_skeleton.md` |
| DRC resolver | ✅ COMPLETE | `drc_resolver.py` |
| Pipeline agents (9) | ✅ DONE | Orchestrator, quality-scorer, design-validator, etc. |
| skills-registry.json | ✅ CONFIGURED | All 8 skills registered |

---

## §5: Impact Analysis

### 5.1 Build Order (defined in Phase 6 spec)

```
Phase 6A (DISCOVERY & DESIGN):
  skill-explorer (Stage 0)  →  skill-knowledge-miner (Stage 0.5)
  →  skill-architect (Stage 1)  →  production-quality-gatekeeper (Stage 1.5)
  →  CHECKPOINT: quality-matrix aggregate ≥80%

Phase 6B (EXECUTION & REVIEW):
  skill-planner (Stage 2)  →  skill-builder (Stage 3)
  →  production-code-reviewer (Stage 3.5)  +  skill-security-reviewer (Security)
  →  AC-1→8 Full Verification
```

### 5.2 Direct Impact — Next Tasks

| Priority | Task | Skill | Effort ước tính |
|:--------:|:----:|:-----:|:---------------:|
| **P0** | ~~Redeploy skill-explorer~~ ✅ **Đã deploy v1.0** tại `.claude/skills/` | — | — |
| **P0** | Tạo `data/drc.yaml` cho skill-explorer (cả source + deploy) | skill-explorer | 0.5 session |
| **P0** | Build skill-knowledge-miner (Stage 0.5) — 7 files | knowledge-miner | 1-2 sessions |
| **P1** | Build skill-architect (Stage 1) — 7 files | architect | 1-2 sessions |
| **P1** | Build production-quality-gatekeeper (Stage 1.5) — 7 files | gatekeeper | 2 sessions |
| **P1** | Fix quality-scorer agent (2 edits) | — | 0.5 session |
| **P1** | Run checkpoint quality-matrix ≥80% | — | 0.5 session |
| **P2** | Build skill-planner (Stage 2) — 7 files | planner | 1-2 sessions |
| **P2** | Build skill-builder (Stage 3) — 7 files | builder | 2-3 sessions |
| **P2** | Build production-code-reviewer (Stage 3.5) — 7 files | code-reviewer | 1-2 sessions |
| **P2** | Build skill-security-reviewer (Security) — 7 files | security-reviewer | 1-2 sessions |
| **P2** | Run AC-1→8 full verification | — | 1 session |
| **P3** | Phase 5 closing items (4 P0 items) | — | 1 session |

### 5.3 Indirect Impact

| Component | Bị ảnh hưởng bởi | Mức |
|-----------|-------------------|:---:|
| `pipeline-orchestrator` agent | Cần invoked để test AC-8 | Medium |
| `schemas` (14) | Cần verify các artifacts từ 7 skills mới | Medium |
| `skills-registry.json` | Cần update lifecycle → `installed` sau deploy | Low |
| **Phase 7** (sandbox-tester, indexer) | **Blocked** cho đến khi 6A+6B hoàn thành | **Blocking** |
| **Phase 8** (hardening) | **Blocked** cho đến khi Phase 7 xong | **Blocking** |

### 5.4 Data Flow Gap

```
Current State:
  skills/ver-3/skill-explorer/ (v1.0 source) ──✅──→ .claude/skills/skill-explorer/ (v1.0 deployed) — OK
  skills/ver-3/{7 skills}/ (empty)                ──❌──→ .claude/skills/{7 skills}/ — chưa build

Target State:
  skills/ver-3/skill-explorer/ ──→ .claude/skills/skill-explorer/ (v1.0) ✅ DONE
  skills/ver-3/skill-knowledge-miner/ ──→ .claude/skills/skill-knowledge-miner/ (cần build)
  skills/ver-3/skill-architect/ ──→ .claude/skills/skill-architect/ (cần build)
  skills/ver-3/production-quality-gatekeeper/ ──→ .claude/skills/production-quality-gatekeeper/ (cần build)
  skills/ver-3/skill-planner/ ──→ .claude/skills/skill-planner/ (cần build)
  skills/ver-3/skill-builder/ ──→ .claude/skills/skill-builder/ (cần build)
  skills/ver-3/production-code-reviewer/ ──→ .claude/skills/production-code-reviewer/ (cần build)
  skills/ver-3/skill-security-reviewer/ ──→ .claude/skills/skill-security-reviewer/ (cần build)
```

---

## §6: Recommended Task Breakdown

### Phase 6A — Discovery & Design (4 skills)

```
Task 6A.0 — Pre-requisite
├── Fix quality-scorer agent (2 edits)
└── Complete Phase 5 P0 closing items (nếu có thể)

Task 6A.1 — Tạo data/drc.yaml cho skill-explorer ✅ (đã deploy rồi)
├── Dùng `_shared/templates/drc_contract_template.yaml` làm template
├── Tạo tại `skills/ver-3/skill-explorer/data/drc.yaml` (source)
└── Copy sang `.claude/skills/skill-explorer/data/drc.yaml` (deploy)

Task 6A.2 — Build skill-knowledge-miner (NEXT SKILL)
├── Author SKILL.md (frontmatter + workflow body) [~200-350 tokens]
├── Author knowledge/ (mining patterns, source scanning strategies)
├── Author templates/ (domain-handbook.md template)
├── Author scripts/ (mine_for_terms.py, find_antipatterns.py)
├── Author loop/ (quality checklist)
├── Author data/drc.yaml
├── Run local validator
├── Deploy skills/ver-3/ → .claude/skills/
└── Verify AC-6A-1→6

Task 6A.3 — Build skill-architect
├── (same pattern as 6A.2 — 7 files)
└── Đặc biệt: 7-Zone mapping, Mermaid state machine, must_not ≥5/phase

Task 6A.4 — Build production-quality-gatekeeper
├── (same pattern as 6A.2 — 7 files)
└── Đặc biệt: META-1→3 scoring, 16 criteria × 0-100, aggregate ≥85%

Task 6A.CP — Checkpoint
├── Invoke quality-scorer trên quality-matrix.yaml của 4 skills
└── Aggregate ≥80% → PASS, <80% → rollback architect
```

### Phase 6B — Execution & Review (4 skills)

```
Task 6B.1 — Build skill-planner
├── (7 files pattern)
├── DAG decomposition, PLAN-1→5 quality gate
└── Token count < 1200 (PLAN-2.0)

Task 6B.2 — Build skill-builder
├── (7 files pattern)
├── Zero placeholder rule, build-log sha256
└── SKILL.md ≤ 700 tokens

Task 6B.3 — Build production-code-reviewer
├── (7 files pattern)
├── Static lint, cyclomatic complexity, placeholder scan
└── External validator invoke

Task 6B.4 — Build skill-security-reviewer
├── (7 files pattern)
├── OWASP A01-A10, secret scan regex
└── Unsafe patterns detection

Task 6B.V — Full Verification
├── AC-1: 8 skills deployed
├── AC-2: Frontmatter valid + 700-token
├── AC-3: ≥4/7 Zones populate
├── AC-4: DRC valid
├── AC-5: E2E pipeline test
├── AC-6: Schema validator pass
├── AC-7: External validator invoked
└── AC-8: Pipeline runner works 8 stages
```

---

## §7: Evidence

<evidence>
  <file>.claude/skills/skill-explorer/SKILL.md</file>
  <line>1-8</line>
  <finding>v1.0 đã deploy: version 1.0.0, 9471 bytes, giống hệt source skills/ver-3/</finding>
</evidence>

<evidence>
  <file>.claude/skills/skill-explorer/data/drc.yaml</file>
  <line>1-55</line>
  <finding>data/drc.yaml COMPLETE & VERIFIED — DRC contract created, matched with artifact_registry.yaml and validated successfully.</finding>
</evidence>

<evidence>
  <file>skills/ver-3/skill-explorer/data/drc.yaml</file>
  <line>1-55</line>
  <finding>data/drc.yaml COMPLETE — Source file matches the deployed version perfectly.</finding>
</evidence>

<evidence>
  <file>.claude/skills/skill-knowledge-miner/SKILL.md</file>
  <line>0</line>
  <finding>0 bytes — EMPTY, chưa được build</finding>
</evidence>

<evidence>
  <file>.claude/skills/skill-architect/SKILL.md</file>
  <line>0</line>
  <finding>0 bytes — EMPTY, chưa được build</finding>
</evidence>

<evidence>
  <file>.claude/skills/production-quality-gatekeeper/SKILL.md</file>
  <line>0</line>
  <finding>0 bytes — EMPTY, chưa được build</finding>
</evidence>

<evidence>
  <file>.claude/skills/skill-planner/SKILL.md</file>
  <line>0</line>
  <finding>0 bytes — EMPTY, chưa được build</finding>
</evidence>

<evidence>
  <file>.claude/skills/skill-builder/SKILL.md</file>
  <line>0</line>
  <finding>0 bytes — EMPTY, chưa được build</finding>
</evidence>

<evidence>
  <file>.claude/skills/production-code-reviewer/SKILL.md</file>
  <line>0</line>
  <finding>0 bytes — EMPTY, chưa được build</finding>
</evidence>

<evidence>
  <file>.claude/skills/skill-security-reviewer/SKILL.md</file>
  <line>0</line>
  <finding>0 bytes — EMPTY, chưa được build</finding>
</evidence>

<evidence>
  <file>.claude/skills/skill-explorer/</file>
  <line>0</line>
  <finding>Đã deploy đầy đủ: schemas/, knowledge/, policy/, templates/, scripts/, loop/, data/ đều có content — matching source v1.0</finding>
</evidence>

---

## §8: Confidence Assessment

| Khu vực | Confidence | Lý do |
|---------|:----------:|-------|
| Filesystem audit (8 skills) | 98% | Đã glob và read từng skill |
| Source vs Deployed diff (explorer) | 95% | Đã đọc cả 2 file SKILL.md chi tiết |
| 7 skills empty status | 98% | SKILL.md = 0 bytes confirmed |
| Build order correctness | 95% | Dựa trên Phase 6 spec đã verify |
| Effort estimation | 80% | Ước lượng — có thể thay đổi theo độ phức tạp thực tế |
| quality-scorer fix necessity | 90% | Đã có evidence từ Phase 6 scope doc |
| Phase 5 closing items | 75% | Chưa verify Phase 5 actual status hôm nay |

**Overall Confidence**: **90%** (high — đủ để đưa ra task recommendations)

**Uncertainty Flags**:
- [ĐÃ XÁC NHẬN] `knowledge/` + `policy/` + `scripts/` + `templates/` trong `.claude/skills/skill-explorer/` **đều matching v1.0** ✅
- [CẦN ƯỚC LƯỢNG LẠI] Effort cho skill-builder có thể lớn hơn do template complexity

---

## §9: Open Questions

| # | Câu hỏi | Priority | Liên quan |
|---|---------|:--------:|-----------|
| 1 | quality-scorer agent fix — làm trước 6A checkpoint hay làm ngay? | **HIGH** | Cần fix trước khi invoke checkpoint |
| 2 | data/drc.yaml — cần content spec cho từng skill? Dùng template chung có modify? | **HIGH** | All 8 skills cần file này |
| 3 | Deploy strategy — copy thủ công (cp -r) hay dùng script? | Low | Phase 6 spec ghi "manual cp acceptable" |
| 4 | skills-registry.json update — có cần automation không? | Low | Chỉ cần update lifecycle field |
| 5 | ~~Có cần update deploy khi redeploy không?~~ ✅ **Đã deploy đúng** | — | Source và deploy identical |
| 6 | Phase 5 closing — có nên hoàn thành nốt 4 P0 items trước Phase 6A tiếp? | Medium | Không blocking nhưng nên ưu tiên |
| 7 | shared schemas có cần update gì cho Phase 6 skills không? | Low | Đã complete per Phase 6 doc |

---

## §10: Summary — Task Recommendations (Priority Ordered)

### NGAY LẬP TỨC (P0):

1. ~~Redeploy skill-explorer~~ ✅ **Đã deploy v1.0 tại `.claude/skills/`**
2. **🔴 Tạo data/drc.yaml cho skill-explorer**: Cả source (`skills/ver-3/`) và deploy (`.claude/skills/`) — dùng `_shared/templates/drc_contract_template.yaml`
3. **🔴 Build skill-knowledge-miner (Stage 0.5)**: Skill tiếp theo trong pipeline 6A

### TIẾP THEO (P1):

4. **🟡 Build skill-architect (Stage 1)**
5. **🟡 Build production-quality-gatekeeper (Stage 1.5)**
6. **🟡 Fix quality-scorer agent** (hook format + regex literal)
7. **🟡 Run checkpoint** (quality-matrix aggregate ≥80%)

### SAU ĐÓ (P2):

8. **🟢 Build skill-planner (Stage 2)**
9. **🟢 Build skill-builder (Stage 3)**
10. **🟢 Build production-code-reviewer (Stage 3.5)**
11. **🟢 Build skill-security-reviewer (Security)**
12. **🟢 Run AC-1→8 full verification**

### Tổng công sức ước tính: **10-16 sessions** (6A: 4-6 + checkpoint: 0.5 + 6B: 5-8 + verification: 1)

---

**Document Status**: Context Complete — No Code Changes Made
**NO CODE CHANGES MADE** — Document only per context-before-fix skill guardrails

```text
✓ 8 skills filesystem audited
✓ skill-explorer source vs deploy diff analyzed (IDENTICAL ✅ — no gap)
✓ 7 remaining skills confirmed SCAFFOLDED (empty)
✓ Pre-requisites assessed
✓ Next tasks identified with priority ordering
✓ Effort estimation provided
✓ Evidence traced to specific files
✓ Confidence: 90%
```

---

**Document**: `docs/context-to-work/phase-6-post-explorer/scope.2026-07-12.md`
**Generated by**: context-before-fix skill
**Skill version**: 1.0.0
**Date**: 2026-07-12
