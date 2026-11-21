# React Server Components (RSC) & Server Action Boundaries

> **Objective**: Minimize client JavaScript bundles, prevent secret/DB leakage into browser bundles, and enforce Zod-validated Server Actions with clean optimistic rollback.

---

## 1. Server vs. Leaf Client Boundary Rules

| Component Role | Directive | Allowed Imports | Prohibited |
| :--- | :--- | :--- | :--- |
| **Page / Layout / Data Shell** | None (RSC default) | DB repositories, typed data accessors, `server-only`, env secrets | `useState`, `useEffect`, browser `window` APIs |
| **Leaf Interactive Control** | `"use client"` | React hooks, UI state, Lucide icons, Framer/Rive wrappers | Direct DB clients, secret env vars, raw `data/generated/` JSON |
| **Server Action** | `"use server"` | Zod schemas, session auth checks, domain services, `revalidateTag` | Trusting unvalidated `FormData` or skipping tenant checks |

### Serialization & Composition Pattern
Pass serializable props (`string`, `number`, plain objects) from Server Components into small Client leaf components, or pass Server Components as `children` slots inside Client Providers so heavy markdown/data trees never ship JS to the browser.

---

## 2. React 19 `useActionState` + `useOptimistic` Rollback

```tsx
"use client";

import { useActionState, useOptimistic, startTransition } from "react";
import { saveTitleAction } from "@/actions/itemActions";

export function TitleEditor({ itemId, initialTitle }: { itemId: string; initialTitle: string }) {
  const [state, submitAction, pending] = useActionState(saveTitleAction, { ok: true, error: null as string | null });
  const [optimisticTitle, setOptimisticTitle] = useOptimistic(initialTitle, (_prev, next: string) => next);

  const onSubmit = (formData: FormData) => {
    const next = String(formData.get("title") ?? "").trim();
    startTransition(() => setOptimisticTitle(next));
    submitAction(formData);
  };

  return (
    <form action={onSubmit} className="flex flex-col gap-2">
      <input type="hidden" name="itemId" value={itemId} />
      <input name="title" defaultValue={optimisticTitle} disabled={pending} className="rounded border border-zinc-800 bg-zinc-950 px-3 py-2 text-sm text-zinc-100" />
      {state.error && <p role="alert" className="text-xs text-rose-400">{state.error}</p>}
    </form>
  );
}
```

- Always mark Server Action modules with `import "server-only";` where database access occurs, re-authenticate the caller inside every action, and return structured `{ ok, error }` payloads instead of throwing raw exceptions across the RSC wire.
