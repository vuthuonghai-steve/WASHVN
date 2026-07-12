---
derived_from:
  - .skill-context/upvote-board/ba-elicitor/elicitation-report.md
  - .skill-context/upvote-board/ba-analyst/analyst-output.md
feature: upvote-board
status: completed
pipeline_ready: true
quality_score_percentage: 92
---

# Business Analysis — upvote-board

## 1. Executive Summary
The upvote-board is a lightweight demand-signaling surface: users submit feature requests (FR-001), express demand via a one-vote-per-user toggle (FR-002), and consume a live ranking sorted by net votes with recency tie-break (FR-003). It targets product teams that need credible, crowd-sourced prioritization without heavyweight forum tooling. Moderators keep the board clean through reason-logged soft-deletes (FR-005) and duplicate-merge (FR-007) to prevent vote-splitting. Non-functional guardrails center on read-path performance (p95 < 300ms @ 10k RPS), vote-integrity (unique constraint), and 99.5% read availability via a 60s cached ranking snapshot. The v1 scope deliberately excludes comments (FR-006) and downvotes, both deferred pending signal.

## 2. Scope
- in_scope: [submit request, upvote toggle, ranked list, keyword search, moderator delete+audit, duplicate merge]
- out_of_scope: [comment threads (FR-006 v2), downvotes, user reputation weighting]
- assumptions: [auth/session provides user_id, soft-delete for audit, integer votes only v1]

## 3. Requirements Summary
- total: 10
- functional: 6
- non_functional: 4
- p1_count: 3

## 4. Traceability Matrix
- requirement_id: FR-001
  source_elicitation: "FR-001 submit request [TỪ INPUT]"
  acceptance_criteria: ["201 + request_id on valid POST", "422 on title>120/empty body"]
  test_scenario: "Authed user POST valid request → 201; POST oversized title → 422."
- requirement_id: FR-002
  source_elicitation: "FR-002 upvote toggle [TỪ INPUT]"
  acceptance_criteria: ["toggle on 2nd call removes vote", "409 + zero dup rows on double-vote"]
  test_scenario: "User votes twice concurrently → exactly one row; 2nd call deletes it."
- requirement_id: FR-003
  source_elicitation: "FR-003 sorted list [SUY LUẬN]"
  acceptance_criteria: ["votes desc then created_at desc", "deleted excluded"]
  test_scenario: "Seed 3 requests with mixed votes/times → list order matches rule; deleted hidden."
- requirement_id: FR-004
  source_elicitation: "FR-004 keyword search [CẦN LÀM RÕ]"
  acceptance_criteria: ["case-insensitive substring match"]
  test_scenario: "q=Auth returns requests containing 'auth' anywhere in title/body."
- requirement_id: FR-005
  source_elicitation: "FR-005 moderator delete [SUY LUẬN]"
  acceptance_criteria: ["soft-delete + audit row", "422 missing reason / 403 non-mod"]
  test_scenario: "Moderator DELETE with reason → is_deleted=true + audit; without reason → 422."
- requirement_id: FR-007
  source_elicitation: "FR-007 duplicate merge [SUY LUẬN]"
  acceptance_criteria: ["votes reassigned to `to`, `from` marked merged"]
  test_scenario: "Merge req A→B → B vote count = A+B; A hidden + merged flag."
- requirement_id: NFR-001
  source_elicitation: "NFR-001 p95<300ms [SUY LUẬN]"
  acceptance_criteria: ["load test 10k RPS p95<=300ms"]
  test_scenario: "k6 10k RPS sustained → p95 list latency <= 300ms."
- requirement_id: NFR-002
  source_elicitation: "NFR-002 unique vote [SUY LUẬN]"
  acceptance_criteria: ["no dup row under concurrent load"]
  test_scenario: "100 concurrent votes same (user,request) → exactly 1 row."
- requirement_id: NFR-003
  source_elicitation: "NFR-003 scale 50k/1M [SUY LUẬN]"
  acceptance_criteria: ["cached snapshot TTL 60s, stateless read"]
  test_scenario: "Ranking read served from cache; DB blip 60s tolerated."
- requirement_id: NFR-004
  source_elicitation: "NFR-004 99.5% uptime [CẦN LÀM RÕ]"
  acceptance_criteria: ["SLO dashboard; cache absorbs DB blip"]
  test_scenario: "Synthetic read check 30d → availability >= 99.5%."

## 5. Cross-Validation
- consistency_checks:
  - {check: "FR priority vs dependency (P1 FR-001/002/003 form chain)", result: PASS, detail: "no P1 depends on P2-only."}
  - {check: "FR↔NFR coverage (vote integrity NFR-002 backs FR-002)", result: PASS, detail: "unique constraint maps to toggle."}
  - {check: "Scope exclusion FR-006 not in any dependency", result: PASS, detail: "deferred cleanly, no dangling ref."}
  - {check: "Duplicate-merge vs ranking (FR-007 + FR-003)", result: PASS, detail: "merged requests excluded from list, votes summed."}
- known_gaps:
  - "[CẦN LÀM RÕ] Downvote support undecided — upvote-only v1."
  - "[CẦN LÀM RÕ] Pagination strategy (page vs infinite scroll)."
  - "[CẦN LÀM RÕ] Vote history retention window."

## 6. Recommendations
- recommendation: "Ship FR-001/002/003 + NFR-001/002 as v1 MVP." rationale: "core demand-signal loop; everything else is enhancement." priority: P1
- recommendation: "Add moderator dup-detection on submit (title similarity warn) before FR-007 heavy merge UX." rationale: "cheaper prevention than cleanup." priority: P2
- recommendation: "Defer FR-006 comments to v2." rationale: "not needed to validate demand hypothesis." priority: P3
