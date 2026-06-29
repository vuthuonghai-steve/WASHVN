# CLAUDE.md — Skills Directory Agent Guide

> **Version:** 1.0.1 | **Updated:** 2026-06-08
> **Scope:** Quy tắc phát triển và bảo trì trong thư mục `skills/`.

<instructions>
Luôn tuân thủ quy trình quản lý và đồng bộ kỹ năng (skills). Bất kỳ thay đổi nào về cấu trúc thư mục hoặc danh sách kỹ năng chính thức đều phải được phản ánh chính xác trong tệp đăng ký hệ sinh thái.
</instructions>

---

## 📌 Quy tắc Quan trọng Nhất (Crucial Rule)

> [!IMPORTANT]
> **CẬP NHẬT ĐĂNG KÝ HỆ SINH THÁI (ECOSYSTEM REGISTRY)**
> Trong suốt quá trình bảo trì và phát triển:
> - **Mỗi khi BỔ SUNG** một skill mới thuộc về các phiên bản chính thức trong thư mục [skills](file:///home/steve/Work-space/WASHVN/skills) (ví dụ: `skills/ver-0.0.1/`, `skills/ver-0.0.2/`, v.v.)
> - **Hoặc loại bỏ (LOẠI BỎ)** một skill thuộc về các phiên bản chính thức này
>
> ➡️ **BẮT BUỘC phải cập nhật ngay lập tức** danh sách đăng ký trong tệp [skills-registry.json](file:///home/steve/Work-space/WASHVN/skills-registry.json) ở root thư mục để đảm bảo tính đồng bộ và định tuyến động (Dynamic Routing) hoạt động chính xác.
>
> ⚠️ **Ngoại lệ (Exceptions)**:
> Các skill được tạo ngoài các thư mục version chính thức (ví dụ: các skill kiểm thử, thử nghiệm tạm thời, chơi nháp) **KHÔNG cần thiết** phải cập nhật hay đăng ký quản lý trong `skills-registry.json`.

---

## 📁 Cấu trúc Thư mục `skills/`

- `skills/ver-0.0.1/`: Phiên bản baseline thô sơ hiện tại.
- `skills/ver-0.0.2/`: Phiên bản nâng cấp (hiện đang trống).
- [skills-registry.json](file:///home/steve/Work-space/WASHVN/skills-registry.json): Sổ cái cấu trúc chứa thông tin chi tiết từng kỹ năng chính thức, input/output và sơ đồ luồng dữ liệu.

## 🛠️ Quy trình Thực hiện khi Thêm/Bớt Skill thuộc Version chính thức

1. **Khi thêm Skill mới**:
   - Khởi tạo thư mục skill theo chuẩn 7 Zones dưới phiên bản tương ứng (ví dụ: `skills/ver-0.0.1/new-skill/`).
   - Khai báo đầy đủ metadata (name, stage, type, target_variable, role, src_path, boot_file, inputs, outputs) trong `skills-registry.json`.

2. **Khi xóa/loại bỏ Skill**:
   - Xóa thư mục skill trong phiên bản tương ứng.
   - Xóa định nghĩa của skill đó khỏi mảng `"skills"` trong `skills-registry.json`.
