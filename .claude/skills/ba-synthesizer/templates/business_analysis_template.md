---
# Template-level handoff fields (NOT the artifact frontmatter)
skill_name: "{{ skill_name }}"
target_skill: "{{ target_skill }}"
scs_complexity_score: {{ scs_complexity_score }}   # 0-10
quality_gate_status: "{{ quality_gate_status }}"     # PASS | WARNING
quality_score_percentage: {{ quality_score_percentage }}  # 0-100
pipeline_ready: {{ pipeline_ready }}                # true | false
---

> **Metadata:** `schema_ref: "synthesis.schema.yaml"` · `artifact_lifecycle: "WORM"`
> **Artifact frontmatter (4 fields):** `skill_name`, `synthesized_requirements[]`, `congruence_check{}`, `pipeline_ready`

# Báo Cáo Tổng Hợp Nghiệp Vụ: {{ skill_name }}

## §1: Cross-Reference Validation Results

### 1A. Actor-Entity Matching
- Trạng thái: {{ actor_entity_status }} `[TỪ ELICITATION]`
- Actor: {{ actor_count }} · Entity: {{ entity_count }} · Matching rate: {{ matching_rate }}%
- **Cảnh báo:** {{ actor_entity_warnings }}

### 1B. MoSCoW-Gherkin Matching
- Trạng thái: {{ moscow_gherkin_status }} `[TỪ ANALYSIS]`
- MoSCoW items: {{ moscow_count }} · Gherkin scenarios: {{ gherkin_count }}
- **Cảnh báo:** {{ moscow_gherkin_warnings }}

### 1C. Congruence Check Verdict
```yaml
congruence_check:
  conflicts_found: {{ conflicts_found }}
  conflicts_resolved: {{ conflicts_resolved }}
  check_verdict: "{{ check_verdict }}"
```

## §2: Quality Score Assessment

### 2A. Deliverable Scores (0.0–1.0)

| Mã | Deliverable | Trọng số | Score |
|:---|:------------|:--------:|:-----:|
| BA-DEL-01 | Elicitation Report & Thought Cache | 0.15 | {{ del_01_score }} |
| BA-DEL-02 | Classification & MoSCoW Matrix | 0.15 | {{ del_02_score }} |
| BA-DEL-03 | Sequence Diagram | 0.15 | {{ del_03_score }} |
| BA-DEL-04 | Flowchart Diagram | 0.15 | {{ del_04_score }} |
| BA-DEL-05 | Entity Relationship Diagram (ERD) | 0.15 | {{ del_05_score }} |
| BA-DEL-06 | Gherkin Acceptance Criteria | 0.15 | {{ del_06_score }} |
| BA-DEL-07 | Risk Assessment Matrix | 0.10 | {{ del_07_score }} |

### 2B. Weighted Sum
```yaml
quality_score:
  weights:
    BA-DEL-01: 0.15
    BA-DEL-02: 0.15
    BA-DEL-03: 0.15
    BA-DEL-04: 0.15
    BA-DEL-05: 0.15
    BA-DEL-06: 0.15
    BA-DEL-07: 0.10
  weighted_sum: {{ weighted_sum }}  # 0.0–1.0 (Σ score_i × weight_i)
  percentage: {{ percentage }}%     # 0–100
```

### 2C. Quality Gate Verdict
- **PASS** nếu percentage >= 80%, **WARNING** nếu < 80%
- Kết quả: **{{ quality_gate_status }}** ({{ percentage }}%)

## §3: Consolidated Requirements

> Merged từ elicitation + analysis, deduplicated, cross-referenced trace tags.

```yaml
synthesized_requirements:
  - req_id: "REQ-{{ seq_1 }}"
    title: "{{ req_title_1 }}"
    description: "{{ req_desc_1 }}"
    source: "{{ req_source_1 }}"
    classification: "{{ req_class_1 }}"
  - req_id: "REQ-{{ seq_2 }}"
    title: "{{ req_title_2 }}"
    description: "{{ req_desc_2 }}"
    source: "{{ req_source_2 }}"
    classification: "{{ req_class_2 }}"
  - req_id: "REQ-{{ seq_n }}"
    title: "{{ req_title_n }}"
    description: "{{ req_desc_n }}"
    source: "{{ req_source_n }}"
    classification: "{{ req_class_n }}"
```

Tổng: {{ total_requirements }} yêu cầu (FR: {{ fr_count }}, NFR: {{ nfr_count }}).

## §4: Pipeline Readiness

```yaml
pipeline_ready: {{ pipeline_ready }}
```

- **Điều kiện:** {{ condition_1 }} `[TỪ ELICITATION]`, {{ condition_2 }} `[TỪ ANALYSIS]`, {{ condition_3 }} `[SUY LUẬN]`
- **Blocker:** {{ blocker_1 }} `[CẦN LÀM RÕ]`, {{ blocker_2 }} `[CẦN LÀM RÕ]`
