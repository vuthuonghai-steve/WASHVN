# Bug Report — BA Pipeline Runner: State-File Write Blocked by Self-Contradictory Hook

- **Date:** 2026-07-11
- **Severity:** High (pipeline break after stage completion)
- **Status:** Analyzed — fix proposed, not yet applied
- **Component:** `.claude/agents/ba-pipeline-runner.md` + `.claude/hooks/events/*` + `.claude/hooks/validate-state-ledger.sh`
- **Branch:** `feat/architect-v1`

---

## 1. Symptom

The `ba-pipeline-runner` subagent dispatches the 3 BA wrapper agents (elicitor → analyst → synthesizer) successfully. Each subagent completes its task and returns TEXT. However, after a stage finishes, the runner **cannot persist its tracking state file** (`_ba_pipeline_state.yaml`), so the pipeline breaks immediately after stage completion — artifacts from stages may or may not persist, but the lifecycle ledger never gets written.

User-reported phrasing: *"subagent được call nhưng không thể write sau khi task được hoàn thiện, việc bị cản trở bởi một hooks."*

---

## 2. Root Cause (Primary — Definitive)

**Self-contradiction inside the agent-local PreToolUse Write hook.**

`ba-pipeline-runner.md` defines a local Write gate (frontmatter, PreToolUse):

```bash
# line 20
if [[ ! "$FILE_PATH" =~ \.skill-context/.*/ba-(elicitor|analyst|synthesizer)/ ]]; then
  echo "BLOCKED: ba-pipeline-runner chỉ write vào .skill-context/{feature}/ba-*" >&2
  exit 2
fi
```

This regex **only** permits Write paths containing the segment `ba-elicitor/`, `ba-analyst/`, or `ba-synthesizer/`.

But the agent's own `<task>` spec (lines 94-110) **mandates** writing the lifecycle ledger at:

```
.skill-context/{feature}/_ba_pipeline_state.yaml
```

That file lives **directly under** `.skill-context/{feature}/` — it has **no** `ba-*/` segment. The regex does not match → `[[ ! ... ]]` is true → **`exit 2` → BLOCKED**.

The 3 per-stage artifacts (`ba-elicitor/`, `ba-analyst/`, `ba-synthesizer/`) pass the gate. The ledger file (written *after* a stage completes) is blocked. This is exactly the reported break: stage done, state write refused.

---

## 3. Root Cause (Secondary — Validation Dead Zone)

`validate-state-ledger.sh` (hooks/validate-state-ledger.sh line 15) only fires on:

```bash
[[ "$FILE_PATH" =~ _state_ledger\.yaml$ ]] || exit 0
```

The runner writes `_ba_pipeline_state.yaml`, which does **not** match `_state_ledger\.yaml$`. Therefore:

1. The state-ledger YAML/schema validator **never runs** for the BA pipeline.
2. Even if the primary block were lifted, the ledger is effectively unvalidated — a malformed ledger would be written silently (Λ-9 stage state leakage risk, which the hook was designed to prevent).

Combined effect: the state-ledger protection is **dead** for the BA pipeline, and the file that should be protected is the one being blocked.

---

## 4. Git History — What Was Changed to "Bypass"

File: `.claude/agents/ba-pipeline-runner.md`

| Commit | Message | Change |
|---|---|---|
| `02b423e` | phase-3: add frontmatter + decompose aggregate-quality-gatekeeper + hybrid hooks | File created (+196). Subagents wrote their own outputs. |
| `1eee86b` | fix(agents): repair hook stdin keys, hook format, XML tags | Hook keys `params.filePath` / `params.subagent_type`; typed hooks. |
| `6103396` | update hooks | retrieved_docs path fix; added failure mode F6. |
| `bbe9e7b` | fix debug temp agent | **The workaround.** |

**Commit `bbe9e7b` ("lách luật") delta:**

- **Model:** `opus` → `sonnet`.
- **Dispatch model reversed:** subagents no longer Write their own output. Platform guard forbids subagents from writing files, so the runner became a **write-proxy**: dispatch subagent → receive TEXT → runner `Write` the artifact into `.skill-context/{feature}/ba-*/`.
- **Notification:** added mandatory `[BA PIPELINE]` echo after each stage + on done/fail.
- **Artifact rename:** `ba-analyst/analysis-report.md` → `ba-analyst/analyst-output.md`.

