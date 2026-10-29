# Zustand Atomic Slices & Selector Memoization

Global client state must be partitioned into cohesive atomic slices to prevent unnecessary component re-renders.

---

## 1. Slice Pattern Implementation

```typescript
import { create } from 'zustand';

interface ThemeSlice {
  theme: 'light' | 'dark';
  setTheme: (theme: 'light' | 'dark') => void;
}

const createThemeSlice = (set): ThemeSlice => ({
  theme: 'dark',
  setTheme: (theme) => set({ theme }),
});

export const useAppStore = create<ThemeSlice>()((...a) => ({
  ...createThemeSlice(...a),
}));
```

---

## 2. Selector Discipline

Always consume state via atomic selectors:
```typescript
// Good: only re-renders when 'theme' changes
const theme = useAppStore((state) => state.theme);

// Bad: re-renders on ANY store change
const { theme } = useAppStore();
```
