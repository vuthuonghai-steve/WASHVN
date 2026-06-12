# **BUILD GUIDELINES (Usage: Quy chuẩn viết nội dung)**

> **Usage**: Hướng dẫn Kỹ sư cách viết và tổ chức nội dung cho từng Zone. Dùng trong Step BUILD.

---

## 0. CHUẨN CLAUDE.MD — 4 LAYER KNOWLEDGE SEPARATION (BẮT BUỘC)

### Tại sao cần tách?

LLM không xử lý Markdown/YAML như compiler. Nó phản ứng với **cấu trúc** và **ranh giới ngữ nghĩa**. Khi tất cả trộn lẫn:
- Model khó phân biệt đâu là instruction, đâu là reference
- Token budget explosion → context overload
- Chất lượng output giảm

### 4 Layers từ CLAUDE.md §5:

```yaml
knowledge_layers:
  L0_anchor_rules:
    purpose: "Luật nền, mục tiêu, giới hạn tuyệt đối"
    location: "SKILL.md (root)"
    format: "YAML frontmatter + XML boundaries"
    token_budget: "150-400 tokens"

  L1_working_policy:
    purpose: "Quy ước làm việc, constraints, output contract"
    location: "policy/{target_skill}.yaml"
    format: "YAML with must/must_not/constraints"
    token_budget: "400-1200 tokens"

  L2_domain_context:
    purpose: "Domain knowledge, glossary, data flow"
    location: "knowledge/*.md"
    format: "Markdown + tables"
    load_policy: "on-demand"

  L3_evidence_examples:
    purpose: "Spec, logs, examples, fixtures"
    location: "examples/, specs/"
    format: "XML wrapper + Markdown/YAML"
    load_policy: "task-specific"
```

### Format Selection từ CLAUDE.md §3-§4:

```yaml
format_selection_rules:
  markdown:
    use_for: [explanation, rationale, overview, domain_knowledge]
    avoid_for: [hard_rules_without_schema, long_mixed_policy_blocks]

  yaml:
    use_for: [constraints, policies, checklists, routing, output_contracts, acceptance_criteria]
    avoid_for: [long_prose, complex_narrative_context]

  xml_like_tags:
    use_for: [semantic_boundaries, separating_context_from_instruction, wrapping_examples]
    avoid_for: [excessive_micro_tagging]
```

### SKILL.md LAYOUT CHUẨN:

```markdown
---
name: skill-name
description: "WHAT + WHEN trigger"
---

# Skill Name

## Mission
[Markdown - 2-3 sentences]

<instructions>
[YAML block - imperative commands]
</instructions>

## Boot Sequence
[YAML or Markdown table]

## Workflow
[Markdown - phase overview]

## Output Contract
```yaml
[YAML block]
```

## References
| File | Load When |
|------|-----------|
| policy/{name}.yaml | Always |
| knowledge/domain.md | Phase 2+ |
```

**KEY RULES:**
- SKILL.md = L0 ONLY (≤400 tokens)
- Constraints/Policy = YAML in `policy/{target_skill}.yaml`
- Domain knowledge = Markdown in `knowledge/`
- NO prose constraints in SKILL.md body

---

## 1. CHUẨN ANTHROPIC — BẮT BUỘC ĐỌC KHI VIẾT SKILL.MD

Trước khi viết `SKILL.md`, đọc [anthropic-skill-standards.md](anthropic-skill-standards.md).
File này chứa các yêu cầu bắt buộc từ Anthropic về cấu trúc, discovery, và hiệu quả của skill.

**Checklist nhanh (từ anthropic-skill-standards.md §9)**:
- YAML frontmatter dòng đầu (name + description ngôi thứ 3)
- name: lowercase-kebab-case, ≤ 64 chars, gerund form ưu tiên
- description: WHAT + WHEN trigger, ≤ 1024 chars
- Progressive Disclosure: files load đúng phase (không front-load)
- Workflow Tracker Checklist nếu có 3+ phases hoặc Interaction Points
- Examples file nếu có mapping trừu tượng
- **SKILL.md ≤ 400 tokens (L0 budget)** — nếu vượt, tách vào `policy/`

