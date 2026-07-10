#!/usr/bin/env python3
"""BA Elicitor output validator — 8 mechanical criteria.

Reads:
  --report  <path>  elicitation-report.md (markdown, may contain YAML frontmatter)
  --thought <path>  thought-cache.yaml
  --raw     <path>  optional raw request text (for XML boundary check)

Exit 0 if ALL 8 criteria pass, else exit 1.
Each criterion is an independent function returning (bool, detail).
"""
import argparse
import re
import sys

AMBIGUOUS = {"nhanh", "dễ", "dễ dùng", "tốt", "mượt", "mượt mà", "an toàn tối đa",
             "fast", "easy", "good", "smooth", "secure max", "quick"}
TRACE_TAGS = ("[TỪ INPUT]", "[SUY LUẬN]", "[CẦN LÀM RÕ]")


def _read(p):
    with open(p, encoding="utf-8") as f:
        return f.read()


def _frontmatter(text):
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            return text[3:end].strip(), text[end + 4:]
    return "", text


# ---- Criterion 1: XML boundary on raw input ----
def c1_xml_boundary(raw):
    if not raw:
        return True, "no raw input supplied (skipped)"
    if "<user_skill_request>" in raw and "</user_skill_request>" in raw:
        return True, "raw wrapped in <user_skill_request>"
    return False, "raw request not wrapped in <user_skill_request> boundary"


# ---- Criterion 2: NFR quantification (no ambiguous adjectives survive) ----
def c2_nfr_quant(report, thought):
    body = report.lower() + thought.lower()
    hits = [w for w in AMBIGUOUS if w in body]
    if hits:
        return False, f"ambiguous term(s) not quantified: {hits}"
    return True, "no unquantified subjective terms"


# ---- Criterion 3: trace tags presence ----
def c3_trace_tags(report):
    missing = [t for t in TRACE_TAGS if t not in report]
    if missing:
        return False, f"missing trace tag(s): {missing}"
    return True, "all trace tags present"


# ---- Criterion 4: 3-path decomposition ----
def c4_three_paths(report):
    paths = ["happy path", "alternative path", "exception path"]
    missing = [p for p in paths if p.lower() not in report.lower()]
    if missing:
        return False, f"missing path(s): {missing}"
    return True, "happy/alternative/exception all present"


# ---- Criterion 5: 5W1H minimum questions ----
def c5_w5h(report):
    q = re.findall(r"^\s*[-*]\s*\*\*(Câu hỏi|Question)\s*\d+", report, re.I | re.M)
    if len(q) < 5:
        return False, f"only {len(q)} 5W1H questions (need >=5)"
    return True, f"{len(q)} 5W1H questions"


# ---- Criterion 6: zero placeholder ----
def c6_zero_placeholder(text):
    pat = re.compile(r"\b(TODO|FIXME|XXX|mock|pass\b|null\b|\.\.\.|TBD)\b", re.I)
    hits = pat.findall(text)
    if hits:
        return False, f"placeholder token(s): {set(h.lower() for h in hits)}"
    return True, "no placeholder tokens"


# ---- Criterion 7: thought-cache completeness ----
def c7_thought_cache(thought):
    try:
        import yaml
        data = yaml.safe_load(thought)
    except Exception as e:  # noqa
        return False, f"thought-cache parse error: {e}"
    if not isinstance(data, dict):
        return False, "thought-cache is not a mapping"
    for req in ("business_thought_process", "stakeholder_empathy", "reverse_questions"):
        if req not in data or not data[req]:
            return False, f"missing required thought section: {req}"
    if len(data.get("stakeholder_empathy", [])) < 2:
        return False, "stakeholder_empathy needs >=2 entries"
    if len(data.get("reverse_questions", [])) < 4:
        return False, "reverse_questions needs >=4 entries"
    return True, "thought-cache 3 required sections + depth present"


# ---- Criterion 8: schema compliance (elicitation.schema.yaml fields) ----
# Report mixes YAML frontmatter (skill_name) + markdown body sections
# (domain_ontology / stakeholder_analysis / nrfs as §2/§4/§5; thought_cache is separate artifact).
# Accept either form so template-generated reports pass (ponytail: if schema_validator.py
# later enforces strict frontmatter-only, move the 4 fields into frontmatter instead).
def c8_schema_compliance(report, thought):
    fm, body = _frontmatter(report)
    try:
        import yaml
        meta = yaml.safe_load(fm) if fm else {}
        tc = yaml.safe_load(thought)
    except Exception as e:  # noqa
        return False, f"parse error: {e}"
    if not isinstance(meta, dict):
        return False, "frontmatter not a mapping"
    full = (fm + "\n" + body).lower()
    # skill_name required in frontmatter
    if "skill_name" not in meta:
        return False, "missing report field: skill_name (frontmatter)"
    # 4 schema fields present as frontmatter keys OR body section markers.
    # thought_cache is a SEPARATE artifact (validated by C7), not required in report body.
    section_map = {
        "domain_ontology": ["domain_ontology", "ontology"],
        "stakeholder_analysis": ["stakeholder_analysis", "stakeholder analysis"],
        "nrfs": ["nrfs", "nfrs"],
    }
    missing = []
    for req, tokens in section_map.items():
        if not any(t in full for t in tokens):
            missing.append(req)
    if missing:
        return False, f"missing schema field(s): {missing}"
    if not isinstance(tc, dict) or "business_thought_process" not in tc:
        return False, "thought_cache artifact missing/invalid"
    return True, "5 schema fields present (frontmatter + body sections)"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--report", required=True)
    ap.add_argument("--thought", required=True)
    ap.add_argument("--raw")
    a = ap.parse_args()

    report = _read(a.report)
    thought = _read(a.thought)
    raw = _read(a.raw) if a.raw else ""

    checks = [
        ("C1  XML boundary", c1_xml_boundary(raw)),
        ("C2  NFR quantified", c2_nfr_quant(report, thought)),
        ("C3  Trace tags", c3_trace_tags(report)),
        ("C4  3-path", c4_three_paths(report)),
        ("C5  5W1H", c5_w5h(report)),
        ("C6  Zero placeholder", c6_zero_placeholder(report + thought)),
        ("C7  Thought-cache", c7_thought_cache(thought)),
        ("C8  Schema compliance", c8_schema_compliance(report, thought)),
    ]

    print("BA Elicitor — validate_outputs.py")
    print("-" * 40)
    failed = 0
    for name, (ok, detail) in checks:
        mark = "PASS" if ok else "FAIL"
        if not ok:
            failed += 1
        print(f"[{mark}] {name}: {detail}")

    print("-" * 40)
    if failed:
        print(f"RESULT: FAIL ({failed}/{len(checks)} criteria failed)")
        sys.exit(1)
    print(f"RESULT: PASS ({len(checks)}/8 criteria)")
    sys.exit(0)


if __name__ == "__main__":
    main()
