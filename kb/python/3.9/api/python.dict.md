---
library: python
version: "3.9.0"
category: api
item: python.dict
type: type
signature: "d = {key: value}"
keywords: ["dict", "dictionary", "hash map", "mapping"]
aliases: ["dictionary", "hash map", "associative array"]
intent: "Store key-value pairs with O(1) average lookup, providing fast data retrieval based on unique keys."
last_updated: "2025-03-02"
schema_version: "2.0"
source_url: "https://docs.python.org/3/library/stdtypes.html#dict"
source_title: "Dictionaries"
alternatives:
  - option: "list"
    reason: "Ordered sequence, O(n) lookup."
  - option: "collections.defaultdict"
    reason: "Provides default values for missing keys."
  - option: "ordereddict"
    reason: "Preserves insertion order (now default in Python 3.7+)."
---

# Dictionary

## Signature
```python
d = {}  # empty dict
d = {"key": "value"}
d = dict(key="value")
d = dict.fromkeys(["a", "b"], 0)
```

## What It Does
Unordered collection of key-value pairs. Keys must be hashable (immutable). Provides O(1) average time complexity for lookup, insertion, and deletion.

## Use When
- Fast lookups by key.
- Counting occurrences (Counter).
- Caching/memoization.
- JSON-like data structures.

## Examples
```python
user = {"name": "Alice", "age": 30, "active": True}
print(user["name"])  # Alice
```

```python
# All methods
d = {"a": 1, "b": 2}

# Access
d["a"]           # 1
d.get("c", 0)    # 0 (default if missing)
d.setdefault("c", 3)  # 3, sets if missing

# Modify
d["a"] = 10           # update
d.update({"c": 3})     # bulk update
d.pop("b")             # remove and return
del d["a"]             # delete

# Iterate
for key, value in d.items():
    print(key, value)
for key in d.keys():
    print(key)
for value in d.values():
    print(value)
```

```python
# Dict comprehension
squares = {x: x**2 for x in range(5)}  # {0: 0, 1: 1, 2: 4, 3: 9, 4: 16}
```

## Returns
Dictionary object

## Gotchas / Version Notes
- Python 3.7+ guarantees insertion order.
- Keys must be hashable (int, str, tuple, etc.).
- Use dict comprehension for cleaner code.
- dict.keys(), .values(), .items() return views (reflect changes).

## References
- Dict docs: https://docs.python.org/3/library/stdtypes.html#dict
- HOWTO: https://docs.python.org/3/howto/classes.html#dictionarys
