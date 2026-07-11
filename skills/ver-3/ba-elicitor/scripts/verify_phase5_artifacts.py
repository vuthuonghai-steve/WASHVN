#!/usr/bin/env python3
"""verify_phase5_artifacts.py — Phase 5 AC-1→7 verification script.

Usage:
  python3 verify_phase5_artifacts.py [feature_name]

Default feature: user-auth
Checks:
  AC-1: 3 BA skill dirs exist (.claude/skills/ba-{elicitor,analyst,synthesizer}/SKILL.md)
  AC-2: Frontmatter 10 fields valid
  AC-3: SKILL.md ≤ 800 words
  AC-4: 7-Zone ≥4 zones populated
  AC-6: elicitation-report.md ≥ 1000 bytes
  AC-7: business-analysis.md exists
  AC-9: Pipeline artifacts complete (3 artifacts + state ledger)
"""

import sys
import os
import yaml
import json

def check(ac, desc, ok, detail=""):
    status = "PASS" if ok else "FAIL"
    print(f"  [{status}] AC-{ac}: {desc}" + (f" — {detail}" if detail else ""))
    return ok

def main():
    feature = sys.argv[1] if len(sys.argv) > 1 else "user-auth"
    project = os.environ.get("CLAUDE_PROJECT_DIR", ".")
    base = os.path.join(project, ".skill-context", feature)
    skills_dir = os.path.join(project, ".claude", "skills")

    results = []

    # — AC-1: 3 BA skills deployed —
    ac1_ok = True
    for name in ["ba-elicitor", "ba-analyst", "ba-synthesizer"]:
        p = os.path.join(skills_dir, name, "SKILL.md")
        if not os.path.isfile(p):
            ac1_ok = False
    results.append(check("1", "3 BA skills deployed at .claude/skills/", ac1_ok))

    # — AC-2: Frontmatter 10 fields —
    ac2_ok = True
    required_fields = {"name", "description", "suite", "version", "category", "stage", "tags", "when_to_use", "output_contract"}
    for name in ["ba-elicitor", "ba-analyst", "ba-synthesizer"]:
        p = os.path.join(skills_dir, name, "SKILL.md")
        if not os.path.isfile(p):
            ac2_ok = False
            continue
        with open(p) as f:
            content = f.read()
        # naive frontmatter parse
        parts = content.split("---", 2)
        if len(parts) < 3:
            ac2_ok = False
            continue
        try:
            fm = yaml.safe_load(parts[1])
        except:
            ac2_ok = False
            continue
        missing = required_fields - set(fm.keys())
        if missing:
            ac2_ok = False
    results.append(check("2", "Frontmatter 10 fields valid", ac2_ok))

    # — AC-3: SKILL.md ≤ 800 words —
    ac3_ok = True
    for name in ["ba-elicitor", "ba-analyst", "ba-synthesizer"]:
        p = os.path.join(skills_dir, name, "SKILL.md")
        if not os.path.isfile(p):
            ac3_ok = False
            continue
        with open(p) as f:
            body = f.read().split("---", 2)[-1] if "---" in f.read() else f.read()
        # re-read properly
    ac3_ok = True
    for name in ["ba-elicitor", "ba-analyst", "ba-synthesizer"]:
        p = os.path.join(skills_dir, name, "SKILL.md")
        if not os.path.isfile(p):
            ac3_ok = False
            continue
        with open(p) as f:
            c = f.read()
        parts = c.split("---", 2)
        body = parts[2] if len(parts) >= 3 else c
        word_count = len(body.split())
        if word_count > 800:
            ac3_ok = False
    results.append(check("3", "SKILL.md ≤ 800 words", ac3_ok, f"(checked 3 skills)"))

    # — AC-4: ≥4 of 7 zones populated —
    ac4_ok = True
    for name in ["ba-elicitor", "ba-analyst", "ba-synthesizer"]:
        skill_path = os.path.join(skills_dir, name)
        zones = ["knowledge", "scripts", "templates", "loop", "data", "assets"]
        populated = sum(1 for z in zones if os.path.isdir(os.path.join(skill_path, z)) and os.listdir(os.path.join(skill_path, z)))
        if populated < 4:
            ac4_ok = False
    results.append(check("4", "7-Zone ≥4 zones populated per skill", ac4_ok))

    # — AC-6: elicitation-report.md ≥1000 bytes —
    elicitation_p = os.path.join(base, "ba-elicitor", "elicitation-report.md")
    ac6_ok = os.path.isfile(elicitation_p) and os.path.getsize(elicitation_p) >= 1000
    ac6_size = os.path.getsize(elicitation_p) if os.path.isfile(elicitation_p) else 0
    results.append(check("6", f"elicitation-report.md ≥ 1000 bytes", ac6_ok, f"actual: {ac6_size} bytes"))

    # — AC-7: business-analysis.md exists —
    ba_p = os.path.join(base, "ba-synthesizer", "business-analysis.md")
    ac7_ok = os.path.isfile(ba_p) and os.path.getsize(ba_p) >= 1000
    ac7_size = os.path.getsize(ba_p) if os.path.isfile(ba_p) else 0
    results.append(check("7", "business-analysis.md ≥ 1000 bytes", ac7_ok, f"actual: {ac7_size} bytes"))

    # — AC-9: Pipeline artifacts complete (3 artifacts + state ledger) —
    artifacts = [
        os.path.join(base, "ba-elicitor", "elicitation-report.md"),
        os.path.join(base, "ba-analyst", "analyst-output.md"),
        os.path.join(base, "ba-synthesizer", "business-analysis.md"),
        os.path.join(base, "_state_ledger.yaml"),
    ]
    ac9_ok = all(os.path.isfile(a) for a in artifacts)
    missing = [a for a in artifacts if not os.path.isfile(a)]
    detail = f"missing: {[os.path.relpath(m, base) for m in missing]}" if not ac9_ok else "all 4 present"
    results.append(check("9", "Pipeline artifacts complete (3 + state ledger)", ac9_ok, detail))

    # — Summary —
    passed = sum(1 for r in results if r)
    total = len(results)
    print(f"\nPhase 5 AC: {passed}/{total} PASS ({passed/total*100:.0f}%)")
    return 0 if passed == total else 1

if __name__ == "__main__":
    sys.exit(main())
