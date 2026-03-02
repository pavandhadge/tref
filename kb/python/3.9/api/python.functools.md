---
library: python
version: "3.9.0"
category: api
item: python.functools
type: module
signature: "@lru_cache, partial(func, *args), reduce(func, iterable)"
keywords: ["functools", "cache", "higher order", "decorator"]
aliases: ["memoization", "function tools", "partial application"]
intent: "Higher-order functions and operations on callable objects, including caching, partial application, and function wrapping."
last_updated: "2025-03-02"
schema_version: "2.0"
source_url: "https://docs.python.org/3/library/functools.html"
source_title: "functools Module"
alternatives:
  - option: "custom caching"
    reason: "More control but more code to write."
  - option: "cachetools"
    reason: "Additional cache algorithms (LRU, TTL)."
---

# functools

## Signature
```python
import functools

@functools.lru_cache(maxsize=128)
def expensive_function(x):
    ...

functools.partial(func, *args, **kwargs)
functools.reduce(function, iterable, initializer)
```

## What It Does
Module for higher-order functions: functions that operate on or return functions. Provides caching, partial application, function composition, and method decorators.

## Use When
- Memoization/caching expensive computations.
- Creating specialized functions from general ones.
- Functional programming patterns.
- Method decorators (singledispatch).

## Examples
```python
# lru_cache - memoization decorator
@functools.lru_cache(maxsize=128)
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

fibonacci.cache_info()  # CacheInfo(hits=..., misses=...)
fibonacci.cache_clear()
```

```python
# partial - create function with some args fixed
from functools import partial

def power(base, exponent):
    return base ** exponent

square = partial(power, exponent=2)
cube = partial(power, exponent=3)

square(5)   # 25
cube(5)     # 125
```

```python
# reduce - accumulate values
from functools import reduce

reduce(lambda x, y: x + y, [1, 2, 3, 4])  # 10
reduce(lambda x, y: x * y, [1, 2, 3, 4])  # 24

# With initializer
reduce(lambda x, y: x + y, [], 100)  # 100
```

```python
# singledispatch - function overloading
@functools.singledispatch
def process(data):
    print(f"Default: {data}")

@process.register(int)
def _(data):
    print(f"Integer: {data * 2}")

@process.register(str)
def _(data):
    print(f"String: {data.upper()}")
```

```python
# wraps - preserve function metadata in decorators
def my_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print("Before")
        return func(*args, **kwargs)
    return wrapper
```

## Returns
Various (decorators, partial objects, etc.)

## Gotchas / Version Notes
- lru_cache requires hashable arguments.
- reduce replaced by sum/product in many cases.
- wraps required for proper introspection.
- Total ordering available via @total_ordering.

## References
- functools docs: https://docs.python.org/3/library/functools.html
