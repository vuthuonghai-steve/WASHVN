---
name: hooks-reference
version: 0.1.0
last_updated: 2026-07-10
status: canonical
target_consumer: subagent-forge
suite: WASHVN
description: "Hook reference — complete event table, matcher syntax, configuration schema, if-condition, placeholder substitution"
tags: [hooks, events, reference, schema, matcher]
---

<instructions priority="informational">
This is a REFERENCE spoke file loaded on-demand. Read it when you need: the full 27-event table, matcher syntax details, configuration schema, if-condition expressions, or placeholder substitution rules. For lifecycle, core events, and quick reference, see the hub file: `hooks-and-events.md`.
</instructions>

> **Hub:** [hooks-and-events.md](hooks-and-events.md) — lifecycle, core events, compact quick reference

---

## 1. Complete Event Reference

Every event in the system with its firing context, matcher support, and input schema.

| Event | Phase | Matcher | Input |
|-------|-------|---------|-------|
| `SessionStart` | Session start | No | `{ sessionId: string, projectDir: string }` |
| `Setup` | Session start | No | Configuration object |
| `UserPromptSubmit` | Per-turn | Yes (prompt pattern) | User message text |
| `UserPromptExpansion` | Per-turn | Yes (expansion tag) | Expanded context |
| `PreToolUse` | Tool lifecycle | Yes | `{ tool: string, params: object }` |
| `PermissionRequest` | Tool lifecycle | No | Permission descriptor |
| `PermissionDenied` | Tool lifecycle | No | Denial reason |
| `PostToolUse` | Tool lifecycle | Yes | `{ tool, params, result: object }` |
| `PostToolUseFailure` | Tool lifecycle | Yes | `{ tool, params, error: object }` |
| `PostToolBatch` | Tool lifecycle | No | Batch result array |
| `Notification` | Any | Yes | Notification payload |
| `MessageDisplay` | Per-turn | Yes | Rendered message |
| `SubagentStart` | Orchestration | Yes | Subagent config |
| `SubagentStop` | Orchestration | Yes | Subagent result |
| `TaskCreated` | Orchestration | Yes | Task descriptor |
| `TaskCompleted` | Orchestration | Yes | Task result |
| `TeammateIdle` | Orchestration | Yes | `{ teammateId, duration }` |
| `InstructionsLoaded` | Session start | No | Instructions hash |
| `ConfigChange` | Runtime | Yes | Diff of config |
| `CwdChanged` | Runtime | Yes | New working directory |
| `FileChanged` | Runtime | Yes | File path + event type |
| `WorktreeCreate` | Runtime | Yes | Worktree path |
| `WorktreeRemove` | Runtime | Yes | Worktree path |
| `Elicitation` | Per-turn | Yes | Clarification question |
| `ElicitationResult` | Per-turn | Yes | User response |
| `PreCompact` | Session end | No | Current memory snapshot |
| `PostCompact` | Session end | No | Compact result |
| `Stop` | Session end | No | `{ reason: string, sessionId: string }` |
| `StopFailure` | Session end | No | Error details |
| `SessionEnd` | Session end | No | Session summary |

---

## 2. Matcher Syntax (Detailed)

Matchers determine which tool calls or events trigger a hook. The matcher string is evaluated using three strategies in sequence.

### 2.1 Exact Matching

If the matcher consists solely of Latin letters, digits, hyphens, spaces, commas, or pipe characters, it is evaluated as exact/multi-exact match.

```
Allowed chars:   [a-zA-Z0-9\- ,|]
Evaluation:      split by comma, whitespace-trim each token, exact match
Examples:
  "bash"                  → matches only bash
  "Read, Write, Edit"     → matches any of the three
  "bash, Write"           → matches bash or Write
```

### 2.2 OR Patterns (Pipe)

When matcher contains `|` and passes the exact-match character filter, each pipe-delimited segment is an alternative:

```
PreToolUse|PostToolUse|Stop
→ matches any of: PreToolUse, PostToolUse, Stop
```

Whitespace around pipes is stripped.

### 2.3 Regex Patterns

