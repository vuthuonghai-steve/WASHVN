# Scope Document — Skill-Knowledge-Miner: Phạm vi Triển khai

**Date**: 2026-07-12
**Status**: Initial
**Feature**: skill-knowledge-miner-deploy
**Input Sources**:
- `docs/context-to-work/phase-6-post-explorer/scope.2026-07-12.md` (417 dòng)
- `docs/context-to-work/phase-6-main-pipeline-skills/scope.2026-07-11.md` (712 dòng)
- `Temps/spec/roadmaps/06-skill-build-main-pipeline.md` L163-207 (Stage 0.5 spec)
- `Temps/spec/architects/P6-deconstructor-and-miner/` (4 files — miner-analyzer, dual-mode, adapters)
- `skills/ver-3/_shared/schemas/domain-handbook.schema.yaml` (output contract schema)
- `skills/ver-3/_shared/templates/skill_skeleton.md` (SKILL.md template)
- `skills/ver-3/_shared/templates/drc_contract_template.yaml` (DRC template)
- Filesystem audit: `skills/ver-3/skill-knowledge-miner/` + `.claude/skills/skill-knowledge-miner/`
- Existing pattern: `skills/ver-3/skill-explorer/` (v1.0 reference)
- `.claude/agents/pipeline-orchestrator.md` (Stage 0.5 invocation spec)

---

## §1: Problem Summary

Xác định phạm vi triển khai chi tiết cho **skill-knowledge-miner (Stage 0.5)** — skill tiếp theo trong pipeline Phase 6A sau skill-explorer. Cần:

1. **Phân tích trạng thái hiện tại** — source & deploy
2. **Xác định yêu cầu đầu đủ** từ roadmap + architect specs
3. **Xác định files cần tạo** (7 zones)
4. **Xác định subagents liên quan** (hiện có + cần tạo)
5. **Xác định acceptance criteria** cho build + deploy

---

## §2: Entry Point

| Entry | Path | Vai trò |
|-------|------|---------|
| Skill source | `skills/ver-3/skill-knowledge-miner/` | 7 directories, SKILL.md = 0 bytes |
| Skill deploy | `.claude/skills/skill-knowledge-miner/` | 7 directories, SKILL.md = 0 bytes |
| Roadmap spec | `Temps/spec/roadmaps/06-skill-build-main-pipeline.md` L163-207 | D6-2-x requirements |
| Architect spec (Miner) | `Temps/spec/architects/P6-deconstructor-and-miner/miner-analyzer.md` | CREATE/UPDATE workflow |
| Architect spec (Dual-mode) | `Temps/spec/architects/P6-deconstructor-and-miner/dual-mode-create-update.md` | 3 execution modes |
| Output schema | `skills/ver-3/_shared/schemas/domain-handbook.schema.yaml` | domain-handbook.md validation |
| Pipeline orchestration | `.claude/agents/pipeline-orchestrator.md` L67-69 | Stage 0.5 invocation |
| Reference pattern | `skills/ver-3/skill-explorer/` | v1.0 — cấu trúc mẫu |

---

## §3: Scope Definition

### 3.1 Problem Area

```yaml
scope:
  skill: skill-knowledge-miner
  stage: "Stage 0.5"
  pipeline_position: "After skill-explorer (Stage 0), before skill-architect (Stage 1)"
  
  current_state:
    source: skills/ver-3/skill-knowledge-miner/ — SCAFFOLDED (0 bytes)
    deploy: .claude/skills/skill-knowledge-miner/ — SCAFFOLDED (0 bytes)
    knowledge/: .gitkeep only
    templates/: .gitkeep only
    scripts/: .gitkeep only
    loop/: .gitkeep only
    data/drc.yaml: MISSING
  
  target_state:
    source: 7+ files with full content
    deploy: .claude/skills/skill-knowledge-miner/ — identical copy
    output: domain-handbook.md (validated by domain-handbook.schema.yaml)
```

### 3.2 Boundary

**IN SCOPE**:
- Build 7 files cho skill-knowledge-miner (source tại `skills/ver-3/`)
- Deploy sang `.claude/skills/`
- Xác định subagents cần dùng khi skill chạy (runtime)
- Xác định subagents cần deployed cho pipeline (build-time)
- domain-handbook.md output contract (schema, fallbacks)
- AC-6A verification

