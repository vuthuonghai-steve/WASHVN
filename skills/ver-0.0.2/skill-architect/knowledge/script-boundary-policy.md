# Script Boundary Policy

> **Mục đích:** Định nghĩa ranh giới deterministic cho Scripts Zone — ngăn script làm thay việc của LLM.
> **Áp dụng cho:** skill-architect thiết kế scripts zone của bất kỳ skill nào.
> **Version:** 0.0.1 | **Suite:** WASHVN

---

## 1. Nguyên tắc cốt lõi

```yaml
core_principle:
  - "Script CHỈ xử lý deterministic tasks — input xác định → output xác định"
  - "Mọi quyết định nghiệp vụ PHẢI để LLM xử lý qua knowledge/ + SKILL.md instructions"
  - "Script KHÔNG được chứa business logic, decision trees, prompt templates"
```

## 2. Decision Boundary

### ✅ Script được phép làm (Deterministic)

```
- IO operations: tạo thư mục, copy file, move file
- Parse và validate cấu trúc (YAML frontmatter, JSON schema)
- Export: extract Mermaid blocks, sinh standalone files
- Run checklist: kiểm tra required sections, so khớp §3 vs §4
- Network calls gọi API deterministic (GET static data)
```

### ❌ Script KHÔNG được làm (Business Logic)

```
- Quyết định zone nào cần/không cần
- Chọn knowledge files cần cho skill
- Sinh nội dung design templates
- Sinh prompt templates hoặc instructions cho LLM
- Data transformation rules, conditional branching logic
- Decision trees: "nếu X thì làm Y"
```

## 3. Quy tắc thiết kế

1. **Scripts được thiết kế SAU KHI knowledge zone hoàn tất** — knowledge quyết định business logic, script chỉ chạy deterministic tasks
2. **Mỗi script PHẢI có deterministic boundary comment** — 3 dòng đầu file ghi rõ: script này làm gì / KHÔNG làm gì
3. **Input/Output schema bắt buộc** — mọi script phải khai báo input format và output format
4. **Zero side-effect với LLM context** — script không đọc/sửa context của LLM

## 4. Anti-patterns cần tránh

| Anti-pattern | Ví dụ | Fix |
|-------------|-------|-----|
| Script sinh template thiết kế | `init_context.py` tạo `design.md.template` | Chỉ tạo thư mục, không pre-populate nội dung |
| Script chứa conditional business logic | `if skill_type == "api": add api-rules.md` | Chuyển vào knowledge/ zone, LLM tự quyết định |
| Script generate prompt | Script sinh instructions cho LLM | Instructions để trong SKILL.md |

## 5. Checklist validation

- [ ] Script output có thay đổi khi input giống nhau không? (Phải: không)
- [ ] Script có quyết định "nên làm gì" không? (Phải: không)
- [ ] Script có thể thay bằng shell one-liner không? (Nếu có: ưu tiên shell)
- [ ] Script dependency có portable không? (Shell > Python > Docker)
