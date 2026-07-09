---
skill_name: "test-skill-one"
tasks:
  - task_id: "task-01"
    description: "Prepare project structure"
    zone: "core"
    priority: "urgent"
    input_schema: "raw/ver-3/_shared/schemas/exploration.schema.yaml"
    output_schema: "raw/ver-3/_shared/schemas/criteria.schema.json"
    verification_cmd: "python3 test.py"
    must_not:
      - "No stub files."
dag_dependencies: []
total_tasks: 1
---
# Todo Plan
This is the markdown body.
