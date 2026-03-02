---
library: python
version: "3.9.0"
category: api
item: python.pandas_dataframe
type: class
signature: "pd.DataFrame(data, index, columns)"
keywords: ["dataframe", "pandas", "table", "data"]
aliases: ["pandas dataframe", "data table", "tabular data"]
intent: "Two-dimensional labeled data structure with columns of potentially different types, similar to spreadsheet or SQL table."
last_updated: "2025-03-02"
schema_version: "2.0"
source_url: "https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html"
source_title: "DataFrame Documentation"
alternatives:
  - option: "numpy array"
    reason: "Homogeneous numeric data only, less features."
  - option: "polars DataFrame"
    reason: "Faster, more modern, but fewer integrations."
  - option: "dask DataFrame"
    reason: "Out-of-core computation for large datasets."
---

# DataFrame

## Signature
```python
import pandas as pd

df = pd.DataFrame({
    "name": ["Alice", "Bob", "Charlie"],
    "age": [25, 30, 35],
    "salary": [50000, 60000, 70000]
})
```

## What It Does
Two-dimensional data structure with labeled axes (rows and columns). Supports heterogeneous data types, missing values, slicing, grouping, merging, and time series operations.

## Use When
- Tabular data analysis.
- CSV/Excel file processing.
- Statistical analysis.
- Data cleaning and transformation.

## Examples
```python
# Create
df = pd.DataFrame({"a": [1, 2], "b": [3, 4]})

# Access
df["column"]         # Series
df[["col1", "col2"]] # DataFrame
df.iloc[0]           # Row by position
df.loc["row_name"]   # Row by label

# Query
df[df["age"] > 25]
df.query("age > 25")

# Transform
df["new_col"] = df["a"] + df["b"]
df.assign(new=df["a"] * 2)

# Aggregate
df.groupby("category").agg({"price": "sum", "quantity": "mean"})
df.describe()  # stats summary
```

```python
# IO
df = pd.read_csv("file.csv")
df = pd.read_excel("file.xlsx")
df.to_csv("output.csv", index=False)
df.to_json("output.json")

# Missing data
df.dropna()           # remove rows with NaN
df.fillna(0)          # fill NaN with value
df.isnull()           # boolean mask
```

```python
# Merge
pd.merge(left, right, on="key", how="inner")
pd.concat([df1, df2], axis=0)
```

## Returns
DataFrame object

## Gotchas / Version Notes
- Use method chaining for readable code.
- Watch for SettingWithCopyWarning.
- Use inplace=True carefully (being deprecated).
- Index alignment happens automatically.

## References
- DataFrame docs: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html
- 10 min guide: https://pandas.pydata.org/docs/user_guide/10min.html
