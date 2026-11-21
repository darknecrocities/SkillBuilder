# Zustand Atomic Slices, Selector Memoization & State Machines

> **Objective**: Prevent whole-tree re-renders and impossible boolean-soup UI states by using atomic selectors and explicit state machines.

---

## 1. Atomic Selector Pattern (Never Destructure Whole Stores)

```typescript
// BAD: Component re-renders on EVERY unrelated slice update in the store
const { sidebarOpen, activeFilter, audioVolume } = useAppStore();

// GOOD: Subscribe strictly to the single primitive or useShallow tuple
import { useShallow } from "zustand/react/shallow";

const sidebarOpen = useAppStore((s) => s.sidebarOpen);
const { activeFilter, setActiveFilter } = useAppStore(
  useShallow((s) => ({ activeFilter: s.activeFilter, setActiveFilter: s.setActiveFilter }))
);
```

---

## 2. Explicit State Machines Over Boolean Flag Soup

Replace `isLoading && !isError && isRetrying` with a typed discriminated transition reducer / XState machine:

```typescript
type UploadState =
  | { status: "idle" }
  | { status: "validating"; fileName: string }
  | { status: "processing"; fileName: string; progress: number }
  | { status: "ready"; outputUrl: string }
  | { status: "error"; message: string };
```

- Validate transitions (`validating -> processing -> ready`) in one pure reducer/transition table so impossible transitions (e.g., jumping directly from `idle` to `ready` with no `outputUrl`) are unrepresentable at compile time.

---

## 3. State Scope Separation Rules
- **URL Search Params (`nuqs` / `useSearchParams`)**: Shareable filters, pagination, active tabs, selected item IDs.
- **TanStack Query / RSC**: Remote or persisted database records.
- **Zustand**: Client-only ephemeral UI shell state (`drawerOpen`, `selectedTool`, `playbackState`) — never duplicate DB entities or form field buffers globally.
