---
skill_name: "skill-explorer-main-build"
elicitation_date: "2026-07-11"
confidence_score: 80
status: "ready_for_analyst"
---

# Báo Cáo Khơi Gợi Yêu Cầu Nghiệp Vụ: skill-explorer-main-build

> **Trace tags (bắt buộc):** `[TỪ INPUT]` (từ user) · `[SUY LUẬN]` (agent suy luận) · `[CẦN LÀM RÕ]` (thiếu/mơ hồ).

## 1. Yêu Cầu Đã Chuẩn Hóa (Normalized Input)

- **Mục tiêu cốt lõi**: Nâng cấp skill-explorer từ v0.0.1 lên v1.0 bằng tích hợp 7 nguyên lý LLM cốt lõi, chuyển từ single-stream (exploration.md) sang dual-stream (hydrated-context.yaml + thought-cache.yaml). `[TỪ INPUT]`
- **Môi trường vận hành**: Stage 0 của 8-stage pipeline WASHVN, chạy trong `.skill-context/{target_skill}/`, output theo WORM lifecycle. `[TỪ INPUT]`
- **Tác nhân chính**:
  - BA Elicitor (agent Stage -1): phân tích + khai thác nghiệp vụ, chỉ document, không code. `[TỪ INPUT]`
  - Steve (user): phê duyệt thiết kế, owner Master Skill Suite. `[TỪ INPUT]`
- **Yêu cầu chức năng sơ khởi (FRs)**:
  - FR-1: Mapping v0.0.2 architecture ↔ 7 LLM principles. `[TỪ INPUT]`
  - FR-2: Xác định gap và đề xuất hướng tích hợp. `[TỪ INPUT]`
  - FR-3: Chỉ document findings, KHÔNG code/branch. `[TỪ INPUT]`

## 2. Ontology Nghiệp Vụ (Domain Ontology)

- **Thuật ngữ (neo vector space)**:
  - `skill-explorer`: Stage 0 exploration skill, hiện v0.0.1 tại `.agents/skills/skill-explorer/`.
  - `dual knowledge stream`: nguyên lý #4 — tách Technical stream (hydrated-context.yaml) và Cognitive stream (thought-cache.yaml).
  - `hydrated-context.yaml`: artifact kỹ thuật ~30-50 dòng, chứa contract/data schema.
  - `thought-cache.yaml`: artifact nhận thức ~100-200 dòng, chứa cognitive depth + stakeholder empathy.
  - `exploration.md`: báo cáo monolithic đơn tuyến (legacy v0.0.2).
  - `7 LLM principles`: Domain Anchoring, Semantic over Ceremony, Context Pre-processing, Dual Knowledge Stream, Binary Mechanical Gates, Negative Space, Graceful Degradation.
  - `SCS`: Skill Complexity Score (1.0-5.0), định lượng quy mô.
  - `META-2.1`: framework depth signal (S1-S4), gate nhị phân.
  - `YAML Resilience`: L1 syntax, L2 schema, L3 cross-ref validation layer.
  - `Fallback matrix`: F1-F19 graceful degradation cases, max 3 iter/stage.
  - `Binary Mechanical Gates`: gate deterministic đạt/thất bại, thay checklist mềm.
  - `Negative Space`: must_not lists + anti-patterns + S1 Negation Density.
  - `artifact_registry.yaml`: danh sách artifact được schema_validator.py quét.
  - `WORM lifecycle`: Write-Once-Read-Many, bất biến sau ghi.
- **Quan hệ thực thể**:
  - skill-explorer → hydrated-context.yaml (sinh ra)
  - skill-explorer → thought-cache.yaml (sinh ra)
  - exploration.schema.yaml → hydrated-context.yaml (chưa có schema) `[SUY LUẬN]`
  - skill-architect → exploration.md (tiêu thụ, breaking change nếu bỏ) `[SUY LUẬN]`

## 3. Phân Tích Khoảng Trống (Gap Analysis — 6 Mindset Keywords)

