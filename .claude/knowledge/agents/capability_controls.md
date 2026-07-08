---
name: capability-controls
version: 0.0.1
last_updated: 2026-07-07
status: canonical
target_consumer: subagent-forge
suite: WASHVN
description: "Tool/MCP/skills scoping, permission mode governance, memory scoping rules, and risk matrix for Claude Code subagent capability controls"
tags: [subagent, capability, permissions, security, scoping]
---

# Capability Scoping and Controls

This document defines the capability scoping patterns for Claude Code subagents
within the WASHVN skill suite. Every subagent declaration must apply explicit
tool restrictions, permission-mode governance, and MCP server boundaries to
prevent capability over-scoping and context waste.

---

## Allowlist and Denylist Mechanics

Tool access follows a two-stage filter pipeline: denylist evaluation occurs first,
then allowlist evaluation. A tool is available only if it passes both stages.

### Disallowed Tools (Denylist)

The `disallowedTools` field removes specific tools from the agent context before
any allowlist resolution. This is the primary mechanism for blocking dangerous
or irrelevant capabilities.

```yaml
agent:
  disallowedTools:
    - Bash
    - Write
```

Disallowed tools are evaluated at context-build time. The agent never sees them
in its available tool list.

### Tool Allowlist

The `tools` field declares the explicit set of tools the agent is permitted to
use. When present, it acts as a strict allowlist: only tools named in the array
are available (after denylist removal). Omitting the field inherits the caller's
full tool set.

```yaml
agent:
  tools:
    - Read
    - Grep
    - Glob
```

### Interaction Rules

- `disallowedTools` is applied before `tools`. If a tool appears in both lists,
  it is denied.
- An empty `tools: []` denies all tools. An empty `disallowedTools: []` denies
  none.
- The union of `tools` plus any inherited tools from the parent context forms
  the effective set after denylist filtering.

---

## Permission Modes

Every subagent and tool call operates under a permission mode. The mode
determines whether the agent must prompt the user before executing an action.

| Mode | Behavior | Use Case |
|---|---|---|
| `default` | Prompt on every tool invocation. Slowest but safest. | Unaudited agents, exploration tasks. |
| `acceptEdits` | Automatically approve file writes and edits; prompt on Bash and network. | Code generation, refactoring pipelines. |
| `auto` | Approve all tools without prompting. Fastest mode. | Fully trusted, read-only agents. |
| `dontAsk` | Suppress all permission prompts. Equivalent to auto for the subagent scope. | Headless or background agents. |
| `bypassPermissions` | Bypass all permission checks at the process level. **Not allowed in WASHVN.** | Outside agents, local dev shells only. |
| `plan` | Agent describes intent without executing. Used for audit trails before action. | Review workflows, design phases. |

### WASHVN Constraint

The `bypassPermissions` mode is forbidden in all WASHVN subagent declarations.
Any agent that requires elevated permissions must use `acceptEdits` instead and
be paired with a lightweight review gate in the calling hook.

Reference configuration:

```yaml
agent:
  permissionMode: acceptEdits
  disallowedTools:
    - Bash
```

---

## MCP Server Scoping

Claude Code loads Model Context Protocol (MCP) servers from
`file:///home/stveve/.config/claude/mcp.json` and project-local
`.claude/mcp.json` (or `.mcp.json`). Capability controls apply per-server and per-tool.

### Blocking Individual Servers

Use the `mcp__<server_name>` pattern to block all tools from a specific MCP
server:

```yaml
agent:
  disallowedTools:
    - mcp__filesystem    # blocks all tools from the filesystem MCP server
    - mcp__playwright    # blocks all browser automation
```

### Blocking All MCP

Use the wildcard pattern `mcp__*` to block every MCP server in a single
declaration:

```yaml
agent:
  disallowedTools:
    - mcp__*
```

### Inline MCP Definitions

For specialized agents, define MCP servers inline within the agent declaration.
Reference servers are resolved first, then inline entries are merged.

```yaml
agent:
  mcpServers:
    - name: custom-fs
      transport: stdio
      command: npx
      args:
        - -y
        - @modelcontextprotocol/server-filesystem
```

### Plugin Restrictions

MCP servers loaded via Claude Code plugins inherit the same scoping rules.
Block a plugin-provided server the same way: `mcp__plugin-server-name`.

---

## Skills Preload Mechanics

Skills provide context injection: instructions, policies, and knowledge scoped
to a task. The preload system governs which skills load and how their content
is injected.

### Preload Limit

A maximum of **3 skills** may be preloaded into a single subagent context.
Exceeding this limit degrades prompt quality and consumes context budget.

```yaml
agent:
  skills:
    - skill-architect
    - skill-planner
```

### Content Injection

Each preloaded skill injects its full `SKILL.md` content into the system prompt.
Skills with large knowledge directories must be referenced on-demand rather than
preloaded.

### Disable Model Invocation Handler

When `disable-model-invocation: true` is set on a skill, the model-invocation
handler in `CLAUDE.md` is suppressed for the duration of that skill's
activation. This prevents recursive agent spawning when the skill is used inside
a subagent.

```yaml
agent:
  skills:
    - name: skill-architect
      disable-model-invocation: true
```

---

## Persistent Memory Scoping

