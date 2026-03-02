---
library: postgresql
version: "17.0"
category: api
item: postgresql.merge
type: command
signature: "MERGE INTO target_table USING source ON condition WHEN MATCHED THEN UPDATE WHEN NOT MATCHED THEN INSERT"
keywords: ["merge", "upsert", "insert update", "conditional insert"]
aliases: ["upsert", "insert or update", "conditional insert"]
intent: "Conditionally insert, update, or delete rows based on a source table or query, combining INSERT, UPDATE, and DELETE in a single statement."
last_updated: "2025-03-02"
schema_version: "2.0"
source_url: "https://www.postgresql.org/docs/17/sql-merge.html"
source_title: "MERGE Documentation"
alternatives:
  - option: "INSERT ON CONFLICT"
    reason: "Simpler upsert for single table with unique constraint."
  - option: "PL/pgSQL with IF/ELSE"
    reason: "More control over complex merge logic."
---

# MERGE

## Signature
```sql
MERGE INTO target_table AS t
USING source_table_or_query AS s
ON t.key_column = s.key_column
WHEN MATCHED THEN
    UPDATE SET col1 = s.col1, col2 = s.col2
WHEN NOT MATCHED THEN
    INSERT (col1, col2) VALUES (s.col1, s.col2);
```

## What It Does
Atomically inserts, updates, or deletes rows based on conditions. Like UPSERT but more powerful - can perform different actions based on match status. Ensures data integrity in single transaction.

## Use When
- Syncing data between tables.
- Implementing change data capture (CDC).
- Bulk upsert with complex conditions.
- Data warehouse incremental loads.

## Examples
```sql
MERGE INTO orders AS o
USING new_orders AS n
ON o.order_id = n.order_id
WHEN MATCHED THEN
    UPDATE SET status = n.status, updated_at = NOW()
WHEN NOT MATCHED THEN
    INSERT (order_id, status, created_at)
    VALUES (n.order_id, n.status, NOW());
```

```sql
MERGE INTO inventory i
USING (VALUES (101, 50), (102, 30)) AS v(product_id, quantity)
ON i.product_id = v.product_id
WHEN MATCHED THEN
    UPDATE SET stock = i.stock + v.quantity
WHEN NOT MATCHED THEN
    INSERT (product_id, stock) VALUES (v.product_id, v.quantity);
```

```sql
MERGE INTO users u
USING source s
ON u.email = s.email
WHEN MATCHED AND s.deleted THEN
    DELETE
WHEN MATCHED THEN
    UPDATE SET last_login = s.last_login
WHEN NOT MATCHED THEN
    INSERT (email, name, created_at) 
    VALUES (s.email, s.name, NOW());
```

## Returns
MERGE command completion tag with row counts

## Gotchas / Version Notes
- Available in PostgreSQL 15+.
- Requires ON clause with condition.
- Can have multiple WHEN clauses.
- Source can be a table, VALUES, or subquery.
- Each row can only match once to avoid ambiguity.

## References
- PostgreSQL MERGE: https://www.postgresql.org/docs/17/sql-merge.html
- INSERT ON CONFLICT: https://www.postgresql.org/docs/17/sql-insert.html
