---
name: configuration
version: 0.0.1
last_updated: 2026-07-07
status: canonical
target_consumer: subagent-forge
suite: WASHVN
description: "16-field YAML frontmatter schema for Claude Code subagents — field types, validation rules, model resolution order, WASHVN constraints"
tags: [subagent, configuration, schema, frontmatter, validation]
---

# Frontmatter Configuration Reference

> [!IMPORTANT]
> This document defines the full 16-field YAML frontmatter schema for the
> `.claude/agents/<name>.md` files. Every subagent in the WASHVN workspace must
> adhere to this schema. This document is consumed by
> [subagent-forge](file:///home/stveve/Documents/workspace/build-workflow/WASHVN/.claude/agents/subagent-forge.md)
> during the subagent design and evaluation process.

---

## 1. Field Schema (16 Fields)

The table below lists all 16 supported frontmatter fields, along with their data types, requirement levels, default values, validation rules, and descriptions.

### 1.1 Detailed Table

| # | Field | Type | Required | Default | Validation Rules | Description |
| :- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | `name` | `string` | Yes | — | Kebab-case identifier, unique within `.claude/agents/`. Max 64 characters. Only `[a-z0-9-]` allowed. | Unique identifier of the subagent. Example: `code-reviewer`, `db-reader--strict`. |
| 2 | `description` | `string` | Yes | — | Max 500 characters. Must contain trigger phrases to activate proactive use. Description in English, imperative. | Short description of the purpose and when to use the subagent. |
| 3 | `tools` | `list[string]` | No | `[Read]` | Max 8 tools. Each tool must be in the Claude Code tool registry: `Read, Write, Edit, Bash, Glob, Grep, Task, Agent, WebFetch, NotebookEdit, TodoWrite`. Parameterized versions `Agent(type)` and `Task(type)` are supported for subagent spawning control. | List of tools the subagent is allowed to call. |
| 4 | `disallowedTools` | `list[string]` | No | `[]` | List of prohibited tools (deny before allow). Takes precedence over `tools`. Default is empty. Used to limit tools in the system scope. | List of prohibited tools, overriding the allowlist. |
| 5 | `model` | `string` | Yes | `inherit` | Valid values: `sonnet, opus, haiku, fable, inherit`, or full model ID (e.g., `anthropic/claude-3.5-sonnet-20241022`). | Model used by the subagent. See Model Resolution Order section. |
| 6 | `permissionMode` | `string` | Yes | `default` | Valid values: `default, acceptEdits, auto, dontAsk, bypassPermissions, plan`. See Permission Modes. | Authorization mechanism for the subagent. |
| 7 | `maxTurns` | `integer` | No | — | Positive integer. Limits the number of interaction turns before the subagent automatically terminates. No limit if not specified. | Maximum number of interaction turns for the subagent. |
| 8 | `skills` | `list[string]` | No | `[]` | Max 3 skills. Each skill must exist in `skills-registry.json` or be defined inline. Skill name in kebab-case. | List of skills preloaded when the subagent starts. |
| 9 | `mcpServers` | `list[object]` | No | `[]` | Each entry can be an inline definition or a reference to a registered server in the config. Server name must be pre-registered. | List of MCP servers the subagent is allowed to access. |
| 10 | `hooks` | `object` | No | `{}` | Keys are event names (e.g., `PreToolUse`, `Stop`). Each key maps to an array of matcher groups, which contain a `matcher` and a `hooks` array. Inside `hooks` is a list of hook handlers defining type, command, etc. | Hook scripts listening to tool/session lifecycle events. |
| 11 | `memory` | `list[string]` | No | `[]` | Valid values: `user, project, local`. Activates corresponding memory mechanisms. Memory is not standalone; managed via the state ledger. | Activates session memory for the subagent. |
| 12 | `background` | `boolean` | No | `true` | `true`: subagent runs in the background after spawn. `false`: subagent runs in the foreground, blocking the parent session. | Determines if the subagent runs in the background or as a foreground process. |
| 13 | `effort` | `string` | No | — | Valid values: `low, medium, high, xhigh, max`. Affects computing resources and processing time. | Computational effort level for the subagent. |
| 14 | `isolation` | `string` | No | — | Valid value: `worktree`. When set, the subagent runs in a separate worktree, completely isolated from the parent session. | Isolates the working environment of the subagent. |
| 15 | `color` | `string` | No | — | Valid values: `red, blue, green, yellow, purple, orange, pink, cyan`. Sets the display color for the subagent in Claude Code UI (tags, badges, terminal). | Display color to distinguish the subagent in the interface. |
| 16 | `initialPrompt` | `string` | No | — | Markdown text automatically sent to the tool call when starting the subagent with `--agent <name>`. Replaces or complements the default system prompt. | Initial prompt message sent automatically when the subagent is invoked. |
| 17 | `version` | `string` | No | — | SemVer format version string (e.g., `0.0.1`). | Version of the subagent configuration. |
| 18 | `status` | `string` | No | — | E.g., `canonical`, `experiment`, `archived`. | Lifecycle status of the subagent. |
| 19 | `parent` | `string` | No | — | Absolute file path URL. | Link back to the parent agent from which this fork was created. |
| 20 | `fork_rationale` | `string` | No | — | Max 500 characters. | Rationale explaining why this subagent was forked. |
| 21 | `suite` | `string` | No | — | E.g., `WASHVN`. | Workspace or project suite identifier. |

---

## 2. Model Resolution Order

The resolution order for the subagent model is as follows:

1. **Environment variables** — `CLAUDE_MODEL` or `ANTHROPIC_MODEL` env var.
2. **Per-invocation** — `--model` flag when invoking the subagent.
3. **Frontmatter** — `model` field in the subagent frontmatter.
4. **Main conversation model** — Model of the current parent session.

If no model is resolved at any level, the system defaults to `sonnet`.

```yaml
model_resolution_order:
  1: "CLAUDE_MODEL / ANTHROPIC_MODEL env var"
  2: "--model flag per invocation"
  3: "frontmatter.model field"
  4: "parent session conversation model"
  fallback: sonnet
```

---

## 3. Permission Modes

| Value | Meaning | Notes |
| :--- | :--- | :--- |
| `default` | Ask the user before every action (write, bash, etc.) | Safest. Recommended default for WASHVN. |
| `acceptEdits` | Automatically accept Edit tool calls. Must block write path using PreToolUse hook. | Does not apply to Bash or WebFetch. |
| `auto` | Automatically accept decisions within allowed boundaries. | Rarely used in WASHVN. |
| `dontAsk` | Do not ask the user. Subagent decides. | Requires evaluation by the safety-auditor. |
| `bypassPermissions` | Bypass all permission mechanisms. | **PROHIBITED** in WASHVN. Always rejected by safety-auditor. |
| `plan` | Read-only mode. Does not trigger edit tools. | Used for analysis, review, and design. |

> [!WARNING]
> **WASHVN constraint:** `permissionMode: bypassPermissions` is strictly prohibited.
> Any subagent with this permissionMode will be rejected by safety-auditor
> with severity HIGH. See
> [capability_controls.md](file:///home/stveve/Documents/workspace/build-workflow/WASHVN/.claude/knowledge/agents/capability_controls.md)
> for more details.

---

## 4. Subagent Scope Locations

The priority order when the system searches for a subagent:

```yaml
scope_locations:
  1: managed_settings
    description: "Settings managed by Claude Code settings (Claude Code for Desktop, IDE plugin)"
    example: "Claude Code > Settings > Agents"
  2: CLI_flag
    description: "The `--agent` or `--subagent` parameter when invoking Claude Code"
    example: "claude --agent code-reviewer"
  3: project_agents
    description: "Subagent in the local project"
    path: ".claude/agents/<name>.md"
    example: "file:///home/stveve/Documents/workspace/build-workflow/WASHVN/.claude/agents/subagent-forge.md"
  4: user_agents
    description: "Subagent in the user-level config"
    path: "~/.claude/agents/<name>.md"
  5: plugin_registry
    description: "Subagent defined by a plugin"
    path: "plugin registry"
```

Subagents in managed settings have the highest priority. When invoking `--agent <name>`, the system scans in the order above and uses the first definition found.

> [!NOTE]
> WASHVN only uses project-level subagents located at
> [.claude/agents/](file:///home/stveve/Documents/workspace/build-workflow/WASHVN/.claude/agents/).
> User-level and plugin-level subagents are not used in this workspace.

---

## 5. WASHVN Constraints

### 5.1 Special rules for the WASHVN workspace

```yaml
washvn_constraints:
  bypassPermissions:
    status: PROHIBITED
    note: "permissionMode: bypassPermissions is always rejected by safety-auditor"
    severity: HIGH

  max_tools_per_agent:
    limit: 8
    note: "Do not exceed 8 tools in the subagent's tools list"

  max_skills_preload:
    limit: 3
    note: "Do not preload more than 3 skills in the skills field"

  privileged_tools:
    - tool: Bash
      constraint: "Requires justification in <acceptance_criteria> before allowance"
    - tool: WebFetch
      constraint: "Requires justification in <acceptance_criteria> before allowance"
    - tool: NotebookEdit
      constraint: "Requires justification in <acceptance_criteria> before allowance"

  default_tools:
    - Read
    note: "New subagents default to Read only. Adding other tools requires specific justification."

  forbidden_combinations:
    - "[Bash, bypassPermissions]"
      note: "Severe security risk. Bash tool + bypassPermissions = FULL ACCESS."
    - "[WebFetch, bypassPermissions]"
      note: "Potential to download malicious content without controls."
```

### 5.2 Excluded or restricted fields

The WASHVN workspace applies the following restrictions beyond the 16-field schema:

- `dangerouslyDisableSandbox` — Not allowed. Subagent-forge will automatically reject it.
- `extendedThinking` — Not allowed in the subagent context. Only used by the parent session.
- `dedicatedThread` — Does not apply to the WASHVN workspace.
- `disableOutputSandbox` — Not allowed. Similar to dangerouslyDisableSandbox.

---

## 6. Valid Values

### 6.1 Tool names

List of valid tools in the Claude Code tool registry:

[Read, Write, Edit, Bash, Glob, Grep, Task, Agent, WebFetch, NotebookEdit, TodoWrite]

### 6.2 Model aliases

| Alias | Model ID |
| :--- | :--- |
| `sonnet` | `anthropic/claude-5` |
| `opus` | `anthropic/claude-4-8` |
| `haiku` | `anthropic/claude-4-5` |
| `fable` | `anthropic/claude-5` ⚠️ **Workspace-internal alias** — not a public Anthropic model ID. May be rejected by the API if used outside WASHVN. Consider using `sonnet` or `haiku` instead. |
| `inherit` | Inherits from parent session model |
| Full ID | E.g.: `anthropic/claude-4.5` |

### 6.3 Color values

```text
red, blue, green, yellow, purple, orange, pink, cyan
```

---

## 7. Validation

### 7.1 YAML parse validation

Use the following Python script to validate YAML frontmatter:

```python
#!/usr/bin/env python3
"""Validate YAML frontmatter of a subagent agent file."""
import yaml
import sys
from pathlib import Path


def validate_frontmatter(file_path: Path) -> bool:
    """Parse and validate frontmatter YAML, return True if valid."""
    content = file_path.read_text(encoding="utf-8")

    # Extract content between first pair of --- delimiters
    if not content.startswith("---"):
        print(f"FAIL: {file_path.name} — missing opening ---")
        return False

    _, frontmatter, _ = content.split("---", 2)

    try:
        data = yaml.safe_load(frontmatter)
    except yaml.YAMLError as exc:
        print(f"FAIL: {file_path.name} — YAML parse error: {exc}")
        return False

    if not isinstance(data, dict):
        print(f"FAIL: {file_path.name} — frontmatter is not a mapping")
        return False

    print(f"PASS: {file_path.name} — valid YAML ({len(data)} fields)")
    return True


if __name__ == "__main__":
    for path in sys.argv[1:]:
        validate_frontmatter(Path(path))
```

Run validation:

```bash
python3 -c "import yaml; yaml.safe_load(open(sys.argv[1]))" \
  .claude/agents/subagent-forge.md
```

### 7.2 Validation Checklist

- [ ] File starts with `---` and ends the frontmatter with `---`
- [ ] YAML parses without error (`yaml.safe_load` returns a dict)
- [ ] `name` field exists, kebab-case, maximum 64 characters
- [ ] `description` field exists, maximum 500 characters
- [ ] `model` field exists, valid value
- [ ] `tools` field (if present) contains at most 8 tools, each tool is valid
- [ ] `permissionMode` field (if present) has a valid value, not `bypassPermissions`
- [ ] `skills` field (if present) contains at most 3 skills
- [ ] No invalid fields (only the 16 allowed fields and fork lifecycle metadata: version, status, parent, fork_rationale, suite)

### 7.3 Cross-Check: Output Contract ↔ PreToolUse Write Gate Alignment ⚠️

**Rule:** Mọi file path được liệt kê trong `<output_contract>` và `<constraints>.must` PHẢI được phép bởi `PreToolUse` Write gate regex (nếu agent có Write tool).

**Vì sao:** Nếu không, agent sẽ bị chính hook của nó chặn — một class bug đã xảy ra với `ba-pipeline-runner` (`_state_ledger.yaml` bị chặn bởi Write gate vì regex quá hẹp, dù output_contract yêu cầu ghi file đó).

**Cách kiểm tra:**
```yaml
cross_check:
  1: "Liệt kê tất cả file paths từ output_contract (items 1..N)"
  2: "Liệt kê tất cả file paths từ constraints.must"
  3: "Với mỗi path, kiểm tra PreToolUse Write regex: path có được allow không?"
  4: "Nếu bất kỳ path nào bị chặn → agent sẽ FAIL ở runtime → cần sửa regex"
```

**Checklist bổ sung cho agent có Write tool:**
- [ ] Mọi output file trong `<output_contract>` được PreToolUse Write gate cho phép
- [ ] Mọi file trong `<constraints>.must` được Write gate cho phép
- [ ] Write gate regex không quá hẹp (missing paths) cũng không quá rộng (cho phép paths ngoài zone)
- [ ] Nếu có `<constraints>.must_not` về write zone, nó không contradicted với must + output_contract

---

## 8. References

- [subagent-forge.md](file:///home/stveve/Documents/workspace/build-workflow/WASHVN/.claude/agents/subagent-forge.md) — Subagent designer, directly consumes this document
- [capability_controls.md](file:///home/stveve/Documents/workspace/build-workflow/WASHVN/.claude/knowledge/agents/capability_controls.md) — Tool/MCP/Skills scoping
- [examples.md](file:///home/stveve/Documents/workspace/build-workflow/WASHVN/.claude/knowledge/agents/examples.md) — 4 reference patterns
- [forks.md](file:///home/stveve/Documents/workspace/build-workflow/WASHVN/.claude/knowledge/agents/forks.md) — Experimental fork semantics
- [hooks_and_events.md](file:///home/stveve/Documents/workspace/build-workflow/WASHVN/.claude/knowledge/agents/hooks_and_events.md) — Hook protocol specification
- [workflow_patterns.md](file:///home/stveve/Documents/workspace/build-workflow/WASHVN/.claude/knowledge/agents/workflow_patterns.md) — Invocation patterns
- [xml_tags_standards.yaml](file:///home/stveve/Documents/workspace/build-workflow/WASHVN/.claude/knowledge/agents/xml_tags_standards.yaml) — 9-tag XML whitelist
- [standards.md](file:///home/stveve/Documents/workspace/build-workflow/WASHVN/standards.md) — LLM Knowledge Activation Standard (format rules)
