# External Skill Adapter

> Role: **Deconstructor** | Domain: **Migration** | Design: **Contract**
> Source: `skill-migration-spec.md §14.2` (clean/)

## Purpose

Reads non-WASHVN skill code (external repos, raw Python/JS/Go files) and converts to standardized metadata and contracts.

## Input

External source directory with arbitrary structure containing:
- `.py`, `.js`, `.go` source files
- Prompt files
- Configuration files

## Process

1. Scan entire directory recursively
2. Use LLM analysis to determine:
   - Original persona/goal of the skill
   - Core logic entry points
   - Configuration patterns
   - Dependencies
3. Map to canonical WASHVN contracts:
   - Persona → SKILL.md persona
   - Logic → knowledge/ files
   - Configs → scripts/ + templates/
   - Validation → data/ contracts

## Output

```yaml
deconstructed_context:
  original_persona: "Micro-skill that validates OTP inputs"
  advantages_and_intent: "Handles rate limiting and replay attack prevention"
  extracted_knowledge:
    - file_name: "otp-rules.md"
      content: "OTP must be 6 digits, E.164 phone format..."
  extracted_guardrails:
    original_must: ["Validate OTP format before processing"]
    original_must_not: ["Do not log plain-text OTP"]
  extracted_contracts:
    - contract_id: "otp_validation"
      path_template: "custom/otp_validate.py"
      format: "python"
```

## Risk

LLM analysis may hallucinate intent for complex external code. Human verification recommended before REBUILD.
