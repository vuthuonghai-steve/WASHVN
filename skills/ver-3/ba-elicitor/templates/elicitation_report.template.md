---
skill_name: "{{ skill_name }}"
elicitation_date: "{{ date }}"
confidence_score: {{ confidence }}   # 0-100
status: "{{ status }}"               # clarify_needed | ready_for_analyst
---

# Báo Cáo Khơi Gợi Yêu Cầu Nghiệp Vụ: {{ skill_name }}

> **Trace tags (bắt buộc):** `[TỪ INPUT]` (từ user) · `[SUY LUẬN]` (agent suy luận, ghi rõ lý do) · `[CẦN LÀM RÕ]` (thiếu/mơ hồ).

## 1. Yêu Cầu Đã Chuẩn Hóa (Normalized Input)

- **Mục tiêu cốt lõi**: {{ core_objective }} `[TỪ INPUT]` / `[SUY LUẬN]`
- **Môi trường vận hành**: {{ operating_environment }} `[TỪ INPUT]`
- **Tác nhân chính**:
  - {{ actor_1 }}: {{ actor_1_role }} `[TỪ INPUT]`
- **Yêu cầu chức năng sơ khởi (FRs)**:
  - FR-1: {{ fr_1 }} `[TỪ INPUT]`

## 2. Ontology Nghiệp Vụ (Domain Ontology)

- **Thuật ngữ (≥10 terms, neo vector space)**:
  - `{{ term_1 }}`: {{ definition_1 }}
  - `{{ term_2 }}`: {{ definition_2 }}
- **Quan hệ thực thể**:
  - {{ source }} → {{ target }} ({{ rel_type }})

## 3. Phân Tích Khoảng Trống (Gap Analysis — 6 Mindset Keywords)

- **Systems Thinking**: {{ gap_systems }} `[SUY LUẬN]`
- **Root Cause Isolation**: {{ gap_root_cause }} `[SUY LUẬN]`
- **MECE**: {{ gap_mece }} `[SUY LUẬN]`
- **First Principles**: {{ gap_first_principles }} `[SUY LUẬN]`
- **Impact Analysis**: {{ gap_impact }} `[SUY LUẬN]`
- **Structural Decomposition**: {{ gap_decomp }} `[SUY LUẬN]`

## 4. Stakeholder Analysis (≥2 góc độ)

- **{{ role_1 }}**: goals=[{{ goals_1 }}] · pain_points=[{{ pain_1 }}]
- **{{ role_2 }}**: goals=[{{ goals_2 }}] · pain_points=[{{ pain_2 }}]

## 5. NFRs Đã Lượng Hóa (SMART — ISO/IEC 25010)

- NFR-1: id=`perf-1`, category=`performance`, metric=`latency_p95`, value=`{{ v1 }}`, unit=`ms` `[SUY LUẬN]`
- NFR-2: id=`sec-1`, category=`security`, metric=`token_expiry`, value=`{{ v2 }}`, unit=`min` `[CẦN LÀM RÕ]`

## 6. Bộ Câu Hỏi Khơi Gợi (5W1H — Multiple-choice)

### Who / What
- **Câu hỏi 1**: {{ who_what_q }}
  - [ ] A: {{ opt_a }}
  - [ ] B: {{ opt_b }}
  - [ ] C: {{ opt_c }}
  - Tag: `[CẦN LÀM RÕ]`

### How / When
- **Câu hỏi 2**: {{ how_when_q }}
  - [ ] A: {{ opt_a2 }}
  - [ ] B: {{ opt_b2 }}
  - Tag: `[CẦN LÀM RÕ]`

## 7. Phân Rã 3-Path (Happy / Alternative / Exception)

- **Happy Path**: {{ happy }} `[SUY LUẬN]`
- **Alternative Path**: {{ alternative }} `[SUY LUẬN]`
- **Exception Path**: {{ exception }} `[SUY LUẬN]`

## 8. Tự Kiểm Định (Self-Verification)

- [ ] XML boundary `<user_skill_request>`: {{ xml_status }}
- [ ] Số `[CẦN LÀM RÕ]`: {{ clarify_count }}
- [ ] Số `[TỪ INPUT]`: {{ input_count }}
- [ ] Số `[SUY LUẬN]`: {{ inference_count }}
- [ ] Confidence ≥ 60%: {{ conf_ok }}
