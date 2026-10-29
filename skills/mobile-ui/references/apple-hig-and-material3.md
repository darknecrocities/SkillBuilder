# Apple HIG & Material 3 Expressive Guidelines

Mobile application interfaces must honor platform-native conventions rather than porting web idioms.

---

## 1. Ergonomic Touch Targets & Safe Areas

Platform Rule | Target Dimension | Spacing
:--- | :--- | :---
Apple HIG Minimum | $44 \times 44\,\text{pt}$ | $\ge 8\,\text{pt}$ inter-element padding
Material 3 Minimum | $48 \times 48\,\text{dp}$ | $\ge 8\,\text{dp}$ inter-element padding
Safe Area Insets | Top notch, dynamic island, home indicator | Always wrap root in `SafeAreaView` or `.safeAreaPadding()`

---

## 2. Platform Color & Typography Systems

- **iOS (SwiftUI)**: Use semantic dynamic colors (`Color(uiColor: .systemBackground)`, `Color(uiColor: .secondarySystemBackground)`) and San Francisco fonts with Dynamic Type support.
- **Android (Jetpack Compose / Material 3)**: Use `MaterialTheme.colorScheme` (Primary, OnPrimary, SurfaceContainer) and Roboto / Google Sans with predictive back animation.
