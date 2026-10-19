# Design Systems & Tailwind CSS v4 Architecture

Guidelines for establishing scalable design tokens and accessible component primitives.

---

## 1. Tailwind CSS v4 CSS-First Configuration
Tailwind v4 embraces native CSS variables and `@theme` directives instead of legacy `tailwind.config.js`:

```css
@import "tailwindcss";

@theme {
  --color-primary-50: oklch(0.97 0.02 260);
  --color-primary-500: oklch(0.55 0.22 260);
  --color-primary-900: oklch(0.25 0.15 260);

  --font-sans: "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  --radius-lg: 0.5rem;
}
```

---

## 2. Accessible Primitive Wrapping (Radix & shadcn/ui)
- Build on unstyled, accessible primitives (`@radix-ui/react-dialog`, `@radix-ui/react-dropdown-menu`).
- Keep components composable via the `Slot` pattern (`asChild` prop).
- Separate component style variants using `cva` (Class Variance Authority):

```typescript
import { cva, type VariantProps } from "class-variance-authority";

export const buttonVariants = cva(
  "inline-flex items-center justify-center rounded-md font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50",
  {
    variants: {
      variant: {
        primary: "bg-primary-600 text-white hover:bg-primary-700 focus-visible:ring-primary-500",
        secondary: "bg-neutral-100 text-neutral-900 hover:bg-neutral-200",
        ghost: "hover:bg-neutral-100 text-neutral-700",
        destructive: "bg-red-600 text-white hover:bg-red-700 focus-visible:ring-red-500",
      },
      size: {
        sm: "h-8 px-3 text-xs",
        md: "h-10 px-4 text-sm",
        lg: "h-12 px-6 text-base",
      },
    },
    defaultVariants: {
      variant: "primary",
      size: "md",
    },
  }
);
```
