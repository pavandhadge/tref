---
library: vue
version: "3.3.0"
category: api
item: vue.composition_api
type: feature
signature: "setup() function, ref(), reactive(), computed()"
keywords: ["vue", "composition", "api", "reactivity"]
aliases: ["Vue 3", "setup", "ref", "reactive"]
intent: "Group component logic by concern rather than options, enabling better code reuse and TypeScript support."
last_updated: "2025-03-02"
schema_version: "2.0"
source_url: "https://vuejs.org/guide/extras/composition-api-faq.html"
source_title: "Composition API FAQ"
alternatives:
  - option: "Options API"
    reason: "Traditional Vue 2 style with data, methods, computed options."
  - option: "Pinia"
    reason: "State management library for Vue 3 applications."
---

# Composition API

## Signature
```typescript
import { ref, reactive, computed, watch } from 'vue';

export default {
  setup() {
    // Composition logic here
    return { /* exposed to template */ };
  }
}
```

## What It Does
Allows defining component logic using imported functions instead of object options. Groups related code together, enabling better TypeScript support and reusable logic extraction via composables.

## Use When
- Building large components with complex logic.
- Sharing stateful logic between components.
- Wanting better TypeScript type inference.
- Creating reusable component utilities (composables).

## Examples
```typescript
import { ref, computed } from 'vue';

export default {
  setup() {
    const count = ref(0);
    const doubled = computed(() => count.value * 2);
    
    function increment() {
      count.value++;
    }
    
    return { count, doubled, increment };
  }
}
```

```typescript
// Reusable composable
function useMouse() {
  const x = ref(0);
  const y = ref(0);
  
  onMounted(() => {
    window.addEventListener('mousemove', e => {
      x.value = e.x;
      y.value = e.y;
    });
  });
  
  return { x, y };
}
```

```typescript
// Reactive object
const state = reactive({
  user: null,
  isLoggedIn: computed(() => state.user !== null)
});
```

## Returns
setup function returns object exposed to template

## Gotchas / Version Notes
- Available since Vue 3.0, improved in 3.3.
- Use `.value` to access ref values in script.
- No need for `.value` in template.
- Can mix with Options API in same component.
- `ref()` for primitives, `reactive()` for objects.

## References
- Composition API docs: https://vuejs.org/api/reactivity-core.html
- Vue 3 migration: https://vuejs.org/guide/extras/composition-api-faq.html
