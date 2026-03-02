---
library: algorithms
version: "1.0.0"
category: api
item: algorithms.binary_search
type: algorithm
signature: "def binary_search(arr, target):"
keywords: ["binary search", "search", "sorted array", "divide and conquer"]
aliases: ["binary search algorithm", "logarithmic search", "half-interval search"]
intent: "Efficiently find the position of a target value in a sorted array by repeatedly dividing the search interval in half."
last_updated: "2025-03-02"
schema_version: "2.0"
source_url: "https://en.wikipedia.org/wiki/Binary_search_algorithm"
source_title: "Binary Search Algorithm"
alternatives:
  - option: "linear search"
    reason: "O(n) - simpler but slower for large arrays."
  - option: "hash table lookup"
    reason: "O(1) average but requires extra space."
---

# Binary Search

## Signature
```python
def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1
```

## What It Does
Searches a sorted array by repeatedly dividing the search interval in half. Compares target with middle element; if equal, found; if less, search left half; if greater, search right half.

## Use When
- Searching in sorted data.
- Need O(log n) time complexity.
- Dictionary lookups in sorted keys.
- Finding insertion points.

## Examples
```python
arr = [1, 3, 5, 7, 9, 11, 13, 15]
print(binary_search(arr, 7))  # 3
print(binary_search(arr, 6))  # -1 (not found)
```

```python
# Recursive version
def binary_search_recursive(arr, target, left, right):
    if left > right:
        return -1
    mid = (left + right) // 2
    if arr[mid] == target:
        return mid
    elif arr[mid] < target:
        return binary_search_recursive(arr, target, mid + 1, right)
    else:
        return binary_search_recursive(arr, target, left, mid - 1)
```

## Returns
Index of target if found, -1 otherwise

## Complexity
- Time: O(log n)
- Space: O(1) iterative, O(log n) recursive

## Gotchas / Version Notes
- Array must be sorted.
- Works only on random-access structures.
- Beware of integer overflow in other languages.
- Use bisect module in Python for built-in.

## References
- Wikipedia: https://en.wikipedia.org/wiki/Binary_search_algorithm
- Python bisect: https://docs.python.org/3/library/bisect.html
