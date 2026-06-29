# Token Budget Soft Gate + REV-3.0 Refactor

> Role: **Reviewer** | Domain: **Quality** | Design: **Quality**
> Source: `skill-migration-spec.md §13.7`, `architecture-design.md §S3.5` (clean/)

## Problem

Hard-enforcing token budget (e.g., SKILL.md ≤ 700 tokens) can destroy business context and cause hallucination.

## Solution

Token budget becomes a **Soft Gate** (Warning, not Hard Halt):

| Gate | Type | On violation |
|:---|:---|:---|
| BUILD-2.1 | Placeholder Density | Warning → logged in build-log.md |
| BUILD-3.1 | Token Budget ≤ 700 | Warning → logged in build-log.md |

## REV-3.0 Refactor Trigger

When `build-log.md` records soft gate warnings:

1. **Code Reviewer** (Stage 3.5) auto-detects warnings
2. Activates **Refactor subagent** to:
   - Clean placeholder/mock code → real implementation
   - Extract verbose sections from `SKILL.md` into `knowledge/` directory
   - Restructure to meet token budget WITHOUT losing business context
3. Refactored skill sent to Sandbox

## Why soft gate

- Prevents LLM hallucination from aggressive truncation
- Preserves unique business logic that happens to exceed token limit
- Auto-refactor is cleaner than force-truncation
- Still produces compliant output (through refactoring, not deletion)
