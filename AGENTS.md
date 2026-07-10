# AGENTS.md

> **Chế độ đồng bộ hóa hành vi (Behavior Synchronization Mode)**
> **Chuẩn chung:** [CLAUDE.md](file:///home/stveve/Documents/workspace/build-workflow/WASHVN/CLAUDE.md) (Root Guide của dự án WASHVN)

Tài liệu này được thiết kế để điều hướng hành vi của toàn bộ các AI Agent (Antigravity, Hermes, Claude Code, OMC/OMX) về một nguồn tri thức chuẩn duy nhất.

---

## ⚠️ YÊU CẦU BẮT BUỘC ĐỐI VỚI LLM / AI AGENT

1. **ĐỌC CLAUDE.MD ĐẦU TIÊN:**
   Trước khi thực hiện bất kỳ hành động hay thay đổi mã nguồn nào, bạn **BẮT BUỘC** phải đọc nội dung tệp tin [CLAUDE.md](file:///home/stveve/Documents/workspace/build-workflow/WASHVN/CLAUDE.md) tại thư mục hiện tại để nắm bắt toàn bộ:
   - Tổng quan dự án (Project Overview)
   - Ngăn xếp công nghệ (Tech Stack)
   - Quy ước lập trình và phong cách code (Code Style & Conventions)
   - Các lệnh kiểm tra, xác thực và đồng bộ hóa (Commands)
   - Quy tắc ứng xử và cấm kỵ (Do's & Don'ts)

2. **TUÂN THỦ CÁC CHỈ THỊ TRONG CLAUDE.MD:**
   Mọi hành động triển khai phải tuân thủ nghiêm ngặt theo các chính sách và quy chuẩn (L0 anchor rules + L1 working policy) được quy định trong [CLAUDE.md](file:///home/stveve/Documents/workspace/build-workflow/WASHVN/CLAUDE.md).

3. **KHÔNG SAO CHÉP NGỮ CẢNH:**
   Không tự ý định nghĩa lại hoặc sao chép ngữ cảnh cấu hình từ [CLAUDE.md](file:///home/stveve/Documents/workspace/build-workflow/WASHVN/CLAUDE.md) vào đây để tránh trôi lệch thông tin (Semantic Drift). Luôn tra cứu trực tiếp từ [CLAUDE.md](file:///home/stveve/Documents/workspace/build-workflow/WASHVN/CLAUDE.md).

---

**These guidelines are working if:** You immediately load [CLAUDE.md](file:///home/stveve/Documents/workspace/build-workflow/WASHVN/CLAUDE.md) and align all implementation steps with its protocol.
