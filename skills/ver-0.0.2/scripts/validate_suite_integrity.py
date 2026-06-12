#!/usr/bin/env python3
"""
validate_suite_integrity.py — Programmatic verification script to check path references and
format specifications for the ver-3 Master Skill Suite.

Usage:
    python3 validate_suite_integrity.py
"""

import sys
import os
import re
import yaml
from pathlib import Path

# Base directories
SUITE_ROOT = Path(__file__).resolve().parent.parent
SHARED_DIR = SUITE_ROOT / "_shared"

SKILLS = [
    "skill-explorer",
    "skill-knowledge-miner",
    "skill-architect",
    "production-quality-gatekeeper",
    "skill-planner",
    "skill-builder",
    "production-code-reviewer",
    "ba-elicitor",
    "ba-analyst",
    "ba-synthesizer",
    "skill-security-reviewer"
]

def check_file_path(base_dir, relative_str):
    # Try resolving relative path based on file directory
    clean_str = relative_str.strip().strip("'").strip('"')
    
    # Ignore absolute system environment variables
    if clean_str.startswith("${CLAUDE_SKILL_DIR}"):
        clean_str = clean_str.replace("${CLAUDE_SKILL_DIR}", "")
        
    if not clean_str:
        return True, ""
        
    target_path = Path(base_dir) / clean_str
    if target_path.exists():
        return True, str(target_path.resolve())
    return False, str(target_path)

def analyze_skill_markdown(skill_name):
    skill_dir = SUITE_ROOT / skill_name
    skill_file = skill_dir / "SKILL.md"
    
    if not skill_file.exists():
        return {
            "name": skill_name,
            "status": "MISSING",
            "errors": [f"Tệp SKILL.md không tồn tại tại {skill_file}"]
        }
        
    content = skill_file.read_text(encoding="utf-8")
    errors = []
    warnings = []
    
    # 1. Frontmatter check
    fm_match = re.match(r"^---\s*\n(.*?)\n(?:---|\.\.\.)", content, re.DOTALL)
    if not fm_match:
        errors.append("Thiếu frontmatter YAML bắt buộc ở dòng 1.")
    else:
        try:
            fm_data = yaml.safe_load(fm_match.group(1))
            if not fm_data:
                errors.append("Frontmatter YAML rỗng.")
            else:
                # Check version
                version = str(fm_data.get("version", ""))
                if version != "0.0.1":
                    errors.append(f"Frontmatter 'version' phải là '0.0.1' (hiện tại: '{version}').")
                # Check suite
                suite = fm_data.get("suite", "")
                if suite != "WASHVN":
                    errors.append(f"Frontmatter 'suite' phải là 'WASHVN' (hiện tại: '{suite}').")
        except Exception as e:
            errors.append(f"Lỗi cú pháp frontmatter YAML: {e}")

    # 2. XML Boundaries
    for tag in ["instructions", "context", "output_contract"]:
        if f"<{tag}>" not in content or f"</{tag}>" not in content:
            errors.append(f"Thiếu thẻ XML ranh giới ngữ nghĩa: <{tag}> hoặc </{tag}>.")
            
    # 3. must/must_not YAML block in instructions
    if "<instructions>" in content:
        instr_match = re.search(r"<instructions>(.*?)</instructions>", content, re.DOTALL)
        if instr_match:
            instr_text = instr_match.group(1).lower()
            if "must:" not in instr_text and "must_not:" not in instr_text:
                errors.append("Khối <instructions> thiếu phân cấp YAML 'must:' hoặc 'must_not:'.")

    # 4. output_contract DRC check
    if "<output_contract>" in content:
        oc_match = re.search(r"<output_contract>(.*?)</output_contract>", content, re.DOTALL)
        if oc_match:
            try:
                oc_data = yaml.safe_load(oc_match.group(1))
                if not oc_data:
                    errors.append("output_contract rỗng.")
                else:
                    output_type = oc_data.get("output_type", "")
                    if output_type not in ["Type 1 (Monolithic Stage)", "Type 2 (Hierarchical Micro-skill)"]:
                        errors.append(f"output_contract: output_type không hợp lệ: '{output_type}'")
                    
                    target_var = oc_data.get("target_context_variable", "")
                    if target_var not in ["target_skill", "feature_name"]:
                        errors.append(f"output_contract: target_context_variable không hợp lệ: '{target_var}'")
                        
                    dest_rules = oc_data.get("destination_rules", [])
                    if not isinstance(dest_rules, list) or len(dest_rules) == 0:
                        errors.append("output_contract: destination_rules phải là danh sách hợp lệ và không rỗng.")
                    else:
                        for rule in dest_rules:
                            file_id = rule.get("file_id")
                            path_template = rule.get("path_template")
                            fmt = rule.get("format")
                            if not file_id or not path_template or not fmt:
                                errors.append(f"output_contract rule thiếu file_id, path_template, hoặc format: {rule}")
                            else:
                                if not path_template.startswith(".skill-context/"):
                                    errors.append(f"output_contract: path_template phải bắt đầu bằng '.skill-context/': '{path_template}'")
                                var_bracket = f"{{{target_var}}}"
                                if var_bracket not in path_template:
                                    errors.append(f"output_contract: path_template '{path_template}' phải chứa biến '{var_bracket}'")
            except Exception as e:
                errors.append(f"Lỗi cú pháp output_contract YAML: {e}")
                
    # 5. Path references inside boot sequence or progressive disclosure
    # Find all path-like strings (e.g. ../_shared/..., knowledge/..., templates/...)
    paths = re.findall(r"[`'\"]?(\.\.?/[a-zA-Z_0-9\-\.\/_]+|knowledge/[a-zA-Z_0-9\-\.\/_]+|policy/[a-zA-Z_0-9\-\.\/_]+|templates/[a-zA-Z_0-9\-\.\/_]+|scripts/[a-zA-Z_0-9\-\.\/_]+|data/[a-zA-Z_0-9\-\.\/_]+|loop/[a-zA-Z_0-9\-\.\/_]+)[`'\"]?", content)
    for p in paths:
        # Ignore extensionless references or template values like {skill-name} / {target_skill} / {feature_name}
        if any(v in p for v in ["{skill-name}", "{target_skill}", "{feature_name}"]):
            continue
        # Ignore prose examples in planners or dynamic runtime outputs
        if p in ["data/config.yaml", "data/schema.json", "knowledge/domain-handbook.md", "data/quality-matrix.yaml", "policy/quality-matrix.yaml", "policy/review-rules.yaml", "scripts/orchestrate.py", "loop/build-log.md", "knowledge/domain-rules.md"]:
            continue
        exists, resolved = check_file_path(skill_dir, p)
        if not exists:
            # Check if it refers to context directories which will be created dynamically
            if ".skill-context" in p or "resources/" in p:
                continue
            errors.append(f"Liên kết tham chiếu hỏng (Broken link): '{p}' không tồn tại.")

    return {
        "name": skill_name,
        "status": "FAIL" if errors else "PASS",
        "errors": errors,
        "warnings": warnings,
        "output_contract": oc_data if 'oc_data' in locals() else None
    }

