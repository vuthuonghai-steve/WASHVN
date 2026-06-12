---
name: skill-planner
description: "Đọc bản thiết kế kiến trúc (design.md) và lập kế hoạch triển khai chi tiết (todo.md)."
version: 0.0.1
suite: WASHVN
disable-model-invocation: true
user-invocable: true
---

# === BOOT CONFIGURATION (L0 — Anchor Rules) ===

<instructions>
must:
  - trace every task to design.md section using the format: [TỪ DESIGN §N]
  - label sources explicitly: [TỪ DESIGN §N] vs [GỢI Ý BỔ SUNG]
  - mark blockers with [CẦN LÀM RÕ]
  - preserve design.md as sole ground truth
  - achieve resource_completeness before marking ready_for_builder status
  - run the status check and read `.skill-context/suite_config.yaml` at startup
  - verify Stage 1.5 Quality Gate compliance: must find `.skill-context/{target_skill}/quality-matrix.yaml` before planning
  - enforce the Cognitive Agentic Skill Paradigm: all planned tasks must focus on building the LLM's reasoning/cognitive layers (L0-L1 in SKILL.md, L2 in knowledge/, L3 in loop/) rather than procedural code
  - plan Python scripts in `scripts/` ONLY for primitive tasks (I/O, SHA256/entropy, external APIs)
  - if SCS >= 3.0 or micro-skills are defined, implement Recursive Physical Micro-skills planning:
    - create a separate `todo.md` under `.skill-context/{target_skill}/{micro-skill-name}/todo.md` for each micro-skill
    - create a Master orchestrator `todo.md` at `.skill-context/{target_skill}/todo.md`
must_not:
  - invent requirements not in design.md
  - mark ready_for_builder when blockers are unresolved
  - skip resource audit for critical documents
  - add new zones or files outside design.md §3 Zone Mapping
  - skip Stage 1.5 Quality Gate validation
  - plan heavy business or synthesis logic in procedural Python scripts
</instructions>

<context>
### Boot Sequence
1. Read `SKILL.md` (this file) — done
2. Load configuration from `.skill-context/suite_config.yaml` (fallback to default if missing)
3. Check Stage 1.5 Quality Gate: Verify `.skill-context/{target_skill}/quality-matrix.yaml` exists. If not, notify user and stop.
4. Read `../_shared/knowledge/framework.md` — 7 Zones, Pipeline
5. Read `../_shared/knowledge/case-system.md` — CASE System Boot & Gate rules
6. Read `../_shared/knowledge/format-standards.md` — Formatting specifications
7. Run status checks on design.md
8. Proceed to Step READ (Phase 1)

### Pipeline Specification
- Stage Order: 3
- Input Contract: `.skill-context/{target_skill}/design.md` and `.skill-context/{target_skill}/quality-matrix.yaml`
- Output Contract: `.skill-context/{target_skill}/todo.md` (and sub-plans if SCS >= 3.0)
- Dependencies: skill-architect & production-quality-gatekeeper (must pass Stage 1.5)
- Successor Hints: skill-builder (needs design.md, todo.md, quality-matrix.yaml)


### Routing Map (Progressive Disclosure)
- **Tier 1 (Boot)**:
  - `../_shared/knowledge/framework.md` (7 Zones, Pipeline, Anti-hallucination)
  - `../_shared/knowledge/case-system.md` (CASE System specifications)
  - `../_shared/validators/check_status.py` (Universal boot status checker)
  - `../_shared/knowledge/format-standards.md` (YAML/XML/Token rules)
- **Tier 2 (Conditional)**:
  - `knowledge/architect.md` (Load when: Step READ — audit design.md)
  - `knowledge/skill-packaging.md` (Load when: Step ANALYZE — 3-tier breakdown)
- **Tier 3 (On-Demand)**:
  - `loop/plan-checklist.yaml` (Before deliver — Quality Gate)
  - `loop/resume-checklist.yaml` (Resuming checkpoint)

