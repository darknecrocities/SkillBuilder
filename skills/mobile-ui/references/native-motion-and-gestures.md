# Native Motion, Spring Physics & Tactile Feedback

---

## 1. Physically-Modeled Springs

Avoid linear duration-based easing (`ease-in-out` 300ms). Use physically grounded spring damping:

```swift
// SwiftUI Interactive Spring
withAnimation(.interactiveSpring(response: 0.35, dampingFraction: 0.86, blendDuration: 0.2)) {
    isExpanded.toggle()
}
```

```kotlin
// Jetpack Compose Spring Spec
val animatedOffset by animateFloatAsState(
    targetValue = targetX,
    animationSpec = spring(
        dampingRatio = Spring.DampingRatioMediumBouncy,
        stiffness = Spring.StiffnessMedium
    )
)
```

---

## 2. Haptic Feedback Standards

Feedback Level | Use Case
:--- | :---
Light / Selection | Picker scrolling, segment switching, tab selection
Medium / Impact | Toggle switch flipping, button tap confirmation
Heavy / Warning | Destructive action confirmation, long-press trigger
Error | Transaction rejected, form validation error
