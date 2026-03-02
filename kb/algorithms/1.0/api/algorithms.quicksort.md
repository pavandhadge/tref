---
library: algorithms
version: "1.0.0"
category: api
item: algorithms.quicksort
type: algorithm
signature: "def quicksort(arr):"
keywords: ["quicksort", "sort", "divide and conquer", "partition"]
aliases: ["quick sort", "partition-exchange sort"]
intent: "Efficiently sort an array by selecting a pivot element and partitioning the array around it, then recursively sorting the partitions."
last_updated: "2025-03-02"
schema_version: "2.0"
source_url: "https://en.wikipedia.org/wiki/Quicksort"
source_title: "Quicksort Algorithm"
alternatives:
  - option: "merge sort"
    reason: "O(n log n) guaranteed, stable, but uses O(n) extra space."
  - option: "heap sort"
    reason: "O(n log n) in-place but not stable."
  - option: "timsort"
    reason: "Python's built-in sort - hybrid O(n) best case."
---

# Quicksort

## Signature
```python
def quicksort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quicksort(left) + middle + quicksort(right)
```

## What It Does
Sorts elements by choosing a pivot, partitioning into elements less than/equal to/greater than pivot, then recursively sorting partitions. Average O(n log n) time complexity.

## Use When
- General-purpose sorting.
- In-memory sorting of arrays.
- Need good average performance.
- Space is limited (O(log n) stack).

## Examples
```python
arr = [3, 6, 8, 10, 1, 2, 1]
print(quicksort(arr))  # [1, 1, 2, 3, 6, 8, 10]
```

```python
# In-place quicksort with Lomuto partition
def quicksort_inplace(arr, low=0, high=None):
    if high is None:
        high = len(arr) - 1
    if low < high:
        pi = partition(arr, low, high)
        quicksort_inplace(arr, low, pi - 1)
        quicksort_inplace(arr, pi + 1, high)
    return arr

def partition(arr, low, high):
    pivot = arr[high]
    i = low - 1
    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1
```

## Returns
Sorted array

## Complexity
- Time: O(n log n) average, O(n²) worst
- Space: O(log n) stack

## Gotchas / Version Notes
- Unstable sort (equal elements may change order).
- Worst case with sorted input and bad pivot choice.
- Randomize pivot or use median-of-three.
- Use built-in sorted() in production.

## References
- Wikipedia: https://en.wikipedia.org/wiki/Quicksort
- Visualizer: https://www.geeksforgeeks.org/quick-sort/
