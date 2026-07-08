#!/usr/bin/env bash
# Stop hook: log session termination status to audit and handle YAML resilience
# Input: { stop_hook_active }
# Exit 0 = allow stop

INPUT=$(cat)

# Graceful degradation: check jq
JQ_AVAILABLE=true
if ! command -v jq &>/dev/null; then
  JQ_AVAILABLE=false
fi

# Graceful degradation: check malformed JSON
if [ "$JQ_AVAILABLE" = "true" ]; then
  if ! echo "$INPUT" | jq empty &>/dev/null; then
    JQ_AVAILABLE=false
  fi
fi

STOP_ACTIVE="false"
if [ "$JQ_AVAILABLE" = "true" ]; then
  STOP_ACTIVE=$(echo "$INPUT" | jq -r '.stop_hook_active // false' 2>/dev/null)
fi

LOG_DIR=".skill-context/_state-archive"
LOG=""
if mkdir -p "$LOG_DIR" 2>/dev/null; then
  LOG="$LOG_DIR/session-$(date +%Y-%m-%d).log"
  TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
  if [ "$JQ_AVAILABLE" = "true" ]; then
    printf '%s\tSTOP\tstop_hook_active=%s\n' "$TIMESTAMP" "$STOP_ACTIVE" >> "$LOG" 2>/dev/null
  else
    printf '%s\tSTOP\tstop_hook_active=unknown\n' "$TIMESTAMP" >> "$LOG" 2>/dev/null
  fi
fi

STATE_FILE=".skill-context/_state.yaml"
if [ -f "$STATE_FILE" ] && [ -s "$STATE_FILE" ]; then
  if ! command -v python3 &>/dev/null; then
    if [ -n "$LOG" ]; then
      echo "WARNING: python3 not available — skip YAML check" >> "$LOG" 2>/dev/null
    fi
  else
    # Check if pyyaml is installed
    if ! python3 -c "import yaml" &>/dev/null; then
      if [ -n "$LOG" ]; then
        echo "WARNING: pyyaml not available — skip YAML check" >> "$LOG" 2>/dev/null
      fi
    else
      # Check syntax using safe_load
      if ! python3 -c "import yaml; yaml.safe_load(open('$STATE_FILE'))" &>/dev/null; then
        TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
        BACKUP="$LOG_DIR/_state-${TIMESTAMP}-corrupt.yaml"
        if cp "$STATE_FILE" "$BACKUP" 2>/dev/null; then
          if [ -n "$LOG" ]; then
            echo "STATE CORRUPT: backed up to $BACKUP before any re-init" >> "$LOG" 2>/dev/null
          fi
        else
          if [ -n "$LOG" ]; then
            echo "WARNING: backup corrupt _state.yaml failed" >> "$LOG" 2>/dev/null
          fi
        fi
      fi
    fi
  fi
fi

exit 0
