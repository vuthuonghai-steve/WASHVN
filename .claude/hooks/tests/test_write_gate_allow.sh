#!/usr/bin/env bash
# Test: pre-tool-use_write_gate.sh allows workspace writes
set -e
WORKSPACE_ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
JSON="{\"tool_name\":\"Write\",\"tool_input\":{\"file_path\":\"$WORKSPACE_ROOT/skills/ver-3/test/SKILL.md\"}}"
EXIT=0
echo "$JSON" | bash "$WORKSPACE_ROOT/.claude/hooks/events/pre-tool-use_write_gate.sh" 2>/dev/null || EXIT=$?
[ "$EXIT" = "0" ] || { echo "FAIL: expected exit 0, got $EXIT"; exit 1; }
echo "PASS: hook allows write inside workspace"
