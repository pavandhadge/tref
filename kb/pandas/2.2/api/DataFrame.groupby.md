---
library: pandas
version: "2.2.0"
category: api
item: DataFrame.groupby
type: method
signature: "DataFrame.groupby(by=None, axis=0, level=None, as_index=True, sort=True, group_keys=True, observed=False, dropna=True)"
keywords: ["groupby", "group by", "aggregation", "multi-column"]
aliases: ["df.groupby", "group by columns", "group rows"]
intent: "Group rows by one or more keys, then aggregate or transform."
last_updated: "2025-03-02"
schema_version: "2.0"
source_url: "https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.groupby.html"
source_title: "pandas.DataFrame.groupby"
alternatives:
  - option: "DataFrame.pivot_table(...)"
    reason: "Use spreadsheet-style grouped summaries with explicit values/index/columns."
  - option: "DataFrame.resample(...)"
    reason: "Use time-series frequency buckets for datetime-indexed aggregation."
  - option: "DataFrame.value_counts(...)"
    reason: "Use fast frequency counts for value combinations."
---

# pandas.DataFrame.groupby

## Signature
```python
df.groupby(
    by=None,
    axis=0,
    level=None,
    as_index=True,
    sort=True,
    group_keys=True,
    observed=False,
    dropna=True,
)
```

## Parameters
- by: str, list, dict, Series, callable, or None (default `None`).
- axis: `{0, 1}` (default `0`), deprecated in pandas 2.1+ for this API surface.
- level: int or str when grouping MultiIndex levels.
- as_index: bool (default `True`), set `False` to keep grouping columns in output.
- observed: bool for categorical groupers.
- dropna: bool (default `True`), explicitly set for predictable NA-group handling.

## What It Does
Creates grouped views of rows using keys in `by`, enabling aggregation (`agg`), transformation (`transform`), and filtering (`filter`) per group.

## Use When
- You need summaries per category (team, region, month).
- You need multi-key aggregations such as `['country', 'city']`.
- You need per-group transforms (z-score, rolling within group).

## Examples
```python
out = df.groupby(['A', 'B']).agg({'C': 'mean'})
```

```python
out = (
    df.groupby("team", as_index=False)
      .agg(avg_points=("points", "mean"), max_assists=("assists", "max"))
)
```

```python
out = df.groupby("segment", dropna=False)["revenue"].sum()
```

```python
out = (
    df.groupby(df["ts"].dt.to_period("M"))
      .agg({"sales": ["sum", "mean"], "orders": "count"})
)
```

## Returns
pandas.core.groupby.generic.DataFrameGroupBy

## Alternatives
- `DataFrame.pivot_table(...)` for spreadsheet-like grouped summaries with explicit value/row/column pivots.
- `DataFrame.resample(...)` for time-series bucket aggregation.
- `DataFrame.value_counts(...)` for fast frequency counts of value combinations.

## Gotchas / Version Notes
- In 2.2+, behavior around categorical groupers and `observed` can affect output shape.
- Prefer explicit `dropna=` for stable behavior across environments.
- `as_index=True` changes result shape and can surprise downstream merges.

## References
- pandas.DataFrame.groupby docs: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.groupby.html
- GroupBy user guide: https://pandas.pydata.org/docs/user_guide/groupby.html
