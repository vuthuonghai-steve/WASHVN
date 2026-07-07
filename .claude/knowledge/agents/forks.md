---
name: forks
version: 0.0.1
last_updated: 2026-07-07
status: canonical
target_consumer: subagent-forge
suite: WASHVN
description: "Fork semantics for Claude Code subagents — naming convention (parent--suffix), 4-stage lifecycle (Experiment/Evaluate/Promote/Archive), conflict resolution, anti-abuse rules"
tags: [subagent, fork, experiment, lifecycle, versioning]
---

# Agent Fork Semantics

An agent fork is a variant of a parent agent that diverges in tools,
instructions, or configuration for experimental purposes. Forks let you test
changes to subagent behavior without disrupting stable agents. This document
defines the naming convention, lifecycle stages, conflict resolution rules,
and anti-abuse policies that govern all agent forks in the WASHVN workspace.

## Fork Naming Convention

Every fork MUST follow the `<parent-name>--<fork-suffix>` pattern. The double
hyphen (`--`) is the separator between the parent name and the fork suffix.
This convention ensures that fork files sort adjacent to their parent in
directory listings and that automated tooling can parse the relationship.

Valid examples:
- `code-reviewer--strict-mode`
- `debugger--verbose`
- `explorer--minimal-tools`
- `planner--aggressive-split`
- `architect--full-context`

The fork suffix MUST be kebab-case and SHOULD describe the single dimension of
change from the parent. A suffix like `tweaks` or `modified` is too vague --
prefer `strict-mode`, `verbose`, `no-browser-tools`, or `timeout-300s`.

