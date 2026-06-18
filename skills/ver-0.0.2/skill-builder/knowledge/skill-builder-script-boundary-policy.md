# Script Boundary Policy — skill-builder (Builder Scripts vs Target Skill Scripts)
# [TỪ DESIGN §2.5 + §3 knowledge/skill-builder-script-boundary-policy.md (NEW, KG-2, P1)]
# [TỪ BA §6 KG-2, FR-17, FR-18, HANDBOOK §7.4, §10.3 §10.3.1]
# [TỪ sibling: skills/ver-0.0.2/skill-architect/knowledge/script-boundary-policy.md]

> **Usage**: Load tại Phase 3 §3 Zone Mapping khi thiết kế `scripts/` zone của TARGET skill. Phân biệt rõ scripts của skill-builder (deterministic IO) vs scripts của target skill (cũng phải deterministic).

---

## 1. Vấn đề

Khi Builder tạo skill mới, có nguy cơ nhúng **high-level cognitive logic** vào Python scripts dưới `scripts/` zone. Điều này vi phạm **Cognitive Agentic Skill Paradigm** (SKILL.md §must line 21-22): scripts phải là system primitives, không phải cognitive reasoning.

## 2. Quy tắc phân chia

### 2.1 `scripts/` zone của TARGET skill CHỈ ĐƯỢC làm

| Loại operation | Ví dụ | Status |
|----------------|-------|--------|
| **I/O operations** | `open()`, `read()`, `write()`, `os.path.*`, `os.walk()` | ✅ Allowed |
| **Parse structured data** | `yaml.safe_load()`, `json.load()`, `re.findall()`, markdown parser | ✅ Allowed |
| **Count placeholders** | count of `[MISSING_DOMAIN_DATA]` markers | ✅ Allowed |
| **Compute line ratios** | `len(source) / len(target)` cho fidelity check | ✅ Allowed |
| **Run CLI subcommands** | `subprocess.run(['cli-cmd', '--flag'])` no LLM calls | ✅ Allowed |
| **SHA256/entropy computation** | `hashlib.sha256()`, `random.SystemRandom()` | ✅ Allowed |
| **API wrappers (no LLM)** | HTTP client to REST API, gRPC stubs | ✅ Allowed |
| **Math operations** | statistics, ratios, percentages | ✅ Allowed |

### 2.2 `scripts/` zone của TARGET skill KHÔNG ĐƯỢC làm

| Loại operation | Ví dụ | Status |
|----------------|-------|--------|
| **Generate prompt templates** | `f"Translate this: {text}"` cho LLM call | ❌ Forbidden |
| **Make zone/file decisions** | `if complexity > 5: create_policy_yaml()` | ❌ Forbidden (caller's job) |
| **Embed business logic** | conditional branching dựa trên domain rules | ❌ Forbidden |
| **Call LLM API** | `openai.ChatCompletion.create()`, `anthropic.messages.create()` | ❌ Forbidden |
| **Generate content from scratch** | write markdown prose từ prompt template | ❌ Forbidden |
| **Domain-specific decisions** | "Should we use Stripe or Braintree for payment?" | ❌ Forbidden |

## 3. Lý do

1. **Separation of concerns**: AI agent (caller) làm high-level decisions, scripts chỉ làm IO primitives
2. **Testability**: Pure IO scripts dễ test hơn scripts có embedded logic
3. **Reusability**: Scripts không phụ thuộc vào specific skill context
4. **Determinism**: IO primitives deterministic, logic scripts có thể không
5. **Token efficiency**: Logic trong scripts không được load vào LLM context, giảm token overhead

## 4. Ví dụ

### ✅ ĐÚNG (scripts/validate_skill.py của skill-builder)

```python
def check_placeholder_density(skill_path: str) -> int:
    """Count [MISSING_DOMAIN_DATA] markers across all .md files."""
    count = 0
    for root, _, files in os.walk(skill_path):
        for file in files:
            if file.endswith('.md'):
                path = os.path.join(root, file)
                with open(path, 'r', encoding='utf-8') as f:
                    count += f.read().count("[MISSING_DOMAIN_DATA]")
    return count
```

→ Pure IO + count operation. No decision-making.

### ❌ SAI (cognitive logic embedded in script)

```python
def should_create_policy_file(complexity_score: int) -> bool:
    """Decide whether to create policy/ based on complexity."""
    if complexity_score > 5:
        return True
    elif complexity_score > 3 and has_many_phases():
        return True
    return False
```

→ Business logic decision. Caller (AI agent) should make this decision based on design.md §3, not script.

## 5. Enforcement

### 5.1 Static checks (in `scripts/validate_skill.py`)

| Check | Rule | Severity |
|-------|------|----------|
| Import check | No `import openai`, `import anthropic`, `import langchain.*` | MUST |
| Function naming | Functions should be `_check_*`, `_count_*`, `_parse_*` — not `_decide_*`, `_should_*` | SHOULD |
| LLM API detection | grep for `Completion.create(`, `messages.create(`, `chat.completions` | MUST |
| Return type | Functions return data structures, not `True/False` decisions | SHOULD |

### 5.2 Runtime contract

If a script MUST make a decision, it should expose it as data:

```python
# ❌ SAI: Script makes decision
def recommend_token_split(token_count: int) -> bool:
    return token_count > 700

# ✅ ĐÚNG: Script provides data, caller decides
def measure_token_count(skill_path: str) -> int:
    # ... return token_count
    return token_count
# Caller: if token_count > 700: split_to_policy()
```

## 6. Exception: `scripts/orchestrate.py` for Meta-Skills

`scripts/orchestrate.py` for meta-skills (per `policy/skill-builder.yaml` §must line 24) is an exception — it MAY contain orchestration logic for sub-skills using SSP (State & Signal Protocol). However:
- Orchestration logic = IO + state passing, NOT domain decisions
- Sub-skill selection = data-driven (from registry), NOT script-decided
- LLM calls are still forbidden

## 7. Migration from v0.0.2

| Aspect | v0.0.2 | v0.0.3 |
|--------|--------|--------|
| Boundary enforcement | Implicit (must line 32-33) | Explicit policy file |
| Static check | None | Grep for LLM imports |
| Test fixtures | None | `tests/script-boundary.test.py` (planned) |
| Documentation | SKILL.md body (mixed) | This file (L2 knowledge) |
