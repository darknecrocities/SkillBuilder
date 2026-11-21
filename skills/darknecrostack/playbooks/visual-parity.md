# Playbook: Visual Parity & Anti-Slop UI Audit (`visual-parity`)

Use when building or reviewing UI screens, 2D mascots (`.riv`/SVG), app logos, or editorial assets.

## Steps
1. **Lock Design Grammar First**: Choose 1 art movement (`/ui`: Industrial Tactical, Swiss Editorial, Wabi-Sabi, or Technical CAD) and lock 60-30-10 surface/accent tokens.
2. **Enforce Anti-Slop Replacement Rules**: Zero purple-pink hero gradients, zero 3-card icon grids, zero `zinc-500` low-contrast copy, zero emoji buttons, zero neon halos.
3. **4-Tier Viewport & Touch Audit**: Verify rendering and overflow across `375px`, `768px`, `1280px`, and `1920px+`, ensuring `>=44x44px` tap targets and visible `:focus-visible` rings.
4. **Asset & Mascot Integrity**: Run `verify_mascot_assets.py` (`.riv`/Lottie/SVG node counts + reduced-motion) and `verify_brand_assets.py` (squircle, favicon, `<30` logo nodes).
5. **Computed Parity Check**: Inspect live DOM/screenshot or browser verification output (`CLS < 0.05`, WCAG `>=4.5:1`).