The parent agent file and all its forks reside in the same directory ([agents/](file:///home/stveve/Documents/workspace/build-workflow/WASHVN/.claude/agents/)).
When a fork is promoted, its file replaces the parent file.

### Environment Variable Behavior

When the environment variable `CLAUDE_CODE_FORK_SUBAGENT` is set to `1`, every
subagent invocation runs in background mode regardless of the `background`
field in the subagent frontmatter. In this mode, the `background` field in
fork definitions has no effect -- all subagents behave as if
`background: true` were set. This is designed for CI pipelines and batch
evaluation runs where synchronous subagent execution would block progress.

## Fork Lifecycle

Every fork progresses through four stages: Experiment, Evaluation, Promote,
and Archive. A fork MUST NOT skip a stage. A fork MUST NOT remain in the
Experiment stage for longer than one development cycle (seven days) without
explicit renewal.

### Stage 1: Experiment

The fork runs in parallel with its parent. During this stage, the fork is a
copy of the parent with exactly one dimension of change applied. The fork
SHOULD be tested in a subset of workflows to gather behavioral data.

Rules for the Experiment stage:
- Change exactly one dimension (tools, instructions, or configuration --
  never more than one).
- Document the change rationale in the fork file's YAML frontmatter under a
  `fork_rationale` field.
- Run at least three different workflows through the fork before advancing
  to Evaluation.
- Link back to the parent agent using a `parent` field in frontmatter
  referencing the absolute path.

Example frontmatter for a fork in Experiment stage:

```yaml
---
name: code-reviewer--strict-mode
version: 0.0.1
status: experiment
parent: file:///home/stveve/Documents/workspace/build-workflow/WASHVN/.claude/agents/code-reviewer.md
fork_rationale: Add explicit denial keywords list to instructions
suite: WASHVN
---
```

### Stage 2: Evaluation

Assess fork effectiveness against the parent using a defined test harness.
The evaluation MUST compare the fork and parent on identical inputs and
produce a written comparison.

Evaluation criteria:
- Does the fork produce different output than the parent on the same input?
- Is the difference an improvement by the metrics defined in the evaluation
  plan?
- Does the fork introduce any regression in unrelated workflows?
- Are the fork's behavioral changes predictable from its configuration
  change?

If the fork passes evaluation, it advances to Stage 3 (Promote). If it fails,
it moves to Stage 4 (Archive).

### Stage 3: Promote

Rename the fork file to replace the parent agent. The promote workflow:

1. Rename the fork file from `<parent-name>--<fork-suffix>.md` to
   `<parent-name>.md`.
2. Rename the old parent file to `<parent-name>--<archive-timestamp>.md` and
   move it to the archive directory.
3. Update all cross-references that pointed to the old parent.
4. Set the frontmatter `status` field to `canonical` and remove the
   `fork_rationale` field.
5. Remove the `parent` frontmatter field -- the promoted fork is now the
   authoritative agent definition.

The archive directory is at ([archive/](file:///home/stveve/Documents/workspace/build-workflow/WASHVN/.claude/agents/_archive/)).

### Stage 4: Archive

If the fork fails evaluation or is superseded by another fork, freeze and
store it. The archive workflow:

1. Set frontmatter `status` to `archived`.
2. Add an `archived_reason` field explaining why the fork was not promoted.
3. Move the file to the archive directory.
4. Keep the file for a minimum of 90 days before deletion, in case the
   evaluation criteria change and the fork merits reconsideration.

## When to Fork vs When to Modify the Parent

Forking is appropriate when:
- The change is experimental and may be rejected.
- The change affects tool selection, which can alter behavior in
  unpredictable ways.
- Multiple variants need comparison in parallel.
- The change is specific to a single workflow or domain and would bloat
  the parent agent's instructions.

Modifying the parent directly is appropriate when:
- The change is a bug fix or clarification that applies universally.
- The change is a dependency update (e.g., a tool name changed).
- The change adds a new capability without removing or altering existing
  behavior.
- The change is proven by a fork that has completed the Promote stage.

Rule: If you are unsure whether to fork or modify, fork first. A fork can
always be promoted, but a broken parent must be reverted from source control.

## Anti-Abuse Rules

These rules prevent misuse of the fork mechanism. Violations MUST be
reverted and logged.

### No Shadow Forks

A shadow fork is a fork file that changes only the agent `description` field
while keeping the tools and instructions identical to the parent. This is an
anti-pattern because it creates a nominally distinct agent with identical
behavior, confusing both operators and automated tooling.

Detection: Compare the tools block and instruction hash between fork and
parent. If only the description differs, the fork is a shadow fork.

Remediation: Delete the shadow fork file. If a different description is
needed, the parent's description should be updated directly.

### No Description-Only Changes

Changing only the description of a fork without altering tools or
instructions is prohibited for the same reason as shadow forks. A fork MUST
change at least one of the following: the tools list, the instructions text,
or a configuration parameter that affects runtime behavior.

### No Fork Chains

A fork of a fork (a chain longer than one level) MUST NOT exist. If you need
a variant of a fork, wait for the fork to either be promoted (then fork the
new parent) or archived (then start a new fork from the original parent).

Rationale: Fork chains create diamond dependencies that make conflict
resolution intractable. The double-hyphen naming convention would also break
down with multi-level forks (e.g., `parent--fork--subfork` is not parsable).

### No Stale Forks

Any fork in the Experiment or Evaluation stage that has not been touched in
14 days is stale. Stale forks MUST be either promoted, archived, or deleted.
An automated cleanup script runs daily at 0200 UTC and warns about forks
approaching the 14-day limit.

## Conflict Resolution

When a parent agent is updated after one or more forks have diverged from it,
conflicts may arise. Conflicts occur when the parent and fork modify the same
tool or instruction section.

### Low-Conflict Changes

If the parent update does not overlap with the fork's changed section, the
fork inherits the parent update automatically. Apply the parent's changes to
the fork's unchanged sections.

### High-Conflict Changes

If the parent update overlaps with the fork's changed section, a manual
reconciliation is required:

1. Identify the specific lines in conflict.
2. Determine whether the fork's change is still valid given the parent
   update.
3. If the fork's change is still valid, update the fork to incorporate both
   the parent change and the fork change.
4. If the fork's change is superseded by the parent change, the fork is now
   redundant -- archive it.
5. Document the resolution in the fork's frontmatter under `conflict_resolution`.

If a fork accumulates three or more conflict resolutions, it is a strong
signal that the fork should be promoted or archived -- it has diverged too
far to maintain as a parallel variant.

### Broadcast Updates

When a parent is updated, all active forks SHOULD receive a notification.
The broadcast mechanism checks each fork's `parent` frontmatter field and
flags the fork as requiring review. The flag is cleared once the fork is
updated or archived.

## Fork Cleanup and Orphan Management

An orphan fork is a fork whose parent no longer exists (the parent was
renamed, archived, or deleted). Orphan forks MUST be resolved within 7 days.

Orphan detection: Any fork whose `parent` field points to a file that does
not exist is an orphan. The automated cleanup script identifies orphans daily.

Orphan resolution options:
- If the parent was promoted from another fork, update the orphan's `parent`
  field to point to the new parent.
- If the parent was archived, either fork from the current canonical agent or
  delete the orphan.
- If the parent was deleted without being archived, file an incident report
  and archive the orphan.

Unresolved orphans after 7 days are automatically archived with the reason
`orphan-unresolved`.

## Practical Fork Scenarios

### Scenario 1: Strict Mode Code Reviewer

Parent agent `code-reviewer` has a permissive set of review rules. A fork
named `code-reviewer--strict-mode` adds explicit denial keywords to the
instructions. The fork is tested on three pull requests, the output is
compared against the parent, and the stricter mode catches two real issues
the parent missed. The fork is promoted.

### Scenario 2: Verbose Debugger

Parent agent `debugger` uses compact output. A fork named
`debugger--verbose` adds full stack trace logging to the instructions. The
fork is tested but the verbose output overwhelms the context window. The
fork fails evaluation and is archived with reason `context-overhead-too-high`.

### Scenario 3: Minimal Explorer

Parent agent `explorer` has twelve tools. A fork named
`explorer--minimal-tools` reduces the tool count to five by removing
infrequently used tools. The fork passes evaluation and is promoted. The old
parent is archived as `explorer--2026-07-07-full-tools`.

### Scenario 4: Aggressive Task Splitter

Parent agent `planner` breaks work into three to five tasks. A fork named
`planner--aggressive-split` breaks work into eight to twelve tasks. The fork
passes evaluation for large codebases but fails for small changes. The fork
is kept in Experiment stage for domain-specific use rather than promoted --
this is allowed only when the fork and parent serve different input domains.
The fork's frontmatter MUST document the domain constraint.

## Cross-References

- [Agent configuration patterns](file:///home/stveve/Documents/workspace/build-workflow/WASHVN/.claude/knowledge/agents/configuration.md)
- [Subagent forge contract](file:///home/stveve/Documents/workspace/build-workflow/WASHVN/.claude/agents/subagent-forge.md)
- [Workflow pattern registry](file:///home/stveve/Documents/workspace/build-workflow/WASHVN/.claude/knowledge/agents/workflow_patterns.md)
- [Capability controls](file:///home/stveve/Documents/workspace/build-workflow/WASHVN/.claude/knowledge/agents/capability_controls.md)
- [XML tags standards](file:///home/stveve/Documents/workspace/build-workflow/WASHVN/.claude/knowledge/agents/xml_tags_standards.yaml)
- [Fork archive directory](file:///home/stveve/Documents/workspace/build-workflow/WASHVN/.claude/agents/_archive/)
- [WASHVN master skill suite architecture](file:///home/stveve/Documents/workspace/build-workflow/WASHVN/architecture.md)
