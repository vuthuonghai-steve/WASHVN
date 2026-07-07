---
name: advanced-hooks-capability
description: Phân tích sâu về khả năng gọi Prompt-based và Agent-based hooks trong Claude Code
version: 0.0.1
suite: WASHVN
tags: [hooks, prompt-hook, agent-hook, advanced-capability, research]
when_to_use: "Khi cần thiết kế các chốt chặn sử dụng trí tuệ nhân tạo (LLM/Agent) để kiểm duyệt thay vì chỉ dùng shell script tĩnh"
---

# Khai Thác Khả Năng Nâng Cao của Hooks: Prompt-based & Agent-based Hooks

## 1. Bối Cảnh & Đặt Vấn Đề

Trong các kịch bản kiểm soát chất lượng và an toàn thông thường, các hook dạng shell script (`type: "command"`) với sự hỗ trợ của các công cụ như `grep` hay `jq` hoạt động rất tốt đối với các luật tĩnh (ví dụ: cấm đường dẫn cụ thể, cấm từ khóa lệnh phá hoại). 

Tuy nhiên, đối với các nghiệp vụ phức tạp đòi hỏi **khả năng suy luận ngữ nghĩa** hoặc **kiểm tra chéo trạng thái dự án**, các script shell tĩnh sẽ gặp giới hạn lớn hoặc trở nên cực kỳ cồng kềnh. Ví dụ:
- Đánh giá xem cuộc hội thoại đã thực sự hoàn thành tất cả các mục tiêu đề ra chưa trước khi đóng session (`Stop` event).
- Phân tích xem đoạn mã nguồn vừa được viết (`PostToolUse`) có tuân thủ đúng triết lý kiến trúc của dự án hay không.
- Phân tích ý định của một câu lệnh bash phức tạp để đánh giá mức độ rủi ro thay vì chặn regex thô thiển.

Để giải quyết vấn đề này, Claude Code cung cấp hai loại hook handler nâng cao: **Prompt-based hooks** (`type: "prompt"`) và **Agent-based hooks** (`type: "agent"`). Cả hai đều cho phép tích hợp "trí óc của LLM/Agent" trực tiếp vào quá trình ra quyết định chặn/cho phép (gating) của hook.

---

## 2. Đặc Tả Chi Tiết Prompt-based Hooks (`type: "prompt"`)

Prompt-based hooks gửi trực tiếp một yêu cầu dạng prompt tới mô hình ngôn ngữ (mặc định là mô hình nhanh - Haiku) để đánh giá sự kiện trong một lượt duy nhất (single-turn).