**OUT OF SCOPE**:
- Các skill khác trong Phase 6 (architect, gatekeeper, planner, ...)
- Phase 5 closing items
- quality-scorer fix (là task riêng)
- Phase 7, Phase 8

---

## §4: Yêu Cầu Chi Tiết Theo Spec

### 4.1 Roadmap Spec (D6-2-x) — Tổng hợp

```yaml
# Từ Temps/spec/roadmaps/06-skill-build-main-pipeline.md L163-207
skill:
  name: skill-knowledge-miner
  stage: "Stage 0.5"
  category: monolithic-stage
  target_variable: target_skill
  tags: [knowledge-mining, domain-handbook, glossary]
  when_to_use: "After skill-explorer produces exploration.md. Scan Temps/, .claude/, _shared/, related skill's knowledge/ to extract domain terms and patterns."
  output_contract: ".skill-context/{target_skill}/drc-skill-knowledge-miner.yaml"

workflow_phases:
  1. Read exploration.md + business-analysis.md (if available)
  2. Scan workspace: search related skill knowledge/, glossaries, exemplars
  3. Extract terms: ≥10 glossary terms with definitions
  4. Extract anti-patterns: ≥3 with name, symptom, solution
  5. Extract exemplars: ≥1 with name, description, optional reference
  6. Emit: Write domain-handbook.md

acceptance_criteria:
  - domain-handbook.md has ≥10 glossary terms (F6 trigger if <10)
  - anti-patterns section has ≥3 examples with reason
  - exemplars section has ≥1 example with code structure
  - All references use clickable file:// links
  - Schema validates against domain-handbook.schema.yaml
```

### 4.2 Architect Spec (Miner) — CREATE Mode Flow

```yaml
# Từ Temps/spec/architects/P6-deconstructor-and-miner/miner-analyzer.md
standard_flow:
  1. Read business-analysis.md from Context Bus
  2. Scan project documentation for domain specifics
  3. Build domain-handbook.md with 4 components:
     - Keyword Trigger Library — domain anchors + context triggers
     - Success Criteria & Quality Gates — binary pass/fail
     - Error Boundaries & Anti-Patterns — what NOT to do
     - Structural Exemplars — API contracts + sample code

update_rebuild_flow:
  1. Read deconstructed_context from Context Bus
  2. Integrate extracted knowledge into domain-handbook.md
  3. Preserve original advantages_and_intent
  4. Flag any deprecated patterns found in old skill

fallback:
  - F2: Domain-handbook insufficient (glossary < 10 or missing anti-patterns)
  - F6: Glossary terms < 10 after hydration
```

### 4.3 Output Schema (domain-handbook.schema.yaml)

```yaml
# Từ skills/ver-3/_shared/schemas/domain-handbook.schema.yaml
required_fields:
  - skill_name: string (kebab-case)
  - glossary: array (minItems: 10)
    - term: string
    - definition: string
  - anti_patterns: array (minItems: 3)
    - name: string
    - symptom: string
    - solution: string
  - exemplars: array
    - name: string
    - description: string
    - reference_url_or_path: string (optional)
  - domain_anchors: array of strings

optional_fields:
  - success_criteria: array of strings
  - error_boundaries: array of strings
  - structural_exemplars: array of objects
```

### 4.4 Pipeline Orchestration Context

```yaml
# Từ .claude/agents/pipeline-orchestrator.md L67-69
stage_0_5:
  invoke: skill-knowledge-miner via Task
  gate: knowledge-miner hoàn thành gathering
  output: knowledge/ directory với domain references
  next_stage: skill-architect (Stage 1)
```

---

## §5: Files Cần Tạo — 7 Zones Breakdown

### 5.1 File Inventory

