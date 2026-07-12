---
derived_from: .skill-context/upvote-board/ba-elicitor/elicitation-report.md
feature_name: upvote-board
status: completed
analyzed_at: "2026-07-11"
---

# BA Analysis Report — upvote-board

## 1. Requirements Catalog

### Functional
- FR-001 (category: api) Submit request {title<=120, body<=2000, author_id}. deps: [] priority: P1
  priority_rationale: "Core write path; nothing works without submission."
  acceptance_criteria:
    - "POST /requests with valid auth + body returns 201 + request_id."
    - "Title > 120 chars or empty body returns 422."
- FR-002 (category: api) Upvote toggle, one vote per user per request. deps: [FR-001] priority: P1
  priority_rationale: "Defines the value proposition (demand signal)."
  acceptance_criteria:
    - "POST /requests/{id}/vote toggles vote; second call removes it."
    - "Same user double-vote rejected with 409, zero duplicate rows."
- FR-003 (category: api) List sorted by net votes desc, created_at desc. deps: [FR-001, FR-002] priority: P1
  priority_rationale: "Primary read surface; ranking is the product."
  acceptance_criteria:
    - "GET /requests returns items ordered by votes desc then created_at desc."
    - "Deleted requests excluded from list."
- FR-004 (category: ux) Keyword search title/body. deps: [FR-003] priority: P2
  priority_rationale: "Discoverability; not launch-blocking."
  acceptance_criteria:
    - "GET /requests?q=foo returns substring matches (case-insensitive)."
- FR-005 (category: security) Moderator delete with reason log. deps: [FR-001] priority: P2
  priority_rationale: "Spam control; needs audit trail."
  acceptance_criteria:
    - "DELETE /requests/{id} by moderator with reason=>soft-delete + audit row."
    - "Missing reason returns 422; non-moderator returns 403."
- FR-007 (category: ux) Duplicate-merge links two requests, sums votes. deps: [FR-001, FR-002] priority: P2
  priority_rationale: "Prevents vote-splitting dilution."
  acceptance_criteria:
    - "POST /requests/merge {from,to} reassigns votes to `to`, marks `from` merged."

### Non-Functional
- NFR-001 (category: performance) List p95 < 300ms @ 10k req. acceptance_criteria: ["Load test 10k RPS: p95 list latency <= 300ms."] verification_method: automated
- NFR-002 (category: security) Unique(user_id, request_id) enforced. acceptance_criteria: ["DB unique constraint + app guard; no duplicate vote row under concurrent load."] verification_method: automated
- NFR-003 (category: scalability) 50k req / 1M votes no degradation. acceptance_criteria: ["Ranking snapshot cached TTL 60s; read path stateless."] verification_method: review
- NFR-004 (category: availability) Read path 99.5% monthly uptime. acceptance_criteria: ["SLO dashboard; cached ranking tolerates 60s DB blip."] verification_method: automated

## 2. Priority Matrix
- p1: [FR-001, FR-002, FR-003]
- p2: [FR-004, FR-005, FR-007, NFR-001, NFR-002, NFR-003, NFR-004]
- p3: [FR-006]  # commented out — deferred to v2

## 3. Dependency Graph
- {from: FR-002, to: FR-001, type: requires}
- {from: FR-003, to: FR-002, type: requires}
- {from: FR-004, to: FR-003, type: requires}
- {from: FR-007, to: FR-002, type: requires}
- {from: FR-005, to: FR-001, type: requires}

## 4. Risks
- risk: "Vote-fraud / sybil (bot farms votes)" impact: high mitigation: "NFR-002 unique constraint + rate-limit 1 vote/2s/user + moderator review queue."
- risk: "Vote-splitting via duplicate requests" impact: medium mitigation: "FR-007 merge; moderator dup-detection on submit (title similarity warn)."
- risk: "Ranking staleness under burst" impact: medium mitigation: "NFR-003 cached snapshot TTL 60s; invalidation on new vote."
- risk: "Hard-delete breaks audit" impact: medium mitigation: "Soft-delete flag (assumption confirmed high confidence)."
