#!/usr/bin/env bash
# SessionStart hook: record session metadata
# Input: { cwd, pid, boot_id, session_id }
# Exit 0 = allow session to start

# Graceful degradation: check jq
if ! command -v jq &>/dev/null; then
  exit 0
fi

INPUT=$(cat)

# Graceful degradation: check malformed JSON
if ! echo "$INPUT" | jq empty &>/dev/null; then
  exit 0
fi

CWD=$(echo "$INPUT" | jq -r '.cwd // empty' 2>/dev/null)
PID=$(echo "$INPUT" | jq -r '.pid // empty' 2>/dev/null)
BOOT_ID=$(echo "$INPUT" | jq -r '.boot_id // empty' 2>/dev/null)
SESSION_ID=$(echo "$INPUT" | jq -r '.session_id // empty' 2>/dev/null)

LOG_DIR=".skill-context/_state-archive"
if ! mkdir -p "$LOG_DIR" 2>/dev/null; then
  exit 0
fi

LOG="$LOG_DIR/session-start.log"
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

printf '%s\tSTART\tsession=%s\tpid=%s\tboot=%s\tcwd=%s\n' \
  "$TIMESTAMP" "$SESSION_ID" "$PID" "$BOOT_ID" "$CWD" >> "$LOG" 2>/dev/null

exit 0
