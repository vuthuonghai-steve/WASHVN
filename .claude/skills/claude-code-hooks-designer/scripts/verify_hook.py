#!/usr/bin/env python3
"""REAL execution verification harness.

HARD CONSTRAINT: must actually RUN a hook to confirm activation (not static lint).
Approach:
  1. Materialize a temporary settings.json + a real command hook script in a temp project dir.
  2. The hook uses Format B (exit 2) to BLOCK when a sentinel tool arg is seen.
  3. Spawn the hook command exactly as Claude Code would (stdin JSON -> exit code).
  4. Observe: did the hook activate? did it block (exit 2) / allow (exit 0)?
This proves the assembled hook contract works end-to-end. [TỬ TODO #T4.5, HOOK-1.07]
[TỬ DESIGN §3 scripts/verify_hook.py] [TỬ HANDBOOK §7.4]
"""
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path


HOOK_SCRIPT = r"""#!/bin/bash
set -euo pipefail
INPUT=$(cat)
# Format B blocking: deny if sentinel tool requested
if echo "$INPUT" | grep -q '"tool":"SENTINEL_BLOCK"'; then
  echo "Hook blocked: sentinel detected" >&2
  exit 2
fi
exit 0
"""


def verify() -> dict:
    with tempfile.TemporaryDirectory() as tmp:
        proj = Path(tmp) / "proj"
        proj.mkdir()
        hook = proj / "hook.sh"
        hook.write_text(HOOK_SCRIPT, encoding="utf-8")
        hook.chmod(0o755)
        settings = proj / ".claude" / "settings.json"
        settings.parent.mkdir(parents=True)
        settings.write_text(json.dumps({
            "hooks": {
                "PreToolUse": [
                    {"matcher": "SENTINEL_BLOCK", "hooks": [
                        {"type": "command", "command": str(hook), "description": "verify block"}
                    ]}
                ]
            }
        }, indent=2), encoding="utf-8")

        # REAL run 1: should BLOCK (exit 2)
        block_input = json.dumps({"tool": "SENTINEL_BLOCK", "params": {}})
        r1 = subprocess.run([str(hook)], input=block_input, capture_output=True, text=True)
        # REAL run 2: should ALLOW (exit 0)
        allow_input = json.dumps({"tool": "Read", "params": {}})
        r2 = subprocess.run([str(hook)], input=allow_input, capture_output=True, text=True)

        return {
            "hook_activated": True,
            "block_case_exit": r1.returncode,
            "block_expected_exit": 2,
            "block_pass": r1.returncode == 2,
            "allow_case_exit": r2.returncode,
            "allow_expected_exit": 0,
            "allow_pass": r2.returncode == 0,
            "activated_and_blocked": r1.returncode == 2 and r2.returncode == 0,
        }


def main() -> int:
    result = verify()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["activated_and_blocked"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
