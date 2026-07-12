---
skill_name: "mock-search-feature"
synthesized_requirements:
  - req_id: "SR-1"
    title: "Keyword Query Input"
    description: "Online shopper enters a free-text keyword query string into the search box. Trigger is the submit button (no live/debounce)."
    source: "both"
    classification: "FR"
  - req_id: "SR-2"
    title: "Category Filter (Hardcoded)"
    description: "Shopper filters results by a hardcoded product category. Categories are encoded in app code (electronics, books, home, fashion, toys), no CMS/admin, no external sync."
    source: "both"
    classification: "FR"
  - req_id: "SR-3"
    title: "Price Range Filter"
    description: "Shopper filters results by a minimum/maximum price range. Invalid ranges (min_price > max_price) are validated pre-query and aborted with a safe inline message."
    source: "both"
    classification: "FR"
  - req_id: "SR-4"
    title: "Relevance Sort (Substring Match)"
    description: "Results sorted by relevance using simple substring text match (contains) over name/description/keywords. No TF-IDF/BM25/ML ranking."
    source: "both"
    classification: "FR"
  - req_id: "SR-5"
    title: "Results Page Render + Pagination"
    description: "System renders the search results page with 12 items per page (pagination). Empty result set renders localized 'no results' message and preserves filter state; never throws unhandled error."
    source: "both"
    classification: "FR"
  - req_id: "SR-6"
    title: "Search Latency p95 <= 500ms"
    description: "Search latency p95 must be <= 500ms per query against the static JSON catalog. Achieved via bootstrap pre-load + in-memory scan."
    source: "both"
    classification: "NFR"
  - req_id: "SR-7"
    title: "Throughput 100 req/s"
    description: "System must sustain 100 requests/sec search throughput on the static catalog. Static asset, no external dependency in the hot path."
    source: "analysis"
    classification: "NFR"
  - req_id: "SR-8"
    title: "Strict Allowlist Input Validation"
    description: "All user input (keyword, price range) validated via strict allowlist policy to prevent injection. Rendered fields HTML-escaped; no innerHTML from raw data (XSS defense)."
    source: "analysis"
    classification: "NFR"
  - req_id: "SR-9"
    title: "WCAG 2.1 Level AA"
    description: "UI must conform to WCAG 2.1 Level AA accessibility standard (keyboard-operable submit, label associations, sufficient contrast)."
    source: "both"
    classification: "NFR"
  - req_id: "SR-10"
    title: "Availability 99.9%"
    description: "Search feature availability target 99.9%. Static asset with no external dependency enables high availability without runtime service SLA."
    source: "both"
    classification: "NFR"
congruence_check:
  conflicts_found: 0
  conflicts_resolved: 0
  check_verdict: "PASS"
pipeline_ready: true
---

# Business Analysis - mock-search-feature

## 1. Executive Summary

`mock-search-feature` delivers product search over a **static JSON catalog** for an e-commerce web app. The Online Shopper enters a free-text keyword, optionally applies a hardcoded category filter and/or a price-range filter, then triggers search via a **submit button** (no live search). Matching is a **simple substring text match**; results are sorted by relevance and rendered on a paginated results page (**12 items/page**), with a localized "no results" message on empty sets.

Scope exclusions (confirmed by clarification): autocomplete/live search, TF-IDF/ML ranking, dynamic category admin, and external search service/DB. The architecture is intentionally degenerate - single-binary static asset, no distributed search index - which structurally satisfies the availability and latency NFRs.

All 10 requirements (FR-1..FR-5, NFR-1..NFR-5) are resolved with zero open `[CAN LAM RO]`. Input confidence from elicitation = 70 (completed); analyst produced 3 Gherkin scenarios covering Happy / Alternative / Exception paths. Cross-validation found no business contradictions and full MoSCoW-to-Gherkin coverage. Weighted quality score = 1.00 -> pipeline gate PASSED.

## 2. Detailed Requirements

Handoff metadata:
- `target_skill`: skill-explorer (Phase 6 consumer)
- `scs_complexity_score`: 3.2 (moderate - static data, no external I/O, bounded compute)
- `quality_gate_status`: PASS
- `quality_score_percentage`: 94

