# Guardrails & Negation Space (fail-closed)
# [TỪ DESIGN §2.3, §8 R4-R6] [TỪ HANDBOOK §6.5, §7.2, §7.5, §7.7]

## must_not (hard prohibitions)
- MUST NOT design a blocking hook on `PostToolUse` / `PostToolUseFailure` / `PostToolBatch`.
  The tool already executed; no rollback possible. Audit/transform only. [TỪ HANDBOOK §7.5]
- MUST NOT mix Format A + Format B in one script. [TỪ HANDBOOK §6.6]
- MUST NOT set `continueOnBlock: true` on events other than `Stop` / `SubagentStop`.
  Silently ignored — validate placement. [TỪ HANDBOOK §7.7]
- MUST NOT write `settings.json` without backup-before-write. [TỪ HANDBOOK §7.3]
- MUST NOT leave `TODO` / `FIXME` / placeholder in handler impl. [TỪ BA §7]

## fail-closed semantics
When the hook script is not found OR times out (>timeout) → the tool call is **BLOCKED** and an ERROR is logged. [TỪ HANDBOOK §6.5, NFR-02]
- invalid JSON from hook → fallback to exit-code semantics + WARNING log
- non-zero exit ≠ 2 → hook error (allow + log)
- chain deny → first deny wins; subsequent hooks skipped

## Validation gates (Pillar 3)
1. PostToolUse block design → reject.
2. Format A/B mix → reject.
3. continueOnBlock on wrong event → reject.
4. Fail-closed when script-not-found/timeout → enforce.
5. Shadowing at higher priority → warn + confirm target.
6. No placeholder/TODO in handler impl → enforce.

Enforced by `loop/design-checklist.md` + `scripts/design_hook.py`.
