---
library: postgresql
version: "13.5"
category: api
item: postgresql.insert
type: command
signature: "INSERT INTO table (cols) VALUES (values)"
keywords: ["insert", "add", "create", "row"]
aliases: ["insert row", "add data", "insert into"]
intent: "Add new rows to a table, specifying column values or using results from query or DEFAULT values."
last_updated: "2025-03-02"
schema_version: "2.0"
source_url: "https://www.postgresql.org/docs/13/sql-insert.html"
source_title: "INSERT Documentation"
alternatives:
  - option: "COPY"
    reason: "Bulk load from files."
  - option: "INSERT ON CONFLICT"
    reason: "Upsert - insert or update."
---

# INSERT

## Signature
```sql
INSERT INTO table (col1, col2) VALUES (val1, val2);
INSERT INTO table SELECT ...;
INSERT INTO table DEFAULT VALUES;
```

## What It Does
Adds new rows to table. Can insert single row, multiple rows, or results from SELECT. Columns can be in any order, omitted columns get DEFAULT.

## Use When
- Adding new data to tables.
- Importing data from other sources.
- Initializing tables with data.
- Inserting with ON CONFLICT for upserts.

## Examples
```sql
INSERT INTO users (name, email, age) VALUES ('Alice', 'alice@email.com', 30);
```

```sql
INSERT INTO users (name, email) VALUES 
  ('Bob', 'bob@email.com'),
  ('Charlie', 'charlie@email.com');
```

```sql
INSERT INTO orders (user_id, product_id, quantity)
SELECT id, product_id, 1
FROM users, products
WHERE users.name = 'Alice' AND products.name = 'Widget';
```

```sql
INSERT INTO logs (message) DEFAULT VALUES;
```

```sql
INSERT INTO users (name, email)
VALUES ('Dave', 'dave@email.com')
RETURNING id, name;
```

```sql
INSERT INTO users (id, name)
ON CONFLICT (id) DO UPDATE SET name = EXCLUDED.name;
```

## Returns
INSERT oid rows or nothing with RETURNING

## Gotchas / Version Notes
- Use RETURNING to get inserted values.
- ON CONFLICT for upserts (PostgreSQL 9.5+).
- DEFAULT for default values.
- Multiple rows in single statement is faster.

## References
- PostgreSQL INSERT: https://www.postgresql.org/docs/13/sql-insert.html
