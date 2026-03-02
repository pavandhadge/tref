---
library: nextjs
version: "14.2.0"
category: api
item: nextjs.server_actions
type: feature
signature: "'use server' directive; action = async () => {}"
keywords: ["server actions", "form actions", "mutation", "post"]
aliases: ["server actions", "form submission", "server mutations"]
intent: "Define server-side functions that can be called directly from client components, enabling form submissions and data mutations without API routes."
last_updated: "2025-03-02"
schema_version: "2.0"
source_url: "https://nextjs.org/docs/app/building-your-application/data-fetching/server-actions-and-mutations"
source_title: "Server Actions Documentation"
alternatives:
  - option: "API Routes"
    reason: "Traditional REST API endpoints in app/api."
  - option: "API routes (pages)"
    reason: "Legacy pages/api routes."
  - option: "tRPC"
    reason: "Type-safe API layer with client generation."
---

# Server Actions

## Signature
```typescript
// In a server file
'use server'

export async function createUser(formData: FormData) {
  'use server'
  // Server-side logic
}
```

## What It Does
Allow server functions to be called directly from client components or forms. Handle form submissions, data mutations, and revalidation without creating API endpoints. Built-in validation and progressive enhancement.

## Use When
- Form submissions without API routes.
- Data mutations from client components.
- Need server-side logic that runs on specific actions.
- Want progressive enhancement (works without JS).

## Examples
```typescript
// actions/create-post.ts
'use server'

export async function createPost(formData: FormData) {
  const title = formData.get('title');
  
  await db.posts.create({ title });
  
  revalidatePath('/posts');
  redirect('/posts');
}
```

```tsx
// Component using server action
import { createPost } from '@/app/actions';

export function CreatePost() {
  return (
    <form action={createPost}>
      <input name="title" />
      <button type="submit">Create</button>
    </form>
  );
}
```

```typescript
// With useFormStatus for pending state
'use client'
import { useFormStatus } from 'react-dom';

function SubmitButton() {
  const { pending } = useFormStatus();
  return <button disabled={pending}>Submit</button>;
}
```

```typescript
// Using useActionState for form state
'use client'
import { useActionState } from 'react';
import { createPost } from '@/actions';

const [state, formAction] = useActionState(createPost, null);
```

```typescript
// Server action with validation
'use server'
import { z } from 'zod';

const schema = z.object({
  email: z.string().email(),
});

export async function registerUser(prevState, formData) {
  const validated = schema.safeParse(Object.fromEntries(formData));
  if (!validated.success) {
    return { errors: validated.error.flatten() };
  }
  // ... create user
}
```

## Returns
Server function that returns result

## Gotchas / Version Notes
- Mark functions with 'use server' at top of file or function.
- Can only be called from Client Components or forms.
- Use revalidatePath/revalidateTag to refresh data.
- Use redirect for navigation after mutation.
- Works progressively without JavaScript.

## References
- Server Actions: https://nextjs.org/docs/app/building-your-application/data-fetching/server-actions-and-mutations
- Forms: https://nextjs.org/docs/app/building-your-application/data-fetching/server-actions-and-mutations#forms
