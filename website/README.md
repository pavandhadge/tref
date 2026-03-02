# tref Website

This is the marketing/docs site for `tref`.

## Stack

- React + TypeScript
- Vite
- Tailwind CSS

## Local Development

```bash
cd website
npm install
npm run dev
```

## Build

```bash
npm run build
npm run preview
```

## Content Sources

- Homepage copy: `src/pages/Index.tsx`
- Docs page renderer: `src/pages/Docs.tsx`
- Markdown docs used by site tabs:
  - `public/docs/interface.md`
  - `public/docs/architecture.md`
  - `public/docs/tools.md`

## Current Product Positioning

Website content is aligned with current `tref` capabilities:

- offline-first versioned retrieval (`library@version`)
- structured output (description/signature/cautions/examples/references)
- trust-aware update flow (checksum + optional signature requirement)
- compatibility-aware version mapping
- language-aware examples (`--lang`)
- regression quality gates (`tref eval`)
