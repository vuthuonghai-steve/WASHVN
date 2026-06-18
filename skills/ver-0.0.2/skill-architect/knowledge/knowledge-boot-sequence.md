# Knowledge Boot Sequence

> **Mục đích:** Định nghĩa boot sequence v2 cho skill-architect — tích hợp knowledge scan trước khi thiết kế.
> **Áp dụng cho:** skill-architect SKILL.md boot sequence.
> **Version:** 0.0.1 | **Suite:** WASHVN

---

## 1. Boot Sequence v2

```yaml
boot_sequence_v2:
  step_1: "Read SKILL.md (this file)"
  step_2: "Read _shared/knowledge/framework.md"
  step_3: "Scan skills/ver-0.0.2/{target_skill}/ knowledge/ — Tier 1 (ALWAYS)"
  step_4: "Read knowledge/ files found in step 3"
  step_5: "Check .skill-context/{target_skill}/ — upstream artifacts"
  step_6: "IF exploration.md exists → read (primary upstream source)"
  step_7: "IF domain-handbook.md exists → read (domain knowledge from Knowledge Miner)"
  step_8: "Proceed to Phase 1: Collect — ONLY after context built"
```

## 2. Knowledge Source Priority

| Tier | Nguồn | Điều kiện load | Bắt buộc? |
|------|-------|---------------|-----------|
| Tier 1 | `skill-architect/knowledge/*.md` | ALWAYS | ✅ |
| Tier 1 | `.skill-context/{target}/exploration.md` | IF EXISTS | ✅ |
| Tier 1 | `.skill-context/{target}/domain-handbook.md` | IF EXISTS | ✅ |
| Tier 2 | `_shared/knowledge/*.md` | ALWAYS | ✅ |
| Tier 3 | `skill-architect/references/examples/*.md` | WHEN cần reference | ❌ |

## 3. Knowledge Gap Handling

```yaml
knowledge_gap_protocol:
  condition: "No knowledge files found in Tier 1 source"
  action:
    - "Set confidence < 70%"
    - "ASK user: provide domain knowledge before continuing"
    - "DO NOT hallucinate §2 content"
  if_user_cannot_provide:
    - "Log knowledge gap to design.md §9 Open Questions"
    - "Flag [CẦN LÀM RÕ] trên mọi assertion"
    - "Proceed with 'LIMITED KNOWLEDGE' warning in design.md frontmatter"
```

## 4. Design.md §2 Capability Map — Trace Rules

Mọi item trong §2 Capability Map PHẢI trace về knowledge source:

```yaml
attribution_rules:
  "[TỪ knowledge/{file}.md]":
    - "Dùng khi thông tin lấy từ knowledge/ file của skill-architect"
  "[TỰ SUY LUẬN]":
    - "Dùng khi không có knowledge source — phải kèm confidence level"
    - "Chỉ dùng nếu confidence ≥ 70%"
  "[CẦN LÀM RÕ]":
    - "Dùng khi thông tin không đủ để thiết kế"
```

## 5. Checklist

- [ ] Boot scan đã tìm thấy knowledge files? (Có/Không → gap protocol)
- [ ] §2 mọi item có trace tag?
- [ ] Nếu confidence < 70% → đã hỏi user?
- [ ] exploration.md được ưu tiên làm primary source?
