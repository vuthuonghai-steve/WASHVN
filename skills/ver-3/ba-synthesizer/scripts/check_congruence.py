#!/usr/bin/env python3
"""check_congruence.py — Binary congruence gate for ba-synthesizer business-analysis.md.

Validates 6 mechanical criteria (C1-C6) against synthesis.schema.yaml contract.
No NLP scoring. Exit 0 = all pass, 1 = fail. Click CLI. Stdlib + PyYAML only.
"""
import re
import sys
import yaml
import click

SOURCE_ENUM = ("elicitation", "analysis", "both")
CLASSIFICATION_ENUM = ("FR", "NFR")
VERDICT_ENUM = ("PASS", "FAIL")
REQUIRED_FIELDS = ("skill_name", "synthesized_requirements", "congruence_check", "pipeline_ready")
PLACEHOLDER_RE = re.compile(
    r"TODO|FIXME|TBD|INCOMPLETE|placeholder|Lorem Ipsum|\.\.\.\s*$", re.IGNORECASE
)

PASS = "✅ PASS"
FAIL = "❌ FAIL"


def parse_frontmatter(path):
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    if not content.startswith("---"):
        raise ValueError("No YAML frontmatter (---) at top of file")
    parts = re.split(r"^---\s*$", content, maxsplit=2, flags=re.MULTILINE)
    if len(parts) < 3:
        raise ValueError("Frontmatter block not closed with ---")
    return yaml.safe_load(parts[1]) or {}


def run_checks(fm):
    errors = []

    # C1: YAML frontmatter parse
    if not isinstance(fm, dict):
        return ["C1: frontmatter không parse thành dict hợp lệ"]

    # C2: 4 required fields present
    for field in REQUIRED_FIELDS:
        if field not in fm:
            errors.append(f"C2: thiếu required field '{field}'")
    reqs = fm.get("synthesized_requirements")
    if "synthesized_requirements" in fm and not (isinstance(reqs, list) and len(reqs) > 0):
        errors.append("C2: synthesized_requirements phải là list non-empty")

    # C3 + C4: per-item enums
    if isinstance(reqs, list):
        for i, item in enumerate(reqs):
            if not isinstance(item, dict):
                errors.append(f"C3/C4: synthesized_requirements[{i}] không phải object")
                continue
            src = item.get("source")
            if src not in SOURCE_ENUM:
                errors.append(f"C3: item[{i}].source='{src}' không thuộc {SOURCE_ENUM}")
            cls = item.get("classification")
            if cls not in CLASSIFICATION_ENUM:
                errors.append(f"C4: item[{i}].classification='{cls}' không thuộc {CLASSIFICATION_ENUM}")

    # C5: congruence_check.check_verdict enum
    cc = fm.get("congruence_check")
    if isinstance(cc, dict):
        if cc.get("check_verdict") not in VERDICT_ENUM:
            errors.append(f"C5: congruence_check.check_verdict='{cc.get('check_verdict')}' không thuộc {VERDICT_ENUM}")
        for sub in ("conflicts_found", "conflicts_resolved"):
            if not isinstance(cc.get(sub), bool):
                errors.append(f"C5: congruence_check.{sub} phải là boolean")
    elif "congruence_check" in fm:
        errors.append("C5: congruence_check phải là object")

    # C6: pipeline_ready boolean
    if not isinstance(fm.get("pipeline_ready"), bool):
        errors.append(f"C6: pipeline_ready phải là boolean, nhận được {type(fm.get('pipeline_ready')).__name__}")

    return errors


def check_placeholder(path):
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    hits = [m.group(0) for m in PLACEHOLDER_RE.finditer(text)]
    return hits


@click.command()
@click.option("--artifact", required=True, type=click.Path(exists=True), help="Path to business-analysis.md")
@click.option("--schema", type=click.Path(exists=True), help="Path to synthesis.schema.yaml (reserved for future jsonschema cross-check)")
def main(artifact, schema):
    """Congruence checker for ba-synthesizer output. Exit 0 = PASS, 1 = FAIL."""
    click.echo(f"[C1] YAML frontmatter parse .......................... ", nl=False)
    try:
        fm = parse_frontmatter(artifact)
        click.echo(PASS)
    except Exception as e:
        click.echo(FAIL)
        click.echo(f"  Lỗi: {e}")
        sys.exit(1)

    errors = run_checks(fm)

    c2_ok = all("C2" not in e for e in errors)
    c3_ok = all("C3" not in e for e in errors)
    c4_ok = all("C4" not in e for e in errors)
    c5_ok = all("C5" not in e for e in errors)
    c6_ok = all("C6" not in e for e in errors)
    status = lambda ok: PASS if ok else FAIL

    lines = [
        ("C2", "4 required fields present", c2_ok),
        ("C3", "synthesized_requirements source enum", c3_ok),
        ("C4", "synthesized_requirements classification enum", c4_ok),
        ("C5", "congruence_check.check_verdict enum", c5_ok),
        ("C6", "pipeline_ready boolean", c6_ok),
    ]
    for cid, desc, ok in lines:
        click.echo(f"[{cid}] {desc} ".ljust(52) + status(ok))

    # C7: placeholder scan
    hits = check_placeholder(artifact)
    click.echo("[C7] no placeholder (TODO/TBD/mock/...) ".ljust(52), nl=False)
    if hits:
        click.echo(FAIL)
        errors.append(f"C7: placeholder tìm thấy: {hits[:5]}")
    else:
        click.echo(PASS)

    # C8: internal quality score threshold >= 0.80 (QG-SYN-03).
    # synthesis.schema.yaml uses additionalProperties:false, so quality_score_percentage
    # lives in the artifact BODY, not frontmatter. Scan body; also accept a top-level
    # frontmatter field if present (lenient for non-schema-conformant inputs).
    qsp = fm.get("quality_score_percentage")
    c8_ok = False
    if isinstance(qsp, (int, float)) and qsp >= 80:
        c8_ok = True
    else:
        # Fallback: scan body for "weighted_sum: 0.XX" or "percentage: XX%"
        with open(artifact, "r", encoding="utf-8") as f:
            body = f.read()
        m = re.search(r"weighted_sum:\s*([0-9]*\.?[0-9]+)", body)
        if m and float(m.group(1)) >= 0.80:
            c8_ok = True
        else:
            m2 = re.search(r"percentage:\s*([0-9]+)%", body)
            if m2 and int(m2.group(1)) >= 80:
                c8_ok = True
    click.echo("[C8] internal quality score >= 0.80 (80%) ".ljust(52), nl=False)
    if c8_ok:
        click.echo(PASS)
    else:
        click.echo(FAIL)
        errors.append("C8: quality_score_percentage < 80% (hoặc không tìm thấy weighted_sum >= 0.80)")

    total = 8
    passed = sum(1 for ok in (c2_ok, c3_ok, c4_ok, c5_ok, c6_ok, not hits, c8_ok)) + 1  # C1 passed
    click.echo("")
    if errors:
        click.echo("Result: FAIL — các lỗi:")
        for e in errors:
            click.echo(f"  - {e}")
        click.echo(f"Result: FAIL ({passed}/{total}) — exit code 1")
        sys.exit(1)
    click.echo(f"Result: PASS ({total}/{total}) — exit code 0")
    sys.exit(0)


if __name__ == "__main__":
    main()
