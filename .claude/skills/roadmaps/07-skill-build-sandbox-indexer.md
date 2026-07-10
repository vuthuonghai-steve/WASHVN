# Phase 7 — Build Sandbox-Tester + Indexer (Stage 4 → 5)

> **Order:** 8th phase | **Estimated effort:** M (medium) | **Predicted duration:** 2 sessions
> **Depends on:** Phase 6 (8 main pipeline skills ready, including business-analysis.md → exploration.md cascade)
> **Downstream:** Phase 8 (Integration tests & hardening)
> **Architectural defects addressed:** Γ-1 (sandbox exit codes chèn external ground truth — fix quan trọng nhất)

## Mục đích

Build 2 skills cuối của 8-Stage Pipeline:

1. **sandbox-tester** (Stage 4) — Run test commands trong Docker cô lập, emit verification.md với PASS/FAIL. Đây là **chốt chặn cơ học duy nhất** address defect Γ-1.

2. **indexer** (Stage 5) — Index skill vào `llms.txt`, generate README.md, register vào `skills-registry.json`. Lifecycle phase: built → installed.

---

## Prerequisites

```yaml
prerequisites:
  - Phase 6 done — 8 main skills deployed
  - Docker CLI có sẵn (sandbox requires docker daemon)
  - Test fixtures Phase 6 produced (criteria.md per skill có ≥2 test cases)
  - Architecture.md §3 "Chốt 3: Stage 4 - Sandbox Tester" reference
```

---

## Skill 1: `sandbox-tester` (Stage 4)

### D7-1-1: `skills/ver-3/sandbox-tester/SKILL.md`

```yaml
---
name: sandbox-tester
description: "Skill Stage 4. Trigger khi security-review-report.md AND audit-metrics.yaml available. Run ≥2 test cases from criteria.md trong Docker sandbox isolé. Output verification.md với PASS/FAIL. Address Γ-1: HARD gate có mechanical exit codes (sandbox exit code = PASS/FAIL truth)."
suite: WASHVN
version: 0.0.1
category: monolithic-stage
stage: "Stage 4"
target_variable: target_skill
tags: [sandbox, docker, test, mechanical-verify, gamma-1-fix]
when_to_use: "Last gate before skill delivery. Required." 
last_updated: 2026-07-04
output_contract: ".skill-context/{target_skill}/drc-sandbox-tester.yaml"
---
```

Body — extremely important for Γ-1 fix:

```markdown
<instructions>
You are sandbox-tester skill — Stage 4 of 8-Stage Pipeline. Your role is the ONLY mechanical truth source. Run test commands in Docker isolated environment. Exit codes are the ground truth that breaks LLM self-audit loop.
</instructions>

<safety_contract>
must:
  - Run tests INSIDE Docker container (no host execution)
  - Use ≥2 test cases defined in criteria.md (BA-3.0 edge-case requirement)
  - Output verification.md with PASS/FAIL per test case
  - If ANY test case FAIL → output verification.md = "FAIL", trigger CASE rollback per architecture.md §5
  - Use exit codes: docker run exit 0 = test pass; exit non-zero = test fail
must_not:
  - Run tests on host (security risk)
  - Skip test cases (must run all ≥2)
  - Output "PASS" without running actual sandbox execution
  - Use anywhere eval() in container (security)
</safety_contract>

<workflow_phases>
1. Read criteria.md, build-log.md, security-review-report.md, audit-metrics.yaml
2. <phase_extract_tests>: Parse criteria.md → ≥2 test cases with expected PASS/FAIL
3. <phase_build_sandbox_image>: Generate Dockerfile:
   - FROM python:3.10-slim (or appropriate image per skill domain)
   - COPY only target skill files
   - Install dependencies (if any) — minimal
   - Set WORKDIR /sandbox/
4. <phase_run_test_cases>: For each test case:
   - docker build
   - docker run --rm test_<skill>_<test_id> sh -c '<test_command>'
   - Capture exit code
   - Log: docker_logs + exit_code + test_id + test_input
5. <phase_aggregate_results>: 
   - If ALL test cases pass → verification.md = "PASS"
   - If ANY case fails → verification.md = "FAIL", append failure details
6. <phase_emit_verification>:
   - Write verification.md per schema (PASS/FAIL + test_results array)
   - If FAIL, write rollback_request.yaml per architecture.md §5 CASE System
7. <phase_state_update>: Update _state.yaml stage_status = "Stage 4 completed" hoặc "Stage 4 FAILED → rollback triggered"
</workflow_phases>

<input_contract>
- name: criteria
  path: .skill-context/{target_skill}/criteria.md
  required: true
- name: build_log
  path: .skill-context/{target_skill}/build-log.md
  required: true
- name: security_review
  path: .skill-context/{target_skill}/security-review-report.md
  required: true
</input_contract>

<output_contract>
- file_id: verification
  path: .skill-context/{target_skill}/verification.md
  schema: skills/ver-3/_shared/schemas/verification.schema.yaml
  lifecycle: WORM
- file_id: rollback_request (conditional)
  path: .skill-context/{target_skill}/rollback_request.yaml
  lifecycle: created_on_fail_only
</output_contract>

<acceptance_criteria>
- verification.md has frontmatter: target_skill, test_count, pass_count, fail_count, overall_verdict
- Each test case has test_id, command, expected_outcome, actual_outcome, exit_code, observed_at
- ≥2 test cases run (per criteria.md BA-3.0)
- Docker container image built successfully
- ZERO host execution (only docker run)
- Overall verdict PASS requires ALL test cases pass
- Rollback triggered automatically on FAIL (per architecture.md §5)
</acceptance_criteria>

<failure_modes>
- F15: sandbox fail (Branch A) → back to skill-builder (Phase compression PC-3 retry, max 3)
- F14: sandbox fail (Branch B) → back to assembler (re-merge micro-skill)
- Sandbox container build error → skip tests, emit FAIL reasoning
- Timeout (5 minutes per test case) → mark FAIL with timeout reason
</failure_modes>
```