| # | File | Zone | Mục đích | Pattern (từ skill-explorer) |
|:-:|:----|:----|:---------|:---------------------------|
| 1 | `SKILL.md` | root | Frontmatter + workflow body + output contract | `skills/ver-3/skill-explorer/SKILL.md` (148 lines) |
| 2 | `knowledge/mining-standards.md` | knowledge/ | Domain mining patterns, source scanning strategies | `skills/ver-3/skill-explorer/knowledge/exploration-standards.md` |
| 3 | `templates/domain-handbook.md.template` | templates/ | Template cho domain-handbook.md output | `skills/ver-3/skill-explorer/templates/exploration.md.template` |
| 4 | `scripts/mine_for_terms.py` | scripts/ | Extract glossary terms from source docs | `skills/ver-3/skill-explorer/scripts/init_context.py` |
| 5 | `scripts/find_antipatterns.py` | scripts/ | Detect anti-patterns from codebase | — (new script) |
| 6 | `loop/mining-checklist.md` | loop/ | Self-verification checklist | `skills/ver-3/skill-explorer/loop/exploration-checklist.md` |
| 7 | `data/drc.yaml` | data/ | DRC contract per template | `_shared/templates/drc_contract_template.yaml` |
| — | `assets/.gitkeep` | assets/ | Giữ nguyên (không cần content) | — |

### 5.2 SKILL.md — Cấu trúc đề xuất

Based on `skill_skeleton.md` template + `skill-explorer` v1.0 pattern:

```yaml
frontmatter:
  name: skill-knowledge-miner
  description: "Skill Stage 0.5. Mine domain knowledge from exploration.md + codebase. Output domain-handbook.md with ≥10 glossary terms, anti-patterns, exemplars."
  suite: WASHVN
  version: 1.0.0
  category: monolithic-stage
  stage: "Stage 0.5"
  target_variable: target_skill
  tags: [knowledge-mining, domain-handbook, glossary]
  when_to_use: "After skill-explorer produces exploration.md. Scan Temps/, .claude/, _shared/, related skill's knowledge/ to extract domain terms and patterns."
  output_contract: ".skill-context/{target_skill}/drc-skill-knowledge-miner.yaml"
```

Required sections (theo pattern v1.0):
1. **Boot Configuration (L0)** — must/must_not rules
2. **Boot Sequence** — read order + progressive disclosure
3. **Workflow Phases** — 6 phases (input → scan → extract terms → extract anti-patterns → extract exemplars → emit)
4. **Phase 2.5 Context Hydrator** — nếu cần thought-cache cho cognitive depth
5. **Phase 3.5 Depth Signal Verification** — META-2.1 binary gates
6. **Output Contract** — domain-handbook.md + criteria + DRC
7. **Acceptance Criteria** — AC từ roadmap spec
8. **Failure Modes** — F2, F6 fallback triggers
9. **Dual-Mode Support** — CREATE vs UPDATE/REBUILD

### 5.3 Scripts Design

**`scripts/mine_for_terms.py`**:
```yaml
purpose: Extract domain terms from exploration.md and project files
input: 
  - .skill-context/{target_skill}/exploration.md
  - .skill-context/{target_skill}/resources/ (optional)
output: JSON list of {term, definition} candidates
features:
  - Parse markdown for bold/italic terms + their definitions
  - Scan code comments for domain terminology
  - Cross-reference with _shared/knowledge/ glossaries
  - Min 10 terms (F6 trigger if <10)
```

**`scripts/find_antipatterns.py`**:
```yaml
purpose: Detect common anti-patterns from codebase patterns
input: 
  - exploration.md (has standards assessment)
  - Related skill's knowledge/ files
output: JSON list of {name, symptom, solution}
features:
  - Scan for "must_not", "cấm", "không", "tránh", "never" patterns
  - Identify TODO/FIXME/hack patterns in existing skill code
  - Cross-reference with _shared/ anti-pattern knowledge
  - Min 3 anti-patterns
```

---

## §6: Subagents Analysis

### 6.1 Subagents Hiện Có (trong `.claude/agents/`)

| Agent | Vai trò | Liên quan đến knowledge-miner? |
|:------|:--------|:----------------------------:|
| `pipeline-orchestrator` | Orchestrate 8-stage pipeline | ✅ **Invokes** knowledge-miner via Task |
| `user-knowledge-ingestor` | Ingest user domain docs | ⚠️ **Tương tự** — ingest domain knowledge, nhưng khác stage |
| `quality-scorer` | META scoring quality | ✅ **Có thể dùng** — score domain-handbook quality |
| `drift-detector` | Check back-link fidelity | ✅ **Có thể dùng** — verify domain-handbook vs exploration.md |
| `design-validator` | Validate design schema | ❌ Không liên quan (Stage 1 scope) |
| `ba-pipeline-runner` | Run BA chain | ❌ Không liên quan (Phase 5) |
| `external-code-reviewer` | External code review | ❌ Không liên quan (Stage 3.5) |
| `branch-orchestrator` | Branch B orchestration | ❌ Không liên quan (SCS ≥3.0) |
| `subagent-forge` | Create new subagents | ❌ Chỉ dùng khi cần tạo agent mới |

