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

# Scope to workspace root — bare substring match would catch $HOME/.claude/skills/ (false positive)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
RUNTIME_SKILLS_DIR="${WORKSPACE_ROOT}/.claude/skills/"
STAGING_SUBDIR="${WORKSPACE_ROOT}/.claude/skills/_staging/"

case "$FILE_PATH" in
  "$STAGING_SUBDIR"*)
    exit 0
    ;;
  "$RUNTIME_SKILLS_DIR"*)
    if [ -z "$WASHVN_DEPLOY_PHASE_ACTIVE" ]; then
      echo "[SKILL-STAGING-GATE] BLOCKED: direct writes to runtime .claude/skills/ gated." >&2
      echo "  path: $FILE_PATH" >&2
      echo "  Fix: edit at skills/ver-3/<name>/ then deploy via 'deploy-skill <name>'" >&2
      echo "  Bypass: set WASHVN_DEPLOY_PHASE_ACTIVE env var (reserved for deploy flow)" >&2
      exit 2
    fi
    ;;
esac

exit 0
