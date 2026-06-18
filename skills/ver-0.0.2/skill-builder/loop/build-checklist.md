# Build Checklist: Skill Builder Self-Verification — ver-2.0.0
# [TỪ DESIGN §3 loop/build-checklist.md, BA §1.1 S5, design.md §3 (mirror of YAML)]
# v2.0.0 changes vs v1.0.0:
#   - Add §11 "Tier Knowledge Parity" (KG-9 closure, Q5 RESOLVED)
#   - Add §12 "Token Budget Enforcement" (NFR-03, Q3 RESOLVED)
#   - Add §13 "Zone Contract Strictness" (G7 enforcement)

## 1. Structure Check (Vùng Kiến trúc)
- [ ] Sự hiện diện của các Zone bắt buộc (Core, Knowledge, Scripts, Loop, Policy, Templates, Data, Examples, References).
- [ ] Tuân thủ quy tắc đặt tên file: kebab-case cho resources/knowledge/scripts.
- [ ] File `SKILL.md` nằm đúng vị trí tại root của skill.

## 2. Source & Design Check (Đối chiếu Nguồn)
- [ ] Nội dung bám sát 100% bản thiết kế `design.md`.
- [ ] **Zone Contract Fidelity**: Tất cả files được tạo ĐỀU CÓ tên cụ thể trong `design.md §3` (Files cần tạo). Tuyệt đối KHÔNG tự ý tạo file/thư mục mới khác ngoài thiết kế.
- [ ] **Core Alignment**: `SKILL.md` đã tích hợp `design.md §7` (vào Boot Sequence), `§5` (Workflow Steps), và `§6` (Interaction Gates).
- [ ] Mọi mục `[CẦN LÀM RÕ]` trong `todo.md` đã được giải quyết hoặc trả lời tại `design.md §9`.
- [ ] Mọi Task trong `todo.md` đồng bộ với thực tế file đã tạo.
- [ ] Đã tạo `Resource Inventory` trong `.skill-context/{target_skill}/build-log.md`.
- [ ] Đã tạo `Resource Usage Matrix` trong `.skill-context/{target_skill}/build-log.md`.
- [ ] 100% file `Critical` (`design.md`, `todo.md`, `resources/*`, `data/*`) có evidence được dùng.

## 3. Progressive Disclosure Check (Phân tầng thông tin)
- [ ] Mọi file Tier 2 đều được dẫn link từ `SKILL.md` hoặc registry `data/builder-knowledge-sources.yaml`.
- [ ] File Tier 1 đã được đưa rõ vào 'Mandatory Boot Sequence' của `SKILL.md` dựa theo `design.md §7`.
- [ ] Không có file mồ côi (Orphan files) không được sử dụng.
- [ ] `SKILL.md` < 500 dòng.

## 4. Build-Log Template & Schema Check (build-log.schema.yaml)

- [ ] `build-log.md.template` has YAML frontmatter matching build-log.schema.yaml
- [ ] `execution_trace` array has entries with: timestamp, task_id, action, status
- [ ] `action` is one of: CREATE_FILE, MODIFY_FILE, VALIDATE, RUN_SCRIPT
- [ ] `status` is one of: success, failed, skipped
- [ ] `feedback_to_planner: []` and `feedback_to_architect: []` present
- [ ] `quality_metrics` has: placeholder_ratio (0..1), critical_tasks_done (bool), validator_pass (bool)
- [ ] `stage: "builder"` and NO handoff field (Builder is final stage)
- [ ] Comment: "Snapshot từ feedback.yaml. Builder KHÔNG update trực tiếp."

## 5. Completeness & Performance (Hoàn thiện & Chất lượng)
- [ ] Mật độ Placeholder `[MISSING_DOMAIN_DATA]` < 5 (Normal). Thresholds unified: <5 PASS / 5-9 WARNING / >=10 FAIL.
- [ ] **Zero-Summarization Verification**: Đã đối soát 1:1 với resources; không có hiện tượng tóm tắt hay lược bỏ chi tiết kỹ thuật.
- [ ] Script `validate_skill.py` trả về Exit Code 0 (PASS).
- [ ] Nhật ký `build-log.md` phản ánh trung thực trạng thái validation.

