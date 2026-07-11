#!/usr/bin/env python3
"""
init_context.py — Khởi tạo cấu trúc thư mục .skill-context/{target_skill}/ cho Stage 0: skill-explorer.
Hỗ trợ cả chế độ khởi tạo Explorer ban đầu và chế độ Smart Context Splitter để phân rã Micro-skills.

Usage:
    # Chế độ khởi tạo đơn (mặc định)
    python3 init_context.py <skill-name>

    # Chế độ Smart Context Splitter (phân rã Micro-skills hạ nguồn)
    python3 init_context.py --split .skill-context/knowledge-distiller/exploration.md
"""

import sys
import os
import re
import yaml
import shutil
from pathlib import Path
from datetime import datetime, timezone

KEBAB_CASE_PATTERN = re.compile(r"^[a-z][a-z0-9]*(-[a-z0-9]+)*$")
MAX_WALK_UP_LEVELS = 10


def find_project_root(start_dir: Path) -> Path | None:
    """Walk up to find the directory containing .claude/ or .git/."""
    current = start_dir.resolve()
    for _ in range(MAX_WALK_UP_LEVELS):
        if (current / ".claude").is_dir() or (current / ".git").is_dir():
            return current
        parent = current.parent
        if parent == current:
            break
        current = parent
    return None


def validate_skill_name(name: str) -> bool:
    """Check if skill name is valid kebab-case."""
    return bool(KEBAB_CASE_PATTERN.match(name))


def replace_placeholders(content: str, replacements: dict[str, str]) -> str:
    """Replace all placeholders in content."""
    for placeholder, value in replacements.items():
        content = content.replace(placeholder, value)
    return content


def safe_create_file(filepath: Path, content: str) -> str:
    """Create file only if it does not exist. Return status string."""
    if filepath.exists():
        return "SKIPPED (already exists)"
    filepath.write_text(content, encoding="utf-8")
    return "CREATED"


def parse_frontmatter(filepath: Path):
    """Parse YAML frontmatter from exploration.md."""
    try:
        content = filepath.read_text(encoding="utf-8")
    except Exception as e:
        return None, f"Failed to read file: {e}"

    match = re.match(r"^---\s*\n(.*?)\n(?:---|\.\.\.)", content, re.DOTALL)
    if not match:
        return None, "No YAML frontmatter found"

    try:
        data = yaml.safe_load(match.group(1))
        return data, None
    except Exception as e:
        return None, f"YAML parsing error: {e}"


def handle_single_init(skill_name: str, project_root: Path, script_dir: Path) -> int:
    """Initialize a single Stage 0 exploration context."""
    context_root = project_root / ".skill-context"
    skill_context_dir = context_root / skill_name
    resources_dir = skill_context_dir / "resources"
    template_path = script_dir.parent / "templates" / "exploration.md.template"

    now_iso = datetime.now(timezone.utc).isoformat()
    replacements = {
        "{skill_name}": skill_name,
        "{date}": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "{generated_at}": now_iso,
    }

    context_root.mkdir(exist_ok=True)
    skill_context_dir.mkdir(exist_ok=True)
    resources_dir.mkdir(exist_ok=True)

    print(f"\nContext directory: {skill_context_dir}")
    print("-" * 50)

    exploration_path = skill_context_dir / "exploration.md"
    if template_path.is_file():
        raw_content = template_path.read_text(encoding="utf-8")
        content = replace_placeholders(raw_content, replacements)
        status = safe_create_file(exploration_path, content)
        print(f"  exploration.md       → {status}")
    else:
        fallback = f"# {skill_name} — Exploration\n"
        status = safe_create_file(exploration_path, fallback)
        print(f"  exploration.md       → {status}")

    print(f"\nDone: {resources_dir} and exploration.md configured successfully.")
    return 0


