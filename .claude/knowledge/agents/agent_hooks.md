---
name: agent-hooks
version: 0.0.1
last_updated: 2026-07-10
status: canonical
target_consumer: subagent-forge
suite: WASHVN
description: "Hooks configuration and event integration for Claude Code subagents — lifecycle events, prompt/agent hook types, frontmatter declaration, auto-repair mechanism"
tags: [agents, subagent, hooks, lifecycle, orchestration]
---

# Agent Hooks Reference

<instructions priority="high">
This document covers hooks as they relate to agent/subagent configuration in the WASHVN suite. For the full hook protocol, event lifecycle, matcher syntax, and blocking protocol, see the [Hooks & Events Specification](../hooks/hooks_and_events.md). This document focuses on the agent-specific aspects: subagent lifecycle events, frontmatter hooks declaration, and prompt/agent-based hook types.
</instructions>

---

## 1. Agent-Specific Hook Events

The following events in the hook system are specific to agent/subagent orchestration. They fire during subagent lifecycle management.

| Event | Phase | Matcher Support | Input | Description |
|-------|-------|-----------------|-------|-------------|
| `SubagentStart` | Orchestration | Yes (agent type) | `{ agentType, config, sessionId }` | Fires when a subagent is spawned |
| `SubagentStop` | Orchestration | Yes (agent type) | `{ agentType, result, sessionId }` | Fires when a subagent finishes |
| `TaskCreated` | Orchestration | Yes (task type) | `{ taskId, type, params }` | Fires when a task is created via TaskCreate |
| `TaskCompleted` | Orchestration | Yes (task type) | `{ taskId, result }` | Fires when a task is marked completed |
| `TeammateIdle` | Orchestration | Yes (teammate ID) | `{ teammateId, duration }` | Fires when an agent team teammate is about to go idle |

### 1.1 SubagentStart

Fires when Claude spawns a subagent. The matcher filters on the **agent type name** (e.g., `Explore`, `Plan`, `general-purpose`, or custom agent names).

**Use cases:**
- Log subagent spawns for audit trails
- Inject environment variables before the subagent begins
- Validate that the subagent is authorized to run

**Input format:**
```json
{
  "agentType": "code-reviewer",
  "config": {
    "tools": ["Read", "Grep", "Glob"],
    "model": "sonnet"
  },
  "sessionId": "ses_abc123def"
}
```

### 1.2 SubagentStop

Fires when a subagent completes, errors, or is cancelled. Paired with `SubagentStart` for lifecycle tracking.

**Use cases:**
- Collect subagent result summaries
- Trigger post-processing workflows
- Clean up temporary resources created for the subagent

**Input format:**
```json
{
  "agentType": "code-reviewer",
  "result": {
    "status": "success",
    "summary": "Reviewed 3 files, found 2 issues"
  },
  "sessionId": "ses_abc123def"
}
```

### 1.3 TaskCreated / TaskCompleted

Fire when tasks are created and completed within the agentic loop. These are lower-level than SubagentStart/SubagentStop and fire for every discrete task unit.

**Use cases:**
- Track task-level progress across a session
- Measure time spent on individual operations
- Implement task-level resource governance

### 1.4 TeammateIdle

