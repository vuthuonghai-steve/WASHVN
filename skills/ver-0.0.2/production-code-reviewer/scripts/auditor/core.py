"""Core orchestrator — walks the AST, dispatches visitors, aggregates violations."""

from __future__ import annotations

import ast
from pathlib import Path
from typing import Any

from . import checks
from .visitors import (
    _ParentMixin,
    NamingVisitor,
    FunctionShapeVisitor,
    ExceptionVisitor,
    CallVisitor,
    AssignmentVisitor,
    ClassLengthVisitor,
)


def _attach_parents(tree: ast.AST) -> None:
    """Augment every AST node with a .parent pointer (used by context checks)."""
    _ParentMixin.attach(tree)


def _collect_unused_imports(tree: ast.AST) -> list[dict]:
    """REV-STY-04: detect imports that are never referenced."""
    imported: dict[str, int] = {}
    used: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imported[alias.asname or alias.name] = node.lineno
        elif isinstance(node, ast.ImportFrom):
            for alias in node.names:
                imported[alias.asname or alias.name] = node.lineno
        elif isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
            used.add(node.id)
    violations: list[dict] = []
    for name, line in imported.items():
        if name not in used and not name.startswith("_"):
            violations.append(checks.make_violation(
                "REV-STY-04", "Unused Import", line,
                f"Module/hàm '{name}' được import nhưng không sử dụng.",
                f"Xóa dòng import '{name}' để giữ code sạch.",
            ))
    return violations


def audit_file_content(file_path: str) -> dict:
    """Run the full audit pipeline on a single Python file.

    Returns a dict with: file, total_lines, violations_count, blocking_count,
    violations, exit_code. exit_code is 0 for PASS, 1 for any blocking issue,
    2 for unrecoverable errors (file missing, syntax error).
    """
    path = Path(file_path)
    if not path.exists():
        return {"error": f"File not found: {file_path}", "exit_code": 2, "violations": []}

    try:
        content = path.read_text(encoding="utf-8")
    except OSError as exc:
        return {"error": f"Cannot read file: {exc}", "exit_code": 2, "violations": []}

    lines = content.split("\n")
    total_lines = len(lines)
    sink: list[dict] = []

    # ---- Parse AST and walk visitors ----
    try:
        tree = ast.parse(content)
        _attach_parents(tree)
        for visitor in (
            NamingVisitor(sink),
            FunctionShapeVisitor(sink),
            ExceptionVisitor(sink),
            CallVisitor(sink),
            AssignmentVisitor(sink),
            ClassLengthVisitor(sink),
        ):
            visitor.visit(tree)
        sink.extend(_collect_unused_imports(tree))
    except SyntaxError as se:
        sink.append(checks.make_violation(
            "REV-FUN-01", "Compilation Error", se.lineno or 1,
            f"Mã nguồn lỗi cú pháp: {se.msg}",
            "Khắc phục lỗi cú pháp để mã nguồn chạy được.",
        ))

    # ---- Line-level regex checks ----
    for idx, line in enumerate(lines, start=1):
        v = checks.check_unregistered_todo(line, idx)
        if v: sink.append(v)
        v = checks.check_long_line(line, idx)
        if v: sink.append(v)

    # ---- Cross-module heuristics ----
    v = checks.check_threading_without_lock(content)
    if v: sink.append(v)
    v = checks.check_missing_test_file(file_path, path)
    if v: sink.append(v)

    # ---- Aggregate ----
    blocking = [x for x in sink if x["severity"] == "blocking"]
    return {
        "file": str(file_path),
        "total_lines": total_lines,
        "violations_count": len(sink),
        "blocking_count": len(blocking),
        "violations": sink,
        "exit_code": 1 if blocking else 0,
    }


def audit_file(file_path: str) -> dict:
    """Public alias — mirrors the old monolithic signature."""
    return audit_file_content(file_path)
