# Integration Assembler (Stage 3c)

> Role: **Assembler** | Domain: **Execution** | Design: **Integration**
> Source: `architecture-design.md §S3c` (clean/)

## Responsibilities

1. Collect outputs from N micro-skill builders
2. Validate SSP contracts across micro-skills (schema matching)
3. Generate `orchestrate.py` — runtime coordination script
4. Merge into complete micro-skill bundle
5. Generate `integration-test-report.md`

## Process

```
Orchestrator → micro-skill-1, micro-skill-2, micro-skill-3
       │
       ▼
Integration Assembler:
  1. Collect all micro-skill packages
  2. Validate SSP contracts (input_schema ↔ output_schema)
  3. Generate orchestrate.py
  4. Run integration test
  5. Output: integration-test-report.md + micro-skill-bundle/
```

## Output structure

```
micro-skill-bundle/
├── orchestrate.py          # SSP runtime coordinator
├── ms-01-otp-validation/
├── ms-02-payment-gateway/
├── ms-03-webhook-handler/
└── integration-test-report.md
```

## Fallback

- F11: Review fail (Branch B) → back to Stage 3c (re-assemble)
- F14: Sandbox fail (Branch B) → back to Stage 3c (re-assemble)
