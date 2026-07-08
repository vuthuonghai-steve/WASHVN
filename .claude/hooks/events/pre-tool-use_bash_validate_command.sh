#!/usr/bin/env bash
# Block destructive bash patterns: rm -rf, truncate, dd of=, mv over, sudo, ...
# Piped JSON stdin: { tool_name, tool_input: { command } }
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

CMD=$(echo "$INPUT" | jq -r '.tool_input.command // empty' 2>/dev/null)
[ -z "$CMD" ] && exit 0

# Pattern blocklist for destructive commands
if echo "$CMD" | grep -qE "(rm -rf|sudo |truncate -s 0|dd of=/dev/|chmod -R|chown -R .* /|> */dev/)"; then
  echo "BLOCKED: destructive pattern detected in Bash command" >&2
  echo "Command snippet: $(echo "$CMD" | head -c 200)" >&2
  exit 2
fi

# Phase-specific gate: block running external network from commands unless bypass is set
if echo "$CMD" | grep -qE "(curl|wget|nc )"; then
  # Only allowed if env MARK_NETWORK_ALLOWED is set to true
  if [ -z "$MARK_NETWORK_ALLOWED" ] || [ "$MARK_NETWORK_ALLOWED" != "true" ]; then
    echo "BLOCKED: network access requires MARK_NETWORK_ALLOWED env var to be set to true" >&2
    exit 2
  fi
fi

exit 0
