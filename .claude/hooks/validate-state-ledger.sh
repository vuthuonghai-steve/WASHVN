#!/usr/bin/env bash
# [traced-to: agent-architecture.md §3-bis State Ledger Validation Hook]
# Path: .claude/hooks/validate-state-ledger.sh
# Trigger: PostToolUse trên Write|Edit match `_state_ledger.yaml` / `_ba_pipeline_state.yaml`
# Purpose: Ngăn pipeline tê liệt do YAML parse error / schema violation trước
#          khi agent kế tiếp đọc file hỏng (Λ-9 stage state leakage).
# Compat: `_ba_pipeline_state.yaml` legacy pattern được giữ để backward compat
#          trong quá trình migration → `_state_ledger.yaml` canonical naming.
# Cost: free — pure bash + python, không tốn model token.

set -euo pipefail

# Error handling trap
err_report() {
    echo "[VALIDATE-LEDGER-ERROR] Script failed at line $1" >&2
}
trap 'err_report $LINENO' ERR

log_debug() {
    # Luôn ghi ra stderr để hỗ trợ debug khi cần thiết
    echo "[DEBUG] [validate-state-ledger] $1" >&2
}

# 1) Kiểm tra dependencies
if ! command -v jq &>/dev/null; then
    echo "ERROR: jq is not available. Gating fail closed." >&2
    exit 2
fi

INPUT=$(cat)

# Kiểm tra JSON đầu vào hợp lệ
if ! echo "$INPUT" | jq empty &>/dev/null; then
    echo "ERROR: Malformed JSON input to validate-state-ledger.sh" >&2
    exit 2
fi

FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')

# Bỏ qua nếu không có file path
[ -z "$FILE_PATH" ] && exit 0

# Bỏ qua nếu không phải state_ledger
if [[ ! "$FILE_PATH" =~ _state_ledger\.yaml$ ]] && [[ ! "$FILE_PATH" =~ _ba_pipeline_state\.yaml$ ]]; then
    exit 0
fi

log_debug "Starting validation for: $FILE_PATH"

# 2) Chạy Python để kiểm tra cấu trúc YAML & Schema đồng thời (try-except bọc kỹ)
PYTHON_OUTPUT=$(python3 <<PYEOF
import yaml
import sys
import json

file_path = "$FILE_PATH"
try:
    with open(file_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
except yaml.YAMLError as ye:
    print(json.dumps({"status": "parse_fail", "reason": f"YAML Parse Error: {str(ye)}"}))
    sys.exit(0)
except Exception as e:
    print(json.dumps({"status": "read_fail", "reason": f"File read error: {str(e)}"}))
    sys.exit(0)

if not isinstance(data, dict):
    print(json.dumps({"status": "schema_fail", "reason": "Root element of state ledger must be a YAML dictionary"}))
    sys.exit(0)

required = ["schema_version", "skill_name", "mode", "current_stage", "stage_status", "artifacts"]
missing = [r for r in required if r not in data]

if missing:
    print(json.dumps({"status": "schema_fail", "reason": f"Missing required fields: {', '.join(missing)}"}))
    sys.exit(0)

print(json.dumps({"status": "success"}))
PYEOF
)

# Parse kết quả trả về từ Python script (chỉ lấy dòng cuối cùng đề phòng có cảnh báo/warning khác trước đó)
LAST_LINE=$(echo "$PYTHON_OUTPUT" | tail -n 1)
STATUS=$(echo "$LAST_LINE" | jq -r '.status // "error"' 2>/dev/null || echo "error")
REASON=$(echo "$LAST_LINE" | jq -r '.reason // "Unknown python validation error"' 2>/dev/null || echo "Unknown python validation error")

if [ "$STATUS" = "success" ]; then
    log_debug "Validation SUCCESS for $FILE_PATH"
    exit 0
fi

log_debug "Validation FAILED for $FILE_PATH: $REASON"

# Dùng jq để sinh ra JSON Format A chuẩn chỉnh, tự động escape mọi ký tự xuống dòng và nháy kép trong $REASON
jq -n \
  --arg file "$FILE_PATH" \
  --arg reason "$REASON" \
  '{
    hookSpecificOutput: {
      hookEventName: "PostToolUse",
      decision: "block",
      reason: ("State Ledger VALIDATION FAIL tại " + $file + ". Chi tiết: " + $reason + ". Agent ghi file phải auto-repair ngay trong turn tiếp theo — không để agent kế tiếp đọc file hỏng (Λ-9 stage state leakage).")
    }
  }'

exit 0