## 6. Engineer Stance (Thẩm định Kỹ sư)
- [ ] Đã thực hiện phản biện bản thiết kế (nếu có phi logic).
- [ ] Quy trình xử lý lỗi tuân thủ Log-Notify-Stop (Dừng ngay khi có lỗi hệ thống).
- [ ] Không có kết luận nào không truy vết được về resource hoặc design/todo.

## 7. Anthropic Skill Standards Compliance (BẮT BUỘC cho mọi SKILL.md)

> Reference: `knowledge/anthropic-skill-standards.md`

### 7.1 YAML Frontmatter
- [ ] `SKILL.md` bắt đầu bằng YAML frontmatter (`---` block) tại dòng 1.
- [ ] `name`: lowercase-kebab-case, ≤ 64 ký tự, không có reserved words.
- [ ] `description`: ngôi thứ 3, bao gồm WHAT + WHEN trigger, ≤ 1024 ký tự.
- [ ] `description` KHÔNG dùng "I can...", "You can use this to...".

### 7.2 Progressive Disclosure
- [ ] `SKILL.md` body ≤ 500 lines.
- [ ] Knowledge/template/loop files được link từ **đúng phase cần**, không phải tất cả ở Boot Sequence.
- [ ] Không có file được front-loaded mà không cần ngay từ đầu mọi invocation.
- [ ] References one level deep (không có nested: A.md → B.md → content).

### 7.3 Workflow Tracker Checklist
- [ ] Nếu skill có 3+ phases hoặc Interaction Points → có Tracker Checklist trong SKILL.md.
- [ ] Tracker Checklist yêu cầu Claude copy vào response ngay khi bắt đầu.

### 7.4 Examples Pattern
- [ ] Nếu skill có abstract mapping (schema→component, data→format, rule→output) → có examples file.
- [ ] Examples file được reference từ phase cần dùng (không front-load).
- [ ] Examples là concrete (real field names, real values) không phải trừu tượng.

### 7.5 Content Quality
- [ ] Không có time-sensitive information (ngày tháng, "before/after YYYY-MM").
- [ ] Terminology nhất quán xuyên suốt tất cả files.
- [ ] Scripts handle errors explicitly (không punt to Claude).
- [ ] Mỗi knowledge file có header `> **Usage**: ...` mô tả khi nào load.

---

## 8. Token Budget Check (ver-0.0.3, NFR-03)

> Reference: `knowledge/builder-token-budget.md` (KG-8, Tier 2)

