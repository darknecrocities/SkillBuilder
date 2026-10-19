# Cinematic Motion, Spring Physics & Scroll Choreography

A technical design specification for implementing high-craft, cinematic motion in modern web applications. It replaces floaty, generic AI transition tropes with physically grounded spring dynamics, typographic reveals, and responsive scroll choreography.

---

## 1. The Physics of High-Craft Motion

AI-generated interfaces frequently feel sluggish or synthetic because they use linear curves or slow generic easings (`transition: all 0.5s ease`). Premium interfaces (Linear, Raycast, Apple) use **physically grounded springs**:

### Recommended Spring Physics Configurations (Framer Motion)

```typescript
// 1. Tactile Micro-Interactions (Buttons, Toggles, Sliders)
// Snappy, energetic, zero overshoot, instant feedback.
export const microSpring = {
  type: "spring",
  stiffness: 450,
  damping: 32,
  mass: 0.8,
};

// 2. View & Layout Transitions (Modals, Drawers, Shared Elements)
// Balanced, elegant settlement without feeling floaty.
export const layoutSpring = {
  type: "spring",
  stiffness: 280,
  damping: 26,
  mass: 1.0,
};

// 3. Staggered Entrance Physics (Lists, Grids, Card Columns)
export const staggerContainer = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.05,
      delayChildren: 0.02,
    },
  },
};
```

### High-Craft CSS Cubic Bezier Timing Curve
When using pure CSS transitions, use Apple's signature deceleration curve instead of `ease-in-out`:
```css
:root {
  --ease-out-expo: cubic-bezier(0.16, 1, 0.3, 1);
  --ease-in-out-expo: cubic-bezier(0.87, 0, 0.13, 1);
  --duration-micro: 180ms;
  --duration-macro: 320ms;
}
```

---

## 2. Cinematic Typographic Reveals

### The Blur-to-Focus Headline Reveal
Rather than fading in or using amateurish typewriter effects, use progressive blur interpolation combined with subtle vertical settlement:

```tsx
import { motion, useReducedMotion } from "framer-motion";

export const CinematicHeadline = ({ text }: { text: string }) => {
  const shouldReduceMotion = useReducedMotion();
  const words = text.split(" ");

  return (
    <h1 className="flex flex-wrap gap-x-3 text-4xl font-semibold tracking-tight text-neutral-100 md:text-6xl">
      {words.map((word, index) => (
        <motion.span
          key={index}
          initial={shouldReduceMotion ? { opacity: 0 } : { opacity: 0, filter: "blur(10px)", y: 14 }}
          animate={{ opacity: 1, filter: "blur(0px)", y: 0 }}
          transition={{
            duration: 0.5,
            delay: index * 0.06,
            ease: [0.16, 1, 0.3, 1],
          }}
          className="inline-block"
        >
          {word}
        </motion.span>
      ))}
    </h1>
  );
};
```

---

## 3. Numeric Ticker & Tabular Figures

Counters, timestamps, and live metrics must never cause layout shift or horizontal jumping when digits change:

```css
.tabular-nums {
  font-variant-numeric: tabular-nums;
  font-feature-settings: "tnum";
}
```

Animate numeric values with smooth column translation rather than random number flickering.

---

## 4. Scroll Choreography & Viewport Triggers

### 1. Viewport Stagger via IntersectionObserver
Reveal sections only as they cross the 15% viewport threshold:

```tsx
import { motion } from "framer-motion";

export const ScrollFadeIn = ({ children }: { children: React.ReactNode }) => (
  <motion.div
    initial={{ opacity: 0, y: 24 }}
    whileInView={{ opacity: 1, y: 0 }}
    viewport={{ once: true, margin: "-15% 0px" }}
    transition={{ duration: 0.6, ease: [0.16, 1, 0.3, 1] }}
  >
    {children}
  </motion.div>
);
```

### 2. Native CSS Scroll-Driven Animations
Leverage modern browser scroll timelines without JavaScript bundle overhead:

```css
@keyframes scrubScale {
  from {
    transform: scale(0.95);
    opacity: 0.6;
  }
  to {
    transform: scale(1);
    opacity: 1;
  }
}

.scroll-hero-image {
  animation: scrubScale linear both;
  animation-timeline: view();
  animation-range: entry 10% cover 40%;
}
```

---

## 5. Non-Negotiable Motion Accessibility

Every animation must respect `prefers-reduced-motion`:

```css
@media (prefers-reduced-motion: reduce) {
  *, ::before, ::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```
