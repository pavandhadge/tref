---
library: typescript
version: "4.9.0"
category: api
item: typescript.satisfies
type: operator
signature: "expr satisfies Type"
keywords: ["satisfies", "type", "narrowing", "validation"]
aliases: ["satisfies operator", "type satisfaction"]
intent: "Validate that an expression matches a type without changing the inferred type."
last_updated: "2025-03-02"
schema_version: "2.0"
source_url: "https://www.typescriptlang.org/docs/handbook/release-notes/typescript-4-9.html"
source_title: "TypeScript 4.9 Release Notes"
alternatives:
  - option: "type annotations"
    reason: "Explicitly declares a type but may widen the type unnecessarily."
  - option: "type guards"
    reason: "Narrow types within conditional blocks."
---

# satisfies

## Signature
```typescript
expr satisfies Type
```

## What It Does
Checks that an expression is of a specified type while preserving the expression's original type for inference. Unlike type annotations, `satisfies` doesn't change the inferred type.

## Use When
- Validating object literals match expected shapes.
- Preserving literal types while checking compatibility.
- Getting IDE IntelliSense for specific types.

## Examples
```typescript
const colors = {
  red: "#ff0000",
  green: "#00ff00",
} satisfies Record<string, string>;
// colors is inferred as { red: "#ff0000", green: "#00ff00" }
```

```typescript
function createConfig() {
  return {
    port: 3000,
    host: "localhost"
  } satisfies { port: number; host: string };
}
```

```typescript
const nums = [1, 2, 3] satisfies number[];
// Preserves number[] type, not just number[]
```

## Returns
The original expression type (narrowed to match)

## Gotchas / Version Notes
- Available in TypeScript 4.9+.
- Unlike annotations, doesn't widen types.
- Useful for catching errors early in development.
- Still validates at compile time like type annotations.

## References
- TypeScript 4.9 notes: https://www.typescriptlang.org/docs/handbook/release-notes/typescript-4-9.html
