#!/usr/bin/env bash
# Test: pre-tool-use_bash_validate_command.sh allows safe command
set -e
WORKSPACE_ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
JSON='{"tool_name":"Bash","tool_input":{"command":"ls -la"}}'
EXIT=0
echo "$JSON" | bash "$WORKSPACE_ROOT/.claude/hooks/events/pre-tool-use_bash_validate_command.sh" 2>/dev/null || EXIT=$?
[ "$EXIT" = "0" ] || { echo "FAIL: expected exit 0, got $EXIT"; exit 1; }
echo "PASS: hook allows safe command"
