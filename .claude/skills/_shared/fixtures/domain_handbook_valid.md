---
skill_name: "test-skill-one"
glossary:
  - term: "DRC"
    definition: "Dynamic Routing Contract"
  - term: "SSP"
    definition: "Simple State Protocol"
  - term: "SCS"
    definition: "Skill Complexity Score"
  - term: "WORM"
    definition: "Write Once Read Many"
  - term: "ADR"
    definition: "Architectural Decision Record"
  - term: "NFR"
    definition: "Non-Functional Requirement"
  - term: "FR"
    definition: "Functional Requirement"
  - term: "CLI"
    definition: "Command Line Interface"
  - term: "YAML"
    definition: "YAML Ain't Markup Language"
  - term: "JSON"
    definition: "JavaScript Object Notation"
anti_patterns:
  - name: "Placeholder leak"
    symptom: "Unimplemented blocks in code."
    solution: "Implement strict validation."
  - name: "Manual sync"
    symptom: "Stale skill copies."
    solution: "Use automated sync script."
  - name: "Direct editing"
    symptom: "Editing active skill workspace directly."
    solution: "Edit raw, then sync."
exemplars:
  - name: "Validator code"
    description: "Good implementation pattern."
domain_anchors:
  - "Anchor Word"
---
# Domain Handbook
This is the markdown body.
