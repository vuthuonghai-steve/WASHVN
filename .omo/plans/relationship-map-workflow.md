# Workflow Plan: Vẽ Sơ Đồ Quan Hệ — skills/ver-0.0.2

## Trigger
Khi user nói: "vẽ sơ đồ quan hệ" hoặc "relationship map" hoặc "map components"

## Workflow Steps

### Step 1: Parallel Scan (5 background explore agents)
Launch simultaneously:
1. `explore` — Scan pipeline skills (explorer → miner → architect → gatekeeper → planner → builder → reviewer)
2. `explore` — Scan BA micro-skills (elicitor → analyst → synthesizer) + security-reviewer
3. `explore` — Scan _shared/ core (validators, schemas, rules, knowledge, templates, fixtures)
4. `explore` — Scan scripts inventory (all .py files across suite)
5. `explore` — Scan cross-skill references (pattern `../_shared/`, handoff contracts, pipeline ordering)

### Step 2: Synthesis (unspecified-high)
Merge 5 findings → build adjacency matrix → classify relationship types

### Step 3: Generate Diagrams (visual-engineering)
Generate 3 Mermaid diagrams:
- Component relationship graph
- Pipeline flow
- Data dependency

### Step 4: Verify
Cross-check vs actual code → validate Mermaid syntax → output RELATIONSHIP-REPORT.md

## Output Directory
`docs/relationship-mapping-workflow/`

## Prompt Templates

### Agent A: Pipeline Scanner
```
[CONTEXT]: Phân tích 7 pipeline skills trong /home/steve/Work-space/WASHVN/skills/ver-0.0.2/: skill-explorer, skill-knowledge-miner, skill-architect, production-quality-gatekeeper, skill-planner, skill-builder, production-code-reviewer
[GOAL]: Với mỗi skill, xác định: stage number, input contract, output contract, dependencies, successor hints, boot sequence files, knowledge references, checklist items
[DOWNSTREAM]: Tạo JSON để xây dựng ma trận kề và sơ đồ quan hệ
[REQUEST]: Đọc SKILL.md của mỗi skill. Trích xuất pipeline_spec, handoff_contracts, routing_map. Return JSON array với các field: name, stage, input_contract, output_contract, depends_on, depended_by, boot_files, knowledge_refs, checklist_count
```

### Agent B: BA Scanner
```
[CONTEXT]: Phân tích 3 BA micro-skills + security-reviewer trong /home/steve/Work-space/WASHVN/skills/ver-0.0.2/: ba-elicitor, ba-analyst, ba-synthesizer, skill-security-reviewer
[GOAL]: Với mỗi skill, xác định: workflow phases, output contract template path, knowledge dependencies, trigger conditions
[DOWNSTREAM]: Xác định vị trí của BA layer trong pipeline tổng thể
[REQUEST]: Đọc SKILL.md. Xác định workflow sequence (agent nào → agent nào), output_contract path_template, tag/phân loại. Return JSON.
```

### Agent C: Shared Core Scanner
```
[CONTEXT]: Phân tích _shared/ directory tại /home/steve/Work-space/WASHVN/skills/ver-0.0.2/_shared/
[GOAL]: Liệt kê toàn bộ files, đọc nội dung để xác định schema nào cho skill nào, validator nào được skill nào gọi
[DOWNSTREAM]: Xây dựng sơ đồ shared dependency
[REQUEST]: Đọc tất cả files trong _shared/ (validators/, schemas/, rules/, knowledge/, templates/, fixtures/). Với mỗi file, xác định target skills sử dụng nó. Return JSON grouped by zone.
```

### Agent D: Scripts Scanner
```
[CONTEXT]: Phân tích tất cả .py files trong /home/steve/Work-space/WASHVN/skills/ver-0.0.2/
[GOAL]: Xác định ownership (skill nào sở hữu script nào), imports, dependencies
[DOWNSTREAM]: Vẽ sơ đồ script dependency
[REQUEST]: Đọc imports và docstring của mỗi .py file. Xác định: owner_skill, imports, exports, gọi trong boot_sequence của skill nào. Return JSON.
```

### Agent E: Cross-ref Scanner
```
[CONTEXT]: Tìm references chéo giữa các skills trong /home/steve/Work-space/WASHVN/skills/ver-0.0.2/
[GOAL]: Xác định tất cả cross-references, handoff contracts, pipeline ordering
[DOWNSTREAM]: Hoàn thiện adjacency matrix và sơ đồ pipeline flow
[REQUEST]: Grep tất cả SKILL.md + knowledge/*.md + policy/*.md cho pattern: "../_shared/", "Dependencies:", "Successor Hints:", "Input Contract:", "Output Contract:", "pipeline", "stage". Return JSON edges array với source, target, type, contract, file_path.
```

## Momus Gate
Trước khi execute, invoke Momus để review plan này.
