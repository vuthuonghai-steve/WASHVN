---
name: workflow-patterns
version: 0.0.1
last_updated: 2026-07-07
status: canonical
target_consumer: subagent-forge
suite: WASHVN
description: Complete reference for Claude Code subagent invocation and workflow patterns including foreground, background, resume, compaction, cascading, and cross-runtime patterns.
tags: [subagent, invocation, workflow, task, delegation, runtime]
when_to_use: "When designing or implementing subagent invocation patterns — choose between foreground, background, resume, compaction, cascading, and cross-runtime patterns based on subtask characteristics"
---

# Agent Workflow Patterns

This document catalogs the six invocation and workflow patterns available when
delegating work to Claude Code subagents. Use it during skill design and
implementation to choose the correct pattern for each subtask.

Related documents:
- [forks.md](file:///home/stveve/Documents/workspace/build-workflow/WASHVN/.claude/knowledge/agents/forks.md)
- [configuration.md](file:///home/stveve/Documents/workspace/build-workflow/WASHVN/.claude/knowledge/agents/configuration.md)
- [examples.md](file:///home/stveve/Documents/workspace/build-workflow/WASHVN/.claude/knowledge/agents/examples.md)
- [capability_controls.md](file:///home/stveve/Documents/workspace/build-workflow/WASHVN/.claude/knowledge/agents/capability_controls.md)
- [architecture.md](file:///home/stveve/Documents/workspace/build-workflow/WASHVN/architecture.md)

---

## 1. Foreground Invocation (Sync)

The parent session blocks and waits for the subagent to complete. Use when the
parent cannot proceed without the subagent result and the subagent turn budget
is small (2-3 turns).

### Task Call Syntax

```python
task(subagent_type="explore", run_in_background=false)
```

### Behavior

- Parent stalls until subagent returns.
- Subagent shares the parent token window (no separation).
- Errors propagate directly to the parent caller.
- Maximum practical depth: 1 level. Nesting foreground calls exhausts the
  context window quickly.

### When to Use

- Quick lookups: type definitions, import paths, single-file analysis.
- Validation steps: check schema, verify a signature.
- Conditional branching: if subagent result determines which branch the parent
  takes.

### When Not to Use

- Long-running research (use background).
- Multi-file refactors (use cascading or background).

---

## 2. Background Invocation (Async)

The parent continues executing while the subagent runs independently. Use for
any subtask that exceeds 2-3 turns or runs I/O-heavy exploration.

### Task Call Syntax

```python
task(subagent_type="explore", run_in_background=true)
```

### Behavior

- Returns immediately with a `task_id` (e.g. `bg_abc123`).
- Parent polls completion via `background_output(task_id="bg_abc123")`.
- Subagent has its own isolated context window.
- As of Claude Code v2.1.198, subagents run in background by default. Explicit
  `run_in_background=true` is still recommended for clarity.
- Parent can launch multiple background subagents in parallel.

### Retrieving Results

```python
# Block until done
background_output(task_id="bg_abc123", block=true)

# Read final message only (non-blocking)
background_output(task_id="bg_abc123", block=false)
```

### When to Use

- Parallel exploration of multiple areas.
- Long-running compilation or test suites.
- Research that feeds into a synthesis step.

---

## 3. Resume Pattern (Continue via session_id)

Reconnect to an existing subagent session to continue work where it left off.
Useful when a subagent was interrupted, hit a token limit, or needs a follow-up
prompt after returning intermediate results.

### Syntax

```python
task(subagent_type="explore", session_id="ses_abc123", prompt="Continue analyzing the remaining files")
```

### Behavior

- Subagent loads the full prior session context.
- Continues from the exact conversation state.
- No re-reading of earlier context; picks up with the new prompt.
- Token window carries forward; compaction may be needed before resuming a long
  session.

### When to Use

- Interrupted background tasks that need more work.
- Multi-stage analysis where each stage depends on prior reasoning.
- Debugging flows where the subagent identified a lead and needs to pursue it.

---

## 4. Compaction Pattern (Self-Summarize)

When a subagent nears its context window limit (~80% full), it can compact by
summarizing what it has learned and discarding raw conversation history.

### Trigger Mechanisms

- Automatic: triggered by the runtime at ~80% context utilization.
- Manual: the agent or skill code can request compaction explicitly.

### Behavior

- Subagent writes a structured summary of findings (what was learned, what
  remains, open questions).
- Raw turn history is discarded.
- Compaction preserves the summary, the original goal, and any explicit output
  artifacts.
- After compaction the subagent resumes with a fresh token budget plus the
  summary.

### Best Practices

- Design skills to produce compact intermediate artifacts (YAML, structured
  lists) rather than verbose prose.
- Avoid storing raw file contents in subagent context; reference file paths
  instead.
- After compaction, validate that no critical data was lost by comparing the
  summary with checkpointed artifacts.

---

## 5. Cascading Agents (Nested Delegation)

A subagent spawns its own subagent, creating a delegation tree. The WASHVN
maximum depth is 2 (root -> child -> grandchild).

### Depth Limit

```text
Root (level 0)
  └─ Subagent (level 1)
       └─ Subagent (level 2)  <-- max depth
```

### Behavior

- Level-2 subagents run in background relative to their parent.
- Each level has its own isolated context window.
- Depth is enforced by the runtime; attempts to exceed depth 2 are rejected.
- Token cost compounds: a level-2 subagent consumes its own budget plus its
  parent's, so plan for 25k-50k tokens per cascade chain.

### When to Use

- Multi-stage pipelines: Explorer (level 1) spawns a Knowledge Miner (level 2)
  for deep investigation of one finding.
- Research -> validate: subagent researches, its child validates specific
  claims.
- Sandboxed execution: parent plans, child runs untrusted code in isolation.

### Token Cost Warning

Deep cascades consume context rapidly. Prefer launching level-1 subagents in
parallel over nesting to depth 2 when the subtasks are independent.

---

## 6. Cross-Runtime Invocation

Delegate work to a non-Claude-Code runtime such as Codex CLI, Hermes, or
Antigravity. The parent Claude Code session communicates with the foreign
runtime through subprocess calls or MCP bridges.

### Supported Targets

- Codex CLI: via `claude --agent codex` or programmatic subprocess.
- Hermes agent: via MCP tool calls routed through `.hermes/` configuration.
- Antigravity: via `claude --agent antigravity` or `task()` with a
  cross-runtime agent type.

### Syntax

```bash
claude --agent codex "analyze the memory usage in src/core/"
```

```python
task(subagent_type="hermes", run_in_background=true, prompt="Index the new schema")
```

### Behavior

- The foreign runtime gets its own process, context window, and tool set.
- Results are returned as structured output (JSON/YAML) or text.
- Error handling follows the foreign runtime's conventions; the parent must
  parse and validate the response.
- MCP-based bridging provides type-safe invocation when the MCP server is
  configured.

---

## Token Cost Estimation Table

| Pattern | Typical Turns | Estimated Token Consumption |
|---|---|---|
| Foreground Explore | 2-3 turns | ~5k - 10k tokens |
| Background Explore | 3-5 turns | ~10k - 25k tokens |
| Resume (continue session) | 2-4 additional turns | ~8k - 15k tokens (plus carry-over) |
| Compaction | 1 turn (self-summary) | ~1k - 3k tokens for summary |
| Cascading (depth=2) | 5-10 turns total | ~25k - 50k tokens |
| Cross-Runtime (Codex) | 3-6 turns | ~15k - 30k tokens (separate process) |
| Cross-Runtime (Hermes MCP) | 2-4 turns | ~8k - 15k tokens |

---

## Automatic Delegation Mechanics

Subagents can be selected automatically based on the `description` field in
their registration. When a skill or agent definition includes a `description`
field, the runtime matches it against the current task context to suggest or
auto-route delegation.

### Description-Based Routing

1. The parent agent needs a subtask completed (e.g., "check the security of
   this auth flow").
2. The runtime scans registered subagents whose `description` field matches the
   task semantics.
3. A matching subagent is recommended or auto-invoked depending on
   `settings.json` auto-delegation flags.
4. The parent can override, confirm, or reject the suggested routing.

### Configuration

In `settings.json`, the `agent` field and `auto_delegate` flags control whether
routing is automatic or requires confirmation. See
[configuration.md](file:///home/stveve/Documents/workspace/build-workflow/WASHVN/.claude/knowledge/agents/configuration.md)
for full schema.

---

## Explicit Invocation Methods

### Natural Language

Describe the subtask in prose within the parent prompt. The runtime infers the
appropriate subagent or executes inline:

```text
"I need you to explore the data layer and find all repository classes."
```

### @-Mention

Tag a specific registered agent by name to route the request:

```markdown
@"code-reviewer (agent)" look at the auth changes in the latest commit
```

The parenthetical `(agent)` disambiguates from file or symbol names.

### --agent Flag

Launch a specific agent directly from the command line:

```bash
claude --agent code-reviewer
claude --agent architect
claude --agent security-reviewer
```

### settings.json agent Field

Declare a default agent per project in `.claude/settings.json`:

```json
{
  "agent": "architect",
  "permissions": {
    "bypass": true
  }
}
```

This configures the agent that runs when no explicit `--agent` flag is
provided.

---

## Foreground vs Background Behavior Differences

| Aspect | Foreground | Background |
|---|---|---|
| Parent execution | Blocks until subagent returns | Continues immediately |
| Context isolation | Shares parent context | Isolated context window |
| Result retrieval | Direct return value | Poll via background_output |
| Error handling | Exception propagates | Must check task status |
| Parallelism | None (sequential) | Multiple can run concurrently |
| Max recommended depth | 1 level | 2 levels |
| Token budget | Subset of parent budget | Independent budget |

---

## Fork Mode (CLAUDE_CODE_FORK_SUBAGENT)

When the environment variable `CLAUDE_CODE_FORK_SUBAGENT` is set to `true` (or `1`),
subagents are spawned as child OS processes (forked) rather than in-process
threads. This provides stronger isolation at the cost of higher memory per
subagent.

### Behavior

- Each forked subagent is a separate OS process.
- Parent and subagent cannot share in-memory state.
- Communication happens through the background_output mechanism.
- Recommended for cross-runtime and security-sensitive subtasks.

For details see
[forks.md](file:///home/stveve/Documents/workspace/build-workflow/WASHVN/.claude/knowledge/agents/forks.md).

---

## API Error Handling and Subagent Error Recovery

Subagents can fail due to API errors, rate limits, context exhaustion, or
internal tool failures. The following recovery strategies apply per pattern.

### Transient Failures (API Errors, Rate Limits)

- Automatic retry with exponential backoff (3 attempts by default).
- Configurable via `settings.json`:
  ```json
  "subagent_retry": {
    "max_attempts": 3,
    "backoff_ms": 1000,
    "backoff_multiplier": 2
  }
  ```
- Background subagents retry independently; the parent sees only the final
  success or failure.

### Permanent Failures (Invalid Prompt, Missing Agent)

- Error is returned immediately with a descriptive message.
- Parent must handle the error by either correcting the prompt, choosing a
  different agent, or falling back to inline execution.
- No automatic retry for permanent failures.

### Recovery Cascade

1. Detect failure (timeout, error response, empty result).
2. If transient: wait and retry up to `max_attempts`.
3. If permanent or all retries exhausted: escalate to parent with error context.
4. Parent may resume the subagent via `session_id` with a corrective prompt
   (Resume pattern).
5. If resume also fails, the parent executes the subtask inline or reports the
   failure to the user.

### Timeout Handling

- Foreground subagents inherit the parent timeout context.
- Background subagents have an independent timeout, configurable via the
  `timeout` parameter in the `task()` call.
- Default timeout: 120 seconds. Set via
  `task(subagent_type="explore", run_in_background=true, timeout=300000)` (parameter value is in milliseconds, i.e. 300,000 ms = 300 seconds) for
  long-running tasks. Note that this differs from Hook configurations which define timeouts in seconds.

---

## Summary: Pattern Selection Guide

| If your subtask is... | Use pattern |
|---|---|
| A quick lookup (1-2 turns) | Foreground |
| Long-running or parallel work | Background |
| Continuing interrupted work | Resume |
| Running out of context | Compaction |
| Multi-stage with dependent steps | Cascading (depth <= 2) |
| Needs a different runtime | Cross-Runtime |
