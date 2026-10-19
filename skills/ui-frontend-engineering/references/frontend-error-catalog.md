# Frontend & UI Error Catalog

Specialized catalog of user interface defects, root causes, and resolutions.

---

### [UI-ERR-001] Hydration Mismatch on Browser Globals
- **Symptom**: `Hydration failed because the initial UI does not match that which was rendered on the server.`
- **Root Cause**: Reading `window.innerWidth`, `navigator.userAgent`, or `localStorage` during initial render.
- **Remediation**: Guard with `useEffect` or render placeholder until mounted on client:
  ```typescript
  const [mounted, setMounted] = useState(false);
  useEffect(() => setMounted(true), []);
  if (!mounted) return <SkeletonLoader />;
  ```

---

### [UI-ERR-002] Layout Shift on Late-Loading Images (CLS Spike)
- **Symptom**: Page content jerks or jumps vertically when an image completes loading.
- **Root Cause**: `<img>` rendered without intrinsic aspect ratio or `width`/`height` attributes.
- **Remediation**: Always specify aspect ratio in CSS (`aspect-video`, `aspect-square`) or use Next.js `<Image fill />` with parent container dimensions.

---

### [UI-ERR-003] Missing Accessible Name on Icon Button
- **Symptom**: Lighthouse / axe accessibility audit fails with `button-name: Buttons must have discernible text`.
- **Root Cause**: Rendering `<button><TrashIcon /></button>` without an accessible label.
- **Remediation**:
  ```tsx
  <button aria-label="Delete item" className="p-2 text-red-600">
    <TrashIcon aria-hidden="true" />
  </button>
  ```

---

### [UI-ERR-004] CSS Stacking Context & Z-Index Collision
- **Symptom**: Modal overlay or dropdown menu rendered underneath sibling elements despite `z-index: 9999`.
- **Root Cause**: Sibling parent element has a transform, filter, or opacity property creating an isolated stacking context.
- **Remediation**: Use a React Portal (`createPortal`) to mount floating UI components directly at the root of `document.body`.
