# Quality Gate: Exploration Quality Checklist

> **Vai trò**: Binary gate verification before Stage 0 handoff. Every check is PASS/FAIL.

---

## 1. Artifact Integrity

- [ ] `exploration.md` exists and non-empty
- [ ] `hydrated-context.yaml` exists and non-empty
- [ ] `thought-cache.yaml` exists and non-empty

---

## 2. META-2.1 Depth Gate (per thought-cache block)

For EVERY thought block in `thought-cache.yaml`:

- [ ] **S1 (Negation)**: Contains 'must_not' or 'không'
- [ ] **S2 (Interrogation)**: Contains '?'
- [ ] **S3 (Stakeholder)**: Contains user/dev/agent/người
- [ ] **S4 (Constraint)**: Contains 'constraint' or 'ràng buộc'

**Result**: All 4 present = PASS. Any absent = FAIL → regenerate block.

---

## 3. Budget Gates

- [ ] Glossary in hydrated-context.yaml: ≥10 terms
- [ ] Each thought block in thought-cache.yaml: ≥200 words
- [ ] hydrated-context.yaml total: ≤50 lines

---

## 4. YAML Resilience (L1-L3 Pre-commit)

- [ ] **L1 Syntax**: All YAML files parse without error (`python3 -c "import yaml; yaml.safe_load(open('...'))"`)
- [ ] **L2 Schema**: hydrated-context.yaml and thought-cache.yaml conform to their respective schema files
- [ ] **L3 Cross-refs**: All cross-references between exploration.md, hydrated-context.yaml, and thought-cache.yaml resolve (e.g., glossary terms referenced in exploration.md exist in hydrated-context.yaml)

---

## 5. Kiểm tra Cấu trúc & Định dạng Tệp

- [ ] Frontmatter đầy đủ các trường yêu cầu và khớp chuẩn `exploration.schema.yaml`.
- [ ] Tồn tại đầy đủ **8 chương mục tiêu đề bắt buộc** từ §1 đến §8.
- [ ] Mọi đề xuất tri thức domain đều có nguồn tham chiếu thực tế tại thư mục `resources/`.
- [ ] Tài liệu được biên soạn 100% bằng Tiếng Việt chuẩn mực kỹ thuật.

---

## 6. 7 Golden Standards Check

- [ ] **Reusability**: Separated static knowledge from dynamic instructions?
- [ ] **Composability**: Priority / meta-prompting rules defined?
- [ ] **Maintainability**: SKILL.md follows 4-layer structure + Goldilocks zone?
- [ ] **Security**: XML delimiters + Docker sandbox isolation in place?
- [ ] **Token Efficiency**: Progressive Disclosure tier strategy defined?
- [ ] **Portability**: Relative paths only? No implicit model lock-in?
- [ ] **Resilience**: Execution logging + HITL fallback defined?
- [ ] **Scale & Complexity**: SCS score computed? Micro-skill split decision clear?
- [ ] **Orchestration**: Mermaid coordination diagram drawn for multi-micro-skill flows?

---

## Result

- [ ] **ALL CHECKS PASS** → proceed to handoff
- [ ] **ANY FAIL** → fix blocker, re-run checklist
