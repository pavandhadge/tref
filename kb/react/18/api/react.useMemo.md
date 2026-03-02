---
library: react
version: "18.2.0"
category: api
item: react.useMemo
type: hook
signature: "const value = useMemo(() => compute(), deps)"
keywords: ["useMemo", "memo", "cache", "performance"]
aliases: ["memoize", "cached value", "computed value"]
intent: "Memoize expensive computations, returning cached value that only recomputes when dependencies change."
last_updated: "2025-03-02"
schema_version: "2.0"
source_url: "https://react.dev/reference/react/useMemo"
source_title: "useMemo Hook Documentation"
alternatives:
  - option: "useCallback"
    reason: "For caching functions, not values."
  - option: "React.memo"
    reason: "For component-level memoization."
---

# useMemo

## Signature
```javascript
const value = useMemo(() => expensiveCalculation(a, b), [a, b]);
```

## Parameters
- factory: Function that computes value.
- deps: Array of values that trigger recomputation.

## What It Does
Caches computed value. Only recalculates when dependencies change. Use for expensive computations to avoid unnecessary recalculations.

## Use When
- Expensive calculations.
- Object/array creation passed to child.
- Filtering/sorting large lists.
- Preventing unnecessary re-computations.

## Examples
```javascript
function ExpensiveComponent({ items, filter }) {
  const filtered = useMemo(() => {
    return items.filter(item => item.name.includes(filter));
  }, [items, filter]);
  
  return <List items={filtered} />;
}
```

```javascript
// With complex computation
const stats = useMemo(() => {
  return {
    total: data.reduce((sum, x) => sum + x, 0),
    average: data.reduce((sum, x) => sum + x, 0) / data.length,
    max: Math.max(...data),
  };
}, [data]);
```

```javascript
// Prevent object recreation
const options = useMemo(() => ({
  enableTooltip: true,
  animationDuration: 300,
}), []);  // Empty deps - never changes
```

## Returns
Memoized value

## Gotchas / Version Notes
- Only for expensive ops.
- Don't use for every value.
- Dependencies must include all used values.
- Runs on every render (dev mode).
- Empty deps = computed once.

## References
- useMemo docs: https://react.dev/reference/react/useMemo
