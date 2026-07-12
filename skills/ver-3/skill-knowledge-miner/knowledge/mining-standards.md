# Tiêu Chuẩn Khai Thác Tri Thức (Mining Standards)

> **Mã số**: STG07-KNOW-01
> **Vai trò**: Heuristic guidelines cho glossary extraction, anti-pattern detection, exemplar identification, và domain anchor construction.
> **Áp dụng cho**: `mine_for_terms.py`, `find_antipatterns.py`, domain-handbook pipeline.
> **Nguyên tắc**: Zero-dependency, heuristic-based, không dùng ML/AI external APIs.

---

## 1. Glossary Extraction Heuristics

Hệ thống phân cấp ưu tiên (Priority) khi trích xuất glossary terms từ workspace. Miner phải duyệt theo thứ tự A → E và **gộp tất cả term tìm được** trước khi chạy quality filters (§5). Nếu term count ≥ 10 sau gộp, dừng scan sớm (early-exit optimization).

### Priority A — knowledge/*.md

**Nguồn**: `skills/ver-3/*/knowledge/*.md` (tất cả skill knowledge files)

**Regex/keyword patterns**:

| Pattern | Mục tiêu | Ví dụ match |
|---------|----------|-------------|
| `^## (Glossary|Thuật ngữ)` | Section heading glossary | `## Glossary` hoặc `## Thuật ngữ` |
| `\| \*\*(.+?)\*\* \| (.+?) \|` | Bảng glossary (cột term + definition) | `\| **SCS** \| Skill Complexity Score 1.0-5.0 \|` |
| `^\- \*\*(.+?)\*\*[：:] (.+)` | Danh sách term + định nghĩa | `- **Domain Handbook**: Artifact đầu ra 5 trường` |
| `(?m)^(?:term|thuật ngữ)[=:]\s*(.+)$` | Cặp term/definition dạng YAML key-value | `term=SCS` |

