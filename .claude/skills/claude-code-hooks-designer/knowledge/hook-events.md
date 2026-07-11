# 30 Canonical Hook Events
# [TỪ DESIGN §2.1, §3 knowledge/hook-events.md] [TỪ HANDBOOK §2]

Claude Code hooks fire at lifecycle points inside the LLM agent's tool-use/session flow — NOT git hooks, NOT webhooks, NOT framework lifecycle hooks.

## Blocking constraint (critical)
Only **`PreToolUse`** can block (deny) a tool call. Every other event is audit/transform/observe only.
[TỪ HANDBOOK §6.1, §7.2]

## Event table

| Event | Phase | Matcher? | Block? |
|-------|-------|----------|--------|
| SessionStart | session-start | No | No |
| Setup | session-start | No | No |
| UserPromptSubmit | per-turn | Yes | No |
| UserPromptExpansion | per-turn | Yes | No |
| PreToolUse | tool-lifecycle | Yes | **YES** |
| PermissionRequest | tool-lifecycle | No | No |
| PermissionDenied | tool-lifecycle | No | No |
| PostToolUse | tool-lifecycle | Yes | No |
| PostToolUseFailure | tool-lifecycle | Yes | No |
| PostToolBatch | tool-lifecycle | No | No |
| Notification | any | Yes | No |
| MessageDisplay | per-turn | Yes | No |
| SubagentStart | orchestration | Yes | No |
| SubagentStop | orchestration | Yes | No |
| TaskCreated | orchestration | Yes | No |
| TaskCompleted | orchestration | Yes | No |
| TeammateIdle | orchestration | Yes | No |
| InstructionsLoaded | session-start | No | No |
| ConfigChange | runtime | Yes | No |
| CwdChanged | runtime | Yes | No |
| FileChanged | runtime | Yes | No |
| WorktreeCreate | runtime | Yes | No |
| WorktreeRemove | runtime | Yes | No |
| Elicitation | per-turn | Yes | No |
| ElicitationResult | per-turn | Yes | No |
| PreCompact | session-end | No | No |
| PostCompact | session-end | No | No |
| Stop | session-end | No | No |
| StopFailure | session-end | No | No |
| SessionEnd | session-end | No | No |

Matcher-supporting: 19. Non-supporting: 11.
[TỪ HANDBOOK §2 G1 — design/quality-matrix state 20/30; grounded to canonical table = 19/11. See build-log R-extra.]

## Selection guidance
- Want to BLOCK a tool call → `PreToolUse` (only choice). [TỪ HANDBOOK §7.2]
- Want to audit/transform a result → `PostToolUse`. Cannot undo. [TỪ HANDBOOK §7.5]
- Want self-healing auto-repair with `continueOnBlock` → only `Stop` / `SubagentStop`. [TỪ HANDBOOK §7.7]
