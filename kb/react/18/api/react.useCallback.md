---
library: react
version: "18.2.0"
category: api
item: react.useCallback
type: hook
signature: "const fn = useCallback(() => {}, deps)"
keywords: ["useCallback", "callback", "stable", "reference"]
aliases: ["memoize function", "stable callback", "cached function"]
intent: "Memoize callback function, returning stable reference that only changes when dependencies change, preventing child re-renders."
last_updated: "2025-03-02"
schema_version: "2.0"
source_url: "https://react.dev/reference/react/useCallback"
source_title: "useCallback Hook Documentation"
alternatives:
  - option: "useMemo"
    reason: "For memoizing values, not functions."
  - option: "useReducer"
    reason: "For complex state logic."
---

# useCallback

## Signature
```javascript
const fn = useCallback(() => doSomething(a, b), [a, b]);
const fn = useCallback(event => handle(event), [handle]);
```

## Parameters
- callback: Function to memoize.
- deps: Array of values that trigger recreation.

## What It Does
Returns memoized callback. Only creates new function when dependencies change. Use when passing callbacks to optimized child components.

## Use When
- Passing callbacks to memoized children.
- Event handlers in dependency arrays.
- Optimizing with React.memo.
- Avoiding stale closures.

## Examples
```javascript
function Parent() {
  const [count, setCount] = useState(0);
  
  const handleClick = useCallback((id) => {
    console.log("Clicked", id, count);
  }, [count]);  // Recreated when count changes
  
  return <MemoizedChild onClick={handleClick} />;
}
```

```javascript
// With event handlers
function Form() {
  const handleSubmit = useCallback((e) => {
    e.preventDefault();
    // submit logic
  }, []);  // Stable reference
  
  return <form onSubmit={handleSubmit} />;
}
```

```javascript
// Use with useReducer
const [state, dispatch] = useReducer(reducer, initialState);
const lazyInit = useCallback(() => initialState, []);
```

## Returns
Memoized callback function

## Gotchas / Version Notes
- Not needed for most callbacks.
- Only for prop to memoized component.
- Wraps automatically in deps lint rule.
- Prefer inline functions when simple.
- Dependencies must be complete.

## References
- useCallback docs: https://react.dev/reference/react/useCallback
