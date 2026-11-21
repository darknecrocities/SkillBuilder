# Apple HIG & Material 3 Expressive Engineering Manual

> **Objective**: Build mobile interfaces that respect native OS ergonomics, safe areas, Dynamic Type scaling, and platform idioms instead of shipping web-wrapped layouts.

---

## 1. Ergonomic Touch Targets & Thumb-Zone Matrix

| Platform Rule | Minimum Tap Target | Inter-Target Gap | Primary Action Placement |
| :--- | :--- | :--- | :--- |
| **Apple iOS 18/19 HIG** | `44 x 44 pt` | `>= 8 pt` | Bottom 60% thumb arc (tab bar, bottom sheet, floating pill) |
| **Android Material 3** | `48 x 48 dp` | `>= 8 dp` | Navigation bar / FAB / bottom sheet actions |
| **Destructive Actions** | `>= 48 pt/dp` | `>= 16 pt/dp` away from Confirm | Explicit confirmation sheet or slide-to-confirm |

---

## 2. Safe Area & Edge-to-Edge Geometry

- **iOS (SwiftUI)**: Allow background materials (`.ultraThinMaterial`) to bleed edge-to-edge under status/home bars while keeping interactive content inset via `.safeAreaInset(edge: .bottom)` and `.ignoresSafeArea(.keyboard, edges: .bottom)` intentionally per screen.
- **Android (Jetpack Compose)**: Enable `enableEdgeToEdge()`, consume `WindowInsets.systemBars` / `WindowInsets.displayCutout`, and pad inputs with `Modifier.imePadding()`.
- **React Native**: Wrap root in `<SafeAreaProvider>` from `react-native-safe-area-context` and respect `useSafeAreaInsets()`. Never hardcode `paddingTop: 44` for the Dynamic Island.
- **Flutter**: Use `SafeArea` inside `Scaffold` bodies and `MediaQuery.viewInsetsOf(context).bottom` for smooth keyboard avoidance.

---

## 3. Dynamic Type (200% Accessibility Scaling) & Contrast

1. **SwiftUI**: Use semantic `.font(.body)`, `.font(.headline)` or `@ScaledMetric` for icon/row heights — never fix `frame(height: 44)` on multi-line text containers (use `minHeight: 44` instead).
2. **Compose**: Express typography in `sp` (`MaterialTheme.typography.*`) and expand container heights dynamically with `defaultMinSize(minHeight = 48.dp)`.
3. **Adaptive Dark/Light Tokens**: Use `Color(.secondarySystemBackground)` (iOS) or `MaterialTheme.colorScheme.surfaceContainer` (Android) instead of hardcoded `#000000` or `#ffffff`.
4. **Reduced Motion**: Check `UIAccessibility.isReduceMotionEnabled` (iOS), `ValueAnimator.areAnimatorsEnabled()` (Android), or `MediaQuery.disableAnimationsOf(context)` (Flutter) before triggering hero geometry transitions.
