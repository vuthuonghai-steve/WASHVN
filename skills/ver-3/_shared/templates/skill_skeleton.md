---
name: "skill-name-placeholder"
description: "A detailed description of the skill's purpose and functionality"
suite: "WASHVN"
version: "0.0.1"
category: "general"
stage: 0
target_variable: "target-variable-name"
tags: ["tag1", "tag2"]
when_to_use: "Describe when this skill should be activated"
output_contract: "raw/ver-3/_shared/templates/drc_contract_template.yaml"
---

# Skill Description

<instructions>
Define the core imperatives, rules, and logic for the skill.
Use imperative tone (Do X, Never Y).
Ensure rules are clear and structured.
</instructions>

<safety_contract>
Specify security boundaries, restricted tools, and sandbox configuration.
Define limits on token usage, execution time, and repair attempts.
</safety_contract>

<knowledge_anchors>
Provide semantic mappings, ontology references, and domain configuration.
Reference external docs, guidelines, or dictionaries.
</knowledge_anchors>

<workflow_phases>
Describe the step-by-step execution path of the skill from start to finish.
Include checkpoints, validation triggers, and data capture steps.
</workflow_phases>

<input_contract>
Define the input requirements, files, and schemas that must exist before execution.
</input_contract>

<output_contract>
Define the output artifacts, schemas, and persistence rules.
</output_contract>

<acceptance_criteria>
Specify Gherkin or checklist acceptance criteria for this skill to pass verification.
</acceptance_criteria>

<failure_modes>
Identify potential failure points, error signals, and fallback paths (e.g. rollback_request.yaml).
</failure_modes>
