# Karpathy-Inspired Coding and Documentation Standards

## 1. Introduction
This document defines the high-fidelity coding and documentation guidelines (L1 working policy) for the WASHVN Master Skill Suite. These principles are heavily inspired by safe, intent-focused engineering patterns, designed to minimize LLM drift and maximize execution confidence.

---

## 2. Behavioral Coding Principles

### 2.1 Think Before Coding
- **Never assume or bypass confusion.** If requirements are ambiguous, clarify them immediately.
- Explicitly state architectural assumptions, trade-offs, and dependency maps before modifying code.
- If multiple technical approaches exist, present them to the developer first rather than silently choosing.

### 2.2 Simplicity First
- **Implement the minimum code necessary** to solve the problem. Speculative features, unused abstractions, or over-configurability are strictly forbidden.
- Avoid code bloat. If 10 lines of code can solve the problem as safely as 50 lines, rewrite and simplify.
- Ask: "Would a senior developer find this design over-engineered?" If yes, reduce the complexity footprint.

### 2.3 Surgical Changes
- **Keep changes highly scoped.** Touch only the files and lines that directly address the target issue or feature.
- Avoid refactoring adjacent code, formatting unrelated blocks, or altering existing comments unless explicitly requested.
- Maintain consistency with the surrounding codebase style, conventions, and formatting, even if you prefer a different layout.
- Remove all unused variables, dead imports, or functions introduced by your changes.

### 2.4 Goal-Driven Execution
- **Define clear, reproducible verification criteria** before executing the task.
- Build incremental verification steps (e.g. running unit tests or validation scripts) at each stage of development.
- Maintain a feedback loop: write tests, observe failures, fix, and confirm pass state.

---

## 3. Strict Code Quality Gates

### 3.1 Zero-Placeholder Policy
- **Absolutely no placeholders.** Comments such as `// TODO`, `pass`, `mock()`, or stub functions are forbidden in final deliverables.
- If a section of code is not yet implementable, halt execution, document the blocker, and request assistance.

### 3.2 Error-Boundary Enforcement
- **Every functional script must specify clear entry/exit criteria.**
- Explicitly define error boundaries, expected exceptions, and non-zero exit codes.
- Use robust YAML resilience layers to wrap configuration loads and parsing tasks.

---

## 4. Documentation Standards (LLM Activation Protocol)

### 4.1 Hybrid Formatting
- **Markdown**: Use primarily for natural language explanations, system architectures, overview sections, and conceptual walk-throughs.
- **YAML**: Use strictly for structured data, rules, policies, constraints, checklists, and I/O contracts.
- **XML-like Tags**: Use to establish hard semantic boundaries (e.g. `<instructions>`, `<context>`, `<examples>`) to prevent model instruction leakage.

### 4.2 Clickable File Links
- Always provide fully-resolved, clickable file links using the scheme: `[filename](file:///absolute/path/to/file)`.
- For line-specific references, append `#L123-L145`.
- **CRITICAL**: Never wrap the visible link label in backticks (e.g. `[`main.py`](file://...)` is broken). Always use plain text: `[main.py](file://...)`.

### 4.3 GitHub-style Alerts
- Emphasize critical context and rules using standard alerts:
  > [!NOTE]
  > Background context or implementation details.
  > [!IMPORTANT]
  > Essential requirements or constraints that must be followed.
  > [!WARNING]
  > Potential breaking changes or side effects.

### 4.4 Mermaid Diagrams
- Use Mermaid diagrams to visualize states, dependency paths, and sequence steps.
- Ensure all node labels with special characters are quoted, and avoid HTML tags inside labels to prevent render failures.

---

## 5. Knowledge Isolation Policy

### 5.1 Multi-Layer Architecture
Tri thức được chia làm 4 lớp để tối ưu hóa token budget và tránh quá tải bối cảnh:
1. **L0 Anchor Rules**: Hiến pháp cốt lõi, giới hạn cứng, anti-goals. Luôn luôn nạp.
2. **L1 Working Policy**: Quy ước lập trình, hướng dẫn style, các quality gates (tài liệu này). Nạp theo phạm vi task.
3. **L2 Domain Context**: Thuật ngữ nghiệp vụ, luồng dữ liệu kiến trúc, sơ đồ thực thể. Nạp khi cần hiểu chi tiết.
4. **L3 Evidence & Examples**: Bản vẽ kỹ thuật, log lỗi, test fixtures, spec của task. Chỉ nạp trong session tương ứng.

### 5.2 Token Budget Limits
- **L0 Anchor**: ≤ 700 tokens.
- **L1 Working Policy**: 400 - 1200 tokens.
- **L2 Domain**: 600 - 2500 tokens.
- **L3 Evidence**: 300 - 2000 tokens.
- **Section size**: If any markdown section exceeds 900 tokens, extract details to L2/L3 files.
