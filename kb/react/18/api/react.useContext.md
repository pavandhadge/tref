---
library: react
version: "18.2.0"
category: api
item: react.useContext
type: hook
signature: "const value = useContext(Context)"
keywords: ["useContext", "context", "global", "theme"]
aliases: ["React context", "context API", "global state"]
intent: "Access context value in function components without nesting Consumer components, enabling prop-free data passing."
last_updated: "2025-03-02"
schema_version: "2.0"
source_url: "https://react.dev/reference/react/useContext"
source_title: "useContext Hook Documentation"
alternatives:
  - option: "Context.Consumer"
    reason: "Class component compatible, verbose."
  - option: "Props drilling"
    reason: "Explicit prop passing, no context needed."
---

# useContext

## Signature
```javascript
const value = useContext(Context);
```

## What It Does
Returns context value. Re-renders when context changes. Components using context re-render when provider value changes.

## Use When
- Theme/locale passing.
- User authentication state.
- Global app settings.
- Avoiding prop drilling.

## Examples
```javascript
// Create context
const ThemeContext = React.createContext('light');

// Provide in parent
<ThemeContext.Provider value="dark">
  <App />
</ThemeContext.Provider>

// Consume in component
function Button() {
  const theme = useContext(ThemeContext);
  return <button className={theme}>Click</button>;
}
```

```javascript
// Complex context
const UserContext = React.createContext(null);

function UserProvider({ children }) {
  const [user, setUser] = useState(null);
  
  const login = (userData) => setUser(userData);
  const logout = () => setUser(null);
  
  return (
    <UserContext.Provider value={{ user, login, logout }}>
      {children}
    </UserContext.Provider>
  );
}

// Use
function Profile() {
  const { user, logout } = useContext(UserContext);
  return user ? <button onClick={logout}>Logout</button> : <Login />;
}
```

## Returns
Context value

## Gotchas / Version Notes
- Re-renders on ANY context change.
- Split contexts for performance.
- Memoize context value to prevent.
- Use for global-ish state only.

## References
- useContext docs: https://react.dev/reference/react/useContext
