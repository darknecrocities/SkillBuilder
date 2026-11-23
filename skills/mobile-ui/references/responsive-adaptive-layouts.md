# Responsive & Adaptive Mobile Layouts (iOS & Android)

> **Objective**: Ensure every native screen scales gracefully from compact phones to foldables, Split View, Stage Manager, and tablets without clipped text, lost scroll state, or portrait-only locks.

---

## 1. Unified Breakpoint & Size-Class Matrix

| Window Width Class | iOS (`horizontalSizeClass`) | Android (`WindowWidthSizeClass`) | Navigation Chrome | Content Layout Pattern |
| :--- | :--- | :--- | :--- | :--- |
| **Compact (`< 600 dp/pt`)** | `.compact` (iPhone portrait, iPad `1/3` Split View) | `COMPACT` (`< 600 dp`) | Bottom `TabView` / `NavigationBar` | Single-column vertical scroll, modal sheets |
| **Medium (`600–839 dp/pt`)** | `.compact` or `.regular` (iPad `1/2` Split View, mini portrait) | `MEDIUM` (`600–839 dp`, unfolded foldables) | `NavigationRail` / adaptive sidebar | 2-column grid (`160–200pt` min tile), `FlowRow` |
| **Expanded (`>= 840 dp/pt`)** | `.regular` (iPad landscape, Stage Manager) | `EXPANDED` (`>= 840 dp`, tablets, DeX) | `NavigationSplitView` / permanent `NavigationDrawer` | 2–3 pane `ListDetailPaneScaffold`, prose `maxWidth <= 680–720` |

---

## 2. iOS Adaptive SwiftUI Patterns

- **Preserve State Across Layout Changes**: Switch `VStackLayout` <-> `HStackLayout` via `AnyLayout` driven by `@Environment(\.horizontalSizeClass)` so child `@State` and scroll position survive rotation or Split View resizing.
- **Zero Truncation (`ViewThatFits`)**: Prefer `ViewThatFits(in: .horizontal)` for action bars/badges instead of fixed truncation or `UIScreen.main.bounds` (deprecated; breaks iPad multi-window).
- **Dynamic Type (`200%`)**: Use `@ScaledMetric` for icon/spacer scaling and `.frame(minHeight: 44)` instead of fixed `.frame(height: 44)` on text rows.

```swift
struct AdaptiveSummaryRow: View {
    @Environment(\.horizontalSizeClass) private var hSize
    var body: some View {
        let layout = hSize == .regular ? AnyLayout(HStackLayout(spacing: 16)) : AnyLayout(VStackLayout(spacing: 12))
        layout {
            MetricPanel()
            ActionPanel()
        }
        .frame(maxWidth: 700)
        .safeAreaInset(edge: .bottom) { PrimaryActionBar() }
    }
}
```

---

## 3. Android Jetpack Compose & Material 3 Adaptive

- **WindowSizeClass & NavigationSuiteScaffold**: Drive top-level chrome from `currentWindowAdaptiveInfo().windowSizeClass` so Bottom `NavigationBar` automatically morphs into `NavigationRail` (`Medium`) and permanent `NavigationDrawer` (`Expanded`).
- **Two-Pane & Foldable Hinge Safety**: Use `ListDetailPaneScaffold` (`rememberListDetailPaneScaffoldNavigator()`) and respect `FoldingFeature` hinge bounds from Jetpack `WindowManager` so controls never straddle a physical fold crease.
- **Readable Measure & Font Scaling**: Cap centered prose columns with `Modifier.widthIn(max = 680.dp)`, use `LazyVerticalGrid(GridCells.Adaptive(minSize = 160.dp))`, and set `Modifier.heightIn(min = 48.dp)` + `Modifier.imePadding()`.

```kotlin
@Composable
fun AdaptiveCatalogPane(items: List<CatalogItem>, onSelect: (CatalogItem) -> Unit) {
    val windowSize = currentWindowAdaptiveInfo().windowSizeClass
    val columns = if (windowSize.windowWidthSizeClass == WindowWidthSizeClass.COMPACT) 1 else 2
    LazyVerticalGrid(
        columns = GridCells.Adaptive(minSize = if (columns == 1) 300.dp else 180.dp),
        contentPadding = WindowInsets.systemBars.asPaddingValues(),
        modifier = Modifier.fillMaxSize().imePadding()
    ) {
        items(items, key = { it.id }) { item ->
            Surface(modifier = Modifier.heightIn(min = 48.dp)) { CatalogRow(item, onSelect) }
        }
    }
}
```

---

## 4. React Native & Flutter Cross-Platform Parity

| Framework | Reactive Bounds Hook | Adaptive Grid & Chrome | Anti-Pattern to Ban |
| :--- | :--- | :--- | :--- |
| **React Native / Expo** | `const { width } = useWindowDimensions();` | Derive `numColumns` from active `width`, center with `maxWidth: 680`, wrap in `<SafeAreaView>` | Module-level `Dimensions.get("window")` (stale on rotation/Split View) |
| **Flutter** | `LayoutBuilder` + `MediaQuery.sizeOf(context)` | `SliverGridDelegateWithMaxCrossAxisExtent(maxCrossAxisExtent: 240)` + `NavigationBar` -> `NavigationRail` | `MediaQuery.of(context).size` (rebuilds on every keyboard animation frame) |
