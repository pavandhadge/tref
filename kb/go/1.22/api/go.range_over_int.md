---
library: go
version: "1.22.0"
category: api
item: go.range_over_int
type: feature
signature: "for i := range n { ... }"
keywords: ["range", "int", "iterate", "loop"]
aliases: ["range int", "integer iteration", "numeric range"]
intent: "Iterate over integers from 0 to n-1 directly in for loops, previously required workaround."
last_updated: "2025-03-02"
schema_version: "2.0"
source_url: "https://go.dev/doc/go1.22#range-int"
source_title: "Go 1.22 Release Notes"
alternatives:
  - option: "traditional for loop"
    reason: "for i := 0; i < n; i++ { }"
  - option: "reflect.Select()"
    reason: "More complex runtime-based iteration."
---

# Range Over Integers

## Signature
```go
for i := range n {
    // i goes from 0 to n-1
}
```

## What It Does
Allows iterating over integers directly in for-range loops. Previously required `for i := 0; i < n; i++` pattern. The range expression must be an integer constant or non-constant.

## Use When
- Simple counting loops.
- Iterating a known number of times.
- Replaces traditional C-style for loops.
- When you need index only, not element from slice.

## Examples
```go
// Print 0 to 9
for i := range 10 {
    fmt.Println(i)
}
```

```go
// Iterate n times with dynamic value
n := getCount()
for i := range n {
    process(i)
}
```

```go
// Works with variables
limit := 5
for i := range limit {
    if i == 3 {
        break
    }
    fmt.Println(i) // prints 0, 1, 2
}
```

```go
// Nested ranges
for i := range 3 {
    for j := range 3 {
        fmt.Println(i, j)
    }
}
```

## Returns
Iterates values 0 to n-1

## Gotchas / Version Notes
- Available in Go 1.22+.
- Negative range values cause panic.
- Range expression evaluated once at start of loop.
- Works with constants and variables.
- If n <= 0, loop body doesn't execute.

## References
- Go 1.22 release: https://go.dev/doc/go1.22#range-int
- For statements: https://go.dev/ref/spec#For_range
