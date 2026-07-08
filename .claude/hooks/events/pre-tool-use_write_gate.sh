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

# Canonical allowlist (canonical paths, never modify without commit review)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
ALLOWLIST_REGEX="^${WORKSPACE_ROOT}/(\.claude/|raw/ver-3/|\.skill-context/|docs/context-to-work/|Temps/spec/)"

if [[ ! "$FILE_PATH" =~ $ALLOWLIST_REGEX ]]; then
  echo "BLOCKED: write target outside WASHVN workspace: $FILE_PATH" >&2
  echo "Allowed prefixes: .claude/, raw/ver-3/, .skill-context/, docs/context-to-work/, Temps/spec/" >&2
  exit 2
fi

exit 0
