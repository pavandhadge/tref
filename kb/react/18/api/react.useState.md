---
library: react
version: "18.2.0"
category: api
item: react.useState
type: hook
signature: "const [state, setState] = useState(initialState)"
keywords: ["useState", "state", "hook", "reactive"]
aliases: ["React state", "component state", "set state"]
intent: "Add state management to functional components, returning a stateful value and a function to update it."
last_updated: "2025-03-02"
schema_version: "2.0"
source_url: "https://react.dev/reference/react/useState"
source_title: "useState Hook Documentation"
alternatives:
  - option: "useReducer"
    reason: "Complex state logic with multiple sub-values or when next state depends on previous."
  - option: "Context API"
    reason: "Share state across many components without prop drilling."
  - option: "External state (Redux, Zustand)"
    reason: "Global state management for large applications."
---

# useState

## Signature
```typescript
const [state, setState] = useState(initialState);
const [state, setState] = useState(() => initialExpensiveValue);
```

## Parameters
- initialState: Initial value (or function that returns initial value for lazy initialization).

## Returns
- state: Current state value.
- setState: Function to update state (can take new value or function).

## What It Does
Declares a state variable that persists between renders. Calling setState triggers re-render with updated value. Supports lazy initialization for expensive computations.

## Use When
- Storing component-local UI state.
- Managing simple state logic without external libraries.
- Triggering re-renders on data changes.

## Examples
```jsx
function Counter() {
  const [count, setCount] = useState(0);
  return (
    <button onClick={() => setCount(c => c + 1)}>
      Count: {count}
    </button>
  );
}
```

```jsx
function Form() {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  return (
    <form>
      <input value={name} onChange={e => setName(e.target.value)} />
      <input value={email} onChange={e => setEmail(e.target.value)} />
    </form>
  );
}
```

```jsx
// Lazy initialization
const [data, setData] = useState(() => {
  const saved = localStorage.getItem("data");
  return saved ? JSON.parse(saved) : null;
});
```

## Returns
`[state, setState]` tuple

## Gotchas / Version Notes
- State updates are batched in React 18.
- Objects must be merged: `setState(prev => ({...prev, ...updates})`.
- Use functional updates to avoid stale closures.
- Initial state lazy evaluation only runs once.

## References
- useState docs: https://react.dev/reference/react/useState
- State and lifecycle: https://react.dev/learn/state-a-components-memory
