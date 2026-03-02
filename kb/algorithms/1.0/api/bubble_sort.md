---
library: algorithms
version: "1.0.0"
category: api
item: bubble_sort
type: concept
signature: "bubble_sort(array) -> list"
keywords: ["bubble sort", "sorting", "quadratic", "algorithm"]
aliases: ["exchange sort", "basic sort"]
intent: "Sort by repeatedly swapping adjacent out-of-order elements."
last_updated: "2025-03-02"
schema_version: "2.0"
source_url: "https://en.wikipedia.org/wiki/Bubble_sort"
source_title: "Bubble sort"
alternatives:
  - option: "sorted(...) / Timsort"
    reason: "Production-grade stable sort in Python."
  - option: "Merge sort / quicksort / heapsort"
    reason: "Better asymptotic performance for larger datasets."
  - option: "Insertion sort"
    reason: "Simple and often better for small nearly-sorted arrays."
---

# algorithms.bubble_sort

## Signature
```python
def bubble_sort(arr: list[int]) -> list[int]:
    ...
```

## What It Does
Performs repeated passes through the list and swaps adjacent pairs when out of order until no swaps remain.

## Use When
- Educational/demonstration contexts.
- Very small input lists.
- You need an easy-to-understand in-place algorithm.

## Examples
```python
def bubble_sort(arr):
    out = arr[:]
    n = len(out)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if out[j] > out[j + 1]:
                out[j], out[j + 1] = out[j + 1], out[j]
                swapped = True
        if not swapped:
            break
    return out
```

```python
sorted_vals = bubble_sort([5, 1, 4, 2, 8])  # [1, 2, 4, 5, 8]
```

## Alternatives
- `sorted(...)` / Timsort in Python for production usage.
- Merge sort / quicksort / heapsort for larger datasets.
- Insertion sort can be better for nearly sorted small inputs.

## Gotchas / Version Notes
- Time complexity is `O(n^2)` average/worst; poor scalability.
- Not suitable for large arrays in production systems.
- Early-exit optimization improves best case to `O(n)`.

## References
- Bubble sort overview: https://en.wikipedia.org/wiki/Bubble_sort
- Python sorting howto: https://docs.python.org/3/howto/sorting.html
