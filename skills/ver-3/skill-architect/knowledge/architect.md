---
name: architect-knowledge
version: 0.0.1
suite: WASHVN
tags: [architect, framework, gates, iqd, depth-signals]
---

# ARCHITECT FRAMEWORK — Knowledge Base

> Usage: Read at boot time, Tier 2. Provides 3 Pillars framework, META/ARCH gate definitions, IQD thresholds, and Depth Signals for architect workflow.

---

## Glossary (≥10 terms)

| Term | Definition |
|------|-----------|
| Semantic Anchor | A domain keyword or phrase that grounds design decisions to upstream source |
| ARCH Gate | Binary PASS/FAIL gateway for deterministic design verification (ARCH-1→4) |
| META Gate | Multi-component quality gate (META-1 structural, META-2 semantic depth, META-3 mechanical) |
| S1 Negation Density | Count of must_not rules per phase (minimum 5 per phase) |
| S2 Reverse Questions | Defensive reasoning questions per aspect (minimum 4 per aspect) |
| S3 Multi-Stakeholder | Distinct downstream roles whose expectations the design must satisfy (≥2) |
| S4 Constraint Anchoring | Real-world constraints (token budget, schema version, path resolution) embedded in design |
| IQD Threshold | Information Quality Density — measurable boundary for anchoring quality |
| DRC | Dynamic Routing Contract — YAML contract defining I/O paths between pipeline stages |
| Dual Knowledge Stream | Separation of technical (design.md, drc.yaml) and cognitive (knowledge/*.md) outputs |
| BUILD-3.1 | Soft gate: SKILL.md ≤700 tokens. Warning + auto-refactor if exceeded |
| 7-Zone Mapping | Core, Knowledge, Templates, Scripts, Data, Loop, Assets — each with files, purpose, constraints |
| F3/F8 Fallback | Graceful degradation routes: F3=gatekeeper fail→revise, F8=drift→re-elicit |
| WORM | Write Once, Read Many — lifecycle status for immutable design artifacts |
| Negation Space | Complete set of must_not rules per phase, defining what the system MUST NOT do |

## META Gate Definitions

META-1 (Structural): Domain anchor present + 6 phases defined + 7-zone table complete + all required frontmatter fields. Weight: 0.30. Pass threshold: 0.80.

META-2 (Semantic Depth): S1 ≥5/phase ∧ S2 ≥4/aspect ∧ S3 ≥2 stakeholders ∧ S4 constraints. AND gate: all 4 must pass. Weight: 0.35.

META-3 (Mechanical): ARCH-1/2/3/4 all PASS + BUILD-3.1 ≤700t + zero placeholder. Weight: 0.35. Pass threshold: 1.00 (all).

## ARCH Criteria

ARCH-1: Semantic anchors present in §1 problem statement. Verification: regex match for anchor keywords against domain-handbook.md glossary.

ARCH-2: Input schema AND output schema valid per design.schema.yaml. Verification: script validates required fields present.

ARCH-3: Complete 7-zone table with specific filenames, purpose, constraints. Verification: count zones = 7, no blank rows.

ARCH-4: Valid Mermaid stateDiagram-v2 in §4 with states, transitions, fallback routes. Verification: Mermaid syntax check.

## 4 Depth Signals

S1 (Negation Density): ≥5 must_not rules per phase, each phase-specific, no contradictions. Count enforced by binary gate.

S2 (Reverse Questions): ≥4 defensive questions per aspect (S2.1 negation implications, S2.2 design wrongness, S2.3 stakeholder harm, S2.4 constraint breaks).

S3 (Multi-Stakeholder): ≥2 distinct stakeholders with pain point, expectation, success signal defined.

S4 (Constraint Anchoring): Real-world constraints (token budget, schema pinning, path resolution, format freeze) documented in design.must_not_rules.

## 6-Phase Workflow Mapping

| Design Phase | Knowledge Zone Reference | Key Constraints |
|-------------|------------------------|-----------------|
| P1 Read | Glossary, Semantic Anchors | Trace to source, no hallucination |
| P2 Zone Mapping | 7-Zone rules, Zone Decision Tree | Specific filenames, all 7 zones |
| P3 Data Contracts | META-2, Schema refs | I/O schemas valid, DRC routing |
| P4 State Diagram | stateDiagram syntax | Fallback routes, deterministic transitions |
| P5 Must-Not Rules | S1 Negation Space | ≥5/phase, phase-specific |
| P6 Emit | META gates, BUILD-3.1 | No placeholders, token ≤700t |

## Graceful Degradation Integration

- If upstream missing: reject with F6 request at Phase 1, do not proceed
- If template missing: use fallback inline content, mark degraded
- If token exceeds: mark degraded, auto-refactor, preserve semantics
- If schema mismatch: annotate in §10 metadata, proceed with warning

## Source Attribution Rules (Anti-Hallucination)

Valid trace tags: `[TỪ DESIGN §N]`, `[TỪ NGUỒN EXTERNAL]`, `[GỢI Ý BỔ SUNG]`, `[CẦN LÀM RÕ]`. Every assertion in design.md must trace to source.

## 3 Pillars Framework

- Pillar 1 (Knowledge): Domain knowledge needed — from domain-handbook.md glossary
- Pillar 2 (Process): Workflow logic, branching conditions — from exploration.md problem statement
- Pillar 3 (Guardrails): Where AI typically fails — from criteria.md acceptance criteria + architect experience

## IQD Thresholds Reference

- Glossary ≥10 terms in knowledge/architect.md
- Semantic anchor density ≥1 per 200 tokens in design.md
- Thought block depth ≥200 words (if cognitive stream active)
- Dual anchor types required: technical + stakeholder
- Semantic density (keyword): 30-60%, target 40%
- Meaningful content ratio: ≥60%, target 75%
- Prose-to-contract ratio: 1:1 to 1:4, target 1:2
