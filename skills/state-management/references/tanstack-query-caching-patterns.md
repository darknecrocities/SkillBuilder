# TanStack Query Key Factories & Optimistic Cache Invalidation

> **Objective**: Eliminate stale server state, missed cache invalidations, and race conditions during optimistic mutations.

---

## 1. Hierarchical Query Key Factory

Never scatter raw array keys (`["tasks", id]`) across components. Centralize keys in a typed factory per domain so prefix invalidation works deterministically:

```typescript
export const taskKeys = {
  all: ["tasks"] as const,
  lists: () => [...taskKeys.all, "list"] as const,
  list: (filters: { status?: string; query?: string }) => [...taskKeys.lists(), filters] as const,
  details: () => [...taskKeys.all, "detail"] as const,
  detail: (id: string) => [...taskKeys.details(), id] as const,
};
```

---

## 2. Optimistic Mutation with Snapshot Rollback & `onSettled`

```typescript
export function useUpdateTaskStatus() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ id, completed }: { id: string; completed: boolean }) =>
      patchTask(id, { completed }),
    onMutate: async (vars) => {
      await queryClient.cancelQueries({ queryKey: taskKeys.detail(vars.id) });
      const previous = queryClient.getQueryData<TaskRecord>(taskKeys.detail(vars.id));
      if (previous) {
        queryClient.setQueryData(taskKeys.detail(vars.id), { ...previous, completed: vars.completed });
      }
      return { previous };
    },
    onError: (_err, vars, ctx) => {
      if (ctx?.previous) {
        queryClient.setQueryData(taskKeys.detail(vars.id), ctx.previous);
      }
    },
    onSettled: (_data, _err, vars) => {
      queryClient.invalidateQueries({ queryKey: taskKeys.detail(vars.id) });
      queryClient.invalidateQueries({ queryKey: taskKeys.lists() });
    },
  });
}
```

---

## 3. Caching & Request Hygiene Rules
- Pass `{ signal }` from `queryFn: ({ signal }) => fetch(..., { signal })` so navigating away aborts in-flight requests cleanly.
- Set explicit `staleTime` (`30_000–120_000` ms) to prevent redundant refetch storms on window focus for stable reference data.
- Never mirror TanStack Query server responses into Zustand or Redux — keep a single source of truth.
