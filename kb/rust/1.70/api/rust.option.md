---
library: rust
version: "1.70.0"
category: api
item: rust.option
type: type
signature: "enum Option<T> { Some(T), None }"
keywords: ["option", "optional", "null", "maybe"]
aliases: ["Option type", "optional value", "maybe monad"]
intent: "Represents an optional value - either Some(T) containing a value or None representing absence, eliminating null pointer exceptions."
last_updated: "2025-03-02"
schema_version: "2.0"
source_url: "https://doc.rust-lang.org/std/option/enum.Option.html"
source_title: "Option Enum Documentation"
alternatives:
  - option: "null (other languages)"
    reason: "Runtime error prone, no compile-time checking."
  - option: "Result<T, E>"
    reason: "For operations that can fail with error information."
---

# Option<T>

## Signature
```rust
enum Option<T> {
    Some(T),
    None,
}
```

## What It Doe
Encapsulates optional values. Either contains a value (`Some(T)`) or nothing (`None`). Forces handling of the absent case at compile time, eliminating null reference errors.

## Use When
- Return value might not exist (e.g., find operations).
- Input parameter is optional.
- Handling missing configuration values.
- Safe optional chaining without null checks.

## Examples
```rust
fn find_user(id: u32) -> Option<User> {
    // Returns Some(user) if found, None if not
    users.iter().find(|u| u.id == id).cloned()
}

fn main() {
    let user = find_user(1);
    match user {
        Some(u) => println!("Found: {}", u.name),
        None => println!("User not found"),
    }
}
```

```rust
// Using if let for concise handling
if let Some(name) = get_name() {
    println!("Hello, {}!", name);
}
```

```rust
// Chaining with and_then
let config = load_config()
    .and_then(|c| c.database)
    .and_then(|db| db.host);

// With unwrap_or default
let value = get_optional().unwrap_or(default_value);
```

```rust
// Question mark operator
fn get_nested(config: &Config) -> Option<String> {
    let db = config.database.as_ref()?;
    Some(db.host.clone())
}
```

## Returns
Option<T> enum value

## Gotchas / Version Notes
- Never use `unwrap()` in production code.
- `?` operator propagates None values.
- Can contain any type, including references.
- Use `is_some()`, `is_none()` for boolean checks.
- Methods: `map()`, `and_then()`, `unwrap_or()`, `or_else()`.

## References
- Option docs: https://doc.rust-lang.org/std/option/enum.Option.html
- Error handling: https://doc.rust-lang.org/book/ch09-02-recoverable-errors-with-result.html
