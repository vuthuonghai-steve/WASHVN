---
name: design-checklist
version: 0.0.1
suite: WASHVN
tags: [architect, checklist, quality, gates]
---

# Design Quality Checklist — skill-architect ver-3

> Run BEFORE handoff. Any `[ ]` → fix before deliver.
> META/ARCH gates replace old G1-G7 framework.

---

## ARCH Binary Gates

- [ ] ARCH-1 PASS: Semantic anchors present in §1 (≥1 anchor from domain-handbook.md)
- [ ] ARCH-2 PASS: Input/output schema valid per design.schema.yaml
- [ ] ARCH-3 PASS: Complete 7-zone table (all 7 rows, specific filenames, no blanks)
- [ ] ARCH-4 PASS: Valid Mermaid stateDiagram-v2 in §4 with fallback routes (F3, F8)
- [ ] All ARCH gates binary PASS before proceeding to META checks

---

## META-1: Structural Check

- [ ] Domain anchor present in §1 (trigger keywords match domain-handbook.md)
- [ ] 6 phases defined (P1-P6) with gates and outputs
- [ ] 7-zone mapping table complete (all 7 zones with files, purpose, constraints, required)
- [ ] YAML frontmatter has all required fields (skill_name, target_variable, zone_mapping, data_contracts, state_machine, must_not_rules, quality_gates)
- [ ] Frontmatter version: 0.0.1 and suite: WASHVN present

---

## META-2: Semantic Depth

### S1 Negation Density
- [ ] Phase 1: ≥5 must_not rules
- [ ] Phase 2: ≥5 must_not rules
- [ ] Phase 3: ≥5 must_not rules
- [ ] Phase 4: ≥5 must_not rules
- [ ] Phase 5: ≥5 must_not rules
- [ ] Phase 6: ≥5 must_not rules
- [ ] No generic rules (all must be phase-specific with violation examples)

### S2 Reverse Questions
- [ ] ≥4 questions on negation implications (S2.1)
- [ ] ≥4 questions on design wrongness (S2.2)
- [ ] ≥4 questions on stakeholder harm (S2.3)
- [ ] ≥4 questions on constraint breaks (S2.4)

### S3 Multi-Stakeholder
- [ ] ≥2 distinct stakeholders defined
- [ ] Each stakeholder has: role, pain point, expectation, success signal

### S4 Constraint Anchoring
- [ ] Token budget (BUILD-3.1 ≤700) documented as constraint
- [ ] Schema version pinned in frontmatter
- [ ] Path resolution fallback documented
- [ ] Template freeze boundary documented

---

## META-3: Mechanical Verification

- [ ] ARCH-1 PASS (binary)
- [ ] ARCH-2 PASS (binary)
- [ ] ARCH-3 PASS (binary)
- [ ] ARCH-4 PASS (binary)
- [ ] BUILD-3.1 soft gate: SKILL.md ≤700 tokens
- [ ] Zero placeholder scan: no TODO, FIXME, <!-- -->, xxx.md, pass(), mock()

---

## 6 Acceptance Criteria (ver-3)

- [ ] AC1: 7-zone table with specific filenames and constraints
- [ ] AC2: ≥1 Mermaid diagram (stateDiagram must be present in §4)
- [ ] AC3: ≥5 must_not rules per phase (≥30 total)
- [ ] AC4: ≥4 reverse questions per aspect (≥16 total)
- [ ] AC5: ≥2 stakeholders with full role/expectation/success signal
- [ ] AC6: Constraint anchoring (token budget, schema version, path fallback)

---

## Graceful Degradation Paths

- [ ] Token >700t → degraded:true marker present and refactor path documented
- [ ] Missing template → inline fallback documented
- [ ] Schema mismatch → annotate in §10 metadata documented
- [ ] Degradation evidence archived before handoff

---

## Handoff Readiness

- [ ] design.md written to `.skill-context/{target_skill}/design.md`
- [ ] data/drc.yaml written with routing to gatekeeper + planner
- [ ] All HTML comments replaced with real content
- [ ] State ledger artifacts archived in `.skill-context/{target_skill}/`
- [ ] Quality-matrix aggregate ≥80% (Phase 6A checkpoint)

---

## Final Verification

- [ ] All files have real content (no stubs)
- [ ] Zero placeholders in all files
- [ ] Token count: SKILL.md ≤700t (soft gate BUILD-3.1)
- [ ] All ARCH+META gates documented with PASS status
- [ ] Downstream handoff notification ready (Gatekeeper S1.5)
