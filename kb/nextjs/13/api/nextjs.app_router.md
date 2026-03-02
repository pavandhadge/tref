---
library: nextjs
version: "13.4.0"
category: api
item: nextjs.app_router
type: feature
signature: "app/ directory with page.tsx, layout.tsx, route.ts"
keywords: ["app router", "react server components", "routing"]
aliases: ["Next.js 13", "app directory", "file-based routing"]
intent: "Next.js 13+ file-based routing and layout system using React Server Components, supporting nested layouts, streaming, and co-located data fetching."
last_updated: "2025-03-02"
schema_version: "2.0"
source_url: "https://nextjs.org/docs/app/building-your-application/routing"
source_title: "Next.js App Router Documentation"
alternatives:
  - option: "pages directory"
    reason: "Traditional Next.js pages router (still supported)."
  - option: "getStaticProps / getServerSideProps"
    reason: "Data fetching in pages directory."
  - option: "Next.js API routes"
    reason: "Backend API endpoints in pages/api."
---

# App Router

## Structure
```
app/
├── page.tsx          # Route: /
├── layout.tsx        # Root layout (wraps all pages)
├── globals.css      # Global styles
├── loading.tsx      # Loading UI
├── error.tsx        # Error UI
├── not-found.tsx    # 404 page
├── route.ts         # API route handler
└── [slug]/          # Dynamic segment
    ├── page.tsx     # /:slug
    └── layout.tsx   # Segment-specific layout
```

## What It Does
File-based routing with React Server Components (RSC). Supports layouts, nested routes, streaming with Suspense, and simplified data fetching. Pages are Server Components by default.

## Use When
- Building new Next.js applications.
- Using React Server Components for server-first data fetching.
- Need nested layouts with persistent UI.
- Want streaming and selective hydration.

## Examples
```tsx
// app/page.tsx - Home page
export default function HomePage() {
  return <h1>Welcome</h1>;
}
```

```tsx
// app/layout.tsx - Root layout
export default function RootLayout({ children }) {
  return (
    <html>
      <body>
        <nav>...</nav>
        {children}
      </body>
    </html>
  );
}
```

```tsx
// app/blog/[slug]/page.tsx - Dynamic route
import { getPost } from '@/lib';

export default async function BlogPost({ params }) {
  const post = await getPost(params.slug);
  return <article>{post.content}</article>;
}
```

```tsx
// app/dashboard/layout.tsx - Nested layout
export default function DashboardLayout({ children }) {
  return (
    <div className="dashboard">
      <Sidebar />
      {children}
    </div>
  );
}
```

```tsx
// app/api/route.ts - API route
import { NextResponse } from 'next/server';

export async function GET() {
  return NextResponse.json({ data: 'hello' });
}
```

## Returns
Renders React Server Components

## Gotchas / Version Notes
- Pages are Server Components by default.
- Use "use client" for interactive components.
- params is a Promise in Next.js 15+.
- Dynamic rendering based on dynamic functions/headers.
- Static generation for layouts and pages without dynamic data.

## References
- App Router docs: https://nextjs.org/docs/app
- Server Components: https://nextjs.org/docs/app/building-your-application/rendering/server-components