**KẾT LUẬN**: **Không cần tạo subagent mới** cho knowledge-miner. Các agent hiện có đủ để support runtime.

### 6.2 Subagents Khả Dụng Khi Skill Chạy (Runtime)

Khi skill-knowledge-miner được invoke, nó có thể sử dụng các subagent sau:

```yaml
runtime_subagents:
  explore:
    role: "Contextual grep để tìm domain terms trong codebase"
    usage: "Phase 2 (scan workspace) — tìm knowledge/ files, glossaries, patterns"
    trigger: "Khi cần grep codebase cho domain-specific terms"
    
  librarian:
    role: "Tra cứu external docs, best practices"
    usage: "Phase 3 (extract exemplars) — tìm reference implementations"
    trigger: "Khi cần external reference cho exemplars"
    
  quality-scorer:
    role: "Score quality của domain-handbook.md"
    usage: "Post-processing verification"
    trigger: "Khi domain-handbook.md đã được tạo"
```

### 6.3 Pipeline Subagents (Build-time)

Khi pipeline-orchestrator dispatch Stage 0.5:

```yaml
pipeline_dispatch:
  orchestrator: pipeline-orchestrator (invokes)
  skill: skill-knowledge-miner (via Task call)
  pre_conditions:
    - skill-explorer đã PASS gate (exploration.md tồn tại)
    - business-analysis.md có sẵn (optional, từ Phase 5)
  post_conditions:
    - domain-handbook.md tồn tại
    - domain-handbook.md validate với schema
    - criteria.md cập nhật
  gate_verification:
    - Có thể dùng quality-scorer hoặc drift-detector để verify output
```

---

## §7: Data Flow

### 7.1 Input → Output

```
Input:
  .skill-context/{target_skill}/
  ├── exploration.md              ← từ skill-explorer (MANDATORY)
  ├── business-analysis.md        ← từ Phase 5 BA (OPTIONAL)
  ├── resources/                  ← từ skill-explorer (OPTIONAL)
  └── criteria.md                 ← từ skill-explorer (OPTIONAL)

Output:
  .skill-context/{target_skill}/
  ├── domain-handbook.md          ← MAIN OUTPUT (MANDATORY)
  ├── criteria.md                 ← UPDATED (nếu có)
  └── drc-skill-knowledge-miner.yaml  ← DRC contract
```

### 7.2 Inter-Skill Flow

```
skill-explorer (Stage 0) → exploration.md
                              ↓
                    skill-knowledge-miner (Stage 0.5)
                              ↓
                    domain-handbook.md
                              ↓
                    skill-architect (Stage 1)
```

### 7.3 Dependencies

| Dependency | Type | Status | Ghi chú |
|-----------|:----:|:------:|---------|
| `domain-handbook.schema.yaml` | Schema | ✅ COMPLETE | `_shared/schemas/` |
| `schema_validator.py` | Validator | ✅ COMPLETE | `_shared/validators/` |
| `drc_contract_template.yaml` | Template | ✅ COMPLETE | `_shared/templates/` |
| `skill_skeleton.md` | Template | ✅ COMPLETE | `_shared/templates/` |
| `exploration.md` (runtime input) | Data | ✅ TỪ EXPLORER | Stage 0 output |
| `business-analysis.md` (runtime) | Data | ⚠️ OPTIONAL | Từ Phase 5 |
| `pipeline-orchestrator` | Agent | ✅ DEPLOYED | Dispatch Stage 0.5 |

---

## §8: Acceptance Criteria

### AC cho Build (kiểm tra sau khi tạo files)