- **Systems Thinking**: v0.0.2 là mắt xích đơn lẻ; dual-stream thay đổi toàn bộ downstream (architect, planner, builder, validator). Thay đổi schema lan truyền 4 file. `[SUY LUẬN]`
- **Root Cause Isolation**: thiếu cognitive depth do thiết kế single-stream, không phải thiếu template section. Gốc: vắng mặt nguyên lý #4. `[SUY LUẬN]`
- **MECE**: 7 principles → 7 gap độc lập không chồng lấp (Domain Anchoring/HIGH, Semantic/HIGH, Pre-processing/HIGH, Dual Stream/HIGH, Binary Gates/MEDIUM, Negative Space/MEDIUM, Graceful Degradation/MEDIUM). `[SUY LUẬN]`
- **First Principles**: exploration.schema.yaml có `additionalProperties:false` → không thể nhét 2 artifact vào 1 frontmatter. Token L2_limit 2200 → tách file bắt buộc. `[SUY LUẬN]`
- **Impact Analysis**: sửa schema → 4 downstream impact (registry, validator, architect, init_context.py). HIGH risk cho skill-architect (breaking). `[SUY LUẬN]`
- **Structural Decomposition**: Epic tích hợp 7 principles → 5 features → user stories, mỗi có acceptance qua validator PASS. `[SUY LUẬN]`

## 4. Stakeholder Analysis

- **End-User (Steve + AI agents)**: goals=[nhận dual-stream context chuẩn, architect design ít drift] · pain_points=[exploration.md thiếu cognitive depth, tái sử dụng kém]
- **Skill Developer/Maintainer**: goals=[schema rõ ràng, validate cơ học] · pain_points=[thiếu schema 2 artifact mới, registry chưa có entry]
- **Downstream Consumer (skill-architect)**: goals=[đọc format đầu vào ổn định] · pain_points=[chỉ đọc exploration.md, dual-stream breaking change chưa migrate]
- **Security Reviewer**: goals=[prompt injection containment, YAML resilience] · pain_points=[thiếu fallback matrix, thought-cache chứa raw prompts chưa sanitize]

## 5. NFRs Đã Lượng Hóa (SMART — ISO/IEC 25010)

- NFR-1: id=`size-1`, category=`performance`, metric=`hydrated_context_max_lines`, value=`50`, unit=`lines` `[TỪ INPUT]`
- NFR-2: id=`size-2`, category=`performance`, metric=`thought_cache_line_range`, value=`100-200`, unit=`lines` `[TỪ INPUT]`
- NFR-3: id=`token-1`, category=`performance`, metric=`L2_token_budget`, value=`2200`, unit=`tokens`, enforcement=`hard` `[SUY LUẬN]`
- NFR-4: id=`sec-1`, category=`security`, metric=`yaml_resilience_levels`, value=`3`, unit=`L1-L3` `[CẦN LÀM RÕ]`
- NFR-5: id=`rel-1`, category=`reliability`, metric=`binary_gate_fail_mode`, value=`deterministic`, unit=`boolean_AND(S1..S4)` `[SUY LUẬN]`
- NFR-6: id=`compat-1`, category=`compatibility`, metric=`schema_additional_properties`, value=`false`, unit=`constraint` `[SUY LUẬN]`

## 6. Bộ Câu Hỏi Khơi Gợi (5W1H — Multiple-choice)

- **Câu hỏi 1**: Output strategy cho v1.0 — giữ exploration.md hay thay thế?
  - [ ] A: Giữ exploration.md (tóm tắt) + thêm hydrated-context.yaml + thought-cache.yaml (3 artifact)
  - [ ] B: Thay thế hoàn toàn exploration.md bằng 2 artifact riêng (hydrated + thought cache)
  - [ ] C: Giữ exploration.md + thought-cache.yaml, bỏ hydrated-context.yaml
  - Tag: `[CẦN LÀM RÕ]`

