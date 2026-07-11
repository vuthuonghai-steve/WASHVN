# Handler Types, Dual-Format Blocking, Timeouts
# [TỪ DESIGN §2.1, §3 knowledge/handler-types.md] [TỪ HANDBOOK §6.3, §6.6]

## Three handler types
| Type | Executes | Default timeout | Notes |
|------|----------|-----------------|-------|
| `command` | local shell script | 30s | default when `script` provided |
| `prompt` | LLM (typically Haiku) single-turn eval | 30s | returns `{ok, reason}` JSON |
| `agent` | background subagent (up to 50 turns) | 60s | experimental, high latency [TỪ HANDBOOK §2] |

## Handler fields
`event` (required). Optional: `type`, `script`/`prompt`, `model`, `timeout`, `continueOnBlock`, `if`, `description`, `matcher` (inherits parent).

## Dual-Format Blocking (MUST NOT MIX)
Two protocols to deny a tool call. Never combine in one script. [TỪ HANDBOOK §6.6]
- **Format A**: exit 0 + JSON deny on stdout.
  `{"permissionDecision": "deny", "reason": "..."}`
  Takes precedence if detected. Enables machine-readable audit chains.
- **Format B**: exit code 2 + message on stderr. Simpler, more robust.
- Any other non-zero (≠2) exit → hook ERROR (allow + log). [TỪ HANDBOOK §6.5]

Recommendation: Format B for simple gates; Format A for audit chains.

## continueOnBlock
Boolean. Auto-repair loop: on `ok:false`, reason fed back as new turn.
ONLY valid on `Stop` / `SubagentStop`. Silently ignored elsewhere. [TỪ HANDBOOK §7.7]
