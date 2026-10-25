# Kinetic Typography & Variable Font Engineering Guide

This guide establishes the production engineering standard for kinetic typography, variable font interpolation, and clip-path text reveals across Web (CSS / Framer Motion) and Mobile (Flutter / Dart / Impeller).

---

## 1. The Death of Generic Font Flatland

AI-generated interfaces almost universally default to static sans-serif fonts (e.g., standard Inter or Roboto 400/600) set at static weights inside uninspired card layouts. This homogenizes digital products into generic "AI slop."

Variable fonts and kinetic typography introduce:
1. **Dynamic Character**: Fluid interpolation across physical axes (`wght`, `wdth`, `slnt`, `opsz`, `GRAD`).
2. **Tabular Metric Stability**: Zero-jitter numeric tickers and telemetry readouts via OpenType tabular numbers (`tnum`).
3. **Cinematic Narrative Reveals**: Staggered clip-path masking that treats typography as an architectural element rather than passive prose.

---

## 2. Variable Font Registered & Parametric Axes

Variable fonts (`woff2` on Web, `.ttf` in Flutter assets) contain continuous interpolation coordinates:

| Axis Tag | Name | Typical Range | Engineering Purpose & Motion Behavior |
| :--- | :--- | :--- | :--- |
| `'wght'` | Weight | `100` – `900` | Dynamic visual hierarchy; hover impact; focus emphasis. |
| `'wdth'` | Width | `75` – `125` | Responsive headline fitting; expands on active state. |
| `'slnt'` | Slant | `-10` – `0` | Subtle italics accentuation without font-file switching. |
| `'opsz'` | Optical Size | `6` – `72` | Adjusts stroke contrast, counter-forms, and x-height for readability. |
| `'GRAD'` | Grade | `-200` – `150` | Alters stroke thickness **without changing glyph advance width** (zero layout reflow). |

> [!TIP]
> When animating weight on hover or focus in navigational menus, use `'GRAD'` instead of `'wght'` if the font supports it. `'GRAD'` modifies visual density without altering character spacing, completely eliminating text jitter and layout reflow.

---

## 3. Web Kinetic Typography (CSS & Framer Motion)

### 3.1 CSS Low-Level Control & Tabular Telemetry

```css
/* Industrial CAD / Telemetry readout with zero horizontal drift */
.telemetry-readout {
  font-family: 'Geist Mono', 'JetBrains Mono', monospace;
  font-feature-settings: 'tnum' 1, 'zero' 1;
  font-variant-numeric: tabular-nums slashed-zero;
  letter-spacing: -0.02em;
}

/* Variable font hover transition without layout reflow */
.variable-headline {
  font-family: 'Cabinet Grotesk Variable', sans-serif;
  font-variation-settings: 'wght' 450, 'wdth' 100;
  transition: font-variation-settings 0.35s cubic-bezier(0.16, 1, 0.3, 1);
  will-change: font-variation-settings;
}

.variable-headline:hover {
  font-variation-settings: 'wght' 780, 'wdth' 115;
}

@media (prefers-reduced-motion: reduce) {
  .variable-headline {
    transition: none;
  }
}
```

### 3.2 Clip-Path Character / Line Reveal (Framer Motion)

Clip-path text masking reveals text as if emerging from an architectural slit:

```tsx
import { motion } from 'framer-motion';

const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: { staggerChildren: 0.04, delayChildren: 0.1 },
  },
};

const charVariants = {
  hidden: {
    y: '100%',
    transition: { ease: [0.33, 1, 0.68, 1], duration: 0.5 },
  },
  visible: {
    y: '0%',
    transition: { ease: [0.16, 1, 0.3, 1], duration: 0.65 },
  },
};

export function MaskedHeadline({ text }: { text: string }) {
  const characters = Array.from(text);

  return (
    <motion.h1
      variants={containerVariants}
      initial="hidden"
      animate="visible"
      className="flex flex-wrap overflow-hidden text-5xl font-extrabold tracking-tighter"
      style={{ clipPath: 'polygon(0 0, 100% 0, 100% 100%, 0 100%)' }}
    >
      {characters.map((char, i) => (
        <span key={`${char}-${i}`} className="inline-block overflow-hidden">
          <motion.span
            variants={charVariants}
            className="inline-block"
          >
            {char === ' ' ? '\u00A0' : char}
          </motion.span>
        </span>
      ))}
    </motion.h1>
  );
}
```