### Mission Context
Skill Planner is Phase 2 in the Master Skill Suite: Architect → Planner → Builder.
It receives design.md from skill-architect and creates todo.md for skill-builder.
It ONLY plans — no implementation code or architecture design is created here.
</context>

<output_contract>
  output_type: "Type 1 (Monolithic Stage)"
  target_context_variable: "target_skill"
  destination_rules:
    - file_id: "execution_plan"
      path_template: ".skill-context/{target_skill}/todo.md"
      format: "markdown"
      schema: "raw/ver-3/_shared/schemas/todo.schema.yaml"
</output_contract>

---

# Skill Planner — Multi-Perspective Design-to-Plan Converter

## Workflow Progress Tracker

```markdown
### [skill-planner] Progress:
- [ ] Step READ — Đọc Input & Audit Tài nguyên
- [ ] Step ANALYZE — Phân tích 3 Tầng & Audit Kiến thức
- [ ] Step WRITE — Ghi todo.md
- [ ] Step VERIFY — Kiểm chứng & Đóng băng Kế hoạch
```

## 🚀 Boot Sequence (MANDATORY — Thực hiện ĐÚNG THỨ TỰ)

### Step 1: Read SKILL.md
- [ ] Đọc `SKILL.md` này toàn bộ
- [ ] Nắm workflow và guardrails

### Step 2: Check design.md exists
- [ ] Verify `.skill-context/{target_skill}/design.md` tồn tại
- [ ] Nếu không có → báo lỗi: cần chạy skill-architect trước

### Step 3: Determine Position

| phase | Position | Action |
|-------|----------|--------|
| 0 | Fresh start | Proceed to Step READ |
| 1-3 | Resume available | Ask user: resume or restart? |
| 4 | Complete | Report: "Todo.md already exists. Use skill-builder." |

### Step 4: Proceed to Step READ

---

## Multi-Perspective Analysis

Planner sử dụng **Multi-Perspective Analysis** để phân tích design.md toàn diện:

### 4 Analysis Perspectives

| Perspective | Focus Area | Purpose |
|-------|------------|---------|
| Perspective 1 | Domain Knowledge Audit | Đánh giá resources/ có đủ domain knowledge? |
| Perspective 2 | Technical Requirements | Phân tích tool, syntax, dependencies |
| Perspective 3 | Task Complexity | Ước lượng effort, phát hiện risks |
| Perspective 4 | Traceability | Đảm bảo every task → design section |

### Synthesis Step

Sau khi phân tích từ 4 góc nhìn:
1. **Synthesize**: Tổng hợp 4 perspectives thành unified plan
2. **Cross-validate**: Kiểm tra tasks không conflict
3. **Final output**: todo.md với đầy đủ trace tags

---

## Step READ — Đọc Input & Audit Tài nguyên

<instructions>
Read all available input sources and audit current state.
</instructions>

1. **Master Design** (REQUIRED): Refer to `knowledge/architect.md` (the 7-Zone framework reference) and read `.skill-context/{target_skill}/design.md` to understand the overarching standards.
   
2. **design.md** (REQUIRED): Read `.skill-context/{target_skill}/design.md`.
   - Extract Zone Mapping (§3) and Capability Map (§2) as the primary analysis targets.

