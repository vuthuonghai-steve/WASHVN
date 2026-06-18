"""Concrete check functions for the 68 Google review rules.

Each check is a callable that receives a context dict and returns either:
- None  (rule passed)
- dict  (violation, with keys: rule_id, name, line, severity, error, fix_hint)

The core orchestrator in core.py binds these checks to AST visitor hooks.
"""

from __future__ import annotations

import ast
import re
from typing import Any, Optional


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_SECRET_KEYS = ("api_key", "secret", "token", "password", "private_key")
_PASCAL_CASE = re.compile(r"^[A-Z][a-zA-Z0-9]*$")
_SNAKE_CASE = re.compile(r"^[a-z_][a-z0-9_]*$")
_TODO_PATTERN = re.compile(r"TODO\([a-zA-Z0-9\-]+\):")
_NETWORK_MODULES = ("requests", "socket")
_NETWORK_METHODS = ("get", "post", "put", "delete", "connect")
_SHELL_METHODS = ("run", "Popen", "call")

MAX_FUNCTION_LINES = 50
MAX_FUNCTION_ARGS = 5
MAX_NESTING_DEPTH = 3
MAX_CLASS_LINES = 300
MAX_LINE_LENGTH = 100


def make_violation(rule_id: str, name: str, line: int, error: str, fix_hint: str, severity: str = "blocking") -> dict:
    """Construct a violation dict. Centralized so format stays consistent."""
    return {
        "id": rule_id,
        "name": name,
        "line": line,
        "severity": severity,
        "error": error,
        "fix_hint": fix_hint,
    }


# ---------------------------------------------------------------------------
# Naming & style
# ---------------------------------------------------------------------------

def check_class_naming(node: ast.ClassDef) -> Optional[dict]:
    """REV-STY-02: PascalCase class names."""
    if _PASCAL_CASE.match(node.name):
        return None
    return make_violation(
        "REV-STY-02", "Class Naming Style", node.lineno,
        f"Tên Class '{node.name}' không đúng chuẩn PascalCase.",
        "Đổi tên Class thành chữ cái đầu viết hoa, ví dụ: 'AdvancedBilling'.",
    )


def check_function_naming(node: ast.FunctionDef) -> Optional[dict]:
    """REV-STY-01: snake_case function names."""
    if _SNAKE_CASE.match(node.name):
        return None
    return make_violation(
        "REV-STY-01", "Function Naming Style", node.lineno,
        f"Tên hàm '{node.name}' không tuân thủ snake_case chuẩn PEP 8.",
        "Đổi tên hàm thành chữ thường ngăn cách bởi dấu gạch dưới, ví dụ: 'calculate_billing_total'.",
    )


def check_long_line(line: str, line_number: int) -> Optional[dict]:
    """REV-CMP-10: lines over MAX_LINE_LENGTH."""
    if len(line) <= MAX_LINE_LENGTH:
        return None
    return make_violation(
        "REV-CMP-10", "Long Expression Splitting", line_number,
        f"Dòng {line_number} dài {len(line)} ký tự (tối đa {MAX_LINE_LENGTH}).",
        "Tách dòng thành nhiều dòng ngắn hơn sử dụng line continuation hoặc intermediate variables.",
        severity="nit",
    )


# ---------------------------------------------------------------------------
# Function shape
# ---------------------------------------------------------------------------

def check_docstring(node: ast.AST) -> Optional[dict]:
    """REV-CMT-02: missing docstring on public ClassDef/FunctionDef."""
    name = getattr(node, "name", "")
    if name.startswith("_") or name in ("__init__", "__str__", "__repr__"):
        return None
    if ast.get_docstring(node):
        return None
    return make_violation(
        "REV-CMT-02", "Missing Public Docstring", node.lineno,
        f"Entity public '{name}' thiếu docstring mô tả hành vi.",
        f"Bổ sung docstring Google-style (Args:, Returns:, Raises:) cho '{name}'.",
    )


def check_function_length(node: ast.FunctionDef) -> Optional[dict]:
    """REV-CMP-01: function > MAX_FUNCTION_LINES."""
    end = getattr(node, "end_lineno", None)
    length = (end - node.lineno + 1) if end else 0
    if length <= MAX_FUNCTION_LINES:
        return None
    return make_violation(
        "REV-CMP-01", "Excessive Function Length", node.lineno,
        f"Hàm '{node.name}' quá dài ({length} dòng), vượt giới hạn {MAX_FUNCTION_LINES} dòng.",
        "Tách hàm thành các helper functions nhỏ hơn theo Single Responsibility.",
    )


