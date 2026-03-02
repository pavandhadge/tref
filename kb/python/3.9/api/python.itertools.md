---
library: python
version: "3.9.0"
category: api
item: python.itertools
type: module
signature: "itertools.chain(*iterables), itertools.product(*iterables)"
keywords: ["itertools", "iterator", "combinations", "permutations"]
aliases: ["iterator utilities", "combinations", "infinite iterators"]
intent: "Fast, memory-efficient iterator functions for working with iterables, including combinations, permutations, and infinite counters."
last_updated: "2025-03-02"
schema_version: "2.0"
source_url: "https://docs.python.org/3/library/itertools.html"
source_title: "itertools Module"
alternatives:
  - option: "list comprehension"
    reason: "Creates full list in memory, less efficient."
  - option: "numpy"
    reason: "Numerical operations on arrays."
  - option: "more-itertools"
    reason: "Extended itertools functionality."
---

# itertools

## Signature
```python
import itertools

# Infinite
count(start), cycle(iterable), repeat(elem, n)

# Finite  
chain(*iterables), islice(iterable, stop), takewhile(pred, iterable)
dropwhile(pred, iterable), groupby(iterable), tee(iterable, n)
```

## What It Does
Module providing fast, memory-efficient iterator building blocks. Functions return iterators rather than lists, enabling processing of large streams.

## Use When
- Generating combinations/permutations.
- Processing large files lazily.
- Iterating over multiple sequences.
- Functional programming patterns.

## Examples
```python
# chain - connect multiple iterables
list(itertools.chain([1, 2], [3, 4], [5]))  # [1, 2, 3, 4, 5]
list(itertools.chain.from_iterable([[1,2], [3,4]])  # [1, 2, 3, 4]
```

```python
# islice - slice iterator
list(itertools.islice(range(10), 2, 8, 2))  # [2, 4, 6]
```

```python
# product - Cartesian product
list(itertools.product([1, 2], ["a", "b"]))  
# [(1,'a'), (1,'b'), (2,'a'), (2,'b')]

list(itertools.product("AB", repeat=2))  
# [('A','A'), ('A','B'), ('B','A'), ('B','B')]
```

```python
# permutations and combinations
list(itertools.permutations("ABC", 2))  
# [('A','B'), ('A','C'), ('B','A'), ('B','C'), ('C','A'), ('C','B')]

list(itertools.combinations("ABC", 2))  
# [('A','B'), ('A','C'), ('B','C')]

list(itertools.combinations_with_replacement("AB", 2))  
# [('A','A'), ('A','B'), ('B','B')]
```

```python
# groupby - group consecutive elements
for key, group in itertools.groupby("aaabbbcca"):
    print(key, list(group))
# a ['a', 'a', 'a']
# b ['b', 'b', 'b']
# c ['c', 'c']
# a ['a']
```

```python
# cycle and repeat
counter = itertools.count(start=1)
next(counter)  # 1
next(counter)  # 2

list(itertools.repeat(5, 3))  # [5, 5, 5]
```

## Returns
Iterator objects

## Gotchas / Version Notes
- Returns iterators, not lists.
- groupby requires sorted data for proper grouping.
- tee creates n independent iterators (memory).
- Use islice for memory-efficient slicing.

## References
- itertools docs: https://docs.python.org/3/library/itertools.html
