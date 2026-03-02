---
library: go
version: "1.20.0"
category: api
item: go.goroutine
type: feature
signature: "go function(args)"
keywords: ["goroutine", "concurrent", "async", "parallel"]
aliases: ["go routine", "concurrency", "lightweight thread"]
intent: "Start a concurrent function execution - a lightweight thread managed by Go runtime for parallel processing."
last_updated: "2025-03-02"
schema_version: "2.0"
source_url: "https://go.dev/doc/effective_go#concurrency"
source_title: "Effective Go - Concurrency"
alternatives:
  - option: "threads (OS)"
    reason: "Heavier weight, managed by OS, more overhead."
  - option: "async/await (other languages)"
    reason: "Different concurrency model in other ecosystems."
  - option: "worker pools"
    reason: "Pre-spawned goroutines for bounded concurrency."
---

# Goroutines

## Signature
```go
go function(args)
go func() { /* code */ }()
```

## What It Does
Creates a lightweight concurrent execution context (goroutine) that runs independently in the same address space. Goroutines are multiplexed onto fewer OS threads, making them extremely efficient.

## Use When
- Handling concurrent I/O operations (HTTP requests, DB queries).
- Background tasks like processing queues.
- Parallel processing of independent tasks.
- Building responsive applications with non-blocking operations.

## Examples
```go
go func() {
    result := heavyComputation()
    ch <- result
}()
```

```go
func fetchURL(url string) string {
    resp, _ := http.Get(url)
    defer resp.Body.Close()
    body, _ := io.ReadAll(resp.Body)
    return string(body)
}

// Concurrent fetches
urls := []string{"https://a.com", "https://b.com", "https://c.com"}
results := make(chan string, len(urls))

for _, url := range urls {
    go func(u string) {
        results <- fetchURL(u)
    }(url)
}

for range urls {
    fmt.Println(<-results)
}
```

```go
// With sync.WaitGroup
var wg sync.WaitGroup
for _, task := range tasks {
    wg.Add(1)
    go func(t Task) {
        defer wg.Done()
        process(t)
    }(task)
}
wg.Wait()
```

## Returns
Starts execution immediately, doesn't block

## Gotchas / Version Notes
- Goroutines are cheap but not free (stack starts at 2KB, grows dynamically).
- No built-in goroutine pooling in standard library.
- Use channels for communication, not shared memory.
- `runtime.Goexit()` can terminate goroutine early.
- Main goroutine exiting ends program.

## References
- Effective Go: https://go.dev/doc/effective_go#concurrency
- Go memory model: https://go.dev/ref/mem
