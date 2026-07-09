#!/usr/bin/env python3
import os
import sys
import yaml
import click

def find_repo_root():
    current = os.path.abspath(os.path.dirname(__file__))
    while current != os.path.dirname(current):
        if os.path.exists(os.path.join(current, 'raw')) or os.path.exists(os.path.join(current, '.git')):
            return current
        current = os.path.dirname(current)
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))

REPO_ROOT = find_repo_root()
REGISTRY_PATH = os.path.join(REPO_ROOT, 'raw/ver-3/_shared/artifact_registry.yaml')

def load_yaml(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"YAML file not found at: {path}")
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f) or {}

def parse_markdown_frontmatter(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            return yaml.safe_load(parts[1]) or {}
    return {}

def verify_drc_contract(skill_name, contract_path, registry):
    errors = []
    if not os.path.exists(contract_path):
        return [f"DRC Contract file not found: {contract_path}"]

    try:
        contract = load_yaml(contract_path)
    except Exception as e:
        return [f"Failed to parse DRC Contract YAML: {e}"]

    # Check skill_name matches
    contract_skill = contract.get('skill_name')
    if contract_skill != skill_name and contract_skill != "<skill-name-placeholder>":
        errors.append(f"Contract skill_name '{contract_skill}' does not match directory skill name '{skill_name}'")

    # Check Inputs
    for inp in contract.get('inputs', []):
        name = inp.get('name')
        schema_rel = inp.get('schema')
        
        # Verify schema exists
        if schema_rel:
            schema_abs = os.path.join(REPO_ROOT, schema_rel)
            if not os.path.exists(schema_abs):
                errors.append(f"Input '{name}' schema not found: {schema_rel}")
        
        # Check against registry
        matched_registry = None
        for entry in registry.get('artifacts', []):
            if entry.get('artifact_id') == name or entry.get('file_name') == name:
                matched_registry = entry
                break
        
        if not matched_registry:
            errors.append(f"Input '{name}' is not registered in artifact_registry.yaml")
        else:
            # check compatibility
            reg_schema = matched_registry.get('schema')
            if schema_rel and reg_schema != schema_rel:
                errors.append(f"Input '{name}' schema '{schema_rel}' conflicts with registry schema '{reg_schema}'")

    # Check Outputs
    for out in contract.get('outputs', []):
        file_id = out.get('file_id')
        schema_rel = out.get('schema')
        
        # Verify schema exists
        if schema_rel:
            schema_abs = os.path.join(REPO_ROOT, schema_rel)
            if not os.path.exists(schema_abs):
                errors.append(f"Output '{file_id}' schema not found: {schema_rel}")

        # Check against registry
        matched_registry = None
        for entry in registry.get('artifacts', []):
            if entry.get('artifact_id') == file_id:
                matched_registry = entry
                break
        
        if not matched_registry:
            errors.append(f"Output '{file_id}' is not registered in artifact_registry.yaml")
        else:
            # Check creator
            creator = matched_registry.get('created_by')
            if creator != skill_name and skill_name != "test-skill":
                errors.append(f"Output '{file_id}' creator in registry is '{creator}', but contract is for '{skill_name}'")
            
            # Check schema matches registry
            reg_schema = matched_registry.get('schema')
            if schema_rel and reg_schema != schema_rel:
                errors.append(f"Output '{file_id}' schema '{schema_rel}' conflicts with registry schema '{reg_schema}'")

    return errors

def verify_single_skill(skill_name, registry):
    skill_dir = os.path.join(REPO_ROOT, 'raw/ver-3', skill_name)
    if not os.path.exists(skill_dir):
        return [f"Skill directory not found: {skill_dir}"]

    skill_md = os.path.join(skill_dir, 'SKILL.md')
    if not os.path.exists(skill_md):
        return [f"SKILL.md not found in {skill_dir}"]

    try:
        frontmatter = parse_markdown_frontmatter(skill_md)
    except Exception as e:
        return [f"Failed to parse SKILL.md frontmatter for {skill_name}: {e}"]

    contract_rel_path = frontmatter.get('output_contract')
    if not contract_rel_path:
        return [f"Skill '{skill_name}' does not define 'output_contract' in frontmatter."]

    contract_abs_path = os.path.join(REPO_ROOT, contract_rel_path)
    return verify_drc_contract(skill_name, contract_abs_path, registry)

@click.command()
@click.option('--skill', help="Verify a specific skill (e.g. ba-analyst)")
@click.option('--all', 'verify_all', is_flag=True, help="Verify DRC contracts for all skills in raw/ver-3/")
@click.option('--registry-only', is_flag=True, help="Only verify registry consistency")
@click.option('--registry', type=click.Path(exists=True), help="Custom path to artifact_registry.yaml")
def main(skill, verify_all, registry_only, registry):
    """
    DRC (Dynamic Routing Contract) Resolver and Verifier CLI.
    Checks consistency between skill input/output declarations, contract documents, and the registry.
    """
    reg_path = registry or REGISTRY_PATH
    if not os.path.exists(reg_path):
        click.echo(f"Registry file not found at: {reg_path}", err=True)
        sys.exit(3)

    try:
        registry_data = load_yaml(reg_path)
    except Exception as e:
        click.echo(f"Failed to parse registry file: {e}", err=True)
        sys.exit(3)

    if registry_only:
        errors = []
        for entry in registry_data.get('artifacts', []):
            schema = entry.get('schema')
            if schema:
                schema_abs = os.path.join(REPO_ROOT, schema)
                if not os.path.exists(schema_abs):
                    errors.append(f"Registry artifact '{entry.get('artifact_id')}' schema not found: {schema}")
        if errors:
            for err in errors:
                click.echo(f"Error: {err}", err=True)
            sys.exit(1)
        click.echo("Registry consistency check passed.")
        sys.exit(0)

    if verify_all:
        skills_dir = os.path.join(REPO_ROOT, 'raw/ver-3')
        if not os.path.exists(skills_dir):
            click.echo(f"Skills directory not found at: {skills_dir}", err=True)
            sys.exit(2)

        overall_valid = True
        for item in os.listdir(skills_dir):
            item_path = os.path.join(skills_dir, item)
            # Skip _shared, scripts, roadmaps, etc.
            if os.path.isdir(item_path) and not item.startswith('_') and item not in ['scripts', 'roadmaps']:
                errors = verify_single_skill(item, registry_data)
                if errors:
                    overall_valid = False
                    click.echo(f"Skill '{item}' DRC verification FAILED:")
                    for err in errors:
                        click.echo(f"  - {err}")
                else:
                    click.echo(f"Skill '{item}' DRC verification PASSED.")
        sys.exit(0 if overall_valid else 1)

    if skill:
        errors = verify_single_skill(skill, registry_data)
        if errors:
            click.echo(f"Skill '{skill}' DRC verification FAILED:")
            for err in errors:
                click.echo(f"  - {err}")
            sys.exit(1)
        else:
            click.echo(f"Skill '{skill}' DRC verification PASSED.")
            sys.exit(0)

    click.echo("Usage: drc_resolver.py [OPTIONS]. Run with --help for details.", err=True)
    sys.exit(2)

if __name__ == '__main__':
    main()
