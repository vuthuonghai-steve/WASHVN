---
skill_name: "test-skill-one"
target_variable: "data-sync"
zone_mapping:
  core:
    purpose: "Holds core logic"
    files: ["core.py"]
    constraints: ["no-external-deps"]
  knowledge:
    purpose: "Holds docs"
    files: ["rules.md"]
    constraints: ["max-700-tokens"]
  scripts:
    purpose: "Holds scripts"
    files: ["run.sh"]
    constraints: ["non-interactive"]
  templates:
    purpose: "Holds templates"
    files: ["temp.yaml"]
    constraints: ["yaml-only"]
  data:
    purpose: "Holds config"
    files: ["config.yaml"]
    constraints: ["no-hardcoded-secrets"]
  loop:
    purpose: "Holds loop mechanisms"
    files: ["state.yaml"]
    constraints: ["append-only"]
  assets:
    purpose: "Holds diagrams"
    files: ["flow.png"]
    constraints: ["optimized"]
data_contracts:
  - contract_id: "contract-01"
    description: "Syncs input configuration"
    input_schema: "raw/ver-3/_shared/schemas/exploration.schema.yaml"
    output_schema: "raw/ver-3/_shared/schemas/criteria.schema.json"
state_machine:
  initial_state: "IDLE"
  states: ["IDLE", "RUNNING", "COMPLETED"]
  transitions:
    - from: "IDLE"
      to: "RUNNING"
      trigger: "START"
must_not_rules:
  - "Rule 1: Too few rules."
---
# Design Document
This is the markdown body.
