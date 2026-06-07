# MASTER FORMAT STANDARDS — Shared Knowledge Base

## Nguồn gốc

Tài liệu này chuẩn hóa định dạng dữ liệu, quy định sử dụng cú pháp YAML/Markdown/XML và hệ thống Trace Tags từ `/CLAUDE.md` §3, §4, §10 cho toàn bộ Master Skill Suite.

---

## 1. Chọn Format

| Khi cần | Dùng format | Lý do |
|---------|-------------|-------|
| Giải thích, rationale, overview | Markdown | Đọc tự nhiên |
| Luật, constraints, policy, checklist | YAML | Ép cấu trúc, giảm ambiguity |
| Tạo ranh giới ngữ nghĩa | XML-like tags | Phân biệt instruction vs reference |

---

## 2. YAML Keys cho Policy

```yaml
must:           # Hành vi bắt buộc
must_not:       # Hành vi cấm
should:         # Best practice
priority_order: # Thứ tự ưu tiên khi xung đột
constraints:    # Ràng buộc
scope:          # Phạm vi áp dụng
output_contract:# Định dạng đầu ra bắt buộc
acceptance_criteria: # Tiêu chí chấp nhận
stop_conditions:# Điều kiện dừng
validation:     # Kiểm tra
```

---

## 3. XML-like Tags

```xml
<instructions>Luật điều khiển hành vi (imperative mode)</instructions>
<context>Dữ liệu tham chiếu, không phải lệnh</context>
<examples>Ví dụ minh họa pattern đúng</examples>
<input>Thông tin người dùng hoặc tài liệu nguồn</input>
<output_contract>Định dạng đầu ra bắt buộc — AI MUST comply</output_contract>
```

---

## 4. Token Budget

```yaml
L0_limit: 600    # Root guide / SKILL.md boot
L1_limit: 1500   # Policy files
L2_limit: 2500   # Domain context
tokenizer: cl100k_base
enforcement: hard  # REJECT if exceeded, return to agent for fix
```

---

## 5. Trace Tags (Anti-hallucination)

Mọi content/task phải có source attribution và tuân thủ chuẩn Trace Tags thống nhất:

```markdown
[TỪ INPUT]             # Nguồn thông tin thô từ yêu cầu của User (cho BA, Explorer)
[SUY LUẬN]             # Suy luận logic nghiệp vụ của AI (cho BA, Architect)
[TỪ DESIGN §N]         # Tham chiếu trực tiếp tới mục N trong bản thiết kế design.md (regex: ^\[TỪ DESIGN §[0-9]+(\.[0-9]+)?\]$)
[GỢI Ý BỔ SUNG]        # Đề xuất bổ sung của Planner/Builder, không có trong design
[TỪ AUDIT TÀI NGUYÊN]  # Sinh ra do thiếu tài nguyên trong quá trình Resource Audit
[CẦN LÀM RÕ]           # Điểm mơ hồ, chưa rõ — BLOCKER, phải giải quyết trước khi chuyển pha
```

## 5.1 Semantic Activation Anchors

Từ CLAUDE.md §9: những từ khóa này TRIGGER mode xử lý đặc biệt trong LLM.

```yaml
activation_anchors:
  imperative:
    - must
    - must_not
    - priority_order
    - constraints
    - stop_conditions
  contextual:
    - context
    - reference
    - examples
    - evidence
  quality:
    - output_contract
    - acceptance_criteria
    - validation_checklist
    - definition_of_done
```

Dùng các anchor này trong output để đảm bảo LLM hiểu đúng intent:
- `must:` → Hành vi bắt buộc (YAML block)
- `must_not:` → Hành vi cấm (YAML block)
- `stop_conditions:` → Khi nào PHẢI dừng (YAML list)
- `<output_contract>` → Output format bắt buộc (XML tag)

## 5.2 Format Selection Rules

Từ CLAUDE.md §4: khi nào dùng format gì.

```yaml
format_selection:
  markdown:
    use_for: [explanation, rationale, overview, onboarding, domain_knowledge]
    avoid_for: [hard_rules_without_schema, long_mixed_policy_blocks]
  yaml:
    use_for: [constraints, policies, checklists, routing, output_contracts, acceptance_criteria]
    avoid_for: [long_prose, complex_narrative_context]
  xml_tags:
    use_for: [semantic_boundaries, separating_context_from_instruction, wrapping_examples]
    avoid_for: [excessive_micro_tagging, replacing_all_markdown]
```

---

## 6. Output Contract cho todo.md

todo.md phải có 6 sections bắt buộc:

| Section | Format | Must have |
|---------|--------|-----------|
| §1 Pre-requisites | Markdown table | #, Tài liệu/Kiến thức, Tier, Mục đích, Trace, Status |
| §2 Phase Breakdown | Markdown table | #, Task, Priority, Est. Hours, Dependencies, Trace |
| §3 Knowledge & Resources | Markdown list | All documents and tools |
| §4 Definition of Done | Checklist | Completion criteria |
| §5 Notes | Markdown | [CẦN LÀM RÕ] flags |
| §6 Builder Feedback | Checklist | [TỪ DESIGN §N] tags |

### YAML Frontmatter cho todo.md

```yaml
---
skill_schema_version: "3.0.0"
artifact_type: "todo"
skill_name: "{skill-name}"
generated_by: "skill-planner"
generated_at: "{iso8601}"
stage: "planner"
status: "in_progress|ready_for_builder|blocked"
trace_to_design: "design.md"
---
```

---

## 7. Progressive Disclosure cho Planner

```yaml
progressive_disclosure:
  tier1:
    - path: "SKILL.md"
    - path: "../_shared/knowledge/framework.md"
    - path: "knowledge/case-system.md"
    - path: "scripts/check_status.py"
  tier2:
    - path: "knowledge/architect.md"       # load_when: Step READ
    - path: "knowledge/skill-packaging.md" # load_when: Step ANALYZE
  tier3:
    - path: "loop/plan-checklist.yaml"    # load_when: Quality Gate
    - path: "loop/resume-checklist.yaml"   # triggers: resuming
```

---

## 8. Enforce: Hard

**Format compliance là bắt buộc tuyệt đối.** Không có ngoại lệ.

```yaml
enforcement: hard
reject_if:
  - missing_trace_tags
  - missing_xml_boundaries_in_output
  - missing_yaml_blocks_in_constraints
  - token_budget_exceeded
```
