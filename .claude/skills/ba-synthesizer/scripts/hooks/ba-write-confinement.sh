#!/usr/bin/env bash
# ba-write-confinement.sh — PreToolUse Write gate for ba-synthesizer.
# BLOCKS writes outside .skill-context/{feature}/ba-synthesizer/ (plus allowed
# quality-* artifacts). Exit 2 = block, 0 = allow.
# Hook input is JSON on stdin: { "params": { "filePath": "..." } }

set -euo pipefail

INPUT="$(cat)"
FILE_PATH="$(printf '%s' "$INPUT" | jq -r '.params.filePath // empty' 2>/dev/null || true)"

if [[ -z "$FILE_PATH" ]]; then
  exit 0
fi

# Allowed: inside .skill-context/{feature}/ba-synthesizer/
if [[ "$FILE_PATH" =~ \.skill-context/[^/]+/ba-synthesizer/ ]]; then
  exit 0
fi

# Allowed: quality-matrix.yaml / quality-report.md / defect-log.yaml (skill-internal QA artifacts)
if [[ "$FILE_PATH" =~ (quality-matrix\.yaml|quality-report\.md|defect-log\.yaml)$ ]]; then
  exit 0
fi

echo "BLOCKED: ba-synthesizer chỉ write .skill-context/{feature}/ba-synthesizer/ (hoặc quality-* artifacts)" >&2
exit 2
