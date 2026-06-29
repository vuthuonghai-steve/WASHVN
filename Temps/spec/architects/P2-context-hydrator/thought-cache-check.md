# Thought-Cache Check (HYD-4)

> Role: **Hydrator** | Domain: **Quality** | Design: **Fallback**
> Source: `architecture-design.md §4.A` (clean/)

## Requirement

Hydrator MUST verify `thought-cache.yaml` exists and is valid on Context Bus before proceeding.

## Schema

```yaml
reflection_cache:
  business_thought_process: []    # thought blocks >200 tokens (META-2.1)
  stakeholder_empathy: []          # role goals + pain points
  reverse_questions: []            # 4-aspect probing (META-2.2)
  defensive_reasoning: []          # edge cases + mitigation
  semantic_anchors: {}             # domain anchor table
```

## Verification gates

| Gate | Check | Fail action |
|:---|:---|:---|
| HYD-4.0 | Depth Cache Presence | Check file exists |
| HYD-4.1 | thought-cache.yaml exists | Trigger F18 |
| HYD-4.2 | thought-cache.yaml not empty | Trigger F18 |

## Fallback F18

If thought-cache missing or empty:
1. Hydrator **stops immediately** — no resources wasted on Planner
2. Trigger **F18**: back to Stage 0 (BA Elicitor Depth Recovery)
3. BA Elicitor regenerates thought-cache with META-2.1 + empathy + reverse Q + defensive reasoning
4. Pipeline iterates

## Related fallbacks

- F16: thought-cache missing `business_thought_process` → Stage 0 re-do
- F17: thought-cache missing `stakeholder_empathy` or `reverse_questions` → Stage 0 re-do
