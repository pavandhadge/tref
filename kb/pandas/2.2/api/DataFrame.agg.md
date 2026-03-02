---
library: pandas
version: "2.2.0"
category: api
item: DataFrame.agg
type: method
signature: "DataFrame.agg(func=None, axis=0, *args, **kwargs)"
keywords: ["agg", "aggregate", "groupby", "summary"]
last_updated: "2025-03-02"
---

# pandas.DataFrame.agg

## Signature
```python
df.agg(func=None, axis=0, *args, **kwargs)
```

## Parameters
- func: Function, string, list, or dict of aggregation operations.
- axis: Axis to aggregate on (`0` for columns, `1` for rows).

## Examples
```python
df.groupby('team').agg({'points': 'mean', 'assists': 'max'})
```

## Gotchas / Version Notes
- Dict aggregation preserves column-level targeting and is usually more explicit.
- Mixed return types may produce MultiIndex columns.
