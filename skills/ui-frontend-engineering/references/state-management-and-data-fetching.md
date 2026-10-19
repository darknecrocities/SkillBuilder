# State Management & Resilient Data Fetching

Patterns for separating server state, client state, and optimistic mutations.

---

## 1. State Topology

| Layer | Responsibility | Recommended Tool |
| :--- | :--- | :--- |
| **Server State** | Caching, invalidation, background re-fetching, deduplication | TanStack Query, SWR, Next.js Server Components |
| **Global Client State** | User preferences, active modal, sidebar toggle | Zustand, Nanostores |
| **Local Component State** | Form field typing, accordion toggle | React `useState`, `useReducer` |

---

## 2. Optimistic Mutations with Rollback

When a user triggers an action (e.g. liking a post or renaming an item), update the UI immediately and roll back on network failure:

```typescript
import { useMutation, useQueryClient } from "@tanstack/react-query";

export function useUpdateItem() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (updatedItem: { id: string; name: string }) => {
      const res = await fetch(`/api/items/${updatedItem.id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(updatedItem),
      });
      if (!res.ok) throw new Error("Failed to update item");
      return res.json();
    },
    onMutate: async (newItem) => {
      await queryClient.cancelQueries({ queryKey: ["items", newItem.id] });
      const previousItem = queryClient.getQueryData(["items", newItem.id]);
      queryClient.setQueryData(["items", newItem.id], newItem);
      return { previousItem };
    },
    onError: (err, newItem, context) => {
      if (context?.previousItem) {
        queryClient.setQueryData(["items", newItem.id], context.previousItem);
      }
    },
    onSettled: (data, err, variables) => {
      queryClient.invalidateQueries({ queryKey: ["items", variables.id] });
    },
  });
}
```
