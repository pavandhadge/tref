---
library: polars
version: "0.20.0"
category: api
item: DataFrame.group_by
type: method
signature: "DataFrame.group_by(by, *more_by, maintain_order=False)"
keywords: ["group_by", "aggregation", "multiple columns", "polars"]
aliases: ["pl group by", "df.group_by", "polars groupby"]
intent: "Group rows by expressions and compute fast aggregations."
last_updated: "2025-03-02"
schema_version: "2.0"
source_url: "https://docs.pola.rs/api/python/stable/reference/dataframe/api/polars.DataFrame.group_by.html"
source_title: "polars.DataFrame.group_by"
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

## What It Does
Groups rows by one or more columns/expressions and evaluates expression-based aggregations in `.agg(...)`.

## Use When
- You need high-performance grouped aggregations.
- You want expression-driven aggregations.
- You need optional source-order group preservation.

## Examples
```python
out = (
    df.group_by(['A', 'B'])
      .agg(pl.col('C').mean())
)
```

```python
out = (
    df.group_by("team")
      .agg(
          pl.col("points").mean().alias("avg_points"),
          pl.col("assists").max().alias("max_assists"),
          pl.len().alias("rows"),
      )
)
```

```python
out = df.group_by("category", maintain_order=True).agg(pl.col("value").sum())
```

## Alternatives
- Lazy query with `scan_*` + `group_by` for larger-than-memory pipelines.
- `partition_by(...)` when you need materialized per-group DataFrames.

## Gotchas / Version Notes
- `group_by` is the canonical API name in Polars.
- Use expression API in `.agg(...)` for best performance.
- `maintain_order=True` can trade speed for deterministic ordering.

## References
- polars.DataFrame.group_by docs: https://docs.pola.rs/api/python/stable/reference/dataframe/api/polars.DataFrame.group_by.html
- Polars user guide: https://docs.pola.rs/user-guide/
