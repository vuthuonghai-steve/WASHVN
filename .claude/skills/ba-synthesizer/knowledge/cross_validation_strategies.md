# Chiến lược Kiểm định Chéo & Chấm điểm Chất lượng (Cross-Validation & Quality Scoring Strategies)

Tài liệu kiến thức cốt lõi của `ba-synthesizer` (Stage BA-0.2). Gộp 3 tài liệu cũ (`cross-ref-rules.md`, `quality-criteria.md`, `quality-matrix.yaml`) thành 1 file 3 phần. Load on-demand từ SKILL.md.

<context>
Mục tiêu: (1) phát hiện sớm mâu thuẫn chéo giữa Sequence Diagram ↔ ERD và MoSCoW ↔ Gherkin; (2) chấm điểm chất lượng bằng weighted sum deterministic (KHÔNG dùng NLP/subjective); (3) neo trace tags giữa yêu cầu, sơ đồ, kịch bản và rủi ro.
</context>

---

## §1. Cross-Reference Validation Rules (Quy tắc Kiểm định Chéo)

Quét 2 nguồn (`elicitation-report.md` + `analysis-report.md`) để đối chiếu tính nhất quán.

### Rule 1 — Actor-Entity Matching (SD ↔ ERD)
- **Mô tả**: Mọi Actor/Participant trong Sequence Diagram phải có thực thể (bảng) tương ứng trong ERD.
- **Steps**:
  1. Quét `sequenceDiagram` Mermaid → trích xuất actors/participants.
  2. Quét `erd` Mermaid → trích xuất entities.
  3. So khớp: mỗi actor thao tác dữ liệu PHẢI có bảng trong ERD.
- **fail_trigger**: Actor/Participant trong SD không tồn tại trong ERD.
- **warning_tag**: `[MAU THUẪN NGHIỆP VỤ: Thực thể CSDL thiếu hụt]`
- **mitigation**: Bổ sung entity bị thiếu vào ERD HOẶC điều chỉnh SD cho đúng cấu trúc.

### Rule 2 — MoSCoW-Gherkin Matching (Must-Have ↔ Scenarios)
- **Mô tả**: Mọi tính năng Must-Have (P0) PHẢI có ≥1 Gherkin scenario (Happy + Exception).
- **Steps**:
  1. Lọc bảng MoSCoW → danh sách Must-Have.
  2. Quét Acceptance Criteria → trích xuất Scenario names.
  3. So khớp: 100% Must-Have có ≥1 scenario tương ứng.
- **fail_trigger**: Must-Have feature thiếu Gherkin scenario.
- **warning_tag**: `[THIẾU KỊCH BẢN KIỂM THỬ: Tính năng Must-Have chưa được bao phủ]`
- **mitigation**: Bổ sung scenario Given-When-Then cho Must-Have bị thiếu.

### Warning Tags (Semantic Anchors)
```yaml
warning_tags:
  MAU_THUAN_NGHIEP_VU:
    trigger: "Actor/participant trong Sequence Diagram không tồn tại trong ERD"
    format: "[MAU THUẪN NGHIỆP VỤ: Thực thể CSDL thiếu hụt]"
    severity: WARNING
  THIEU_KICH_BAN_KIEM_THU:
    trigger: "Must-Have feature (P0) không có Gherkin scenario tương ứng"
    format: "[THIẾU KỊCH BẢN KIỂM THỬ: Tính năng Must-Have chưa được bao phủ]"
    severity: WARNING
```
- **output_effect**:
  - consistent → `congruence_check.check_verdict: PASS`
  - có ≥1 warning chưa resolve → `conflicts_found: true`, resolve hết mới `conflicts_resolved: true`. Nếu không resolve được → `check_verdict: FAIL` (block pipeline).

---

## §2. Quality Criteria & Weighted Scoring (Tiêu chí & Chấm điểm Trọng số)

7 deliverables, weighted sum deterministic. Threshold **≥ 0.80 = PASS**, < 0.80 = WARNING (KHÔNG đổi thành 0.70).

### Weights
```
BA-DEL-01  Elicitation Report & Thought Cache        0.15
BA-DEL-02  Classification & MoSCoW Matrix            0.15
BA-DEL-03  Sequence Diagram                          0.15
BA-DEL-04  Flowchart Diagram                         0.15
BA-DEL-05  Entity Relationship Diagram (ERD)         0.15
BA-DEL-06  Gherkin Acceptance Criteria              0.15
BA-DEL-07  Risk Assessment Matrix                   0.10
                                                 Σ = 1.00
```

### Formula
```
weighted_sum = Σ(score_i × weight_i)  cho i = 1..7
quality_score_percentage = weighted_sum × 100
verdict: PASS nếu weighted_sum ≥ 0.80, WARNING nếu < 0.80
```

