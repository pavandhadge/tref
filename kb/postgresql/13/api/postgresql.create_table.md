---
library: postgresql
version: "13.5"
category: api
item: postgresql.create_table
type: command
signature: "CREATE TABLE name (columns) [OPTIONS]"
keywords: ["create", "table", "schema", "define"]
aliases: ["create table", "define table", "schema"]
intent: "Create a new table with specified columns, data types, constraints, and optional storage parameters."
last_updated: "2025-03-02"
schema_version: "2.0"
source_url: "https://www.postgresql.org/docs/13/sql-createtable.html"
source_title: "CREATE TABLE Documentation"
alternatives:
  - option: "CREATE TABLE AS"
    reason: "Create table from query results."
  - option: "INHERITS"
    reason: "Table inheritance for partitioning."
---

# CREATE TABLE

## Signature
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE,
    created_at TIMESTAMP DEFAULT NOW()
);
```

## What It Does
Creates new table with columns, types, constraints. Supports primary keys, foreign keys, unique, not null, defaults, check constraints.

## Use When
- Creating new database tables.
- Defining schema structure.
- Setting up relationships.
- Adding constraints.

## Examples
```sql
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    price DECIMAL(10,2) CHECK (price >= 0),
    category_id INTEGER REFERENCES categories(id),
    created_at TIMESTAMP DEFAULT NOW()
);
```

```sql
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    total DECIMAL(10,2) DEFAULT 0,
    status VARCHAR(20) DEFAULT 'pending',
    CONSTRAINT valid_status CHECK (status IN ('pending', 'shipped', 'delivered'))
);
```

```sql
-- With indexes
CREATE TABLE logs (
    id SERIAL PRIMARY KEY,
    message TEXT,
    created_at TIMESTAMP DEFAULT NOW()
) USING BRIN (created_at);
```

```sql
-- Temporary table
CREATE TEMP TABLE session_data ( ... );
```

```sql
-- If not exists
CREATE TABLE IF NOT EXISTS users ( ... );
```

## Returns
Success or error

## Gotchas / Version Notes
- Use descriptive names.
- Always include PRIMARY KEY.
- Use appropriate data types.
- Consider storage parameters for large tables.
- BRIN indexes for time-series.

## References
- CREATE TABLE: https://www.postgresql.org/docs/13/sql-createtable.html
