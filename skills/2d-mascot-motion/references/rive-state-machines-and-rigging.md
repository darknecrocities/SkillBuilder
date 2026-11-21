# Rive (`.riv`) State Machines, Rigging & Cross-Platform Integration

> **Objective**: Structure `.riv` character files and runtime controllers so animations are lightweight (`< 150 KB`), interactive, leak-free, and deterministic across Web, Flutter, React Native, iOS, and Android.

---

## 1. Rive Artboard & Rig Hierarchy

Organize artboards cleanly inside Rive before exporting `.riv`:

```text
MascotArtboard (512x512, origin center-bottom or center)
├── root_anchor (Translation / global squash-stretch pivot)
│   ├── ground_contact_shadow (subtle radial opacity scale linked to root Y)
│   ├── body_pelvis
│   │   ├── torso_shell (clipping path + 3-value shadow plane)
│   │   └── head_group (pivot at neck joint)
│   │       ├── antenna_or_ears (secondary follow-through delay +40ms)
│   │       ├── visor_or_face_plate
│   │       │   ├── eyes_group (blink scaleY -> 0.05)
│   │       │   ├── pupils_track (1D/2D Blend State driven by lookX / lookY)
│   │       │   └── mouth_or_waveform (Idle / Happy / Alert / Thinking visemes)
│   └── limbs_or_badges (optional minimal flippers/hands, <= 25 nodes each)
```

### `.riv` Export Discipline
- **File Size Budget**: `< 150 KB` per `.riv` binary (use vector shapes, trim unused artboards/raster PNGs before export).
- **Named Contract**: Always name the primary state machine `MascotSM` (never leave default `"State Machine 1"` in production apps) and verify input names match runtime bindings exactly.
- **ViewModel Data Binding (Rive 2025+)**: When driving text labels, progress percentages, or color themes dynamically, bind properties via Rive ViewModels rather than duplicating artboards.

---

## 2. Canonical `MascotSM` Layer Architecture

Split concerns across independent additive layers inside Rive so blinking and pointer tracking never fight state transitions:

| Layer Name | Purpose | Inputs Used |
| :--- | :--- | :--- |
| **`BaseBehavior`** | `Idle` <-> `Hover` <-> `Thinking` <-> `Success` <-> `Error` <-> `Sleep` | `isHovered` (Bool), `isThinking` (Bool), `onSuccess` (Trigger), `onError` (Trigger) |
| **`EyeGaze`** | 2D Blend State interpolating pupils + subtle head parallax | `lookX` (`0..100`), `lookY` (`0..100`) |
| **`BlinkCycle`** | Independent randomized `120ms` blink timeline | Auto-looping timer / `isSleeping` |

---

## 3. Production Runtime Patterns

### Web / React (`@rive-app/react-canvas`)
- Preload WASM runtime once at app shell level (`RuntimeLoader.setWasmUrl(...)` if self-hosting for CSP/offline).
- Pause Rive playback when scrolled off-screen via `IntersectionObserver` (`rive.pause()` / `rive.play()`).
- Always call `rive?.cleanup()` on component unmount (see [templates/RiveMascotStage.tsx](../templates/RiveMascotStage.tsx)).

### Flutter (`rive` package — 120Hz Impeller Safe)
```dart
class MascotStage extends StatefulWidget {
  const MascotStage({super.key, required this.isThinking});
  final bool isThinking;

  @override
  State<MascotStage> createState() => _MascotStageState();
}

class _MascotStageState extends State<MascotStage> {
  StateMachineController? _controller;
  SMIBool? _thinkingInput;

  void _onInit(Artboard artboard) {
    final ctrl = StateMachineController.fromArtboard(artboard, 'MascotSM');
    if (ctrl == null) return;
    artboard.addController(ctrl);
    _controller = ctrl;
    _thinkingInput = ctrl.getBoolInput('isThinking');
    _thinkingInput?.value = widget.isThinking;
  }

  @override
  void didUpdateWidget(covariant MascotStage oldWidget) {
    super.didUpdateWidget(oldWidget);
    if (oldWidget.isThinking != widget.isThinking) {
      _thinkingInput?.value = widget.isThinking;
    }
  }

  @override
  void dispose() {
    _controller?.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final reduceMotion = MediaQuery.disableAnimationsOf(context);
    return AspectRatio(
      aspectRatio: 1,
      child: RiveAnimation.asset(
        'assets/mascot.riv',
        stateMachines: const ['MascotSM'],
        onInit: _onInit,
        animations: reduceMotion ? const ['IdleStatic'] : const [],
      ),
    );
  }
}
```

### React Native / Native iOS & Android
- **React Native**: Use `rive-react-native` with `stateMachineName="MascotSM"`, explicit `style={{ aspectRatio: 1 }}`, and `setInputState` calls guarded by mount checks.
- **iOS (`RiveRuntime`)**: `RiveViewModel(fileName: "mascot", stateMachineName: "MascotSM")` + `UIAccessibility.isReduceMotionEnabled` guard.
- **Android (`rive-android`)**: Bind `RiveAnimationView` inside `AndroidView` (Compose) and call `controller.reset()` / release in `DisposableEffect`.