**Hành vi**: Parse toàn bộ knowledge/*.md files. Ưu tiên section heading `## Glossary` hoặc `## Thuật ngữ`. Nếu không tìm thấy, fallback sang `\| **term** \|` pattern trong toàn file.

**Ví dụ trích xuất** từ exploration-standards.md:
```
Input: "| **Reusability** | Reusable skills anchor to domain knowledge files..."
Output: {term: "Reusability", definition: "Reusable skills anchor to domain knowledge files, not hardcoded logic"}
```

### Priority B — .claude/agents/*.md

**Nguồn**: `.claude/agents/*.md` (agent configuration files)

**Regex/keyword patterns**:

| Pattern | Mục tiêu | Ví dụ match |
|---------|----------|-------------|
| `^## (Terminology|Terminology Guidelines)` | Section heading terminology | `## Terminology` |
| `^\|\s*\*{0,2}(\w+(?:\s+\w+)*)\*{0,2}\s*\|\s*(.+?)\s*\|` | Bảng terminology | `\| Domain Handbook \| Artifact đầu ra 5 trường \|` |
| `\*\*(\w+(?:\s+\w+)*)\*\*\s*[：:]?\s*(.+)` | key-value pair với bold key | `**Glossary Term**: Cặp (term, definition) min 10` |
| `^-\s+\*\*(\w+)\*\*\s*:\s*(.+)` | Danh sách key-value | `- **Anti-Pattern**: Cặp (name, symptom, solution)` |

**Hành vi**: Parse toàn bộ `.claude/agents/*.md`. Agent files thường chứa section `## Terminology` với bảng key-value.

### Priority C — Temps/spec/**

**Nguồn**: `Temps/spec/**` (specification documents, đặc biệt là `Temps/spec/architects/` và `Temps/spec/roadmaps/`)

**Regex/keyword patterns**:

| Pattern | Mục tiêu | Ví dụ match |
|---------|----------|-------------|
| `^[-*#]+\s*\*{0,2}(\w+(?:\s+\w+)*)\*{0,2}\s*[：:]?\s*(.+)` | Định nghĩa từ section đầu | `- **Miner**: Stage 0.7, mining domain knowledge` |
| `###\s+(\d+\.?\d*\s+\w[\w\s]+)\s*\n+\s*(.+?)(?:\n###|\n---|\n$)` | Section đầu spec với định nghĩa | `### 2.1 Architecture Overview\nMiner là stage...` |
| `(?:định nghĩa|là|khái niệm|giải thích)[=:]\s*(.+?)(?:\n\n|\n-|\n#)` | Các câu định nghĩa tường minh | `định nghĩa: Domain Handbook là artifact...` |

**Hành vi**: Chỉ parse **section đầu tiên** (từ heading đầu tiên đến heading thứ hai) của mỗi file spec. Các spec files thường định nghĩa khái niệm chính ngay phần mở đầu.

### Priority D — _shared/knowledge/*

**Nguồn**: `skills/ver-3/_shared/knowledge/*.md` (shared knowledge base)

**Regex/keyword patterns**:

| Pattern | Mục tiêu | Ví dụ match |
|---------|----------|-------------|
| `^-\s+\*\*(.+?)\*\*\s*[：:]\s*(.+)` | Danh sách term definition | `- **Layer Separation**: Tri thức chia 4 lớp...` |
| `^\|\s*\*{0,2}(\w+(?:\s+\w+)*)\*{0,2}\s*\|\s*(.+?)\s*\|` | Bảng term + definition | `\| **L0 Anchor Rules** \| Hiến pháp cốt lõi \|` |
| `^#{2,3}\s+(.+?)\s*\n+([^#\n][\s\S]*?)(?=\n#{2,3}|\n---|$)` | Section headings + nội dung làm definition | `## Behavioral Coding Principles` + nội dung bên dưới |

**Hành vi**: Parse toàn bộ `_shared/knowledge/*.md`. Shared knowledge thường chứa domain terms từ karpathy-standards, framework, case-system, format-standards.

### Priority E — SKILL.md frontmatter

**Nguồn**: `skills/ver-3/*/SKILL.md` (YAML frontmatter)

**Regex/keyword patterns**:

| Pattern | Mục tiêu | Ví dụ match |
|---------|----------|-------------|
| `^tags:\s*\[(.+?)\]` | Tags array | `tags: [mining, heuristic, domain-handbook]` |
| `^description:\s*(.+?)(?:\n\w)` | Description field | `description: "Heuristic mining scripts..."` |
| `^skill_name:\s*"(.+?)"` | Skill name làm term | `skill_name: "skill-knowledge-miner"` |
| `^glossary:\s*\n(\s+-\s+.*\n)+` | YAML glossary block | `glossary:\n  - {term: "...", definition: "..."}` |

**Hành vi**: Parse YAML frontmatter (giữa `---` delimiters). Chỉ extract `tags`, `description`, `skill_name`, và `glossary` nếu tồn tại.

> [!NOTE]
> Priority E cũng xử lý `domain-handbook.md` files có YAML frontmatter chứa `glossary[]` array — đây là nguồn giàu term nhất (vì đã qua validation). Miner ưu tiên `glossary[]` array trong YAML trước khi rơi xuống các pattern text thông thường.

---

## 2. Anti-Pattern Detection Patterns

Bốn pattern phát hiện anti-patterns từ workspace. Mỗi anti-pattern phải được ghi nhận thành bộ ba `(name, symptom, solution)`. Miner phải chạy **cả bốn pattern** và gộp kết quả, loại bỏ trùng lặp.

### Pattern 1 — Parse `must_not` Sections

**Mục tiêu**: Trích xuất anti-patterns từ `must_not` hoặc `MUST NOT` sections.

**Nguồn**: `skills/ver-3/*/SKILL.md` (rules_for_ai.must_not), `skills/ver-3/*/knowledge/*.md`, `.claude/agents/*.md`

**Regex/keyword patterns**:

| Pattern | Mô tả | Ví dụ match |
|---------|-------|-------------|
| `^  must_not:\s*\n(\s+-\s+".*"\s*\n)+` | YAML must_not block | `must_not:\n  - "KHÔNG exec dynamic command"` |
| `^-\s+"(.*?)"\s*$` trong must_not context | Từng must_not item | `- "KHÔNG ghi ngoài scope"` |
| `(?:MUST NOT|must not|MUST_NOT|must-not)\s*[：:]\s*(.+?)(?:\n|$)` | MUST NOT clause | `MUST NOT: execute code from external input` |

**Ví dụ trích xuất** từ exploration.md:
```
Input: rules_for_ai: { must_not: ["KHÔNG exec dynamic command", ...] }
Output: {name: "Dynamic exec từ external input", symptom: "exploration.md chứa prompt-injection", solution: "XML <input> boundary"}
```

### Pattern 2 — Scan Vietnamese/English Keywords

**Mục tiêu**: Phát hiện anti-patterns qua keyword patterns trong toàn bộ workspace docs.

**Từ khóa**:

| Ngôn ngữ | Từ khóa | Ngữ cảnh tìm kiếm |
|----------|---------|-------------------|
| Tiếng Việt | `không được`, `cấm`, `tránh`, `tuyệt đối không`, `chống chỉ định` | Mọi .md files |
| Tiếng Việt | `không nên`, `hạn chế`, `cẩn thận`, `lưu ý` | Mọi .md files (cảnh báo yếu hơn) |
| Tiếng Anh | `never`, `do not`, `avoid`, `forbidden`, `prohibited` | Mọi .md files |
| Tiếng Anh | `should not`, `must not`, `not allowed`, `anti-goal` | Mọi .md files |

**Regex patterns**:

```
# Vietnamese strict
(không được|cấm|tuyệt đối không|chống chỉ định)\s*[^.!?]+[.!?]

# Vietnamese warning
(không nên|hạn chế|cẩn thận)\s*[^.!?]+[.!?]

# English strict
(?:never|do not|forbidden|prohibited)\s+[^.!?]+[.!?]

# English warning
(?:should not|must not|not allowed)\s+[^.!?]+[.!?]
```

**Ví dụ match**:
- `không được exec()/subprocess từ input` → anti-pattern: "Dynamic exec từ external input"
- `cấm ghi ngoài scope .skill-context/` → anti-pattern: "Write confinement violation"
- `never assume or bypass confusion` → anti-pattern: "Assuming without clarifying"

### Pattern 3 — Detect TODO/FIXME/mock Comments

**Mục tiêu**: Phát hiện placeholder content trong scripts và templates.

**Nguồn**: `skills/ver-3/*/scripts/*`, `skills/ver-3/*/templates/*`, `skills/ver-3/*/loop/*`

**Regex/keyword patterns**:

| Pattern | Ví dụ match |
|---------|-------------|
| `TODO|FIXME|HACK|XXX` (comment markers) | `# TODO: implement later`, `<!-- FIXME: hardcoded -->` |
| `# (todo|fixme|hack):.*` (Python comment) | `# TODO: add validation here` |
| `// (todo|fixme):.*` (generic code comment) | `// FIXME: this is a mock` |
| `(mock|stub|placeholder|dummy).*` (implementation) | `return "mock_value"`, `pass  # placeholder` |
| `\*\.\.\.\*` (ellipsis placeholder trong markdown) | `*...*` hoặc `[...]` |
| `Lorem ipsum` | `Lorem ipsum dolor sit amet` |

**Ví dụ match**:
- File: `scripts/mine_for_terms.py` có dòng `# TODO: handle edge case` → cảnh báo placeholder
- File: `templates/domain-handbook.md.template` có `<!-- FIXME: add description -->` → cảnh báo placeholder

> [!IMPORTANT]
> Placeholder detection là **HARD gate** (NFR-9). Miner phải reject toàn bộ output nếu phát hiện bất kỳ TODO/FIXME/mock nào. Zero-placeholder policy: không emit domain-handbook.md nếu scripts/templates chứa placeholder.

### Pattern 4 — Negative Space Catch-All

**Mục tiêu**: Phát hiện anti-patterns từ **Negative Space principle** — những điều hệ thống KHÔNG được làm nhưng không được ghi rõ trong must_not sections.

**Nguyên lý**: Mọi thiết kế skill đều có "vùng cấm" ngầm định. Pattern này khai thác:
1. **Error boundaries** trong domain-handbook (§4) — các edge case liệt kê behavior KHÔNG được phép
2. **Rủi ro (Risks)** trong exploration.md (§7) — mapping risk → anti-pattern
3. **NFR constraints** — mọi NFR là "phải làm" nhưng vi phạm NFR là anti-pattern
4. **Schema constraints** — `additionalProperties: false` = anti-pattern khi emit field lạ

**Heuristic rules**:

| Rule | Mô tả | Ví dụ |
|------|-------|-------|
| Error boundary → anti-pattern | Mọi error boundary mapping thành anti-pattern | E2: Glossary<10 → anti-pattern "Pass-form FAIL-meaning handbook" |
| Risk → anti-pattern | Risk có mitigation → anti-pattern (risk là symptom, mitigation là solution) | RR-01 prompt-injection → anti-pattern "Dynamic exec" |
| NFR violation → anti-pattern | Nếu NFR bị vi phạm, đó là anti-pattern | NFR-3 vi phạm → anti-pattern "Write confinement" |
| Schema drift → anti-pattern | Nếu output chứa field schema không cho phép | additionalProperties field → anti-pattern "Schema drift" |

**Ví dụ trích xuất** từ domain-handbook §4:
```
Error boundary E2: "Glossary<10 sau hydration → F6 re-scan → F2 escalate, NO EMIT"
→ Anti-pattern: {name: "Pass-form FAIL-meaning handbook", symptom: "glossary<10 nhưng vẫn emit", solution: "F6→F2 gate trước emit"}
```

---

## 3. Exemplar Identification

Exemplars là các skill hoàn chỉnh (v1.0+) trong cùng pipeline, dùng làm reference structure cho Builder ở Stage 1. Miner phải identify tối thiểu **1 exemplar** (≥1). Mỗi exemplar gồm `(name, description, optional reference_url_or_path)`.

### 3.1 Rules for Identifying Good Exemplars

| # | Rule | Tiêu chí | Ví dụ |
|---|------|----------|-------|
| R1 | **Completed v1.0+** | Skill đã build xong v1.0, có đủ 7-zone layout | skill-explorer v1.0 |
| R2 | **Same pipeline** | Skill trong pipeline (Stage 0→Stage 5), càng gần Stage càng tốt | skill-explorer (Stage 0 → Miner Stage 0.7) |
| R3 | **7-zone layout present** | Thư mục đủ core/knowledge/scripts/templates/data/loop/assets | skill-explorer có đủ 7 zones |
| R4 | **SKILL.md boot config** | Có SKILL.md ≤700 tokens với must/must_not, output_contract | skill-explorer/SKILL.md |
| R5 | **Quality gates operational** | Có loop/checklist, schema validation, DRC contract | skill-explorer/loop/ |
| R6 | **Knowledge files populated** | Có knowledge/*.md với nội dung thực (non-empty, non-placeholder) | exploration-standards.md |

### 3.2 Primary Exemplar — skill-explorer v1.0

**Vị trí**: `skills/ver-3/skill-explorer/`

**Lý do chọn**: skill-explorer là Stage 0 (immediate upstream của Miner Stage 0.7), đã complete v1.0 với đủ 7-zone layout, SKILL.md boot config, quality gates, knowledge files.

**Cấu trúc tham khảo**:
- `SKILL.md`: Boot config pattern, must/must_not format, output_contract ref
- `knowledge/exploration-standards.md`: Knowledge file format, section structure với numbered headings, bảng, code blocks
- `templates/`: Template pattern cho output generation
- `loop/exploration-checklist.md`: Checklist binary gates pattern
- `data/drc.yaml`: DRC contract format

**Pattern kế thừa cụ thể cho Miner**:

| skill-explorer pattern | Miner áp dụng |
|------------------------|---------------|
| SKILL.md boot sequence (≤700 tokens) | SKILL.md worker config |
| 7-zone layout (core/knowledge/scripts/...) | 7-zone layout mirror |
| knowledge/exploration-standards.md format | knowledge/mining-standards.md format |
| templates/ output template | templates/domain-handbook.md.template |
| data/drc.yaml contract | data/drc.yaml contract |
| loop/ checklist gates | loop/mining-checklist.md gates |

### 3.3 Secondary Pattern — ba-synthesizer Pipeline

**Vị trí**: `skills/ver-3/ba-synthesizer/` (BA Pipeline Stage 3 — synthesis)

**Lý do chọn**: ba-synthesizer là multi-stage orchestration pattern với context bus handoff. Tuy Miner là monolithic (SCS 2.6, Branch A), ba-synthesizer cho thấy:
- Cách input/output contract định nghĩa trong drc.yaml
- Cách quality score weighted sum tính pass/fail
- Cách pipeline readiness gate vận hành

**Khác biệt chính**: Miner monolithic, không cần multi-stage orchestration. Chỉ tham khảo contract pattern và quality gate mechanism.

### 3.4 Exemplar Extraction Algorithm

```
1. Scan skills/ver-3/*/ directories
2. For each: check SKILL.md tồn tại và non-empty
3. Check 7-zone layout: ls core/ knowledge/ scripts/ templates/ data/ loop/ assets/
4. Check quality gates: loop/*checklist*.md, data/drc.yaml
5. Check knowledge files: knowledge/*.md có nội dung >100 bytes
6. Prefer skills from same pipeline (explorer → architect → planner → builder → synthesizer)
7. Score exemplars: R1(3pts) + R2(3pts) + R3(2pts) + R4(1pt) + R5(1pt) + R6(1pt)
8. Chọn top exemplar + top secondary (nếu có)
```

---

## 4. Domain Anchor Construction

Domain anchors là chuỗi neo vector giúp Architect giữ ổn định ngữ nghĩa xuyên pipeline. Miner phải tạo tối thiểu **3 domain anchors** (≥3). Anchors được ghi vào `domain_anchors[]` trong domain-handbook YAML frontmatter.

### 4.1 Naming Convention

```
{stage}-{domain}-{concept}
```

**Rules**:
| Rule | Mô tả | Ví dụ |
|------|-------|-------|
| Kebab-case | Chữ thường, phân cách bằng `-` | `stage-0.7-miner` |
| Stage-prefixed | Stage hiện tại làm prefix | `stage-0.7-*`, `knowledge-foundation-*` |
| Domain-specific | Tên domain ngắn gọn | `miner`, `heuristic`, `handbook` |
| Concept chính | Concept chính của anchor | `output`, `gate`, `fallback` |
| No underscores | Dùng `-` thay vì `_` | `schema-validation-gate` (đúng), `schema_validation_gate` (sai) |
| No CamelCase | Chữ thường | `domain-handbook-output` (đúng), `DomainHandbookOutput` (sai) |
| Max 30 chars | Độ dài tối đa mỗi anchor | `write-confinement-gate` (21 chars) |

### 4.2 Anchor Categories

Mỗi skill cần anchors từ ít nhất 3 category khác nhau:

| Category | Pattern | Ý nghĩa | Ví dụ |
|----------|---------|---------|-------|
| **Pipeline** | `stage-{n}-{function}` | Vị trí trong pipeline | `stage-0.7-miner` |
| **Knowledge** | `knowledge-{layer}-{type}` | Layer knowledge foundation | `knowledge-foundation-layer-1` |
| **Output** | `{artifact}-{action}` | Output artifact + hành động | `domain-handbook-output` |
| **Constraint** | `{principle}-{constraint}` | Ràng buộc thiết kế | `heuristic-zero-dependency` |
| **Security** | `{mechanism}-{scope}` | Cơ chế bảo mật | `write-confinement-gate` |
| **Quality** | `{gate}-{type}` | Quality gate | `schema-validation-gate` |
| **Fallback** | `{level}-{action}` | Fallback behavior | `f2-f6-fallback` |

### 4.3 Minimum 3 Anchors Per Skill

Miner phải tạo ít nhất 3 anchors. Ví dụ cho skill-knowledge-miner:

```
domain_anchors:
  - "stage-0.7-miner"              # Pipeline — vị trí Stage 0.7
  - "knowledge-foundation-layer-1" # Knowledge — Layer 1 domain mining
  - "domain-handbook-output"       # Output — artifact chính
  - "heuristic-zero-dependency"    # Constraint — zero-dependency principle
  - "write-confinement-gate"       # Security — NFR-3 write scope
  - "schema-validation-gate"       # Quality — NFR-5 pre-emit validation
  - "f2-f6-fallback"              # Fallback — insufficient recovery
```

### 4.4 Anchor Stability Protocol

```
1. Anchors được ghi vào domain_anchors[] trong domain-handbook frontmatter
2. Anchors là WORM (Write Once, Read Many) — KHÔNG thay đổi giữa CREATE→UPDATE
3. Nếu UPDATE mode: preserve anchor cũ, chỉ thêm anchor mới (KHÔNG xóa)
4. Architect dùng anchors để: neo context → giữ consistent terminology → chống drift
5. Mỗi anchor phải xuất hiện ít nhất 1 lần trong glossary (để có definition)
```

---

## 5. Quality Filters

Bộ lọc chất lượng cho tất cả term/anti-pattern/exemplar/anchor trước khi emit vào domain-handbook.md.

### 5.1 Term Validation

Mỗi `{term, definition}` pair phải pass tất cả filter sau:

| # | Filter | Rule | Reject nếu |
|---|--------|------|------------|
| F1 | **Minimum length** | term string ≥ 3 characters | term = "AI", "ML", "SC" (≤2 chars) |
| F2 | **Non-empty definition** | definition string ≥ 5 characters | definition = "" hoặc definition = " " |
| F3 | **No placeholder** | definition không chứa placeholder | definition chứa "TODO", "FIXME", "mock", "..." |
| F4 | **No generic term** | term không phải từ quá phổ biến | term = "skill", "file", "code", "data" |
| F5 | **No numeric-only** | term không chỉ gồm số | term = "123", "3.14" |
| F6 | **Contentful definition** | definition chứa nội dung thực (không chứa các ký hiệu biến template như "{}" hoặc "<>") | definition = "{term} là một khái niệm..." |
| F7 | **Valid JSON/YAML** | Nếu definition chứa code block, syntax phải valid | Code block với syntax error |
| F8 | **No system metadata** | term không trùng với các từ khóa metadata hệ thống | term = "author", "status", "created at", "completed at", "version", "suite" (case-insensitive) |

**Implementation rule**: Filter sequence là **AND gate** — term bị reject nếu FAIL bất kỳ filter nào. Log lý do reject vào stderr.

### 5.2 Deduplication Rules

| # | Rule | Cơ chế | Ví dụ |
|---|------|--------|-------|
| D1 | **Exact match** | `term.lower()` trùng nhau → giữ cái có definition dài hơn | "SCS" và "scs" → giữ definition dài hơn |
| D2 | **Normalized match** | Normalize (lowercase, trim, remove diacritics) trùng nhau → giữ cái đầu | "Domain-handbook" vs "Domain Handbook" → giữ cái đầu |
| D3 | **Non-conflicting rename** | Term khác nhau nhưng definition trùng >80% → giữ term rõ hơn | "META-2.1 depth signals" vs "META-2.1" → giữ "META-2.1 depth signals" |
| D4 | **Source priority** | Same term từ nhiều source → ưu tiên Priority A > B > C > D > E | knowledge/*.md term thắng SKILL.md frontmatter term |
| D5 | **Handbook precedence** | Domain handbook glossary[] override tất cả | handbook term KHÔNG bị dedup nếu term khớp — handbook là source of truth |

**Deduplication algorithm**:
```
1. Group terms by exact lowercase match (D1)
2. Trong mỗi group, expand với normalized match (D2)
3. Giữ term duy nhất theo priority D4
4. Nếu definition conflict, giữ definition dài hơn (D1)
5. Nếu handbook có term đó, handbook definition wins (D5)
6. Output: list deduplicated terms, sorted alphabetically
```

### 5.3 Cross-Reference Against Existing Handbooks

| # | Rule | Mô tả |
|---|------|-------|
| X1 | **Handbook lookup** | Kiểm tra term đã tồn tại trong `.skill-context/*/domain-handbook.md` glossary chưa |
| X2 | **Definition alignment** | Nếu term đã tồn tại, definition trong handbook hiện tại phải consistent với định nghĩa mới (so khớp qua Prompt Hook "verify-semantic-alignment" của harness, hoặc tính toán cơ học Jaccard similarity ≥ 0.6 / edit distance ≤ 0.3) |
| X3 | **Anchor cross-ref** | Mỗi domain_anchor phải có ít nhất 1 term trong glossary khớp concept |
| X4 | **Anti-pattern coverage** | Mỗi anti_pattern phải có ít nhất 1 NFR hoặc 1 risk trong exploration.md làm evidence |
| X5 | **Exemplar validation** | Exemplar phải tồn tại thực tế (directory + SKILL.md non-empty), không reference vào skill chưa build |

**Cross-reference output**: Ghi list term conflict vào mining log nếu phát hiện inconsistency. KHÔNG tự động sửa — escalate F2 nếu critical conflict.

### 5.4 Aggregate Quality Gate

Trước khi emit domain-handbook.md, Miner phải pass aggregate gate:

```
PASS iff:
  glossary_count ≥ 10                  (FR-8 threshold)
  AND anti_patterns_count ≥ 3          (Negative Space requirement)
  AND exemplars_count ≥ 1              (Reference requirement)
  AND domain_anchors_count ≥ 3         (Anchor stability requirement)
  AND no_placeholder_found             (NFR-9 zero-placeholder)
  AND schema_validation_pass           (NFR-5 schema valid)