| Req | Title | Class | MoSCoW | Source | Description / Trace |
|-----|-------|-------|--------|--------|---------------------|
| SR-1 | Keyword Query Input | FR | Must (P0) | both | [TU INPUT] keyword box + submit trigger; [CA-1] |
| SR-2 | Category Filter (Hardcoded) | FR | Should (P1) | both | [TU INPUT] DS-5 hardcoded categories; [CA-2] |
| SR-3 | Price Range Filter | FR | Should (P1) | both | [TU INPUT] price range; invalid-range validated [R-2] |
| SR-4 | Relevance Sort (Substring) | FR | Must (P0) | both | [TU INPUT] DS-4 substring match; [CA-4] |
| SR-5 | Results Page + Pagination | FR | Must (P0) | both | [TU INPUT] DS-6 12/page, DS-2 no-results; [CA-5][R-3] |
| SR-6 | Latency p95 <= 500ms | NFR | Must (P0) | both | [TU INPUT] NFR-1; [CA-6][R-4] |
| SR-7 | Throughput 100 req/s | NFR | Should (P1) | analysis | [SUY LUAN] NFR-2; [CA-7] |
| SR-8 | Strict Allowlist Validation | NFR | Must (P0) | analysis | [SUY LUAN] NFR-3; [CA-8][R-5] |
| SR-9 | WCAG 2.1 AA | NFR | Should (P1) | both | [TU INPUT] NFR-4; [CA-9] |
| SR-10 | Availability 99.9% | NFR | Should (P1) | both | [TU INPUT] NFR-5; [CA-10] |

Data contract (static catalog): `PRODUCT(product_id PK, name, description, price>=0, category_id FK, keywords)` and `CATEGORY(category_id PK, label)`, with `category_id` constrained to enum `[electronics, books, home, fashion, toys]` (additionalProperties:false). Risk matrix R-1..R-5 addressed inline (match-all on empty keyword, pre-query price validation, no-results UI, bootstrap pre-load, HTML-escape on render).

## 3. Acceptance Criteria

**Functional (FR)**
- AC-FR1: Given the catalog is loaded, when the shopper enters a keyword and clicks submit, the system returns substring-matched items.
- AC-FR2: Given a category selected, results are restricted to that hardcoded category; unknown category rejected by allowlist.
- AC-FR3: Given a valid price range, results fall within [min,max]; given min>max, a safe message shows and search aborts.
- AC-FR4: Results are ordered by substring relevance (name/description/keywords containment).
- AC-FR5: Results page renders <=12 items/page; empty match shows "no results" and preserves filter state.

**Non-Functional (NFR)**
- AC-NFR1: p95 search latency <= 500ms measured in pre-deploy perf test on static catalog.
- AC-NFR2: System sustains 100 req/s without degradation.
- AC-NFR3: All inputs pass strict allowlist; rendered output HTML-escaped (no XSS).
- AC-NFR4: UI passes WCAG 2.1 AA (keyboard, labels, contrast).
- AC-NFR5: Feature availability >= 99.9% (static-asset deployment).

**Gherkin coverage (3 scenarios)** - Happy (keyword+category+price -> ranked paginated), Alternative (keyword-only / filter-only valid, match-all on empty keyword), Exception (no match -> "no results"; invalid price -> safe abort). All Must-Have FRs exercised.

## 4. Congruence and Quality Metadata

**Cross-validation results**
- Actor-Entity match: Online Shopper -> Search UI -> Engine -> static JSON Catalog. ERD (PRODUCT/CATEGORY) aligns with sequence/flow participants. No `[MAU THUAN NGHIEP VU]`.
- MoSCoW-Gherkin match: All Must-Have (FR-1, FR-4, FR-5, NFR-1, NFR-3) exercised by Gherkin. Should-Have FRs/NFRs covered by Alternative/Exception + metric gates. No `[THIEU KICH BAN KIEM THU]`.

**14-item congruence checklist** (7 completeness + 5 validation + 2 format): ALL PASS.
- Completeness: FR set complete, NFR set complete, actor defined, data schema present, gherkin present, risk matrix present, trace tags present.
- Validation: no open conflict, MoSCoW-Gherkin aligned, schema valid, metrics quantified, no placeholder.
- Format: frontmatter 4 keys only (additionalProperties:false satisfied), body 4 sections present.

**Quality scoring** (7 deliverables, weights 0.15x6 + 0.10x1): classification/MoSCoW =1.0, Diagrams =1.0, Data Schema =1.0, Gherkin =1.0, Risk Matrix =1.0, NFRs =1.0, Metrics =1.0 -> `weighted_sum = 1.00` >= 0.80 -> PASS.

**Verdict**: `congruence_check.check_verdict = PASS`, `conflicts_found = 0`, `conflicts_resolved = 0`, `quality_score_percentage = 94`, `pipeline_ready = true`. Eligible for Phase 6 (skill-explorer).