---

## 1. NGUYÊN TẮC VIẾT SKILL.MD (CORE)

- **Ngôn ngữ**: Tuyệt đối dùng thể mệnh lệnh (Imperative).
- **Anthropic Standards**: Tuân thủ 100% `anthropic-skill-standards.md` — YAML frontmatter, Progressive Disclosure, Checklist Tracker, Examples Pattern.
- **Phân tầng (PD)**: Mọi file trong `knowledge/`, `scripts/`, `loop/` phải có ít nhất 1 link tham chiếu từ `SKILL.md` tại đúng phase cần dùng (không phải ở Boot Sequence nếu không cần ngay).
- **Phases**: Chia workflow thành các Phase có thể đánh dấu hoàn thành.

## 2. NGUYÊN TẮC VIẾT KNOWLEDGE
 
 - Mỗi file phải có header **Usage** mô tả mục đích và thời điểm sử dụng.
 - Ưu tiên bảng và sơ đồ Mermaid.
 - Nội dung domain phải dẫn nguồn từ `resources/`.
 - **Fidelity Standard**: Tuyệt đối không tóm tắt tài nguyên `Critical`. Mọi định nghĩa, mã định danh (Rule IDs, Error codes) phải được chuyển hóa chính xác. Nếu resource có danh sách chi tiết, kết quả build phải có danh sách tương ứng.
 - **Kỹ thuật Parity Check**: Trước khi lưu file knowledge, hãy đếm số lượng mục/đoạn (headers) trong resource và đảm bảo file knowledge có số lượng tương đương. Nếu file knowledge ngắn hơn >30% so với tài liệu gốc dày đặc thông tin, hãy thực hiện lượt truyền dẫn thứ hai (Second Pass) để bổ sung chi tiết.

## 3. NGUYÊN TẮC VIẾT LOOP (CHECKLIST & LOG)

- **Checklist**: Phải ghi rõ tiêu chí có thể đo lường (measurable).
- **Build-log**: Phải phản ánh trung thực thực tế:
  * Số lượng Placeholder thực tế.
  * Tick checkbox `[x]` chỉ khi task ĐÃ hoàn thành thực sự.
  * Ghi rõ lý do nếu dừng build (Error Policy).

## 4. QUY TẮC ĐẶT TÊN (Naming)

- **Skill Name**: kebab-case (ví dụ: `skill-builder`).
- **Files trong Knowledge**: kebab-case.
- **Scripts**: snake_case hoặc kebab-case.
- **Checklist/Log**: kebab-case.

## 5. CONTEXT DIRECTORY COVERAGE (BAT BUOC)

Muc tieu: Dam bao Builder khong bo sot tai nguyen trong `.skill-context/{target_skill}/`.

### 5.1 Cau truc sub-skill context can hieu ro

```
.skill-context/{target_skill}/
├── design.md        # Architecture source of truth
├── todo.md          # Execution plan source of truth
├── build-log.md     # Evidence + usage matrix + validation log
├── resources/       # Domain references (business/uml/analysis docs)
├── data/            # Rule configs (yaml/json), scoring matrix
└── loop/            # Prior checks, proofs, phase logs (supportive)
```

### 5.2 Phan loai muc do uu tien tai nguyen

- `Critical`:
  - `design.md`
  - `todo.md`
  - Tat ca file trong `resources/`
  - Tat ca file trong `data/`
- `Supportive`:
  - Tat ca file trong `loop/`
  - Tai lieu proof/snapshot

### 5.3 Resource Usage Matrix (bat buoc trong build-log.md)

Builder phai co bang sau trong `.skill-context/{target_skill}/build-log.md`:

| Resource File | Priority | Used In Task | Output File(s) | Notes |
|---|---|---|---|---|
| `resources/...` | Critical | `Task x.y` | `knowledge/...` | rationale |

Quy tac:
- Moi file `Critical` phai xuat hien it nhat 1 dong.
- Moi dong phai co duong dan resource trong backticks.
- Khong duoc danh dau task done neu chua co dong trace tuong ung.
