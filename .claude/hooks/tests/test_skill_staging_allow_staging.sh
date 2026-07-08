#!/usr/bin/env bash
# Test: pre-tool-use_skill_staging_gate.sh allows writes to skills staging
set -e
WORKSPACE_ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
JSON="{\"tool_name\":\"Write\",\"tool_input\":{\"file_path\":\"$WORKSPACE_ROOT/.claude/skills/_staging/test.md\"}}"
EXIT=0
echo "$JSON" | bash "$WORKSPACE_ROOT/.claude/hooks/events/pre-tool-use_skill_staging_gate.sh" 2>/dev/null || EXIT=$?
[ "$EXIT" = "0" ] || { echo "FAIL: expected exit 0, got $EXIT"; exit 1; }
echo "PASS: hook allows skill staging write"
