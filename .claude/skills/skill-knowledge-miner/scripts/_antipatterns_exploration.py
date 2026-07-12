"""
_antipatterns_exploration.py — Exploration context fallback for find_antipatterns.py

Split from find_antipatterns.py during barrel refactor.
"""

import os
import re
from skill_miner_common import read_file_safely


def extract_from_exploration(exploration_path, logger=None):
    """Parse exploration.md for existing anti-pattern documentation"""
    antipatterns = []
    if not exploration_path or not os.path.isfile(exploration_path):
        return antipatterns

    content = read_file_safely(exploration_path, logger)
    if content is None:
        return antipatterns

    in_risk_section = False
    for line in content.split('\n'):
        if re.match(r'^##\s*(?:Risks?\s*&?\s*Open|Anti-Pattern|Rủi ro|Risks?)', line):
            in_risk_section = True
            continue
        if in_risk_section and line.startswith('## ') and not line.startswith('###'):
            in_risk_section = False
            continue
        if in_risk_section:
            tm = re.match(r'^\|\s*\d+\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|', line)
            if tm:
                name = tm.group(1).strip()
                symptom = tm.group(2).strip()
                solution = tm.group(3).strip()
                if name and solution:
                    antipatterns.append({
                        "name": f"Risk: {name}",
                        "symptom": symptom,
                        "solution": solution,
                        "_source": os.path.basename(exploration_path),
                    })

    return antipatterns
