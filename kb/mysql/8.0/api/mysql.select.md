---
library: mysql
version: "8.0.0"
category: api
item: mysql.select
type: command
signature: "SELECT columns FROM table [WHERE] [GROUP BY] [HAVING] [ORDER BY] [LIMIT]"
keywords: ["select", "query", "read", "retrieve"]
aliases: ["mysql select", "query data", "fetch rows"]
intent: "Retrieve data from MySQL tables with filtering, grouping, sorting, and advanced SQL features."
last_updated: "2025-03-02"
schema_version: "2.0"
source_url: "https://dev.mysql.com/doc/refman/8.0/en/select.html"
source_title: "SELECT Documentation"
alternatives:
  - option: "SHOW"
    reason: "Display table structure and metadata."
  - option: "EXPLAIN"
    reason: "Analyze query execution plan."
  - option: "DESCRIBE"
    reason: "Get table column information."
---

# SELECT

## Signature
```sql
SELECT [DISTINCT] columns
FROM table
[JOIN tables ON condition]
[WHERE condition]
[GROUP BY column]
[HAVING group_condition]
[ORDER BY column [ASC|DESC]]
[LIMIT count] [OFFSET start];
```

## What It Does
Retrieves data from one or more MySQL tables. Supports complex queries with joins, subqueries, window functions, CTEs, and JSON operations. MySQL 8.0 added significant analytical capabilities.

## Use When
- Fetching data for applications.
- Aggregating and analyzing data.
- Complex reporting queries.
- Working with JSON data.

## Examples
```sql
SELECT * FROM users;
```

```sql
SELECT name, email FROM users WHERE active = 1;
```

```sql
SELECT department, AVG(salary) as avg_salary
FROM employees
GROUP BY department
HAVING AVG(salary) > 50000
ORDER BY avg_salary DESC;
```

```sql
SELECT u.name, o.total
FROM users u
INNER JOIN orders o ON u.id = o.user_id
WHERE o.created >= '2024-01-01'
ORDER BY o.total DESC
LIMIT 10;
```

```sql
-- Window functions (MySQL 8.0+)
SELECT 
  name,
  department,
  salary,
  RANK() OVER (PARTITION BY department ORDER BY salary DESC) as dept_rank
FROM employees;
```

```sql
-- CTE (MySQL 8.0+)
WITH monthly_sales AS (
  SELECT DATE_FORMAT(created_at, '%Y-%m') as month, SUM(total) as sales
  FROM orders
  GROUP BY 1
)
SELECT * FROM monthly_sales ORDER BY month;
```

## Returns
Result set (rows and columns)

## Gotchas / Version Notes
- MySQL 8.0+ supports CTEs and window functions.
- Indexes critical for query performance.
- Use EXPLAIN ANALYZE for query profiling.
- NULL comparisons use IS NULL/IS NOT NULL.
- String literals use single quotes.

## References
- MySQL SELECT: https://dev.mysql.com/doc/refman/8.0/en/select.html
- Window functions: https://dev.mysql.com/doc/refman/8.0/en/window-function-descriptions.html