---

## 4. Mobile Kinetic Typography (Flutter / Dart / Impeller)

### 4.1 Variable Font Axes & OpenType Features in Flutter

Flutter supports variable font axes via `FontVariation` and OpenType feature tags via `FontFeature`:

```dart
import 'dart:ui';
import 'package:flutter/material.dart';

class TelemetryTextStyle {
  static TextStyle get industrialReadout => const TextStyle(
    fontFamily: 'JetBrainsMono',
    fontSize: 22,
    letterSpacing: -0.5,
    fontFeatures: [
      FontFeature.tabularFigures(),
      FontFeature.slashedZero(),
    ],
  );

  static TextStyle variableHeadline({
    required double weight,
    double width = 100.0,
    double opticalSize = 24.0,
  }) {
    return TextStyle(
      fontFamily: 'CabinetGrotesk',
      fontSize: 32,
      fontVariations: [
        FontVariation('wght', weight.clamp(100.0, 900.0)),
        FontVariation('wdth', width.clamp(75.0, 125.0)),
        FontVariation('opsz', opticalSize.clamp(6.0, 72.0)),
      ],
    );
  }
}
```

### 4.2 Flutter Masked Staggered Text Reveal

```dart
import 'package:flutter/material.dart';

class MaskedTextReveal extends StatefulWidget {
  final String text;
  final TextStyle style;

  const MaskedTextReveal({
    super.key,
    required this.text,
    required this.style,
  });

  @override
  State<MaskedTextReveal> createState() => _MaskedTextRevealState();
}

class _MaskedTextRevealState extends State<MaskedTextReveal>
    with SingleTickerProviderStateMixin {
  late final AnimationController _controller;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 700),
    )..forward();
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final chars = widget.text.split('');
    final step = 1.0 / (chars.isEmpty ? 1 : chars.length);

    return Row(
      mainAxisSize: MainAxisSize.min,
      children: List.generate(chars.length, (index) {
        final start = (index * step * 0.6).clamp(0.0, 0.8);
        final end = (start + 0.4).clamp(0.0, 1.0);
        final animation = CurvedAnimation(
          parent: _controller,
          curve: Interval(start, end, curve: Curves.easeOutCubic),
        );

        return ClipRect(
          child: AnimatedBuilder(
            animation: animation,
            builder: (context, child) {
              return Transform.translate(
                offset: Offset(0, (1.0 - animation.value) * 32.0),
                child: Opacity(
                  opacity: animation.value.clamp(0.0, 1.0),
                  child: child,
                ),
              );
            },
            child: Text(
              chars[index] == ' ' ? '\u00A0' : chars[index],
              style: widget.style,
            ),
          ),
        );
      }),
    );
  }
}
```

### 4.3 Universal Mobile Tabular Figures (React Native, SwiftUI, Compose)

```tsx
// React Native Tabular Telemetry
<Text style={{ fontFamily: 'Courier', fontVariant: ['tabular-nums'] }}>
  {count.toLocaleString()}
</Text>
```

```swift
// Native iOS SwiftUI Tabular Digits
Text(verbatim: "\(count)")
    .font(.system(size: 28, weight: .bold, design: .monospaced))
    .monospacedDigit()
```

```kotlin
// Android Jetpack Compose Tabular Figures
Text(
    text = count.toString(),
    style = TextStyle(
        fontFamily = FontFamily.Monospace,
        fontFeatureSettings = "tnum 1, zero 1"
    )
)
```

---

## 5. Anti-Slop Typography Checklist

| Requirement | Failure Pattern (AI Slop) | High-Craft Production Standard |
| :--- | :--- | :--- |
| **Numeric Telemetry** | Numbers jittering left/right on countdowns (`tnum` omitted) | `font-variant-numeric: tabular-nums` or `FontFeature.tabularFigures()` |
| **Headline Weight** | Static bold 700 without visual pacing | Variable weight/width scaling on hover / scroll position |
| **Entry Transitions** | Standard fade-in or jarring pop-in | Architectural clip-path mask reveals (`overflow-hidden` + `translateY`) |
| **Accessibility** | Infinite kinetic loops triggering vestibular discomfort | Respects `prefers-reduced-motion` and `accessibleNavigation` |
| **Layout Stability** | Layout re-flow on hover text-bolding | Use `'GRAD'` axis or CSS fixed inline-block bounds |
