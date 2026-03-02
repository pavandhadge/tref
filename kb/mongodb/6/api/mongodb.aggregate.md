---
library: mongodb
version: "6.0.0"
category: api
item: mongodb.aggregate
type: command
signature: "db.collection.aggregate([stage1, stage2, ...])"
keywords: ["aggregate", "pipeline", "transform", "analytics"]
aliases: ["aggregation pipeline", "mongodb aggregate", "data processing"]
intent: "Process documents through a multi-stage pipeline for transformation, grouping, filtering, and analytics operations."
last_updated: "2025-03-02"
schema_version: "2.0"
source_url: "https://docs.mongodb.com/manual/aggregation/"
source_title: "Aggregation Documentation"
alternatives:
  - option: "find + JavaScript"
    reason: "Processing in application code, less efficient."
  - option: "mapReduce"
    reason: "Legacy, replaced by aggregation pipeline."
  - option: "separate queries"
    reason: "Multiple round trips, less atomic."
---

# aggregate()

## Signature
```javascript
db.collection.aggregate([
  { $match: { ... } },
  { $group: { ... } },
  { $sort: { ... } },
  { $project: { ... } }
])
```

## Pipeline Stages
- $match: Filter documents.
- $group: Group and aggregate.
- $project: Reshape documents.
- $sort: Sort documents.
- $limit, $skip: Pagination.
- $lookup: Join collections.
- $unwind: Deconstruct arrays.

## What It Does
Runs documents through an aggregation pipeline. Each stage transforms documents and passes to next. Enables complex analytics, grouping, and transformations within MongoDB.

## Use When
- Calculating aggregations (sum, avg, count).
- Grouping data by categories.
- Complex transformations and projections.
- Joining collections.
- Creating materialized views.

## Examples
```javascript
db.orders.aggregate([
  { $match: { status: "completed" } },
  { $group: { _id: "$customerId", total: { $sum: "$amount" } } }
])
```

```javascript
db.products.aggregate([
  { $match: { category: "electronics" } },
  { $sort: { price: -1 } },
  { $limit: 10 }
])
```

```javascript
db.orders.aggregate([
  {
    $lookup: {
      from: "products",
      localField: "productId",
      foreignField: "_id",
      as: "product"
    }
  }
])
```

```javascript
db.users.aggregate([
  { $unwind: "$tags" },
  { $group: { _id: "$tags", count: { $sum: 1 } } },
  { $sort: { count: -1 } }
])
```

```javascript
db.sales.aggregate([
  {
    $group: {
      _id: { $dateToString: { format: "%Y-%m", date: "$date" } },
      revenue: { $sum: "$amount" }
    }
  }
])
```

## Returns
Cursor with aggregated results

## Gotchas / Note
- Pipeline runs on MongoDB server, not application.
- Use $match early for performance.
- Indexes improve $match and $sort stages.
- $group is memory-intensive for large datasets.
- Use allowDiskUse for large aggregations.

## References
- Aggregation: https://docs.mongodb.com/manual/aggregation/
- Pipeline stages: https://docs.mongodb.com/manual/reference/operator/aggregation-pipeline/
