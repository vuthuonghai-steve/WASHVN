# 5-Location Merge + Shadowing
# [TỪ DESIGN §2.1, §8 R2] [TỪ HANDBOOK §7.1]

Hooks resolve from 5 locations in ascending priority. **Last writer wins by MERGE** (not override). For the same event+matcher pair, higher-priority handlers replace lower-priority ones at the handler level.

| Priority | Key | Scope | File |
|----------|-----|-------|------|
| 1 (low) | user | all projects | `~/.claude/settings.json` |
| 2 | project | single project | `.claude/settings.json` |
| 3 | local | single project, gitignored | `.claude/settings.local.json` |
| 4 | plugin | per-plugin | plugin manifest |
| 5 (high) | agent_frontmatter | per-agent | `.claude/agents/<name>.md` |

## Shadowing
A hook written at priority 2 (project) can be **silently nullified** by:
- same event+matcher at priority 3 (local), or
- agent-frontmatter hook (priority 5).

`scripts/location_resolver.py` detects collisions and the skill MUST warn (Interaction Point #3).
[TỪ HANDBOOK §10 insight 2]

## Nested merge semantics (Q7)
Behavior for conflicting matcher groups across locations with same event is **empirically unconfirmed**.
**Policy: WARN only. Do NOT auto-merge.** [TỪ DESIGN §9 Q7]
The skill surfaces a warning and asks the user to confirm target location; it never silently reconciles.
