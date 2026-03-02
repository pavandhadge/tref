---
library: pandas
version: "2.2.0"
category: api
item: DataFrame.agg
type: method
signature: "DataFrame.agg(func=None, axis=0, *args, **kwargs)"
keywords: ["agg", "aggregate", "groupby", "summary"]
aliases: ["df.agg", "aggregate dataframe"]
intent: "Apply one or more aggregation functions across rows or columns."
last_updated: "2025-03-02"
schema_version: "2.0"
source_url: "https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.agg.html"
source_title: "pandas.DataFrame.agg"
---

# pandas.DataFrame.agg

## Signature
```python
df.agg(func=None, axis=0, *args, **kwargs)
```

## What It Does
Executes aggregation functions over DataFrame axes. Supports single function, list of functions, dict per-column, and custom callables.

## Use When
- You want compact summary stats over multiple columns.
- You need different aggregations per column.
- You need row-wise aggregation (`axis=1`).

## Examples
```python
df.groupby('team').agg({'points': 'mean', 'assists': 'max'})
```

```python
out = df.agg({"points": ["min", "max", "mean"], "assists": "sum"})
```

```python
out = df[["x", "y", "z"]].agg("sum", axis=1)
```

```python
out = df.agg({"latency_ms": ["mean", "median", lambda s: s.quantile(0.95)]})
```

## Alternatives
- `DataFrame.describe()` for quick default summaries.
- `GroupBy.agg(...)` for per-group aggregation.
- `DataFrame.transform(...)` when output must align 1:1 with original shape.

## Gotchas / Version Notes
- Dict aggregation preserves column targeting and is usually more explicit.
- Mixed return types may produce MultiIndex columns.
- Custom lambdas can be slower than vectorized built-ins.

## References
- pandas.DataFrame.agg docs: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.agg.html
- Aggregation guide: https://pandas.pydata.org/docs/user_guide/basics.html#basics-apply
