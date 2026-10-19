# Responsive & Accessible UI Engineering

Best practices for responsive layouts and WCAG 2.2 AA accessibility compliance.

---

## 1. Responsive Viewport Matrix

| Breakpoint | Minimum Width | Target Devices | Primary Layout Pattern |
| :--- | :--- | :--- | :--- |
| **sm** | 640px | Large Mobile / Phablet | Single column, bottom navigation bar |
| **md** | 768px | Tablets / Small Laptops | Collapsible drawer, 2-column grid |
| **lg** | 1024px | Desktops | Fixed sidebar navigation, multi-column dashboard |
| **xl** | 1280px | Wide Screens | Max-width content container (`max-w-7xl mx-auto`) |

---

## 2. Accessibility (a11y) Invariants
1. **Focus Rings**: Never remove focus outlines without providing a visible replacement (`focus-visible:ring-2`).
2. **Keyboard Traps in Modals**: When a modal or dialog opens:
   - Focus must automatically move inside the modal.
   - Tab cycling must remain trapped within modal boundaries.
   - Pressing `Escape` must dismiss the modal and restore focus to the trigger.
3. **Screen Reader Visibility**:
   - Icon-only buttons must include `aria-label="Close dialog"` or a visually hidden `<span className="sr-only">Close</span>`.
4. **Form Labels**: Every `<input>` must be explicitly linked to a `<label>` via `htmlFor="input-id"` or nested inside the label.
