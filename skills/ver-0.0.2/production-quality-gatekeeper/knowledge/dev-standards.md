# 💻 Tiêu chuẩn Kỹ thuật Lập trình và Kiến trúc Hệ thống (Dev standards)
# Phiên bản: 1.1.0 — Chuẩn Production-Grade Khắt khe của Google

Tài liệu này đặc tả chi tiết 40 tiêu chí đánh giá chất lượng lập trình (Dev Domain) thuộc Bộ Cổng Chất lượng Chủ thể (Master Quality Gates). Mỗi tiêu chí được phân tầng rõ ràng để định hình, thử thách và cưỡng bức AI Agent sản sinh mã nguồn chất lượng cao nhất.

---

## Tầng 1: Kiến trúc & Nền tảng (Foundation & Architecture)

*   **[DEV-1.01] SOLID - Single Responsibility Principle (Đơn nhiệm)**:
    *   *Mô tả*: Mỗi hàm hoặc phương thức chỉ được đảm nhận duy nhất một nhiệm vụ rõ ràng. Độ dài phần thân hàm không được phép vượt quá 50 dòng code thực thi.
*   **[DEV-1.02] Tài liệu hóa Hàm Public (Docstrings)**:
    *   *Mô tả*: Mọi hàm/phương thức public bắt buộc phải có docstring giải thích tham số đầu vào, kiểu dữ liệu trả về, và các ngoại lệ có thể sinh ra.
*   **[DEV-1.03] Tài liệu hóa Class**:
    *   *Mô tả*: Mọi Class mới phải chứa docstring mô tả chi tiết chức năng của Class đó trong kiến trúc chung.
*   **[DEV-1.04] Đặt tên Hàm chuẩn PEP 8**:
    *   *Mô tả*: Tên hàm phải viết hoàn toàn bằng chữ thường và ngăn cách bởi dấu gạch dưới (`snake_case`).
*   **[DEV-1.05] Đặt tên Class chuẩn PEP 8**:
    *   *Mô tả*: Tên Class phải viết bằng chuẩn `PascalCase` (chữ cái đầu viết hoa, viết liền).
*   **[DEV-1.06] Đặt tên Biến chuẩn PEP 8**:
    *   *Mô tả*: Tên biến phải viết bằng `snake_case` và có độ dài tối thiểu 3 ký tự (ngoại trừ biến vòng lặp chuẩn như `i`, `j`, `k`, `_`, `e`).
*   **[DEV-1.07] Tuyệt đối không nuốt Exception**:
    *   *Mô tả*: Nghiêm cấm sử dụng khối `except:` rỗng hoặc `except Exception: pass` nuốt chửng lỗi mà không ghi log hay xử lý.
*   **[DEV-1.08] Bảo vệ các Ranh giới Ngoại vi (Exception Boundaries)**:
    *   *Mô tả*: Các cuộc gọi I/O, database, API mạng phải được bọc trong các khối `try/except` có khoanh vùng cụ thể.
*   **[DEV-1.09] Context Manager cho File IO**:
    *   *Mô tả*: Chỉ mở file bằng cấu trúc context manager `with open(...) as f:` để tự động giải phóng mô tả file.
*   **[DEV-1.10] Đóng kết nối DB và Socket**:
    *   *Mô tả*: Đảm bảo mọi kết nối Socket và DB mở ra phải được đóng trong khối `finally` hoặc quản lý thông qua context manager.

---

## Tầng 2: Vận hành & Hiệu năng (Operational & Efficiency)

*   **[DEV-2.01] Bảo vệ tương tranh (Concurrency Lock)**:
    *   *Mô tả*: Khi làm việc với đa luồng (`threading` / `multiprocessing`), mọi thao tác ghi/đọc tài nguyên chia sẻ bắt buộc phải dùng Lock hoặc Semaphore.
*   **[DEV-2.02] Phòng tránh Deadlock tương tranh**:
    *   *Mô tả*: Không thực hiện các hành vi lock lồng nhau từ các đối tượng Lock khác nhau mà không sắp xếp thứ tự lock nhất quán.
*   **[DEV-2.03] Làm sạch Biến không sử dụng**:
    *   *Mô tả*: Không khai báo các biến cục bộ bên trong hàm mà không sử dụng trong logic tính toán sau đó.
*   **[DEV-2.04] Làm sạch Import thừa**:
    *   *Mô tả*: Loại bỏ toàn bộ các thư viện được import ở đầu file nhưng không bao giờ được gọi.
*   **[DEV-2.05] Không dùng Số ma thuật (Magic Numbers)**:
    *   *Mô tả*: Các giá trị số dùng trong tính toán (ngoại trừ -1, 0, 1) phải được khai báo dưới dạng HẰNG SỐ viết hoa.
*   **[DEV-2.06] Tránh Đường dẫn cứng (Hardcoded Paths)**:
    *   *Mô tả*: Không gán cứng đường dẫn tuyệt đối như `/home/steve/...` trong mã nguồn. Hãy dùng relative path hoặc cấu hình môi trường.
*   **[DEV-2.07] Bắt buộc có tệp Unit Test đi kèm**:
    *   *Mô tả*: Mỗi module chức năng phải đi kèm một file test tương ứng (ví dụ: `test_billing.py` cho `billing.py`).
*   **[DEV-2.08] Chất lượng Unit Test tối thiểu**:
    *   *Mô tả*: File unit test phải chứa ít nhất 5 test cases bao phủ đầy đủ các biên thành công, thất bại và dữ liệu bất thường.
