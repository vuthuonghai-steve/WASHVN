Dưới đây là một bài phân tích chuyên sâu về các nhược điểm, rủi ro và các điểm yếu còn tồn đọng trong bản thiết kế này:
1. Đánh đổi trong cơ chế Gộp Giai đoạn (Phase Compression) ở Nhánh A
Để giải quyết sự cồng kềnh (over-engineering) cho các tác vụ đơn giản, bản thiết kế đã gộp 8 stages tuyến tính thành 3 phases
. Dù giảm được số lần gọi LLM (LLM calls), cơ chế này mang lại những nhược điểm rõ rệt:
Mất đi khả năng cô lập lỗi (Loss of Isolation): Trước đây, lỗi ở stage nào sẽ được cô lập ở stage đó. Với Phase Compression, một Agent đóng vai trò kết hợp (combined role) phải chịu trách nhiệm cho toàn bộ phase. Nếu có lỗi nhỏ, nó có thể ảnh hưởng dây chuyền đến toàn bộ các artifact trong phase đó
.
Mất đi khả năng tái sử dụng (Loss of Reusability): Các phase gộp luôn phải chạy một cách trọn vẹn (full run). Hệ thống không thể bỏ qua (skip) hoặc chỉ gọi lại một bước nhỏ (sub-step) bên trong nó nếu cần
.
Mất tính chi tiết của ma trận Fallback: Ma trận khôi phục lỗi chi tiết F1-F9 bị gộp thành các vòng lặp thử lại nội bộ (internal retry loop) PC-1 đến PC-4
. Điều này làm giảm khả năng theo dõi (traceability) nguyên nhân lỗi gốc ở cấp độ từng tác vụ nhỏ
.
Tiết kiệm Token không tuyến tính: Dù giảm 62.5% số lần gọi LLM (từ 8 xuống 3), lượng token thực tế chỉ giảm được khoảng 50%
. Lý do là prompt của các phase gộp phải gánh thêm rất nhiều hướng dẫn (instructions) cho nhiều vai trò cùng lúc (ví dụ: Agent vừa làm Architect vừa làm Gatekeeper), làm prompt phình to lên ~150%
.
2. Rủi ro từ lỗ hổng "PASS-form nhưng FAIL-meaning"
Hệ thống sử dụng Drift Detector (Stage 2.5) để đảm bảo kế hoạch (todo.md) khớp với thiết kế (design.md)
. Tuy nhiên, bản thiết kế thừa nhận một lỗ hổng nghiêm trọng:
Kiểm chứng mù về mặt ngữ nghĩa (Semantic Blindness): Drift Detector hoạt động hoàn toàn dựa trên cấu trúc (structural presence). Nó chỉ đếm xem các mẫu (patterns) như cấu trúc dữ liệu, ranh giới thư mục có tồn tại hay không, chứ không hiểu ý nghĩa nghiệp vụ của chúng
. Một LLM đủ khôn ngoan có thể sao chép y hệt định dạng để vượt qua vòng kiểm tra này dù logic bên trong hoàn toàn sai lệch
.
Dựa dẫm vào xác suất của Sampling Audit: Để vá lỗ hổng này, hệ thống thêm lớp Semantic Sampling Audit
. Tuy nhiên, mặc định lớp này chỉ kiểm tra ngẫu nhiên 20% số lượng kế hoạch (có thể giảm xuống 10% nếu hệ thống đánh giá LLM đang làm tốt)
. Điều này đồng nghĩa với việc 80% - 90% kế hoạch vẫn có nguy cơ mang vỏ bọc hoàn hảo nhưng sai lệch về mặt ngữ nghĩa lọt xuống cho Builder xây dựng. Hơn nữa, nếu kích hoạt chế độ "Human Audit", hệ thống sẽ tạo ra điểm nghẽn cổ chai (bottleneck) do phải chờ con người can thiệp
.
3. Khe hở chất lượng từ các "Soft Gates" (Chốt chặn mềm)
Nhằm tránh việc Pipeline bị dừng cứng (Hard Halt) và bảo vệ ngữ cảnh nghiệp vụ, một số chốt chặn chất lượng đã bị hạ cấp xuống thành "Soft Gate". Điều này vô tình để lại rác trong hệ thống:
Ngân sách Token (Token Budget): Yêu cầu file SKILL.md phải <= 700 tokens được chuyển thành Soft Gate (BUILD-3.1)
. Nếu Builder tạo ra một file quá dài và cồng kềnh, hệ thống không chặn build mà chỉ đưa ra cảnh báo để con người tối ưu bằng tay
. Việc này có thể dẫn đến hiện tượng phình to ngữ cảnh (context bloat) cho các agent downstream.
Mật độ từ khóa rác (Placeholder Density): Chốt chặn BUILD-2.1 cho phép cảnh báo khi code có quá nhiều từ khóa rác (TODO, FIXME, pass) (>= 10 lần) nhưng không hề đánh rớt (fail) quá trình build
. LLM vẫn có thể tạo ra các đoạn mã "mock" hoặc chưa hoàn thiện mà vẫn lọt qua bước Delivery.
4. Phát hiện lỗi chậm trễ và phụ thuộc vào kiểm tra thủ công (Reflection Cache)
Bản thiết kế tách thought-cache.yaml (chứa tư duy sâu) ra khỏi hydrated-context.yaml (chứa hợp đồng kỹ thuật) để tiết kiệm token cho Planner
. Tuy nhiên:
Bỏ lọt lỗi ở Stage 1.7: Context Hydrator (Stage 1.7) hoàn toàn không chạm vào thought-cache.yaml
.
Fallback tốn kém: Hệ thống chỉ nhận ra file thought-cache.yaml bị thiếu hoặc rỗng khi luồng chạy đến tận Stage 3 (Builder Phase 1)
. Lúc này, các fallback F16, F17, F18 sẽ bị trigger thủ công bởi Builder, bắt buộc hệ thống phải quay ngược toàn bộ quy trình về lại Stage 0 (BA Elicitor) để moi móc lại thông tin
. Đây là một sự lãng phí rất lớn về thời gian chờ và token do lỗi không được bắt ngay từ đầu.
5. Rủi ro từ "Graceful Degradation" (Suy giảm nhẹ nhàng) của YAML Resilience
Lớp YAML Resilience được đưa vào để ngăn toàn bộ hệ thống bị treo cứng (Hard Halt) do một lỗi lùi dòng YAML (indentation)
.
Nhược điểm nằm ở Level 3: Cross-reference Check
. Khi phát hiện một liên kết bị hỏng (dangling ref), thay vì báo lỗi cứng, hệ thống cho phép các stage tiếp theo bỏ qua (skip) luôn bước phụ thuộc vào tài liệu đó
.
Ví dụ: Nếu orchestration-plan bị hỏng, Orchestrator sẽ bỏ qua kế hoạch điều phối và chỉ build như một single skill
. Hoặc nếu quality-matrix bị hỏng, Planner sẽ bỏ qua cổng chất lượng và dùng cấu hình mặc định
. Tính năng "khoan dung" này tiềm ẩn rủi ro rất cao: hệ thống vẫn báo hoàn thành (build-completed) nhưng sản phẩm đầu ra thực chất bị thiếu chức năng, thiếu cổng chất lượng hoặc gãy kiến trúc điều phối.
6. Độ phức tạp trong việc vận hành và bảo trì (Maintenance Burden)
Bản thân tài liệu kiến trúc đã tự minh chứng cho sự cồng kềnh của hệ thống:
Phân mảnh tri thức: File kiến trúc gốc ban đầu dài 1300 dòng, nặng 60KB
. Dù đã được phân rã thành nhiều file đặc tả nhỏ lẻ (Context Bus, Phase Compression, Reflection Cache, Orchestrator...) để tối ưu cho LLM
, nó lại tạo ra gánh nặng khổng lồ cho kỹ sư vận hành (Human Operator). Mọi thay đổi ở một stage giờ đây phải được kiểm tra chéo (cross-link) qua hàng loạt các file YAML, ma trận Fallback và biểu đồ trạng thái (State Diagram) để đảm bảo không có xung đột
.
Overhead từ quá nhiều Agent phụ trợ: Sự xuất hiện của hàng loạt các subagent như YAML Auto-repair Agent
, Spec Gatekeeper
, Drift Detector
, và Oracle Audit
 khiến một quy trình build đơn giản cũng phải gọi (invoke) LLM hàng chục lần. Dù hệ thống ngăn chặn được rác (slop) của AI, nhưng cái giá phải trả là độ trễ (latency) tổng thể cực kỳ cao và tiêu hao một lượng lớn chi phí vận hành mô hình.