# Workflow Phases — skill-architect

## Nguồn gốc

Phần này được trích từ SKILL.md cũ, lines 224-324.



## Phase 0: Boot Sequence — Nạp tri thức nền

**Mục tiêu**: Xây dựng context đầy đủ trước khi thiết kế — tích hợp knowledge scan trước Phase 1.

### 8-Step Knowledge-Aware Boot

1. **Read** `SKILL.md` — nắm cấu trúc và constraints của skill-architect
2. **Read** `_shared/knowledge/framework.md` — framework chuẩn
3. **Scan** `skills/ver-0.0.2/{target_skill}/knowledge/` — Tier 1 source
4. **Read** knowledge files tìm thấy ở step 3
5. **Check** `.skill-context/{target_skill}/` — upstream artifacts từ các stage trước
6. **IF** `.skill-context/{target_skill}/exploration.md` exists → read (primary upstream)
7. **IF** `.skill-context/{target_skill}/domain-handbook.md` exists → read (domain knowledge)
8. **Proceed to Phase 1** — chỉ sau khi context đã built

### Knowledge Source Priority

| Tier | Nguồn | Điều kiện load | Bắt buộc? |
|------|-------|---------------|-----------|
| Tier 1 | `skill-architect/knowledge/*.md` | ALWAYS | ✅ |
| Tier 1 | `.skill-context/{target}/exploration.md` | IF EXISTS | ✅ |
| Tier 1 | `.skill-context/{target}/domain-handbook.md` | IF EXISTS | ✅ |
| Tier 2 | `_shared/knowledge/*.md` | ALWAYS | ✅ |
| Tier 3 | `skill-architect/references/examples/*.md` | WHEN cần reference | ❌ |

### Knowledge Gap Protocol

```yaml
condition: "No Tier 1 knowledge files found"
action:
  - "Set confidence < 70% — STOP, cannot proceed"
  - "ASK user: provide domain knowledge before continuing"
  - "DO NOT hallucinate §2 (Capability Map) content"
if_user_cannot_provide:
  - "Log knowledge gap to design.md §9 Open Questions"
  - "Flag [CẦN LÀM RÕ] trên mọi assertion"
  - "Proceed with 'LIMITED KNOWLEDGE' warning in design.md frontmatter"
```

---

## Phase 1: Collect — Thu thập yêu cầu

**Mục tiêu**: Hiểu rõ Pain Point, người dùng, và output mong đợi.

**Thực hiện**:

1. Xác định **skill-name** (kebab-case). Nếu user chưa đặt tên → gợi ý tên dựa trên mô tả.
2. Thu thập 3 điều từ user:
   - **Pain Point**: Vấn đề gì đang gặp? Tại sao cần skill này?
   - **User & Context**: Ai sẽ dùng? Trong bối cảnh nào?
   - **Expected Output**: Output cuối cùng của skill là gì? (Mermaid? Markdown? JSON?)
3. Nếu confidence < 70% về bất kỳ điều nào → hỏi thêm trước khi tiếp tục.

> **⏸️ Gate 1**: Tóm tắt lại những gì đã hiểu. Chờ user confirm. Sau khi confirm → ghi §1 + §10 vào design.md → Proceed to Phase 2.

---

## Phase 2: Analyze — Phân tích yêu cầu

**Mục tiêu**: Map yêu cầu vào Framework 3 Pillars & 7 Zones.

**Thực hiện**:

1. **3 Pillars Analysis** (từ `knowledge/architect.md`):
   - **Pillar 1 – Knowledge**: Skill cần tri thức gì? Dưới dạng nào?
   - **Pillar 2 – Process**: Workflow logic là gì? Bộc bước nào? Điều kiện rẽ nhánh nào?
   - **Pillar 3 – Guardrails**: AI thường sai ở đâu? Cần kiểm soát gì?

2. **Confidence Check** — Heavy Thinking Decision Point:
   - **Confidence >85%** + cả 3 Pain Points rõ ràng → Skip to Zone Mapping
   - **Confidence 70-85%** hoặc ambiguous → Activate K=8 chains
   - **Confidence <70%** → Quay lại Phase 1

