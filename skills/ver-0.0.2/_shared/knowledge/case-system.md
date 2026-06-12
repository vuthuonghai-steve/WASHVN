# CASE System — Confidence-Aware Skill Execution

> **Framework**: Heavy Thinking inspired improvements for Agent Skills
> **Purpose**: 3-mechanism system to PREVENT → DETECT → RECOVER from errors

---

## Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    CASE SYSTEM                               │
│                                                              │
│   PREVENT        →        DETECT         →        RECOVER     │
│   State-aware        Gate validators         Rollback         │
│   boot + PD         + reverse              procedures       │
│   triggers          trace                                    │
└─────────────────────────────────────────────────────────────┘
```

---

## Mechanism 1: PREVENT

### State-Aware Boot

Every skill invocation MUST check status BEFORE proceeding:

```python
# check_status.py pseudocode
def check_status(design_path):
    frontmatter = read_yaml_frontmatter(design_path)
    status = frontmatter.get('status', {})
    
    return {
        'phase': status.get('phase', 0),
        'gates_passed': status.get('gates_passed', []),
        'last_actor': status.get('last_actor', 'unknown'),
        'updated': status.get('updated', None)
    }
```

### Boot Sequence

```
1. AI reads SKILL.md (Tier 1)
2. AI runs check_status.py → gets status block
3. AI determines current position:
   - phase = 0 → Fresh start, load Tier 2 files
   - phase > 0 → Ask user: resume or restart?
4. AI loads required Tier 2 files per triggers
5. AI continues from checkpoint
```

### Explicit Progressive Disclosure Triggers

Tier 2 files have CONCRETE triggers, not "load when needed":

```yaml
tier2:
  - path: "knowledge/case-system.md"
    triggers:
      - WHEN: skill-name is confirmed
      - WHEN: entering Phase 1
      - WHEN: confidence < 70%
    MUST_READ_BEFORE:
      - gates.phase1
  
  - path: "scripts/check_status.py"
    triggers:
      - WHEN: boot_sequence
    MUST_READ_BEFORE:
      - boot.sequence
```

---

## Mechanism 2: DETECT

### Gate Validators

Each gate has a MACHINE-CHECKABLE checklist:

```python
# Gate 1 Checklist
gate1_checklist = {
    'skill_name_kebab': 'file exists and kebab-case',
    'problem_statement_min_50_words': True,
    'user_specified': 'not just "user"',
    'confidence_declared': '>= 70%',
}

# Gate 2 Checklist
gate2_checklist = {
    'pillar1_knowledge_min_2': True,
    'pillar2_process_has_branching': True,
    'pillar3_guardrails_min_3': True,
    'zone_mapping_no_empty': True,
    'zone_mapping_files_exist_or_na': True,
}

# Gate 3 Checklist
gate3_checklist = {
    'd1_folder_structure_min_3_zones': True,
    'd2_execution_flow_min_2_decisions': True,
    'd3_workflow_all_phases': True,
    'section5_matches_section6': True,
    'section7_pds_tier1_mandatory': True,
}
```

### Validation Script Pattern

```python
# validate_gate.py
import sys
import yaml

def validate_gate(gate_number, design_path):
    checklist = load_checklist(gate_number)
    frontmatter = load_frontmatter(design_path)
    
    failures = []
    for item, criterion in checklist.items():
        if not check(item, criterion, frontmatter):
            failures.append(item)
    
    if failures:
        print(f"GATE {gate_number} FAILED: {failures}")
        sys.exit(1)  # Exit code 1 = FAIL
    
    print(f"GATE {gate_number} PASSED")
    sys.exit(0)  # Exit code 0 = PASS
```

### Reverse Trace

After each phase, verify coherence WITH PREVIOUS phases:

```python
def reverse_trace(design):
    """Verify output matches input"""
    issues = []
    
    # §3 Zone Mapping must trace to §1 Pain Point
    zones = design['zone_mapping']
    pain_points = design['problem_statement']
    
    for zone, files in zones.items():
        if files and not trace_to_pain_point(zone, pain_points):
            issues.append(f"{zone} has files but no pain point trace")
    
    return issues
```

---

## Mechanism 3: RECOVER

### Rollback Triggers

| Trigger | Action |
|---------|--------|
| User rejects gate output | Rollback to previous phase |
| Validation fails 3 times | Stop and report |
| Emergency: design corrupted | Restore from last valid checkpoint |

### Rollback Procedure

```python
def rollback(design_path, target_phase):
    """Rollback design.md to checkpoint at target_phase"""
    
    # 1. Read current design
    with open(design_path) as f:
        content = f.read()
    
    # 2. Find checkpoint marker
    checkpoint = find_checkpoint(content, target_phase)
    
    if checkpoint:
        # 3. Restore to checkpoint
        restore_to_checkpoint(checkpoint)
        # 4. Update status
        update_status_phase(target_phase - 1)
        print(f"Rolled back to phase {target_phase - 1}")
    else:
        print("ERROR: No valid checkpoint found")
        sys.exit(2)  # Exit code 2 = EMERGENCY
```

### Checkpoint Resume

```python
def resume_from_checkpoint(design_path):
    """Resume skill execution from last checkpoint"""
    
    status = check_status(design_path)
    phase = status['phase']
    
    if phase == 0:
        return "fresh_start"
    
    # Load checkpoint data
    checkpoint = load_checkpoint(design_path, phase)
    
    # Verify checkpoint not stale (> 7 days)
    if is_stale(checkpoint):
        print("WARNING: Checkpoint is stale (> 7 days)")
        return "stale_checkpoint"
    
    return f"resume_phase_{phase}"
```

---

## Quality Dimensions

### 3-Dimensional Fitness Check

| Dimension | Metric | Pass Criterion |
|-----------|--------|----------------|
| **Completeness** | §3 Zone Mapping filled | All zones have values |
| **Coherence** | §4 matches §3, §5 matches §6 | No drift |
| **Usability** | SKILL.md can be summarized in 3 sentences | Boot <= 5 steps |

### Placeholder Density

```
Count placeholders in SKILL.md content:
- < 5: PASS (green)
- 5-9: WARNING (yellow)
- 10+: FAIL (red)
```

---

## Scripts Required

| Script | Purpose | Exit Codes |
|--------|---------|------------|
| `check_status.py` | Read status block from design.md | 0=success, 1=parse error |
| `validate_gate.py` | Validate gate checklist | 0=pass, 1=fail, 2=emergency |
| `validate_zone_mapping.py` | Validate §3 schema | 0=pass, 1=fail |

---

## Integration Points

### With skill-architect
- Architect writes status block after each gate
- Architect runs validate_gate.py before user confirmation

### With skill-planner
- Planner reads status block to determine starting point
- Planner validates §3 Zone Mapping before task creation

### With skill-builder
- Builder reads status block to resume from checkpoint
- Builder runs validation before declaring complete

---

## Key Takeaways

1. **PREVENT**: State-aware boot prevents starting from wrong position
2. **DETECT**: Gate validators catch errors BEFORE they propagate
3. **RECOVER**: Rollback procedures limit damage from failures
4. **EXIT CODES**: Machine-readable success/failure (0=pass, 1=fail)
5. **EXPLICIT TRIGGERS**: No "load when needed" — concrete conditions only
