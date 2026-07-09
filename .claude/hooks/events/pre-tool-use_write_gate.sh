#!/usr/bin/env bash
# Gate: Write|Edit tool — block writes outside allowlisted paths
# Piped JSON stdin: { tool_name, tool_input: { file_path, content } }
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

# Fail-safe: if no file_path extracted (e.g., Bash tool), allow
[ -z "$FILE_PATH" ] && exit 0

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"

ALLOWED_DIRS_REGEX="^${WORKSPACE_ROOT}/(\.claude/|\.skill-context/|\.agents/|\.omc/|\.omo/|raw/|skills/|docs/|Temps/|scratch/)"
ALLOWED_ROOT_FILES_REGEX="^${WORKSPACE_ROOT}/(AGENTS|CLAUDE|architecture|standards|ROADMAP|workspce_tree)\.md$|^${WORKSPACE_ROOT}/skills-registry\.json$"

if [[ ! "$FILE_PATH" =~ $ALLOWED_DIRS_REGEX ]] && [[ ! "$FILE_PATH" =~ $ALLOWED_ROOT_FILES_REGEX ]]; then
  echo "[WORKSPACE-GATE] BLOCKED: write target outside WASHVN workspace: $FILE_PATH" >&2
  echo "  Allowed: .claude/, .skill-context/, .agents/, .omc/, .omo/, raw/, skills/, docs/, Temps/, scratch/, and root *.md / skills-registry.json" >&2
  exit 2
fi

exit 0
