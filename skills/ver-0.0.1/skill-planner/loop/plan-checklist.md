# Plan Quality & Resource Checklist

> Dùng trong Step VERIFY của Skill Planner
> Đối chiếu với todo.schema.yaml: phases, dependencies, blockers, prerequisites, handoff ready_condition.

## 1. YAML Frontmatter — todo.schema.yaml Required Fields

- [ ] `skill_schema_version: "3.0.0"` present
- [ ] `artifact_type: "todo"` present
- [ ] `skill_name` matches design.md
- [ ] `generated_by: "skill-planner"` present
- [ ] `generated_at` has ISO 8601 timestamp
- [ ] `stage: "planner"` present
- [ ] `status` is one of: in_progress, ready_for_builder, blocked
- [ ] `trace_to_design` points to `design.md`

## 2. Phases & Tasks Check

- [ ] `phases` array has at least one phase with `id`, `name`, `tasks`
- [ ] Phase IDs match pattern `^PH[0-9]+$` (e.g. PH0, PH1)
- [ ] Every task has `id` (pattern `^T[0-9]+\.[0-9]+$`), `title`, `zone`, `priority`, `trace`, `status`
- [ ] Priority is one of: critical, high, medium, low
- [ ] Task `zone` is one of: core, knowledge, scripts, templates, data, loop, assets
- [ ] Task `status` is one of: pending, in_progress, done, skipped

## 3. Dependencies Check

- [ ] `depends_on` references only existing task IDs
- [ ] Dependencies form a DAG (no circular references)
- [ ] Phase order is logical (Knowledge/Audit → Setup → Build → Verify)

## 4. Blockers Check

- [ ] `blockers` array present (may be empty `[]`)
- [ ] Every blocker has: `id`, `type`, `description`, `resolved`
- [ ] Blocker `type` is one of: CLARIFICATION_NEEDED, DESIGN_CONFLICT, RESOURCE_MISSING
- [ ] No blocker has `resolved: false` when status is ready_for_builder

## 5. Prerequisites Check

- [ ] `prerequisites` array present
- [ ] Every prerequisite has: `item`, `tier`, `status`
- [ ] `tier` is one of: domain, technical, packaging
- [ ] `status` is one of: ready, missing, thin
- [ ] Missing prerequisites have `action_if_missing` filled

## 6. Handoff Ready Condition Check

- [ ] `handoff.next_stage: "builder"` present
- [ ] `handoff.ready_condition.required.blockers_empty: true` can be satisfied
- [ ] `handoff.ready_condition.required.phase0_done: true` — PH0 tasks all done
- [ ] `handoff.ready_condition.required.prerequisites_ready: true` — no missing critical prereqs
- [ ] `handoff.ready_condition.required.schema_valid: true` — YAML passes schema validation
- [ ] `handoff.ready_condition.required.design_zones_covered: true` — all 7 zones from design addressed

## 7. Resource Verification (Cốt lõi)

- [ ] **Existence**: Mọi tài nguyên liệt kê trong `todo.md` prerequisites đều có file tương ứng trong `resources/`.
- [ ] **Richness**: Tài liệu trong `resources/` không phải là file rỗng. Có đủ thông tin "hành động được" (actionable).
- [ ] **Traceability**: `todo.md` chỉ ra rõ task nào sử dụng tài nguyên nào qua `trace` field.

## 8. Gatekeeper Rule

- [ ] Planner có đang để trạng thái `ready_for_builder` trong khi blockers chưa resolved không? (NẾU CÓ -> Chuyển về `blocked`).
