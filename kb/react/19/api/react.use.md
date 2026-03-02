---
library: react
version: "19.0.0"
category: api
item: react.use
type: hook
signature: "const value = use(resource)"
keywords: ["use", "promise", "async", "resource"]
aliases: ["React use", "async data", "promise resolution"]
intent: "Read the value or result of a promise or context directly in components, enabling async data handling in render."
last_updated: "2025-03-02"
schema_version: "2.0"
source_url: "https://react.dev/reference/react/use"
source_title: "use Hook Documentation"
alternatives:
  - option: "useEffect + useState"
    reason: "Traditional pattern for fetching data with loading/error states."
  - option: "React Query / SWR"
    reason: "Production data fetching with caching and synchronization."
  - option: "Suspense"
    reason: "For component-level async rendering with boundaries."
---

# use

## Signature
```typescript
const value = use(promise);
const value = use(context);
```

## What It Does
A new primitive that unwraps Promises and Context directly in components. Provides a simpler alternative to useEffect for data fetching while integrating with Suspense and error boundaries.

## Use When
- Fetching async data directly in components.
- Consuming React Context without useContext.
- Handling Promise results in render.

## Examples
```jsx
async function getUser(id) {
  const res = await fetch(`/api/users/${id}`);
  return res.json();
}

function UserProfile({ userId }) {
  const user = use(getUser(userId));
  return <h1>{user.name}</h1>;
}
```

```jsx
function Message() {
  const message = use(MessageContext);
  return <p>{message.text}</p>;
}
```

```jsx
// With error handling
function UserData({ userId }) {
  const user = use(fetchUser(userId));
  if (user.error) return <Error />;
  return <div>{user.name}</div>;
}
```

## Returns
Resolved value of Promise or Context

## Gotchas / Version Notes
- Available in React 19+.
- Promises are automatically caught by nearest Suspense boundary.
- Must wrap in try/catch for error handling.
- Works with both Promise and Context.
- Not a hook - can be called conditionally in some cases.

## References
- use docs: https://react.dev/reference/react/use
- React 19 blog: https://react.dev/blog/2024/12/05/react-19
