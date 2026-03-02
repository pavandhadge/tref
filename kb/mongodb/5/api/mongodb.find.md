---
library: mongodb
version: "5.0.0"
category: api
item: mongodb.find
type: command
signature: "db.collection.find(query, projection)"
keywords: ["find", "query", "select", "read"]
aliases: ["mongodb find", "query documents", "search collection"]
intent: "Query documents from a MongoDB collection with filtering, projection, sorting, and pagination support."
last_updated: "2025-03-02"
schema_version: "2.0"
source_url: "https://docs.mongodb.com/manual/reference/method/db.collection.find/"
source_title: "find Documentation"
alternatives:
  - option: "aggregate"
    reason: "Complex queries with multiple stages and transformations."
  - option: "findOne"
    reason: "Returns single document, more efficient for one result."
  - option: "findOneAndUpdate"
    reason: "Find and update in single atomic operation."
---

# find()

## Signature
```javascript
db.collection.find(query, projection)
db.collection.find(query).sort(sort).limit(n).skip(n)
```

## Parameters
- query: Document with selection criteria (empty = all).
- projection: Document specifying fields to include/exclude.
- sort: Sort order document.
- limit: Maximum documents to return.
- skip: Number of documents to skip.

## What It Does
Returns documents matching the query criteria. Supports complex queries with operators ($eq, $gt, $in, $regex, etc.). Cursor provides additional methods for sorting, limiting, and pagination.

## Use When
- Retrieving documents from a collection.
- Filtering by field values or operators.
- Paginating results.
- Projecting specific fields.

## Examples
```javascript
db.users.find()
```

```javascript
db.users.find({ age: { $gte: 18 } })
```

```javascript
db.users.find({ status: "active" }, { name: 1, email: 1, _id: 0 })
```

```javascript
db.orders.find().sort({ createdAt: -1 }).limit(10)
```

```javascript
db.products.find({ 
  category: "electronics",
  price: { $lte: 1000 }
}).skip(20).limit(10)
```

```javascript
db.users.find({ name: { $regex: "^J" } })
```

## Returns
Cursor with matching documents

## Gotchas / Version Notes
- Use explain() to analyze query performance.
- Create indexes for frequently queried fields.
- Projection: 1 to include, 0 to exclude (except _id).
- Use explain("executionStats") for query planning.
- Empty query {} returns all documents.

## References
- find(): https://docs.mongodb.com/manual/reference/method/db.collection.find/
- Query operators: https://docs.mongodb.com/manual/reference/operator/query/
