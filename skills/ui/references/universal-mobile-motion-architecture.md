# Universal Mobile Motion Architecture Guide

This guide establishes the engineering standard for physical spring dynamics, 120Hz UI-thread animation pipelines, and tactile haptic feedback across all modern mobile platforms:
1. **React Native (Expo / Reanimated 3 / Gesture Handler)**
2. **Native iOS (SwiftUI / CoreHaptics / Metal)**
3. **Native Android (Jetpack Compose / Kotlin)**
4. **Flutter (Dart / Impeller GPU)**

---

## 1. The Physics of High-Craft Mobile Interfaces

Generic AI-generated mobile applications suffer from three critical flaws:
1. **Thread Starvation**: Running animations on the JavaScript/main event loop, dropping frames during garbage collection or background I/O.
2. **Numb Interactions**: Zero physical tactile response; taps feel dead and synthetic on modern smartphones equipped with linear resonant actuators.
3. **Artificial Easing**: Using robotic linear cubic-beziers instead of mass-spring-damper harmonic oscillators ($m\ddot{x} + c\dot{x} + kx = 0$).

---

## 2. Platform Motion Pipeline Comparison

| Platform | Animation Engine | Gesture Handling | Haptic Feedback API | 120Hz Sync Mechanism |
| :--- | :--- | :--- | :--- | :--- |
| **React Native** | Reanimated 3 Worklets (C++ UI Thread) | `react-native-gesture-handler` | `expo-haptics` / `selectionAsync()` | CADisplayLink / Choreographer |
| **iOS (SwiftUI)** | `withAnimation(.interactiveSpring)` | `DragGesture(minimumDistance: 0)` | `sensoryFeedback()` / `UIImpactFeedbackGenerator` | ProMotion Display Link |
| **Android (Compose)** | `Animatable.animateTo(spring())` | `Modifier.pointerInput` | `LocalHapticFeedback` / `HapticFeedbackType` | SurfaceFlinger Choreographer |
| **Flutter** | `AnimationController.unbounded` + `SpringSimulation` | `GestureDetector` / Pan | `HapticFeedback.selectionClick()` | Impeller AOT Engine |

---

## 3. React Native: 120Hz UI-Thread Worklets

In React Native, gesture updates must **never cross the JavaScript bridge** during active dragging. Reanimated worklets execute directly on the native runtime thread.

```tsx
import React from 'react';
import { View, StyleSheet } from 'react-native';
import { Gesture, GestureDetector } from 'react-native-gesture-handler';
import Animated, {
  useSharedValue,
  useAnimatedStyle,
  withSpring,
  runOnJS,
} from 'react-native-reanimated';
import * as Haptics from 'expo-haptics';

export function TactileSpringDial() {
  const rotation = useSharedValue(0);
  const lastDetent = useSharedValue(0);
  const detentStep = 15; // 15 degrees per detent tick

  function triggerDetentHaptic() {
    Haptics.selectionAsync();
  }

  const panGesture = Gesture.Pan()
    .onUpdate((e) => {
      // 1px delta = 0.8 degrees of rotation
      rotation.value = rotation.value - e.changeY * 0.8;

      // Check for discrete detent tick boundary crossing
      if (Math.abs(rotation.value - lastDetent.value) >= detentStep) {
        lastDetent.value = rotation.value;
        runOnJS(triggerDetentHaptic)();
      }
    })
    .onEnd(() => {
      // Snap to nearest detent tick using physical spring
      const target = Math.round(rotation.value / detentStep) * detentStep;
      rotation.value = withSpring(target, {
        stiffness: 350,
        damping: 28,
        mass: 1.0,
      });
    });

  const animatedDialStyle = useAnimatedStyle(() => ({
    transform: [{ rotate: `${rotation.value}deg` }],
  }));

  return (
    <GestureDetector gesture={panGesture}>
      <Animated.View style={[styles.dialKnob, animatedDialStyle]} />
    </GestureDetector>
  );
}

const styles = StyleSheet.create({
  dialKnob: {
    width: 140,
    height: 140,
    borderRadius: 70,
    backgroundColor: '#18181b',
    borderWidth: 1.5,
    borderColor: '#3f3f46',
  },
});
```

---

## 4. Native iOS: SwiftUI & CoreHaptics

SwiftUI provides physical spring parameterization directly via `.interactiveSpring(response:dampingFraction:blendDuration:)`.