### 2.1 Cấu Hình Trong Settings JSON

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Đánh giá xem phiên làm việc đã hoàn thành chưa. Dữ liệu đầu vào: $ARGUMENTS. Trả về JSON: {\"ok\": true} để cho phép dừng, hoặc {\"ok\": false, \"reason\": \"lý do cụ thể\"} để tiếp tục.",
            "timeout": 120,
            "continueOnBlock": true
          }
        ]
      }
    ]
  }
}
```

### 2.2 Các Tham Số Quan Trọng
- **`prompt` (Bắt buộc)**: Đoạn văn bản hướng dẫn gửi tới LLM. Sử dụng placeholder `$ARGUMENTS` để Claude Code tự động chèn dữ liệu JSON đầu vào của sự kiện (chứa `session_id`, `tool_name`, `tool_input`, v.v.). Nếu không khai báo `$ARGUMENTS`, JSON đầu vào sẽ tự động được append vào cuối prompt.
- **`model` (Tùy chọn)**: Định nghĩa mô hình sẽ đánh giá prompt. Mặc định là mô hình nhanh (Haiku). Bạn có thể nâng cấp lên Sonnet nếu cần suy luận logic rất cao.
- **`timeout` (Tùy chọn)**: Giới hạn thời gian chạy tính bằng giây (mặc định là 30 giây).
- **`continueOnBlock` (Tùy chọn, mặc định `false`)**: Khi mô hình quyết định block (`ok: false`), tham số này quyết định xem có chuyển tiếp lý do block ngược lại cho Claude tiếp tục thực hiện công việc (turn) hay dừng/ngắt hoàn toàn session và cảnh báo người dùng.

### 2.3 Phản Hồi Từ Mô Hình (Response Schema)

Mô hình bắt buộc phải trả về một chuỗi JSON có định dạng sau:

```json
{
  "ok": true | false,
  "reason": "Giải thích chi tiết lý do đưa ra quyết định này"
}
```

- **`ok: true`**: Cho phép hành động/sự kiện tiếp tục diễn ra bình thường.
- **`ok: false`**: Chặn hành động/sự kiện lại. Trường `reason` là bắt buộc trong trường hợp này để cung cấp lý do chặn.

---

## 3. Đặc Tả Chi Tiết Agent-based Hooks (`type: "agent"`)

Agent-based hooks là một bước tiến xa hơn của prompt-based hooks. Thay vì chỉ đánh giá thông tin tĩnh được truyền vào, Claude Code sẽ **khởi tạo một subagent** chạy ẩn trong nền. Subagent này được trang bị đầy đủ các công cụ tìm kiếm và đọc file (`Read`, `Grep`, `Glob`) để chủ động khám phá codebase nhằm xác thực các điều kiện thực tế trước khi đưa ra quyết định.

### 3.1 Cấu Hình Trong Settings JSON

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write",
        "hooks": [
          {
            "type": "agent",
            "prompt": "Kiểm tra xem file chuẩn bị ghi có vi phạm các quy tắc kiến trúc không. Sử dụng công cụ Grep để tìm các import tương tự trong dự án nhằm đối chiếu bối cảnh. Dữ liệu sự kiện: $ARGUMENTS",
            "timeout": 90
          }
        ]
      }
    ]
  }
}
```

### 3.2 Quy Trình Hoạt Động Của Agent Hook
1. **Khởi chạy**: Sự kiện kích hoạt -> Spawn subagent với system prompt được cấu hình và tham số `$ARGUMENTS`.
2. **Tương tác nhiều lượt (Multi-turn)**: Subagent có thể chạy tối đa **50 lượt** gọi tool. Nó tự động sử dụng các công cụ đọc/quét mã nguồn để điều tra trạng thái dự án.
3. **Quyết định**: Kết thúc quá trình điều tra, subagent bắt buộc phải trả ra kết quả có cấu trúc `{ "ok": true }` hoặc `{ "ok": false, "reason": "lý do" }`.
4. **Hành động**: Claude Code tiếp nhận và xử lý quyết định tương tự như Prompt-based hook.

> [!WARNING]
> Agent-based hooks hiện tại là tính năng **thử nghiệm (experimental)**. Thời gian chạy của chúng thường lâu hơn (timeout mặc định 60 giây, có thể lên đến vài phút nếu subagent gọi nhiều tool), do đó chỉ nên áp dụng ở các chốt chặn quan trọng như `Stop` (kết thúc phiên) hoặc `PostToolBatch` để tránh làm chậm các lượt gõ lệnh hàng ngày.

---

## 4. Tác Động Của Quyết Định `ok: false` Theo Từng Sự Kiện

Hành vi khi prompt/agent hook trả về `ok: false` phụ thuộc rất lớn vào loại sự kiện mà nó đăng ký:

