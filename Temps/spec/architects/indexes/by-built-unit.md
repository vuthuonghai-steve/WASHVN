# Index by Built Unit — Completion Inventory

> **Mục đích:** Single Source of Truth ánh xạ mọi unit ĐÃ BUILD (skills, agents, hooks, schemas) ↔ spec stage ↔ lifecycle.
> Dùng làm **completion checklist** — khi dự án hoàn thành, sweep file này để đảm bảo KHÔNG miss bất kỳ unit nào đã xây dựng.
> Spec chỉ định nghĩa BA ở dạng 1 stage (BA Elicitor). 3-skill BA chain + ba-pipeline-runner + quality-scorer là extension build OUTSIDE spec gốc → được ghi nhận tại đây để hết drift.

---

## 🤖 Agents (`.claude/agents/`)

| Agent | Spec stage / role | Lifecycle | Notes |
|:---|:---|:---|:---|
| `pipeline-orchestrator` | P4 Orchestrator (Branch B, SCS≥3.0) | built | KHÔNG wire BA (by design — BA ở intake L0) |
| `ba-pipeline-runner` | **BA chain runner** (extension, not in spec) | built | Gọi elicitor→analyst→synthesizer độc lập qua Task |
| `ba-elicitor` (agent) | BA Stage -1 executor wrapper | built | Wrapper: chạy skill `ba-elicitor`, trả TEXT (không Write) |
| `ba-analyst` (agent) | BA Stage -0.5 executor wrapper | built | Wrapper: chạy skill `ba-analyst`, trả TEXT |
| `ba-synthesizer` (agent) | BA Stage -0.2 executor wrapper | built | Wrapper: chạy skill `ba-synthesizer`, trả TEXT |
| `quality-scorer` | maps to P1 **Spec Gatekeeper** META-scoring | built | Tách chức năng scoring của Gatekeeper |
| `design-validator` | P1 Spec Gatekeeper (schema validation) | built | |
| `drift-detector` | P3 Drift Detector | built | |
| `external-code-reviewer` | P7 Code Reviewer (post-build) | built | |
| `branch-orchestrator` | P4 Orchestrator (SCS≥3.0 trigger) | built | |
| `subagent-forge` | Agent authoring (meta) | built | |
| `user-knowledge-ingestor` | P1/P2 knowledge ingest | built | |
| `_archive/`, `_staging/` | — | parked | không active |

## 🛡️ Hooks (`.claude/hooks/`)

| Hook | Spec phase | Lifecycle |
|:---|:---|:---|
| `registry.yaml` | P0 state ledger | built |
| `validate-state-ledger.sh` | P0 | built |
| `events/` | P5 fallback/audit | built |
| `tests/` | P5 verification | built |

> BA-specific hooks (`anti-recursion.sh`, `ba-write-confinement.sh`) nằm trong `ba-synthesizer/scripts/hooks/` — chưa registered vào global `.claude/hooks/registry.yaml` (known minor gap).

## 📦 Skills (`.claude/skills/` + `skills/ver-3/`)

### BA Chain (extension — not in original spec)

| Skill | Spec stage (assigned) | Lifecycle | DRC output |
|:---|:---|:---|:---|
| `ba-elicitor` | **BA Stage -1** (L0 Intake) | built/verified-deploy | `elicitation-report.md` |
| `ba-analyst` | **BA Stage -0.5** (L0) | built/verified-deploy | `analysis-report.md` |
| `ba-synthesizer` | **BA Stage -0.2** (L0) | built/verified-deploy | `business-analysis.md` |

### Main 8-Stage Pipeline (spec-defined)

| Skill | Spec stage | Lifecycle |
|:---|:---|:---|
| `skill-explorer` | Stage 0 | built |
| `skill-knowledge-miner` | Stage 0.5 (L1) | built |
| `skill-architect` | Stage 1 (L2) | built |
| `production-quality-gatekeeper` | Stage 1.5 / P1 Gatekeeper | built |
| `skill-planner` | Stage 2 (L3) | built |
| `skill-builder` | Stage 3 (L4) | built |
| `production-code-reviewer` | Stage 3.5 (L4) | built |
| `skill-security-reviewer` | Stage 3.5 (L4) | built |
| `sandbox-tester` | Stage 4 (L4) | built |
| `indexer` | Stage 5 (L4) | built |

### Support / Adjacent

| Skill | Spec stage | Lifecycle |
|:---|:---|:---|
| `context-before-fix` | L0 Intake-adjacent (problem scoping) | built |
| `roadmaps/` | Không phải skill — roadmap docs (`05-skill-build-ba-pipeline.md` cover BA chain) | docs |

## 📐 Schemas & Shared (`.claude/skills/_shared/`, `skills/ver-3/_shared/`)

| Artifact | Spec phase | Lifecycle |
|:---|:---|:---|
| 14 schemas (YAML+JSON): exploration, analysis, synthesis, design, criteria, elicitation, verification, review-report, build-log, todo, audit-metrics, security-review, domain-handbook, quality-matrix | P0/P1/P3 | built |
| `artifact_registry.yaml` | P0 | built (có 3 BA entries) |
| `drc_contract_template.yaml` | P4 DRC | built |
| `28 test fixtures` (valid+broken pairs) | P5 | built |
| `schema_validator.py`, `drc_resolver.py` | P0/P4 | built |

## ✅ Completion Sweep Protocol

Khi dự án hoàn thành, chạy checklist này để đảm bảo 0 miss:

1. Mọi agent trong `.claude/agents/` (trừ `_archive/_staging`) có entry ở bảng trên.
2. Mọi skill trong `.claude/skills/` có entry + `lifecycle ∈ {built, verified-deploy, installed}`.
3. Mọi schema trong `_shared/schemas/` có entry + validator PASS.
4. `skills-registry.json` có entry cho mọi skill built (3 BA + 10 main + 2 support).
5. `artifact_registry.yaml` reference đúng path cho mọi artifact (incl. 3 BA outputs).

> **Drift đã giải quyết:** BA 3-skill chain + ba-pipeline-runner + quality-scorer từng là undefined trong spec → nay ghi nhận tại index này. Future reader thấy BA = Stage -1→-0.2 chain, không phải 1 stage đơn.

> **⚠️ Dispatch cơ chế (quan trọng):** `ba-pipeline-runner` gọi bộ 3 qua `Task(subagent_type=ba-elicitor/analyst/synthesizer)`. Claude Code `Task` chỉ resolve **agent name**, không resolve skill name → cần 3 **wrapper agents** (`.claude/agents/ba-{elicitor,analyst,synthesizer}.md`), mỗi agent mang skill qua `skills:` + gọi `Skill` tool.
>
> **🚫 Platform write guard:** Claude Code CẤM subagent ghi file (chỉ trả text). Vì vậy wrapper agents KHÔNG có `Write` — chúng trả nội dung artifact dưới dạng TEXT. `ba-pipeline-runner` (agent cha, có `Write`) mới là người **persist** toàn bộ artifact vào `.skill-context/{feature}/ba-*/`. Gate check = file tồn tại trên disk do runner ghi. Nếu sửa sai (cho wrapper Write) → Stage 2/3 bị platform block → pipeline dừng (F2).