### D7-1-2: `skills/ver-3/sandbox-tester/knowledge/docker_patterns.md`

Knowledge doc about Docker isolation patterns:

```markdown
# Docker Sandbox Patterns

## Pattern 1: Pure Python skill testing
FROM python:3.10-slim
COPY skills/ver-3/<target_skill>/ /sandbox/
WORKDIR /sandbox/
RUN pip install --no-cache-dir <deps>
CMD ["python3", "scripts/validate_outputs.py"]

## Pattern 2: Shell script skill testing
FROM bash:5
COPY skills/ver-3/<target_skill>/ /sandbox/
WORKDIR /sandbox/
CMD ["bash", "scripts/run_test.sh"]

## Pattern 3: Skill with hooks
FROM python:3.10-slim
# Need jq for hooks
RUN apt-get update && apt-get install -y jq && rm -rf /var/lib/apt/lists/*
COPY skills/ver-3/<target_skill>/ /sandbox/
WORKDIR /sandbox/
# Hooks need stdin JSON
CMD ["echo $TEST_JSON | bash scripts/hook_under_test.sh"]

## Pattern 4: Network-isolated
FROM python:3.10-slim
# Disable network at build AND run
COPY skills/ver-3/<target_skill>/ /sandbox/
WORKDIR /sandbox/
# docker run --network=none ...
```

### D7-1-3: `skills/ver-3/sandbox-tester/templates/verification_template.md`

```markdown
---
target_skill: {skill_name}
test_count: {n}
pass_count: {n}
fail_count: {n}
overall_verdict: {PASS|FAIL}
sandbox_image: {docker_image_id}
verified_at: {timestamp}
container_runtime: {docker_version}
---

# Verification Report — {skill_name}

## Test Cases Executed

### Test Case 1: {test_id}
- **Command:** `{command}`
- **Expected:** {expected_outcome}
- **Actual:** {actual_outcome}
- **Exit Code:** {exit_code}
- **Verdict:** {PASS|FAIL}
- **Logs (last 10 lines):**
  ```
  {docker_logs}
  ```

### Test Case 2: {test_id}
... (repeat for each test case)

## Aggregate Verdict

- Overall: **{PASS|FAIL}**
- Pass rate: {pass_count}/{test_count} = {%}
- Image built: {sha256}

## Rollback {if FAIL}

Reason: {fail_reason}
Trigger: Architecture §5 CASE System
Target stage: Stage 1 (re-design)
Action: bk-dated to skill-architect for redesign
```

### D7-1-4: `skills/ver-3/sandbox-tester/templates/rollback_request_template.yaml`

```yaml
# Triggered when verification.md verdict = FAIL
request_id: rollback_{skill}_{timestamp}
skill_name: <target_skill>
trigger_criterion: "verification.md FAIL OR score < 85%"
failed_test_cases:
  - test_id: <id>
    failure: <reason>
    log: <tail>
target_stage: "Stage 1"  # architect re-design
requested_at: <timestamp>
```

### D7-1-5: `skills/ver-3/sandbox-tester/loop/sandbox_checklist.md`

### D7-1-6: `skills/ver-3/sandbox-tester/scripts/build_and_run.py`

Master script — orchestrates docker build + run + log aggregation:

```python
#!/usr/bin/env python3
"""Sandbox-tester orchestration script.

Reads criteria.md, extracts test cases, builds Docker image, runs each case, captures logs+exit codes, emits verification.md.

Usage:
  python3 build_and_run.py --target-skill <name>
"""
# Implementation:
# 1. Parse criteria.md for test cases
# 2. Build Dockerfile per pattern
# 3. docker build -t sandbox_<skill>_<timestamp>
# 4. For each test: docker run --rm --network=none -e TIME_LIMIT=300
# 5. Capture logs, exit codes
# 6. Aggregate to verification.md
# 7. If FAIL: write rollback_request.yaml
```

