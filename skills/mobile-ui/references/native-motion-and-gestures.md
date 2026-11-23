# Native Motion, Spring Physics & Tactile Feedback Manual

> **Objective**: Deliver 120Hz frame-accurate native mobile interactions across SwiftUI, Jetpack Compose, React Native Reanimated 3, and Flutter Impeller.

---

## 1. Harmonic Spring Parameters by Interaction Tier

Replace duration-based CSS-style `easeInOut(300ms)` with velocity-preserving springs:

| Interaction Type | SwiftUI (`response`, `dampingFraction`) | Compose (`stiffness`, `dampingRatio`) | Reanimated 3 (`stiffness`, `damping`) |
| :--- | :--- | :--- | :--- |
| **Snappy Toggle / Chip** | `response: 0.25, dampingFraction: 0.78` | `StiffnessMedium, 0.78f` | `stiffness: 260, damping: 22` |
| **Card / Sheet Morph** | `response: 0.36, dampingFraction: 0.82` | `StiffnessMediumLow, 0.82f` | `stiffness: 180, damping: 20` |
| **Confirmation Pop** | `response: 0.28, dampingFraction: 0.66` | `StiffnessMedium, DampingRatioMediumBouncy` | `stiffness: 240, damping: 14` |

---

## 2. Platform-Native Motion Implementations

### iOS SwiftUI (`PhaseAnimator` & `matchedGeometryEffect`)
```swift
struct FeedCardView: View {
    let item: FeedItem
    var namespace: Namespace.ID
    var body: some View {
        VStack(alignment: .leading, spacing: 12) {
            Image(item.heroImage)
                .matchedGeometryEffect(id: "image_\(item.id)", in: namespace)
                .frame(maxWidth: .infinity, maxHeight: 240)
                .clipShape(RoundedRectangle(cornerRadius: 20, style: .continuous))
            Text(item.title).matchedGeometryEffect(id: "title_\(item.id)", in: namespace)
        }
        .padding(16)
        .background(.ultraThinMaterial)
        .clipShape(RoundedRectangle(cornerRadius: 24, style: .continuous))
        .overlay(RoundedRectangle(cornerRadius: 24, style: .continuous).stroke(Color.white.opacity(0.12), lineWidth: 1))
    }
}
```
- Prepare `UIImpactFeedbackGenerator(style: .medium)` before gesture threshold crossings (`generator.prepare()`).

### Android Jetpack Compose (`SharedTransitionLayout` & `PredictiveBackHandler`)
```kotlin
@Composable
fun SharedElementFeedCard(item: FeedItem, sharedScope: SharedTransitionScope, visScope: AnimatedVisibilityScope) {
    with(sharedScope) {
        Surface(
            shape = RoundedCornerShape(24.dp),
            tonalElevation = 2.dp,
            modifier = Modifier.sharedBounds(
                rememberSharedContentState(key = "card_${item.id}"),
                animatedVisibilityScope = visScope,
                boundsTransform = { _, _ -> spring(dampingFraction = 0.78f, stiffness = Spring.StiffnessMediumLow) }
            )
        ) { /* Card Content */ }
    }
}
```
- Use `LookaheadScope` / `SharedTransitionLayout` for continuous bounds morphing without layout re-measurement jank.
- Handle `PredictiveBackHandler` (`CancellationException` springs back cleanly when swipe is aborted).

### React Native (`react-native-reanimated` v3 Worklets)
- Mark gesture callbacks `'worklet';` so drag physics run 100% on the native UI thread with zero JS bridge round-trips.
- Trigger `Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light)` via `runOnJS` only when crossing discrete snap detents.

### Flutter (120Hz Impeller)
- Use `AnimationController.unbounded` paired with `SpringSimulation` and `TickerProviderStateMixin`, disposing controllers in `dispose()`.

---

## 3. Haptic Semantics Matrix

| Feedback Tier | Trigger Condition | Platform API |
| :--- | :--- | :--- |
| **Selection / Tick** | Rotary encoder detent, picker snap | `UISelectionFeedbackGenerator`, `HapticFeedback.selectionClick()` |
| **Light / Medium Impact** | Primary toggle, card lock-in | `UIImpactFeedbackGenerator(.medium)`, `HapticFeedbackType.TextHandleMove` |
| **Notification Success / Error** | Persisted save, validation reject | `UINotificationFeedbackGenerator`, `HapticFeedback.heavyImpact()` |
