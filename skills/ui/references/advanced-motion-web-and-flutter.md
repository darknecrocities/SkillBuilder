# Advanced Motion Architecture: Web & Flutter Guide

This guide establishes the production engineering framework for spring physics, gesture orchestration, and tactile feedback across **Web (React / Framer Motion)** and **Mobile (Flutter / Dart / Impeller)**.

---

## 1. Physical Springs vs. Artificial Easing Curves

Artificial cubic-bezier curves (e.g., standard `ease-in-out`) feel robotic, linear, and synthetic because real physical objects possess mass, inertia, and friction. 

Spring dynamics use the harmonic oscillator differential equation:
$$m \frac{d^2x}{dt^2} + c \frac{dx}{dt} + k x = 0$$

Where:
- $m$: Mass (inertia)
- $c$: Damping coefficient (resistance/viscosity)
- $k$: Stiffness (spring tension)

### Damping Ratio ($\zeta = \frac{c}{2\sqrt{mk}}$)

| Damping Ratio | Dynamic Behavior | Recommended Interface Use |
| :--- | :--- | :--- |
| $\zeta < 1.0$ (Underdamped) | Oscillates across target value before settling | Delight micro-interactions, toggles, badge bounces ($\zeta \approx 0.70 - 0.85$) |
| $\zeta = 1.0$ (Critically Damped) | Settles at target in minimum time with **zero overshoot** | Industrial encoders, CAD viewports, tactical switches, modal sheets |
| $\zeta > 1.0$ (Overdamped) | Slowly approaches target without oscillation | Viscous drag sliders, heavy mechanical machinery sliders |

---

## 2. The Production Spring Parameter Matrix

| Profile Name | Mass ($m$) | Stiffness ($k$) | Damping ($c$) | Target Sensation |
| :--- | :--- | :--- | :--- | :--- |
| **Tactical Snappy** | `1.0` | `380` | `30` | Precision toggle, keyboard shortcut response |
| **Spatial Card** | `1.0` | `220` | `24` | 3D tilt, magnetic card tracking, dialog pop |
| **Mechanical Dial** | `1.2` | `140` | `18` | Rotary knob, heavy scroll thumb, detent snap |
| **Gentle Drawer** | `1.0` | `100` | `16` | Bottom sheet reveal, sidebar sliding transition |

---

## 3. Web Motion Architecture (React & Framer Motion)

### 3.1 Zero-Re-Render Gesture Pipeline

Updating React state on `mousemove` or pointer drag triggers re-renders on every frame, degrading performance below 60fps. Framer Motion's `useMotionValue` and `useTransform` mutate transform matrices directly in the DOM without React virtual DOM re-renders.

```tsx
import { motion, useMotionValue, useTransform, useSpring } from 'framer-motion';

export function MagneticControl() {
  const x = useMotionValue(0);
  const y = useMotionValue(0);

  // Smooth raw pointer coordinates with physical spring
  const springConfig = { stiffness: 250, damping: 20 };
  const smoothX = useSpring(x, springConfig);
  const smoothY = useSpring(y, springConfig);

  // Derived 3D rotation transforms
  const rotateX = useTransform(smoothY, [-100, 100], [15, -15]);
  const rotateY = useTransform(smoothX, [-100, 100], [-15, 15]);

  function handlePointerMove(e: React.PointerEvent<HTMLDivElement>) {
    const rect = e.currentTarget.getBoundingClientRect();
    const centerX = rect.left + rect.width / 2;
    const centerY = rect.top + rect.height / 2;
    x.set(e.clientX - centerX);
    y.set(e.clientY - centerY);
  }

  function handlePointerLeave() {
    x.set(0);
    y.set(0);
  }

  return (
    <motion.div
      onPointerMove={handlePointerMove}
      onPointerLeave={handlePointerLeave}
      style={{
        rotateX,
        rotateY,
        transformStyle: 'preserve-3d',
      }}
      className="h-48 w-48 rounded-xl bg-zinc-900 border border-zinc-800"
    />
  );
}
```

### 3.2 Shared Element Morphing (`layoutId`)

Use `layoutId` to morph continuous elements (active tabs, floating highlights) across distinct DOM subtrees without calculating bounding rects manually:

```tsx
{isActive && (
  <motion.div
    layoutId="active-pill"
    className="absolute inset-0 rounded-full bg-zinc-800"
    transition={{ type: 'spring', stiffness: 350, damping: 30 }}
  />
)}
```