| AC | Check | Method |
|:---|:------|:-------|
| AC-6A-1 | SKILL.md tồn tại, frontmatter valid | `test -f` + yaml parse |
| AC-6A-2 | SKILL.md body ≤ 700 tokens | `wc -c < 3500` |
| AC-6A-3 | ≥4/7 zones populated | `ls` each zone, exclude .gitkeep |
| AC-6A-4 | DRC valid | `python3 drc_resolver.py` |
| AC-6A-5 | `knowledge/mining-standards.md` exists | `test -f` |
| AC-6A-6 | `templates/domain-handbook.md.template` exists | `test -f` |
| AC-6A-7 | `scripts/mine_for_terms.py` exists + executable | `test -x` |
| AC-6A-8 | `scripts/find_antipatterns.py` exists + executable | `test -x` |
| AC-6A-9 | `loop/mining-checklist.md` exists | `test -f` |

### AC cho Domain-Handbook Output (runtime)

| AC | Check | Method |
|:---|:------|:-------|
| AC-MINER-1 | glossary ≥ 10 terms | Schema validation |
| AC-MINER-2 | anti_patterns ≥ 3 entries | Schema validation |
| AC-MINER-3 | exemplars ≥ 1 entry | Schema validation |
| AC-MINER-4 | domain_anchors array present | Schema validation |
| AC-MINER-5 | Schema valid | `schema_validator.py --schema domain-handbook.schema.yaml` |
| AC-MINER-6 | File:// links clickable | grep check |
| AC-MINER-7 | Fallback F2/F6 defined in failure_modes | SKILL.md check |

### AC cho Deploy

| AC | Check | Method |
|:---|:------|:-------|
| AC-DEPLOY-1 | Source → deploy identical | `diff -r` |
| AC-DEPLOY-2 | `.claude/skills/skill-knowledge-miner/SKILL.md` exists | `test -f` |
| AC-DEPLOY-3 | `data/drc.yaml` exists in deploy | `test -f` |

---

## §9: Evidence

<evidence>
  <file>skills/ver-3/skill-knowledge-miner/SKILL.md</file>
  <line>0</line>
  <finding>0 bytes — EMPTY, cần build 7 files từ đầu</finding>
</evidence>

<evidence>
  <file>.claude/skills/skill-knowledge-miner/SKILL.md</file>
  <line>0</line>
  <finding>0 bytes — EMPTY, deploy cũng trống</finding>
</evidence>

<evidence>
  <file>skills/ver-3/skill-knowledge-miner/knowledge/</file>
  <line>0</line>
  <finding>Chỉ .gitkeep — cần tạo mining-standards.md</finding>
</evidence>

<evidence>
  <file>skills/ver-3/skill-knowledge-miner/templates/</file>
  <line>0</line>
  <finding>Chỉ .gitkeep — cần tạo domain-handbook.md.template</finding>
</evidence>

<evidence>
  <file>skills/ver-3/skill-knowledge-miner/scripts/</file>
  <line>0</line>
  <finding>Chỉ .gitkeep — cần tạo mine_for_terms.py + find_antipatterns.py</finding>
</evidence>

<evidence>
  <file>skills/ver-3/skill-knowledge-miner/loop/</file>
  <line>0</line>
  <finding>Chỉ .gitkeep — cần tạo mining-checklist.md</finding>
</evidence>

<evidence>
  <file>skills/ver-3/skill-knowledge-miner/data/</file>
  <line>0</line>
  <finding>Chỉ .gitkeep — data/drc.yaml MISSING</finding>
</evidence>

<evidence>
  <file>Temps/spec/roadmaps/06-skill-build-main-pipeline.md</file>
  <line>163-207</line>
  <finding>D6-2-x spec: frontmatter, 6 workflow phases, acceptance criteria, 7 files cần tạo</finding>
</evidence>

<evidence>
  <file>Temps/spec/architects/P6-deconstructor-and-miner/miner-analyzer.md</file>
  <line>1-30</line>
  <finding>CREATE/UPDATE flow, domain-handbook 4 components, F2/F6 fallback triggers</finding>
</evidence>

<evidence>
  <file>Temps/spec/architects/P6-deconstructor-and-miner/dual-mode-create-update.md</file>
  <line>6-31</line>
  <finding>Dual-mode pipeline: CREATE vs UPDATE/REBUILD -> Miner behavior khác nhau</finding>
