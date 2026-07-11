#!/usr/bin/env python3
"""validate_metrics.py — Binary quality gate for ba-analyst analyst-output.md.

Validates 8 mechanical criteria (C1-C8). No NLP scoring. Exit 0 = all pass, 1 = fail.
Stdlib + PyYAML + Click only. Schema is read-only (skills/ver-3/_shared/schemas/analysis.schema.yaml).
"""
import re
import sys
import yaml
import click

REQUIRED_FIELDS = ("skill_name", "criteria_analysis", "metrics", "risk_assessment")
SUBJECTIVE_KEYWORDS = {
    "nhanh", "mượt", "tốt", "hiệu quả", "ổn định", "an toàn", "linh hoạt",
    "dễ dùng", "thân thiện", "fast", "smooth", "good", "efficient", "reliable",
    "secure", "flexible", "user-friendly",
}
PLACEHOLDER_RE = re.compile(r"TODO|FIXME|TBD|INCOMPLETE|placeholder|Lorem Ipsum", re.IGNORECASE)


def parse_frontmatter(path):
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    if not content.startswith("---"):
        raise ValueError("No YAML frontmatter (---) at top of file")
    parts = content.split("---", 2)
    if len(parts) < 3:
        raise ValueError("Frontmatter not closed by second ---")
    return yaml.safe_load(parts[1]), content


def check_c1_c2(fm):
    try:
        if fm is None:
            raise ValueError("frontmatter is empty")
        results = {"C1": (True, "YAML frontmatter parse")}
    except Exception as e:
        return {"C1": (False, f"parse fail: {e}")}
    missing = [k for k in REQUIRED_FIELDS if k not in fm]
    ok = not missing
    results["C2"] = (ok, "4 required fields present" if ok else f"missing: {missing}")
    return results


def check_c3(fm):
    items = fm.get("criteria_analysis") or []
    if not isinstance(items, list) or not items:
        return (False, "criteria_analysis empty/non-list")
    bad = [i.get("criterion_id", "?") for i in items
           if not isinstance(i, dict) or i.get("classification") not in ("FR", "NFR")]
    return (not bad, "category ∈ [FR,NFR]" if not bad else f"bad: {bad}")


def check_c4(fm):
    metrics = fm.get("metrics") or []
    for m in metrics:
        name = (m.get("name") or "").lower() if isinstance(m, dict) else ""
        if any(k in name for k in SUBJECTIVE_KEYWORDS):
            return (False, f"subjective keyword in metric name: '{m.get('name')}'")
        # placeholder scan across whole metric entry
        if PLACEHOLDER_RE.search(str(m)):
            return (False, f"placeholder in metric: {m.get('name')}")
    return (True, "metrics không chứa từ mơ hồ")


def check_c5(fm):
    metrics = fm.get("metrics") or []
    for m in metrics:
        if not isinstance(m, dict):
            return (False, "metric not a mapping")
        val = m.get("value")
        if val is None or m.get("unit") in (None, ""):
            return (False, f"missing value/unit in metric: {m.get('name')}")
        if not isinstance(val, (int, float)) or isinstance(val, bool):
            return (False, f"value must be number in metric: {m.get('name')}")
    return (True, "metrics value(number)+unit tồn tại")


def check_c6(content):
    blocks = re.findall(r"```mermaid\n(.*?)```", content, re.DOTALL)
    if not blocks:
        return (False, "no mermaid block found")
    for blk in blocks:
        for line in blk.splitlines():
            s = line.strip()
            if not s or s.startswith("%%"):
                continue
            # operator lines with a text label must quote it
            if re.search(r"(->>|-->>|--x|->|-\.->|-->)", s) and ":" in s:
                label = s.split(":", 1)[1].strip()
                if label and not (label.startswith('"') and label.endswith('"')):
                    return (False, f"unquoted mermaid label: {label[:40]}")
            # node/edge definitions with [..] or {..} text label unquoted
            for m in re.finditer(r'[\[\{]([^"\'\]}]+)[\}\]]', s):
                txt = m.group(1).strip()
                if txt and re.search(r"[()/,:]", txt):
                    return (False, f"unquoted node label: {txt[:40]}")
    return (True, "Mermaid labels double-quoted")


def check_c7(content):
    blocks = re.findall(r"```gherkin\n(.*?)```", content, re.DOTALL)
    count = 0
    for blk in blocks:
        count += len(re.findall(r"^\s*Scenario(?: Outline)?\s*:", blk, re.MULTILINE))
    return (count >= 3, f"Gherkin scenarios = {count} (need ≥3)")


def check_c8(fm):
    risks = fm.get("risk_assessment") or []
    for r in risks:
        if not isinstance(r, dict) or not str(r.get("mitigation", "")).strip():
            return (False, f"empty mitigation in risk: {r.get('risk_id','?')}")
        if PLACEHOLDER_RE.search(str(r.get("mitigation", ""))):
            return (False, f"placeholder in mitigation: {r.get('risk_id','?')}")
    return (True, "risk_assessment mitigation không trống")


@click.command()
@click.option("--artifact", required=True, type=click.Path(exists=True), help="Path to analyst-output.md")
@click.option("--schema", type=click.Path(exists=True), help="Path to analysis.schema.yaml (unused for C-criteria, kept for parity)")
def main(artifact, schema):
    try:
        fm, content = parse_frontmatter(artifact)
    except Exception as e:
        click.echo(f"[C1] YAML frontmatter parse .................... ❌ FAIL ({e})")
        sys.exit(1)

    fm = fm or {}
    results = check_c1_c2(fm)
    results["C3"] = check_c3(fm)
    results["C4"] = check_c4(fm)
    results["C5"] = check_c5(fm)
    results["C6"] = check_c6(content)
    results["C7"] = check_c7(content)
    results["C8"] = check_c8(fm)

    passed = 0
    for cid in ["C1", "C2", "C3", "C4", "C5", "C6", "C7", "C8"]:
        ok, msg = results[cid]
        icon = "✅ PASS" if ok else "❌ FAIL"
        click.echo(f"[{cid}] {msg:<40} {icon}")
        passed += ok

    total = len(results)
    all_ok = passed == total
    click.echo(f"Result: {'PASS' if all_ok else 'FAIL'} ({passed}/{total}) — exit code {0 if all_ok else 1}")
    sys.exit(0 if all_ok else 1)


if __name__ == "__main__":
    main()
