"""auditor package — modular static analysis for Google Code Review rules.

Public entry point: audit_file() in core.py.

Submodules:
- core:        ASTAuditor + audit_file_content orchestrator
- visitors:    individual node visitors (naming, function shape, calls, security)
- rules:       rule registry (rule_id -> check function)
- reporting:   YAML emitter + summary formatter
"""

from .core import audit_file, audit_file_content  # noqa: F401

__all__ = ["audit_file", "audit_file_content"]
__version__ = "0.2.0"