</evidence>

<evidence>
  <file>skills/ver-3/_shared/schemas/domain-handbook.schema.yaml</file>
  <line>1-79</line>
  <finding>Schema: required = skill_name, glossary (min10), anti_patterns (min3), exemplars, domain_anchors</finding>
</evidence>

<evidence>
  <file>.claude/agents/pipeline-orchestrator.md</file>
  <line>67-69</line>
  <finding>Stage 0.5: invoke skill-knowledge-miner via Task, gate = gathering complete, output = knowledge/ directory</finding>
</evidence>

<evidence>
  <file>.claude/agents/</file>
  <line>1-9</line>
  <finding>9 agents deployed sẵn — KHÔNG cần tạo agent mới cho knowledge-miner</finding>
</evidence>

<evidence>
  <file>skills/ver-3/skill-explorer/SKILL.md</file>
  <line>1-148</line>
  <finding>Pattern reference: v1.0 SKILL.md — 148 lines, 6 phases, dual-stream, META-2.1 gates. Dùng làm template style cho knowledge-miner</finding>
</evidence>

---

## §10: Confidence Assessment

| Khu vực | Confidence | Lý do |
|---------|:----------:|-------|
| Spec understanding (roadmap) | 95% | D6-2-x spec rõ ràng, đã đọc full |
| Architect spec (miner) | 90% | miner-analyzer.md, dual-mode.md đã đọc |
| Output schema (domain-handbook) | 98% | Schema file đã đọc, rất rõ |
| Files cần tạo (7 zones) | 95% | Dựa trên Phase 6 spec + explorer pattern |
| Subagent requirements | 90% | Đã audit 9 agents — all adequate |
| Effort estimation | 80% | Ước lượng sơ bộ |
| Pipeline integration | 85% | Cần verify pipeline-orchestrator gate sau build |

**Overall Confidence**: **90%** (high)

**Uncertainty Flags**:
- [NHẸ] `mine_for_terms.py` implementation detail — cần quyết định heuristic hay ML-based?
- [NHẸ] `find_antipatterns.py` — cần anti-pattern catalog reference?
- [NHẸ] Dual-mode (CREATE vs UPDATE/REBUILD) — có implement full ngay v1.0 hay chỉ CREATE?

---

## §11: Open Questions

| # | Câu hỏi | Priority | Gợi ý |
|---|---------|:--------:|-------|
| 1 | Dual-mode (CREATE + UPDATE/REBUILD) có implement trong v1.0 không? | **HIGH** | Architect spec có đề cập, roadmap chỉ đề cập CREATE |
| 2 | `business-analysis.md` có bắt buộc là input không? | Medium | Roadmap ghi "if available" |
| 3 | Range mở rộng: có cần thought-cache.yaml cho cognitive depth không? | Low | Pattern từ explorer có, nhưng miner có thể không cần |
| 4 | META-2.1 binary gates có cần cho miner không? | Medium | Explorer có (Phase 3.5), miner có thể cần phiên bản đơn giản hơn |

---

## §12: Task Breakdown — Build Plan

### Phase 1: Tạo Source Files (tại `skills/ver-3/skill-knowledge-miner/`)

