# React Server Components (RSC) & Server Action Boundaries

---

## 1. Clean Boundary Architecture

- **React Server Components (RSC)**: Default for all components in Next.js App Router. RSC executes only on the server, producing static or streamed virtual DOM without increasing client bundle size.
- **Client Boundaries (`"use client"`)**: Pushed down strictly to interactive leaves (e.g. `IconButton`, `FilterDropdown`, `ColorPicker`).
- **Data Fetching**: Performed in RSC via async/await directly from databases or backend services with cached fetch tags (`fetch(url, { next: { tags: ['posts'] } })`).

---

## 2. Server Action Mutation Pattern

```typescript
// app/actions/update-profile.ts
'use server';

import { z } from 'zod';
import { revalidateTag } from 'next/cache';

const ProfileSchema = z.object({
  name: z.string().min(2).max(50),
});

export async function updateProfile(prevState: any, formData: FormData) {
  const result = ProfileSchema.safeParse({
    name: formData.get('name'),
  });

  if (!result.success) {
    return { success: false, errors: result.error.flatten().fieldErrors };
  }

  // Execute database mutation
  revalidateTag('user-profile');
  return { success: true, errors: null };
}
```
