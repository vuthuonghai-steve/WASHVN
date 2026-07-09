#!/usr/bin/env python3
import os
import sys
import yaml
import hashlib
import time
from datetime import datetime
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

def calculate_sha256(file_path):
    if not os.path.exists(file_path):
        return None
    h = hashlib.sha256()
    with open(file_path, 'rb') as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()

def load_registry():
    if not os.path.exists(REGISTRY_PATH):
        click.echo(f"Registry file not found at: {REGISTRY_PATH}", err=True)
        sys.exit(3)
    with open(REGISTRY_PATH, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def get_state(skill_dir):
    state_path = os.path.join(skill_dir, '_state.yaml')
    if os.path.exists(state_path):
        with open(state_path, 'r', encoding='utf-8') as f:
            try:
                data = yaml.safe_load(f)
                return data if isinstance(data, dict) else {}
            except Exception:
                return {}
    return {}

def save_state(skill_dir, state):
    os.makedirs(skill_dir, exist_ok=True)
    state_path = os.path.join(skill_dir, '_state.yaml')
    with open(state_path, 'w', encoding='utf-8') as f:
        yaml.safe_dump(state, f)

def parse_frontmatter(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            return yaml.safe_load(parts[1]) or {}
    return {}

def check_skill_lifecycle(skill_name, registry):
    skill_dir = os.path.join(REPO_ROOT, '.skill-context', skill_name)
    if not os.path.exists(skill_dir):
        return {"valid": False, "error": f"Skill context directory not found: {skill_dir}"}

    state = get_state(skill_dir)
    hashes = state.get('artifact_hashes', {})
    updated_hashes = hashes.copy()

    errors = []
    warnings = []

    # 1. Check generated artifacts (created_by == skill_name)
    for entry in registry.get('artifacts', []):
        if entry.get('created_by') == skill_name:
            file_name = entry.get('file_name')
            file_path = os.path.join(skill_dir, file_name)
            
            if not os.path.exists(file_path):
                # If WORM, it MUST exist if the stage ran
                if entry.get('lifecycle') == 'WORM':
                    errors.append(f"Required output artifact '{file_name}' (WORM) is missing.")
                continue

            # Parse frontmatter/data
            data = {}
            try:
                if entry.get('format') == 'markdown':
                    data = parse_frontmatter(file_path)
                elif entry.get('format') == 'yaml':
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = yaml.safe_load(f) or {}
            except Exception as e:
                errors.append(f"Failed to parse artifact '{file_name}': {e}")
                continue

            # Check timestamp
            created_at = data.get('created_at') or data.get('creation_timestamp') or data.get('analyzed_at')
            if not created_at:
                warnings.append(f"Artifact '{file_name}' is missing a creation timestamp.")

            # Check version
            version = data.get('version') or data.get('skill_version')
            if not version:
                warnings.append(f"Artifact '{file_name}' does not have a pinned version.")

            # Calculate and store current hash
            current_hash = calculate_sha256(file_path)
            updated_hashes[file_name] = current_hash

    # 2. Drift Detection (mtime vs upstream)
    # Find all upstream artifacts consumed by this skill
    for entry in registry.get('artifacts', []):
        if skill_name in entry.get('consumed_by', []):
            upstream_skill = entry.get('created_by')
            file_name = entry.get('file_name')
            upstream_file_path = os.path.join(REPO_ROOT, '.skill-context', upstream_skill, file_name)

            if os.path.exists(upstream_file_path):
                # We calculate current hash of upstream artifact
                upstream_hash = calculate_sha256(upstream_file_path)
                saved_upstream_hash = hashes.get(f"upstream_{file_name}")

                # If upstream file has a newer mtime than downstream outputs
                # But hash hasn't changed, we do NOT trigger drift warning
                mtime_upstream = os.path.getmtime(upstream_file_path)
                
                # Check downstream outputs
                for out_entry in registry.get('artifacts', []):
                    if out_entry.get('created_by') == skill_name:
                        out_file_path = os.path.join(skill_dir, out_entry.get('file_name'))
                        if os.path.exists(out_file_path):
                            mtime_out = os.path.getmtime(out_file_path)
                            if mtime_upstream > mtime_out:
                                # mtime indicates possible drift. Verify with SHA-256
                                if saved_upstream_hash and upstream_hash != saved_upstream_hash:
                                    errors.append(
                                        f"Drift detected! Upstream artifact '{file_name}' (from {upstream_skill}) "
                                        f"has been modified since outputs were built."
                                    )
                                elif not saved_upstream_hash:
                                    warnings.append(
                                        f"Possible drift. Upstream artifact '{file_name}' is newer than output, "
                                        f"and no baseline hash was found."
                                    )
                
                updated_hashes[f"upstream_{file_name}"] = upstream_hash

    # Update state
    state['artifact_hashes'] = updated_hashes
    state['last_checked'] = datetime.utcnow().isoformat()
    save_state(skill_dir, state)

    return {
        "skill": skill_name,
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings
    }

@click.command()
@click.option('--skill', help="Skill name to check (e.g. ba-analyst)")
@click.option('--all', 'check_all', is_flag=True, help="Check lifecycle for all skills in .skill-context/")
def main(skill, check_all):
    """
    Artifact Lifecycle and Integrity Validator CLI.
    Checks directory presence, timestamps, version pins, and mtime drift (with SHA-256 fallbacks).
    """
    registry = load_registry()
    context_dir = os.path.join(REPO_ROOT, '.skill-context')

    if check_all:
        if not os.path.exists(context_dir):
            click.echo("No .skill-context directory found.", err=True)
            sys.exit(2)
        
        results = []
        overall_valid = True
        for item in os.listdir(context_dir):
            skill_path = os.path.join(context_dir, item)
            if os.path.isdir(skill_path) and not item.startswith('.'):
                res = check_skill_lifecycle(item, registry)
                results.append(res)
                if not res.get("valid", True):
                    overall_valid = False
        
        click.echo(yaml.dump(results))
        sys.exit(0 if overall_valid else 1)

    if skill:
        res = check_skill_lifecycle(skill, registry)
        click.echo(yaml.dump(res))
        sys.exit(0 if res.get("valid", True) else 1)

    click.echo("Usage: artifact_lifecycle.py [OPTIONS]. Run with --help for details.", err=True)
    sys.exit(2)

if __name__ == '__main__':
    main()
