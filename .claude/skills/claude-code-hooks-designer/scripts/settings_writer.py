#!/usr/bin/env python3
"""AUTO-WRITE settings.json — backup / diff-preview / fail-closed / rollback.

HARD CONSTRAINT (task + design §8 R3 + HOOK-1.06): every write is IRREVERSIBLE.
This module enforces:
  1. backup-before-write (timestamped)
  2. diff preview (returned, caller must confirm)
  3. fail-closed: on write failure -> restore from backup atomically
  4. never-stale: abort if target changed since backup
  5. rollback(target) -> restore last backup

Primitive only: file I/O, json, hashlib. No business logic.
[TỬ TODO #T4.3] [TỬ DESIGN §3 scripts/settings_writer.py] [TỬ HANDBOOK §7.3]
"""
import hashlib
import json
import shutil
import sys
import tempfile
from datetime import datetime
from pathlib import Path


def _checksum(path: Path) -> str:
    if not path.exists():
        return "missing"
    return hashlib.sha256(path.read_bytes()).hexdigest()


def backup(target: Path) -> Path:
    """Copy target to timestamped backup. Returns backup path."""
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup_path = target.with_name(f"settings.backup.{ts}.json")
    if target.exists():
        shutil.copy2(target, backup_path)
    else:
        backup_path.write_text("{}", encoding="utf-8")
    return backup_path


def diff_preview(target: Path, fragment: dict) -> str:
    """Return a human-readable diff of target vs target+merge(fragment)."""
    current = json.loads(target.read_text(encoding="utf-8") or "{}") if target.exists() else {}
    merged = _merge(current, fragment)
    lines = ["--- current hooks ---", json.dumps(current.get("hooks", {}), indent=2),
             "+++ after merge ---", json.dumps(merged.get("hooks", {}), indent=2)]
    return "\n".join(lines)


def _merge(base: dict, fragment: dict) -> dict:
    """Merge fragment.hooks into base.hooks (Claude Code merge semantics)."""
    out = json.loads(json.dumps(base))
    out.setdefault("hooks", {})
    for event, groups in fragment.get("hooks", {}).items():
        out["hooks"].setdefault(event, [])
        out["hooks"][event].extend(groups)
    return out


def write(target: Path, fragment: dict, backup_path: Path, confirm: bool) -> dict:
    """Fail-closed write. Returns {ok, restored, reason}."""
    if not confirm:
        return {"ok": False, "restored": False, "reason": "user did not confirm diff"}
    # never-stale: target must match backup
    if target.exists() and _checksum(target) != _checksum(backup_path):
        return {"ok": False, "restored": True,
                "reason": "NEVER-STALE: target changed since backup; restore+abort",
                "restored_path": str(backup_path)}
    merged = _merge(
        json.loads(target.read_text(encoding="utf-8") or "{}") if target.exists() else {},
        fragment,
    )
    tmp = target.with_suffix(target.suffix + ".tmp")
    try:
        tmp.write_text(json.dumps(merged, indent=2, ensure_ascii=False), encoding="utf-8")
        # validate JSON round-trip
        json.loads(tmp.read_text(encoding="utf-8"))
        shutil.move(str(tmp), str(target))
        return {"ok": True, "restored": False, "reason": "written"}
    except Exception as exc:  # fail-closed
        if tmp.exists():
            tmp.unlink()
        shutil.copy2(backup_path, target)  # restore
        return {"ok": False, "restored": True,
                "reason": f"write failed ({exc}); restored from backup"}


def rollback(target: Path, backup_path: Path) -> dict:
    """Undo last write by restoring backup."""
    try:
        shutil.copy2(backup_path, target)
        return {"ok": True, "reason": f"restored {backup_path}"}
    except Exception as exc:
        return {"ok": False, "reason": str(exc)}


def main() -> int:
    if len(sys.argv) < 3:
        print("usage: settings_writer.py <target.json> <fragment.json> [--confirm]", file=sys.stderr)
        return 2
    target = Path(sys.argv[1]).expanduser()
    fragment = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))
    confirm = "--confirm" in sys.argv
    bp = backup(target)
    print(f"BACKUP: {bp}")
    print("--- DIFF PREVIEW ---")
    print(diff_preview(target, fragment))
    if not confirm:
        print("DRY-RUN: pass --confirm to write.")
        return 0
    res = write(target, fragment, bp, confirm=True)
    print(json.dumps(res, ensure_ascii=False))
    return 0 if res["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
