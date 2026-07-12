---
feature_name: upvote-board
business_context: "Lightweight feature-request board: users submit requests, other users upvote to signal demand, ranked by vote count, with spam moderation."
status: completed
elicited_at: "2026-07-11"
---

# BA Elicitation Report — upvote-board

## 1. Stakeholders
- `[TỪ INPUT]` End User (submitter + voter): wants fast, credible ranking of ideas.
- `[TỪ INPUT]` Moderator (Community Manager): must remove spam/duplicate without bias.
- `[SUY LUẬN]` Product Owner: consumes ranked list to prioritize roadmap.
- `[SUY LUẬN]` Security Reviewer: prevents vote-fraud / sybil attacks.

## 2. Goals
- `[TỪ INPUT]` Collect feature requests in one place.
- `[TỪ INPUT]` Let users upvote to express demand.
- `[SUY LUẬN]` Surface top requests by net votes, with recency tie-breaker.

## 3. Functional Requirements
- FR-001 (P1) Submit request: title (<= 120 chars), body (<= 2000 chars), author_id. `[TỪ INPUT]`
- FR-002 (P1) Upvote / remove-upvote (toggle), one vote per user per request. `[TỪ INPUT]`
- FR-003 (P1) List requests sorted by net votes desc, then created_at desc. `[SUY LUẬN]`
- FR-004 (P2) Search by keyword (title/body). `[CẦN LÀM RÕ]` — fuzzy vs exact?
- FR-005 (P2) Moderator delete request (spam/duplicate) with reason log. `[SUY LUẬN]`
- FR-006 (P3) Comment thread per request. `[SUY LUẬN]` — out-of-scope candidate.
- FR-007 (P2) Duplicate-merge: link two requests, sum votes. `[SUY LUẬN]`

## 4. Non-Functional Requirements
- NFR-001 (performance) List endpoint p95 latency < 300ms at 10k requests. `[SUY LUẬN]`
- NFR-002 (security) Prevent multi-vote by same user: unique(user_id, request_id). `[SUY LUẬN]`
- NFR-003 (scalability) Support 50k requests, 1M votes without degradation. `[SUY LUẬN]`
- NFR-004 (availability) 99.5% monthly uptime for read path. `[CẦN LÀM RÕ]`

## 5. Implicit Requirements / Assumptions
- assumption: Auth already exists; upvote-board consumes user_id from session. `[SUY LUẬN]` confidence: medium
- assumption: Soft-delete (is_deleted flag), not hard delete, for audit. `[SUY LUẬN]` confidence: high
- assumption: Votes are integers, no weighting by user reputation (v1). `[SUY LUẬN]` confidence: high

## 6. Must-Not Rules (negative space)
- scenario: A user casts more than one vote on the same request. consequence: rejected with 409, no duplicate row.
- scenario: Deleted request still appears in ranked list. consequence: filtered out of public list.
- scenario: Moderator deletes request without logging reason. consequence: action rejected (reason required).
- scenario: Unauthenticated user submits/votes. consequence: 401, no write.

## 7. Unknowns
- `[CẦN LÀM RÕ]` Downvote support? (currently upvote-only)
- `[CẦN LÀM RÕ]` Pagination size / infinite scroll vs page numbers.
- `[CẦN LÀM RỖ]` Vote change history retention window.

## 8. Defensive Reasoning (reverse probes)
- probe: "What if two users submit identical requests?" finding: FR-007 duplicate-merge needed; else vote-splitting dilutes signal.
- probe: "What if a bot farms votes?" finding: NFR-002 + rate-limit on vote endpoint (suggest 1 vote / 2s / user).
- probe: "What if request volume spikes post-launch?" finding: NFR-003 read-path must be cacheable (ranking snapshot TTL 60s).
