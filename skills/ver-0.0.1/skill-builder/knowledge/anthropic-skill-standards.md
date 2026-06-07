# Anthropic Skill Standards — Chuẩn Bắt Buộc khi Build SKILL.md

> **Usage**: Load khi bắt đầu viết file `SKILL.md` trong Step 3 BUILD. Đây là bộ tiêu chuẩn khoa học từ Anthropic nhằm đảm bảo skill hoạt động đáng tin cậy, tiết kiệm token, và hỗ trợ Discovery đúng.

---

## 1. YAML Frontmatter — BẮT BUỘC (Dòng đầu tiên)

Mọi `SKILL.md` đều phải bắt đầu bằng YAML frontmatter:

```yaml
---
name: <skill-name>
description: <what it does and when to trigger — third person, under 1024 chars>
---
```

**Quy tắc `name`**:
- Tối đa 64 ký tự
- Chỉ dùng: lowercase letters, numbers, hyphens (`-`)
- Không dùng XML tags, không dùng reserved words: `anthropic`, `claude`
- Ưu tiên gerund form: `processing-pdfs`, `analyzing-schemas`, `building-skills`

**Quy tắc `description`**:
- Viết ngôi thứ 3 (third person): "Extracts...", "Analyzes...", "Builds..."
- KHÔNG dùng: "I can help...", "You can use this to..."
- Bao gồm: **what the Skill does** + **khi nào nên trigger**
- Tối đa 1024 ký tự, không chứa XML tags

**Ví dụ tốt**:
```yaml
description: Extracts UI Screen Specs by analyzing Schema and Diagrams. Use when you need to bridge database logic and flow diagrams into intermediate UI component specifications for a given module.
```

**Ví dụ xấu (vi phạm)**:
```yaml
description: Helps with UI design
description: I can analyze your schema and create UI specs
```

---

## 2. Progressive Disclosure — Nguyên tắc Lazy-Loading

**SKILL.md chỉ là mục lục (table of contents)**, không phải encyclopedia.

### 2.1 Cấu trúc Tier

| Tier | File | Khi nào load |
|------|------|--------------|
| Tier 0 | `SKILL.md` | Luôn luôn (tự động khi invoke) |
| Tier 1 | Files LUÔN cần cho mọi invocation | Boot sequence hoặc Phase 1 |
| Tier 2 | Files chỉ cần cho phase/context cụ thể | Load đúng phase cần đến |

### 2.2 Anti-Pattern cần tránh: Context Overloading

❌ **KHÔNG làm**: Load tất cả files ngay từ Boot Sequence khi không chắc cần.

```markdown
# BAD — Context Overloading
## Mandatory Boot Sequence
Read ALL of these before doing ANYTHING:
1. knowledge/rules.md
2. knowledge/patterns.md
3. templates/output.md
4. loop/checklist.md
5. data/config.yaml
```

✅ **LÀM ĐÚNG**: Mỗi Phase/Step chỉ load file mình cần.

```markdown
# GOOD — Progressive Disclosure

## Phase 1: Discovery
(no extra files needed — run script only)

## Phase 3: Mapping
Read before this phase:
- [knowledge/mapping-rules.md](knowledge/mapping-rules.md)
- [knowledge/examples.md](knowledge/examples.md)

## Phase 4: Synthesis
If creating new: Read [templates/output.md](templates/output.md)

## Phase 5: Verify
Read: [loop/checklist.md](loop/checklist.md)
```

### 2.3 Khi nào Tier 1 (Boot Sequence) là hợp lệ

Boot Sequence chỉ hợp lệ cho file mà **mọi invocation đều cần ngay từ đầu**:
- Framework tổng thể (7-Zone architecture)
- Naming conventions áp dụng toàn bộ workflow
- Config file ảnh hưởng đến tất cả decisions

Nếu file chỉ cần cho 1 phase → đặt vào phase đó, không đặt ở Boot.

### 2.4 Quy tắc depth của references

- ✅ Reference files phải link **trực tiếp từ SKILL.md** (one level deep)
- ❌ Tránh nested references: `SKILL.md → A.md → B.md → actual content`
- Khi file reference > 100 lines: thêm Table of Contents ở đầu file

---

## 3. Workflow Tracker Checklist — BẮT BUỘC cho complex workflows

Với skill có từ 3+ Phase hoặc có Interaction Points (dừng hỏi user), **phải có checklist tracker**:

```markdown
## Workflow Progress Tracker

Copy this checklist into your response and mark off progress:

```markdown
### [Skill Name] Progress:
- [ ] Phase 1: [Tên phase]
- [ ] Phase 2: [Tên phase] → [⏸️ Gate nếu có]
- [ ] Phase 3: [Tên phase]
- [ ] Phase N: [Tên phase]
```
```

**Lý do**: Khi workflow bị gián đoạn bởi nhiều IP (Interaction Points), LLM dễ mất track trạng thái. Checklist được print trong response buộc model giữ đúng mạch xử lý.

**Quy tắc**:
- Claude PHẢI copy checklist này vào response ngay khi bắt đầu
- Mark `[x]` khi phase hoàn thành, update trước mỗi IP pause

