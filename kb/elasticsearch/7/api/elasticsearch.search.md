---
library: elasticsearch
version: "7.17.0"
category: api
item: elasticsearch.search
type: command
signature: "GET /index/_search { query }"
keywords: ["search", "query", "find", "match"]
aliases: ["elasticsearch query", "full text search", "search API"]
intent: "Search documents in Elasticsearch indices using query DSL with full-text, term-level, compound, and aggregations."
last_updated: "2025-03-02"
schema_version: "2.0"
source_url: "https://www.elastic.co/guide/en/elasticsearch/reference/current/search-search.html"
source_title: "Search API Documentation"
alternatives:
  - option: "SQL plugin"
    reason: "SQL-like queries for users familiar with relational DBs."
  - option: "Transport client"
    reason: "Legacy client, replaced by REST client."
  - option: "Aggregations"
    reason: "Analytics over search results."
---

# Search API

## Signature
```http
GET /index/_search
{
  "query": { ... },
  "aggs": { ... },
  "from": 0,
  "size": 10
}
```

## Query DSL
- match: Full-text search
- term: Exact value
- bool: Compound queries
- range: Numeric/date ranges
- must/filter: Query clauses

## What It Does
Executes search query against one or more indices. Returns matching documents with scores. Supports pagination, sorting, highlighting, and aggregations for analytics.

## Use When
- Full-text search across documents.
- Filtering and faceted search.
- Analytics and aggregations.
- Autocomplete/suggestions.

## Examples
```json
GET /products/_search
{
  "query": {
    "match": {
      "name": "laptop"
    }
  }
}
```

```json
GET /products/_search
{
  "query": {
    "bool": {
      "must": [
        { "match": { "name": "laptop" } }
      ],
      "filter": [
        { "range": { "price": { "lte": 1000 } } }
      ]
    }
  }
}
```

```json
GET /orders/_search
{
  "query": { "match_all": {} },
  "aggs": {
    "status_counts": {
      "terms": { "field": "status" }
    },
    "total_sales": {
      "sum": { "field": "amount" }
    }
  }
}
```

```json
GET /products/_search
{
  "query": { "match_all": {} },
  "from": 20,
  "size": 10,
  "sort": [{ "price": "asc" }]
}
```

```json
GET /articles/_search
{
  "query": { "match_phrase": { "content": "machine learning" } },
  "highlight": {
    "fields": { "content": {} }
  }
}
```

## Returns
Search response with hits and optionally aggregations

## Gotchas / Version Notes
- Default size is 10 results.
- Use scroll API for deep pagination.
- Index field types determine query behavior.
- Use filter context for cached filters.
- Match vs term queries (analyzed vs not).

## References
- Search API: https://www.elastic.co/guide/en/elasticsearch/reference/current/search-search.html
- Query DSL: https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl.html
