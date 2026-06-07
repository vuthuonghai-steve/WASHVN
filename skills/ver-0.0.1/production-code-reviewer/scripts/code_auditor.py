#!/usr/bin/env python3
"""
code_auditor.py — High-fidelity static code reviewer using AST & Regex.
Audits python files against the 68 Google Code Review Rules.
Populates audit-metrics.yaml with granular violation results.

Usage:
    python code_auditor.py <file_path>
"""

import sys
import os
import re
import ast
import argparse
import yaml
from pathlib import Path

# AI Clichés and banned patterns
AI_KEYWORDS = ["delve", "tapestry", "testament", "beacon", "multifaceted", "plethora", "nestled"]

class ASTAuditor(ast.NodeVisitor):
    def __init__(self, content, file_path):
        self.content = content
        self.lines = content.split('\n')
        self.file_path = file_path
        self.violations = []
        self.imported_names = {}  # name -> node (Import or ImportFrom)
        self.used_names = set()
        
    def add_violation(self, rule_id, name, error, line_number, fix_hint, severity="blocking"):
        self.violations.append({
            "id": rule_id,
            "name": name,
            "error": error,
            "line": line_number,
            "severity": severity,
            "fix_hint": fix_hint
        })

    def visit_Import(self, node):
        for alias in node.names:
            name = alias.asname or alias.name
            self.imported_names[name] = (node.lineno, "Import")
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        for alias in node.names:
            name = alias.asname or alias.name
            self.imported_names[name] = (node.lineno, "ImportFrom")
        self.generic_visit(node)

    def visit_Name(self, node):
        if isinstance(node.ctx, ast.Load):
            self.used_names.add(node.id)
        self.generic_visit(node)

    def visit_ClassDef(self, node):
        # REV-STY-02: PEP 8 Pascal Case for Classes
        if not re.match(r"^[A-Z][a-zA-Z0-9]*$", node.name):
            self.add_violation(
                "REV-STY-02",
                "Class Naming Style",
                f"Tên Class '{node.name}' không đúng chuẩn PascalCase.",
                node.lineno,
                "Đổi tên Class thành chữ cái đầu viết hoa, ví dụ: 'AdvancedBilling'."
            )
            
        # REV-CMT-02: Public API Docstring Coverage
        if not node.name.startswith("_"):
            docstring = ast.get_docstring(node)
            if not docstring:
                self.add_violation(
                    "REV-CMT-02",
                    "Missing Class Docstring",
                    f"Class public '{node.name}' thiếu tài liệu hướng dẫn (docstring).",
                    node.lineno,
                    f"Thêm docstring bọc trong ba dấu nháy kép giải thích mục đích của Class '{node.name}'."
                )

        # REV-DES-08: Class length limit
        class_lines = node.end_lineno - node.lineno + 1 if hasattr(node, "end_lineno") else 50
        if class_lines > 300:
            self.add_violation(
                "REV-DES-08",
                "Excessive Class Length",
                f"Class '{node.name}' quá dài ({class_lines} dòng), vượt quá giới hạn 300 dòng.",
                node.lineno,
                "Tách Class thành các sub-classes hoặc cấu trúc helper nhỏ gọn hơn.",
                "optional"
            )

        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        # REV-STY-01: PEP 8 Snake Case for Functions
        if not re.match(r"^[a-z_][a-z0-9_]*$", node.name):
            self.add_violation(
                "REV-STY-01",
                "Function Naming Style",
                f"Tên hàm '{node.name}' không tuân thủ snake_case chuẩn PEP 8.",
                node.lineno,
                "Đổi tên hàm thành chữ thường ngăn cách bởi dấu gạch dưới, ví dụ: 'calculate_billing_total'."
            )

        # REV-CMT-02: Public API Docstring Coverage
        if not node.name.startswith("_") and node.name not in ["__init__", "__str__", "__repr__"]:
            docstring = ast.get_docstring(node)
            if not docstring:
                self.add_violation(
                    "REV-CMT-02",
                    "Missing Function Docstring",
                    f"Hàm public '{node.name}' thiếu docstring mô tả hành vi.",
                    node.lineno,
                    f"Bổ sung docstring bọc trong ''' hoặc \"\"\" giải thích tham số đầu vào và kiểu dữ liệu trả về."
                )

        # REV-CMP-01: Excessive Function Length (>50 lines)
        func_lines = node.end_lineno - node.lineno + 1 if hasattr(node, "end_lineno") else 10
        if func_lines > 50:
            self.add_violation(
                "REV-CMP-01",
                "SOLID Function Length",
                f"Hàm '{node.name}' quá dài ({func_lines} dòng), vi phạm Single Responsibility.",
                node.lineno,
                "Tách hàm thành các helper functions nhỏ hơn dưới 50 dòng."
            )

        # REV-CMP-02: Control Flow Nesting Depth
        self.check_nesting_depth(node)

        # REV-FUN-14: Mutable Default Arguments
        for arg in node.args.defaults:
            if isinstance(arg, (ast.List, ast.Dict)):
                self.add_violation(
                    "REV-FUN-14",
                    "Mutable Default Arguments",
                    f"Hàm '{node.name}' sử dụng đối tượng khả biến (List/Dict) làm tham số mặc định.",
                    node.lineno,
                    "Sử dụng giá trị mặc định là 'None' và khởi tạo list/dict rỗng bên trong thân hàm."
                )

        # REV-DES-02: Function Arguments Limit (>5 arguments)
        args_count = len(node.args.args)
        if args_count > 5:
            self.add_violation(
                "REV-CMP-01", # mapped to function length/clean code rules
                "Too Many Function Arguments",
                f"Hàm '{node.name}' nhận quá nhiều tham số ({args_count} tham số), vượt quá 5.",
                node.lineno,
                "Đóng gói các tham số liên quan vào một dataclass hoặc dictionary cấu trúc.",
                "optional"
            )

        self.generic_visit(node)

    def visit_ExceptHandler(self, node):
        # REV-FUN-02: Swallowed Exceptions
        if len(node.body) == 1 and isinstance(node.body[0], ast.Pass):
            self.add_violation(
                "REV-FUN-02",
                "Swallowed Exception",
                "Nuốt ngoại lệ bằng pass trống rỗng trong khối except.",
                node.lineno,
                "Thêm ghi log lỗi bằng logging.error() hoặc re-raise lỗi bằng raise."
            )
        self.generic_visit(node)

    def visit_Call(self, node):
        # REV-FUN-03: Unsafe Resource Management (open)
        if isinstance(node.func, ast.Name) and node.func.id == "open":
            # Check if open() call is inside a With context manager
            if not self.is_inside_with(node):
                self.add_violation(
                    "REV-FUN-03",
                    "Unsafe File Open",
                    "Mở file bằng open() thô mà không sử dụng context manager 'with'.",
                    node.lineno,
                    "Thay thế bằng cú pháp: 'with open(...) as f:' để tài nguyên tự giải phóng an toàn."
                )

            # REV-FUN-04: Unprotected Exception Boundaries (Try-except for open)
            if not self.is_inside_try(node):
                self.add_violation(
                    "REV-FUN-04",
                    "Unprotected File IO",
                    "Thao tác mở file IO không nằm trong khối try/except bảo vệ.",
                    node.lineno,
                    "Bọc khối mở file trong 'try ... except IOError' để phòng tránh file không tồn tại hoặc lỗi quyền truy cập."
                )

        # REV-FUN-05: Missing Requests/Socket Timeouts
        if isinstance(node.func, ast.Attribute) and isinstance(node.func.value, ast.Name):
            module_name = node.func.value.id
            method_name = node.func.attr
            if module_name in ["requests", "socket"] and method_name in ["get", "post", "put", "delete", "connect"]:
                has_timeout = False
                for kw in node.keywords:
                    if kw.arg == "timeout":
                        has_timeout = True
                        break
                if not has_timeout:
                    self.add_violation(
                        "REV-FUN-05",
                        "Missing Network Timeout",
                        f"Cuộc gọi mạng {module_name}.{method_name}() thiếu tham số 'timeout' an toàn.",
                        node.lineno,
                        "Thiết lập tham số 'timeout=10' (hoặc giá trị phù hợp) để tránh bị treo kết nối vô hạn trên production."
                    )

        # REV-FUN-08: Shell Injection Risk (subprocess.run with shell=True)
        if isinstance(node.func, ast.Attribute) and isinstance(node.func.value, ast.Name) and node.func.value.id == "subprocess" and node.func.attr in ["run", "Popen", "call"]:
            for kw in node.keywords:
                if kw.arg == "shell" and isinstance(kw.value, ast.Constant) and kw.value.value is True:
                    # check if the command command is dynamic
                    self.add_violation(
                        "REV-FUN-08",
                        "Shell Injection Risk",
                        "Gọi subprocess với shell=True gây rủi ro bảo mật Shell Injection nghiêm trọng.",
                        node.lineno,
                        "Truyền lệnh dưới dạng mảng tham số (list) và đặt shell=False, ví dụ: subprocess.run(['ls', '-la'])."
                    )

        self.generic_visit(node)

    def visit_Assign(self, node):
        # REV-FUN-11: Hardcoded Secrets
        for target in node.targets:
            if isinstance(target, ast.Name):
                var_name = target.id.lower()
                if any(sec in var_name for sec in ["api_key", "secret", "token", "password", "private_key"]):
                    if isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
                        secret_val = node.value.value
                        if len(secret_val) > 4 and not (secret_val.startswith("${") or secret_val.startswith("os.environ")):
                            self.add_violation(
                                "REV-FUN-11",
                                "Hardcoded Secrets Leak",
                                f"Phát hiện gán cứng chuỗi mật mã cho biến nhạy cảm '{target.id}'.",
                                node.lineno,
                                "Tải khóa bảo mật từ biến môi trường bằng 'os.environ.get()' hoặc file config bảo mật."
                            )

        # REV-CMP-04: Magic Numbers
        if isinstance(node.value, ast.Constant) and isinstance(node.value.value, (int, float)):
            val = node.value.value
            if val not in [-1, 0, 1] and not self.is_module_level_constant(node):
                self.add_violation(
                    "REV-CMP-04",
                    "Magic Number detected",
                    f"Sử dụng số ma thuật '{val}' trực tiếp trong logic.",
                    node.lineno,
                    f"Định nghĩa số '{val}' dưới dạng HẰNG SỐ viết hoa ở đầu module, ví dụ: 'DEFAULT_TIMEOUT_SEC = {val}'.",
                    "optional"
                )

        self.generic_visit(node)

    def is_module_level_constant(self, node):
        # Checks if variable assignment is at the module (global) level and written in uppercase
        curr = node
        while hasattr(curr, "parent"):
            curr = curr.parent
        if isinstance(curr, ast.Module):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id.isupper():
                    return True
        return False

    def is_inside_with(self, call_node):
        curr = call_node
        while hasattr(curr, "parent"):
            curr = curr.parent
            if isinstance(curr, ast.With):
                return True
        return False

    def is_inside_try(self, call_node):
        curr = call_node
        while hasattr(curr, "parent"):
            curr = curr.parent
            if isinstance(curr, ast.Try):
                return True
        return False

    def check_nesting_depth(self, func_node):
        class NestingVisitor(ast.NodeVisitor):
            def __init__(self, outer):
                self.outer = outer
                self.max_depth = 0
                self.current_depth = 0
                
            def visit_For(self, node):
                self.current_depth += 1
                self.max_depth = max(self.max_depth, self.current_depth)
                self.generic_visit(node)
                self.current_depth -= 1

            def visit_While(self, node):
                self.current_depth += 1
                self.max_depth = max(self.max_depth, self.current_depth)
                self.generic_visit(node)
                self.current_depth -= 1

            def visit_If(self, node):
                self.current_depth += 1
                self.max_depth = max(self.max_depth, self.current_depth)
                self.generic_visit(node)
                self.current_depth -= 1

        visitor = NestingVisitor(self)
        visitor.visit(func_node)
        if visitor.max_depth > 3:
            self.add_violation(
                "REV-CMP-02",
                "Excessive Nesting Depth",
                f"Độ lồng điều khiển trong hàm '{func_node.name}' đạt {visitor.max_depth} lớp (tối đa 3).",
                func_node.lineno,
                "Tái cấu trúc hàm, sử dụng guard clauses hoặc helper methods để làm phẳng cấu trúc logic."
            )

