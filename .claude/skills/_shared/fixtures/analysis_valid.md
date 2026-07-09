---
skill_name: "test-skill-one"
criteria_analysis:
  - criterion_id: "AC-01"
    description: "Must execute in sandbox"
    classification: "NFR"
metrics:
  - name: "Latency limit"
    value: 500.0
    unit: "ms"
risk_assessment:
  - risk_id: "RISK-01"
    edge_case: "Sandbox unavailable"
    mitigation: "Graceful abort"
---
# Analysis Report
This is the markdown body.
