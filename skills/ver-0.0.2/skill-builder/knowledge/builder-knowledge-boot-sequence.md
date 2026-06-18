# Builder Knowledge Boot Sequence (Boot v2)
# [TỪ DESIGN §3 knowledge/builder-knowledge-boot-sequence.md (NEW, KG-1, P1)]
# [TỪ BA §6 KG-1, FR-01, HANDBOOK §10.3 #4]
# [TỪ sibling: skills/ver-0.0.2/skill-architect/knowledge/knowledge-boot-sequence.md]

> **Usage**: Load tại Phase 1 (PREPARE & Evaluate) của skill-builder. Mô tả cách scan `data/builder-knowledge-sources.yaml` để routing Tier 1/2/3 files theo đúng nhu cầu của mỗi phase.

---

## 1. Mục đích

Builder knowledge scan v2 thay thế static "Boot Sequence" trong SKILL.md ver-0.0.2. Thay vì load tất cả `../_shared/knowledge/*` cứng nhắc, v2 routing động dựa trên registry `data/builder-knowledge-sources.yaml` với:
- **Tier 1 (mandatory)**: luôn load tại boot
- **Tier 2 (conditional)**: load theo phase cần
- **Tier 3 (on-demand)**: load manual khi cần Mermaid diagrams, fidelity case studies, migration guide

## 2. Scan Order

```
Step 1: Read data/builder-knowledge-sources.yaml
  → Build registry: {KS-01: {path, tier, priority, load_condition}}

Step 2: Tier 1 filter (tier=1, priority=P0)
  → Load: SKILL.md + policy/skill-builder.yaml + data/builder-knowledge-sources.yaml + loop/build-checklist.yaml

Step 3: Phase detection
  → Determine current phase (PH1-PH5) from todo.md or user request

Step 4: Tier 2 filter (tier=2, load_condition matches current phase)
  → Load: knowledge/architect.md (PH1-PH3), knowledge/builder-knowledge-boot-sequence.md (this file), knowledge/skill-builder-script-boundary-policy.md (PH3 §3), knowledge/build-guidelines.md (PH3), knowledge/builder-token-budget.md (PH4), knowledge/anthropic-skill-standards.md (PH3 first file), templates/build-log.md.template (PH5), examples/build-exemplars.md (PH3)

Step 5: Tier 3 filter (tier=3, manual reference)
  → Hold for explicit request: knowledge/build-visualization-guidelines.md, examples/fidelity-checks.md, docs/MIGRATION-0.0.2-to-0.0.3.md
```

## 3. Registry Schema (KS-01..KS-07)

Mỗi entry trong `data/builder-knowledge-sources.yaml` follow schema:

```yaml
- id: "KS-01"
  path: "SKILL.md"
  tier: 1
  priority: "P0"
  load_condition: "always"
  description: "L0 anchor — persona + 5-phase workflow summary + routing map"
- id: "KS-02"
  path: "policy/skill-builder.yaml"
  tier: 1
  priority: "P0"
  load_condition: "always"
  description: "L1 working policy — G1-G8 guardrails + must/must_not + thresholds"
- id: "KS-03"
  path: "knowledge/architect.md"
  tier: 2
  priority: "P0"
  load_condition: "phase_1_to_3"
  description: "Builder-specific 10 guardrails (G1-G10)"
- id: "KS-04"
  path: "knowledge/skill-builder-script-boundary-policy.md"
  tier: 2
  priority: "P0"
  load_condition: "phase_3_zone_design"
  description: "scripts/ zone deterministic boundary (KG-2)"
- id: "KS-05"
  path: "knowledge/builder-token-budget.md"
  tier: 2
  priority: "P0"
  load_condition: "phase_4_verify"
  description: "L0/L1/L2/L3 token budget concrete numbers (KG-8)"
- id: "KS-06"
  path: "examples/build-exemplars.md"
  tier: 2
  priority: "P1"
  load_condition: "phase_3_abstract_mapping"
  description: ">=2 concrete build examples (leaf skill + meta-skill w/ SSP)"
- id: "KS-07"
  path: "loop/build-checklist.yaml"
  tier: 1
  priority: "P0"
  load_condition: "always"
  description: "v2.0.0 quality gate with tier_knowledge_parity section"
```

## 4. Phase-to-Tier Mapping

| Phase | Tier 1 (already loaded) | Tier 2 (load now) | Tier 3 (on-demand) |
|-------|------------------------|-------------------|--------------------|
| PH1 PREPARE | SKILL.md, policy/, data/, loop/ | knowledge/architect.md, knowledge/builder-knowledge-boot-sequence.md (this file), knowledge/anthropic-skill-standards.md | — |
| PH2 CLARIFY | (same) | (none new) | — |
| PH3 BUILD | (same) | knowledge/build-guidelines.md, knowledge/skill-builder-script-boundary-policy.md, examples/build-exemplars.md | knowledge/build-visualization-guidelines.md (Mermaid) |
| PH4 VERIFY | (same) | knowledge/builder-token-budget.md, examples/fidelity-checks.md | — |
| PH5 DELIVER | (same) | templates/build-log.md.template | docs/MIGRATION-0.0.2-to-0.0.3.md (if migrating) |

## 5. Anti-Pattern: Context Overloading

❌ **KHÔNG làm** (v0.0.2 anti-pattern):
```
Boot Sequence: Read ALL of these before doing ANYTHING:
1. knowledge/architect.md
2. knowledge/build-guidelines.md
3. knowledge/anthropic-skill-standards.md
4. loop/build-checklist.yaml
5. loop/build-log.md.template
```

✅ **LÀM ĐÚNG** (v2.0.3):
```
Boot (Tier 1): SKILL.md + policy/skill-builder.yaml + data/builder-knowledge-sources.yaml + loop/build-checklist.yaml
PH1: + knowledge/architect.md, knowledge/anthropic-skill-standards.md
PH3: + knowledge/build-guidelines.md, knowledge/skill-builder-script-boundary-policy.md, examples/build-exemplars.md
PH4: + knowledge/builder-token-budget.md
PH5: + templates/build-log.md.template
```

## 6. Fallback: When Registry Empty

If `data/builder-knowledge-sources.yaml` is missing or empty:
- Halt at Phase 1 (Boot step)
- Emit `[CẦN LÀM RÕ: data/builder-knowledge-sources.yaml missing]`
- Use legacy static Boot Sequence from skill-builder ver-0.0.2 as fallback (with WARN log)
- Continue with `LIMITED KNOWLEDGE` warning in SKILL.md frontmatter

## 7. Migration Note (ver-0.0.2 → 0.0.3)

| Aspect | v0.0.2 | v0.0.3 |
|--------|--------|--------|
| Boot logic | Hardcoded list in SKILL.md | Dynamic registry `data/builder-knowledge-sources.yaml` |
| Tier resolution | Implicit (3 levels in SKILL.md) | Explicit (registry schema with tier/priority/load_condition) |
| Fallback | None | Legacy static + LIMITED KNOWLEDGE warning |
| Extensibility | Add knowledge file → update SKILL.md | Add knowledge file → update registry only |
