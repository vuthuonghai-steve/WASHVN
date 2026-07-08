#!/usr/bin/env bash
# Test: pre-tool-use_bash_validate_command.sh blocks network access without bypass
set -e
WORKSPACE_ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
JSON='{"tool_name":"Bash","tool_input":{"command":"curl https://example.com"}}'
EXIT=0
# Ensure MARK_NETWORK_ALLOWED is unset/empty
unset MARK_NETWORK_ALLOWED
echo "$JSON" | bash "$WORKSPACE_ROOT/.claude/hooks/events/pre-tool-use_bash_validate_command.sh" 2>/dev/null || EXIT=$?
[ "$EXIT" = "2" ] || { echo "FAIL: expected exit 2, got $EXIT"; exit 1; }
echo "PASS: hook blocks unauthorized network command"
