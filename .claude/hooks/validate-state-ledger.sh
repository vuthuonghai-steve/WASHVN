#!/usr/bin/env bash
# [traced-to: agent-architecture.md §3-bis State Ledger Validation Hook]
# Path: .claude/hooks/validate-state-ledger.sh
# Trigger: PostToolUse trên Write|Edit match `_state_ledger.yaml`
# Purpose: Ngăn pipeline tê liệt do YAML parse error / schema violation trước
#          khi agent kế tiếp đọc file hỏng (Λ-9 stage state leakage).
# Cost: free — pure bash + python, không tốn model token.

set -euo pipefail

INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')

# Bỏ qua nếu không phải state_ledger
[[ "$FILE_PATH" =~ _state_ledger\.yaml$ ]] || exit 0

# 1) YAML parse check
if ! python3 -c "import yaml, sys; yaml.safe_load(open(sys.argv[1]))" "$FILE_PATH" 2>/dev/null; then
  cat <<EOF
{
  "hookSpecificOutput": {
    "hookEventName": "PostToolUse",
    "decision": "block",
    "reason": "State Ledger YAML PARSE FAIL tại $FILE_PATH. Agent ghi file phải auto-repair ngay trong turn tiếp theo — không để agent kế tiếp đọc file hỏng (Λ-9 stage state leakage)."
  }
}
EOF
  exit 0
fi

# 2) Schema required-fields check
MISSING=$(python3 <<PYEOF
import yaml, sys
with open("$FILE_PATH") as f: data = yaml.safe_load(f)
required = ["schema_version", "skill_name", "mode", "current_stage", "stage_status", "artifacts"]
missing = [r for r in required if r not in data]
print(",".join(missing))
PYEOF
)

if [[ -n "$MISSING" ]]; then
  cat <<EOF
{
  "hookSpecificOutput": {
    "hookEventName": "PostToolUse",
    "decision": "block",
    "reason": "State Ledger SCHEMA FAIL — thiếu fields: $MISSING. Mọi agent có state_ledger_validation_hook=true phải re-Write với đầy đủ required_fields."
  }
}
EOF
  exit 0
fi

# 3) Pass — không can thiệp
exit 0
