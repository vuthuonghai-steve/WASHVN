#!/usr/bin/env python3
"""Bash validator hook — boundary test suite."""
import subprocess
import json
import os
import sys

WORKSPACE_ROOT = "/home/stveve/Documents/workspace/build-workflow/WASHVN"
HOOK = f"{WORKSPACE_ROOT}/.claude/hooks/events/pre-tool-use_bash_validate_command.sh"

PASS = 0
FAIL = 0

def check(cmd, expect, label):
    global PASS, FAIL
    payload = json.dumps({"tool_name": "Bash", "tool_input": {"command": cmd}})
    r = subprocess.run(["bash", HOOK], input=payload, capture_output=True, text=True)
    actual = r.returncode
    if actual == expect:
        print(f"PASS: {label}  expected={expect} actual={actual}")
        PASS += 1
    else:
        print(f"FAIL: {label}  expected={expect} actual={actual}  stderr={r.stderr.strip()[:80]}")
        FAIL += 1

# Construct destructive patterns at runtime to avoid self-match
rmrf = "rm " + "-" + "rf"
sudo = "su" + "do "
trunc = "truncate " + "-s 0"
chmod = "chmod " + "-R"
dd_of = "dd " + "if=/dev/zero of=/dev/n" + "vme0n1"
network_curl = "cu" + "rl https://example.com"
network_wget = "wg" + "et https://example.com"

# Should ALLOW (exit 0)
check("ls -la", 0, "safe command ls")
check("echo hi > /dev/null", 0, "redirect to /dev/null")
check("cat somefile > /dev/stdout", 0, "redirect to /dev/stdout")
check("echo go > /dev/stderr", 0, "redirect to /dev/stderr")
check("python3 ./run.py", 0, "python script run")
check("cd /home/user/work && ls", 0, "cd + ls")
check("git status", 0, "git status")
check("echo foo > /dev/zero", 0, "redirect to /dev/zero (safe)")

# Should BLOCK (exit 2)
check(f"{rmrf} /home", 2, f"rm -rf")
check(f"{sudo}apt install foo", 2, "sudo")
check(f"{trunc} bigfile", 2, "truncate -s 0")
check(f"{chmod} 777 /home", 2, "chmod -R")
check(f"echo data > /dev/s" + "da", 2, "overwrite /dev/sda")
check(f"echo data > /dev/s" + "db", 2, "overwrite /dev/sdb")
check(f"{dd_of} bs=1M", 2, "dd overwrite nvme device")
check(f"cat foo > /dev/loo" + "p0", 2, "overwrite /dev/loop0")
check(f"echo foo > /dev/dis" + "k0", 2, "overwrite /dev/disk0")
check(f"echo foo > /dev/r" + "am0", 2, "overwrite /dev/ram0")
check(f"{network_curl}", 2, "network curl")
check(f"{network_wget}", 2, "network wget")

# Bypass test — with MARK_NETWORK_ALLOWED=true, network should allow
env = os.environ.copy()
env['MARK_NETWORK_ALLOWED'] = 'true'
payload = json.dumps({"tool_name": "Bash", "tool_input": {"command": "cu" + "rl https://example.com"}})
r = subprocess.run(["bash", HOOK], input=payload, capture_output=True, text=True, env=env)
if r.returncode == 0:
    print(f"PASS: network curl with bypass env  expected=0 actual=0")
    PASS += 1
else:
    print(f"FAIL: network curl with bypass env  expected=0 actual={r.returncode}")
    FAIL += 1

print()
print(f"=== SUMMARY: {PASS} pass, {FAIL} fail ===")
sys.exit(1 if FAIL > 0 else 0)