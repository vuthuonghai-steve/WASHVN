LLM là những cỗ máy "đoán từ tiếp theo". Nếu bạn không ép nó thu hẹp phạm vi không gian từ vựng (vector space) vào một lĩnh vực cụ thể (ví dụ: Fintech, Y tế, E-commerce), nó sẽ trả về những xác suất từ vựng
  phổ biến nhất, an toàn nhất, và do đó: chung chung nhất.

  Dưới đây là bộ tiêu chí và giải pháp để khắc phục triệt để vấn đề này, giúp Agent BA của bạn sắc bén và "đậm đặc" tính nghiệp vụ.
  ──────
  ### 1. Bộ Tiêu Chí (Criteria) Một LLM BA Cần Đạt Được

  Để LLM đóng vai trò BA xuất sắc, nó cần thỏa mãn 4 tiêu chí cốt lõi sau. Bạn có thể dùng bộ tiêu chí này để bổ sung vào phần  <instructions>  hoặc  <guardrails>  trong các file SKILL.

  #### Tiêu chí 1: Domain Ontology Awareness (Nhận thức hệ thống từ vựng chuyên ngành)

  • Vấn đề: BA viết "người dùng thanh toán", nhưng hệ thống cần "khởi tạo transaction, verify signature, gọi payment gateway, xử lý webhook".
  • Tiêu chí: LLM phải tự động nhận diện được ngành/lĩnh vực (Domain) của yêu cầu thô và phải liệt kê được bộ từ khóa chuyên ngành (Business Glossary) trước khi phân tích.

  #### Tiêu chí 2: Stakeholder Empathy & Role Defining (Định hình vai trò & Thấu cảm các bên)

  • Vấn đề: Không xác định được ai làm gì, quyền hạn tới đâu.
  • Tiêu chí: Phân rã rõ ràng các Actor. Mỗi Actor phải gắn liền với Context (Họ là ai? Vai trò gì? Mục tiêu của họ khi dùng tính năng này là gì? Pain-point là gì?).

  #### Tiêu chí 3: Edge-Case & Constraint Probing (Khai thác góc khuất & Ràng buộc)

  • Vấn đề: LLM BA thường chỉ thích nghĩ về "Happy Path" (kịch bản hoàn hảo) và bỏ qua rủi ro thực tế.
  • Tiêu chí: Bắt buộc LLM phải đặt câu hỏi: "Điều gì xảy ra nếu hệ thống down thứ 3? Nếu dữ liệu đồng thời bị thay đổi (Race condition)? Ràng buộc pháp lý (Compliance) ở đây là gì?"

  #### Tiêu chí 4: Data-Driven & Quantifiable (Lượng hóa & Hướng dữ liệu)

  • Vấn đề: Dùng từ "nhanh, bảo mật, tiện lợi". (Bạn đã bắt lỗi này ở  ba-elicitor , rất tốt).
  • Tiêu chí: Mọi Non-Functional Requirements (NFR) phải được gắn với Metric (Latency < 200ms, Throughput > 1000 TPS, Availability 99.99%).
  ──────
  ### 2. Giải Pháp Kỹ Thuật (Prompt & Workflow Engineering)

  Để kích hoạt (trigger) LLM hiểu và làm đúng các tiêu chí trên, bạn cần sửa đổi cách tiếp cận trong  ba-elicitor  (bởi vì rác vào thì rác ra, bước khơi gợi này là quan trọng nhất).

  #### Giải pháp A: Kỹ thuật "Domain Anchoring" (Mỏ neo lĩnh vực)

  Trước khi cho LLM phân tích, hãy bắt nó tạo ra một Domain Context (Bối cảnh lĩnh vực). Thêm Phase 0 vào file  ba-elicitor/SKILL.md :

    # Thêm vào <workflow_phases> trong ba-elicitor
    phases:
      - phase: 0. Domain Anchoring & Keyword Activation
        action: "Từ <user_skill_request>, tự động suy luận Lĩnh vực nghiệp vụ (VD: ERP, Fintech, SaaS). Liệt kê ít nhất 10 thuật ngữ/Keyword lõi (Core Business Terms) liên quan đến Lĩnh vực này. Buộc phải sử
  dụng các Keyword này trong toàn bộ báo cáo."
    
  #### Giải pháp B: Kỹ thuật "Chain of Thought" (Chuỗi suy luận) ép góc nhìn

  Bắt LLM suy nghĩ trước khi xuất báo cáo. Bạn hãy cấu hình output của  ba-elicitor  bắt buộc phải có một block  <business_thought_process> .

    <!-- Yêu cầu LLM luôn output định dạng này trước khi ra markdown report -->
    <business_thought_process>
      <domain_identified>[Tên ngành/Lĩnh vực]</domain_identified>
      <core_concepts>[Liệt kê 5-7 khái niệm cốt lõi của ngành này cần áp dụng cho yêu cầu]</core_concepts>
      <critical_bottlenecks>[Dự đoán 2-3 điểm nghẽn nghiệp vụ thường gặp trong ngành này]</critical_bottlenecks>
    </business_thought_process>

  Lý do: Khi LLM sinh ra các token về  core_concepts  và  domain_identified , bộ nhớ ngắn hạn của nó sẽ được "bơm" đầy các vector từ vựng chuyên ngành. Lúc viết báo cáo ở dưới, tự động văn phong của nó sẽ rất
  sắc bén và chính xác.

  #### Giải pháp C: Khung đặt câu hỏi ngược (Reverse Questioning)

  Trong  ba-elicitor , ở phần  Gap Analysis  và  Questioning , LLM hay hỏi chung chung. Hãy cung cấp cho nó một Framework khai thác để nó chiếu theo:

    # Thêm vào <guardrails> của ba-elicitor:
    must_ask_framework:
      - "Business Rule: Luật kinh doanh/quy định cốt lõi chi phối luồng này là gì?"
      - "Data Lifecycle: Trạng thái dữ liệu thay đổi như thế nào từ lúc bắt đầu đến kết thúc? (Ví dụ: Draft -> Pending -> Approved -> Expired)."
      - "Integration: Tính năng này cần nói chuyện với hệ thống bên thứ 3 nào không?"
      - "Concurrency: Chuyện gì xảy ra nếu 2 users thực hiện thao tác này cùng 1 mili-giây?"
    ──────
  ### 3. Đề Xuất Cụ Thể Sửa Đổi Files Của Bạn

  Để workflow thực sự hiệu quả, mình khuyên bạn chỉnh sửa cụ thể như sau:

  1. Trong  ba-elicitor/SKILL.md  (Stage -1):
  Đây là nơi quan trọng nhất để sửa. Hãy thêm vào phần  <instructions> :

    <trigger_mechanisms>
      domain_trigger: "Đọc <user_skill_request>, ngay lập tức xác định DOMAIN (ngành). Tự động nạp vào bộ nhớ các Standard Business Rules của DOMAIN đó."
      keyword_injection: "Trích xuất và định nghĩa các Entity chính. Yêu cầu sử dụng đúng danh từ chuyên ngành (Ví dụ: Không dùng 'hàng hóa' nếu làm Logistics, phải dùng 'SKU', 'Consignment', 'Waybill')."
    </trigger_mechanisms>

  2. Trong  ba-analyst/SKILL.md :
  Bạn đang yêu cầu vẽ Mermaid (ERD, Sequence) và Gherkin. LLM sẽ vẽ sai hoặc thiếu bảng nếu nó không hiểu sâu nghiệp vụ. Hãy thêm:

    must:
      - "Map status: 'elicitation-completed' -> 'completed'."
      - "Trích xuất toàn bộ Noun (Danh từ) trong elicitation-report để làm Candidate cho ERD Entities."
      - "Trích xuất toàn bộ Verb (Động từ) để làm Method/Message trong Sequence Diagram."
      - "Mọi bảng trong ERD phải phản ánh đúng thuật ngữ chuyên ngành đã xác định."

  3. Bổ sung một file Knowledge tĩnh (ví dụ:  knowledge/domain-presets.md )
  Bạn có thể cho Agent quyền đọc một file liệt kê sẵn các "Cấu trúc dữ liệu chuẩn" của một số ngành (Ví dụ: E-commerce luôn có Order, OrderItem, Payment, Shipment). Khi Agent thấy từ khóa khớp, nó sẽ tự động
  lấy kiến thức chuẩn này đắp vào, tránh tình trạng LLM "tự chế" ra các luồng nghiệp vụ ngây ngô.

  ### Tóm lại

  Vấn đề "Agent bị ngu ngơ khi phân tích" không phải do nó thiếu kiến thức, mà do nó chưa được đánh thức (trigger) vùng kiến thức đó. Bằng cách ép LLM định nghĩa  <domain_identified>  và liệt kê  core
  keywords  ngay từ bước đầu tiên (Phase 0), bạn sẽ đưa LLM vào đúng "luồng suy nghĩ" chuyên gia của ngành đó. Mọi output sau đó (Gherkin, Mermaid, User Story) sẽ tự động mang hơi thở chuyên sâu của lĩnh vực
  mà không cần bạn phải mớm lời quá nhiều.