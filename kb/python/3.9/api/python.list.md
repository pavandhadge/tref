---
library: python
version: "3.9.0"
category: api
item: python.list
type: type
signature: "lst = [item1, item2]"
keywords: ["list", "array", "sequence", "collection"]
aliases: ["python list", "array", "dynamic array"]
intent: "Ordered, mutable sequence supporting indexing, slicing, and dynamic resizing for flexible data manipulation."
last_updated: "2025-03-02"
schema_version: "2.0"
source_url: "https://docs.python.org/3/library/stdtypes.html#list"
source_title: "Lists"
alternatives:
  - option: "tuple"
    reason: "Immutable sequence, used for fixed collections."
  - option: "array.array"
    reason: "More memory efficient for homogeneous numeric data."
  - option: "collections.deque"
    reason: "O(1) append/pop from both ends."
---

# List

## Signature
```python
lst = []              # empty list
lst = [1, 2, 3]
lst = list()          # constructor
lst = list("abc")     # ['a', 'b', 'c']
```

## What It Does
Ordered, mutable sequence. Supports indexing, slicing, appending, extending, inserting, removing. Dynamic array implementation with O(1) amortized append.

## Use When
- Ordered collections.
- Stacks and queues (with list operations).
- Iteration and transformation.
- When you need mutable sequence.

## Examples
```python
lst = [1, 2, 3, 4, 5]

# Access
lst[0]      # 1 (first)
lst[-1]     # 5 (last)
lst[1:4]    # [2, 3, 4] (slice)

# Modify
lst.append(6)      # [1,2,3,4,5,6]
lst.insert(0, 0)   # [0,1,2,3,4,5,6]
lst.extend([7,8])  # [0,1,2,3,4,5,6,7,8]
lst.remove(0)      # removes first occurrence
lst.pop()          # removes and returns last

# List comprehension
squares = [x**2 for x in range(10)]
evens = [x for x in range(20) if x % 2 == 0]
```

```python
# Unpack
a, *b, c = [1, 2, 3, 4, 5]  # a=1, b=[2,3,4], c=5

# Sort
lst = [3, 1, 4, 1, 5]
lst.sort()           # in-place, returns None
sorted_lst = sorted(lst)  # returns new list
```

## Returns
List object

## Gotchas / Version Notes
- Use list comprehension over map/filter (more readable).
- lst.sort() is in-place, sorted() returns new.
- Use list.copy() or lst[:] for shallow copy.
- Negative indexing counts from end.

## References
- List docs: https://docs.python.org/3/library/stdtypes.html#list