If the matcher contains any character outside the exact-match set (`.`, `*`, `+`, `?`, `^`, `$`, `[`, `]`, `(`, `)`, `{`, `}`, `\`), it is compiled as a case-insensitive JavaScript-compatible regex.

```
Examples:
  "^git"               → any tool starting with "git"
  "\.(env|secret)$"    → tools acting on .env or .secret files
  "(bash|zsh|sh)$"     → any shell tool
```

---

## 3. Hook Configuration Schema

### 3.1 Handler Fields (full reference)

```yaml
handler_schema:
  type: object
  required:
    - event
  optional:
    - type           # enum: [command, prompt, agent]
    - script         # path to handler script
    - prompt         # LLM instruction; supports $ARGUMENTS
    - model          # LLM model (e.g. claude-3-5-haiku)
    - timeout        # seconds (30 default command/prompt, 60 agent)
    - continueOnBlock  # boolean; auto-repair on block
    - if             # condition expression
    - description    # human-readable purpose
    - matcher        # inherits from parent if omitted
```

### 3.2 Settings File Structure (full)

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "bash",
        "hooks": [
          {
            "type": "command",
            "command": "scripts/hooks/pre-bash.sh",
            "description": "Block destructive bash commands"
          }
        ]
      },
      {
        "matcher": "Read|Write|Edit",
        "hooks": [
          {
            "type": "command",
            "if": "tool.params.filePath =~ \\.env$",
            "command": "scripts/hooks/block-env-files.sh",
            "description": "Block access to environment files"
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "bash",
        "hooks": [
          {
            "type": "command",
            "command": "scripts/hooks/log-bash.sh",
            "description": "Log all bash commands to audit trail"
          }
        ]
      }
    ]
  }
}
```

---

## 4. If-Condition Filtering

Every handler MAY include an `if` field. If the condition evaluates to false, the handler is skipped without error.

### 4.1 Syntax

| Operator | Meaning | Example |
|----------|---------|---------|
| `==` | Equality | `tool.name == "bash"` |
| `!=` | Inequality | `tool.name != "Read"` |
| `=~` | Regex match (RHS is regex literal) | `tool.params.filePath =~ \.env$` |
| `in` | Membership (RHS comma-separated) | `tool.name in "Read, Write, Edit, Glob"` |

**Available context variables:** `tool.name`, `tool.params.*`, `event.type`, `session.projectDir`

### 4.2 Examples

| Condition | Purpose |
|-----------|---------|
| `tool.params.filePath =~ \.env$` | Only trigger for .env files |
| `tool.name == "bash"` | Only trigger for bash tool |
| `tool.name in "Read, Write, Edit, Glob"` | Gate all file system tools |
| `session.projectDir =~ /washvn/i` | Only run in WASHVN workspace |

---

## 5. Placeholder Path Substitution

Handler script paths and condition expressions support placeholder substitution. Runtime resolves before invoking the handler.

### 5.1 Supported Placeholders

| Placeholder | Resolution | Example |
|-------------|------------|---------|
| `$CLAUDE_PROJECT_DIR` | Absolute path to project root | `/home/user/projects/my-app` |
| `$CLAUDE_GLOBAL_DIR` | Absolute path to Claude config root | `/home/user/.claude` |
| `$CLAUDE_SESSION_ID` | Current session unique ID | `ses_abc123def` |
| `$HOME` | User home directory | `/home/user` |
| `$TMPDIR` | System temp directory | `/tmp` |

### 5.2 Substitution Rules

- Placeholders resolve **before** path normalization
- Relative paths in handler scripts resolve against `$CLAUDE_PROJECT_DIR`
- If a placeholder references a non-existent variable → **hook fails closed (blocked)**
- Substitution supports both script paths and if-condition values
- Literal dollar signs must be escaped as `$$`

### 5.3 Examples

```yaml
# Relative → resolved to project root
raw: "scripts/hooks/pre-bash.sh"
resolved: "$CLAUDE_PROJECT_DIR/scripts/hooks/pre-bash.sh"
effective: "/home/stveve/Documents/workspace/.../scripts/hooks/pre-bash.sh"

# Global script
raw: "$CLAUDE_GLOBAL_DIR/hooks/global-audit.sh"
resolved: "/home/stveve/.claude/hooks/global-audit.sh"

# Condition with placeholder
if: 'session.projectDir == "$CLAUDE_PROJECT_DIR"'
purpose: "Always true — scope to this project only"
```

---

> **See also:** [hooks-and-events.md](hooks-and-events.md) — lifecycle, core events, compact quick reference