If FAIL:
  - glossary < 10 → F6 re-scan via Librarian subagent
  - anti_patterns < 3 → F2 escalate DIRECT
  - exemplars < 1 → F2 escalate DIRECT
  - domain_anchors < 3 → F2 escalate DIRECT
  - placeholder found → F2 escalate DIRECT + log file path
  - schema fail → F2 escalate DIRECT + log schema errors
```

---

## 6. Combined Extraction Algorithm

Luồng xử lý tổng hợp cho miner khi nhận lệnh:

```
Phase 1: Đọc exploration.md (mandatory) + hydrated-context.yaml + thought-cache.yaml
         Nếu có business-analysis.md, parse synthesized_requirements từ frontmatter

Phase 2: Workspace scan theo thứ tự Priority A → B → C → D → E (Section 1)
         Mỗi priority parse theo regex patterns tương ứng
         Gộp tất cả raw terms vào master list

Phase 3: Anti-pattern detection: chạy Pattern 1 → 2 → 3 → 4 (Section 2)
         Gộp raw anti-patterns, dedup theo name

Phase 4: Exemplar identification (Section 3)
         Scan skills/ver-3/*/, score theo R1-R6, chọn top exemplar(s)

Phase 5: Domain anchor construction (Section 4)
         Tạo anchors theo naming convention, min 3 anchors từ ≥3 categories

Phase 6: Quality filters (Section 5)
         Term validation (F1-F7) → Deduplication (D1-D5) → Cross-ref (X1-X5)
         Aggregate quality gate (Section 5.4)

Phase 7: Schema validation (domain-handbook.schema.yaml)
         Nếu PASS: emit domain-handbook.md
         Nếu FAIL: F2 escalate ba-pipeline-runner, NO EMIT
```

---

## 7. Integration với Domain Handbook Schema

Mining output mapping vào domain-handbook YAML frontmatter schema:

```yaml
skill_name: "skill-knowledge-miner"
glossary:                    # Từ Section 1 → Filters Section 5
  - {term: "...", definition: "..."}    # Min 10 items
anti_patterns:               # Từ Section 2 → Filters Section 5
  - {name: "...", symptom: "...", solution: "..."}  # Min 3 items
exemplars:                   # Từ Section 3
  - {name: "...", description: "...", optional reference_url_or_path}  # Min 1 item
domain_anchors:              # Từ Section 4
  - "stage-prefixed-kebab-anchor"  # Min 3 items
```

---

## 8. Token Budget & Loading Strategy

File này là L2 Domain Knowledge (600-2500 tokens) trong 4-layer knowledge architecture:

| Layer | File | Token budget | Loading trigger |
|-------|------|-------------|-----------------|
| L0 | SKILL.md | ≤700 | Always boot |
| L0 | data/drc.yaml | ≤200 | Always boot |
| L2 | knowledge/mining-standards.md | ≤2500 | Phase 2-3-4-5-6 |
| L3 | templates/domain-handbook.md.template | ≤500 | Phase 7 emit |
| L3 | loop/mining-checklist.md | ≤300 | Pre-emit gate |

> [!NOTE]
> mining-standards.md là L2 (không phải L0). Nó được nạp khi Miner vào Phase 2 (Workspace Scan) và giữ cho đến Phase 7 (Emit). Sau emit, context được giải phóng.

---

## 9. Error Boundaries cho Mining Process

| # | Edge case | Behavior |
|---|-----------|----------|
| M-E1 | Workspace empty (không knowledge/, Temps/, .claude/, _shared/) | Fallback: exploration.md §1 glossary làm sole source |
| M-E2 | Regex pattern không match term nào | Tăng threshold: dùng greedy pattern (match mọi `**...**` pair) |
| M-E3 | Term count >100 (data overload) | Cap 100 terms: ưu tiên Priority A→B, loại bỏ trùng D1-D5, cắt dưới cùng |
| M-E4 | Definition >500 chars | Truncate definition tại 500 chars + "..." marker |
| M-E5 | Term chứa special characters ko parse được | Escape/remove non-ASCII trừ tiếng Việt có dấu |
| M-E6 | Anti-pattern count >20 | Cap 20: giữ 5 mỗi pattern (Pattern 1:5, 2:5, 3:5, 4:5) |
| M-E7 | business-analysis.md parse fail | Graceful degradation: bỏ qua, chỉ dùng exploration.md |

---

> **Document status**: Mining standards cho skill-knowledge-miner Stage 0.7.
> **Zero placeholder**: Pass — không có TODO/FIXME/mock.
> **Zero external dependency**: Pass — tất cả heuristic đều regex/keyword thuần.
> **Cross-ref**: Đồng bộ với domain-handbook §3.A, exploration.md §3.3, §6.
