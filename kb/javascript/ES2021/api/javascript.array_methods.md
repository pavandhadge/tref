---
library: javascript
version: "ES2021"
category: api
item: javascript.array_methods
type: api
signature: "[].map(), filter(), reduce(), find(), some(), every()"
keywords: ["array", "map", "filter", "reduce", "iteration"]
aliases: ["array methods", "functional programming", "array iteration"]
intent: "Transform, filter, and aggregate arrays using functional programming methods for cleaner, more expressive code."
last_updated: "2025-03-02"
schema_version: "2.0"
source_url: "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array"
source_title: "Array Documentation"
alternatives:
  - option: "for loop"
    reason: "More verbose but more control."
  - option: "lodash methods"
    reason: "Additional utilities beyond built-in."
---

# Array Methods

## Signature
```javascript
arr.map((item, index, array) => newValue)
arr.filter((item, index, array) => boolean)
arr.reduce((acc, item, index, array) => newAcc, initial)
arr.find((item, index, array) => boolean)
arr.some((item, index, array) => boolean)
arr.every((item, index, array) => boolean)
```

## What It Does
Functional methods for transforming, filtering, and aggregating arrays. Each method takes callback with item, index, array parameters.

## Use When
- Transforming data.
- Filtering collections.
- Computing aggregates.
- Finding specific items.

## Examples
```javascript
// map - transform each element
const numbers = [1, 2, 3, 4];
const doubled = numbers.map(n => n * 2);  // [2, 4, 6, 8]
```

```javascript
// filter - keep matching elements
const evens = numbers.filter(n => n % 2 === 0);  // [2, 4]
```

```javascript
// reduce - aggregate to single value
const sum = numbers.reduce((acc, n) => acc + n, 0);  // 10

// reduce with object
const counts = ['a', 'b', 'a'].reduce((acc, val) => {
  acc[val] = (acc[val] || 0) + 1;
  return acc;
}, {});  // {a: 2, b: 1}
```

```javascript
// find - first matching element
const firstEven = numbers.find(n => n % 2 === 0);  // 2
```

```javascript
// some - any match
const hasEven = numbers.some(n => n % 2 === 0);  // true

// every - all match
const allPositive = numbers.every(n => n > 0);  // true
```

```javascript
// Chaining
const result = numbers
  .filter(n => n > 2)
  .map(n => n * 10);  // [30, 40]
```

## Returns
Array (map, filter), value (reduce, find), boolean (some, every)

## Gotchas / Version Notes
- Don't mutate original array in callbacks.
- Use flatMap for map + flatten.
- findIndex returns index, -1 if not found.
- includes for simple value checking.

## References
- MDN Array: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array
