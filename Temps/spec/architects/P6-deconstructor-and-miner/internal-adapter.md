# Internal Skill Adapter

> Role: **Deconstructor** | Domain: **Migration** | Design: **Contract**
> Source: `skill-migration-spec.md §14.2` (clean/)

## Purpose

Reads an existing WASHVN skill's structure and extracts into Context Bus for UPDATE/REBUILD.

## Input

Path to existing skill directory with canonical 7-Zone structure:
```
{skill-name}/
├── SKILL.md
├── knowledge/
├── scripts/
├── templates/
├── data/
├── loop/
└── assets/
```

## Extraction targets

| Source | Extracted to | Detail |
|:---|:---|:---|
| `SKILL.md` frontmatter | `deconstructed_context.original_persona` | name, description, role |
| `SKILL.md` instructions | `deconstructed_context.advantages_and_intent` | must/must_not rules |
| `knowledge/` files | `deconstructed_context.extracted_knowledge` | file_name + content |
| `loop/` checklists | `deconstructed_context.extracted_guardrails` | must/must_not arrays |
| `data/` contracts | `deconstructed_context.extracted_contracts` | contract_id + schemas |

## Output

Writes into Context Bus `deconstructed_context` block — available for Miner (Stage 0.7) to integrate into `domain-handbook.md`.
