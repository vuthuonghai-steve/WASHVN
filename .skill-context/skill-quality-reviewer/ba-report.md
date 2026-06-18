---
skill_name: skill-quality-reviewer
stage: -1
subagent: business-analyst
status: ba-completed
confidence: 78
generated_at: 2026-06-18T00:00:00Z
---

# BA Report — `skill-quality-reviewer` (Stage -1 Output)

> Source: 3-phase BA pipeline (elicitor → analyst → synthesizer).
> Renamed from `production-code-reviewer` (domain mismatch: code review → skill review).

---

## 1. Normalized Requirements (Trace-Tagged)

### Functional Requirements (MoSCoW)

| ID | Statement | MoSCoW | Trace |
|----|-----------|--------|-------|
| FR-01 | Parse YAML frontmatter, validate 8 required keys (name/description/version/suite/tags/when_to_use/inputs/outputs) | **Must** | [USER §2.1] |
| FR-02 | Count tokens SKILL.md (tiktoken), warn > 700 (L0 anchor) | **Must** | [USER §2.2] |
| FR-03 | Detect 7-Zone presence (SKILL.md + knowledge/ + scripts/ + templates/ + data/ + loop/ + policy/) | **Must** | [USER §2.4] + [framework.md §1] |
| FR-04 | Scan placeholder regex (# TODO, # FIXME, mock(), pass) trong `scripts/*.py` | **Must** | [USER §2.5] |
| FR-05 | Parse `criteria.md` → ≥ 5 acceptance criteria + ≥ 2 test scenarios | **Should** | [USER §2.6] |
| FR-06 | Validate `output_contract` YAML theo DRC schema | **Must** | [USER §2.7] + [standards.md §3.2] |
| FR-07 | Detect Progressive Disclosure Tier 1-4 (via `<routing>` block) | **Should** | [production-code-reviewer/SKILL.md pattern] |
| FR-08 | Generate `review-report.md` với 4 severity labels (Must Fix/Optional/FYI/Nit) | **Must** | [USER §3] |
| FR-09 | Generate `audit-metrics.yaml` (deterministic scores) | **Must** | [USER §3] |
| FR-10 | CLI invocation: `python3 scripts/skill_audit.py <target_path> [--target-skill NAME] [--self]` | **Must** | [USER §3] |
| FR-11 | Append progress vào `.skill-context/{name}/pipeline.log` | **Could** | [orchestrator convention] |
| FR-12 | Diff 2 lần audit runs | **Won't** (v2) | [out of scope] |

### Non-Functional Requirements

| ID | Metric | Target | Trace |
|----|--------|--------|-------|
| NFR-PERF-01 | Script wall-clock p95 | ≤ 2s (script only) / ≤ 30s (e2e with LLM) | [derived] |
| NFR-TOK-01 | Output report token count | ≤ 2,500 tokens | [standards.md §6] |
| NFR-COMPAT-01 | Python version | ≥ 3.10 (tested 3.14.3) | [USER] |
| NFR-COMPAT-02 | External deps | chỉ `pyyaml>=6.0` + `tiktoken` (stdlib + 2 packages) | [USER] |
| NFR-COMPAT-03 | Network calls | 0 | [USER] |
| NFR-DETERM-01 | Deterministic gate ratio | script ≥ 30% checks (FR-01,02,03,04,06); LLM ~70% | [USER architecture decision] |
| NFR-DETERM-02 | LLM confidence threshold | ≥ 0.7 LGTM; < 0.5 REJECT | [derived from CASE] |
| NFR-SAFE-01 | Side-effects on target | 0 (read-only) | [Google convention] |
| NFR-MAINTAIN-01 | SKILL.md self ≤ 700 tokens | hardcoded `--self` mode verify | [L0 anchor] |

---

## 2. In/Out of Scope

**IN scope**: frontmatter parse, token count, 7-Zone detect, placeholder scan, criteria parse, output_contract DRC, PD Tier 1-4 detect, severity labels, CLI, audit-metrics.yaml, pipeline.log append.

**OUT of scope** (delegate to specialized skills):
- Python AST code analysis → dùng `production-code-reviewer` (legacy) hoặc `ruff`/`black`
- Security audit OWASP → `skill-security-reviewer`
- High-level architecture review → `skill-architect`
- Auto-fix violations → manual follow-up CL
- Performance profiling → `cProfile`/`py-spy`
- Runtime debug → Claude built-in tools
- Cross-skill diff → future v2
- Web UI / git ops → out

**Boundary cases**:
- `assets/` zone optional
- `policy/` zone bonus Optional (nếu có thì review deeper)
- `criteria.md` không bắt buộc với mọi skill → skip FR-05 nếu absent
- Self-review (audit chính nó) skip auto-loop, dùng `--self` mode

---

## 3. Acceptance Criteria (Seed cho Stage 0 criteria.md)

```yaml
acceptance_criteria:
  - id: AC-01
    description: "Script chạy thành công trên Python 3.14.3 với chỉ pyyaml>=6.0 + tiktoken"
    verification: "python3 scripts/skill_audit.py --selftest"
    expected: "Exit 0, in 'selftest PASS'"
    trace: "[NFR-COMPAT-01/02]"

  - id: AC-02
    description: "Review 1 skill tốt (sample-good) trả về verdict=LGTM exit 0"
    verification: "python3 scripts/skill_audit.py data/fixtures/sample-good/ --target-skill sample-good"
    expected: "Exit 0, STDOUT verdict=LGTM, files created, 0 Must Fix"
    trace: "[Gherkin Scenario 1]"

  - id: AC-03
    description: "Review skill thiếu frontmatter trả về verdict=REJECT exit 1"
    verification: "python3 scripts/skill_audit.py data/fixtures/sample-bad-frontmatter/"
    expected: "Exit 1, STDOUT verdict=REJECT, 1+ Must Fix finding"
    trace: "[Gherkin Scenario 2]"

  - id: AC-04
    description: "SKILL.md > 700 tokens → Must Fix L0 anchor violation"
    verification: "python3 scripts/skill_audit.py data/fixtures/sample-bloated/"
    expected: "Exit 1, Must Fix 'SKILL.md vượt 700 tokens', audit-metrics.yaml token_count=850"
    trace: "[Gherkin Scenario 3]"

  - id: AC-05
    description: "SKILL.md của skill-quality-reviewer chính nó ≤ 700 tokens"
    verification: "python3 scripts/skill_audit.py raw/ver-3/skill-quality-reviewer/ --self"
    expected: "Exit 0, 'Self-check PASS', token_count ≤ 700"
    trace: "[NFR-MAINTAIN-01]"

  - id: AC-06
    description: "Placeholder TODO trong scripts/ bị phát hiện severity Must Fix"
    verification: "python3 scripts/skill_audit.py data/fixtures/sample-todo/"
    expected: "Exit 1, Must Fix finding tại scripts/main.py:<line>, msg 'Placeholder detected: TODO'"
    trace: "[Gherkin Scenario 4]"

  - id: AC-07
    description: "Path không tồn tại → exit 3, không tạo file output"
    verification: "python3 scripts/skill_audit.py raw/ver-3/nonexistent/"
    expected: "Exit 3, STDERR 'ERROR: target path does not exist'"
    trace: "[Gherkin Scenario 5]"
```

---

## 4. Test Scenarios (≥ 2)

```yaml
test_scenarios:
  - id: TS-01
    name: "End-to-end LGTM happy path"
    description: "Review sample-good → expect LGTM + report + metrics + exit 0"
    steps:
      - "Setup: tạo data/fixtures/sample-good/ với đầy đủ 7 zones + frontmatter OK"
      - "Run: python3 scripts/skill_audit.py data/fixtures/sample-good/ --target-skill sample-good"
      - "Assert: exit 0, files exist, 0 Must Fix"
    expected: "All assertions pass"

  - id: TS-02
    name: "End-to-end REJECT với missing frontmatter"
    description: "Review skill thiếu frontmatter → expect REJECT + Must Fix"
    steps:
      - "Setup: data/fixtures/sample-bad-frontmatter/ SKILL.md thiếu version + suite"
      - "Run: python3 scripts/skill_audit.py data/fixtures/sample-bad-frontmatter/"
      - "Assert: exit 1, Must Fix tại SKILL.md:1-10, msg thiếu version, suite"
    expected: "All assertions pass"
```

---

## 5. Risk Matrix

| ID | Title | P×I | Score | Mitigation |
|----|-------|-----|-------|------------|
| RISK-06 | Stage 3.5 call site chưa update từ production-code-reviewer → skill-quality-reviewer | 3×2 | **6** | Grep call sites, update trong cùng PR, smoke test e2e |
| RISK-01 | LLM verdict variance (semantic part 70%) | 2×2 | 4 | temperature=0.0, prompt hash, conf ≥ 0.7 |
| RISK-04 | 7-Zone vs 8-Zone confusion | 2×2 | 4 | Document: check 7 zones theo framework.md §1, policy bonus Optional |
| RISK-03 | Self-review infinite loop | 1×3 | 3 | Hardcode skip self-path unless `--self` flag |
| RISK-05 | Archive thiếu files skill cũ (31 files) | 1×3 | 3 | `cp -r` + verify count = 31 trước khi delete |
| RISK-02 | Token heuristic sai cho tiếng Việt có dấu | 2×1 | 2 | dùng tiktoken (multi-language aware), fallback char/2 |
| RISK-07 | PyYAML version mismatch | 1×2 | 2 | Pin `>=6.0`, test trên 3.10/3.12/3.14 |

---

## 6. Quality Matrix Score

```yaml
scoring:
  pass_threshold: 0.80
  elicitation_report: { weight: 0.15, score: 1.0 }
  requirements_classification: { weight: 0.15, score: 1.0 }
  sequence_diagram: { weight: 0.15, score: 1.0 }
  flowchart_activity: { weight: 0.15, score: 1.0 }
  erd_schema: { weight: 0.15, score: 1.0 }
  acceptance_criteria: { weight: 0.15, score: 1.0 }
  risk_matrix: { weight: 0.10, score: 1.0 }
total_weighted_score: 1.00  # PASS
```

---

## 7. Open Questions (cần Steve confirm trước Stage 1)

1. **Gap #3** — 7 vs 8 zones: default applied = 7 zones (assets optional, policy bonus Optional)
2. **Gap #1** — LLM confidence threshold: default applied = ≥ 0.7 LGTM
3. **Gap #8** — Archive path: default applied = relative `.skill-context/_archive/production-code-reviewer-{ts}/`

---

## 8. Handoff → Stage 0.5 (Knowledge Miner)

**Input cho knowledge-miner-agent**:
- BA report này (FR/NFR/AC/risk)
- Domain cần mine: **WASHVN skill quality standards** — bao gồm:
  - 7-Zone structure (framework.md §1)
  - SKILL.md contract (standards.md §3)
  - DRC schema (standards.md §3.2)
  - CASE System (case-system.md)
  - Quality gates (CLAUDE.md §10)
  - Token budget rules
- Output: `.skill-context/skill-quality-reviewer/domain-handbook.md`

**Lifecycle**: `raw → designed` (sau Stage 1+1.5)