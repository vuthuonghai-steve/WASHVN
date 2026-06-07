# Miner Quality Gate Checklist

Tệp này chứa danh sách kiểm định chất lượng đối với cẩm nang tri thức `domain-handbook.md` trước khi bàn giao sang Stage 1 (Architect).

<instructions>
must:
  - verify domain-handbook.md contains no placeholder symbols like '...' or TODOs
  - ensure all code examples are enclosed within strict markdown code blocks and contain syntax highlighting
  - verify all business glossaries are in Vietnamese and correct technically
must_not:
  - pass any handbook that has less than 3 major sections
</instructions>

## Checklist Đánh giá
- [ ] §1: Bối cảnh & Thuật ngữ Chuyên ngành đầy đủ?
- [ ] §2: Sơ đồ Kiến trúc & API Spec chính xác theo tài liệu gốc?
- [ ] §3: Mã mẫu lập trình tối giản, sạch, không có placeholder?
- [ ] §4: Danh sách các trường hợp biên và xử lý lỗi được thiết lập?