Claude Code supports persistent memory files that survive across sessions.
Memory is loaded at context-build time and scoped by directory.

### Memory Scopes

| Scope | Path | Lifetime |
|---|---|---|
| User | `file:///$CLAUDE_GLOBAL_DIR/agent-memory/` | Cross-project, permanent |
| Project | `file:///$CLAUDE_PROJECT_DIR/.claude/agent-memory/` | Project-specific, permanent |
| Local | `file:///$CLAUDE_PROJECT_DIR/.claude/agent-memory-local/` | Project-specific, ephemeral |

### MEMORY.md Loading Rules

When a memory file named `MEMORY.md` exists in any scope, it is loaded into the
agent context subject to these limits:

- First **200 lines** of content are injected.
- If the 200-line threshold is reached before 25 KB, injection stops at 200
  lines.
- If 25 KB is reached before 200 lines, injection stops at the 25 KB boundary.
- Remaining content is available on demand via Read.

### Merge Strategy

Memory is loaded in order: user, then project, then local. Later scopes override
earlier scopes on key conflict.

---

## Agent Subagent Spawning Control

Use the `Agent(agent_type)` syntax within a `tools` array to restrict which
subagent types a parent agent may spawn.

### Syntax

```yaml
agent:
  tools:
    - Agent(worker)
    - Agent(researcher)
    - Read
    - Bash
```

The agent above may spawn only subagents of type `worker` or `researcher`,
plus use `Read` and `Bash` directly.

### Allowlisted Agent Types

| Agent Type | Purpose |
|---|---|
| `worker` | Task execution, code generation |
| `researcher` | Exploration, information gathering |
| `architect` | Design and planning |
| `reviewer` | Code review and quality gates |
| `tester` | Sandbox testing, verification |

Omitting `Agent(...)` from the tools list blocks all subagent spawning for that
agent.

---

## Risk Matrix: Capability Anti-Patterns

The following table documents known anti-patterns and their mitigations.

| Anti-Pattern | Risk | Severity | Mitigation |
|---|---|---|---|
| Bash + bypassPermissions | Unrestricted shell execution with no prompts. | Critical | Block bypassPermissions in WASHVN. Use acceptEdits instead. |
| Write + acceptEdits without hook | Silent file overwrites with no review gate. | High | Every acceptEdits agent must have a calling hook that invokes review-work. |
| Too many tools (over 8) | Context window fragmentation, poor instruction adherence. | Medium | Hard limit of 8 tools per agent declaration. |
| Wildcard MCP allow (mcp__* in allowlist) | All MCP servers become available, including dangerous filesystem or browser tools. | High | Explicitly enumerate allowed MCP servers. Never use wildcard in allowlist. |
| Preloading over 3 skills | Prompt degradation, token budget exceeded. | Medium | Enforce max 3 skills. Offload reference material to knowledge/ directory. |
| Nested bypassPermissions agents | Cascading permission escalation through subagent chains. | Critical | Reject any agent declaration where any ancestor used bypassPermissions. |
| Agent(agent_type) omitted with no tool restrict | Subagent may spawn unlimited children, creating resource loops. | Medium | Always constrain Agent(...) types. Use empty tools for leaf agents. |
| Inline MCP with no scope limit | Agent gains file or network access not intended by the workflow. | High | Pair inline MCP with corresponding disallowedTools entries. |

---

## Tool Restriction Patterns

The following YAML examples codify the restriction patterns described above.

### Read-Only Researcher

```yaml
researcher:
  permissionMode: auto
  tools:
    - Read
    - Grep
    - Glob
    - Agent(researcher)
  disallowedTools:
    - Bash
    - Write
    - Edit
    - mcp__*
```

### Code Generator with Review Gate

```yaml
codegen:
  permissionMode: acceptEdits
  tools:
    - Read
    - Write
    - Edit
    - Glob
    - Agent(worker)
  disallowedTools:
    - Bash
    - mcp__playwright
  skills:
    - skill-builder
```

### Sandbox Tester

```yaml
tester:
  permissionMode: acceptEdits
  tools:
    - Read
    - Bash
    - Glob
  disallowedTools:
    - Write
    - Edit
    - mcp__*
```

### Planner (No Execution)

```yaml
planner:
  permissionMode: plan
  tools:
    - Read
    - Grep
    - Glob
  disallowedTools:
    - Write
    - Edit
    - Bash
    - mcp__*
```

---

## Cross-References

- [Agent configuration standards](file:///home/stveve/Documents/workspace/build-workflow/WASHVN/.claude/knowledge/agents/configuration.md)
- [Hook and event contracts](file:///home/stveve/Documents/workspace/build-workflow/WASHVN/.claude/knowledge/agents/hooks_and_events.md)
- [Workflow patterns for agent pipelines](file:///home/stveve/Documents/workspace/build-workflow/WASHVN/.claude/knowledge/agents/workflow_patterns.md)
- [XML tags standards for skill format](file:///home/stveve/Documents/workspace/build-workflow/WASHVN/.claude/knowledge/agents/xml_tags_standards.yaml)
- [Master Skill Suite architecture](file:///home/stveve/Documents/workspace/build-workflow/WASHVN/architecture.md)
- [Documentation format standards](file:///home/stveve/Documents/workspace/build-workflow/WASHVN/standards.md)
