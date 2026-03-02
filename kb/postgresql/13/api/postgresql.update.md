---
library: postgresql
version: "13.5"
category: api
item: postgresql.update
type: command
signature: "UPDATE table SET col = value [WHERE condition] [RETURNING]"
keywords: ["update", "modify", "change", "edit"]
aliases: ["update row", "modify data", "change values"]
intent: "Modify existing rows in a table, updating column values for rows matching optional condition."
last_updated: "2025-03-02"
schema_version: "2.0"
source_url: "https://www.postgresql.org/docs/13/sql-update.html"
source_title: "UPDATE Documentation"
alternatives:
  - option: "INSERT ON CONFLICT"
    reason: "Insert or update in single statement."
  - option: "CTE with UPDATE"
    reason: "Complex updates across multiple tables."
---

# UPDATE

## Signature
```sql
UPDATE table SET col1 = value1, col2 = value2 WHERE condition;
UPDATE table SET col = value RETURNING *;
```

## What It Does
Updates column values in existing rows. Can update multiple columns. WHERE filters rows. RETURNING returns updated values.

## Use When
- Modifying existing data.
- Batch updates based on conditions.
- Setting status flags.
- Counter increments.

## Examples
```sql
UPDATE users SET email = 'new@email.com' WHERE id = 1;
```

```sql
UPDATE products SET price = price * 1.1 WHERE category = 'electronics';
```

```sql
UPDATE orders SET status = 'shipped', shipped_at = NOW() 
WHERE id = 123
RETURNING id, status;
```

```sql
UPDATE users SET last_login = NOW() WHERE id IN (
  SELECT user_id FROM sessions WHERE created > '1 hour ago'::interval
);
```

```sql
-- Using subquery
UPDATE employees SET salary = (
  SELECT avg(salary) * 1.1 FROM employees WHERE dept = employees.dept
);
```

## Returns
Number of affected rows or RETURNING result

## Gotchas / Version Notes
- Without WHERE, updates ALL rows.
- Use RETURNING to get updated values.
- Can reference current row values.
- Use transactions for safety on bulk updates.

## References
- PostgreSQL UPDATE: https://www.postgresql.org/docs/13/sql-update.html
