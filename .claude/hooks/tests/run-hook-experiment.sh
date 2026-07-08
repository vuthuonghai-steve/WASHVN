#!/usr/bin/env bash
# Wrapper to run the Python hook experiment script
set -e
WORKSPACE_ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
python3 "$WORKSPACE_ROOT/.claude/hooks/tests/run-hook-experiment.py"