def add_parent_pointers(tree):
    for node in ast.walk(tree):
        for child in ast.iter_child_nodes(node):
            child.parent = node

def audit_file_content(file_path):
    path = Path(file_path)
    if not path.exists():
        return {"error": f"File not found: {file_path}", "exit_code": 2, "violations": []}
        
    try:
        content = path.read_text(encoding="utf-8")
    except Exception as e:
        return {"error": f"Cannot read file: {e}", "exit_code": 2, "violations": []}
        
    lines = content.split('\n')
    total_lines = len(lines)
    
    # Run AST Analysis
    try:
        tree = ast.parse(content)
        add_parent_pointers(tree)
        visitor = ASTAuditor(content, file_path)
        visitor.visit(tree)
        violations = visitor.violations
        imported_names = visitor.imported_names
        used_names = visitor.used_names
    except SyntaxError as se:
        # If syntax error, write blocking compile violation
        violations = [{
            "id": "REV-FUN-01",
            "name": "Compilation Error",
            "error": f"Mã nguồn lỗi cú pháp không biên dịch được: {se.msg}",
            "line": se.lineno or 1,
            "severity": "blocking",
            "fix_hint": "Khắc phục lỗi cú pháp ngay lập tức để mã nguồn chạy được."
        }]
        imported_names = {}
        used_names = set()

    # Post AST-analysis: check unused imports (REV-STY-04)
    for name, (line, imp_type) in imported_names.items():
        if name not in used_names and not name.startswith("_"):
            violations.append({
                "id": "REV-STY-04",
                "name": "Unused Import",
                "error": f"Module thư viện/hàm '{name}' được import nhưng không bao giờ sử dụng trong code.",
                "line": line,
                "severity": "blocking",
                "fix_hint": f"Xóa dòng import '{name}' không dùng tới để giữ code sạch."
            })

    # Regex Check: REV-CMT-03 (Unregistered TODO Comments)
    for idx, line in enumerate(lines):
        line_num = idx + 1
        if "TODO" in line:
            if not re.search(r"TODO\([a-zA-Z0-9\-]+\):", line):
                violations.append({
                    "id": "REV-CMT-03",
                    "name": "Unregistered TODO",
                    "error": "Phát hiện dòng ghi chú TODO thiếu mã ticket ID tham chiếu (ví dụ: TODO(bug-101): ...).",
                    "line": line_num,
                    "severity": "blocking",
                    "fix_hint": "Thêm ID bug hoặc ID task vào trong dấu ngoặc đơn của TODO, ví dụ: '# TODO(billing-12): ...'"
                })

    # Regex Check: Concurrency imports without Locks (REV-FUN-06)
    if "import threading" in content or "from threading import" in content:
        if "Lock(" not in content and "Semaphore(" not in content:
            violations.append({
                "id": "REV-FUN-06",
                "name": "Missing Concurrency Lock",
                "error": "Sử dụng thư viện threading tương tranh nhưng không thấy khai báo Lock hoặc Semaphore để đồng bộ hóa.",
                "line": 1,
                "severity": "blocking",
                "fix_hint": "Khai báo 'lock = threading.Lock()' và sử dụng 'with lock:' khi thao tác với biến/mảng dùng chung."
            })

    # Check for unit test file existence (REV-TST-01)
    test_file_found = False
    test_file_name1 = path.parent / f"test_{path.name}"
    test_file_name2 = path.parent / path.name.replace(".py", "_test.py")
    
    if test_file_name1.exists() or test_file_name2.exists():
        test_file_found = True
        
    if not test_file_found and "test_" not in path.name:
        violations.append({
            "id": "REV-TST-01",
            "name": "Missing Unit Test File",
            "error": f"Không tìm thấy file unit test đi kèm cho module '{path.name}'.",
            "line": 1,
            "severity": "blocking",
            "fix_hint": f"Tạo một file test mới là '{test_file_name1.name}' đặt cùng thư mục để tự động hóa kiểm định."
        })

    # Summary calculations
    exit_code = 0
    blocking_violations = [v for v in violations if v["severity"] == "blocking"]
    if blocking_violations:
        exit_code = 1 # Return 1 if there are any blocking failures!

    results = {
        "file": str(file_path),
        "total_lines": total_lines,
        "violations_count": len(violations),
        "blocking_count": len(blocking_violations),
        "violations": violations,
        "exit_code": exit_code
    }
    
    return results