3. **7 Zones Mapping** — theo format chuẩn:

```markdown
| Zone            | Files cần tạo            | Nội dung                             | Bắt buộc? |
| --------------- | ------------------------ | ------------------------------------ | --------- |
| Core (SKILL.md) | `SKILL.md`               | Persona, phases, guardrails          | ✅        |
| Knowledge       | `knowledge/xxx.md`       | Tri thức domain, tiêu chuẩn kỹ thuật | ✅ / ❌   |
| Scripts         | `scripts/xxx.py`         | Automation tools                     | ✅ / ❌   |
| Templates       | `templates/xxx.template` | Output format mẫu                    | ✅ / ❌   |
| Data            | `data/xxx.yaml`          | Config tĩnh, schema                  | ✅ / ❌   |
| Loop            | `loop/xxx.md`            | Checklist, verify rules, test cases  | ✅ / ❌   |
| Assets          | N/A                      | Không cần                            | ❌        |
```

> **Quy tắc**: Nếu Zone không cần → ghi "Không cần". Cột "Files cần tạo" là input cho Planner.

4. **Risks Identification**: ít nhất 3 rủi ro cụ thể.

5. **§11 Knowledge Requirements**: mọi tri thức design phải trace về knowledge source (xem Knowledge Boot §2 attribution rules).

6. **§12 When NOT to Use**: mọi design phải có ít nhất 3 tình huống skill KHÔNG nên được dùng (out-of-scope, thiếu context, user expectation mismatch).

> **⏸️ Gate 2**: Trình bày bảng phân tích. Chờ confirm → ghi §2 + §3 + §8 + §11 + §12 → Proceed to Phase 3.

---

## Phase 3: Design & Output — Thiết kế và Xuất kết quả

**Mục tiêu**: Cụ thể hóa kiến trúc thành sơ đồ và kế hoạch rõ ràng.

**Thực hiện** (đúng thứ tự):

1. **Read** `knowledge/visualization-guidelines.md` — nắm chuẩn sơ đồ trước khi vẽ.
2. **Tạo bắt buộc** ≥ 3 sơ đồ Mermaid:
   - `D1 — Folder Structure` (mindmap)
   - `D2 — Execution Flow` (sequenceDiagram)
   - `D3 — Workflow Phases` (flowchart LR)
   - _(Optional)_ `D4 — Pipeline` (flowchart TD)
3. **Thiết kế §6 Interaction Points**: khi nào skill PHẢI dừng hỏi user.
4. **Thiết kế §7 Progressive Disclosure Plan**: Tier 1 vs Tier 2.
5. **Điền §9 Open Questions**: tổng hợp điểm chưa rõ.

> **⏸️ Gate 3**: Trình bày toàn bộ design. Chờ confirm → ghi §4 + §5 + §6 + §7 + §9 + §10.

---

## Progressive Writing Contract

**⚠️ CRITICAL**: Ghi vào `design.md` **ngay sau khi mỗi Phase được user confirm**.

| Sau Phase | Ghi vào design.md |
| --------- | ------------------|
| Phase 1 | §1 Problem Statement, §10 Metadata (IN PROGRESS) |
| Phase 2 | §2 Capability Map, §3 Zone Mapping, §8 Risks, §11 Knowledge Requirements, §12 When NOT to Use |
| Phase 3 | §4-§7, §9, §10 (COMPLETED) — bao gồm §11 + §12 refinement nếu cần |

---

## Quality Gate — Trước khi Deliver

1. Chạy `loop/design-checklist.md` — kiểm tra nội dung toàn diện
2. Chạy `validate_design.py` (nếu có) — kiểm tra schema và tính hợp lệ
3. Nếu fail → sửa trước khi thông báo hoàn thành
4. Sau pass → thông báo cho user

```
✅ design.md hoàn thành tại: .skill-context/{target_skill}/design.md
```
