# Playbook: Responsive & Adaptive Mobile Layouts (`mobile-responsive`)

Use when building, fixing, or reviewing responsive iOS (SwiftUI/UIKit), Android (Jetpack Compose/M3), React Native, or Flutter layouts across phones, foldables, tablets, Split View, and orientation changes.

## Steps
1. **Prune Opposite Platform (PDS)**: Mount `/mobile-ui` and prune `/web-ui` (`~1,850` tokens saved). If spawning subagents, Line 1 MUST read `skills/darknecrostack/worker.md`.
2. **Lock the 3 Window Classes Before Writing Views**: Size strictly from active container/window bounds—never `UIScreen.main.bounds`, module-scope `Dimensions.get("window")`, `MediaQuery.of(context).size`, hardcoded phone widths (`375`, `390`, `414`, `430`), or portrait-only locks:
   - **Compact (`< 600 dp/pt`)**: Single-column vertical stack, bottom tab/navigation bar, modal bottom sheets.
   - **Medium (`600–839 dp/pt`)**: `NavigationRail` / 2-column adaptive grid (`160–200pt` min card width), foldable hinge awareness.
   - **Expanded (`>= 840 dp/pt`)**: Permanent drawer / `NavigationSplitView` / 2–3 pane `ListDetailPaneScaffold`, with readable prose capped at `maxWidth <= 680–720 dp/pt`.
3. **Use State-Preserving Native Adaptive Primitives**:
   - **iOS (SwiftUI)**: `horizontalSizeClass` + `AnyLayout` (`VStackLayout` <-> `HStackLayout` without resetting `@State`), `ViewThatFits`, `NavigationSplitView`, `LazyVGrid([GridItem(.adaptive(minimum: 160, maximum: 320))])`.
   - **Android (Jetpack Compose)**: `currentWindowAdaptiveInfo().windowSizeClass`, `NavigationSuiteScaffold` (Bottom Bar -> Rail -> Drawer), `ListDetailPaneScaffold` / `SupportingPaneScaffold`, `FoldingFeature` hinge avoidance, `LazyVerticalGrid(GridCells.Adaptive(160.dp))`, `FlowRow`.
   - **Cross-Platform**: `useWindowDimensions()` (React Native) or `LayoutBuilder` + `MediaQuery.sizeOf(context)` (Flutter).
4. **Enforce Safe Areas, Scaling & Touch Ergonomics**:
   - Apply `.safeAreaInset` (iOS) / `WindowInsets.systemBars` + `Modifier.imePadding()` (Android) / `SafeAreaView` (RN) / `SafeArea` (Flutter).
   - Keep hit targets `>= 44x44 pt` (iOS) / `>= 48x48 dp` (Android) and use `minHeight`/`heightIn(min=)` instead of fixed heights on text containers so `200%` Dynamic Type / `sp` font scaling never truncates.
5. **Verify & Prove (`[measured]`)**: Run `python3 skills/mobile-ui/scripts/verify_mobile_ui_hygiene.py --path .` (`MOB-001`..`MOB-006`) and verify Compact Phone, Medium Foldable/Split View, Expanded Tablet, and `200%` text scaling.
