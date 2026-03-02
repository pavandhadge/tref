---
library: tailwindcss
version: "3.4.0"
category: api
item: tailwind.utility_classes
type: css
signature: "class='flex justify-center p-4'"
keywords: ["tailwind", "utility", "css", "styling"]
aliases: ["tailwind classes", "utility-first", "responsive"]
intent: "Utility-first CSS framework providing low-level classes for rapid UI development without leaving HTML."
last_updated: "2025-03-02"
schema_version: "2.0"
source_url: "https://tailwindcss.com/docs"
source_title: "Tailwind CSS Documentation"
alternatives:
  - option: "Bootstrap"
    reason: "Component-based, pre-built components."
  - option: "CSS Modules"
    reason: "Scoped styles, component-based."
  - option: "Styled Components"
    reason: "CSS-in-JS with dynamic styling."
---

# Tailwind Utility Classes

## Categories
- Layout: flex, grid, block, absolute, relative
- Spacing: p-4, m-2, gap-4, space-x-4
- Sizing: w-full, h-screen, max-w-lg
- Typography: text-lg, font-bold, text-center
- Colors: bg-blue-500, text-white, border-red-300
- Effects: shadow-lg, opacity-50, rounded-lg
- Responsive: md:flex, lg:w-1/2

## What It Does
Provides small, reusable utility classes for styling. Compose classes in HTML for custom designs without writing custom CSS.

## Use When
- Rapid prototyping.
- Custom designs (not pre-built components).
- Responsive designs.
- Dark mode support.

## Examples
```html
<!-- Layout -->
<div class="flex justify-between items-center">
  <div class="w-1/2">Content</div>
</div>

<!-- Spacing -->
<button class="px-4 py-2 m-2 rounded">Click</button>

<!-- Colors -->
<div class="bg-blue-500 text-white p-4">Blue</div>

<!-- Responsive -->
<div class="hidden md:block lg:w-1/2">Responsive</div>

<!-- Hover/Focus -->
<button class="hover:bg-blue-600 focus:ring">Button</button>

<!-- Dark mode -->
<div class="dark:bg-gray-900">Dark</div>
```

```html
<!-- Grid -->
<div class="grid grid-cols-3 gap-4">
  <div>1</div>
  <div>2</div>
  <div>3</div>
</div>
```

```html
<!-- Flex utilities -->
<div class="flex flex-col sm:flex-row">
  <div class="flex-1">Grows</div>
  <div class="shrink-0">Fixed</div>
</div>
```

## Returns
Styled elements

## Gotchas / Version Notes
- Learning curve for class names.
- JIT compiles only used styles.
- Use arbitrary values: class="top-[100px]".
- Configure in tailwind.config.js.
- Can customize theme.

## References
- Tailwind docs: https://tailwindcss.com/docs
