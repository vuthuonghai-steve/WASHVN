# Interlock Checklist — BA Analyst Quality Gates

> [!NOTE]
> Quality Gate tự động cho `analyst-output.md`. 100% pass (không BORDERLINE) mới ghi file.
> Nếu bất kỳ QG nào FAIL → quay lại phase tương ứng sửa trước khi viết artifact.

```yaml
quality_gates:
  QG-BA-01:
    name: "Classification FR/NFR + MoSCoW"
    type: "Hard"
    phase: "A — Classification"
    criteria: "Mọi yêu cầu phân loại FR/NFR; MoSCoW P0-P3 đầy đủ; NFR có justification kỹ thuật."
    mandatory: true
  QG-BA-02:
    name: "Mermaid diagrams"
    type: "Hard"
    phase: "B — Diagrams"
    criteria: "Sequence ≥3 actors + labels double-quote; Flowchart 3-path; ERD có PK/FK + kiểu dữ liệu."
    mandatory: true
  QG-BA-03:
    name: "NFR metrics quantified"
    type: "Hard"
    phase: "B — Diagrams"
    criteria: "metrics[].name + value (số) + unit tồn tại; name KHÔNG chứa từ mơ hồ (nhanh/mượt/an toàn...)."
    mandatory: true
  QG-BA-04:
    name: "Gherkin ≥3 scenarios"
    type: "Hard"
    phase: "C — Gherkin"
    criteria: "≥3 Scenario (Happy + Alternative + Exception) + User Story format; zero placeholder."
    mandatory: true
  QG-BA-05:
    name: "Risk Matrix P×I + mitigation"
    type: "Hard"
    phase: "D — Risk"
    criteria: "risk_assessment[].risk_id + edge_case + mitigation (không trống); align rủi ro cao + P0."
    mandatory: true
```

## Execution Checklist

### Phase A — Classification
- [ ] **Must**: 100% NFR lượng hóa bằng số đo lường cụ thể?
- [ ] **Must**: Mỗi dòng MoSCoW có cột giải thích kỹ thuật cụ thể?

### Phase B — Diagrams & Metrics
- [ ] **Must**: Sequence ≥3 participants, labels double-quote?
- [ ] **Must**: Flowchart có Happy/Alternative/Exception paths?
- [ ] **Must**: ERD có PK/FK + kiểu dữ liệu mỗi cột?
- [ ] **Must**: metrics[].value là số (number), không phải string?

### Phase C — Gherkin
- [ ] **Must**: ≥3 scenarios phủ Happy/Alternative/Exception?
- [ ] **Must**: Không từ mơ hồ / placeholder trong Gherkin?

### Phase D — Risk
- [ ] **Must**: Mọi risk có mitigation kỹ thuật cụ thể (không chung chung)?
- [ ] **Must**: Rủi ro Cao + P0 có mitigation trong MVP?

### Phase E — Traceability & Gate
- [ ] **Must**: validate_metrics.py → 8/8 PASS (exit 0)?
- [ ] **Must**: schema_validator.py --path analyst-output.md → exit 0 (4 required fields)?
- [ ] **Must**: Trace tags [TỪ INPUT]/[SUY LUẬN]/[CẦN LÀM RÕ] gắn đầy đủ?

## Approval Thresholds

```yaml
approval_rules:
  pass_threshold: "100% các mục Must đạt PASS (QG-BA-01 → QG-BA-05)."
  failure_action: "Bất kỳ FAIL → tái tạo/chỉnh sửa artifact đến khi pass hoàn toàn."
```
