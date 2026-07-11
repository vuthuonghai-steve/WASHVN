---
skill_name: "user-auth"
synthesized_requirements:
  - req_id: "REQ-01"
    title: "Email/Password Login"
    description: "Verify email+hash, issue access(15m)+refresh(7d) tokens."
    source: "elicitation"
    classification: "FR"
  - req_id: "REQ-02"
    title: "Google OAuth Login"
    description: "Federated login via Google, link/create account, issue tokens."
    source: "elicitation"
    classification: "FR"
  - req_id: "REQ-03"
    title: "MFA TOTP"
    description: "Enroll + verify TOTP, P1 security priority."
    source: "both"
    classification: "FR"
  - req_id: "REQ-04"
    title: "Session & Refresh Rotation"
    description: "Rotate refresh token each use; access 15min; revoke API."
    source: "analysis"
    classification: "FR"
  - req_id: "REQ-05"
    title: "Password Reset"
    description: "Email link, single-use token, 1h TTL."
    source: "both"
    classification: "FR"
  - req_id: "REQ-06"
    title: "Rate-limit & Lockout"
    description: "5 fails → 15min lockout, per-account + per-IP."
    source: "both"
    classification: "FR"
  - req_id: "REQ-07"
    title: "Auth Latency"
    description: "p95 ≤ 2000ms."
    source: "analysis"
    classification: "NFR"
  - req_id: "REQ-08"
    title: "Token TTL Policy"
    description: "Access 15min, refresh 7d, reset 1h."
    source: "elicitation"
    classification: "NFR"
congruence_check:
  conflicts_found: false
  conflicts_resolved: true
  check_verdict: "PASS"
pipeline_ready: true
---

> **Metadata (template-level handoff, KHÔNG thuộc frontmatter schema):**
> ```yaml
> target_skill: "skill-explorer"
> scs_complexity_score: 7.0
> quality_gate_status: "PASS"
> quality_score_percentage: 100
> pipeline_ready: true
> ```
> `schema_ref: "synthesis.schema.yaml"` · `artifact_lifecycle: "WORM"`

# Báo Cáo Tổng Hợp Nghiệp Vụ: user-auth

## §1: Cross-Reference Validation Results

### 1A. Actor-Entity Matching
- Trạng thái: PASS `[TỪ ELICITATION]`
- Actor: 5 (User, Client, Auth, DB, Google) · Entity: 3 (USER, SESSION, OAUTH_LINK) · Matching rate: 100%
- **Cảnh báo:** None.

### 1B. MoSCoW-Gherkin Matching
- Trạng thái: PASS `[TỪ ANALYSIS]`
- MoSCoW items: 10 · Gherkin scenarios: 3 (Happy/Alt/Exception)
- **Cảnh báo:** None. `[THIẾU KỊCH BẢN KIỂM THỬ]` không phát hiện.

### 1C. Congruence Check Verdict
```yaml
congruence_check:
  conflicts_found: false
  conflicts_resolved: true
  check_verdict: "PASS"
```

## §2: Quality Score Assessment

### 2A. Deliverable Scores (0.0–1.0)

| Mã | Deliverable | Trọng số | Score |
|:---|:------------|:--------:|:-----:|
| BA-DEL-01 | Elicitation Report & Thought Cache | 0.15 | 1.0 |
| BA-DEL-02 | Classification & MoSCoW Matrix | 0.15 | 1.0 |
| BA-DEL-03 | Sequence Diagram | 0.15 | 1.0 |
| BA-DEL-04 | Flowchart Diagram | 0.15 | 1.0 |
| BA-DEL-05 | Entity Relationship Diagram (ERD) | 0.15 | 1.0 |
| BA-DEL-06 | Gherkin Acceptance Criteria | 0.15 | 1.0 |
| BA-DEL-07 | Risk Assessment Matrix | 0.10 | 1.0 |

### 2B. Weighted Sum
```yaml
quality_score:
  weights:
    BA-DEL-01: 0.15
    BA-DEL-02: 0.15
    BA-DEL-03: 0.15
    BA-DEL-04: 0.15
    BA-DEL-05: 0.15
    BA-DEL-06: 0.15
    BA-DEL-07: 0.10
  weighted_sum: 1.0
  percentage: 100%
```

### 2C. Quality Gate Verdict
- **PASS** (100% ≥ 80%).

## §3: Consolidated Requirements

```yaml
synthesized_requirements:
  - req_id: "REQ-01"
    title: "Email/Password Login"
    description: "Verify email+hash, issue access(15m)+refresh(7d) tokens."
    source: "elicitation"
    classification: "FR"
  - req_id: "REQ-02"
    title: "Google OAuth Login"
    description: "Federated login via Google, link/create account, issue tokens."
    source: "elicitation"
    classification: "FR"
  - req_id: "REQ-03"
    title: "MFA TOTP"
    description: "Enroll + verify TOTP, P1 security priority."
    source: "both"
    classification: "FR"
  - req_id: "REQ-04"
    title: "Session & Refresh Rotation"
    description: "Rotate refresh token each use; access 15min; revoke API."
    source: "analysis"
    classification: "FR"
  - req_id: "REQ-05"
    title: "Password Reset"
    description: "Email link, single-use token, 1h TTL."
    source: "both"
    classification: "FR"
  - req_id: "REQ-06"
    title: "Rate-limit & Lockout"
    description: "5 fails → 15min lockout, per-account + per-IP."
    source: "both"
    classification: "FR"
  - req_id: "REQ-07"
    title: "Auth Latency"
    description: "p95 ≤ 2000ms."
    source: "analysis"
    classification: "NFR"
  - req_id: "REQ-08"
    title: "Token TTL Policy"
    description: "Access 15min, refresh 7d, reset 1h."
    source: "elicitation"
    classification: "NFR"
```

Tổng: 8 yêu cầu (FR: 6, NFR: 2).

## §4: Pipeline Readiness

```yaml
pipeline_ready: true
```

- **Điều kiện:** elicitation completed `[TỪ ELICITATION]`, analysis completed `[TỪ ANALYSIS]`, quality ≥ 80% `[SUY LUẬN]`.
- **Blocker:** `[CẦN LÀM RÕ]` rate-limit scope (per-account vs per-IP), MFA scope (strict vs adaptive), OAuth fallback — không block pipeline nhưng cần clarify trước Phase 6 implementation.