def check_too_many_args(node: ast.FunctionDef) -> Optional[dict]:
    """REV-CMP-01: function args > MAX_FUNCTION_ARGS (optional severity)."""
    count = len(node.args.args)
    if count <= MAX_FUNCTION_ARGS:
        return None
    return make_violation(
        "REV-CMP-01", "Too Many Function Arguments", node.lineno,
        f"Hàm '{node.name}' nhận quá nhiều tham số ({count} > {MAX_FUNCTION_ARGS}).",
        "Đóng gói các tham số liên quan vào một dataclass hoặc dictionary cấu trúc.",
        severity="optional",
    )


def check_mutable_default(node: ast.FunctionDef) -> Optional[dict]:
    """REV-FUN-14: mutable default args (List/Dict)."""
    for arg in node.args.defaults:
        if isinstance(arg, (ast.List, ast.Dict, ast.Set)):
            return make_violation(
                "REV-FUN-14", "Mutable Default Arguments", node.lineno,
                f"Hàm '{node.name}' sử dụng đối tượng khả biến (List/Dict/Set) làm tham số mặc định.",
                "Dùng giá trị mặc định là None và khởi tạo bên trong thân hàm.",
            )
    return None


def check_swallowed_exception(node: ast.ExceptHandler) -> Optional[dict]:
    """REV-FUN-02: bare pass in except handler."""
    if len(node.body) == 1 and isinstance(node.body[0], ast.Pass):
        return make_violation(
            "REV-FUN-02", "Swallowed Exception", node.lineno,
            "Nuốt ngoại lệ bằng pass trống rỗng trong khối except.",
            "Thêm logging.error() hoặc re-raise để giữ khả năng debug.",
        )
    return None


# ---------------------------------------------------------------------------
# Resource & call patterns
# ---------------------------------------------------------------------------

def check_open_without_with(call_node: ast.Call, is_inside_with: bool, is_inside_try: bool) -> list[dict]:
    """REV-FUN-03 + REV-FUN-04: open() without context manager / try."""
    if not (isinstance(call_node.func, ast.Name) and call_node.func.id == "open"):
        return []
    results: list[dict] = []
    if not is_inside_with:
        results.append(make_violation(
            "REV-FUN-03", "Unsafe File Open", call_node.lineno,
            "Mở file bằng open() thô mà không dùng context manager 'with'.",
            "Thay bằng 'with open(...) as f:' để tự giải phóng tài nguyên.",
        ))
    if not is_inside_try:
        results.append(make_violation(
            "REV-FUN-04", "Unprotected File IO", call_node.lineno,
            "Thao tác IO không nằm trong khối try/except bảo vệ.",
            "Bọc mở file trong 'try ... except IOError'.",
        ))
    return results


def check_network_no_timeout(call_node: ast.Call) -> Optional[dict]:
    """REV-FUN-05: requests/socket call without timeout."""
    func = call_node.func
    if not (isinstance(func, ast.Attribute) and isinstance(func.value, ast.Name)):
        return None
    if func.value.id not in _NETWORK_MODULES or func.attr not in _NETWORK_METHODS:
        return None
    for kw in call_node.keywords:
        if kw.arg == "timeout":
            return None
    return make_violation(
        "REV-FUN-05", "Missing Network Timeout", call_node.lineno,
        f"Cuộc gọi mạng {func.value.id}.{func.attr}() thiếu tham số 'timeout'.",
        "Thiết lập timeout=10 (hoặc giá trị phù hợp) để tránh treo vô hạn trên production.",
    )


def check_subprocess_shell_true(call_node: ast.Call) -> Optional[dict]:
    """REV-FUN-08: subprocess.run(..., shell=True)."""
    func = call_node.func
    if not (isinstance(func, ast.Attribute) and isinstance(func.value, ast.Name)):
        return None
    if func.value.id != "subprocess" or func.attr not in _SHELL_METHODS:
        return None
    for kw in call_node.keywords:
        if kw.arg == "shell" and isinstance(kw.value, ast.Constant) and kw.value.value is True:
            return make_violation(
                "REV-FUN-08", "Shell Injection Risk", call_node.lineno,
                "subprocess với shell=True gây rủi ro bảo mật shell injection.",
                "Truyền lệnh dạng list và đặt shell=False, ví dụ: subprocess.run(['ls', '-la']).",
            )
    return None