def handle_split_run(exploration_path: Path, project_root: Path) -> int:
    """Smart Context Splitter - parse exploration.md and generate all micro-skill folders."""
    if not exploration_path.is_file():
        print(f"Error: Exploration file not found at {exploration_path}")
        return 1

    print(f"Parsing exploration file: {exploration_path}")
    data, err = parse_frontmatter(exploration_path)
    if err:
        print(f"Error: {err}")
        return 1

    decomposed = data.get("decomposed", False)
    micro_skills = data.get("micro_skills", [])
    master_name = data.get("skill_name", "master-skill")

    if not decomposed or not micro_skills:
        print("Info: This exploration.md is not flagged for decomposition ('decomposed: true' and 'micro_skills' array needed).")
        print("No micro-skills to split.")
        return 0

    print(f"\nSmart Context Splitter: Found {len(micro_skills)} Micro-skills from Master '{master_name}'")
    print("=" * 60)

    context_root = project_root / ".skill-context"
    master_resources_dir = exploration_path.parent / "resources"
    now_iso = datetime.now(timezone.utc).isoformat()
    now_date = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    results = []

    for item in micro_skills:
        name = item.get("name")
        description = item.get("description", "Không có mô tả")
        zones = item.get("zone_recommendations", "N/A")

        if not name or not validate_skill_name(name):
            print(f"  ❌ Skipping invalid micro-skill name: '{name}'")
            continue

        child_context_dir = exploration_path.parent / name
        child_resources_dir = child_context_dir / "resources"

        # Create child directories
        child_context_dir.mkdir(exist_ok=True)
        child_resources_dir.mkdir(exist_ok=True)

        # Copy resources from master resources dir to inherit 100% of the mined domain knowledge
        copied_resources = []
        if master_resources_dir.is_dir():
            for f in master_resources_dir.iterdir():
                if f.is_file():
                    shutil.copy(f, child_resources_dir / f.name)
                    copied_resources.append(f.name)

        # Generate custom design.md for the micro-skill
        child_design_path = child_context_dir / "design.md"
        
        # Build specific zone_mapping configuration
        zone_mapping_str = """zone_mapping:
  core:
    files:
      - path: "SKILL.md"
        file_required: true
        content_type: "persona-definition"
    zone_required: true
  knowledge:
    files:
      - path: "knowledge/standards.md"
        file_required: true
        content_type: "domain-knowledge"
    zone_required: true
  scripts:
    files: []
    zone_required: false
  templates:
    files: []
    zone_required: false
  data:
    files: []
    zone_required: false
  loop:
    files:
      - path: "loop/checklist.md"
        file_required: true
        content_type: "quality-gate"
    zone_required: true
  assets:
    files: []
    zone_required: false"""

        design_content = f"""---
skill_schema_version: "3.0.0"
artifact_type: "design"
skill_name: "{name}"
generated_by: "skill-explorer"
generated_at: "{now_iso}"
stage: "architect"
status: "in_progress"
is_micro_skill: true
parent_skill: "{master_name}"
canonical_source:
  zone_mapping: "frontmatter.zone_mapping"
  progressive_disclosure: "frontmatter.progressive_disclosure"
{zone_mapping_str}
progressive_disclosure:
  tier1:
    - path: "SKILL.md"
      base: "skill_dir"
    - path: "loop/checklist.md"
      base: "skill_dir"
  tier2:
    - path: "knowledge/standards.md"
      base: "skill_dir"
      load_when: "Executing core logic"
  tier3: []
required_sections:
  - "1_problem_statement"
  - "2_capability_map"
  - "3_zone_mapping"
  - "4_folder_structure"
  - "5_execution_flow"
  - "6_interaction_points"
  - "7_progressive_disclosure"
  - "8_risks"
  - "9_open_questions"
  - "10_metadata"
handoff:
  next_stage: "planner"
  ready_condition:
    required:
      frontmatter_valid: true
      zone_mapping_complete: true
      required_sections_present: true
      no_blockers: true
---

# {name} — Phân Rã Kiến Trúc Micro-Skill

> **Khởi tạo**: {now_date}
> **Nguồn gốc**: Báo cáo Stage 0 của master skill '{master_name}'
> **Bản đồ chỉ dẫn cha**: [master-exploration](file://{exploration_path.resolve()})
> **Quy tắc đệ quy**: [CẤM PHÂN RÃ] Đây là nút lá của hệ thống.

---

## 1. Problem Statement

### A. Vấn đề thực tế (Pain Points)
[TỪ EXPLORATION §1 & §3.3]
Kế thừa từ Master Skill '{master_name}' để giải quyết độc lập tác vụ chuyên biệt sau:
- **Tác vụ**: {description}

### B. Vai trò trong Orchestration Flow
[TỪ EXPLORATION §5]
Quy hoạch khuyến nghị phân vùng Zones ban đầu: {zones}

## 2. Capability Map

[TỪ EXPLORATION §3.3 & §4]
- **Nhiệm vụ nghiệp vụ chính**: {description}
- **Ràng buộc AI chuyên biệt**: Xem chỉ dẫn tương ứng trong tài liệu resources/ đã kế thừa.

## 3. Zone Mapping

## 4. Folder Structure

## 5. Execution Flow

## 6. Interaction Points

## 7. Progressive Disclosure Plan

## 8. Risks & Blind Spots

## 9. Open Questions

## 10. Metadata
"""
        status = safe_create_file(child_design_path, design_content)
        results.append((name, status, len(copied_resources)))

    print(f"\nDone: Micro-skills generated successfully!")
    print("-" * 75)
    print(f"{'Micro-Skill Name':<25} | {'design.md Status':<20} | {'Resources Inherited':<20}")
    print("-" * 75)
    for name, status, res_count in results:
        print(f"{name:<25} | {status:<20} | {res_count:<20} files")
    print("-" * 75)
    print("Mọi micro-skills đã được chuẩn bị sẵn tệp design.md chứa cờ is_micro_skill: true.")
    print("Sẵn sàng cho Stage 1: skill-architect tiếp quản mà không cần chạy lại Stage 0!")
    return 0


def main() -> int:
    import argparse
    parser = argparse.ArgumentParser(description="Initialize Stage 0 exploration or Split Micro-skills context")
    parser.add_argument("skill_name", nargs="?", help="Skill name in kebab-case")
    parser.add_argument("--split", help="Path to exploration.md file to perform Smart Context Splitting")
    parser.add_argument("--project-root", default=None, help="Override project root")
    args = parser.parse_args()

    # --- Detect project root ---
    script_dir = Path(__file__).resolve().parent
    if args.project_root:
        project_root = Path(args.project_root)
    else:
        project_root = find_project_root(Path.cwd())
        if project_root is None:
            project_root = find_project_root(script_dir)
            if project_root is None:
                print("Error: Could not find project root directory.")
                return 1

    if args.split:
        exploration_path = Path(args.split)
        return handle_split_run(exploration_path, project_root)
    elif args.skill_name:
        return handle_single_init(args.skill_name, project_root, script_dir)
    else:
        print("Error: Please provide either a <skill_name> for single init OR --split <path> to split context.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
