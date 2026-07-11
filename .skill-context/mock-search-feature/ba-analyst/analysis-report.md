---
skill_name: "mock-search-feature"
criteria_analysis:
  - criterion_id: "CA-1"
    description: "FR-1: Online shopper enters a free-text keyword query string into the search box."
    classification: "FR"
  - criterion_id: "CA-2"
    description: "FR-2: Shopper filters results by a hardcoded product category."
    classification: "FR"
  - criterion_id: "CA-3"
    description: "FR-3: Shopper filters results by a minimum/maximum price range."
    classification: "FR"
  - criterion_id: "CA-4"
    description: "FR-4: Results sorted by relevance using simple substring text match (no TF-IDF/ML)."
    classification: "FR"
  - criterion_id: "CA-5"
    description: "FR-5: System renders the search results page with 12 items per page (pagination)."
    classification: "FR"
  - criterion_id: "CA-6"
    description: "NFR-1: Search latency p95 must be <= 500ms per query against the static JSON catalog."
    classification: "NFR"
  - criterion_id: "CA-7"
    description: "NFR-2: System must sustain 100 requests/sec search throughput on the static catalog."
    classification: "NFR"
  - criterion_id: "CA-8"
    description: "NFR-3: All user input (keyword, price range) validated via strict allowlist policy to prevent injection."
    classification: "NFR"
  - criterion_id: "CA-9"
    description: "NFR-4: UI must conform to WCAG 2.1 Level AA accessibility standard."
    classification: "NFR"
  - criterion_id: "CA-10"
    description: "NFR-5: Search feature availability target 99.9% (static asset, no external dependency)."
    classification: "NFR"
risk_assessment:
  - risk_id: "R-1"
    edge_case: "Shopper submits empty keyword with filters applied - could match entire catalog or nothing."
    mitigation: "Treat empty keyword as match-all; apply category/price filters only; cap result scan to full catalog (bounded by static size)."
  - risk_id: "R-2"
    edge_case: "Invalid price range where min_price > max_price submitted via manual input."
    mitigation: "Validate min<=max before query; on failure render safe inline message and abort search, no crash."
  - risk_id: "R-3"
    edge_case: "No catalog item matches query+filters - empty result set."
    mitigation: "Render localized 'no results' message; preserve filter state so shopper can adjust; never throw unhandled error."
  - risk_id: "R-4"
    edge_case: "Large static JSON catalog load exceeds p95 500ms on slow clients."
    mitigation: "Pre-load and parse JSON at app bootstrap; in-memory filter scan; measure p95 in pre-deploy perf test."
  - risk_id: "R-5"
    edge_case: "Keyword input containing HTML/script payload triggering XSS on render."
    mitigation: "Strict allowlist validation on input; HTML-escape all rendered result fields; no innerHTML from raw data."
metrics:
  - name: "search_latency_p95"
    value: 500
    unit: "ms"
  - name: "throughput_rps"
    value: 100
    unit: "requests/sec"
  - name: "availability"
    value: 99.9
    unit: "percent"
---

# Business Analysis Output - mock-search-feature

> Analyzed from: ba-elicitor/elicitation-report.md (status=completed, confidence=70, all clarifications resolved)

## 1. Classification and MoSCoW

| ID | Requirement | Type | MoSCoW | Priority |
|----|-------------|------|--------|----------|
| FR-1 | Keyword input | FR | Must | P0 |
| FR-2 | Category filter (hardcoded) | FR | Should | P1 |
| FR-3 | Price range filter | FR | Should | P1 |
| FR-4 | Relevance sort (substring match) | FR | Must | P0 |
| FR-5 | Results page render + 12/page pagination | FR | Must | P0 |
| NFR-1 | Latency p95 <= 500ms | NFR | Must | P0 |
| NFR-2 | Throughput 100 req/s | NFR | Should | P1 |
| NFR-3 | Strict allowlist input validation | NFR | Must | P0 |
| NFR-4 | WCAG 2.1 Level AA | NFR | Should | P1 |
| NFR-5 | Availability 99.9% | NFR | Should | P1 |

Excluded by scope: autocomplete/live search (submit-only), TF-IDF/ML ranking, dynamic category admin, external search service/DB.

## 2. Diagrams (Mermaid - all labels double-quoted)

### 2.1 Sequence Diagram

```mermaid
sequenceDiagram
    participant "Online Shopper" as Shopper
    participant "Search UI" as UI
    participant "Search Engine" as Engine
    participant "Product Catalog (static JSON)" as Catalog
    Shopper->>UI: "enter keyword + select category/price"
    Shopper->>UI: "click submit button"
    UI->>Engine: "submitQuery(keyword, category, priceRange)"
    Engine->>Engine: "validate input (strict allowlist)"
    Engine->>Catalog: "load and scan static JSON"
    Catalog-->>Engine: "return matched items"
    Engine->>Engine: "sort by substring relevance"
    Engine-->>UI: "return page (12 items)"
    UI-->>Shopper: "render search results page"
```

