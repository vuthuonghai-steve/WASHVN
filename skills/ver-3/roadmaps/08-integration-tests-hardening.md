# Phase 8 — Integration Tests & Architectural Hardening

> **Order:** 9th phase (final) | **Estimated effort:** L (large) | **Predicted duration:** 3-4 sessions
> **Depends on:** Phase 2 (Hooks), Phase 3 (Agents), Phase 5 (BA skills), Phase 6 (8 main skills), Phase 7 (sandbox+indexer)
> **Architectural defects addressed:** ALL 10 HIGH/CRITICAL defects từ architectural critic report
> **Roadmap evaluation v1 patches incorporated:** Đề xuất 2 (hysteresis re-eval cap=1 — A2 update), Đề xuất 4 (escalation_report.yaml với traceback đầy đủ — A4 update), Đề xuất 2 về State Summarization thay vì Pruning (A6 update)

## Mục đích

Phase 8 là giai đoạn **tổng hợp và cứng hóa** (hardening). Mục đích kép:

1. **Integration tests end-to-end** — verify toàn bộ 11 skills + 5 agents (subagent-forge + 4 mới) + 6 hooks + 14 schemas + DRC contracts hoạt động như một workflow duy nhất.

2. **Address 10 architectural defects** đã phát hiện trong critic report. Phase 8 patch + bound + structurally modify để các defect không re-produce trong production.

Phase 8 KHÔNG build anything mới. Phase 8 modify/patch existing artifacts từ Phase 0-7 để handle defects.

---

## Prerequisites

```yaml
prerequisites:
  - Phase 1-7 done
  - skills-registry.json valid
  - llms.txt exists with mock-prompt-cleaner entry (from Phase 7)
  - All 11 skills deployed
  - All 5 agents deployed
  - All 6 hooks active
  - 1 full mock skill pipeline previously completed (mock-prompt-cleaner)
```

---

## Phần A: 10 Architectural Defects to Address

### A1 — Defect Γ-1: Self-Referential Blindness (CRITICAL)

**Status Post-Phase 6**: Đã address bằng cách invoke `aggregate-quality-gatekeeper` (Phase 3 agent) + `external-code-reviewer` (Phase 3 agent) + `sandbox-tester` (Phase 7 mechanical validator).

**Phase 8留下了 work**:
- Verify audit logs show external-co-validator được invoked at META gate + code review gate + sandbox gate
- Add hard-fail safety hook — if skill-pipeline-orchestrator tries to skip external validator, the Phase 2 hook `.claude/hooks/events/pre-tool-use_bash_validate_command.sh` should detect

**Action item**: 
- Author `.claude/hooks/events/post-tool-use_external_validator_required.sh`
  - Matcher: `Write`
  - Triggers when `design.md`, `audit-metrics.yaml`, or `verification.md` is written
  - Checks: was aggregate-quality-gatekeeper OR external-code-reviewer invoked since last write to design.md?
  - If not: log WARNING to audit, don't block (allow pipeline continue but flag for review)
- Update `.claude/hooks/registry.yaml` with new entry

**Verification**:
- Verify audit log shows new hook firing
- Run fresh mock-prompt-cleaner pipeline, confirm external validator traceable in audit log

### A2 — Defect Γ-3: SCS 3.0 Cliff (HIGH)

**Status Post-Phase 6**: skill-explorer emits `hysteresis_triggered: true` when SCS ∈ [2.7, 3.3]. **Re-eval cap = 1** đã enforce trong skill-explorer (per eval v1 đề xuất 2, đã incorporate ngay tại Phase 6 — tránh infinite loop Explorer↔Gatekeeper).

**Phase 8 additionally**:
- Update `production-quality-gatekeeper` SKILL.md to enforce: if design.md frontmatter `hysteresis_triggered: true` AND `re_eval_count === 0` → mandatory re-eval before route decision is final
- If `re_eval_count === 1` (cap reached) AND SCS still ∈ [2.7, 3.3] → không block approval, accept Branch B (conservative) per Phase 6 strategy
- Update `_shared/scripts/drc_resolver.py` to validate hysteresis flag AND `re_eval_count ≤ 1`
- Create test case with SCS=2.95:
  - First eval: hysteresis_triggered=true, re_eval_count=0, routing_decision=re-eval → F4 fires
  - After 1 re-eval (re_eval_count=1), still in zone → routing_decision=B (conservative default)
  - Test không trigger F4 lần nữa (cap=None enforced)

