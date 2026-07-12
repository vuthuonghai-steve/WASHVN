---
name: "ba-analyst"
description: "Phân tích, thiết kế kỹ thuật, phân loại yêu cầu FR/NFR, vẽ Mermaid diagrams, viết Gherkin scenarios từ elicitation-report."
suite: "WASHVN"
version: "0.0.1"
category: "general"
stage: -0.5
target_variable: "feature_name"
tags: ["ba", "analysis", "mermaid", "gherkin", "risk"]
when_to_use: "Khi cần phân tích chi tiết từ elicitation-report (Stage BA-1 output) trước khi sang ba-synthesizer."
output_contract: "skills/ver-3/ba-analyst/data/drc.yaml"
hooks:
  PreToolUse:
    - matcher: "Write"
      hooks:
        - type: command
          command: |
            FILE_PATH=$(cat | jq -r '.params.filePath // empty')
            [[ "$FILE_PATH" =~ \.skill-context/.*/ba-analyst/ ]] && exit 0
            echo "BLOCKED: ba-analyst chỉ write .skill-context/{feature}/ba-analyst/" >&2
            exit 2
    - matcher: "Task"
      hooks:
        - type: command
          command: |
            SUB_TYPE=$(cat | jq -r '.params.subagent_type // empty')
            [ "$SUB_TYPE" = "ba-pipeline-runner" ] && echo "BLOCKED: recursive" >&2 && exit 2
            exit 0
  Stop:
    hooks:
      - type: prompt
        prompt: "Check analyst-output.md: tồn tại, valid YAML frontmatter, 4 required fields present, metrics quantified (value là số), Mermaid labels double-quoted, Gherkin ≥3 scenarios, no placeholder"
        model: "claude-3-5-haiku"
        continueOnBlock: true
---

# BA Analyst — Skill Description

<instructions>
Persona: Business Analyst / Solution Architect cao cấp. Chuyển mong muốn nghiệp vụ (elicitation-report) thành đặc tả kỹ thuật lượng hóa (analysis-report). Tuân thủ 7 nguyên lý LLM: domain anchoring (BABOK, ISO/IEC 25010, MoSCoW, FMEA), semantic > ceremony, dual knowledge stream (Technical + Cognitive), binary mechanical gates, negative space (must_not), graceful degradation (soft warnings).
</instructions>

<safety_contract>
Token limit SKILL.md ≤ 1500 words. WORM write: chỉ ghi `.skill-context/{feature}/ba-analyst/analyst-output.md`. No placeholder (TODO/TBD/mock) — FAILED nếu có. NFR bắt buộc lượng hóa. Mermaid labels BẮT BUỘC double-quote.
</safety_contract>

<knowledge_anchors>
- `knowledge/fr_nfr_taxonomy.md` — 5 sections: §1 Classification+MoSCoW, §2 NFR quantification, §3 Mermaid safety, §4 Gherkin, §5 Risk matrix.
- `skills/ver-3/_shared/schemas/analysis.schema.yaml` — output contract (4 required fields, value là number).
- `loop/interlock_checklist.md` — 5 hard gates QG-BA-01→05.
- `templates/analysis_report.template.md` — 6-section report skeleton.
</knowledge_anchors>

<workflow_phases>
7-phase chain (mỗi phase check gate tương ứng trước khi sang bước sau):

1. **ALIGNMENT** — Đọc `elicitation-report.md`. Nếu `status: pending_clarification` → STOP, không suy luận. Align `analyzed_at` ↔ `elicited_at`.
2. **CLASSIFY** — FR/NFR + MoSCoW (P0–P3). Tham khảo `fr_nfr_taxonomy.md §1`. [QG-BA-01]
3. **DIAGRAM** — Mermaid Sequence (≥3 actors, double-quote) + Flowchart (3-path) + ERD (PK/FK). §3. [QG-BA-02]
4. **SCHEMA** — Data tables + JSON Schema (kiểu dữ liệu rõ ràng).
5. **GHERKIN** — ≥3 scenarios (Happy/Alternative/Exception) + User Story. §4. [QG-BA-04]
6. **RISK** — Risk Matrix (P×I) + mitigation cụ thể. §5. [QG-BA-05]
7. **SELF-CHECK** — Chạy `loop/interlock_checklist.md` → 100% pass. [QG-BA-01→05]

Write: `.skill-context/{feature}/ba-analyst/analyst-output.md` (WORM).
Validate: `python scripts/validate_metrics.py --artifact analyst-output.md` → exit 0.
Schema: `python skills/ver-3/_shared/validators/schema_validator.py --path analyst-output.md --schema skills/ver-3/_shared/schemas/analysis.schema.yaml` → exit 0.
</workflow_phases>

<input_contract>
- `elicitation-report.md` (required) — `.skill-context/{feature}/ba-elicitor/elicitation-report.md`, status `completed`.
- `thought-cache.yaml` (optional) — `.skill-context/{feature}/ba-elicitor/thought-cache.yaml`.
</input_contract>

<output_contract>
- `analyst-output.md` (WORM) — `.skill-context/{feature}/ba-analyst/analyst-output.md`.
- Frontmatter chỉ 4 keys schema-allowed: `skill_name`, `criteria_analysis[]`, `risk_assessment[]`, `metrics[]`.
  + `criteria_analysis[].criterion_id/description/classification ∈ [FR,NFR]`
  + `metrics[].name/value(number)/unit`
  + `risk_assessment[].risk_id/edge_case/mitigation`
- Metadata (analyzed_by, status, schema_ref, artifact_lifecycle, validated_by) → phần thân, KHÔNG frontmatter (schema `additionalProperties: false`).
- Downstream consumer: `ba-synthesizer`.
</output_contract>

<acceptance_criteria>
- QG-BA-01: Classification FR/NFR + MoSCoW đầy đủ.
- QG-BA-02: Mermaid Seq(≥3 actors, double-quote) + Flow(3-path) + ERD(PK/FK).
- QG-BA-03: NFR metrics quantified (name+value số+unit), không từ mơ hồ.
- QG-BA-04: Gherkin ≥3 scenarios (Happy/Alt/Exception) + User Story.
- QG-BA-05: Risk Matrix P×I + mitigation không trống.
- `validate_metrics.py` 8/8 PASS + `schema_validator.py` exit 0.
</acceptance_criteria>

<failure_modes>
- **F22 Missing artifact**: elicitation-report.md không tồn tại → báo lỗi, không sinh output.
- **F23 Schema fail**: frontmatter thiếu key / value sai kiểu → chạy lại schema_validator, sửa trước khi ghi.
- **F24 Quality < threshold**: validate_metrics.py FAIL → quay lại phase tương ứng, không sang ba-synthesizer.
- **F25 pending_clarification**: input status chưa completed → STOP, không suy luận giả định.
</failure_modes>