def check_hardcoded_secret(node: ast.Assign) -> Optional[dict]:
    """REV-FUN-11: hardcoded API key/secret/password string assignment."""
    if not (isinstance(node.value, ast.Constant) and isinstance(node.value.value, str)):
        return None
    secret_val = node.value.value
    if len(secret_val) <= 4 or secret_val.startswith("${") or secret_val.startswith("os.environ"):
        return None
    for target in node.targets:
        if isinstance(target, ast.Name):
            var_name = target.id.lower()
            if any(sec in var_name for sec in _SECRET_KEYS):
                return make_violation(
                    "REV-FUN-11", "Hardcoded Secrets Leak", node.lineno,
                    f"Phát hiện gán cứng chuỗi mật mã cho biến nhạy cảm '{target.id}'.",
                    "Tải khóa từ os.environ.get() hoặc file config bảo mật.",
                )
    return None


# ---------------------------------------------------------------------------
# Nesting depth (REV-CMP-02)
# ---------------------------------------------------------------------------

def _walk_nesting(node: ast.AST) -> int:
    """Compute the maximum control-flow nesting depth inside a node."""
    class _Nester(ast.NodeVisitor):
        def __init__(self) -> None:
            self.max_depth = 0
            self.cur_depth = 0

        def _enter(self, _node: ast.AST) -> None:
            self.cur_depth += 1
            self.max_depth = max(self.max_depth, self.cur_depth)
            self.generic_visit(_node)
            self.cur_depth -= 1

        def visit_If(self, node: ast.AST) -> None: self._enter(node)
        def visit_For(self, node: ast.AST) -> None: self._enter(node)
        def visit_While(self, node: ast.AST) -> None: self._enter(node)
        def visit_Try(self, node: ast.AST) -> None: self._enter(node)

    nester = _Nester()
    nester.visit(node)
    return nester.max_depth


def check_nesting_depth(node: ast.FunctionDef) -> Optional[dict]:
    """REV-CMP-02: control flow nesting > MAX_NESTING_DEPTH."""
    depth = _walk_nesting(node)
    if depth <= MAX_NESTING_DEPTH:
        return None
    return make_violation(
        "REV-CMP-02", "Excessive Nesting Depth", node.lineno,
        f"Độ lồng điều khiển trong hàm '{node.name}' đạt {depth} lớp (tối đa {MAX_NESTING_DEPTH}).",
        "Tái cấu trúc hàm, dùng guard clauses hoặc helper methods để làm phẳng logic.",
    )


# ---------------------------------------------------------------------------
# Line-level regex checks
# ---------------------------------------------------------------------------

def check_unregistered_todo(line: str, line_number: int) -> Optional[dict]:
    """REV-CMT-03: TODO without ticket reference."""
    if "TODO" not in line:
        return None
    if _TODO_PATTERN.search(line):
        return None
    return make_violation(
        "REV-CMT-03", "Unregistered TODO", line_number,
        "Dòng TODO thiếu mã ticket ID tham chiếu (ví dụ: TODO(bug-101): ...).",
        "Thêm ID bug/task vào trong dấu ngoặc đơn, ví dụ: '# TODO(billing-12): ...'.",
    )


# ---------------------------------------------------------------------------
# Cross-module heuristics
# ---------------------------------------------------------------------------

def check_threading_without_lock(content: str) -> Optional[dict]:
    """REV-FUN-06: threading import but no Lock/Semaphore."""
    if "import threading" not in content and "from threading import" not in content:
        return None
    if "Lock(" in content or "Semaphore(" in content:
        return None
    return make_violation(
        "REV-FUN-06", "Missing Concurrency Lock", 1,
        "Sử dụng thư viện threading nhưng không khai báo Lock/Semaphore.",
        "Khai báo 'lock = threading.Lock()' và dùng 'with lock:' khi thao tác biến chia sẻ.",
    )


def check_missing_test_file(file_path, path) -> Optional[dict]:
    """REV-TST-01: code file without matching test_*.py alongside."""
    if "test_" in path.name:
        return None
    candidate_1 = path.parent / f"test_{path.name}"
    candidate_2 = path.parent / path.name.replace(".py", "_test.py")
    if candidate_1.exists() or candidate_2.exists():
        return None
    return make_violation(
        "REV-TST-01", "Missing Unit Test File", 1,
        f"Không tìm thấy file unit test đi kèm cho '{path.name}'.",
        f"Tạo '{candidate_1.name}' cùng thư mục để cover module này.",
    )