No hook was bypassed in `bbe9e7b`; the data flow was **redirected** to comply with the platform constraint. The fix in this report addresses the *remaining* self-contradiction the redirect exposed (the ledger path vs. the Write gate).

---

## 5. Items Confirmed NOT Responsible

| Hook | Verdict | Why |
|---|---|---|
| `pre-tool-use_write_gate.sh` | ✅ Not involved | `ALLOWED_DIRS_REGEX` includes `.skill-context/` — permits BA writes. |
| `pre-tool-use_skill_staging_gate.sh` | ✅ Not involved | Only gates `.claude/skills/` runtime; `.skill-context/` unaffected. |
| `pre-tool-use_bash_validate_command.sh` | ✅ Not involved | Runner has no Bash tool. |
| `ba-elicitor` / `ba-analyst` / `ba-synthesizer` | ✅ By design | tools = `[Read, Skill]` — no Write (runner proxies). Correct per workaround. |

---

## 6. Proposed Fix (Surgical — No Bypass)

### 6.1 — Allow the ledger path in the runner's local Write gate
`ba-pipeline-runner.md` line 20-23:

```bash
# BEFORE
if [[ ! "$FILE_PATH" =~ \.skill-context/.*/ba-(elicitor|analyst|synthesizer)/ ]]; then
  echo "BLOCKED: ba-pipeline-runner chỉ write vào .skill-context/{feature}/ba-*" >&2
  exit 2
fi

# AFTER
LEDGER_REGEX='\.skill-context/.*/_ba_pipeline_state\.yaml$'
if [[ ! "$FILE_PATH" =~ \.skill-context/.*/ba-(elicitor|analyst|synthesizer)/ ]] && [[ ! "$FILE_PATH" =~ $LEDGER_REGEX ]]; then
  echo "BLOCKED: ba-pipeline-runner chỉ write .skill-context/{feature}/ba-* hoặc _ba_pipeline_state.yaml" >&2
  exit 2
fi
```

The gate still enforces zone isolation; it now also permits the mandated ledger file.

### 6.2 — Extend the state-ledger validator (optional, recommended)
`validate-state-ledger.sh` line 15:

```bash
# BEFORE
[[ "$FILE_PATH" =~ _state_ledger\.yaml$ ]] || exit 0

# AFTER
[[ "$FILE_PATH" =~ _state_ledger\.yaml$ ]] || [[ "$FILE_PATH" =~ _ba_pipeline_state\.yaml$ ]] || exit 0
```

This reactivates YAML/schema validation for the BA ledger, closing the validation dead zone (§3).

### 6.3 — Deployment
Per `CLAUDE.md` working policy, edits to runtime agents must be made in `skills/ver-3/` then synced:

```bash
cp -r skills/ver-3/* .claude/skills/   # if the runner lives under skills/ver-3
# otherwise edit the staging copy then sync to .claude/agents/
validate_suite_integrity.py            # run before sync
```

---

## 7. Verification (Post-Fix)

1. Run BA pipeline for a test feature (`elicit business for <feature>`).
2. Assert `.skill-context/{feature}/_ba_pipeline_state.yaml` is created after Stage 1.
3. Assert gate still blocks a Write to any path outside `.skill-context/{feature}/ba-*` and outside the ledger file.
4. Assert `validate-state-ledger.sh` returns `decision: block` on a malformed `_ba_pipeline_state.yaml` (negative test).

---

## 8. Appendix — Mechanical Structural Scan (this report session)

Advisory Stop-hook check, executed via bash (evidence, not asserted):

- **Frontmatter** required fields `name/version/suite/tags` present on both `ba-pipeline-runner.md` and `user-knowledge-ingestor.md` → PASS.
- **Code fences** balanced: ba-pipeline-runner.md fences=6 BALANCED; user-knowledge-ingestor.md fences=10 BALANCED → PASS.
- **Placeholder scan** (`\b(TODO|FIXME|XXX|mock\(|pass\s*#|raise NotImplementedError)\b`) across both agents + all `hooks/events/*.sh` + `validate-state-ledger.sh` → none found → PASS.

---

*Report generated from hook-source analysis + git history (`git-master` subagent) + mechanical file scan. No runtime fixes applied yet — pending user approval.*