Fires when an [agent team](https://docs.anthropic.com/en/docs/agent-teams) teammate is about to go idle. Enables automatic wake-up or reassignment logic.

---

## 2. Declaring Hooks in Subagent Frontmatter

Subagents can declare hooks directly in their YAML frontmatter using the `hooks` field. These hooks are scoped to that subagent's lifecycle.

### 2.1 Frontmatter Schema

```yaml
---
name: my-agent
description: Agent with integrated hooks
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: "command"
          command: "scripts/hooks/pre-bash.sh"
  SubagentStart:
    - hooks:
        - type: "command"
          command: "scripts/hooks/log-spawn.sh"
---
```

### 2.2 Priority & Placement

Hooks declared in agent/skill frontmatter have the **highest priority** (level 5) in the [hook resolution order](../hooks/hooks_and_events.md#21-hook-locations), superseding global, project, and plugin settings.

> **Note:** The frontmatter hooks field uses the same logical structure as `settings.json` hooks, but expressed in YAML. Each entry maps an event name to an array of matcher groups, each containing a `hooks` array of handler definitions.

### 2.3 Plugin Restriction

Plugin subagents **cannot** declare `hooks` in their frontmatter — these fields are silently ignored when loading from a plugin. If you need hooks in a plugin, copy the agent definition to `.claude/agents/` or `~/.claude/agents/`.

---

## 3. Prompt-Based Hooks (`type: "prompt"`)

Prompt-based hooks send an instruction directly to an LLM for single-turn evaluation. They are a good fit for **semantic validation** at agent lifecycle points.

### 3.1 Configuration in Subagent Frontmatter

```yaml
---
name: doc-validator
description: Validates documentation completeness before session end
hooks:
  Stop:
    - hooks:
        - type: "prompt"
          prompt: "Evaluate if the workspace documentation is structurally complete. Event context: $ARGUMENTS. Return JSON in schema: {\"ok\": boolean, \"reason\": string}"
          model: "claude-3-5-haiku"
          timeout: 45
          continueOnBlock: true
          description: "Verify MD layout and YAML frontmatter prior to session end"
---
```

### 3.2 Output Schema

The LLM MUST return structured JSON:

```json
{
  "ok": true,
  "reason": "Clear explanation of the decision (mandatory if ok is false)"
}
```

### 3.3 Auto-Repair / Self-Healing Loop (`continueOnBlock: true`)

When `continueOnBlock` is `true` and the hook returns `"ok": false`, the runtime does **not** terminate the session. Instead:

1. The `reason` string is fed back into the agent's context as a new turn
2. The agent must correct the issues described in `reason`
3. The agent retries the operation (e.g., completes the session again)

This enables self-healing workflows for:
- Documentation quality gates
- Code style validation at session end
- Configuration consistency checks

> **Important:** `continueOnBlock` is only supported on session termination events: `Stop`, `SubagentStop`. On other events it is ignored.

---

## 4. Agent-Based Hooks (`type: "agent"`)

Agent-based hooks spin up a **background subagent** (up to 50 turns) with filesystem tools (`Read`, `Grep`, `Glob`) to perform multi-step investigation before returning a decision.

### 4.1 Configuration in Subagent Frontmatter

```yaml
---
name: safe-writer
description: Agent that validates writes against architecture guidelines
hooks:
  PreToolUse:
    - matcher: "Write"
      hooks:
        - type: "agent"
          prompt: "Check if the proposed file write violates workspace architectural guidelines. Inspect the codebase first to verify pattern consistency. Event context: $ARGUMENTS"
          timeout: 120
          description: "Multi-turn semantic audit of code writing"
---
```

### 4.2 Output Format

The subagent MUST output structured JSON at the end of its investigation:

```json
{
  "ok": true,
  "reason": "File write conforms to project architecture patterns"
}
```

### 4.3 Constraints & Caveats

| Aspect | Detail |
|--------|--------|
| **Experimental** | Agent-based hooks are marked experimental and may change in future versions |
| **Latency** | High latency — each invocation runs a full subagent session |
| **Recommendation** | Restrict to non-blocking or low-frequency hooks |
| **Tool access** | Subagent inherits filesystem tools (Read, Grep, Glob) automatically |
| **Max turns** | Capped at 50 autonomous turns |

---

## 5. Dual-Format Blocking for Subagents

Every subagent that intercepts tool calls via `PreToolUse` hooks MUST implement the [Dual-Format Blocking Protocol](../hooks/hooks_and_events.md#6-dual-format-blocking-protocol).

The two valid formats are:
- **Format A** — exit 0 with `{"permissionDecision": "deny"}` on stdout
- **Format B** — exit 2 with human-readable message on stderr

Refer to the [full specification](../hooks/hooks_and_events.md#6-dual-format-blocking-protocol) for exact semantics and examples.

---

## 6. Hook Locations & Resolution for Agents

Hooks configured for subagents are resolved from the following locations in ascending priority:

| Priority | Location | Scope |
|----------|----------|-------|
| 1 (lowest) | `~/.claude/settings.json` | Global user defaults |
| 2 | `.claude/settings.json` | Project-wide |
| 3 | `.claude/settings.local.json` | Local overrides |
| 4 | Plugin-declared hooks | Per-plugin |
| 5 (highest) | **Subagent YAML frontmatter** | Per-agent |

When the same event+matcher pair is configured at multiple levels, the highest-priority definition wins (last writer wins by merge).

---

## 7. Cross-References

- [Full Hook Protocol & Event Specification](../hooks/hooks_and_events.md)
- [Agent Configuration Standards](./configuration.md)
- [Agent Capability Controls](./capability_controls.md)
- [Agent Workflow Patterns](./workflow_patterns.md)

<output_contract>
```yaml
document_summary:
  name: agent-hooks
  version: 0.0.1
  status: canonical
  target_consumer: subagent-forge
  sections:
    - agent_specific_events
    - frontmatter_declaration
    - prompt_based_hooks
    - agent_based_hooks
    - dual_format_blocking
    - resolution_order
    - cross_references
```
</output_contract>
