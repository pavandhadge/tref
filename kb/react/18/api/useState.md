---
library: react
version: "18.0.0"
category: api
item: useState
type: function
signature: "useState(initialState) -> [state, setState]"
keywords: ["react", "useState", "state", "hooks", "component state"]
aliases: ["set state in react", "react state hook", "component local state"]
intent: "Store and update local component state in function components."
last_updated: "2025-03-02"
schema_version: "2.0"
source_url: "https://react.dev/reference/react/useState"
source_title: "React useState"
---

# react.useState

## Signature
```python
const [state, setState] = useState(initialState)
```

## What It Does
Creates local state for a function component and returns the current value plus a setter that schedules re-render.

## Use When
- A component needs local mutable UI state.
- You need user-input state, toggles, counters, loading flags.
- State is component-scoped (not global/shared store).

## Examples
```python
import { useState } from "react";

function Counter() {
  const [count, setCount] = useState(0);
  return <button onClick={() => setCount(c => c + 1)}>{count}</button>;
}
```

```python
function Form() {
  const [form, setForm] = useState({ name: "", email: "" });
  const onChange = e => setForm(prev => ({ ...prev, [e.target.name]: e.target.value }));
  return <input name="name" value={form.name} onChange={onChange} />;
}
```

## Alternatives
- `useReducer` for complex state transitions.
- External stores (`Redux`, `Zustand`) for app-wide shared state.
- `useRef` for mutable values that should not trigger re-renders.

## Gotchas / Version Notes
- State updates are asynchronous and may be batched.
- Use functional updates (`setX(prev => ...)`) when next state depends on previous.
- Do not mutate state objects/arrays directly.

## References
- React useState docs: https://react.dev/reference/react/useState
- Managing state in React: https://react.dev/learn/managing-state
