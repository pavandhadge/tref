---
library: polars
version: "0.20.0"
category: api
item: DataFrame.group_by
type: method
signature: "DataFrame.group_by(by, *more_by, maintain_order=False)"
keywords: ["group_by", "aggregation", "multiple columns", "polars"]
last_updated: "2025-03-02"
---

# polars.DataFrame.group_by

## Signature
```python
df.group_by(
    by,
    *more_by,
    maintain_order=False,
)
```

## Parameters
- by: Column expression(s) used for grouping.
- maintain_order: Keep input order for groups if `True`.

## Examples
```python
out = (
    df.group_by(['A', 'B'])
      .agg(pl.col('C').mean())
)
```

## Gotchas / Version Notes
- `group_by` is the canonical API name in Polars.
- Use expression API in `.agg(...)` for best performance.
