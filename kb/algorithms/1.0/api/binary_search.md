---
library: algorithms
version: "1.0.0"
category: api
item: binary_search
type: concept
signature: "binary_search(sorted_array, target) -> int"
keywords: ["binary search", "sorted array", "log n", "algorithm"]
aliases: ["bsearch", "divide and conquer search"]
intent: "Find a target in a sorted sequence in logarithmic time."
last_updated: "2025-03-02"
schema_version: "2.0"
source_url: "https://en.wikipedia.org/wiki/Binary_search_algorithm"
source_title: "Binary search algorithm"
alternatives:
  - option: "Linear search"
    reason: "Use for unsorted or very small lists."
  - option: "Hash map / set lookup"
    reason: "Use near O(1) membership when extra memory is acceptable."
  - option: "bisect module"
    reason: "Use built-in insertion-point binary operations in Python."
---

# algorithms.binary_search

## Signature
```python
def binary_search(arr: list[int], target: int) -> int:
    ...
```

## What It Does
Repeatedly halves the search interval of a sorted array until the target is found or interval is empty.

## Use When
- Input is sorted.
- You need better than linear lookup performance.
- You can handle index-based lookup.

## Examples
```python
def binary_search(arr, target):
    lo, hi = 0, len(arr) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if arr[mid] == target:
            return mid
        if arr[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1
```

```python
nums = [3, 8, 12, 19, 24, 31]
idx = binary_search(nums, 19)  # 3
```

## Alternatives
- Linear search for unsorted or tiny arrays.
- Hash map/set lookup when preprocessing and memory are acceptable.
- `bisect` module for insertion-point based binary operations in Python.

## Gotchas / Version Notes
- Requires sorted input; wrong order yields wrong results.
- Be explicit about duplicate handling (first/last any-match).
- Time complexity `O(log n)`, space `O(1)` iterative.

## References
- Binary search overview: https://en.wikipedia.org/wiki/Binary_search_algorithm
- Python bisect docs: https://docs.python.org/3/library/bisect.html