### Barem chấm điểm nhị phân (mỗi deliverable)
- **1.0** = Đạt ALL tiêu chí tối thiểu của deliverable đó.
- **0.5** = Đạt ≥50% tiêu chí, còn thiếu ≤1 tiêu chí phụ.
- **0.0** = Thiếu ≥2 tiêu chí chính HOẶC deliverable không tồn tại.

### Barem chi tiết per deliverable
```
BA-DEL-01: 1.0 = frontmatter + stakeholder + NFR quantified.      0.5 = thiếu 1/3.   0.0 = thiếu ≥2.
BA-DEL-02: 1.0 = FR/NFR + MoSCoW + justification.                 0.5 = thiếu justification. 0.0 = thiếu classification.
BA-DEL-03: 1.0 = ≥3 actors + double-quote + business flow.        0.5 = thiếu double-quote. 0.0 = <3 actors.
BA-DEL-04: 1.0 = 3 paths (Happy/Alt/Exception) rõ ràng.           0.5 = chỉ 2 paths. 0.0 = 1 path.
BA-DEL-05: 1.0 = PK/FK + data types.                              0.5 = thiếu data types. 0.0 = thiếu PK/FK.
BA-DEL-06: 1.0 = ≥3 scenarios + Given-When-Then.                  0.5 = 2 scenarios. 0.0 = <2.
BA-DEL-07: 1.0 = P×I matrix + mitigation.                        0.5 = thiếu mitigation. 0.0 = không có matrix.
```

### QUY TẮC NGHIÊM NGẶT
- KHÔNG tự chấm 1.0 nếu deliverable thiếu bất kỳ tiêu chí chính nào.
- KHÔNG dùng thang điểm subjective (0.7, 0.8, 0.9) — chỉ **1.0 / 0.5 / 0.0**.
- Quality matrix YAML embedded (tham khảo `policy/quality-matrix.yaml` cũ, giữ nguyên threshold 0.80):

### Neo Tiêu chuẩn Nghiệp vụ (Standards Anchors)
Chấm điểm tuân thủ các framework chuẩn — không chỉ name-drop:
- **BABOK** (Business Analysis Body of Knowledge): áp dụng Task "Validate Requirements" (chapter 6) — Rule 1/Rule 2 chính là bước verify tính khả thi & nhất quán của requirements trước handoff.
- **ISO/IEC 25010**: Quality characteristic `Functional suitability` (completeness, correctness) ↔ BA-DEL-01..02; `Compatibility`/`Reliability` ↔ risk matrix BA-DEL-07. Mỗi deliverable map vào 1 characteristic.
- **MoSCoW** (Priority): BA-DEL-02 bảng phân loại P0–P3 là input trực tiếp cho Rule 2 (Must-Have ↔ Gherkin).
- **FMEA** (Failure Mode & Effects Analysis): BA-DEL-07 Risk Matrix dùng Probability×Impact để rank severity — cùng logic FMEA Risk Priority Number.
```yaml
quality_matrix:
  rules:
    pass_threshold: 0.80
    calculation_method: weighted_sum
  deliverables:
    elicitation_report:    { weight: 0.15, min_criteria: [normalize_system_description, pain_points_listed, system_assumptions_defined] }
    requirements_classification: { weight: 0.15, min_criteria: [fr_nfr_separation, moscow_matrix_completed] }
    sequence_diagram:      { weight: 0.15, min_criteria: [valid_mermaid_syntax, minimum_three_actors] }
    flowchart_activity:    { weight: 0.15, min_criteria: [valid_mermaid_syntax, three_paths_defined] }
    erd_schema:            { weight: 0.15, min_criteria: [valid_mermaid_syntax, pk_fk_definitions, attribute_data_types] }
    acceptance_criteria:   { weight: 0.15, min_criteria: [gherkin_format_given_when_then, minimum_three_scenarios] }
    risk_matrix:           { weight: 0.10, min_criteria: [minimum_three_risks, mitigation_plans_provided] }
```

---

## §3. Trace Tags Convention (Quy ước Thẻ Truy vết)

Áp dụng convention từ ba-elicitor để neo ngữ cảnh:
```
[TỪ INPUT]    — trích xuất trực tiếp từ yêu cầu gốc (elicitation / analysis)
[SUY LUẬN]    — phân tích / suy diễn từ LLM (synthesizer)
[CẦN LÀM RÕ]  — điểm cần user xác nhận trước khi PASS
```

**Trace mapping** (mỗi requirement truy vết 4 chiều):
```
requirement_id  →  diagram (SD/Flow/ERD)  →  scenario (Gherkin)  →  risk (Matrix)
```

Ví dụ hợp lệ:
```
REQ-AUTH-01 [TỪ INPUT] User đăng nhập → SD: User/Agent → Gherkin: Login_Happy + Login_Exception → Risk: R-1 brute force
```
