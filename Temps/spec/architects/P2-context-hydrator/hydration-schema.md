# Hydration Schema

> Role: **Hydrator** | Domain: **Data** | Design: **Contract**
> Source: `architecture-design.md §S1.7` (clean/)

## Purpose

Hydrator reads all artifacts from Context Bus (L0-L2) and produces a condensed context package. Planner reads ONLY this package — not the original files.

## Input

- `business-analysis.md`
- `domain-handbook.md`
- `design.md`
- `quality-matrix.yaml`
- `thought-cache.yaml` (check existence only)

## Output: `hydrated-context.yaml`

```yaml
hydrated_context:
  domain: "Fintech / Payment Gateways"
  glossary: ["OTP", "Nonce", "HMAC-SHA256", "Replay Attack", ...]
  nfr_metrics:
    - {name: "Latency", value: "< 200ms"}
    - {name: "Rate Limit", value: "3 attempts / 5 min"}
  data_contracts:
    - contract_id: "CONTRACT-OTP-001"
      input_schema: {phone_number: "string E.164", ...}
      output_schema: {status: "APPROVED|REJECTED|BLOCKED", ...}
  zone_map: "design.md §3"
  must_not: ["Không log plain text OTP", "Không dùng Math.random()"]
  edge_cases: ["Expired OTP", "Brute-force", "Session hijacking"]
```

## Processing rules

- Strip prose — keep only semantic anchors
- Glossary must have ≥10 terms (F6 trigger if less)
- Data contracts must reference existing zone mappings
- NFR must be quantified with metrics

## Quality gates: HYD-1→3

| Gate | Check |
|:---|:---|
| HYD-1.0 | Glossary hydrated with ≥10 terms |
| HYD-2.0 | NFR hydrated with metrics |
| HYD-3.0 | Contracts hydrated from design.md |
