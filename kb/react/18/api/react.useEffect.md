---
library: react
version: "18.2.0"
category: api
item: react.useEffect
type: hook
signature: "useEffect(effect, deps)"
keywords: ["useEffect", "effect", "side effect", "lifecycle"]
aliases: ["React effect", "side effects", "componentDidMount"]
intent: "Perform side effects in function components: data fetching, subscriptions, DOM manipulation, cleanup."
last_updated: "2025-03-02"
schema_version: "2.0"
source_url: "https://react.dev/reference/react/useEffect"
source_title: "useEffect Hook Documentation"
alternatives:
  - option: "useLayoutEffect"
    reason: "Synchronous effect before browser paint."
  - option: "useTransition"
    reason: "For non-blocking state updates."
---

# useEffect

## Signature
```javascript
useEffect(() => {
  // effect code
  return () => cleanup;  // optional cleanup
}, [deps]);  // dependency array
```

## Parameters
- effect: Function containing side effect logic.
- deps: Array of dependencies that trigger effect.

## What It Does
Runs after render. Executes effect function and optionally returns cleanup function. Runs when dependencies change. Cleanup runs before re-run.

## Use When
- Data fetching (API calls).
- Subscriptions (WebSocket, event listeners).
- DOM manipulation.
- Timer setup.

## Examples
```jsx
// Basic effect - runs after every render
useEffect(() => {
  console.log("Component rendered");
});
```

```jsx
// Effect with cleanup - runs once on mount
useEffect(() => {
  const subscription = api.subscribe(id, data => {
    setData(data);
  });
  
  return () => subscription.unsubscribe();
}, [id]);
```

```jsx
// Fetch data
useEffect(async () => {
  const res = await fetch(`/api/users/${id}`);
  const data = await res.json();
  setUser(data);
}, [id]);
```

```jsx
// Run only on mount (empty deps)
useEffect(() => {
  const analytics = initAnalytics();
  return () => analytics.destroy();
}, []);
```

```jsx
// Document title
useEffect(() => {
  document.title = `${count} items`;
}, [count]);
```

## Returns
undefined

## Gotchas / Version Notes
- Runs after render, before paint.
- Empty deps = mount only.
- Return function for cleanup.
- Don't update state with stale closures.
- React 18: effects run twice in dev.

## References
- useEffect docs: https://react.dev/reference/react/useEffect
