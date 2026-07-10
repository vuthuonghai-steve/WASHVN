---
name: "ba-synthesizer"
description: "Hợp nhất và kiểm định chéo output từ ba-elicitor và ba-analyst, tính quality score weighted sum, xác nhận pipeline readiness cho Phase 6."
suite: "WASHVN"
version: "0.0.1"
category: "general"
stage: -0.2
target_variable: "feature_name"
tags: ["ba", "synthesis", "cross-validation", "quality-gate", "business-analysis"]
when_to_use: "Khi cần hợp nhất và kiểm định chéo output từ ba-elicitor và ba-analyst, tạo business-analysis.md cho Phase 6 (skill-explorer)."
output_contract: "skills/ver-3/_shared/templates/drc_contract_template.yaml"
hooks:
  PreToolUse:
    - matcher: "Write"
      hooks:
        - type: command
          command: "bash skills/ver-3/ba-synthesizer/scripts/hooks/ba-write-confinement.sh"
    - matcher: "Task"
      hooks:
        - type: command
          command: "bash skills/ver-3/ba-synthesizer/scripts/hooks/anti-recursion.sh"
  Stop:
    hooks:
      - type: prompt
        prompt: "Check business-analysis.md: tồn tại, valid YAML frontmatter, 4 required fields (skill_name, synthesized_requirements, congruence_check, pipeline_ready), congruence_check.PASS, pipeline_ready boolean, no placeholder, quality_score ≥ 80"
        model: "claude-3-5-haiku"
        continueOnBlock: true
---

# BA Synthesizer — Skill Description

<instructions>
Persona: Meta-Generator / Senior Business Analyst. Bạn là **cổng quality gate cuối cùng** của BA Pipeline (Stage BA-0.2), nhận input từ `ba-elicitor` + `ba-analyst`, sinh `business-analysis.md` (WORM) cho Phase 6. KHÔNG chạy thử / simulate runtime — output là file artifact. Tuân thủ 7 nguyên lý LLM: domain anchoring (BABOK, ISO/IEC 25010, MoSCoW, FMEA), semantic > ceremony, dual knowledge stream, binary mechanical gates, negative space (warning tags), graceful degradation (WARNING ≠ FAIL).
</instructions>

<safety_contract>
WORM write: chỉ ghi `.skill-context/{feature}/ba-synthesizer/business-analysis.md`. No placeholder (TODO/TBD/mock/...) — FAILED nếu có. Quality score deterministic (weighted sum), KHÔNG dùng NLP/subjective. Internal threshold **≥ 0.80** (KHÔNG giảm xuống 0.70). Congruence FAIL → block pipeline. Token limit SKILL.md ≤ 1500 words.
</safety_contract>

<knowledge_anchors>
- `knowledge/cross_validation_strategies.md` — §1 Cross-Ref Rules, §2 Quality Criteria & Weighted Scoring, §3 Trace Tags.
- `skills/ver-3/_shared/schemas/synthesis.schema.yaml` — output contract (4 required fields, additionalProperties:false).
- `loop/congruence_checklist.md` — 14 items (7 completeness + 5 validation + 2 format).
- `templates/business_analysis_template.md` — 6-field frontmatter + 4 sections.
</knowledge_anchors>

<workflow_phases>
4-phase chain. Mỗi phase check gate trước khi sang bước sau:

[CROSS-VALIDATE] — Rule 1: Actor-Entity Matching (Sequence Diagram ↔ ERD). Rule 2: MoSCoW-Gherkin Matching (Must-Have ↔ Gherkin). Warning tags: `[MAU THUẪN NGHIỆP VỤ]`, `[THIẾU KỊCH BẢN KIỂM THỬ]`.
    ↓
[SCORE] — 7 deliverables × weights (0.15×6 + 0.10×1). `weighted_sum = Σ(score_i × weight_i)`. ≥ 0.80 = PASS, < 0.80 = WARNING. Barem nhị phân 1.0/0.5/0.0 (tham khảo §2).
    ↓
[SYNTHESIZE] — Merge elicitation + analysis → consolidated requirements. Deduplicate, cross-reference trace tags (`[TỪ INPUT]`/`[SUY LUẬN]`/`[CẦN LÀM RÕ]`). Map vào `synthesized_requirements[]` (req_id, title, description, source, classification).
    ↓
[VERIFY] — 14-item congruence checklist (ALL completeness + format MUST pass). `python scripts/check_congruence.py --artifact business-analysis.md`. `pipeline_ready = (no blocking defect AND quality ≥ 80% AND congruence PASS)`.

Write: `.skill-context/{feature}/ba-synthesizer/business-analysis.md` (WORM).
Validate: `python skills/ver-3/_shared/validators/schema_validator.py --path business-analysis.md --schema skills/ver-3/_shared/schemas/synthesis.schema.yaml` → exit 0.
</workflow_phases>

<input_contract>
- `elicitation-report.md` (required) — `.skill-context/{feature}/ba-elicitor/elicitation-report.md`, status `completed`.
- `analysis-report.md` (required) — `.skill-context/{feature}/ba-analyst/analysis-report.md`, status `completed`.
- `thought-cache.yaml` (optional) — `.skill-context/{feature}/ba-elicitor/thought-cache.yaml`.
</input_contract>

<output_contract>
- `business-analysis.md` (WORM) — `.skill-context/{feature}/ba-synthesizer/business-analysis.md`.
- Frontmatter CHỈ 4 keys schema-allowed: `skill_name`, `synthesized_requirements[]`, `congruence_check{conflicts_found,conflicts_resolved,check_verdict}`, `pipeline_ready`.
  + `synthesized_requirements[].source ∈ [elicitation,analysis,both]`, `classification ∈ [FR,NFR]`.
- Template-level handoff metadata (target_skill, scs_complexity_score, quality_gate_status, quality_score_percentage) → phần thân §2/§4, KHÔNG frontmatter (schema additionalProperties:false).
- Downstream consumer: `skill-explorer` (Phase 6).
</output_contract>

<acceptance_criteria>
- QG-SYN-01: Cross-validation Actor-Entity — không `[MAU THUẪN NGHIỆP VỤ]` unresolved.
- QG-SYN-02: Cross-validation MoSCoW-Gherkin — không `[THIẾU KỊCH BẢN KIỂM THỬ]` unresolved.
- QG-SYN-03: Quality score weighted sum ≥ 0.80.
- QG-SYN-04: Congruence checklist 14 items ALL completeness+format pass.
- QG-SYN-05: pipeline_ready boolean chính xác (true chỉ khi quality ≥ 80% AND congruence PASS).
- `check_congruence.py` 8/8 PASS (C1-C8) + `schema_validator.py` exit 0.
</acceptance_criteria>

<failure_modes>
- **F22 Missing artifact**: elicitation/analysis-report không tồn tại → báo lỗi, không sinh output.
- **F23 Schema fail**: frontmatter thiếu key / sai kiểu → chạy lại schema_validator, sửa trước khi ghi.
- **F24 Quality < 80%**: weighted sum < 0.80 → WARNING, không set pipeline_ready=true.
- **F25 Unresolved conflict**: congruence FAIL → block pipeline, escalate ba-elicitor (re-elicit).
</failure_modes>
