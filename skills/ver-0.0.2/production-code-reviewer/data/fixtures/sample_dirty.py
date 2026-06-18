"""sample_dirty.py — fixture cố tình vi phạm nhiều Google review rules.

Dùng để self-test code_auditor.py: expect blocking_count > 0 và
exit_code = 1 khi chạy audit.
"""

import os
import json
import requests


# Hardcoded secret — REV-FUN-11
api_key = "sk-1234567890ABCDEFGHIJKLMNOP"
password = "super_secret_password_value"


def BadFunction(a, b, c, d, e, f, g):  # REV-STY-01, REV-CMP-01 (too many args)
    """Hàm này vi phạm naming + args count + length."""
    # Magic numbers
    if a > 1000:
        for x in range(len(b)):
            for y in range(len(c)):
                if d == 0:
                    if e is None:
                        try:
                            response = requests.get("https://api.example.com/data")  # REV-FUN-05
                            return response.json()
                        except:  # REV-FUN-02
                            pass  # Swallowed exception
    # Mutable default — REV-FUN-14
    return []


def open_file(path):  # REV-FUN-03, REV-FUN-04
    """Mở file thô mà không có with/try."""
    f = open(path, "r")
    return f.read()


# REV-CMT-03: TODO không có ticket ID
# TODO: fix this later

# Subprocess shell=True — REV-FUN-08
def run_command(user_input):
    import subprocess
    subprocess.run(f"echo {user_input}", shell=True)