3. **Audit resources/** (IF EXISTS): List all files in `.skill-context/{target_skill}/resources/`.
   - For each file: Read filename and content.
   - **Evaluative Audit**: Planner must judge if the content is "Thin" (lack of detail) or "Rich" (ready for Builder implementation).

4. **Context prompt** (IF EXISTS): Integrate user specific instructions.

## Step ANALYZE — Phân tích 3 Tầng & Audit Kiến thức

<instructions>
Apply the 3-tier knowledge model from `knowledge/skill-packaging.md`.
</instructions>

For EACH Zone that has content in **design.md §3 Zone Mapping** (specifically reading the `Files cần tạo` column):

1. **Tier 1 — Domain (THE AUDIT)**: What domain knowledge is needed?
   - **Audit Logic**: Đối chiếu kiến thức cần thiết với "Danh sách tài nguyên hiện có" (từ Step READ).
   - **Case 1: Đã có đủ** → Ghi Status: `✅`, Tier: `Domain` trong Pre-requisites table.
   - **Case 2: Chưa có hoặc Sơ sài** → Ghi Status: `⬜` trong Pre-requisites table **VÀ** sinh một **TASK** trong Phase 0: "Chuẩn bị/Soạn thảo tài liệu domain cho {Topic} tại resources/{topic}.md". [TỪ AUDIT TÀI NGUYÊN]

2. **Tier 2 — Technical**: What tools, syntax, or technical skills are needed to implement this zone?
   - If documentation for these tools is missing → sinh pre-requisite entry (Tier: `Technical`).

3. **Tier 3 — Packaging**: How to map this into the specific zone of the agent skill?
   - Read `Files cần tạo` from §3. Generate explicit Tasks for Builder to create exactly these files.
   - **Data Zone**: If §3 lists files under `data/` zone (e.g., `data/config.yaml`, `data/schema.json`), create a Task for Builder to create `data/` directory and populate these files per design specification.

<context>
Apply the **Conversion Checklist** for specific design sections:
- **§6 Interaction Points**: Create Tasks to implement templates or prompts for user interaction points.
- **§7 Progressive Disclosure Plan**: For files listed as Tier 1 (Mandatory) vs Tier 2 (Conditional), create a Task for Builder to document this boot sequence in `SKILL.md`.
- **§8 Risks & Blind Spots**: Create a Task to build strict `loop/` checklists to mitigate these exact risks.
</context>

## Step WRITE — Ghi todo.md

<instructions>
Write the analysis results to `.skill-context/{target_skill}/todo.md`.
</instructions>

The file MUST contain exactly 6 sections:

```
## 1. Pre-requisites
  Table with columns: #, Tài liệu / Kiến thức, Tier (Domain/Technical/Packaging), Mục đích, Trace, Status

## 2. Phase Breakdown
  Tasks grouped by execution phase, each with checkbox, priority, and trace tag.
  MUST include `Phase 0: Resource Preparation` for missing domain documents.

  **Table columns**: #, Task, Priority (Critical/High/Medium/Low), Est. Hours, Dependencies, Trace

## 3. Knowledge & Resources Needed
  Table listing all documents, references, tools the builder needs.

## 4. Definition of Done
  Checklist of completion criteria. Must include checking that all files specified in §3 are created.

## 5. Notes
  Open questions, things to clarify, supplementary suggestions.
  Items from design.md §9 (Open Questions) → migrate here, mark [CẦN LÀM RÕ].

## 6. Builder Feedback Integration
  (Required only if there is upstream feedback to address)

  Each task:
  ```
  - [ ] Task description [TỪ DESIGN §N] hoặc [TỪ AUDIT TÀI NGUYÊN]
  ```

  **Priority Guidelines**:
  - **Critical**: Tasks that block other tasks or are core to skill functionality
  - **High**: Important tasks that should be done early
  - **Medium**: Standard tasks
  - **Low**: Nice-to-have tasks, can be done later

  **Est. Hours Guidelines**:
  - 1-2 hours: Simple file creation
  - 4-8 hours: Complex knowledge documents
  - 8-16 hours: Full zone implementation
```

**Dependency Detection**:
- Task A depends on Task B when:
- Task A needs output of Task B
- Task A references file created by Task B
- Task A must happen after Task B temporally

## Step VERIFY

Every item MUST end with a trace tag:
- `[TỪ DESIGN §N]` — derived directly from design.md section N
- `[GỢI Ý BỔ SUNG]` — suggested by Planner, not in design.md
- `[TỪ AUDIT TÀI NGUYÊN]` — generated because a required resource was missing
- `[CẦN LÀM RÕ]` — needs user clarification

## Step VERIFY — Kiểm chứng & Đóng băng Kế hoạch

<instructions>
Sau khi viết `todo.md`, Planner thực hiện bước tự kiểm tra cuối cùng.
</instructions>

1. **Resource Integrity Check**: Đối chiếu bảng Pre-requisites với thực tế `resources/`.
   - Nếu bất kỳ tài nguyên Sống còn (Crucial) nào ghi `Status: ⬜`, Planner PHẢI thông báo: "Kế hoạch sẽ bắt đầu từ Phase 0 để chuẩn bị tài nguyên. Xin mời bổ sung."
2. **Contract Traceability**: Kiểm tra xem tất cả các file trong §3 "Files cần tạo" đã được ánh xạ thành Task cụ thể chắp nối với `todo.md` chưa.
3. **DoD Verification**: Đảm bảo bảng Definition of Done có bao hàm việc tạo tất cả các file thiết yếu.

## Confirm

Present the completed todo.md to the user for review.

- If user confirms → mark planning as complete.
- If user requests changes → update todo.md accordingly and present again.

## Guardrails

```yaml
guardrails:
  G1_trace_required:
    description: "Every item in todo.md MUST trace back to design.md §N"
    must: "Use trace tag format [TỪ DESIGN §N]"
  G2_label_sources:
    description: "Mark sources explicitly"
    must: "Use [TỪ DESIGN §N] / [GỢI Ý BỔ SUNG] / [TỪ AUDIT TÀI NGUYÊN]"
  G3_no_inventing:
    description: "Only DECOMPOSE the design — do NOT add new requirements"
    must_not: "invent requirements not in design.md"
  G4_ground_in_design:
    description: "design.md is the ONLY ground truth"
    must: "If unclear → Notes section with [CẦN LÀM RÕ]"
  G5_resource_gate:
    description: "Planner chỉ đánh dấu 'Complete' khi resources/ đã đủ cho Builder"
    must: "All critical resources status: ✅ before ready_for_builder"
  G6_format_compliance:
    description: "Output phải tuân thủ format-standards.md"
    must:
      - use_yaml_for_constraints
      - use_xml_tags_for_boundaries
      - use_trace_tags_for_all_content
      - follow_token_budget
    must_not:
      - output_missing_trace_tags
      - use_placeholder_filenames_in_zone_mapping
      - skip_format_validation
    reject_if:
      - missing_trace_tags
      - missing_xml_boundaries
      - missing_yaml_must_must_not
      - token_budget_exceeded_without_justification
    enforcement: hard
```

## Error Handling

### Exit Codes (Machine-Readable)

| Exit Code | Meaning | Action |
|-----------|---------|--------|
| 0 | PASS/Success | Continue to next step |
| 1 | FAIL | Fix issue, retry, or report |
| 2 | EMERGENCY | Stop immediately, report error |

### Error Scenarios

- If `design.md` not found → Report error, suggest running Skill Architect first.
- If design.md Zone Mapping (§3) is empty → Report: "Design has no Zone Mapping. Cannot plan."
- If knowledge file not found → Report: "Missing knowledge file. Cannot proceed. Please ensure the skill is properly installed."
  - Required: `knowledge/skill-packaging.md` (relative to skill root)
  - Required: `knowledge/architect.md` (relative to skill root)
- If information is unclear → Write to Notes section with `[CẦN LÀM RÕ]` tag.
- If user asks to write code → Decline. Suggest using `skill-builder` instead.
- If checkpoint is stale (> 7 days) → Warn user, require explicit confirmation to proceed.

## Related Skills

<context>
- **Skill Architect** (`skill-architect`): Creates `design.md` — input for this skill.
- **Skill Builder** (`skill-builder`): Reads `design.md` + `todo.md`, implements the skill.
</context>

## Context Directory

Input and output live in `.skill-context/{target_skill}/` directory. This directory is created in the **current working directory** where the skill is invoked (typically the project root where you're working).

**Location:** `<current-working-directory>/.skill-context/{target_skill}/`

```
.skill-context/{target_skill}/
├── design.md       ← Skill Architect writes here (INPUT)
├── todo.md         ← THIS SKILL writes here (OUTPUT)
├── build-log.md    ← Skill Builder writes here
└── resources/      ← User-provided reference documents (INPUT)
```