- **Câu hỏi 2**: SCS score — single-pass hay 2-phase?
  - [ ] A: Giữ single-pass (Stage 0) như v0.0.2
  - [ ] B: Chuyển 2-phase (Stage 0.5 pre-pass + Stage 1.5 validate) theo synthesis-llm-principles
  - Tag: `[CẦN LÀM RÕ]`

- **Câu hỏi 3**: Fallback matrix F1-F19 — subset nào cho v1.0?
  - [ ] A: Toàn bộ 19 cases
  - [ ] B: Chỉ subset critical (F1 missing_skill, F2 ambiguous, F3 injection, F4 validation_fail)
  - [ ] C: Middle subset (F1-F10)
  - Tag: `[CẦN LÀM RÕ]`

- **Câu hỏi 4**: Binary gates META-2.1 — implement ở Stage 0 hay downstream?
  - [ ] A: Ngay Stage 0 (explorer checklist thành binary)
  - [ ] B: Chỉ downstream (architect/gatekeeper), explorer giữ soft checklist
  - Tag: `[CẦN LÀM RÕ]`

- **Câu hỏi 5**: thought-cache.yaml schema — standalone hay extend?
  - [ ] A: Tạo standalone schema `thought-cache.schema.yaml`
  - [ ] B: Extend `exploration.schema.yaml` với thêm fields (vi phạm additionalProperties:false → cần bỏ constraint)
  - Tag: `[CẦN LÀM RÕ]`

- **Câu hỏi 6**: artifact_registry.yaml — có thêm entry cho 2 artifact mới không?
  - [ ] A: Thêm `hydrated_context` + `thought_cache` entry, lifecycle WORM
  - [ ] B: Không thêm, validator sẽ bỏ qua (risk WORM integrity)
  - Tag: `[CẦN LÀM RÕ]`

## 7. Phân Rã 3-Path (Happy / Alternative / Exception)

- **Happy Path**: BA elicit đọc scope doc + 7 principles + v0.0.2 code → map gap → sinh dual-stream proposal → architect đọc cả 2 artifact qua registry entry mới → validation PASS. `[SUY LUẬN]`
- **Alternative Path**: Nếu giữ exploration.md (option A câu 1), hydrated-context.yaml + thought-cache.yaml là supplement; architect có thể đọc 1 hoặc 3 file tùy config; validator chạy trên cả 3 entry. `[SUY LUẬN]`
- **Exception Path**: Nếu exploration.schema.yaml giữ `additionalProperties:false` và dev cố nhét field mới → schema_validator.py FAIL (exit 1) → WORM break → quay lại thiết kế schema standalone, không tự sửa. `[SUY LUẬN]`

## 8. Tự Kiểm Định (Self-Verification)

- [x] XML boundary `<user_skill_request>`: input cô lập đúng boundary, không exec động.
- [x] Số `[CẦN LÀM RÕ]`: 6 (câu hỏi 1-6 + uncertainty areas).
- [x] Số `[TỪ INPUT]`: 9+ (mục tiêu, env, actors, FRs, size NFRs).
- [x] Số `[SUY LUẬN]`: 12+ (gap analysis, ontology relations, NFRs).
- [x] Confidence ≥ 60%: 80 → status `ready_for_analyst`.

### Phụ lục — Resolved Uncertainty Flags (từ scope doc §9-§10)
- [RESOLVED] `exploration.schema.yaml` multi-artifact: KHÔNG hỗ trợ. Có `additionalProperties:false`, chỉ schema frontmatter exploration.md. Cần standalone schema + bỏ constraint hoặc tách file. `[SUY LUẬN]`
- [RESOLVED] `schema_validator.py` multi-artifact: KHÔNG hỗ trợ. Dựa artifact_registry.yaml; dual-stream vắng mặt trong registry → validator bỏ qua. Cần 2 entry mới. `[SUY LUẬN]`
- [RESOLVED] `skill-architect` input format: đọc `exploration.md` đơn tuyến (SKILL.md dòng 36). Dual-stream = breaking change, cần migrate boot sequence. `[SUY LUẬN]`