### 2.2 Flowchart (3-Path)

```mermaid
flowchart TD
    A["Shopper submits query"] --> B{"Input valid?"}
    B -->|"No"| C["Show safe validation message"]
    B -->|"Yes"| D["Scan static JSON catalog"]
    D --> E{"Matches found?"}
    E -->|"Yes"| F["Sort by relevance"]
    F --> G["Render results page 12/page"]
    E -->|"No"| H["Show 'no results' message"]
    D --> I{"Category/price filter set?"}
    I -->|"Yes (Alternative)"| J["Apply filter only, match-all keyword"]
    I -->|"No (Happy/Alt)"| F
    C --> A
    H --> A
```

### 2.3 ERD (PK / FK)

```mermaid
erDiagram
    PRODUCT {
        string product_id PK
        string name
        string description
        decimal price
        string category_id FK
        string keywords
    }
    CATEGORY {
        string category_id PK
        string label
    }
    PRODUCT ||--o{ CATEGORY : "belongs to"
```

## 3. Data Schema

### 3.1 Data Tables

| Entity | Field | Type | Key | Notes |
|--------|-------|------|-----|-------|
| PRODUCT | product_id | string | PK | unique catalog id |
| PRODUCT | name | string | - | display name |
| PRODUCT | description | string | - | free text |
| PRODUCT | price | decimal | - | numeric, >= 0 |
| PRODUCT | category_id | string | FK to CATEGORY | hardcoded set |
| PRODUCT | keywords | string | - | substring match target |
| CATEGORY | category_id | string | PK | hardcoded in app code |
| CATEGORY | label | string | - | human-readable |

### 3.2 JSON Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Product",
  "type": "object",
  "required": ["product_id", "name", "price", "category_id"],
  "properties": {
    "product_id": { "type": "string", "minLength": 1 },
    "name": { "type": "string", "minLength": 1 },
    "description": { "type": "string" },
    "price": { "type": "number", "minimum": 0 },
    "category_id": { "type": "string", "enum": ["electronics", "books", "home", "fashion", "toys"] },
    "keywords": { "type": "string" }
  },
  "additionalProperties": false
}
```

## 4. Gherkin Scenarios and User Story

User Story: As an Online Shopper, I want to enter a keyword and apply category/price filters then submit, so that I can quickly find relevant products ranked by relevance across a paginated results page.

```gherkin
Feature: Product Search over static JSON catalog

  Scenario: Happy Path - query plus filters return ranked paginated results
    Given the static product catalog is loaded
    And the shopper enters keyword "phone"
    And the shopper selects category "electronics"
    And the shopper sets price range 100 to 500
    When the shopper clicks the submit button
    Then the system validates input via strict allowlist
    And the system returns results sorted by substring relevance
    And the results page displays at most 12 items per page

  Scenario: Alternative Path - keyword only or filter only still valid
    Given the static product catalog is loaded
    And the shopper enters no keyword
    And the shopper selects category "books"
    When the shopper clicks the submit button
    Then the system treats empty keyword as match-all
    And the system returns books matching the category filter
    And the results page renders without error

  Scenario: Exception Path - no match and invalid price range
    Given the static product catalog is loaded
    And the shopper enters keyword "zzzznotexist"
    When the shopper clicks the submit button
    Then the system displays the "no results" message
    And the filter state is preserved for adjustment
    Given the shopper sets price range 500 to 100
    When the shopper clicks the submit button
    Then the system shows a safe validation message
    And the search is aborted without crashing
```

## 5. Risk Matrix (P x I)

| Risk | Probability | Impact | Score | Mitigation |
|------|-------------|--------|-------|------------|
| R-1 Empty keyword plus filters | Medium | Low | 4 | Match-all keyword; bounded scan |
| R-2 Invalid price range | Medium | Low | 4 | Pre-query validation, safe message |
| R-3 No match or empty set | High | Low | 3 | "no results" UI, preserve state |
| R-4 Catalog load over p95 500ms | Low | Medium | 3 | Bootstrap pre-load, in-memory scan |
| R-5 XSS via keyword input | Low | High | 4 | Allowlist plus HTML escape on render |

## 6. Metadata

- analyzed_by: ba-analyst (skill v3.0.0)
- status: completed
- schema_ref: skills/ver-3/_shared/schemas/analysis.schema.yaml
- artifact_lifecycle: raw -> designed -> planned -> built
- validated_by: schema_validator.py + validate_metrics.py (8/8 metric gates; exit 0)
