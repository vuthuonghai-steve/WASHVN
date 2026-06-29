# Miner Analyzer

> Role: **Miner** | Domain: **Knowledge** | Design: **Integration**
> Source: `architecture-design.md §S0.7` (clean/)

## Purpose

Miner extracts domain knowledge and builds `domain-handbook.md` — used by Architect for design.

## Standard flow (CREATE mode)

1. Read `business-analysis.md` from Context Bus
2. Scan project documentation for domain specifics
3. Build `domain-handbook.md` with 4 components:
   - **Keyword Trigger Library** — domain anchors + context triggers
   - **Success Criteria & Quality Gates** — binary pass/fail
   - **Error Boundaries & Anti-Patterns** — what NOT to do
   - **Structural Exemplars** — API contracts + sample code

## UPDATE/REBUILD flow

1. Read `deconstructed_context` from Context Bus (populated by Deconstructor)
2. Integrate extracted knowledge into `domain-handbook.md`
3. Preserve original advantages_and_intent
4. Flag any deprecated patterns found in old skill

## Fallback

- F2: Domain-handbook insufficient (glossary < 10 or missing anti-patterns)
- F6: Glossary terms < 10 after hydration