| Sự Kiện (Event) | Hành Vi Khi `ok: false` | Ứng Dụng Thực Tế Trong WASHVN |
|:---|:---|:---|
| `Stop` / `SubagentStop` | Trả lý do về cho Claude làm nhiệm vụ tiếp theo (Turn tiếp tục chạy, Claude tự động sửa lỗi). | **Chốt chặn nghiệm thu**: Bắt Claude tự sửa lỗi nếu phát hiện test bị fail hoặc tài liệu chưa cập nhật trước khi thoát. |
| `PreToolUse` | Chặn đứng việc gọi tool. Trả lỗi về cho model giống như block của shell script. | **Chốt chặn an toàn ngữ nghĩa**: Ngăn viết code phá vỡ cấu trúc thư mục hoặc vi phạm nguyên tắc SOLID. |
| `PostToolUse` | Kết thúc lượt gọi và hiển thị một thông điệp cảnh báo màu vàng trên giao diện chat. | **Cảnh báo chất lượng code**: Nhắc nhở lập trình viên các điểm cần lưu ý về code vừa viết mà không làm gián đoạn luồng làm việc. |
| `UserPromptSubmit` / `UserPromptExpansion` | Từ chối xử lý prompt của người dùng và hiển thị cảnh báo. | **Lọc Prompt đầu vào**: Ngăn chặn prompt injection hoặc yêu cầu lạc đề. |
| `TaskCreated` / `TaskCompleted` | Hủy bỏ / rollback việc tạo hoặc hoàn thành task. | **Kiểm tra tiến độ thực tế**: Ngăn model tự ý đánh dấu Task Done khi chưa chạy kiểm thử thực tế. |

---

## 5. Đề Xuất Ứng Dụng Cho Hệ Thống WASHVN Master Skill Suite

Để tích hợp tối ưu "trí óc của agent" vào hệ thống WASHVN, chúng ta nên định hình các kịch bản áp dụng sau:

### Kịch Bản 1: Đảm Bảo Định Dạng Tài Liệu Cấu Trúc (Stop Hook)
Sử dụng một **Prompt-based hook** tại sự kiện `Stop` để rà soát toàn bộ các tài liệu sinh ra trong phiên làm việc. Prompt sẽ yêu cầu mô hình quét cấu trúc để phát hiện xem có file Markdown nào vi phạm quy tắc: không có frontmatter YAML hoặc sử dụng dấu backticks bao ngoài clickable links (lỗi cực kỳ phổ biến của LLM).
- **Cấu hình**: `type: "prompt"`, `continueOnBlock: true`.
- **Hiệu quả**: Claude sẽ tự động sửa các lỗi định dạng tài liệu trước khi trả lại quyền điều khiển terminal cho Steve.

### Kịch Bản 2: Kiểm Tra Nghiệm Thu Kỹ Thuật (Agent-based Stop Hook)
Sử dụng một **Agent-based hook** tại sự kiện `Stop` để chạy lệnh test sandbox và đọc file logs. Subagent sẽ chạy `pytest` hoặc `validate_suite_integrity.py`, đọc output và đưa ra quyết định có cho phép dừng phiên hay bắt Claude phải debug tiếp.
- **Cấu hình**: `type: "agent"`, `timeout: 120`.
- **Hiệu quả**: Đảm bảo dự án luôn ở trạng thái "xanh" (Green) trước khi kết thúc phiên.

---

## 6. Kế Hoạch Tích Hợp Thử Nghiệm Vào Phase 2

Để đưa các tính năng nâng cao này vào thực tế một cách an toàn mà không ảnh hưởng tới tiến độ xây dựng standalone hook framework cơ bản (dùng Shell script), chúng ta đề xuất bổ sung thêm một Stage nghiên cứu và nghiệm thu vào kế hoạch triển khai của Phase 2:

1. **Stage 5: Nghiên cứu & Thử nghiệm Advanced Hooks**:
   - Thiết lập cấu hình thử nghiệm Prompt-based Hook tại sự kiện `Stop` trong file [.claude/settings.local.json](file:///home/stveve/Documents/workspace/build-workflow/WASHVN/.claude/settings.local.json).
   - Thiết lập kịch bản giả lập kiểm tra chất lượng file MD, ép mô hình trả về `{ "ok": false, "reason": "Thiếu frontmatter YAML ở file X" }` để kiểm tra khả năng tự sửa lỗi của Claude Code.
   - Viết tài liệu đánh giá hiệu năng (đo thời gian phản hồi thực tế của Haiku/Sonnet trong quá trình gating) để đưa ra quyết định ứng dụng chính thức cho các Phase sau.
