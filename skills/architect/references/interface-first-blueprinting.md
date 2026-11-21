# Interface-First Blueprinting Field Manual

## 1. Eliminating Boolean Soup with Discriminated Unions

```typescript
// BAD: 16 combinations, 12 of which are illegal states
interface AsyncFlags<T> {
  isLoading: boolean;
  isError: boolean;
  data?: T;
  error?: string;
}

// GOOD: Only valid states can be constructed
export type AsyncState<T> =
  | { status: "idle" }
  | { status: "loading"; previousData?: T }
  | { status: "ready"; data: T }
  | { status: "error"; message: string; retryable: boolean };
```

## 2. Branded Domain Primitives (Zero BOLA Mix-ups)

```typescript
declare const brand: unique symbol;
export type Brand<T, Name extends string> = T & { readonly [brand]: Name };
export type TenantId = Brand<string, "TenantId">;
export type DocumentId = Brand<string, "DocumentId">;
```

## 3. Pre-Code File Partitioning Rules
| Layer | Target Ceiling | Hard Ceiling | Split Seam |
| :--- | :--- | :--- | :--- |
| **UI Component / View** | `<= 250` lines | `500` lines | Subviews, custom hooks, SVG/Rive rig wrappers |
| **Domain Service** | `<= 300` lines | `500` lines | Pure use-case handlers, policy evaluators |
| **Repository / Store** | `<= 350` lines | `500` lines | Entity query modules, schema mappers |
| **Schemas / Types** | `<= 350` lines | `500` lines | Domain-scoped contract slices |

## 4. UI Shape Contract Checklist
Before writing JSX/SwiftUI/Compose:
- [ ] Art movement locked (Industrial Tactical, Swiss Editorial, Wabi-Sabi, or Technical CAD).
- [ ] Single platform target locked (`/web-ui` OR `/mobile-ui`, never both).
- [ ] Empty, loading, error, offline, and `prefers-reduced-motion` states accounted for.
- [ ] Minimum `44x44px` touch bounds and `>= 4.5:1` text contrast verified.
