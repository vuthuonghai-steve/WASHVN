"""AST visitors that wire checks.py to the actual tree walk.

Pattern: each visitor method calls the corresponding check function from
checks.py and forwards any violation to a shared sink.
"""

from __future__ import annotations

import ast
from typing import Any, Callable

from . import checks


class _ParentMixin(ast.NodeVisitor):
    """Adds parent pointers to every node in the tree."""

    @staticmethod
    def attach(tree: ast.AST) -> None:
        for node in ast.walk(tree):
            for child in ast.iter_child_nodes(node):
                child.parent = node  # type: ignore[attr-defined]


def _inside(node: ast.AST, kind: type) -> bool:
    """Walk up the parent chain looking for a node of the given type."""
    while hasattr(node, "parent"):
        node = node.parent  # type: ignore[attr-defined]
        if isinstance(node, kind):
            return True
    return False


class NamingVisitor(ast.NodeVisitor):
    """Check class + function naming (REV-STY-01, REV-STY-02)."""

    def __init__(self, sink: list[dict]) -> None:
        self.sink = sink

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        v = checks.check_class_naming(node)
        if v: self.sink.append(v)
        self.generic_visit(node)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        v = checks.check_function_naming(node)
        if v: self.sink.append(v)
        self.generic_visit(node)


class FunctionShapeVisitor(ast.NodeVisitor):
    """Check function-level rules: docstring, length, args, mutable defaults, nesting."""

    def __init__(self, sink: list[dict]) -> None:
        self.sink = sink

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        for check in (
            checks.check_docstring,
            checks.check_function_length,
            checks.check_too_many_args,
            checks.check_mutable_default,
            checks.check_nesting_depth,
        ):
            v = check(node)
            if v: self.sink.append(v)
        self.generic_visit(node)


class ExceptionVisitor(ast.NodeVisitor):
    """Check exception handlers for swallowed errors."""

    def __init__(self, sink: list[dict]) -> None:
        self.sink = sink

    def visit_ExceptHandler(self, node: ast.ExceptHandler) -> None:
        v = checks.check_swallowed_exception(node)
        if v: self.sink.append(v)
        self.generic_visit(node)


class CallVisitor(ast.NodeVisitor):
    """Check risky call patterns: open, requests, subprocess."""

    def __init__(self, sink: list[dict]) -> None:
        self.sink = sink

    def visit_Call(self, node: ast.Call) -> None:
        # open()
        is_with = _inside(node, ast.With)
        is_try = _inside(node, ast.Try)
        for v in checks.check_open_without_with(node, is_with, is_try):
            self.sink.append(v)
        # requests / socket
        v = checks.check_network_no_timeout(node)
        if v: self.sink.append(v)
        # subprocess
        v = checks.check_subprocess_shell_true(node)
        if v: self.sink.append(v)
        self.generic_visit(node)


class AssignmentVisitor(ast.NodeVisitor):
    """Check assignment rules: hardcoded secrets."""

    def __init__(self, sink: list[dict]) -> None:
        self.sink = sink

    def visit_Assign(self, node: ast.Assign) -> None:
        v = checks.check_hardcoded_secret(node)
        if v: self.sink.append(v)
        self.generic_visit(node)


class ClassLengthVisitor(ast.NodeVisitor):
    """Check class body length (REV-DES-08, optional severity)."""

    def __init__(self, sink: list[dict]) -> None:
        self.sink = sink

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        end = getattr(node, "end_lineno", None)
        length = (end - node.lineno + 1) if end else 0
        if length > checks.MAX_CLASS_LINES:
            self.sink.append(checks.make_violation(
                "REV-DES-08", "Excessive Class Length", node.lineno,
                f"Class '{node.name}' quá dài ({length} dòng), vượt {checks.MAX_CLASS_LINES} dòng.",
                "Tách Class thành các sub-class hoặc helper gọn hơn.",
                severity="optional",
            ))
        self.generic_visit(node)
