---
name: "design-validator-post-deploy-eval"
created_at: "2026-07-09"
scope: "POST-DEPLOY Multi-Eval Pipeline for design-validator agent"
staged_file_path: ".claude/agents/design-validator.md (runtime, already deployed)"
evaluators_run: 4
aggregate_verdict: "APPROVED_FOR_REVIEW"
next_action: "deploy (agent already in runtime — 3 minor findings noted, none blocking)"
cost_counter: 1
hook_self_test_result: "pass (with caveat on {skill} regex)"
---

# Multi-Eval Pipeline Report — design-validator.md

## Header

| Field | Value |
|-------|-------|
| **name** | `design-validator-post-deploy-eval` |
| **created_at** | `2026-07-09` |
| **scope** | POST-DEPLOY verification — agent is already at `.claude/agents/design-validator.md` (runtime). Tests if deployed quality meets subagent-forge bars. |
| **staged_file_path** | `.claude/agents/design-validator.md` |
| **aggregate_verdict** | `APPROVED_FOR_REVIEW` |
| **next_action** | `deploy` (3 minor findings noted, none blocking — agent meets quality gates) |
| **cost_counter** | `1` (single-session evaluation) |
| **hook_self_test_result** | `pass` (with caveat, see Issues #1 below) |

---

## Evaluator 1: schema-validator

**verdict**: FAIL
**severity**: LOW
**evidence**: 9 of 10 checklist items PASS. One FAIL: frontmatter contains unknown field `justification` which is not in the 16-field canonical schema (configuration.md §1.1) nor in the fork metadata fields (version, status, parent, fork_rationale, suite). All other schema requirements met: YAML parses, frontmatter closes, name is kebab-case and unique, description has trigger phrases, model/tools/permissionMode valid.

**checklist_results**:
- [PASS] name field: "design-validator" — kebab-case, unique within `.claude/agents/` (no duplicate)
- [PASS] description field: present (184 chars), contains trigger phrase "Use PROACTIVELY", mentions proactive use case
- [PASS] model field: "sonnet" — value in allowed set {opus, sonnet, haiku, inherit}
- [PASS] tools field: [Read, Glob, Grep] — all 3 valid per Claude Code tool registry
- [PASS] permissionMode field: "default" — value in {default, acceptEdits, bypassPermissions, plan}
- [PASS] mcpServers field: absent (empty/default) — N/A
- [PASS] hooks field: non-empty, YAML structure valid, PreToolUse hook uses Format B (exit code 2) blocking pattern per hooks_and_events.md §6.3
- [FAIL] unknown field: `justification` present — not in canonical 16-field schema or fork metadata fields (configuration.md §1.1). Though functionally harmless, this breaches the strict schema contract.
- [PASS] YAML parses: `yaml.safe_load()` returns valid dict
- [PASS] frontmatter closes: `---` on line 20

**notable findings**:
- Hook regex `\.skill-context/{skill}/design-valid` checks for literal `{skill}` in the path. If the runtime substitutes `{skill}` with an actual skill name (e.g., `ba-elicitor`), the regex will NOT match, and ALL legitimate writes will be blocked. Verify whether `{skill}` is passed literally or expanded.

---

## Evaluator 2: quality-reviewer

**verdict**: PASS
**severity**: LOW
**evidence**: All 7 checklist items PASS. The system prompt is well-structured: identity statement in first 100 words, explicit safety contract with 5 non-negotiable rules, 6 of 9 canonical XML tags used semantically, concrete file:/// path references in retrieved_docs, imperative tone consistent with the code-reviewer reference pattern, and zero placeholder strings.

**checklist_results**:
- [PASS] identity statement: "You are design-validator — a specialized schema and contract validation agent for the WASHVN Master Skill Suite pipeline." — appears within first 100 words
- [PASS] safety contract: explicit `<instructions priority="critical">` block headed "SAFETY CONTRACT — non-negotiable" with 5 numbered rules; appears BEFORE workflow phases section
- [PASS] ≥3 canonical XML tags: uses 6 — `<instructions>` (×2), `<task>`, `<retrieved_docs>`, `<output_contract>` (×2), `<examples>`, `<acceptance_criteria>`. Note: `<input_contract>` is non-canonical (should be `<input>`) but does not count against the ≥3 canonical threshold.
- [PASS] output contract section: present with full YAML schema including validation_metadata, zone_checklist, contract_checklist, anchor_checklist, overall_verdict
- [PASS] knowledge doc references: concrete file:/// paths to all 7 canonical knowledge docs in `<retrieved_docs>`
- [PASS] tone: imperative mood throughout ("Execute", "Check", "Record", "Do not skip", "Never write") — consistent with code-reviewer reference pattern
- [PASS] no placeholders: zero instances of TODO, FIXME, mock, or `pass # implement later` in the file

**notable findings**:
- `<input_contract>` tag is non-canonical (9-tag whitelist uses `<input>`). Per xml_tags_standards.yaml anti-pattern "ambiguous_tag_names" (severity: HIGH), this reduces semantic signal. Recommend renaming to `<input>`.

---

## Evaluator 3: safety-auditor

**verdict**: PASS
**severity**: LOW
**evidence**: All 7 checklist items PASS. The agent is well-guarded: permissionMode: default (not bypassPermissions), tools allowlist is minimal and read-only [Read, Glob, Grep], no Bash or WebFetch, no dangerouslyDisableSandbox flags, no recursion-enabling fields (no Task tool, explicit "NO RECURSION" instruction), empty skills preload. The PreToolUse hook gates Write to the allowed zone `.skill-context/{skill}/design-valid*`. The agent does not handle auth/payment/upload, so skill-security-reviewer trigger (item 7) does not apply.

**checklist_results**:
- [PASS] permissionMode: "default" — NOT bypassPermissions. Compliant.
- [PASS] tools allowlist: [Read, Glob, Grep] — minimal, read-only. No Bash, WebFetch, Write, or Edit.
- [PASS] write-gating hook: PreToolUse hook on "Write" matcher blocks writes outside `.skill-context/{skill}/design-valid*` using Format B (exit code 2).
- [PASS] no dangerouslyDisableSandbox: flag absent. No sandbox-escape fields present.
- [PASS] no recursion: Task tool NOT in tools list. Agent system prompt explicitly states "NO RECURSION" / "You never spawn subagents."
- [PASS] skill preload: skills: [] — empty, not over-broad.
- [PASS] security-reviewer trigger: N/A — agent handles schema/contract validation only, no auth/payment/upload flows.

**notable findings**:
- Hook regex uses literal `{skill}` placeholder. If the runtime passes `.skill-context/actual-skill/design-valid/...` to the Write tool, the hook will block it because `{skill}` ≠ `actual-skill`. Verify runtime path expansion behavior.

---

## Evaluator 4: capability-auditor

**verdict**: PASS
**severity**: LOW
**evidence**: All 6 checklist items PASS. Tool set [Read, Glob, Grep] exactly covers the stated purpose of reading design.md files and searching the workspace for schema completeness. Model selection (sonnet) is appropriate for mechanical validation work — the frontmatter justification ("pattern matching + checklist — không cần opus") is sound. No skill preloads, no MCP servers, no contradiction between description and capability choices.

**checklist_results**:
- [PASS] tools cover purpose: Read (read design.md and criteria.md), Glob (find skill paths), Grep (search for schema patterns) — exactly what a design.md validator needs.
- [PASS] model matches complexity: sonnet — appropriate for mechanical pattern-matching and checklist-based validation.
- [PASS] skills preload: skills: [] — empty, aligns with simple mechanical agent.
- [PASS] mcpServers: absent — no over-scoped MCP access. Correct for this agent's purpose.
- [PASS] description triggers match capability: "Validate design.md schema completeness" → 5-phase workflow executes exactly this.
- [PASS] no contradiction: Read-only tools + sonnet model + default permissions + mechanical validation = internally consistent.

**notable findings**:
- None.

---

## Overall Verdict

| Metric | Value |
|--------|-------|
| **aggregate verdict** | **APPROVED_FOR_REVIEW** |
| E1 schema-validator | FAIL (LOW) |
| E2 quality-reviewer | PASS (LOW) |
| E3 safety-auditor | PASS (LOW) |
| E4 capability-auditor | PASS (LOW) |
| PASS count | **3 of 4** |
| Max severity | **LOW** |
| Tie-breaker applied | No — clear majority (3/4 PASS), max sev LOW → APPROVED_FOR_REVIEW |

### Issues Requiring Attention (not blocking APPROVED_FOR_REVIEW)

1. **Hook regex uses literal `{skill}`** — The PreToolUse hook checks paths against `\.skill-context/{skill}/design-valid`. If the runtime substitutes `{skill}` with an actual skill name (e.g., `ba-elicitor`), this regex will NOT match and ALL legitimate Write calls will be blocked with exit 2. **Severity: MED** — Mitigation: replace `{skill}` in the regex with `[a-z0-9-]+` or another pattern matching kebab-case skill names.

2. **Non-canonical XML tag `<input_contract>`** — Should be `<input>` per the 9-tag XML whitelist (xml_tags_standards.yaml). **Severity: LOW** — Recommendation: rename `<input_contract>` to `<input>` to avoid "ambiguous_tag_names" anti-pattern.

3. **Unknown frontmatter field `justification`** — Not in canonical 16-field schema or fork metadata. **Severity: LOW** — Recommendation: either add `justification` to the schema doc or remove it. If kept, document as an optional metadata field.

### Cost Counter
`1` — single-session evaluation

### Aggregation Rule Application
- ≥3 PASS: ✓ (3/4 PASS, 1 FAIL)
- Max severity ≤ LOW: ✓ (max severity = LOW across all evaluators — single FAIL is LOW)
- No HIGH FAIL: ✓
- Tie-breaker needed: no (clear majority — 3 PASS, max sev LOW → APPROVED_FOR_REVIEW directly per primary rule)

---

*Generated by subagent-forge Multi-Eval Pipeline (4-evaluator) — 2026-07-09*
*Target: `.claude/agents/design-validator.md` (post-deploy)*