---

## 4. Mobile Motion Architecture (Flutter & Impeller)

### 4.1 Impeller 120Hz GPU Rendering

On iOS and modern Android, Flutter utilizes the Impeller engine. Impeller compiles all shaders Ahead-of-Time (AOT), eliminating shader compilation jank. To maintain 120Hz:
1. Isolate animated subtrees using `RepaintBoundary`.
2. Do not call `setState()` in tick loops; use `AnimatedBuilder` or `CustomPainter`.
3. Animate transforms and opacities rather than layout constraints (`width`, `height`, `padding`).

### 4.2 Realistic Springs with `AnimationController.unbounded`

A standard `AnimationController` clamps values between `lowerBound: 0.0` and `upperBound: 1.0`. Any spring with $\zeta < 1$ will have its oscillation clipped at `1.0`. `AnimationController.unbounded(vsync: this)` allows natural physical overshoot.

```dart
import 'package:flutter/material.dart';
import 'package:flutter/physics.dart';
import 'package:flutter/services.dart';

class TacticalSpringDial extends StatefulWidget {
  const TacticalSpringDial({super.key});

  @override
  State<TacticalSpringDial> createState() => _TacticalSpringDialState();
}

class _TacticalSpringDialState extends State<TacticalSpringDial>
    with SingleTickerProviderStateMixin {
  late final AnimationController _controller;
  double _lastTickAngle = 0.0;
  static const double _tickStep = 0.15; // ~8.6 degrees per detent

  @override
  void initState() {
    super.initState();
    // Unbounded controller preserves spring overshoot past 1.0
    _controller = AnimationController.unbounded(vsync: this);
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  void _onPanUpdate(DragUpdateDetails details) {
    _controller.value += details.delta.dy * 0.01;

    // Trigger physical haptic feedback when crossing detent ticks
    if ((_controller.value - _lastTickAngle).abs() >= _tickStep) {
      HapticFeedback.selectionClick();
      _lastTickAngle = _controller.value;
    }
  }

  void _onPanEnd(DragEndDetails details) {
    // Snap to nearest detent tick using SpringSimulation
    final currentVal = _controller.value;
    final targetVal = (currentVal / _tickStep).round() * _tickStep;
    final velocity = details.velocity.pixelsPerSecond.dy * 0.01;

    final spring = SpringDescription(
      mass: 1.0,
      stiffness: 350.0,
      damping: 26.0,
    );

    final simulation = SpringSimulation(
      spring,
      currentVal,
      targetVal,
      velocity,
    );

    _controller.animateWith(simulation);
  }

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onPanUpdate: _onPanUpdate,
      onPanEnd: _onPanEnd,
      child: RepaintBoundary(
        child: AnimatedBuilder(
          animation: _controller,
          builder: (context, child) {
            return Transform.rotate(
              angle: _controller.value,
              child: child,
            );
          },
          child: Container(
            width: 140,
            height: 140,
            decoration: const BoxDecoration(
              shape: BoxShape.circle,
              color: Color(0xFF18181B),
            ),
          ),
        ),
      ),
    );
  }
}
```

---

## 5. Haptic Feedback Tiering for Touch Interfaces

Haptic feedback bridges visual and tactile reality. Reserve haptic signals for physical events:

1. `HapticFeedback.selectionClick()`: Rotary encoder detents, picker scrolling, segment switching.
2. `HapticFeedback.lightImpact()`: Button tap, toggle activation, drag pick-up.
3. `HapticFeedback.mediumImpact()`: Drop snap, boundary lock, collision against constraint limits.
4. `HapticFeedback.heavyImpact()`: Destructive actions, safety lock trip, emergency override.

---

## 6. Motion QA & Accessibility Checklist

- [ ] **Reduced Motion Support**:
  - Web: Respect `prefers-reduced-motion: reduce` (`useReducedMotion()` in Framer Motion).
  - Flutter: Check `MediaQuery.of(context).accessibleNavigation`.
- [ ] **Frame Rate Budget**: 60fps minimum on low-end hardware; 120fps on ProMotion displays.
- [ ] **Zero Layout Thrashing**: Zero changes to `top`, `left`, `width`, `height` in high-frequency animation loops. Animate only `transform` and `opacity`.
- [ ] **Zero Synthetic Easing**: Zero robotic linear/ease-in-out loops on interactive components. Every user interaction must use mass-stiffness-damping spring physics.