*   **[DEV-2.09] Mocking cuộc gọi Ngoại vi**:
    *   *Mô tả*: Unit test không được phép gọi API mạng thật hoặc database production thật; bắt buộc sử dụng `unittest.mock`.
*   **[DEV-2.10] Sắp xếp Import chuẩn PEP 8**:
    *   *Mô tả*: Nhóm imports thành 3 khối phân biệt: Thư viện chuẩn, thư viện bên thứ ba, thư viện nội bộ cục bộ.

---

## Tầng 3: Kiểm soát Luồng & Độ phức tạp (Complexity & Flow Control)

*   **[DEV-3.01] Giới hạn Độ lồng Điều khiển (Nesting Depth)**:
    *   *Mô tả*: Độ lồng sâu của các khối điều kiện `if/for/while` không được vượt quá 3 lớp.
*   **[DEV-3.02] Giới hạn Độ phức tạp Cyclomatic**:
    *   *Mô tả*: Tổng số nhánh rẽ điều hướng trong một hàm đơn lẻ không được vượt quá chỉ số phức tạp 15.
*   **[DEV-3.03] An toàn Đệ quy**:
    *   *Mô tả*: Các hàm đệ quy bắt buộc phải có điều kiện dừng rõ ràng ở ngay những dòng đầu tiên của hàm.
*   **[DEV-3.04] Tránh Biến toàn cục khả biến**:
    *   *Mô tả*: Không chỉnh sửa trực tiếp giá trị của các biến toàn cục (global) từ bên trong hàm.
*   **[DEV-3.05] Bảo vệ Tham số mặc định khả biến**:
    *   *Mô tả*: Tuyệt đối không khai báo danh sách mặc định khả biến như `def func(data=[])`. Hãy sử dụng `None` và khởi tạo bên trong hàm.
*   **[DEV-3.06] Phòng chống Shell Injection**:
    *   *Mô tả*: Khi dùng `subprocess.run()`, cấm truyền `shell=True` trừ khi câu lệnh là hằng số hoàn toàn.
*   **[DEV-3.07] Phòng chống SQL Injection**:
    *   *Mô tả*: Không cộng chuỗi hay dùng f-string để dựng câu truy vấn SQL; bắt buộc dùng parameterized query.
*   **[DEV-3.08] Phòng chống Path Traversal**:
    *   *Mô tả*: Khi ghép đường dẫn, hãy xác thực độ an toàn bằng `os.path.abspath` và kiểm tra tiền tố thư mục được cho phép.
*   **[DEV-3.09] Mã hóa Bảo mật nâng cao**:
    *   *Mô tả*: Sử dụng băm dữ liệu an toàn như SHA-256 hoặc bcrypt, cấm sử dụng thuật toán lỗi thời MD5 hoặc SHA1 cho dữ liệu nhạy cảm.
*   **[DEV-3.10] Cấm gán cứng Mật khẩu / Secrets**:
    *   *Mô tả*: Mật khẩu, API Token, Private Key phải được lưu trữ trong biến môi trường `.env`, cấm viết trần trong code.

---

## Tầng 4: Clean Code & Chuẩn hóa (Clean Code & Hygiene)

*   **[DEV-4.01] Giới hạn Độ dài Class**:
    *   *Mô tả*: Mỗi Class định nghĩa mới không được vượt quá tổng số 300 dòng code.
*   **[DEV-4.02] Giới hạn Số tham số hàm**:
    *   *Mô tả*: Hàm không được nhận quá 5 đối số đầu vào. Nếu cần truyền nhiều hơn, hãy đóng gói thành Object.
*   **[DEV-4.03] Nhất quán Lệnh Return**:
    *   *Mô tả*: Trong một hàm, tránh viết lẫn lộn có return giá trị và return không giá trị hoặc không return.
*   **[DEV-4.04] Package Entry đầy đủ**:
    *   *Mô tả*: Thư mục chứa package thư viện nội bộ phải có file `__init__.py` hợp lệ.
*   **[DEV-4.05] Tránh trùng lặp mã nguồn (DRY)**:
    *   *Mô tả*: Tuyệt đối không copy-paste các khối code trên 10 dòng lặp lại; hãy cấu trúc hóa thành helper function dùng chung.
*   **[DEV-4.06] Khai báo Type Hints**:
    *   *Mô tả*: Hàm public bắt buộc phải có type hints cho tham số đầu vào và kiểu trả về (ví dụ: `def calculate(val: float) -> float:`).
*   **[DEV-4.07] Defensive Null/None checks**:
    *   *Mô tả*: Luôn kiểm tra None trước khi truy cập thuộc tính của các đối tượng động để tránh lỗi `AttributeError: 'NoneType' object`.
*   **[DEV-4.08] Thiết lập Timeout cho Network**:
    *   *Mô tả*: Cấm thực hiện các truy cập requests API mà không cấu hình đối số `timeout` rõ ràng.
*   **[DEV-4.09] Ghi log bằng Logging thay vì raw Print**:
    *   *Mô tả*: Chỉ dùng thư viện `logging` (ví dụ: `logging.error()`, `logging.info()`) để ghi log; cấm dùng hàm print() trần cho debug/lỗi production.
*   **[DEV-4.10] Xóa mã chết và comment hóa**:
    *   *Mô tả*: Loại bỏ toàn bộ các khối code cũ bị chuyển thành comment hoặc các hàm không còn bất kỳ nơi nào gọi sử dụng.
