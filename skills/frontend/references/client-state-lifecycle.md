# Client State Lifecycle & Optimistic UI Updates

---

## 1. State Scope Hierarchy

Scope | Recommended Primitive | Avoid
:--- | :--- | :---
URL / Search Params | `nuqs` / `useSearchParams` | Local `useState` that breaks deep links & browser back
Server Cache | `TanStack Query` / RSC | Global Redux store without cache invalidation
Optimistic Mutations | `useOptimistic` (React 19) | Manual loading spinners on simple button clicks
UI Transient | `useState` / `useReducer` | Global context for ephemeral dropdown menus

---

## 2. Optimistic Updates with `useOptimistic`

```tsx
'use client';

import { useOptimistic } from 'react';

export function CommentList({ initialComments, addCommentAction }) {
  const [optimisticComments, setOptimistic] = useOptimistic(
    initialComments,
    (state, newComment: string) => [...state, { id: 'temp', text: newComment, pending: true }]
  );

  async function handleSubmit(formData: FormData) {
    const text = formData.get('comment') as string;
    setOptimistic(text);
    await addCommentAction(formData);
  }

  return (
    <div>
      {optimisticComments.map(c => (
        <div key={c.id} style={{ opacity: c.pending ? 0.6 : 1 }}>{c.text}</div>
      ))}
    </div>
  );
}
```
