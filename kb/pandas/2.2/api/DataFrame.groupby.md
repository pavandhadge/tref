---
library: pandas
version: "2.2.0"
category: api
item: DataFrame.groupby
type: method
signature: "DataFrame.groupby(by=None, axis=0, level=None, as_index=True, sort=True, group_keys=True, observed=False, dropna=True)"
keywords: ["groupby", "group by", "aggregation", "multi-column"]
last_updated: "2025-03-02"
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
- by: Label, mapping, function, or list of labels used to determine groups.
- as_index: If `True`, returns grouped labels as index.
- observed: For categorical groupers, show only observed values if `True`.
- dropna: If `False`, NA group keys are preserved.

## Examples
```python
out = df.groupby(['A', 'B']).agg({'C': 'mean'})
```

## Gotchas / Version Notes
- In 2.2+, behavior around categorical groupers and `observed` can affect output shape.
- Prefer explicit `dropna=` for stable behavior across environments.
