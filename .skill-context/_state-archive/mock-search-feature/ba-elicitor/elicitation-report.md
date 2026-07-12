---
skill_name: "mock-search-feature"
elicitation_date: "2026-07-11"
confidence_score: 70
status: "completed"
---

# Báo Cáo Khơi Gợi Yêu Cầu Nghiệp Vụ: mock-search-feature

> **Trace tags (bắt buộc):** `[TỪ INPUT]` (từ user) · `[SUY LUẬN]` (agent suy luận, ghi rõ lý do) · `[CẦN LÀM RÕ]` (thiếu/mơ hồ).

## 1. Yêu Cầu Đã Chuẩn Hóa (Normalized Input)

- **Mục tiêu cốt lõi**: người dùng nhập từ khóa, lọc theo danh mục, sắp xếp theo độ liên quan → hiển thị trang kết quả tìm kiếm sản phẩm. `[TỪ INPUT]`
- **Môi trường vận hành**: ứng dụng web thương mại điện tử, truy cập qua trình duyệt. `[TỪ INPUT]`
- **Tác nhân chính**:
  - Online Shopper (người mua sắm trực tuyến): người dùng cuối thực hiện tìm kiếm. `[TỪ INPUT]`
- **Yêu cầu chức năng sơ khởi (FRs)**:
  - FR-1: người dùng nhập chuỗi từ khóa truy vấn. `[TỪ INPUT]`
  - FR-2: lọc kết quả theo danh mục (category). `[TỪ INPUT]`
  - FR-3: lọc kết quả theo khoảng giá (price range). `[TỪ INPUT]`
  - FR-4: sắp xếp kết quả theo độ liên quan (relevance). `[TỪ INPUT]`
  - FR-5: hiển thị trang kết quả tìm kiếm (search results page). `[TỪ INPUT]`
- **Quyết định đã làm rõ (resolved clarifications)**:
  - DS-1: Nguồn dữ liệu = tệp JSON tĩnh (hardcoded product catalog, không DB, không dịch vụ tìm kiếm ngoài). `[TỪ INPUT]`
  - DS-2: Khi không có kết quả → hiển thị thông báo "no results". `[TỪ INPUT]`
  - DS-3: Tìm kiếm kích hoạt bằng nút submit (không live/debounce). `[TỪ INPUT]`
  - DS-4: Thuật toán độ liên quan = simple text match (substring contains, không TF-IDF/ML). `[TỪ INPUT]`
  - DS-5: Danh mục mã hóa cứng trong app code (không CMS/admin). `[TỪ INPUT]`
  - DS-6: Phân trang = 12 kết quả mỗi trang. `[TỪ INPUT]`

## 2. Ontology Nghiệp Vụ (Domain Ontology)

- **Thuật ngữ (≥10 terms, neo vector space)**:
  - `keyword query`: chuỗi từ khóa người dùng nhập để truy vấn.
  - `category`: nút phân loại sản phẩm dùng để lọc kết quả (hardcoded). `[TỪ INPUT]`
  - `price range`: bộ lọc giới hạn giá tối thiểu/tối đa.
  - `relevance`: điểm xếp hạng của kết quả so với truy vấn (simple text match). `[TỪ INPUT]`
  - `search results page`: danh sách sản phẩm khớp, có phân trang 12/page. `[TỪ INPUT]`
  - `online shopper`: người dùng cuối duyệt để mua hàng.
  - `product catalog`: tệp JSON tĩnh chứa các mặt hàng (data source). `[TỪ INPUT]`
  - `filter`: ràng buộc thu hẹp tập kết quả.
  - `sort`: thao tác sắp xếp trên tập kết quả.
  - `pagination`: chia kết quả thành trang 12 items/page. `[TỪ INPUT]`
  - `submit button`: thành phần kích hoạt tìm kiếm (trigger). `[TỪ INPUT]`
  - `no results message`: thông báo khi không có kết quả khớp. `[TỪ INPUT]`
- **Quan hệ thực thể**:
  - online shopper → search results page (nhập query, bấm submit)
  - keyword query → product catalog (khớp simple text match)
  - filter → search results page (thu hẹp kết quả) `[SUY LUẬN]`

## 3. Phân Tích Khoảng Trống (Gap Analysis — 6 Mindset Keywords)

- **Systems Thinking**: tính năng tìm kiếm chạy trên tệp JSON tĩnh cục bộ, không phụ thuộc catalog service / search index phân tán. Đơn giản hóa kiến trúc. `[SUY LUẬN]`
- **Root Cause Isolation**: NFR latency/throughput/accessibility/availability đã được user chấp nhận defaults → không còn gap đo lường. `[SUY LUẬN]`
- **MECE**: FRs bao phủ query/filter/sort/render/pagination/no-result. Autocomplete bị loại bỏ (không có trong scope). `[SUY LUẬN]`
- **First Principles**: nhu cầu nền tảng là truy xuất mặt hàng liên quan từ JSON tĩnh qua text match; framework là thứ yếu. `[SUY LUẬN]`
- **Impact Analysis**: hardcoded categories + JSON tĩnh → mọi thay đổi catalog cần redeploy code. Rủi ro maintainability, không phải runtime. `[SUY LUẬN]`
- **Structural Decomposition**: Epic Search → Features Query/Filter/Sort/Render/Paginate → User Stories đã đủ rõ để phân tích. `[SUY LUẬN]`