### D7-1-7: `skills/ver-3/sandbox-tester/data/drc.yaml`

### D7-1-8: `skills/ver-3/sandbox-tester/loop/rollback_decision_tree.md`

```markdown
# Rollback Decision Tree

## If verdict = FAIL:

| Failure Type | Target Stage | Action |
|:---|:---|:---|
| Test assertion mismatch | Stage 1.5 (Gatekeeper) | Eventual re-evaluation |
| Code crashes (exit 1) | Stage 3 (Builder) | Re-build addressing root cause |
| Code wrong domain | Stage 0.5 (Explorer) | re-evaluate SCS |
| Resource leak | Stage 3.5 (Code Reviewer) | Static analysis fresh look |
| Rollback triggered >3x | Escalation | Notify user per Phase 8 escalation depth counter (Γ-7 fix) |
```

---

## Skill 2: `indexer` (Stage 5)

### D7-2-1: `skills/ver-3/indexer/SKILL.md`

```yaml
---
name: indexer
description: "Skill Stage 5. Trigger khi verification.md = PASS. Index skill vào llms.txt registry, generate README.md per skill template, register vào skills-registry.json. Lifecycle: built → installed."
suite: WASHVN
version: 0.0.1
category: monolithic-stage
stage: "Stage 5"
target_variable: target_skill
tags: [index, registry, llms-txt, lifecycle-installed]
when_to_use: "After sandbox-tester Stage 4 PASS. Final stage — publishes skill."
last_updated: 2026-07-04
output_contract: ".skill-context/{target_skill}/drc-indexer.yaml"
---
```

Workflow:

```markdown
<workflow_phases>
1. Read verification.md (must PASS), build-log.md, security-review-report.md
2. <phase_generate_readme>: From skill metadata + design.md, output README.md per skill_readme_template.md (Phase 4)
3. <phase_register_llms_txt>: Append skill entry to workspace llms.txt (create if not exists). Format:
   - Name, description, trigger phrases, stage, suite, version, paths
4. <phase_update_registry>: Update skills-registry.json with skill lifecycle_status: "installed"
5. <phase_update_routing>: Update workspce_tree.md with skill entries
6. <phase_emit_completion>: Write _indexer_completion.yaml với skill_name, installed_at, install_path
7. <phase_state_update>: Set _state.yaml status = "completed"
</workflow_phases>

<output_contract>
- file_id: readme
  path: skills/ver-3/<skill>/README.md
  schema: skill README template
- file_id: llms_txt_update
  path: ./llms.txt (workspace root)
  operation: append_or_create
- file_id: registry_update
  path: ./skills-registry.json
  operation: edit_in_place
- file_id: indexer_completion
  path: .skill-context/<skill>/_indexer_completion.yaml
</output_contract>

<acceptance_criteria>
- README.md exists per template
- llms.txt contains skill entry
- skills-registry.json lifecycle_status: "installed" for the skill
- workspce_tree.md updated
- _state.yaml stage_status: "Stage 5 completed"
- _indexer_completion.yaml has install metadata
</acceptance_criteria>
```

### D7-2-2 to D7-2-7: standard pattern

- knowledge/registry_format.md (LLMS.txt format spec)
- templates/llms_txt_entry.template
- templates/readme.template.md (uses Phase 4 template, fully populated)
- loop/lifecycle_checklist.md
- scripts/update_registry.py (JSON update with schema validation)
- scripts/generate_llms_txt.py
- data/drc.yaml

---

## Verification checklist (cơ học)

### AC-1 — 2 skills deployed
```bash
test -f .claude/skills/sandbox-tester/SKILL.md
test -f .claude/skills/indexer/SKILL.md
echo "AC-1 PASS"
```

### AC-2 — Docker available
```bash
docker ps > /dev/null 2>&1 && echo "AC-2 PASS" || { echo "Docker not available — Phase 7 cannot complete"; exit 1; }
```

### AC-3 — Sandbox tester runs mock skill in container
```bash
# Use mock-prompt-cleaner from Phase 6 test:
TARGET="mock-prompt-cleaner"
# Run sandbox-tester script:
python3 .claude/skills/sandbox-tester/scripts/build_and_run.py --target-skill $TARGET

# Verify:
test -f .skill-context/$TARGET/verification.md
# Verify schema:
python3 skills/ver-3/_shared/validators/schema_validator.py --artifact verification --path .skill-context/$TARGET/verification.md
echo "AC-3 PASS"
```

