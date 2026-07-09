#!/usr/bin/env python3
import os
import sys
import json
import yaml
import jsonschema
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

def load_registry():
    if not os.path.exists(REGISTRY_PATH):
        click.echo(f"Registry file not found at: {REGISTRY_PATH}", err=True)
        sys.exit(3)
    with open(REGISTRY_PATH, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def load_schema(schema_path):
    if not os.path.exists(schema_path):
        raise FileNotFoundError(f"Schema file not found at: {schema_path}")
    with open(schema_path, 'r', encoding='utf-8') as f:
        if schema_path.endswith('.json'):
            return json.load(f)
        return yaml.safe_load(f)

def parse_artifact_data(file_path, file_format):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Artifact file not found at: {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    if file_format == 'markdown':
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                return yaml.safe_load(parts[1])
        raise ValueError(f"No YAML frontmatter found in markdown file: {file_path}")
    elif file_format == 'yaml':
        return yaml.safe_load(content)
    elif file_format == 'json':
        return json.loads(content)
    else:
        raise ValueError(f"Unsupported format: {file_format}")

def validate_artifact_file(file_path, schema_path, file_format):
    try:
        data = parse_artifact_data(file_path, file_format)
        schema = load_schema(schema_path)
        jsonschema.validate(instance=data, schema=schema)
        return {"valid": True, "errors": [], "file": file_path, "schema": schema_path}
    except jsonschema.exceptions.ValidationError as e:
        return {"valid": False, "errors": [e.message], "file": file_path, "schema": schema_path}
    except Exception as e:
        return {"valid": False, "errors": [str(e)], "file": file_path, "schema": schema_path}

@click.command()
@click.option('--all', 'validate_all', is_flag=True, help="Validate all artifacts in .skill-context/")
@click.option('--artifact', help="Artifact ID from registry (e.g. exploration_report)")
@click.option('--path', type=click.Path(exists=True), help="Path to the artifact file")
@click.option('--schema', type=click.Path(exists=True), help="Path to a custom schema file")
@click.option('--skills-registry', is_flag=True, help="Cross-check registry paths consistency")
def main(validate_all, artifact, path, schema, skills_registry):
    """
    Schema Validator CLI for Master Skill Suite artifacts.
    Exit codes:
      0: Validation passed
      1: Validation error (invalid structure or values)
      2: Path error (file or directory not found)
      3: Configuration/registry error
    """
    if skills_registry:
        registry = load_registry()
        errors = []
        for entry in registry.get('artifacts', []):
            schema_rel_path = entry.get('schema')
            if not schema_rel_path:
                errors.append(f"Artifact {entry.get('artifact_id')} has no schema defined.")
                continue
            schema_abs_path = os.path.join(REPO_ROOT, schema_rel_path)
            if not os.path.exists(schema_abs_path):
                errors.append(f"Schema file not found for {entry.get('artifact_id')}: {schema_rel_path}")
        
        if errors:
            click.echo(json.dumps({"valid": False, "errors": errors}, indent=2))
            sys.exit(3)
        else:
            click.echo(json.dumps({"valid": True, "message": "Registry paths cross-check passed."}, indent=2))
            sys.exit(0)

    if validate_all:
        registry = load_registry()
        context_dir = os.path.join(REPO_ROOT, '.skill-context')
        if not os.path.exists(context_dir):
            click.echo(json.dumps({"valid": True, "message": "No .skill-context directory found, nothing to validate."}, indent=2))
            sys.exit(0)

        results = []
        overall_valid = True
        
        # Scan .skill-context directory for skill names
        for item in os.listdir(context_dir):
            skill_dir = os.path.join(context_dir, item)
            if os.path.isdir(skill_dir) and not item.startswith('.'):
                # Try to map files in this skill dir to registry entries
                for entry in registry.get('artifacts', []):
                    file_name = entry.get('file_name')
                    artifact_file_path = os.path.join(skill_dir, file_name)
                    if os.path.exists(artifact_file_path):
                        schema_rel_path = entry.get('schema')
                        schema_abs_path = os.path.join(REPO_ROOT, schema_rel_path)
                        res = validate_artifact_file(artifact_file_path, schema_abs_path, entry.get('format'))
                        results.append(res)
                        if not res["valid"]:
                            overall_valid = False
        
        click.echo(json.dumps(results, indent=2))
        sys.exit(0 if overall_valid else 1)

    if path:
        if schema:
            # Custom schema validation
            file_format = 'markdown' if path.endswith('.md') else ('json' if path.endswith('.json') else 'yaml')
            res = validate_artifact_file(path, schema, file_format)
            click.echo(json.dumps(res, indent=2))
            sys.exit(0 if res["valid"] else 1)
        
        if not artifact:
            # Try to infer artifact from registry based on filename
            registry = load_registry()
            basename = os.path.basename(path)
            matched_entry = None
            for entry in registry.get('artifacts', []):
                if entry.get('file_name') == basename:
                    matched_entry = entry
                    break
            if matched_entry:
                artifact = matched_entry.get('artifact_id')
            else:
                click.echo(f"Cannot infer artifact type for file: {basename}. Specify --artifact or --schema.", err=True)
                sys.exit(3)

        registry = load_registry()
        matched_entry = None
        for entry in registry.get('artifacts', []):
            if entry.get('artifact_id') == artifact:
                matched_entry = entry
                break
        
        if not matched_entry:
            click.echo(f"Artifact ID '{artifact}' not found in registry.", err=True)
            sys.exit(3)
        
        schema_rel_path = matched_entry.get('schema')
        schema_abs_path = os.path.join(REPO_ROOT, schema_rel_path)
        res = validate_artifact_file(path, schema_abs_path, matched_entry.get('format'))
        click.echo(json.dumps(res, indent=2))
        sys.exit(0 if res["valid"] else 1)

    click.echo("Usage: schema_validator.py [OPTIONS]. Run with --help for details.", err=True)
    sys.exit(2)

if __name__ == '__main__':
    main()
