---
library: postgresql
version: "13.5"
category: api
item: postgresql.select
type: command
signature: "SELECT columns FROM table [WHERE condition] [GROUP BY] [ORDER BY] [LIMIT]"
keywords: ["select", "query", "read", "retrieve"]
aliases: ["query data", "fetch rows", "select statement"]
intent: "Retrieve data from one or more tables, with filtering, grouping, sorting, and aggregation capabilities."
last_updated: "2025-03-02"
schema_version: "2.0"
source_url: "https://www.postgresql.org/docs/13/sql-select.html"
source_title: "SELECT Documentation"
alternatives:
  - option: "COPY"
    reason: "Bulk export data to files."
  - option: "psql meta-commands"
    reason: "Quick table listing without full query."
---

# SELECT

## Signature
```sql
SELECT [DISTINCT] column_list
FROM table_name
[JOIN other_table ON condition]
[WHERE condition]
[GROUP BY column]
[HAVING group_condition]
[ORDER BY column [ASC|DESC]]
[LIMIT count] [OFFSET start];
```

## What It Does
Retrieves rows from database tables. Can filter, transform, aggregate, and sort data. Supports joins, subqueries, window functions, and CTEs for complex data operations.

## Use When
- Fetching data for display or processing.
- Aggregating and analyzing data.
- Combining data from multiple tables.

## Examples
```sql
SELECT * FROM users;
```

```sql
SELECT name, email FROM users WHERE active = true;
```

```sql
SELECT department, COUNT(*) as employees
FROM employees
GROUP BY department
HAVING COUNT(*) > 10
ORDER BY employees DESC;
```

```sql
SELECT u.name, o.total
FROM users u
JOIN orders o ON u.id = o.user_id
WHERE o.created_at > '2024-01-01'
ORDER BY o.total DESC
LIMIT 10;
```

```sql
WITH monthly_sales AS (
  SELECT DATE_TRUNC('month', created_at) as month, SUM(total) as sales
  FROM orders
  GROUP BY 1
)
SELECT * FROM monthly_sales ORDER BY month;
```

## Returns
Result set (rows and columns)

## Gotchas / Version Notes
- Use `*` sparingly - specify columns for clarity and performance.
- Indexes on WHERE/JOIN columns improve performance.
- DISTINCT removes duplicate rows.
- NULL comparisons require IS NULL/IS NOT NULL.
- String literals use single quotes.

## References
- PostgreSQL SELECT: https://www.postgresql.org/docs/13/sql-select.html
- Tutorial: https://www.postgresql.org/docs/13/tutorial-select.html
