#!/usr/bin/env bash
# anti-recursion.sh — PreToolUse Task gate for ba-synthesizer.
# Blocks recursive spawn of ba-pipeline-runner. Exit 2 = block, 0 = allow.
# Hook input is JSON on stdin: { "params": { "subagent_type": "..." } }

set -euo pipefail

INPUT="$(cat)"
SUB_TYPE="$(printf '%s' "$INPUT" | jq -r '.params.subagent_type // empty' 2>/dev/null || true)"

if [[ "$SUB_TYPE" = "ba-pipeline-runner" ]]; then
  echo "BLOCKED: recursive ba-pipeline-runner spawn" >&2
  exit 2
fi

exit 0
