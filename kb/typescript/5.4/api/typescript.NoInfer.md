---
library: typescript
version: "5.4.0"
category: api
item: typescript.NoInfer
type: utility_type
signature: "NoInfer<T>"
keywords: ["NoInfer", "utility types", "type inference", " generics"]
aliases: ["prevent inference", "type parameters"]
intent: "Prevent TypeScript from inferring types within a specific position in generic expressions."
last_updated: "2025-03-02"
schema_version: "2.0"
source_url: "https://www.typescriptlang.org/docs/handbook/release-notes/typescript-5-4.html"
source_title: "TypeScript 5.4 Release Notes"
alternatives:
  - option: "explicit type parameters"
    reason: "Manually specify type arguments to avoid inference."
  - option: "const assertions"
    reason: "Preserve literal types throughout an object."
---

# NoInfer

## Signature
```typescript
type NoInfer<T> = T & { __spirit?: never };
```

## What It Does
Prevents TypeScript from inferring types at specific positions in generic function calls. Useful when you want to force users to provide explicit types or when you want to preserve literal types.

## Use When
- Creating generic functions where some type parameters should be explicit.
- Preventing unwanted type widening in generic constraints.
- When you want the caller to specify certain type arguments.

## Examples
```typescript
function createPair<T, U>(a: NoInfer<T>, b: NoInfer<U>): [T, U] {
  return [a, b];
}

// T is inferred from first arg, U must be explicit
const pair = createPair("hello", 42);
// Error: Expected 2 type arguments
const pair2 = createPair<string, number>("hello", 42);
```

```typescript
function process<T extends NoInfer<string>>(
  value: T,
  options: { timeout?: number }
): void {}

// Must provide string literal for T
process("hello", { timeout: 1000 });
```

```typescript
// Using NoInfer to preserve literal types
const config = {
  env: "production" as const,
  port: 8080,
} satisfies { env: NoInfer<"production" | "development">; port: number };
```

## Returns
A type that behaves like T but blocks inference

## Gotchas / Version Notes
- Available in TypeScript 5.4+.
- Works by adding a property that TypeScript cannot infer.
- Often combined with constraints for better type safety.
- Useful for library authors to enforce explicit type parameters.

## References
- TypeScript 5.4 Release Notes: https://www.typescriptlang.org/docs/handbook/release-notes/typescript-5-4.html