---

## 4. Examples Pattern — Dùng để giảm Hallucination

Với mọi ánh xạ/mapping trừu tượng (schema → component, data → format), **phải cung cấp concrete examples**:

```markdown
## Mapping Examples

**Example 1 — Simple text field:**
Input schema:
  name: title, type: text, required: true, maxLength: 200

Output binding row:
  | `input-title` | `Input[type=text]` | `Post.title` | ✅ | maxLength: 200 |
```

**Nguyên tắc**:
- Cung cấp ít nhất 2-3 examples cho mỗi domain
- Examples phải là concrete (real field names, real components) không phải trừu tượng
- Edge cases phải có example riêng (nested objects, arrays, polymorphic types)
- Đặt examples trong file riêng (`knowledge/mapping-examples.md`) và reference từ phase cần

---

## 5. Degrees of Freedom — Match strictness to task fragility

| Tình huống | Level | Cách viết |
|---|---|---|
| Nhiều cách đều hợp lệ, context quyết định | **High freedom** | Mô tả text, heuristics |
| Có pattern ưu tiên, variation được chấp nhận | **Medium freedom** | Template với parameters |
| Operations fragile, phải đúng sequence | **Low freedom** | Exact commands, no variation |

**Ví dụ Low Freedom** (db migration phải đúng thứ tự):
```markdown
Run EXACTLY this command:
`python scripts/migrate.py --verify --backup`
Do NOT add flags or modify.
```

**Ví dụ High Freedom** (code review, context determines approach):
```markdown
Review for: structure, bugs, readability, conventions.
Apply judgment based on the specific codebase context.
```

---

## 6. Content Anti-Patterns cần tránh

### 6.1 Thông tin time-sensitive

❌ **KHÔNG làm**:
```markdown
Before August 2025, use the old API. After August 2025, use the new API.
```

✅ **LÀM ĐÚNG** — dùng "old patterns" section:
```markdown
## Current method
Use v2 API: `api.example.com/v2/messages`

## Old patterns (deprecated)
v1 API: `api.example.com/v1/messages` — no longer supported since 2025-08
```

### 6.2 Inconsistent terminology

- Chọn 1 thuật ngữ và dùng xuyên suốt
- "field" hoặc "property" — không mix cả hai
- "screen" hoặc "page" — không mix cả hai
- Nhất quán trong toàn bộ skill (SKILL.md + knowledge files + templates)

### 6.3 Too many options (confusing Claude)

❌ **KHÔNG làm**:
```markdown
You can use pypdf, or pdfplumber, or PyMuPDF, or pdf2image, or...
```

✅ **LÀM ĐÚNG** — Default + escape hatch:
```markdown
Use pdfplumber for text extraction. For scanned PDFs requiring OCR, use pdf2image + pytesseract instead.
```

### 6.4 Magic numbers trong scripts

❌ **KHÔNG làm**:
```python
TIMEOUT = 47
RETRIES = 5
```

✅ **LÀM ĐÚNG** — Self-documenting:
```python
# HTTP requests typically complete within 30 seconds
REQUEST_TIMEOUT = 30
# Three retries balances reliability vs speed
MAX_RETRIES = 3
```

---

## 7. Scripts — Solve, don't punt

Khi skill có utility scripts, scripts phải **handle errors explicitly**:

✅ **Handle errors, provide fallback**:
```python
def read_file(path):
    try:
        return open(path).read()
    except FileNotFoundError:
        print(f"File {path} not found, using default")
        return ""
    except PermissionError:
        print(f"Cannot access {path}, skipping")
        return ""
```

❌ **Punt to Claude**:
```python
def read_file(path):
    return open(path).read()  # Let Claude figure out the error
```

**Nguyên tắc**:
- Validation scripts phải output specific error messages ("Field X not found. Available: A, B, C")
- Phân biệt rõ: "Run script" (execute) vs "See script" (read as reference)
- List required packages trong SKILL.md

---

## 8. SKILL.md Size Limits

| Metric | Target | Hard limit |
|--------|--------|-----------|
| SKILL.md body | < 300 lines | 500 lines |
| Single reference file | < 200 lines | Unlimited (with ToC) |
| Boot Sequence files | ≤ 2 files | 3 files max |
| References per phase | ≤ 3 files | — |

Nếu SKILL.md > 500 lines → split content vào separate files, link từ relevant phase.

---

## 9. Discovery Checklist (Verify before shipping)

```
□ YAML frontmatter present (name + description)
□ description viết ngôi thứ 3 (third person)
□ description có WHAT + WHEN trigger
□ name là lowercase-kebab-case, ≤ 64 chars
□ SKILL.md body ≤ 500 lines
□ Không có time-sensitive information
□ Terminology nhất quán xuyên suốt
□ Complex workflow có Tracker Checklist
□ Ánh xạ trừu tượng có Examples file
□ References one level deep từ SKILL.md
□ Knowledge files có header > Usage
□ Progressive Disclosure: files load đúng phase cần
□ Scripts handle errors explicitly
□ No "too many options" confusion
```
