# TanStack Query Server-State Caching Patterns

Server state is asynchronously owned and must not be duplicated into untracked client stores.

---

## 1. Query Key Conventions

Use structured tuple arrays:
```typescript
// Query Key Factory
export const userKeys = {
  all: ['users'] as const,
  lists: () => [...userKeys.all, 'list'] as const,
  list: (filters: string) => [...userKeys.lists(), { filters }] as const,
  details: () => [...userKeys.all, 'detail'] as const,
  detail: (id: string) => [...userKeys.details(), id] as const,
};
```

---

## 2. Stale Time & Cache Invalidation

- **`staleTime`**: Set to at least 30s to 5 minutes for stable entity data to eliminate unnecessary refetches.
- **Targeted Invalidation**: On mutations, invalidate specific sub-keys (`queryClient.invalidateQueries({ queryKey: userKeys.detail(id) })`).
