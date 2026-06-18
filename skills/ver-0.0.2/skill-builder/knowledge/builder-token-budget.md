# Builder Token Budget — Concrete Numbers per Zone (KG-8)
# [TỪ DESIGN §3 knowledge/builder-token-budget.md (NEW, KG-8, P0 — promoted from P2 per R3 mitigation)]
# [TỪ BA §6 KG-8, NFR-03, HANDBOOK §6.3 §6.4]

> **Usage**: Load tại Phase 4 (VERIFY) khi chạy token budget check. Cung cấp concrete numbers cho L0/L1/L2/L3 token budgets + action plan khi vượt.

---

## 1. L0/L1/L2/L3 Token Budget Table

| Layer | Location | Target (tokens) | Warning (tokens) | Hard Cap (tokens) | Split Action |
|-------|----------|------------------|------------------|-------------------|--------------|
| **L0** | `SKILL.md` | 150-400 | 500-700 | 700 | Extract L1 content → `policy/{name}.yaml` |
| **L1** | `policy/*.yaml` | 400-1200 | 1200-1500 | 1500 | Split into multiple policy files by domain (e.g., `policy/guardrails.yaml`, `policy/workflow.yaml`) |
| **L2** | `knowledge/*.md` | 400-2500/file | 2500-3000 | 3000 | Split into multiple files by topic; link from SKILL.md at relevant phase |
| **L3** | `examples/*.md`, `loop/*.md` | 400-1500/file | 1500-2000 | 2000 | Same as L2 |

## 2. SKILL.md Split Recipe (khi vượt 700 tokens)

```yaml
# Before split: SKILL.md = 1200 tokens
# After split: SKILL.md = 380 tokens, policy/skill-builder.yaml = 850 tokens

# SKILL.md body (L0 anchor, ≤ 400 tokens):
# - YAML frontmatter (name, description, version, suite, tags, when_to_use)
# - <instructions> XML wrapper (5-7 imperative rules)
# - <context> XML wrapper (boot sequence summary, 1-2 lines per Tier 1 file)
# - <output_contract> XML wrapper (3-line DRC summary)
# - Workflow Progress Tracker (5 phases checklist)

# policy/skill-builder.yaml body (L1 working policy, ≤ 1200 tokens):
# - guardrails: G1-G8 with severity + description + must/must_not
# - must:/must_not: priority_order
# - placeholder_threshold: {pass, warning, fail}
# - token_budget: per zone
# - zone_contract: enforcement spec
# - output_contract: DRC template
# - progressive_disclosure: tier1/tier2/tier3 routing
```

## 3. Measurement Method

```python
import tiktoken

def count_tokens(text: str) -> int:
    enc = tiktoken.get_encoding("cl100k_base")
    return len(enc.encode(text))

# Fallback (no tiktoken):
# Vietnamese: ~3 chars/token
# English: ~4 chars/token
# Code: ~4 chars/token
```

`scipts/validate_skill.py` uses tiktoken cl100k_base for accuracy.

## 4. Enforcement

- **PH3 BUILD**: After writing SKILL.md, count tokens. If > 700, HALT and split to L1.
- **PH4 VERIFY**: Re-count after all files written. If any file exceeds hard cap, FAIL.
- **PH5 DELIVER**: Include token_count in build-log.md quality_metrics block.

## 5. Why L0 ≤ 400 (Q3 RESOLVED)?

| Target | Rationale |
|--------|-----------|
| 150-400 (good) | LLM context efficiency; SKILL.md is anchor not encyclopedia |
| 500-700 (warning) | Still acceptable for complex orchestrators |
| > 700 (SPLIT) | Token bloat; LLM wastes context on policy not anchor rules |

Per `design.md §9 Q3 RESOLVED`: SKILL.md 0.0.3 self-target = **400 tokens strict**, 700 = hard cap.

## 6. Aggregate Budget per Skill

Total budget across all zones of a built skill:

```yaml
aggregate_budget:
  L0: 400
  L1: 1200
  L2: "5 files × 2500 = 12500"
  L3: "3 files × 1500 = 4500"
  scripts: "no limit (code, not prose)"
  templates: "no limit (scaffolds)"
  total_prose: "≤ 18600 tokens"
```

## 7. Reference: Sibling skill-architect v0.0.2

| File | skill-architect token count | skill-builder 0.0.3 target |
|------|------------------------------|----------------------------|
| SKILL.md | ~520 (warning zone) | 400 strict |
| policy/*.yaml | 0 (uses MD policy) | 1200 (L1) |
| knowledge/*.md | 6 files, avg 800 | 7 files, avg 1500 |

skill-architect 0.0.2 SKILL.md is in warning zone (500-700). skill-builder 0.0.3 fixes this by extracting L1 to YAML.
