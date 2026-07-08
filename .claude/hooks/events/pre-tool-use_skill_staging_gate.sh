#!/usr/bin/env bash
# Block writes to runtime .claude/skills/ unless explicit deploy_run
# Piped JSON stdin: { tool_name, tool_input: { file_path } }
# Exit 0 = allow, Exit 2 = block

# Graceful degradation: check jq
if ! command -v jq &>/dev/null; then
  echo "ERROR: jq is not available. Gating fail closed." >&2
  exit 2
fi

INPUT=$(cat)

# Graceful degradation: check malformed JSON
if ! echo "$INPUT" | jq empty &>/dev/null; then
  echo "ERROR: malformed stdin JSON. Gating fail closed." >&2
  exit 2
fi

FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty' 2>/dev/null)
[ -z "$FILE_PATH" ] && exit 0

# Block pattern: writes to .claude/skills/<any>/ except for _staging/
if [[ "$FILE_PATH" =~ \.claude/skills/ ]] && [[ ! "$FILE_PATH" =~ \.claude/skills/_staging/ ]]; then
  # Unless DEPLOY_PHASE_ACTIVE env var is set (reserved for deployflow)
  if [ -z "$WASHVN_DEPLOY_PHASE_ACTIVE" ]; then
    echo "BLOCKED: writes to runtime .claude/skills/ gated. Edit at raw/ver-3/<name>/ then deploy via 'deploy-skill <name>'." >&2
    exit 2
  fi
fi

exit 0
