# Matcher Classification (Character-Set Analysis)
# [TỪ DESIGN §2.1, §8 R1] [TỪ HANDBOOK §6.2]

The matcher mode is **inferred from character set** — there is NO mode flag. This is the #1 footgun.

## Rule
| Input characters | Mode | Example |
|---|---|---|
| Only `[a-zA-Z0-9 \-,\|]` | Exact / OR split | `"bash"`, `"Read, Write, Edit"` |
| Contains any other char | Regex (case-insensitive) | `"^git"`, `"\.(env\|secret)$"` |

- OR: pipe segments are alternatives; whitespace around `|` stripped.
- Regex: JS-compatible, case-insensitive.

## Footgun (warn the user)
A literal `.` in the matcher forces REGEX mode.
- `codegraph.explore` → classified as REGEX, NOT exact.
- `my.tool` → REGEX.
The skill MUST emit a warning when a matcher containing `.` is supplied for an exact-match intent.
[TỪ HANDBOOK §10 insight 1]

## Implementation
`scripts/matcher_classifier.py` applies `data/matcher-char-rules.yaml`:
- scan chars → exact_or vs regex
- if `.` present → `warning=true`, `mode=regex`

## If-condition operators (separate from matcher)
`==`, `!=`, `=~`, `in`. Context: `tool.name`, `tool.params.*`, `event.type`, `session.projectDir`.
[TỪ HANDBOOK §6 / hooks-reference.md §4]
