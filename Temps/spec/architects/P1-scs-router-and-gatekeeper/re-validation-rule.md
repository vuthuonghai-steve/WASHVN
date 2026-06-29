# Re-validation Rule

> Role: **Gatekeeper** | Domain: **Quality** | Design: **Fallback**
> Source: `architecture-design.md §S1.5` (clean/)

## Purpose

Spec Gatekeeper (Stage 1.5) re-validates thought blocks from Stage 0 (BA Elicitor) using META-2.1 v2.0 criteria.

## Why

BA Elicitor has incentive to be "fast"; Gatekeeper has incentive to be "accurate". This is a second protection layer against slop.

## Process

1. Gatekeeper reads `thought-cache.yaml` from Context Bus
2. Validates thought blocks against META-2.1 (4 Depth Signals)
3. If any signal FAIL → log to `fallback_history` and trigger **F2 / F19**:
   - F2: Domain-handbook insufficient → re-elicitation (Stage 0)
   - F19: Stage 0 thought block FAIL META-2.1 → BA Elicitor must re-do with deeper thinking

## Coverage

- F16: `thought-cache.yaml` missing `business_thought_process` → Stage 0 re-do
- F17: `thought-cache.yaml` missing `stakeholder_empathy` or `reverse_questions` → Stage 0 re-do
- F19: META-2.1 4 signals not all met → Stage 0 re-do with 4 signals enforced

> Full fallback: see `P5-fallback-and-escalation/`
