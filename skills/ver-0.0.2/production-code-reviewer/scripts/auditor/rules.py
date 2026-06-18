"""Rule registry — central catalog of Google Code Review rules.

Each rule is a frozen dataclass with:
- rule_id:    e.g. "REV-STY-01"
- name:       short label
- severity:   "blocking" | "optional" | "nit"
- category:   "design" | "functionality" | "complexity" | "testing" | "style" | "comments" | "cl_size"
- description: 1-line explanation
- fix_hint:   Vietnamese suggestion for fix
- check:      callable(node_or_context) -> Optional[Violation]

Adding a new rule = add an entry here + write a check() function.
The core auditor pulls from this registry to dispatch AST visitors.
"""

from dataclasses import dataclass, field
from typing import Callable, Optional, Dict, List, Any


@dataclass(frozen=True)
class Rule:
    """Immutable description of a single Google review rule."""
    rule_id: str
    name: str
    severity: str
    category: str
    description: str
    fix_hint: str
    check: Optional[Callable[[Any], Optional[dict]]] = None


# ---------------------------------------------------------------------------
# Rule registry — single source of truth
# ---------------------------------------------------------------------------

REGISTRY: Dict[str, Rule] = {}


def register(rule: Rule) -> Rule:
    """Register a rule into the global registry. Returns the rule for chaining."""
    REGISTRY[rule.rule_id] = rule
    return rule


def by_category(category: str) -> List[Rule]:
    """Return all rules for a given category, sorted by rule_id."""
    return sorted([r for r in REGISTRY.values() if r.category == category], key=lambda r: r.rule_id)


def all_rule_ids() -> List[str]:
    """Return every registered rule_id, sorted."""
    return sorted(REGISTRY.keys())


def by_severity(severity: str) -> List[Rule]:
    """Return all rules for a severity bucket."""
    return sorted([r for r in REGISTRY.values() if r.severity == severity], key=lambda r: r.rule_id)


# Module-level severity buckets for fast lookup
BLOCKING_RULES: List[str] = []
OPTIONAL_RULES: List[str] = []
NIT_RULES: List[str] = []


def rebuild_severity_buckets() -> None:
    """Rebuild severity bucket caches from REGISTRY. Call after bulk register."""
    global BLOCKING_RULES, OPTIONAL_RULES, NIT_RULES
    BLOCKING_RULES = by_severity("blocking")  # type: ignore[assignment]
    BLOCKING_RULES = [r.rule_id for r in BLOCKING_RULES]
    OPTIONAL_RULES = [r.rule_id for r in by_severity("optional")]
    NIT_RULES = [r.rule_id for r in by_severity("nit")]
