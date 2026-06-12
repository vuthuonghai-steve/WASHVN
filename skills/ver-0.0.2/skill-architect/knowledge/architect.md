# ARCHITECT FRAMEWORK — Architect's Knowledge Base

> **Usage**: Read at boot time
> **Shared Source**: `../../_shared/knowledge/framework.md`

---

<context>
## Quick Reference

For complete framework details (7 Zones, Pipeline Flow, Naming Conventions, Anti-hallucination), see:
```
../../_shared/knowledge/framework.md
```
</context>

---

## Source Attribution Rules (Anti-Hallucination)

Every section in design.md MUST trace content to source.

### Valid Trace Tags

| Tag | Meaning | Usage |
|-----|---------|-------|
| `[TỪ DESIGN §N]` | Derived directly from design.md section N | §2 → §3 mapping |
| `[TỪ NGUỒN EXTERNAL]` | From user's resources/ folder | Domain knowledge |
| `[GỢI Ý BỔ SUNG]` | Suggested by Architect, not in design | Rationale |
| `[CẦN LÀM RÕ]` | Needs user clarification | Blockers |

### Required Attribution by Section

```yaml
section_attribution:
  §2_capability_map:
    knowledge_pillar: "[TỪ NGUỒN EXTERNAL]"  # hoặc user input
    process_pillar: "[TỪ DESIGN §1]"          # từ pain point
    guardrails_pillar: "[GỢI Ý BỔ SUNG]"      # architect expertise

  §3_zone_mapping:
    all_zones: "[TỪ DESIGN §2]"                # từ capability map
    files_traced: "[TỪ NGUỒN EXTERNAL]"       # nếu từ resource

  §4_folder_structure:
    structure: "[TỪ DESIGN §3]"                # phản ánh zone mapping
    diagrams: "[TỪ DESIGN §3]"                  # match §3 exactly
```

### Anti-Hallucination Checklist

- [ ] Mỗi sentence trong §2 có trace tag
- [ ] Mỗi file trong §3 có trace tag
- [ ] Risk mitigation có `[GỢI Ý BỔ SUNG]` hoặc `[TỪ NGUỒN EXTERNAL]`
- [ ] Open Questions được flag với `[CẦN LÀM RÕ]`

---

## Architect-Specific Workflow Phases

### Phase 1: Collect

1. Determine **skill-name** (kebab-case)
2. Collect from user:
   - **Pain Point**: What problem needs solving?
   - **User & Context**: Who will use? In what context?
   - **Expected Output**: What is final output? (Mermaid? Markdown? JSON?)
3. Confidence < 70% → Ask clarifying questions

**Gate 1**: Summarize → Wait for confirm → Write §1 + §10 to design.md

---

### Phase 2: Analyze

1. **3 Pillars Analysis**:
   - Pillar 1 – Knowledge: What domain knowledge is needed?
   - Pillar 2 – Process: What is workflow logic? Branching conditions?
   - Pillar 3 – Guardrails: Where does AI typically fail?

2. **7 Zones Mapping**: Fill Zone Mapping table

3. **Risks Identification**: List ≥3 specific risks

**Gate 2**: Present analysis → Wait for confirm → Write §2 + §3 + §8 to design.md

---

### Phase 3: Design & Output

1. Read `knowledge/visualization-guidelines.md` for diagram standards
2. Create ≥3 Mermaid diagrams:
   - D1 — Folder Structure (mindmap)
   - D2 — Execution Flow (sequenceDiagram)
   - D3 — Workflow Phases (flowchart LR)
3. Design §6 Interaction Points
4. Design §7 Progressive Disclosure Plan (Tier 1 vs Tier 2)
5. Fill §9 Open Questions

**Gate 3**: Present full design → Wait for confirm → Write §4 + §5 + §6 + §7 + §9 + §10 to design.md

> **Framework Source**: See `../../_shared/knowledge/framework.md` for complete reference