- [ ] **SKILL.md ≤ 400 tokens** (L0 strict, Q3 RESOLVED). 500-700 = warning. > 700 = FAIL → split to `policy/`.
- [ ] **policy/*.yaml ≤ 1200 tokens** (L1 budget).
- [ ] **knowledge/*.md ≤ 2500 tokens/file** (L2 budget).
- [ ] **examples/*.md ≤ 1500 tokens/file** (L3 budget).
- [ ] Mọi file sau khi ghi phải đếm tokens bằng `tiktoken cl100k_base` (hoặc fallback estimation).

---

## 9. Zone Contract Strictness (ver-0.0.3, G7)

> Reference: `policy/skill-builder.yaml` §zone_contract

- [ ] Parser sử dụng section-number pattern `^## 3\.\s+` (R1 fix) — không literal "## 3. Zone Mapping".
- [ ] Mọi file trong `design.md §3 Zone Mapping` PHẢI tồn tại trong `{runtime_dest}/{target_skill}/`.
- [ ] KHÔNG tạo `README.md`, `LICENSE`, `Makefile` trừ khi có trong `§3`.
- [ ] Extra files (ngoài §3) trigger warning, không block build (trừ `scripts/__pycache__/`).

---

## 10. Format Compliance (Format Standards)

- [ ] XML tags present: `<instructions>`, `<context>`, `<examples>`, `<output_contract>`.
- [ ] YAML blocks use `must:`, `must_not:`, `priority_order:`.
- [ ] Trace tags: `[TỪ DESIGN §N]`, `[GỢI Ý BỔ SUNG]`, `[TỪ AUDIT TÀI NGUYÊN]`, `[CẦN LÀM RÕ]`.
- [ ] No legacy trace tags: `[GỢI Ý]`, `[TỪ AUDIT]`, `[TỪ AUDIT CUSTOM]`, `[CẦU LÀM RÕ]`.
- [ ] YAML frontmatter at line 1 of SKILL.md.

---

## 11. Tier Knowledge Parity (ver-0.0.3, KG-9 closure)

> Reference: `data/builder-knowledge-sources.yaml`

- [ ] **KG-1**: `knowledge/builder-knowledge-boot-sequence.md` exists (Tier 1 boot).
- [ ] **KG-2**: `knowledge/skill-builder-script-boundary-policy.md` exists (Tier 2 scripts).
- [ ] **KG-4**: `examples/build-exemplars.md` exists (Tier 2 concrete builds).
- [ ] **KG-5**: `policy/skill-builder.yaml` exists (Tier 1 L1 working policy).
- [ ] **KG-6**: `data/builder-knowledge-sources.yaml` exists (Tier 1 knowledge source registry).
- [ ] **KG-7**: `templates/build-log.md.template` exists (Tier 2 scaffold).
- [ ] **KG-8**: `knowledge/builder-token-budget.md` exists (Tier 2 token budget).
- [ ] **KG-10**: `docs/MIGRATION-0.0.2-to-0.0.3.md` exists (Tier 3 migration).
- [ ] **Coverage**: ≥ 8/10 (KG-3 visualization + KG-9 fidelity deferred to ver-0.0.4).

---

## 12. Token Budget Enforcement (ver-0.0.3, NFR-03)

- [ ] `loop/build-checklist.yaml` v2.0.0 has `token_budget_enforcement:` block.
- [ ] SKILL.md token count logged in `build-log.md` `quality_metrics.skill_md_token_count`.
- [ ] Each zone file token count checked at Phase 4 VERIFY.
- [ ] No file exceeds hard_cap (L0: 700, L1: 1500, L2: 3000, L3: 2000).

---

## 13. Zone Contract Strictness (ver-0.0.3, G7)

- [ ] Validator uses `^## 3\.\s+` section-number pattern (R1 refactor).
- [ ] Helper `_parse_zone_mapping(design_path)` shared between `check_file_mapping` + `check_todo_cross_reference`.
- [ ] Recursive sub-skill calls in `report()` wrapped in try/except IOError.
- [ ] `loop/build-checklist.yaml` has `zone_contract_strictness: { enabled: true, parser_pattern: "^## 3\\.\\s+" }`.

---

## 14. Stage 3.5 Review Handoff (ver-0.0.3)

> Reference: `loop/build-checklist.yaml` §stage_3_5_review_reference

- [ ] `build-log.md` has all 3 mandatory sections: Resource Inventory + Resource Usage Matrix + Validation Result.
- [ ] `build-log.md` includes `quality_metrics` block: placeholder_ratio, zone_coverage, critical_tasks_done, validator_pass, checklist_pass, trace_tag_coverage, skill_md_token_count.
- [ ] `build-log.md` includes `feedback_to_planner: []` and `feedback_to_architect: []` arrays.
- [ ] `.skill-context/{target_skill}/_state.yaml` lifecycle: `build-completed`.
- [ ] Production-code-reviewer (Stage 3.5) can consume build-log.md without re-reading todo.md or design.md.
