#!/usr/bin/env bash
# [traced-to: agent-architecture.md §3-bis State Ledger Validation Hook]
# Path: .claude/hooks/validate-state-ledger.sh
# Trigger: PostToolUse trên Write|Edit match `_state_ledger.yaml` / `_ba_pipeline_state.yaml`
# Purpose: Ngăn pipeline tê liệt do YAML parse error / schema violation / false completion
#          trước khi agent kế tiếp đọc file hỏng (Λ-9 stage state leakage).
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

# 2) Chạy Python để kiểm tra cấu trúc YAML, Schema & Grounding Artifact Verification trên đĩa
PYTHON_OUTPUT=$(python3 <<PYEOF
import yaml
import sys
import json
import os

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

# Schema Detection: Canonical vs Legacy BA Pipeline State
is_canonical = "skill_name" in data or "schema_version" in data
is_ba_legacy = "feature_name" in data or "_ba_pipeline_state" in file_path

if not (is_canonical or is_ba_legacy):
    print(json.dumps({"status": "schema_fail", "reason": "State ledger must contain 'skill_name' (canonical) or 'feature_name' (legacy)"}))
    sys.exit(0)

if is_canonical:
    req = ["current_stage"]
    missing = [r for r in req if r not in data]
    if missing:
        print(json.dumps({"status": "schema_fail", "reason": f"Missing required fields in state ledger: {', '.join(missing)}"}))
        sys.exit(0)
elif is_ba_legacy:
    req = ["feature_name", "stages", "current_stage"]
    missing = [r for r in req if r not in data]
    if missing:
        print(json.dumps({"status": "schema_fail", "reason": f"Missing required fields in BA pipeline state: {', '.join(missing)}"}))
        sys.exit(0)

# Deterministic Grounding Verification: Verify that artifacts for completed stages actually exist on disk with real content
stages_dict = data.get("stages", {})
if isinstance(stages_dict, dict):
    for stage_name, stage_info in stages_dict.items():
        if not isinstance(stage_info, dict):
            continue
        status = str(stage_info.get("status", "")).lower()
        gate_result = str(stage_info.get("gate_result", "")).lower()

        is_completed = status in ["completed", "pass", "passed", "done"] or gate_result in ["pass", "passed"]

        if is_completed:
            artifacts = []
            if "artifact" in stage_info:
                art = stage_info["artifact"]
                if isinstance(art, str):
                    artifacts.append(art)
                elif isinstance(art, list):
                    artifacts.extend(art)
            if "artifacts" in stage_info:
                arts = stage_info["artifacts"]
                if isinstance(arts, list):
                    for item in arts:
                        if isinstance(item, str):
                            artifacts.append(item)
                        elif isinstance(item, dict) and "path" in item:
                            artifacts.append(item["path"])
                elif isinstance(arts, str):
                    artifacts.append(arts)

            for art_path in artifacts:
                abs_art = art_path if os.path.isabs(art_path) else os.path.abspath(os.path.join(os.getcwd(), art_path))
                if not os.path.exists(abs_art):
                    print(json.dumps({
                        "status": "false_completion_fail",
                        "reason": f"FALSE COMPLETION DETECTED in stage '{stage_name}'! Marked as '{status}', but declared artifact '{art_path}' DOES NOT EXIST on disk."
                    }))
                    sys.exit(0)
                if os.path.getsize(abs_art) <= 10:
                    print(json.dumps({
                        "status": "false_completion_fail",
                        "reason": f"FALSE COMPLETION DETECTED in stage '{stage_name}'! Marked as '{status}', but declared artifact '{art_path}' is empty or stub (size {os.path.getsize(abs_art)}B <= 10B)."
                    }))
                    sys.exit(0)

top_artifacts = data.get("artifacts", [])
if isinstance(top_artifacts, list):
    for item in top_artifacts:
        if isinstance(item, dict) and str(item.get("status", "")).lower() in ["completed", "pass", "passed", "done"]:
            art_path = item.get("path")
            if art_path:
                abs_art = art_path if os.path.isabs(art_path) else os.path.abspath(os.path.join(os.getcwd(), art_path))
                if not os.path.exists(abs_art):
                    print(json.dumps({
                        "status": "false_completion_fail",
                        "reason": f"FALSE COMPLETION DETECTED in root artifacts list! Declared artifact '{art_path}' marked completed but DOES NOT EXIST on disk."
                    }))
                    sys.exit(0)
                if os.path.getsize(abs_art) <= 10:
                    print(json.dumps({
                        "status": "false_completion_fail",
                        "reason": f"FALSE COMPLETION DETECTED in root artifacts list! Declared artifact '{art_path}' is empty/stub (size {os.path.getsize(abs_art)}B <= 10B)."
                    }))
                    sys.exit(0)

print(json.dumps({"status": "success"}))
PYEOF
)

# Parse kết quả trả về từ Python script
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
      reason: ("State Ledger VALIDATION FAIL tại " + $file + ". Chi tiết: " + $reason + ". Agent ghi file phải auto-repair ngay trong turn tiếp theo — không để agent báo cáo hoàn thành ảo khi chưa tạo file thực tế (Λ-9 stage state leakage).")
    }
  }'

exit 0
