---
library: redis
version: "6.2.0"
category: api
item: redis.set
type: command
signature: "SET key value [EX seconds] [PX milliseconds] [NX|XX] [KEEPTTL]"
keywords: ["set", "store", "cache", "key-value"]
aliases: ["redis set", "set key", "store value"]
intent: "Set a string value in Redis with optional expiration and conditions for atomic key assignment."
last_updated: "2025-03-02"
schema_version: "2.0"
source_url: "https://redis.io/commands/set/"
source_title: "SET Command Documentation"
alternatives:
  - option: "MSET"
    reason: "Set multiple keys at once (non-atomic)."
  - option: "HSET"
    reason: "Set field in hash for structured data."
  - option: "SETEX"
    reason: "Set with expiration (older syntax)."
---

# SET

## Signature
```redis
SET key value [EX seconds] [PX milliseconds] [NX|XX] [KEEPTTL]
```

## Parameters
- key: The key to set.
- value: The string value to store.
- EX: Expire time in seconds.
- PX: Expire time in milliseconds.
- NX: Only set if key does not exist.
- XX: Only set if key already exists.
- KEEPTTL: Keep existing TTL (for XX operation on existing key).

## What It Does
Sets a string value in Redis. Supports atomic conditional sets (NX/XX) and automatic expiration (EX/PX). Overwrites existing value unless XX flag is used.

## Use When
- Storing simple key-value data.
- Implementing caching with expiration.
- Distributed locking with NX.
- Session storage with TTL.

## Examples
```redis
SET user:1 "John"
```

```redis
SET session:abc123 "data" EX 3600
```

```redis
SET lock:resource "" NX EX 10
```

```redis
SET counter 0 XX
```

```redis
SET config "value" KEEPTTL
```

## Returns
OK if set, nil if conditions not met

## Gotchas / Version Notes
- NX/XX are mutually exclusive.
- Use KEEPTTL to preserve TTL on update (Redis 6.2+).
- Values can be up to 512MB.
- Use for simple strings; use HSET for objects.
- SET with XX + KEEPTTL is atomic.

## References
- SET docs: https://redis.io/commands/set/
- Keyspace: https://redis.io/docs/data-types/strings/
