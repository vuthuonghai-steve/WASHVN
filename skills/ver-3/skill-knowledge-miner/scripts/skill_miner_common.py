#!/usr/bin/env python3
"""
skill_miner_common.py — Shared utilities for skill-knowledge-miner scripts

Provides safe file I/O, structured logging, and YAML output.
Used by: mine_for_terms.py, find_antipatterns.py
"""

import os
import sys
import json
from datetime import datetime
from enum import Enum


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
MAX_FILE_SIZE = 512 * 1024  # 512 KB — safety limit to prevent OOM


# ---------------------------------------------------------------------------
# Structured Logger
# ---------------------------------------------------------------------------
class LogLevel(Enum):
    ERROR = "ERROR"
    WARN = "WARN"
    INFO = "INFO"
    DEBUG = "DEBUG"


class Logger:
    """Structured logger with levels and timestamps"""

    def __init__(self, name, verbose=False):
        self.name = name
        self.verbose = verbose

    def _log(self, level, msg, force=False):
        if not (force or self.verbose or level in (LogLevel.ERROR, LogLevel.WARN)):
            return
        ts = datetime.now().strftime("%H:%M:%S")
        print(f"[{ts}] [{level.value}] [{self.name}] {msg}", file=sys.stderr)

    def error(self, msg):
        self._log(LogLevel.ERROR, msg, force=True)

    def warn(self, msg):
        self._log(LogLevel.WARN, msg, force=True)

    def info(self, msg):
        self._log(LogLevel.INFO, msg, force=False)

    def debug(self, msg):
        self._log(LogLevel.DEBUG, msg, force=False)


# ---------------------------------------------------------------------------
# Safe File Reading
# ---------------------------------------------------------------------------
def read_file_safely(fpath, logger=None):
    """
    Read a file with size guard and detailed error logging.

    Returns content str on success, None on error / oversize.
    """
    try:
        size = os.path.getsize(fpath)
        if size > MAX_FILE_SIZE:
            if logger:
                logger.warn(
                    f"File {fpath} exceeds {MAX_FILE_SIZE // 1024}KB"
                    f" limit ({size // 1024}KB). Skipping."
                )
            return None
    except OSError as e:
        if logger:
            logger.error(f"Cannot stat {fpath}: {e}")
        return None

    try:
        with open(fpath, "r", encoding="utf-8", errors="replace") as f:
            return f.read()
    except (IOError, PermissionError) as e:
        if logger:
            logger.error(f"Cannot read {fpath}: {e}")
        return None


# ---------------------------------------------------------------------------
# Single-pass File Collection
# ---------------------------------------------------------------------------
def collect_scannable_files(scan_dirs, extensions, logger=None):
    """
    Walk all scan_dirs once, collecting files matching *extensions*.

    Skips: dot-dirs, __pycache__, node_modules, cache, logs.
    """
    files = []
    for scan_dir in scan_dirs:
        if not os.path.isdir(scan_dir):
            continue
        for root, dirs, fnames in os.walk(scan_dir):
            dirs[:] = [
                d
                for d in dirs
                if not d.startswith(".")
                and d not in ("__pycache__", "node_modules", "cache", "logs")
            ]
            for fname in fnames:
                if fname.endswith(extensions):
                    files.append(os.path.join(root, fname))
    if logger and logger.verbose:
        logger.info(f"Collected {len(files)} files")
    return files


# ---------------------------------------------------------------------------
# Safe YAML Output
# ---------------------------------------------------------------------------
def write_yaml_safely(outpath, items, key_name, logger=None):
    """
    Write items as YAML using JSON inline serialization.

    json.dumps correctly escapes special characters, newlines, and Unicode —
    unlike manual string formatting which produces malformed YAML.
    """
    try:
        with open(outpath, "w", encoding="utf-8") as f:
            f.write(f"# Auto-extracted {key_name} ({len(items)} items)\n")
            f.write(f"{key_name}:\n")
            for item in items:
                inline = json.dumps(item, ensure_ascii=False)
                f.write(f"  - {inline}\n")
        if logger:
            logger.info(f"Wrote {len(items)} {key_name} to {outpath}")
        return True
    except IOError as e:
        if logger:
            logger.error(f"Cannot write {outpath}: {e}")
        return False
