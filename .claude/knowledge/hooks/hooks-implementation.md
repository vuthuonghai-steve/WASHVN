---
name: hooks-implementation
version: 0.1.0
last_updated: 2026-07-10
status: canonical
target_consumer: subagent-forge
suite: WASHVN
description: "Hook implementation guide — dual-format blocking protocol, hook types with examples, error handling policy"
tags: [hooks, implementation, blocking, examples, errors]
---

<instructions priority="informational">
This is an IMPLEMENTATION spoke file loaded on-demand. Read it when you need to: code hook handler scripts (bash), configure prompt/agent hooks, understand dual-format blocking, or debug hook failures. For lifecycle, core events, and quick reference, see the hub file: `hooks-and-events.md`.
</instructions>

> **Hub:** [hooks-and-events.md](hooks-and-events.md) — lifecycle, core events, compact quick reference
> **Reference:** [hooks-reference.md](hooks-reference.md) — complete event table, matcher syntax, schema, if-condition, placeholder

---

## 1. Dual-Format Blocking Protocol

Every `PreToolUse` hook script MUST implement one of two blocking formats. The runtime checks exit code + stdout.

### 1.1 Permission Decision Table

| Script Behavior | Runtime Interpretation |
|----------------|----------------------|
| `exit 0` + no `permissionDecision` on stdout | No decision — **allow** |
| `exit 0` + stdout `{"permissionDecision": "deny"}` | **Block** (Format A) |
| `exit 2` (stderr shown to user) | **Block** (Format B) |
| Any other non-zero exit | **Block**, logged as hook error |

> There is NO permanent grant — every `PreToolUse` is independently evaluated.

### 1.2 Format A — Stdout JSON Blocking

Script writes JSON to stdout with `permissionDecision` field. May include extra fields.

```bash
#!/bin/bash
# Format A example: block rm -rf / and chmod 777
set -euo pipefail

INPUT=$(cat)
COMMAND=$(echo "$INPUT" | jq -r '.params.command // ""')

if echo "$COMMAND" | grep -qE 'rm\s+-rf\s+/|chmod\s+777'; then
  cat <<'EOF'
{"permissionDecision": "deny", "reason": "Destructive command blocked by security hook"}
EOF
  exit 0
fi

exit 0
```

### 1.3 Format B — Exit Code 2 Blocking

Script exits with code 2 and writes human-readable explanation to stderr. Simpler, no JSON parsing needed.

```bash
#!/bin/bash
# Format B example: block network write operations
set -euo pipefail

INPUT=$(cat)
COMMAND=$(echo "$INPUT" | jq -r '.params.command // ""')

if echo "$COMMAND" | grep -qE 'curl\s+-X\s+(POST|PUT|DELETE)|wget\s+--post'; then
  echo "Hook blocked: network write operations require explicit approval" >&2
  exit 2
fi

exit 0
```

### 1.4 Choosing Between Formats

| Use Format A when... | Use Format B when... |
|---------------------|---------------------|
| Multiple hooks chain together | Simplicity preferred |
| Audit trail needs machine-parsable reasons | Human-readable error sufficient |
| Caller needs to distinguish deny reason | Standalone gate, no downstream consumers |

**Rules:**
- A single script MUST NOT mix both formats
- If stdout contains valid JSON with `permissionDecision`, Format A takes precedence
- If exit code is 2 and Format A was not detected, Format B is assumed

---

## 2. Hook Types

### 2.1 Command Hooks

Intercept shell command execution. Matcher targets `bash`, `execute`, `shell`, or custom regex.

```yaml
matcher: "bash"
event: "PreToolUse"
handler: "scripts/hooks/pre-bash.sh"
purpose: "Validate and gate all shell commands"
```

### 2.2 HTTP Hooks

Intercept HTTP requests (tool calls with URL parameters).

```yaml
matcher: "http|fetch|webfetch"
event: "PreToolUse"
handler: "scripts/hooks/pre-http.sh"
purpose: "Block outbound requests to unauthorized domains"
```

### 2.3 MCP Tool Hooks

Intercept MCP tool invocations. Matcher targets MCP tool name as reported by the MCP server.

```yaml
matcher: "codegraph_explore|codegraph_node"
event: "PostToolUse"
handler: "scripts/hooks/log-codegraph.sh"
purpose: "Audit all CodeGraph lookups"
```

### 2.4 Prompt and Agent Hooks

Unlike command hooks (local shell scripts), **prompt-based** and **agent-based** hooks execute within the LLM framework for semantic evaluation.

#### 2.4.1 Prompt-Based Hooks (`type: "prompt"`)

Sends an instruction to an LLM (typically Haiku, optionally Sonnet) to evaluate event parameters in a single-turn request.

**Settings config:**
```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Evaluate if the workspace documentation is structurally complete. Event context: $ARGUMENTS. Return JSON in schema: {\"ok\": boolean, \"reason\": string}",
            "model": "claude-3-5-haiku",
            "timeout": 45,
            "continueOnBlock": true,
            "description": "Verify MD layout and YAML frontmatter prior to session end"
          }
        ]
      }
    ]
  }
}
```

**Required output schema:**
```json
{ "ok": true, "reason": "Clear explanation (mandatory if ok is false)" }
```

**Auto-repair loop** (`continueOnBlock: true`):  
When `ok: false` is returned, the `reason` is fed back to the agent as a new turn. The agent must correct the issues and retry. Does not crash the session.

#### 2.4.2 Agent-Based Hooks (`type: "agent"`)

Spins up a background subagent (up to 50 turns) with file system tools (`Read`, `Grep`, `Glob`) to investigate before deciding.

**Settings config:**
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write",
        "hooks": [
          {
            "type": "agent",
            "prompt": "Check if the proposed file write violates workspace architectural guidelines. Inspect the codebase first to verify pattern consistency. Event context: $ARGUMENTS",
            "timeout": 120,
            "description": "Multi-turn semantic audit of code writing"
          }
        ]
      }
    ]
  }
}
```

**Required output:** Same as prompt hooks — `{ "ok": boolean, "reason": string }`.  
> ⚠ Agent hooks are **experimental**. Use for non-blocking or low-frequency hooks only (high latency).

---

## 3. Error Handling & Hook Failure Mode

```yaml
hook_error_policy:
  on_script_not_found:
    behavior: "fail closed — block the tool call"
    log: "ERROR hook script not found at path"
  on_timeout:
    threshold: "30 seconds per handler invocation"
    behavior: "fail closed — block the tool call"
    log: "ERROR hook timed out after 30s"
  on_parse_error:
    scenario: "Format A script produces invalid JSON"
    behavior: "fall back to Format B exit code evaluation"
    log: "WARNING malformed JSON from hook, falling back to exit code"
  on_non_zero_not_2:
    behavior: "fail open — allow the tool call, log the error"
    log: "ERROR hook exited with unexpected code {n}"
  on_chain_break:
    behavior: "first denied decision wins; subsequent hooks skipped"
    log: "INFO hook chain interrupted by deny at {hook_name}"
```

---

## 4. Cross-References

- [Hub — lifecycle, core events, quick reference](hooks-and-events.md)
- [Reference — event table, matcher, schema, if-condition, placeholder](hooks-reference.md)
- [Agent Configuration Standards](../agents/configuration.md)
- [Agent Capability Controls](../agents/capability_controls.md)
- [Agent Hook Protocol](../agents/agent_hooks.md)
