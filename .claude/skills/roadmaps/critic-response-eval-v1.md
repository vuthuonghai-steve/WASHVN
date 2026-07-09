# Roadmap Evaluation v1 → Roadmap Patch v1.1 — Independent Critic-of-Critic Response

> **Date:** 2026-07-04
> **Position:** Architectural critic-of-critic (đánh giá độc lập về evaluation)
> **Subject:** Phân biện các đề xuất trong `../../../../roadmap_evaluation.md`

---

## Tổng quan phản biện

Evaluation external độc lập gợi ý 7 improvements cho roadmap v1.0. Sau khi đối chiếu từng đề xuất với roadmap thực tế (đọc trực tiếp 3 file liên quan: 00, 06, 08), phán xét ứng xử đề xuất như sau:

| # | Đề xuất | Decision | Rationale |
|---|---|---|---|
| 1 | Phase 6 split → 6A + 6B với verify checkpoint giữa | ✅ ACCEPT | Chia giảm XL bottleneck, catch design-side errors trước codegen |
| 2 | Hysteresis re-eval cap = 1 (cho Γ-3) | ✅ ACCEPT (CRITICAL FIX) | Phase 6 original ghi "mandatory re-eval" mà không có max iteration — blind spot thực sự của tôi |
| 3 | Docker AC-8 tại Phase 0 | ✅ ACCEPT | Phase 0 chỉ "verify path"; check daemon+permission+disk early tránh 7 phases rollback |
| 4 | Escalation `escalation_report.yaml` traceback đầy đủ (cho Γ-7) | ✅ ACCEPT | Exit 2 với stderr chung chung không đủ context cho human/oracle triage |
| 5 | Pruning → Summarization cho fallback history (cho Γ-2) | ✅ ACCEPT (CRITICAL FIX) | Hard pruning cứng = mất ký ức LLM về lỗi cũ → lặp lỗi. Summarization (15 cũ → 1 line + 5 close-detail) là best of both |
| 6 | WARNING → toast notification cho user (cho Γ-1) | ⚠️ PARTIAL PUSHBACK | Đây là IDE concern không phải roadmap design — WARNING log + dashboard đủ. Roadmap không define IDE features |
| 7 | Race conditions hook parallel — concern raised | ⚠️ PUSHBACK | Hooks serialized theo Claude Code's tool invocation model; parallel chỉ khi nhiều agents cùng invoke (Phase 3 problem, không Phase 2) |

**Tỷ lệ accept:** 5/7 (71% incorporate into roadmap v1.1) — 2 pushback với lý do technical.

---

## Phân tích chi tiết

### Decision 1 — Phase 6 Split (accept)

**Evaluation nhận định**: Phase 6 XL bottleneck;-split 6A (Explorer, Miner, Architect, Gatekeeper) + 6B (Planner, Builder, Reviewer) giảm tải và dễ verify từng cụm.

**Phán exercised**: Đúng. Critical path pipeline là Phase 6 → 7 → 8, và Phase 6 chiếm ~660 dòng roadmap — double any other phase. Chia 6A/6B cho checkpoint giữa = quality-matrix.yaml của 4 skills 6A phải PASS ≥80% trước khi 6B bắt đầu. Đây là structural change, không chỉ cosmetic.

**Patch applied**:
- `[roadmaps/06-skill-build-main-pipeline.md]` thêm "Phase 6 sub-split" section sau mục đích, đảo table 6A vs 6B với verify checkpoint
- `[roadmaps/index.md]` table stage updated: 6 → 6A + 6B với dependency giữa

### Decision 2 — Hysteresis Re-eval Cap = 1 (CRITICAL accept)

**Evaluation nhận định**: Phase 6 hiện ghi "mandatory re-eval" không có max iteration → infinite loop Explorer↔Gatekeeper.

**Phán judgment**: **CRITICAL fix chính xác**. Đây là lỗi thực sự của tôi. Ban đầu tôi rackups re-eval mechanism nhưng không capping nó — một design defect khác liên quan đến (Γ-7) escalation recursion mà tôi đã note nhưng không apply vào Γ-3 fix.

**Patch applied**:
- `skill-explorer/SKILL.md` workflow: thêm "Re-eval cap = 1" + "post-cap default to Branch B (conservative)"
- `factual` reference table YAML thêm `max_re_eval_cap: 1` + `post_cap_rule`
- `acceptance Criteria` thêm field `re_eval_count` (int, default 0, max 1)
- `[roadmaps/08]` A2 patch — Gatekeeper branch on `re_eval_count` values để enforce cap

### Decision 3 — Docker AC-8 (accept)

**Evaluation nhận định**: Phase 0 chỉ "verify path"; check daemon/permissions/disk early tránh late discovery tại Phase 7.

**Patch applied**:
- `[roadmaps/00]` new AC-8 với 6 sub-checks: CLI exists, daemon running, user permission (no sudo needed), disk ≥1GB, optional network, hello-world test
- Cho phép PASS_WITH_WARNING (user not in docker group but has sudo) — graceful degradation
- Updated DoD to "AC-1 to AC-8 PASS (AC-8 cho phép PASS_WITH_WARNING)"

### Decision 4 — Escalation_report.yaml traceback (accept)

