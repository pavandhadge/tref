---
library: rust
version: "1.74.0"
category: api
item: rust.result
type: type
signature: "enum Result<T, E> { Ok(T), Err(E) }"
keywords: ["result", "error", "handling", "exception"]
aliases: ["Result type", "error handling", "ok err"]
intent: "Represents success (Ok(T)) or failure (Err(E)) of operations, enabling explicit error handling without exceptions."
last_updated: "2025-03-02"
schema_version: "2.0"
source_url: "https://doc.rust-lang.org/std/result/enum.Result.html"
source_title: "Result Enum Documentation"
alternatives:
  - option: "exceptions (other languages)"
    reason: "Not available in Rust, error-prone at runtime."
  - Option<T>
    reason: "For values that may or may not exist, no error details."
---

# Result<T, E>

## Signature
```rust
enum Result<T, E> {
    Ok(T),
    Err(E),
}
```

## What It Does
Represents success with value `Ok(T)` or failure with error `Err(E)`. The standard way to handle recoverable errors in Rust. Forces explicit error handling at compile time.

## Use When
- Operations that can fail (I/O, parsing, network).
- Propagating errors up the call stack.
- Distinguishing between different failure modes.
- Combining multiple fallible operations.

## Examples
```rust
use std::fs::File;

fn read_file(path: &str) -> Result<String, std::io::Error> {
    let mut file = File::open(path)?;  // Propagate error
    let mut contents = String::new();
    file.read_to_string(&mut contents)?;
    Ok(contents)
}

fn main() {
    match read_file("config.txt") {
        Ok(contents) => println!("File: {}", contents),
        Err(e) => eprintln!("Error: {}", e),
    }
}
```

```rust
// Using match
match do_something() {
    Ok(value) => handle_success(value),
    Err(error) => handle_failure(error),
}

// Using unwrap_or
let value = result.unwrap_or(default_value);

// Using map for transformation
let doubled: Result<i32, &str> = Ok(2).map(|x| x * 10);

// Combining multiple results
let final_result = result1.and_then(|a| result2.map(|b| a + b));
```

```rust
// Custom error types
#[derive(Debug)]
enum AppError {
    Io(std::io::Error),
    Parse(std::num::ParseIntError),
    Custom(String),
}
```

## Returns
Result<T, E> enum value

## Gotchas / Version Notes
- Use `?` for error propagation in functions returning Result.
- Implement `From<E>` for automatic error conversion.
- Custom error types often use `thiserror` or `anyhow`.
- `unwrap()` and `expect()` panic on Err - use in tests only.
- Can chain with `and_then()`, `map()`, `or_else()`.

## References
- Result docs: https://doc.rust-lang.org/std/result/enum.Result.html
- Error handling book: https://doc.rust-lang.org/book/ch09-02-recoverable-errors-with-result.html
