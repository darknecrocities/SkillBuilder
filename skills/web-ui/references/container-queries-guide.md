# CSS Container Queries (`@container`) Guide

Container queries decouple component styling from the global browser viewport, enabling components to adapt to the size of their parent container.

---

## 1. Syntax & Declaration

```css
/* 1. Define Container Context */
.card-wrapper {
  container-type: inline-size;
  container-name: card;
}

/* 2. Responsive Component Styles Based on Parent Width */
@container card (min-width: 400px) {
  .card-content {
    display: grid;
    grid-template-columns: 120px 1fr;
    gap: 1.5rem;
  }
}

@container card (min-width: 700px) {
  .card-content {
    grid-template-columns: 240px 1fr;
  }
}
```

### In Tailwind CSS v4:
```html
<div class="@container">
  <div class="flex flex-col @md:flex-row">...</div>
</div>
```