**Evaluation nhận định**: Exit 2 stderr chung chung không đủ; cần structured artifact.

**Patch applied**:
- `[roadmaps/08]` A4 — Stop hook exit 2 generates `escalation-report-YYYYMMDD-HHMMSS.yaml` với fields: triggered_at, escalation_depth, pipeline_phase, failure_summary, previous_escalations (5 last entries), action_required, recommended_recovery
- State schema `escalation` block thêm `last_triggered_at`, `last_failure_summary` để script có thể reference

### Decision 5 — Pruning → Summarization (CRITICAL accept)

**Evaluation nhận định**: Hard pruning 20 entries = LLM loses memory of old errors → can reproduce same error thinking it's new existence. Đề xuất summarize 15 oldest, keep 5 close-detail.

**Patch applied**:
- `[roadmaps/08]` A6 — replaces "max_history_entries: 20 hard cap" với policy `summarize`:
  - soft_cap: 20 (above trigger summarization)
  - detailed_recent: 5 (preserve full detail)
  - summarize_oldest: 15 (compress to summary lines)
  - summary_format: "{count} lần fallback ở Phase {phase_code} do {error_pattern}, all failed"
- Entry type field distinguish raw (5 recent) vs summary entries
- Test: 30+ fallbacks → verify 5 raw + ≤15 summary = ≤20 total

### Decision 6 — Toast Notification (partial pushback)

**Evaluation nhận định**: User cần visual cue (toast/notification) về WARNING states.

**Phán xét của tôi**: Đây là IDE-level concern, không phải roadmap design concern. Roadmap định nghĩa **what to verify and how**, không define view rendering. WARNING log vào audit (đã có trong file `tool-audit-YYYY-MM-DD.log`) + dashboard column trong `index.md` là đủ context cho user khi read.

Accept đưa WARNING vào state dashboard, pushback rằng toast implementation là decision của IDE plugin/Claude Code team.

**Patch applied**: Log note trong `[roadmaps/index.md]` acknowledgment "Toast notification là IDE concern outside roadmap scope — audit log + index.md dashboard suffices".

### Decision 7 — Race Conditions (pushback)

**Evaluation nhận định**: Multi-agents ghi song song `_state.yaml` có thể race.

**Phán xét của tôi**: Trong Claude Code's tool invocation model, hooks là **serialized** theo call sequence (mỗi tool trigger một hook, cùng task sequence). Multi-agent parallel chỉ khi các agents spawn — và khi đó, mỗi agent có session riêng. `_state.yaml` shared write là Phase 3 multi-agent concern (đã có note trong subagent-forge pattern — block recursive), không phải Phase 2 hook concern.

Accept log note vào Phase 8 về risk này để re-evaluate nếu Phase 3 multi-agent tests surface issues.

**Patch applied**: Note trong `[roadmaps/index.md]` Pushback section: "Race Conditions: hooks serialized; parallel concern is Phase 3 problem, logged-not-escalated".

---

## Tóm tắt hành động patch

| File | Lines added | Patch content |
|---|---|---|
| `roadmaps/00-foundation-bootstrap.md` | ~30 | AC-8 Docker checks + header patch + DoD update |
| `roadmaps/06-skill-build-main-pipeline.md` | ~20 | Sub-split 6A/6B + hysteresis cap=1 in workflow + reference YAML + acceptance criteria + header patch |
| `roadmaps/08-integration-tests-hardening.md` | ~80 | A2 (hysteresis cap with Gatekeeper branch on re_eval_count) + A4 (escalation_report.yaml generation) + A6 (summarization replace pruning) + header patch |
| `roadmaps/index.md` | ~40 | Acknowledgment block + 6A/6B table + verification dashboard updated |

**Tổng cộng:** ~170 dòng bổ sung trên ~4366 dòng baseline (3.9% size increase).

---

## Tình trạng Roadmap sau Patch v1.1

Roadmap strengthened:
- ✅ Hidden infinite loop at Γ-3 closed (re-eval cap)
- ✅ XL effort bottleneck at Phase 6 split into 2 verify-checkpoint sub-phases
- ✅ Late discovery risk at Phase 7 (Docker) shifted to Phase 0 (early detection)
- ✅ Uninformative halt protocol (exit 2 stderr) → structured escalation_report.yaml với traceback
- ✅ Lossy state pruning → memory-preserving summarization
- ⚠️ Acceptable tensions remain: IDE notification features phóo cho Claude Code team; race condition note logged for Phase 3 re-evaluation

**Risk profile giảm**: 1 critical (infinite loop), 2 high (XL bottleneck, late discovery), 1 medium (uninformative halt), 1 medium (lossy prune) = 5 risks mitigated.

**No new critical issues introduced by patches**.

---

## Liên kết

- [Roadmap evaluation v1](../../../../roadmap_evaluation.md)
- [Roadmap v1.1 (updated index)](../../../Temps/spec/roadmaps/index.md)
- [Phase 0 updated](../../../Temps/spec/roadmaps/00-foundation-bootstrap.md)
- [Phase 6 updated](../../../Temps/spec/roadmaps/06-skill-build-main-pipeline.md)
- [Phase 8 updated](../../../Temps/spec/roadmaps/08-integration-tests-hardening.md)