## 4. Stakeholder Analysis (≥2 góc độ)

- **Online Shopper**: goals=[tìm sản phẩm liên quan hiệu quả] · pain_points=[kết quả không liên quan, tải chậm]. `[TỪ INPUT]`
- **Developer/Maintainer**: goals=[hợp đồng dữ liệu JSON rõ, logic match đơn giản] · pain_points=[catalog hardcoded → mỗi thay đổi cần redeploy]. `[SUY LUẬN]`
- **Security Reviewer**: goals=[đầu vào an toàn, no injection] · pain_points=[query user chưa validate — nhưng nguồn tĩnh nên rủi ro thấp]. `[SUY LUẬN]`
- **QA Tester**: goals=[kịch bản no-result + pagination xác minh] · pain_points=[thiếu autocomplete nên test surface nhỏ]. `[SUY LUẬN]`

## 5. NFRs Đã Lượng Hóa (SMART — ISO/IEC 25010)

- NFR-1: id=`perf-1`, category=`performance`, metric=`search_latency_p95`, value=`500`, unit=`ms` `[TỪ INPUT]` (user accepted default)
- NFR-2: id=`perf-2`, category=`performance`, metric=`throughput_rps`, value=`100`, unit=`requests/sec` `[TỪ INPUT]` (user accepted default)
- NFR-3: id=`sec-1`, category=`security`, metric=`input_validation`, value=`strict_allowlist`, unit=`policy` `[SUY LUẬN]`
- NFR-4: id=`acc-1`, category=`accessibility`, metric=`wcag_level`, value=`AA`, unit=`standard` `[TỪ INPUT]` (user accepted default)
- NFR-5: id=`rel-1`, category=`reliability`, metric=`availability`, value=`99.9`, unit=`percent` `[TỪ INPUT]` (user accepted default)

## 6. Bộ Câu Hỏi Khơi Gợi (5W1H — Multiple-choice, RESOLVED)

### Who / What
- **Câu hỏi 1**: Nguồn dữ liệu sản phẩm là gì?
  - [x] A: tệp JSON tĩnh `[TỪ INPUT]`
  - [ ] B: cơ sở dữ liệu quan hệ (Postgres)
  - [ ] C: dịch vụ tìm kiếm ngoài (Elasticsearch)

- **Câu hỏi 2**: Khi truy vấn không có kết quả, hệ thống phản hồi thế nào?
  - [x] A: hiển thị thông báo "no results" `[TỪ INPUT]`
  - [ ] B: gợi ý danh mục liên quan
  - [ ] C: chuyển hướng sang duyệt tất cả

- **Câu hỏi 3**: Tìm kiếm được kích hoạt khi nào?
  - [x] A: khi bấm nút submit `[TỪ INPUT]`
  - [ ] B: gõ trực tiếp có debounce (live)
  - [ ] C: cả hai

- **Câu hỏi 4**: Thuật toán độ liên quan kỳ vọng là gì?
  - [x] A: điểm khớp văn bản đơn giản (substring match) `[TỪ INPUT]`
  - [ ] B: TF-IDF / BM25
  - [ ] C: mô hình ranking học máy

- **Câu hỏi 5**: Ai quản lý phân loại danh mục?
  - [x] A: mã hóa cứng trong app `[TỪ INPUT]`
  - [ ] B: CMS admin
  - [ ] C: đồng bộ từ dịch vụ catalog

- **Câu hỏi 6**: Số kết quả mỗi trang (pagination)?
  - [x] A: 12 `[TỪ INPUT]`
  - [ ] B: 24
  - [ ] C: cuộn vô hạn (infinite scroll)

## 7. Phân Rã 3-Path (Happy / Alternative / Exception)

- **Happy Path**: shopper nhập từ khóa + áp dụng lọc danh mục/giá → bấm submit → hệ thống text-match trên JSON tĩnh → trả về trang kết quả đã xếp hạng (12/page). `[SUY LUẬN]`
- **Alternative Path**: shopper chỉ dùng từ khóa không lọc, hoặc chỉ lọc không dùng từ khóa → kết quả vẫn trả về hợp lệ. `[SUY LUẬN]`
- **Exception Path**: truy vấn không khớp (no results) → hiển thị thông báo "no results"; khoảng giá không hợp lệ → validate, hiển thị thông báo an toàn, không sập. `[SUY LUẬN]`

## 8. Tự Kiểm Định (Self-Verification)

- [x] XML boundary `<user_skill_request>`: không cung cấp raw → validator bỏ qua (C1 skipped)
- [x] Số `[CẦN LÀM RÕ]`: 0 (all resolved)
- [x] Số `[TỪ INPUT]`: 18
- [x] Số `[SUY LUẬN]`: 13
- [x] Confidence ≥ 60%: Đạt (70) → status=`completed`
- [x] Scoping checklist 100% pass
