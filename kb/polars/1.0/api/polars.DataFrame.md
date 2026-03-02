---
library: polars
version: "1.0.0"
category: api
item: polars.DataFrame
type: class
signature: "pl.DataFrame(data), pl.from_pandas(df)"
keywords: ["polars", "dataframe", "fast", "data"]
aliases: ["polars dataframe", "data table", "analytics"]
intent: "High-performance DataFrame library written in Rust, providing fast data manipulation with lazy evaluation and native Python API."
last_updated: "2025-03-02"
schema_version: "2.0"
source_url: "https://docs.pola.rs/api/python/stable/reference/dataframe/"
source_title: "Polars DataFrame Documentation"
alternatives:
  - option: "pandas"
    reason: "More mature, more integrations, but slower."
  - option: "dask"
    reason: "Out-of-core computation, not real-time."
  - option: "pyspark"
    reason: "Distributed computing for big data."
---

# Polars DataFrame

## Signature
```python
import polars as pl

df = pl.DataFrame({
    "name": ["Alice", "Bob"],
    "age": [25, 30]
})
```

## What It Does
Fast DataFrame library written in Rust. Offers lazy and eager execution, SIMD optimizations, and expressive API. 10-100x faster than pandas for most operations.

## Use When
- Performance-critical data processing.
- Large dataset manipulation.
- When pandas is too slow.
- ETL pipelines.

## Examples
```python
import polars as pl

# Create
df = pl.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})

# Select
df.select("a")
df.select(pl.col("a", "b"))

# Filter
df.filter(pl.col("a") > 1)

# With expressions
df.select([
    pl.col("a").sum().alias("total"),
    pl.col("b").mean().alias("avg")
])
```

```python
# Lazy execution
query = (
    pl.scan_csv("data.csv")
    .filter(pl.col("value") > 0)
    .group_by("category")
    .agg(pl.col("value").sum())
    .collect()
)
```

```python
# Join
df1.join(df2, on="id", how="left")
```

```python
# Create columns
df.with_columns([
    (pl.col("a") * 2).alias("doubled"),
    pl.col("b").str.uppercase()
])
```

```python
# From pandas
import pandas as pd
df = pl.from_pandas(pandas_df)
pandas_df = df.to_pandas()
```

## Returns
DataFrame or LazyFrame

## Gotchas / Version Notes
- Column-based, not row-based.
- Use lazy for large data.
- Different API than pandas.
- Expressions are composable.

## References
- Polars docs: https://docs.pola.rs/
