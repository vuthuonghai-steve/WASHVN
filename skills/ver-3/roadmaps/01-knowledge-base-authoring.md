# Phase 1 — Knowledge Base Authoring

> **Order:** 2nd phase | **Estimated effort:** M (medium) | **Predicted duration:** 1-2 sessions
> **Depends on:** Phase 0 (Foundation Bootstrap)
> **Downstream:** Phase 2 (Hooks), Phase 3 (Agents)
> **Architectural defects addressed:** Schéma-as-prose (extract from spec's P0 context-bus) — được spec hóa trong docs biết đọc both human và machine-parseable

## Mục đích

Phase 0 đã tạo 7 knowledge-doc stubs tại `.claude/knowledge/agents/`. Phase 1 đưa nội dung đầy đủ vào các stubs này để:
1. `subagent-forge.md` có thể reference chúng mà không bị dangling reference ([L6. Memoryschemy value] ())
2. Phase 3 có cơ sở kiến thức để build các agent production khác
3. Mở đường cho Phase 2 định nghĩa hook conventions chuẩn hoá

Phase 1 trái tim của roadmap vì subagent-forge.md hiện tại **đang broken** — `<retrieved_docs>` của nó liệt kê 7 docs không tồn tại. Mỗi lần subagent-forge invoked và đọc missing paths, nó silently skip và build agent without canonical contract.

---

## Prerequisites

```yaml
prerequisites:
  - Phase 0 done (AC-1 through AC-7 PASS)
  - 7 stubs tại .claude/knowledge/agents/ tồn tại với status: stub
  - subagent-forge.md chưa bị modified (giữ state Phase 0)
  - Temps/spec/architects/ source spec đã read for reference (P0-P7 + shared)
```

---

## Deliverables (file-by-file, 7 docs)

Mỗi doc phải có:
- YAML frontmatter: `name, version, last_updated, status: canonical, target_consumer: subagent-forge|other`
- Nội dung ≥ 100 dòng (theo subagent-forge.md minimum raw read để có context đầy đủ)
- Verbatim ID contracts / field names / examples / boundaries
- Zero placeholders (`TODO`, `FIXME`, `mock`, `pass # implement later` = FAIL)
- Liên kết file dùng cú pháp `[file](file:///absolute/path)` theo standards.md

> [!IMPORTANT]
> Không dùng placeholder. Mỗi doc phải **standalone-readable** mà không cần agent self-discovery.

### D1-1: `configuration.md` — Frontmatter Schema (16-field)

Định nghĩa schema YAML frontmatter mà file `.claude/agents/<name>.md` buộc phải có.

Nội dung bắt buộc:
- Bảng đầy đủ 16 field names — `name` (kebab-case, unique), `description` (sensitive trigger phrases, max 500 chars), `model` (`opus|sonnet|haiku|inherit`), `tools` (`[Read, Write, Edit, Bash, Glob, Grep, Task, WebFetch, NotebookEdit, TodoWrite]` random subset), `permissionMode` (`default|acceptEdits|bypassPermissions|plan`), `skills`, `mcpServers`, `hooks` (object có `PreToolUse|PostToolUse|Stop|SessionStart` keys), `mcpServers`, `dangerouslyDisableSandbox` (anti-pattern: should reject), `extendedThinking`, `dedicatedThread`, `disableOutputSandbox` — và mọi field còn lại 보 feminist trong Claude Code current specs.
- Per-field: required/optional, type, validation rule, example value
- Quy tắc interaction: `permissionMode: bypassPermissions` luôn bị safety-auditor reject
- Tools deny default: `Bash`, `WebFetch`, `NotebookEdit` chỉ cho phép nếu justification trong `<acceptance_criteria>`
- YAML parse test snippet: `python3 -c "import yaml; yaml.safe_load(open(...))"`

### D1-2: `capability_controls.md` — Tool/MCP/Skills Scoping

Định nghĩa cách agent được scope:

- **Tool allowlist**: chỉ tối đa 8 tools per agent, default `Read` + domain-specific (e.g., code-reviewer chỉ thêm `Edit`)
- **PermissionMode**:
  - `default` — hỏi user cho mỗi filter action
  - `acceptEdits` — auto-accept Edit tool calls (cần khóa write path bằng PreToolUse hook)
  - `bypassPermissions` — **REJECTED** bởi safety-auditor
  - `plan` — read-only mode, không trigger edit tools
- **MCP scoping**: mcpServers phải là registered server (lookup trong `mcp_registry.json` nếu có). Mỗi MCP tool phải có justification trong agent's purpose
- **Skills preload**: danh sách skill names (theo skills-registry.json), tối đa 3 skills per agent
- **Memory hooks**: không standalone — memory quản lý thông qua OMC state ledger `.claude/skills/.omc/state/`, agent chỉ record/emit bằng tool `Write` gated bởi hook
- Anti-patterns table: dangerous combinations (e.g., `Bash` + `bypassPermissions` = risk)

### D1-3: `examples.md` — 4 Reference Patterns

Phải cung cấp 4 reference agent patterns để subagent-forge dùng làm template:

1. **code-reviewer pattern** — Read-only, `model: inherit`, format feedback by priority (Critical/Warnings/Suggestions). Tools: `[Read, Glob, Grep]`. Use case: read-only analyst.
2. **debugger pattern** — Edit access, root-cause analysis with evidence. Tools: `[Read, Edit, Bash, Grep]`. Use case: diagnostic-and-fix. Boot pattern: print hypothesis → test → fix → re-verify.
3. **data-scientist pattern** — Sonnet model fixed, SQL/BigQuery focus. Tools: `[Read, Bash, Grep, Task]`. Use case: analytical trên data sources.
4. **db-reader pattern** — Bash access gated by PreToolUse hook blocking write SQL. Tools: `[Read, Bash]`. PreToolUse hook script: parse `.tool_input.command` reject cualquier `INSERT|UPDATE|DELETE|DROP|TRUNCATE`.

Mỗi pattern phải có:
- Frontmatter complete example
- System prompt excerpt (≥ 30 dòng real-world)
- Hook script (nếu có)
- Files referenced via clickable links tới thư mục khác trong workspace

### D1-4: `forks.md` — Experimental Fork Semantics

Document cơ chế "fork" cho agent experimentation:

- Khi nào fork — experimental agent variant
- Naming convention: `<parent-name>--<fork-suffix>` (e.g., `code-reviewer--strict-mode`)
- Fork không overwrite parent; sống song song
- Lifecycle: experiment → evaluated → promote (rename to parent) OR archive
- Risk anti-pattern: overload `description` để "shadow fork" (thân description khác mà cùng tools)
- Explicit warning: "DO NOT use fork unless explicitly requested"

### D1-5: `hooks_and_events.md` — Hook Protocol Specification

Document chuẩn hook protocol:

- **Event types** (canonical Claude Code supported events):
  - `PreToolUse` — fires trước khi tool call execute. Input: JSON `{tool_name, tool_input}` via stdin. Exit 0 = allow, exit 2 = block (stderr=");
  - `PostToolUse` — fires sau khi tool call execute, trước output show to user. Input: JSON `{tool_name, tool_input, tool_output}`. Exit 0 là allow output, exit 2 là hide output (rarely used).
  - `Stop` — fires khi user Ctrl-C hoặc session stop. Input: JSON `{stop_hook_active}`. Exit 0 = allow stop, exit 2 = block stop (warn user).
  - `SessionStart` — fires khi session mới boots. Input: JSON `{cwd, pid, boot_id, session_id}`. Exit 0 = allow boot.
- **Shell script conventions**:
  - `INPUT=$(cat)` — read stdin
  - `jq -r '.tool_input.<field>'` — extract field
  - `>&2` — error messages to stderr
  - utmost: scripts phải idempotent, ≤ 50 dòng, không dùng `write` side-effect (chỉ `read` + `verify`)
- **Permission contract**:
  - Hooks được placed giới hạn write to `.role/` và `.skill-context/_state-archive/` (cho audit log); cần justification để write anywhere else
- **Inline vs standalone**:
  - Inline hook trong agent frontmatter (current subagent-forge pattern) — script nhúng YAML frontmatter
  - Standalone hook tại `.claude/hooks/events/<hook_name>.sh` — được reference trong registry.yaml
  - Khi nào dùng cái nào: inline cho agent-specific gates; standalone cho cross-cutting/triggers

### D1-6: `workflow_patterns.md` — Invocation, Foreground/Background, Resume

Document các workflow patterns:

1. **Foreground invocation** — `subagent_type: <name>` trong Task call, parent waits to completion
2. **Background invocation** — spawn many parallel, parent không wait, results polled sau
3. **Resume pattern** — `task_id: ses_<id>` continuation — same agent instance giữ context; dùng cho multi-turn conversation
4. **Compaction pattern** — agent's context window full → spawn child `general-purpose` với summarization, parent truncates lịch sử
5. **Cascading agents** — agent A invoke agent B (limit depth ≤ 2; recursion protection enforced bởi hook như subagent-forge's matcher)
6. **Cross-runtime invocation** — Claude Code agent gọi Codex/Hermes thông qua CLI executor (costly, rarely done)

Mỗi pattern có:
- Khi nào dùng
- Code example với Task call syntax
- Exit/error handling
- Cost estimates (token call count)

### D1-7: `xml_tags_standards.yaml` — 9-Tag Whitelist

YAML spec định nghĩa 9 XML tags whitelist cho system prompt:

```yaml
canonical_xml_tags:
  - tag: instructions
    usage: "Điều khiển hành vi agent — non-negotiable rules"
    placement: "Đầu system prompt, trước workflow phases"
    required_attribute: priority (normal|critical)
    allow_nested: false
  
  - tag: context
    usage: "Dữ liệu tham chiếu, không phải lệnh"
    allow_nested: false
  
  - tag: examples
    usage: "Ví dụ minh họa pattern đúng"
  
  - tag: input
    usage: "Thông tin người dùng / tài liệu nguồn"
  
  - tag: output_contract
    usage: "Định dạng đầu ra bắt buộc"
  
  - tag: retrieved_docs
    usage: "Reference tới knowledge docs (absolute paths)"
    required_attribute: "list format"
  
  - tag: task
    usage: "Default task definition"
  
  - tag: constraints
    usage: "must/must_not rules"
    sub_tags: [must, must_not]
  
  - tag: acceptance_criteria
    usage: "Criteria nghiệm thu output"
```

Mỗi tag phải có:
- `usage` description
- `placement` (where in prompt)
- `required_attribute` (if any)
- `sub_tags` (if nested allowed)
- Anti-pattern: tag out of whitelist = quality-reviewer auto-fail

---

## Verification checklist (cơ học)

### AC-1 — Path resolution
```bash
for doc in configuration.md capability_controls.md examples.md forks.md hooks_and_events.md workflow_patterns.md xml_tags_standards.yaml; do
  test -f .claude/knowledge/agents/$doc || exit 1
  # File size check (≥ 2KB = substantial content)
  test $(wc -c < .claude/knowledge/agents/$doc) -ge 2000 || exit 2
done
echo "AC-1 PASS"
```

### AC-2 — Frontmatter hợp lệ
```bash
python3 << 'EOF'
import yaml, os
docs = ['configuration.md', 'capability_controls.md', 'examples.md', 'forks.md', 'hooks_and_events.md', 'workflow_patterns.md', 'xml_tags_standards.yaml']
for d in docs:
    p = f'.claude/knowledge/agents/{d}'
    with open(p) as f:
        content = f.read()
    fm = content.split('---')[1] if content.startswith('---') else ''
    data = yaml.safe_load(fm)
    assert 'name' in data, f"{d} missing name"
    assert 'version' in data, f"{d} missing version"
    assert 'status' in data, f"{d} missing status"
    assert data['status'] == 'canonical', f"{d} status != canonical"
print("AC-2 PASS")
EOF
```

### AC-3 — Zero placeholders
```bash
grep -rn "\(TODO\|FIXME\|mock()\|pass # implement\)" .claude/knowledge/agents/ && exit 1 || echo "AC-3 PASS"
```

### AC-4 — Internal cross-links valid
```bash
python3 << 'EOF'
import re, os
docs = os.listdir('.claude/knowledge/agents/')
for d in docs:
    p = f'.claude/knowledge/agents/{d}'
    with open(p) as f:
        c = f.read()
    # Find file:/// links
    for m in re.finditer(r'\]\(file:///([^\)]+)\)', c):
        target = m.group(1)
        if not os.path.exists(target):
            print(f"BROKEN LINK in {d}: {target}")
            exit(1)
print("AC-4 PASS")
EOF
```

### AC-5 — Subagent-forge reads docs without invocation failure
```bash
# Simulate subagent-forge boot — check that 7 docs path found:
for doc in configuration.md capability_controls.md examples.md forks.md hooks_and_events.md workflow_patterns.md xml_tags_standards.yaml; do
  test -r .claude/knowledge/agents/$doc || exit 1
done
# Verify subagent-forge.md references resolve
grep -E "^- \`\.claude/knowledge/agents/${doc}\`" .claude/agents/subagent-forge.md > /dev/null
echo "AC-5 PASS"
```

### AC-6 — Examples conformance (Phase 3 sẽ use)
```bash
# Verify examples.md chứa 4 reference patterns vớifrontmatter complete:
grep -c "^## " .claude/knowledge/agents/examples.md | grep -E "^[1-9]" || \
  grep -E "^### " .claude/knowledge/agents/examples.md | wc -l | awk '$1 >= 4 { exit 0 } END { exit 1 }'
echo "AC-6 PASS"
```

### AC-7 — Hook protocol extractable
```bash
# hooks_and_events.md must define PreToolUse + PostToolUse + Stop + SessionStart
for ev in PreToolUse PostToolUse Stop SessionStart; do
  grep -q "$ev" .claude/knowledge/agents/hooks_and_events.md || exit 1
done
echo "AC-7 PASS"
```

---

## Step-by-step task list

1. **Read reference material** — đọc standards.md §3, subagent-forge.md full, architecture.md §1-2, Temps/spec/architects/shared/glossary.md. Note key contracts.

2. **Author `configuration.md`** — 16 fields spec, với bảng per-field details, YAML parse test snippet. Goal ~150-200 dòng. → commit `phase-1: configuration schema canonical doc`

3. **Author `capability_controls.md`** — tool/MCP/skills scoping, anti-patterns. ~120-150 dòng. → commit `phase-1: capability controls doc`

4. **Author `examples.md`** — 4 reference patterns, mỗi pattern ≥ 30 dòng, full frontmatter + system prompt excerpt. ~400-500 dòng total. → commit `phase-1: examples reference patterns`

5. **Author `forks.md`** — experimental fork semantics. ~80-100 dòng. → commit `phase-1: fork semantics doc`

6. **Author `hooks_and_events.md`** — Protocol spec với 4 event types, shell conventions, prefix vs standalone guidance. ~150-200 dòng. → commit `phase-1: hook protocol spec`

7. **Author `workflow_patterns.md`** — 6 workflow patterns với code examples. ~120-150 dòng. → commit `phase-1: workflow patterns doc`

8. **Author `xml_tags_standards.yaml`** — 9 tag whitelist YAML spec. ~80-100 dòng. → commit `phase-1: xml tags whitelist`

9. **Run full AC-1 đến AC-7** sequentially. Fix any FAIL. → commit `phase-1: acceptance criteria pass`

10. **Update `.claude/knowledge/agents/README.md`** (creating new if not exist) — master knowledge navigation map for subagent-forge consumption. → commit `phase-1: knowledge registry README`

---

## Definition of done (Phase 1)

```yaml
dod:
  - All 7 docs tồn tại với status: canonical
  - All 7 AC PASS
  - 7 docs total ≥ 1100 dòng content
  - subagent-forge.md <retrieved_docs> section giờ reference 7 files đều tồn tại
  - Mỗi doc có ≥ 1 cross-link tới workspace file (clickable file:/path/)
  - Zero placeholder strings anywhere
```

---

## Liên kết

- [Roadmap Index](index.md)
- [Phase 0 trước](00-foundation-bootstrap.md)
- [Phase 2 tiếp theo](02-hook-framework.md)
- [Reference: subagent-forge.md `retrieved_docs` section](file:///home/stveve/Documents/workspace/build-workflow/WASHVN/.claude/agents/subagent-forge.md#L73-L82)
- [Standards](file:///home/stveve/Documents/workspace/build-workflow/WASHVN/standards.md)