**Action items**:
1. Edit `.claude/skills/production-quality-gatekeeper/SKILL.md` — add `<phase_hysteresis_handling>` to workflow:
   ```markdown
   <phase_hysteresis_handling>
   If design.md frontmatter hysteresis_triggered=true:
   1. Read re_eval_count field
   2. If re_eval_count == 0: Block quality_matrix approval, emit feedback.yaml "RE-EVAL REQUIRED", trigger F4 fallback to skill-explorer
   3. If re_eval_count == 1: Authorize Branch B as conservative default. Emit quality-matrix.yaml với note "hysteresis-resolved-conservative". Do NOT trigger F4.
   </phase_hysteresis_handling>
   ```
2. Update DRC resolver script to detect hysteresis + enforce re_eval_count ≤ 1
3. Test with mock SCS=2.95 → verify NO F4 trigger on second visit (cap enforced, no infinite loop)

### A3 — Defect Γ-4: Hydrator Information Loss

**Replaced strategy**: Phase 6 đã include `aggregate-quality-gatekeeper` access to original `design.md` (not just condensed `hydrated-context.yaml` from Phase 2 spec). Verify this override:

**Action items**:
- Verify `.claude/skills/aggregate-quality-gatekeeper/SKILL.md` (Phase 3 agent output)
  -workflow phases reads `design.md` directly, NOT condensed context
- Author test: compare aggregate-quality-gatekeeper input file path vs skills design.md actual path
- Document in `.claude/knowledge/architecture-tensions.md` (new excerpt) explaining the override

### A4 — Defect Γ-7: Escalation Recursion & Open-Loop Fallbacks

