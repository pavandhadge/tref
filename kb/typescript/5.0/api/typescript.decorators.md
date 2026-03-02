---
library: typescript
version: "5.0.0"
category: api
item: typescript.decorators
type: feature
signature: "@decorator class, method, or property"
keywords: ["decorators", "annotations", "metadata", "aop"]
aliases: ["decorator syntax", "class decorators", "method decorators"]
intent: "Attach metadata and modify behavior to classes, methods, accessors, and properties using standardized syntax."
last_updated: "2025-03-02"
schema_version: "2.0"
source_url: "https://www.typescriptlang.org/docs/handbook/decorators.html"
source_title: "Decorators Documentation"
alternatives:
  - option: "Higher-Order Components (React)"
    reason: "Pattern for component composition in React applications."
  - option: "function wrappers"
    reason: "Traditional JavaScript pattern for adding behavior."
---

# Decorators

## Signature
```typescript
@decorator
@decorator(args)
class MyClass {}

@decorator
myMethod() {}
```

## What It Does
Decorators are functions that can be attached to class declarations, methods, accessors, properties, or parameters. They enable declarative composition of behavior and metadata attachment using standardized ECMAScript syntax.

## Use When
- Building frameworks like Angular or NestJS.
- Adding logging, caching, or validation cross-cutting concerns.
- Creating reusable component patterns.
- Implementing dependency injection.

## Examples
```typescript
function logged(target: any, propertyKey: string, descriptor: PropertyDescriptor) {
  const original = descriptor.value;
  descriptor.value = function (...args: any[]) {
    console.log(`Calling ${propertyKey} with`, args);
    return original.apply(this, args);
  };
  return descriptor;
}

class Calculator {
  @logged
  add(a: number, b: number) {
    return a + b;
  }
}
```

```typescript
function readonly(target: any, key: string, descriptor: PropertyDescriptor) {
  descriptor.writable = false;
  return descriptor;
}

class Config {
  @readonly
  apiUrl = "https://api.example.com";
}
```

```typescript
function sealed(constructor: Function) {
  Object.seal(constructor);
  Object.seal(constructor.prototype);
}

@sealed
class Product {}
```

## Returns
Modified property descriptor or class

## Gotchas / Version Notes
- TypeScript 5.0+ uses ECMAScript standardized decorators.
- Old experimental decorators available with `experimentalDecorators`.
- Decorators don't have direct access to instance properties in class field decorators.
- Execution order: parameters → accessor → property → method → class (bottom to top).

## References
- Decorators docs: https://www.typescriptlang.org/docs/handbook/decorators.html
- TC39 Decorators proposal: https://github.com/tc39/proposal-decorators