def main():
    parser = argparse.ArgumentParser(description="Static code auditor producing audit-metrics.yaml")
    parser.add_argument("file_path", help="Path to the code file to audit")
    parser.add_argument("--target-skill", default="production-code-reviewer",
                        help="Target skill context directory under .skill-context/ (default: production-code-reviewer)")
    args = parser.parse_args()

    result = audit_file_content(args.file_path)

    # Save output to active context (dynamic per target_skill)
    output_dir = Path(f".skill-context/{args.target_skill}")
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / "audit-metrics.yaml"
    output_file.write_text(yaml.safe_dump(result, sort_keys=False, allow_unicode=True), encoding="utf-8")
    
    print(f"\n--- AUDITOR ANALYSIS SUMMARY FOR: {file_path} ---")
    print(f"Total Lines: {result['total_lines']}")
    print(f"Total Violations: {result['violations_count']}")
    print(f"Blocking Issues: {result['blocking_count']}")
    print(f"Verdict: {'❌ FAIL (Has Blocking)' if result['blocking_count'] > 0 else '✅ PASS'}\n")
    
    if result['violations']:
        print("Violation Details:")
        for v in result['violations']:
            print(f"- [{v['id']}] {v['name']} ({v['severity'].upper()}) at line {v['line']}")
            print(f"  Error: {v['error']}")
            print(f"  Fix Hint: {v['fix_hint']}")
            
    sys.exit(result["exit_code"])

if __name__ == "__main__":
    main()