**Phase 8 patch** (cập nhật per eval v1 đề xuất 4):
- Add `escalation_depth` field to `_state.yaml` schema (Phase 1's `state-yaml-protocol.md` already has escalation block; Phase 8 adds depth counter)
- Hook `.claude/hooks/events/stop_session_log_state.sh` (Phase 2 already created): enhance to also CHECK escalation depth — if escalation > 2 → trigger HARD halt via Stop hook exit 2
- **CRITICAL (eval v1 patch)**: Trước khi exit 2, tạo `escalation_report.yaml` với traceback đầy đủ — không chỉ stderr chung chung

**Action items**:
1. Edit `_shared/schemas/state.schema.yaml` (or equivalent) — add field:
   ```yaml
   escalation:
     triggered: bool
     reason: string
     escalated_to: "oracle"|"user"|"halt"
     depth: integer (default 0, max 2)
     last_triggered_at: timestamp
     last_failure_summary: string    # One-line summary of what triggered escalation
   ```
2. Update skills × fallback chain to increment `depth` counter when escalation triggers
3. Modify hook `stop_session_log_state.sh` với escalation گزارش structured:
   ```bash
   # NEW: check escalation depth + create structured report
   DEPTH=$(python3 -c "import yaml; print(yaml.safe_load(open('.skill-context/_state.yaml'))['escalation']['depth'])" 2>/dev/null || echo 0)
   if [ "$DEPTH" -ge 2 ]; then
     # Create structured escalation report (eval v1 đề xuất 4) — không chỉ stderr:
     REPORT_PATH=".skill-context/_state-archive/escalation-report-$(date +%Y%m%d-%H%M%S).yaml"
     STDERR_LOG_PATH=".skill-context/_state-archive/session-stderr-$(date +%Y%m%d).log"
     cat > "$REPORT_PATH" << EOF
   triggered_at: $(date -u +"%Y-%m-%dT%H:%M:%SZ")
   escalation_depth: $DEPTH
   pipeline_phase: $(python3 -c "import yaml; print(yaml.safe_load(open('.skill-context/_state.yaml'))['pipeline_state']['current_stage'])" 2>/dev/null || echo unknown)
   failure_summary: $(python3 -c "import yaml; print(yaml.safe_load(open('.skill-context/_state.yaml'))['escalation']['last_failure_summary'])" 2>/dev/null || echo "summary not recorded")
   previous_escalations:
     $(python3 -c "
   import yaml
   data = yaml.safe_load(open('.skill-context/_state.yaml'))
   for entry in data.get('fallback_history', [])[-5:]:
     print(f'  - stage: {entry.get(\"stage\")}, reason: {entry.get(\"reason\")}, timestamp: {entry.get(\"timestamp\")}')
   " 2>/dev/null || echo "  - history unavailable")
   action_required: "Manual intervention needed — pipeline halted"
   recommended_recovery: "Review escalation-report.yaml, identify root cause (not symptom), re-init from checkpoint (.skill-context/_state-archive/)"
   EOF
     echo "ESCALATION DEPTH EXHAUSTED: halt pipeline, escalation_report.yaml created at $REPORT_PATH" >&2
     echo "Read $REPORT_PATH for full traceback. Manual intervention required." >&2
     exit 2  # block stop, alert user with structured artifact for triage
   fi
   ```
4. Verify `escalation_report.yaml` được generate khi test escalation depth=2 simulation

### A5 — Defect Γ-7 (sub): Re-init destroys state

**Status Post-Phase 0 + Phase 2**: Stop hook đã backup `_state.yaml` corrupt → `_state-archive/_state-{timestamp}-corrupt.yaml`.

**Phase 8 verify**:
- Test corrupt state simulation — verify backup created
- Document restore procedure in `.claude/knowledge/state-archive-restore-procedure.md`

### A6 — Defect Γ-2: Combinatorial State (57 fallback paths) — Pruning → Summarization (eval v1 đề xuất 2)

**Phase 8 patch** (cập nhật per eval v1 đề xuất 2 — không chỉ prune cứng, summary để giữ memory):
- `_state.yaml.fallback_history` có bound soft = 20 entries với cơ chế **state summarization** thay vì hard prune
- Khi history vượt 20 entries, gộp 15 entries cũ nhất thành 1 tóm tắt 1-line ("Đã thử 15 lần fallback ở Phase X do lỗi Y, tất cả đều thất bại"), giữ 5 entries close-detail

> [!IMPORTANT]
> Cơ sở lý luận (per eval v1): Hard pruning cứng = mất ký ức LLM về lỗi cũ → có thể lặp lại chính lỗi đó vì nghĩ "first time". Summarization gộp volume cũ thành concise summary + giữ recent raw events = best of both: bounded context window + retained memory.

**Action items**:
1. Update `suite_config.yaml` (Phase 0 created) — đổi `max_history_entries: 20` thành:
   ```yaml
   fallback_history_management:
     policy: summarize
     soft_cap: 20
     detailed_recent: 5
     summarize_oldest: 15
     summary_format: "{count} lần fallback ở Phase {phase_code} do {error_pattern}, all failed"
   ```
2. Update skill-pipeline-orchestrator's `<safety_contract>`:
   ```markdown
   - On each fallback append to `_state.yaml.fallback_history`:
     - If len(fallback_history) <= 20: append raw entry (preserve all detail)
     - If len(fallback_history) > 20 (cap exceeded):
       1. Group last 15 raw entries by (phase_code, error_pattern) tuple
       2. For each group với multiple occurrences: replace với 1 summary line "{count} lần fallback ở Phase {phase_code} do {error_pattern}, all failed"
       3. Keep last 5 raw entries close-detail for direct context
       4. Insert summary lines at the head of history list
     - Total entries never exceed 20 (5 raw + ≤15 summary lines)
   ```
3. Update schema validator to enforce:
   - `len(fallback_history) ≤ 20` after summarization
   - summary entries must have field `entry_type: summary` (vs raw entries `entry_type: raw`)
4. Test: force 30+ fallbacks in mock pipeline
   - Verify: 5 recent raw entries present at tail
   - Verify: ≤15 summary entries at head
   - Verify: total entries ≤ 20
   - Verify: at least 1 summary entryreferences old repeated errors (proving memory retention)

### A7 — Defect Γ-5: Multi-Agent Coordination Tax (P4)

**Phase 8 patch**:
- Update `.claude/knowledge/agents/examples.md` with guidance:
  - "Parallel-branch only recommended for N≥6 micro-tasks"
  - "For N≤3, prefer Branch A (single builder)"
- Update `skill-pipeline-orchestrator` workflow to estimate N during decomposition and REJECT Branch B for small N
- Document this architectural decision in `docs/context-to-work/parallelism-threshold.2026-07-04.md`

### A8 — Defect Γ-6: Token-Saving Routines Cost Tokens

**Phase 8 patch** (P7 spec contradictions):
- Update `skill-builder` (Phase 6) to include `refactor_max_tokens` budget field in DRC:
  ```yaml
  refactoring_budget:
    max_tokens: 1000  # bound on REV-3.0 refactor itself
    prevent_self_referential_loop: true
  ```
- Update `production-code-reviewer` REV-3.0 trigger:
  - If `token_count_skill_md + 200 > refactoring_budget.max_tokens` → skip auto-refactor, dump warning to human instead

### A9 — Defect: F16-F19 Orphan References

**Status**: Phase 1 spec docs sẽ document F16-F19 properly. Phase 8 verify references in:
- `.claude/knowledge/agents/hooks_and_events.md` Phase 1 authored
- `.claude/skills/ba-elicitor/SKILL.md` (failure_modes section)

### A10 — Defect: META-2.2 Phantom Criterion

**Action items**:
1. Update Phase 1's `.claude/knowledge/agents/configuration.md` to define META-2.2 explicitly
2. Update `.claude/skills/production-quality-gatekeeper/SKILL.md` to evaluate META-2.2 (has been phantom before)
3. Test: invoke gatekeeper on mock-prompt-cleaner, verify META-2.2 evaluated (not skipped)

---

## Phần B: Integration Tests End-to-End

### B1: Mock pipeline test with new skill "skill-cleaner-v2"

```bash
# Step 1: User requests building a new skill
USER_REQ="I need a skill that cleans any AI-generated prompt text by removing generic prefixes, removing phrase clichés like 'as an AI language model', and reformatting structure to tight XML-tags"

# Step 2: Invoke ba-pipeline-runner agent (Phase 3)
# task(subagent_type=ba-pipeline-runner, prompt="elicit business for skill 'skill-cleaner-v2' with user input: $USER_REQ")

# Step 3: Verify artifacts:
test -f .skill-context/skill-cleaner-v2/business-analysis.md
test -f .skill-context/skill-cleaner-v2/thought-cache.yaml

# Step 4: Invoke skill-pipeline-orchestrator agent (Phase 3)
# task(subagent_type=skill-pipeline-orchestrator, prompt="build skill 'skill-cleaner-v2'")

# Step 5: Verify end-to-end artifacts:
ARTIFACTS=(
  exploration.md criteria.md domain-handbook.md design.md
  quality-matrix.yaml todo.md build-log.md review-report.md
  audit-metrics.yaml security-review-report.md verification.md
  _indexer_completion.yaml README.md
)
for a in "${ARTIFACTS[@]}"; do
  test -f .skill-context/skill-cleaner-v2/$a || exit 1
done

# Step 6: Verify skill installed
test -f .claude/skills/skill-cleaner-v2/SKILL.md
grep -q "skill-cleaner-v2" skills-registry.json
grep -q "skill-cleaner-v2" llms.txt

# Step 7: Test skill installation works
test $(wc -w < .claude/skills/skill-cleaner-v2/SKILL.md) -le 700

# Step 8: Sandbox PASS
grep -q "PASS" .skill-context/skill-cleaner-v2/verification.md
echo "B1 PASS — full pipeline integration test"
```

### B2: Hook integration test

```bash
# Verify all 6 hooks active during mock pipeline test:
LOG_DIR=.skill-context/_state-archive/
test -f $LOG_DIR/tool-audit-*.log
test -f $LOG_DIR/session-*.log
test -f $LOG_DIR/session-start.log

# Test workspace gate enforcement:
echo '{"tool_name":"Write","tool_input":{"file_path":"/tmp/outside.txt"}}' | \
  bash .claude/hooks/events/pre-tool-use_write_gate.sh
# Expect exit 2

# Test skill staging gate:
echo '{"tool_name":"Write","tool_input":{"file_path":".claude/skills/foo/SKILL.md"}}' | \
  bash .claude/hooks/events/pre-tool-use_skill_staging_gate.sh
# Expect exit 2

# Test bash destructive:
echo '{"tool_name":"Bash","tool_input":{"command":"rm -rf /home"}}' | \
  bash .claude/hooks/events/pre-tool-use_bash_validate_command.sh
# Expect exit 2

echo "B2 PASS — hooks integration"
```

### B3: Agent integration test

```bash
# Verify all 5 agents deployed:
for agent in subagent-forge skill-pipeline-orchestrator aggregate-quality-gatekeeper ba-pipeline-runner external-code-reviewer; do
  test -f .claude/agents/$agent.md || exit 1
done

# Invoke each agent (smoke test — verify no broken references):
# task(subagent_type=skill-pipeline-orchestrator, prompt="status check")
# expect non-error response referencing 7 knowledge docs

# Each agent should read 7 knowledge docs:
for agent in skill-pipeline-orchestrator aggregate-quality-gatekeeper ba-pipeline-runner external-code-reviewer; do
  count=$(grep -c "\.claude/knowledge/agents/" .claude/agents/$agent.md)
  test "$count" -ge 7 || exit 1
done
echo "B3 PASS — agents integration"
```

### B4: Schema DRC integration test

```bash
python3 raw/ver-3/_shared/scripts/drc_resolver.py --all
# Expect exit 0 — all 11 skills have valid DRC pointing to existing schemas
echo "B4 PASS — DRC integration"
```

### B5: Skills-registry consistency test

```bash
python3 .claude/scripts/validate_suite_integrity.py
# Expect exit 0 — registry consistent with filesystem
echo "B5 PASS — registry consistency"
```

### B6: Defect regression tests

For each defect A1-A10, run a regression test:

```bash
# A1 — external validator invoked
grep -E "aggregate-quality-gatekeeper|external-code-reviewer" .skill-context/_state-archive/tool-audit-*.log | head -1

# A2 — hysteresis triggered test
# Create mock exploration with scs_score: 2.95 → verify re-eval triggered

# ... (one regression test per defect)
echo "B6 PASS — defect regression tests"
```

---

## Step-by-step task list

### Step 1: Architectural Defect Patches (Part A)

1.1 (A1): Author `.claude/hooks/events/post-tool-use_external_validator_required.sh`
1.2: Update `.claude/hooks/registry.yaml` with new hook
1.3: Test hook fires on Write to design.md without prior aggregate-quality-gatekeeper Task call

2 (A2): Edit `.claude/skills/production-quality-gatekeeper/SKILL.md` — add hysteresis handling phase
2.2: Update `drc_resolver.py` for hysteresis validation
2.3: Test SCS=2.95 case → verify re-eval triggered

3 (A3): Verify aggregated-gatekeeper reads design.md directly
3.1: Test with mock-prompt-cleaner that gatekeeper DRC references design.md path

4 (A4): Add escalation_depth field to state schema
4.1: Update skill orchestrators to increment depth
4.2: Modify Stop hook to enforce halt at depth=2
4.3: Test escalation depth simulation

5 (A5): Verify state archive restore works (test corrupt state backup → simulate restore)

6 (A6): Update skill-pipeline-orchestrator `<safety_contract>` with prune policy
6.1: Test 30+ force fallbacks on mock skill, verify pruning

7 (A7): Update examples.md with parallelism threshold guidance
7.1: Update skill-explorer to estimate N and reject Branch B if N<6
7.2: Document decision in `docs/context-to-work/parallelism-threshold.2026-07-04.md`

8 (A8): Update skill-builder DRC with `refactor_max_tokens` budget
8.1: Update production-code-reviewer REV-3.0 trigger to respect budget

9 (A9): Verify F16-F19 documented in knowledge base hooks_and_events.md
9.1: Update any skill referencing F16-F19 with consistent definition

10 (A10): Define META-2.2 in `.claude/knowledge/agents/configuration.md`
10.1: Update gatekeeper SKILL.md to actually evaluate META-2.2
10.2: Test gatekeeper invocation, verify META-2.2 evaluated

### Step 2: Integration Tests (Part B)

11. Setup mock skill "skill-cleaner-v2"
11.1: Run B1 full pipeline test
11.2: Run B2 hook test
11.3: Run B3 agent test
11.4: Run B4 DRC test
11.5: Run B5 registry consistency test
11.6: Run B6 defect regression tests

### Step 3: Documentation & Archival

12. Author `docs/context-to-work/phase-8-summary.2026-07-04.md` (per context-before-fix pattern):
    - List of all defects patched
    - Test results
    - Open issues remaning (if any)
    - Lessons learned

13. Author `docs/context-to-work/architectural-tensions-resolutions.2026-07-04.md`:
    - Map each defect (γ-1 to γ-7) to fix applied
    - Document fixes that are structural vs documented guidelines
    - Document unresolved tensions (anything still HIGH severity)

14. Update `Temps/spec/roadmaps/index.md`:
    - Mark all phases `done`
    - Update verification dashboard
    - Add "Post-Phase 8 Confidence Assessment" section

15. Update `architecture.md` with note that:
    - Phase 8 fixes have been applied
    - Reference roadmaps/architectural-tensions-resolutions.md for details

16. Commit final: `phase-8: complete — all 10 defects patched, integration verified, suite hardened`

---

## Definition of done (Phase 8)

```yaml
dod:
  - All 10 defects Gamma-1 → Gamma-7 (including sub-defects) addressed
  - Integration tests B1-B6 all PASS
  - Mock skill "skill-cleaner-v2" successfully built end-to-end
  - All 6 hooks verified firing during mock pipeline
  - All 5 agents verified invokeable with valid references
  - All 14 schemas validated against at least 1 valid fixture
  - Skills-registry.json consistent with deployed skills
  - llms.txt contains all completed skills
  - audit logs show external validators invoked at META + code review gates
  - SCS hysteresis correctness tested with SCS=2.95
  - Escalation depth enforcement tested
  - Phase 8 summary doc + tensions resolutions doc authored
  - index.md marked "all phases done"
```

---

## Tình trạng toàn lộ trình sau Phase 8

Sau Phase 8 completed:

| Thành phần | Số lượng | Status |
|:---|:---:|:---:|
| Skills deployed | 11 | done |
| Agents deployed | 5 (subagent-forge + 4 production) | done |
| Hooks standalone | 7 (6 from Phase 2 + 1 from Phase 8) | done |
| Knowledge docs | 7 canonical + 14 schemas + 2 config = 23 | done |
| DRC contracts | 11 | done |
| Architectural defects patched | 10/10 | done |
| Integration tests passing | 6/6 (B1-B6) | done |
| End-to-end mock skill pipeline tests passing | 2 (mock-prompt-cleaner + skill-cleaner-v2) | done |

Master Skill Suite đạt trạng thái **publication-ready ≥90%** per architectural critic assessment.

---

## Liên kết

- [Roadmap Index](index.md)
- [Phase 7 trước](07-skill-build-sandbox-indexer.md)
- [Architectural critic report reference](file:///home/stveve/Documents/workspace/build-workflow/WASHVN/Temps/spec/architects/README.md)
- [Spec P5 fallback matrix](file:///home/stveve/Documents/workspace/build-workflow/WASHVN/Temps/spec/architects/P5-fallback-and-escalation/fallback-matrix-full.md)