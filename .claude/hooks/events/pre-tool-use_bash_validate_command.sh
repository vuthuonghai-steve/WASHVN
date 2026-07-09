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

# Pattern blocklist — restrict to canonical block devices; /dev/null, /dev/stdout, /dev/zero are safe.
DESTRUCTIVE_REGEX="(rm -rf|sudo |truncate -s 0|chmod -R|chown -R .* /|> */dev/(sd[a-z]+|nvme[0-9]+|disk[0-9]*|loop[0-9]+|ram[0-9]+|md[0-9]+)|of=/dev/(sd[a-z]+|nvme[0-9]+|disk[0-9]*|loop[0-9]+|ram[0-9]+|md[0-9]+))"
if echo "$CMD" | grep -qE "$DESTRUCTIVE_REGEX"; then
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
