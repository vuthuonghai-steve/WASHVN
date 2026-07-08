#!/usr/bin/env bash
# Audit-logs every artifact write (no enforcement, just side-effect)
# Input: { tool_name, tool_input, tool_output }
# Exit 0 = allow output

# Graceful degradation: check jq
if ! command -v jq &>/dev/null; then
  exit 0
fi

INPUT=$(cat)

# Graceful degradation: check malformed JSON
if ! echo "$INPUT" | jq empty &>/dev/null; then
  exit 0
fi

TOOL=$(echo "$INPUT" | jq -r '.tool_name // empty' 2>/dev/null)
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty' 2>/dev/null)

[ -z "$FILE_PATH" ] && exit 0

# Audit log path
LOG_DIR=".skill-context/_state-archive"
if ! mkdir -p "$LOG_DIR" 2>/dev/null; then
  exit 0
fi

LOG="$LOG_DIR/tool-audit-$(date +%Y-%m-%d).log"
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
AGENT="${CLAUDE_AGENT_NAME:-parent}"

printf '%s\tWRITE\tpid=%s\tagent=%s\ttool=%s\tpath=%s\n' \
  "$TIMESTAMP" "$$" "$AGENT" "$TOOL" "$FILE_PATH" >> "$LOG" 2>/dev/null

exit 0