```swift
import SwiftUI

struct TacticalSpringDial: View {
    @State private var currentAngle: Double = 0.0
    @State private var lastHapticAngle: Double = 0.0
    private let detentStep: Double = 12.0 // degrees
    private let impactFeedback = UIImpactFeedbackGenerator(style: .rigid)

    var body: some View {
        ZStack {
            // Machined Dial Face
            Circle()
                .fill(Color(red: 0.09, green: 0.09, blue: 0.11))
                .overlay(Circle().stroke(Color.white.opacity(0.12), lineWidth: 1.5))
                .frame(width: 140, height: 140)
            
            // Needle Indicator
            Capsule()
                .fill(Color(red: 0.96, green: 0.62, blue: 0.04)) // Amber
                .frame(width: 4, height: 24)
                .offset(y: -46)
        }
        .rotationEffect(.degrees(currentAngle))
        .gesture(
            DragGesture(minimumDistance: 0)
                .onChanged { value in
                    currentAngle -= Double(value.translation.height) * 0.05
                    if abs(currentAngle - lastHapticAngle) >= detentStep {
                        impactFeedback.impactOccurred()
                        lastHapticAngle = currentAngle
                    }
                }
                .onEnded { _ in
                    let nearest = (currentAngle / detentStep).rounded() * detentStep
                    withAnimation(.spring(response: 0.35, dampingFraction: 0.72)) {
                        currentAngle = nearest
                    }
                }
        )
        .onAppear {
            impactFeedback.prepare()
        }
    }
}
```

---

## 5. Native Android: Jetpack Compose & LocalHapticFeedback

Android Jetpack Compose uses `Animatable` with `SpringSimulation` to execute non-blocking physical animations on the render thread.

```kotlin
package com.skillbuilder.ui.components

import androidx.compose.animation.core.Animatable
import androidx.compose.animation.core.Spring
import androidx.compose.animation.core.spring
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.gestures.detectDragGestures
import androidx.compose.foundation.layout.size
import androidx.compose.runtime.Composable
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.ui.Modifier
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.drawscope.rotate
import androidx.compose.ui.hapticfeedback.HapticFeedbackType
import androidx.compose.ui.input.pointer.pointerInput
import androidx.compose.ui.platform.LocalHapticFeedback
import androidx.compose.ui.unit.dp
import kotlinx.coroutines.launch
import kotlin.math.abs
import kotlin.math.roundToInt

@Composable
fun TacticalSpringDial() {
    val rotation = remember { Animatable(0f) }
    val scope = rememberCoroutineScope()
    val haptics = LocalHapticFeedback.current
    var lastDetent = remember { 0f }
    val detentStep = 15f

    Canvas(
        modifier = Modifier
            .size(140.dp)
            .pointerInput(Unit) {
                detectDragGestures(
                    onDrag = { change, dragAmount ->
                        change.consume()
                        val next = rotation.value - dragAmount.y * 0.8f
                        scope.launch { rotation.snapTo(next) }

                        if (abs(next - lastDetent) >= detentStep) {
                            haptics.performHapticFeedback(HapticFeedbackType.TextHandleMove)
                            lastDetent = next
                        }
                    },
                    onDragEnd = {
                        val target = (rotation.value / detentStep).roundToInt() * detentStep
                        scope.launch {
                            rotation.animateTo(
                                targetValue = target,
                                animationSpec = spring(
                                    dampingRatio = Spring.DampingRatioMediumBouncy,
                                    stiffness = Spring.StiffnessMediumLow
                                )
                            )
                        }
                    }
                )
            }
    ) {
        val center = Offset(size.width / 2f, size.height / 2f)
        val radius = size.width / 2f

        // Draw dial body
        drawCircle(color = Color(0xFF18181B), radius = radius)
        
        // Draw needle rotated
        rotate(degrees = rotation.value, pivot = center) {
            drawLine(
                color = Color(0xFFF59E0B),
                start = Offset(center.x, center.y - radius + 10.dp.toPx()),
                end = Offset(center.x, center.y - radius + 30.dp.toPx()),
                strokeWidth = 3.dp.toPx()
            )
        }
    }
}
```

---

## 6. Tabular Figures Matrix across Mobile Frameworks

To prevent horizontal number jitter on high-frequency telemetry counters:

| Platform | Code Specification |
| :--- | :--- |
| **React Native** | `style={{ fontVariant: ['tabular-nums'], fontFamily: 'Courier' }}` |
| **iOS (SwiftUI)** | `.font(.system(size: 28, weight: .bold, design: .monospaced)).monospacedDigit()` |
| **Android (Compose)** | `style = TextStyle(fontFeatureSettings = "tnum 1, zero 1", fontFamily = FontFamily.Monospace)` |
| **Flutter** | `style: TextStyle(fontFeatures: [FontFeature.tabularFigures(), FontFeature.slashedZero()])` |

---

## 7. Universal Mobile QA Checklist

- [ ] **Frame Rate Budget**: Stable 60fps on low-end hardware; 120Hz smooth ProMotion/LTPO sync.
- [ ] **Native Threading**: Zero JS-thread calculation during gesture drags.
- [ ] **Tactile Precision**: Haptic feedback triggers only when passing physical detents or boundary collision limits.
- [ ] **Minimum Touch Targets**: 44x44pt on iOS; 48x48dp on Android.
- [ ] **Reduced Motion Support**:
  - React Native: `AccessibilityInfo.isReduceMotionEnabled()`
  - SwiftUI: `@Environment(\.accessibilityReduceMotion) var reduceMotion`
  - Jetpack Compose: `LocalView.current.isAttachedToWindow` / check system animator duration scale
  - Flutter: `MediaQuery.of(context).accessibleNavigation`