def generate_registry_markdown(results):
    from datetime import datetime, timezone
    
    registry_file = SHARED_DIR / "knowledge" / "output-registry.md"
    
    # Header
    now_str = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    lines = [
        "# 📋 WASHVN Skill Suite — Output Registry",
        "",
        f"> **Tự động tạo bởi**: `validate_suite_integrity.py`  ",
        f"> **Phiên bản bộ suite**: `0.0.1`  ",
        f"> **Cập nhật lúc**: `{now_str}`  ",
        "",
        "Tài liệu này đăng ký và liệt kê toàn bộ các tệp đầu ra (output files) được quy hoạch trong bộ kỹ năng WASHVN, phân loại theo cấu trúc Type 1 (Monolithic Stage) và Type 2 (Hierarchical Micro-skill).",
        "",
        "---",
        "",
        "## 1. Phân loại theo Kỹ năng (By Skill)",
        "",
        "| Kỹ năng (Skill) | Loại (Type) | Biến định tuyến (Routing Var) | Tệp đầu ra (Output File) | Đường dẫn định mẫu (Path Template) | Định dạng (Format) |",
        "|---|---|---|---|---|---|",
    ]
    
    all_templates = []
    
    for r in results:
        skill_name = r["name"]
        oc = r.get("output_contract")
        if not oc:
            continue
            
        output_type = oc.get("output_type", "N/A")
        target_var = oc.get("target_context_variable", "N/A")
        dest_rules = oc.get("destination_rules", [])
        
        for rule in dest_rules:
            file_id = rule.get("file_id", "N/A")
            path_template = rule.get("path_template", "N/A")
            fmt = rule.get("format", "N/A")
            
            lines.append(f"| `{skill_name}` | {output_type} | `{target_var}` | `{file_id}` | `{path_template}` | `{fmt}` |")
            all_templates.append((path_template, file_id, skill_name))
            
    lines.extend([
        "",
        "---",
        "",
        "## 2. Danh sách Đường dẫn định mẫu (All Path Templates)",
        ""
    ])
    
    # Sort templates alphabetically by path
    all_templates.sort(key=lambda x: x[0])
    for path, file_id, skill in all_templates:
        lines.append(f"- [ ] `{path}` (ID: `{file_id}` từ `{skill}`)")
        
    lines.append("")
    
    content = "\n".join(lines)
    registry_file.write_text(content, encoding="utf-8")
    print(f"✅ Đã cập nhật tệp đăng ký đầu ra tại: {registry_file}")

def main():
    print("=====================================================================")
    print("🔄 PROGRAMMATIC INTEGRITY CHECKER FOR MASTER SKILL SUITE ver-3")
    print("=====================================================================")
    
    suite_errors = 0
    results = []
    
    # Check Skills
    for skill in SKILLS:
        result = analyze_skill_markdown(skill)
        results.append(result)
        print(f"Skill: {result['name']} -> Verdict: {'✅ PASS' if result['status'] == 'PASS' else '❌ FAIL'}")
        if result["errors"]:
            for err in result["errors"]:
                print(f"  - Error: {err}")
            suite_errors += len(result["errors"])
        if result["warnings"]:
            for warn in result["warnings"]:
                print(f"  - Warning: {warn}")
        print("-" * 69)
        
    # Check _shared directory existence
    if not SHARED_DIR.exists():
        print("❌ FAIL: Thư mục _shared không tồn tại!")
        suite_errors += 1
    else:
        print("✅ PASS: Thư mục _shared tồn tại.")
        # Check standard files in shared
        for f in ["knowledge/framework.md", "knowledge/case-system.md"]:
            p = SHARED_DIR / f
            if p.exists():
                print(f"  - Found: _shared/{f}")
            else:
                print(f"  - Error: Thiếu tệp _shared/{f} quan trọng!")
                suite_errors += 1

    # Generate registry only if there are no errors
    if suite_errors == 0:
        generate_registry_markdown(results)

    print("=====================================================================")
    print(f"📊 SUMMARY OF SUITE INTEGRITY: {suite_errors} Errors Found")
    print("=====================================================================")
    sys.exit(1 if suite_errors > 0 else 0)

if __name__ == "__main__":
    main()