```
Task KM-1 — Author SKILL.md
├── Dùng skill_skeleton.md + skill-explorer v1.0 làm template
├── Frontmatter 10 fields (theo D6-2-1 spec)
├── Workflow: 6 phases (input → scan → extract terms → extract anti-patterns → extract exemplars → emit)
├── Output contract: domain-handbook.md + criteria.md + DRC
├── Acceptance criteria: glossary≥10, anti-patterns≥3, exemplars≥1
├── Failure modes: F2 (insufficient), F6 (glossary<10)
└── Body ≤ 700 tokens

Task KM-2 — Author knowledge/mining-standards.md
├── Domain mining patterns
├── Source scanning strategies (codebase, git history, web)
├── Term extraction heuristics
├── Glossary quality criteria
└── Anti-pattern detection guidelines

Task KM-3 — Author templates/domain-handbook.md.template
├── Dựa trên domain-handbook.schema.yaml
├── Sections: glossary, anti-patterns, exemplars, domain_anchors
├── success_criteria + error_boundaries optional
└── YAML frontmatter cho schema validation

Task KM-4 — Author scripts/mine_for_terms.py
├── Input: exploration.md + resources/
├── Output: JSON candidate terms
├── Parse markdown for bold/italic + definition patterns
├── Cross-reference với _shared/knowledge/ glossaries
└── Min 10 terms threshold with warning

Task KM-5 — Author scripts/find_antipatterns.py
├── Scan must_not patterns, TODO/FIXME markers
├── Detect common anti-patterns từ exploration.md
├── Output: JSON candidates {name, symptom, solution}
└── Min 3 anti-patterns threshold

Task KM-6 — Author loop/mining-checklist.md
├── Self-verification checklist
├── Binary pass/fail gates (glossary≥10?, anti-patterns≥3?, exemplars≥1?)
├── Schema validation step
└── Progressive disclosure links

Task KM-7 — Author data/drc.yaml
├── Dùng drc_contract_template.yaml
├── Input: exploration.md
├── Output: domain-handbook.md
├── Upstream: skill-explorer
└── Downstream: skill-architect
```

### Phase 2: Deploy + Verify

```
Task KM-D1 — Deploy sang .claude/skills/
├── cp -r skills/ver-3/skill-knowledge-miner/ .claude/skills/skill-knowledge-miner/
└── Verify: diff -r skills/ver-3/skill-knowledge-miner/ .claude/skills/skill-knowledge-miner/

Task KM-D2 — Run AC-6A verification
├── test -f SKILL.md + frontmatter valid
├── body < 3500 chars
├── ≥4/7 zones populated (exclude .gitkeep)
├── drc_resolver.py verify
└── schema_validator.py verify

Task KM-D3 — Pipeline integration check
├── pipeline-orchestrator có thể invoke skill-knowledge-miner
├── Gate conditions defined
└── Handoff manifest updated
```

### Tổng công sức ước tính

| Phase | Tasks | Effort |
|:------|:-----:|:------:|
| KM-1: SKILL.md | 1 | 0.5-1 session |
| KM-2: knowledge/ | 1 | 0.5 session |
| KM-3: templates/ | 1 | 0.5 session |
| KM-4 + KM-5: scripts/ | 2 | 0.5-1 session |
| KM-6: loop/ | 1 | 0.25 session |
| KM-7: data/drc.yaml | 1 | 0.25 session |
| KM-D1 + KM-D2 + KM-D3: Deploy + Verify | 3 | 0.5 session |
| **Total** | **10** | **~3-4 sessions** |

---

## §13: Tasks Theo Thứ Tự Ưu Tiên

### P0 — BẮT BUỘC (cần cho build):

```
1. Author SKILL.md (frontmatter + 6 workflow phases + output contract)
2. Author knowledge/mining-standards.md
3. Author templates/domain-handbook.md.template
4. Author scripts/mine_for_terms.py
5. Author scripts/find_antipatterns.py
6. Author loop/mining-checklist.md
7. Author data/drc.yaml
```

### P1 — SAU BUILD:

```
8. Deploy skills/ver-3/ → .claude/skills/
9. Run AC-6A verification subset
10. Verify pipeline-orchestrator integration
```

### 🔴 Lưu ý Quan Trọng:

```
11. data/drc.yaml: nhớ tạo — skill-explorer hiện tại cũng thiếu file này!
```

---

**Document Status**: Context Complete — No Code Changes Made
**NO CODE CHANGES MADE** — Document only per context-before-fix skill guardrails

```text
✓ Skill-knowledge-miner spec fully analyzed (roadmap + architect + schema)
✓ Current state verified (SCAFFOLDED — 0 bytes)
✓ 7 files to create identified with content requirements
✓ 9 existing subagents audited — NO new agents needed
✓ 2 runtime subagents identified (explore, librarian) + quality-scorer for verification
✓ Acceptance criteria defined (build + output + deploy)
✓ Effort estimated (~3-4 sessions for full build)
✓ Pipeline integration mapped
```

---

**Document**: `docs/context-to-work/skill-knowledge-miner-deploy/scope.2026-07-12.md`
**Generated by**: context-before-fix skill
**Skill version**: 1.0.0
**Date**: 2026-07-12