### AC-4 — Indexer updates llms.txt + skills-registry
```bash
TARGET="mock-prompt-cleaner"
python3 .claude/skills/indexer/scripts/update_registry.py --skill $TARGET
python3 .claude/skills/indexer/scripts/generate_llms_txt.py --update

# Verify:
grep -q "$TARGET" llms.txt
grep -q "$TARGET" skills-registry.json
grep -q '"lifecycle_status": "installed"' skills-registry.json

echo "AC-4 PASS"
```

### AC-5 — Integration test: full 8-stage pipeline complete

Run from Phase 6 mock:
```bash
# Verify end state after Phase 6 + Phase 7:
STATE=.skill-context/mock-prompt-cleaner/_state.yaml
ALL_ARTIFACTS=(
  exploration.md criteria.md domain-handbook.md design.md
  quality-matrix.yaml todo.md build-log.md review-report.md
  audit-metrics.yaml security-review-report.md verification.md
  _indexer_completion.yaml README.md
)
for artifact in "${ALL_ARTIFACTS[@]}"; do
  test -f .skill-context/mock-prompt-cleaner/$artifact || exit 1
done
grep -q "Stage 5 completed" $STATE
echo "AC-5 PASS — full pipeline complete for mock-prompt-cleaner"
```

### AC-6 — Rollback triggered on FAIL test

```bash
# Create a deliberately broken skill:
TARGET_BROKEN="mock-broken-skill"
mkdir -p .skill-context/$TARGET_BROKEN/

# Add a criteria.md with test that will fail (test expects exit 0 but script exits 1)
cat > .skill-context/$TARGET_BROKEN/criteria.md << EOF
# Test Criteria for mock-broken-skill

## Test 1
- Command: \`bash scripts/return_1.sh\`
- Expected exit code: 0
EOF

mkdir -p .skill-context/$TARGET_BROKEN/scripts/
echo 'exit 1' > .skill-context/$TARGET_BROKEN/scripts/return_1.sh
chmod +x .skill-context/$TARGET_BROKEN/scripts/return_1.sh

# Run sandbox tester:
python3 .claude/skills/sandbox-tester/scripts/build_and_run.py --target-skill $TARGET_BROKEN

# Verify FAIL + rollback triggered:
VERIFICATION=.skill-context/$TARGET_BROKEN/verification.md
test -f $VERIFICATION
grep -q "FAIL" $VERIFICATION
test -f .skill-context/$TARGET_BROKEN/rollback_request.yaml

# Cleanup:
rm -rf .skill-context/$TARGET_BROKEN/
echo "AC-6 PASS — rollback correctly triggered on fail"
```

---

## Step-by-step task list

1. **Build sandbox-tester SKILL.md** — D7-1-1.
2. **Author docker_patterns.md knowledge** — D7-1-2.
3. **Author verification template** — D7-1-3.
4. **Author rollback template** — D7-1-4.
5. **Author checklist** — D7-1-5.
6. **Author build_and_run.py** — D7-1-6 (full Django-style: argparse with --target-skill, parse criteria.md, run docker, aggregate).
7. **Author DRC** — D7-1-7.
8. **Author rollback decision tree** — D7-1-8.
9. **Invoke quality-scorer** audit sandbox-tester. Fix findings.
10. **Test sandbox-tester với mock skill** from Phase 6 (mock-prompt-cleaner passes, mock-broken-skill fails + rollback).
11. **Deploy sandbox-tester** to .claude/skills/.

12. **Build indexer SKILL.md** — D7-2-1.
13. **Author registry_format.md knowledge** — D7-2-2.
14. **Author templates** — D7-2-3 through D7-2-5.
15. **Author update_registry.py** — D7-2-6.
16. **Author generate_llms_txt.py** — D7-2-7.
17. **Author DRC** — D7-2-7.
18. **Invoke quality-scorer** audit indexer.
19. **Test indexer** on mock-prompt-cleaner after Phase 6 mock passes sandbox.
20. **Deploy indexer**.

21. **Run full AC-1 to AC-6**. Fix any failures.

---

## Definition of done (Phase 7)

```yaml
dod:
  - 2 skills deployed (sandbox-tester, indexer)
  - All AC passed
  - Sandbox-tester verified with mock PASS skill + mock FAIL skill (rollback triggered)
  - llms.txt has mock-prompt-cleaner entry
  - skills-registry.json lifecycle_status installed for completed skills
  - Full 8-Stage Pipeline integration tested with mock-prompt-cleaner
  - Docker isolation enforced (no host execution)
```

---

## Liên kết

- [Roadmap Index](index.md)
- [Phase 6 trước](06-skill-build-main-pipeline.md)
- [Phase 8 kế tiếp](08-integration-tests-hardening.md)
- [Architecture §5 CASE System](../../../architecture.md)
- [Spec P5 fallback matrix](../../../Temps/spec/architects/P5-fallback-and-escalation/fallback-matrix-full.md)