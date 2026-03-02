---
library: redis
version: "7.2.0"
category: api
item: redis.json_set
type: command
signature: "JSON.SET key path json [NX|XX]"
keywords: ["json", "document", "nosql", "cache"]
aliases: ["redis json", "store json", "document cache"]
intent: "Store, update, or retrieve JSON documents in Redis with JSONPath support for partial updates."
last_updated: "2025-03-02"
schema_version: "2.0"
source_url: "https://redis.io/commands/json.set/"
source_title: "JSON.SET Documentation"
alternatives:
  - option: "SET (string)"
    reason: "Simple strings, no JSON operations."
  - option: "HSET"
    reason: "Hash for flat key-value, no nested support."
  - option: "Hash + serialize"
    reason: "Manual JSON serialization to string."
---

# JSON.SET

## Signature
```redis
JSON.SET key path value [NX | XX]
```

## What It Does
Stores a JSON value at the specified path in a Redis key. Supports JSONPath for partial updates and nested documents. Requires Redis Stack (Redis 7.2+).

## Use When
- Storing structured JSON data.
- Partial document updates.
- Need JSON operations (JSON.GET, JSON.ARRAPPEND, etc.).
- Document caching for APIs.

## Examples
```redis
JSON.SET user:1 $ '{"name":"John","age":30}'
```

```redis
JSON.SET config $ '{"debug":true,"version":"1.0"}'
```

```redis
JSON.SET product:1 $.price 29.99
```

```redis
JSON.SET user:1 $.tags '["vip","premium"]' NX
```

```redis
JSON.GET user:1 $
```

## Returns
OK on success, nil if conditions not met

## Gotchas / Version Notes
- Requires Redis Stack module.
- Use `$` for root path.
- JSONPath uses $. prefix.
- Use NX for insert-only (key must not exist).
- Use XX for update-only (key must exist).

## References
- JSON.SET: https://redis.io/commands/json.set/
- Redis Stack: https://redis.io/docs/stack/
