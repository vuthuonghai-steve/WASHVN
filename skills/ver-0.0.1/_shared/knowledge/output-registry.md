# 📋 WASHVN Skill Suite — Output Registry

> **Tự động tạo bởi**: `validate_suite_integrity.py`  
> **Phiên bản bộ suite**: `0.0.1`  
> **Cập nhật lúc**: `2026-06-07 14:15:39 UTC`  

Tài liệu này đăng ký và liệt kê toàn bộ các tệp đầu ra (output files) được quy hoạch trong bộ kỹ năng WASHVN, phân loại theo cấu trúc Type 1 (Monolithic Stage) và Type 2 (Hierarchical Micro-skill).

---

## 1. Phân loại theo Kỹ năng (By Skill)

| Kỹ năng (Skill) | Loại (Type) | Biến định tuyến (Routing Var) | Tệp đầu ra (Output File) | Đường dẫn định mẫu (Path Template) | Định dạng (Format) |
|---|---|---|---|---|---|
| `skill-explorer` | Type 1 (Monolithic Stage) | `target_skill` | `exploration_report` | `.skill-context/{target_skill}/exploration.md` | `markdown` |
| `skill-explorer` | Type 1 (Monolithic Stage) | `target_skill` | `test_criteria` | `.skill-context/{target_skill}/criteria.md` | `markdown` |
| `skill-knowledge-miner` | Type 1 (Monolithic Stage) | `target_skill` | `domain_handbook` | `.skill-context/{target_skill}/domain-handbook.md` | `markdown` |
| `skill-architect` | Type 1 (Monolithic Stage) | `target_skill` | `architect_design` | `.skill-context/{target_skill}/design.md` | `markdown` |
| `production-quality-gatekeeper` | Type 1 (Monolithic Stage) | `target_skill` | `quality_matrix` | `.skill-context/{target_skill}/quality-matrix.yaml` | `yaml` |
| `production-quality-gatekeeper` | Type 1 (Monolithic Stage) | `target_skill` | `evaluation_report` | `.skill-context/{target_skill}/evaluation-report.md` | `markdown` |
| `production-quality-gatekeeper` | Type 1 (Monolithic Stage) | `target_skill` | `refinement_feedback` | `.skill-context/{target_skill}/feedback.yaml` | `yaml` |
| `skill-planner` | Type 1 (Monolithic Stage) | `target_skill` | `execution_plan` | `.skill-context/{target_skill}/todo.md` | `markdown` |
| `skill-builder` | Type 1 (Monolithic Stage) | `target_skill` | `build_log` | `.skill-context/{target_skill}/build-log.md` | `markdown` |
| `production-code-reviewer` | Type 1 (Monolithic Stage) | `target_skill` | `code_review_report` | `.skill-context/{target_skill}/review-report.md` | `markdown` |
| `production-code-reviewer` | Type 1 (Monolithic Stage) | `target_skill` | `audit_metrics` | `.skill-context/{target_skill}/audit-metrics.yaml` | `yaml` |
| `ba-elicitor` | Type 2 (Hierarchical Micro-skill) | `feature_name` | `elicitation_report` | `.skill-context/{feature_name}/ba-elicitor/elicitation-report.md` | `markdown` |
| `ba-analyst` | Type 2 (Hierarchical Micro-skill) | `feature_name` | `analysis_report` | `.skill-context/{feature_name}/ba-analyst/analysis-report.md` | `markdown` |
| `ba-synthesizer` | Type 2 (Hierarchical Micro-skill) | `feature_name` | `synthesized_business_analysis` | `.skill-context/{feature_name}/business-analysis.md` | `markdown` |
| `skill-security-reviewer` | Type 1 (Monolithic Stage) | `target_skill` | `security_review_report` | `.skill-context/{target_skill}/security-review-report.md` | `markdown` |

---

## 2. Danh sách Đường dẫn định mẫu (All Path Templates)

- [ ] `.skill-context/{feature_name}/ba-analyst/analysis-report.md` (ID: `analysis_report` từ `ba-analyst`)
- [ ] `.skill-context/{feature_name}/ba-elicitor/elicitation-report.md` (ID: `elicitation_report` từ `ba-elicitor`)
- [ ] `.skill-context/{feature_name}/business-analysis.md` (ID: `synthesized_business_analysis` từ `ba-synthesizer`)
- [ ] `.skill-context/{target_skill}/audit-metrics.yaml` (ID: `audit_metrics` từ `production-code-reviewer`)
- [ ] `.skill-context/{target_skill}/build-log.md` (ID: `build_log` từ `skill-builder`)
- [ ] `.skill-context/{target_skill}/criteria.md` (ID: `test_criteria` từ `skill-explorer`)
- [ ] `.skill-context/{target_skill}/design.md` (ID: `architect_design` từ `skill-architect`)
- [ ] `.skill-context/{target_skill}/domain-handbook.md` (ID: `domain_handbook` từ `skill-knowledge-miner`)
- [ ] `.skill-context/{target_skill}/evaluation-report.md` (ID: `evaluation_report` từ `production-quality-gatekeeper`)
- [ ] `.skill-context/{target_skill}/exploration.md` (ID: `exploration_report` từ `skill-explorer`)
- [ ] `.skill-context/{target_skill}/feedback.yaml` (ID: `refinement_feedback` từ `production-quality-gatekeeper`)
- [ ] `.skill-context/{target_skill}/quality-matrix.yaml` (ID: `quality_matrix` từ `production-quality-gatekeeper`)
- [ ] `.skill-context/{target_skill}/review-report.md` (ID: `code_review_report` từ `production-code-reviewer`)
- [ ] `.skill-context/{target_skill}/security-review-report.md` (ID: `security_review_report` từ `skill-security-reviewer`)
- [ ] `.skill-context/{target_skill}/todo.md` (ID: `execution_plan` từ `skill-planner`)
