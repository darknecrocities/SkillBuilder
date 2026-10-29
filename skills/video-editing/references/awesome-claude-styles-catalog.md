# Awesome Claude Motion Graphics: The 17 Styles Catalog

Reference catalog compiled from [Awesome Claude Motion Graphics](https://awesomeclaude.ai/claude-motion-graphics). Every style is defined by mathematical easing curves, hex color constraints, entrance/exit rules, and an explicit avoid list.

---

## 1. Swiss Grid & Kinetic Type
- **Summary**: A modular grid, one typeface, one signal colour. Type snaps into cells like a printing press.
- **Rules**:
  - One easing curve for snaps: `cubic-bezier(.7, 0, .2, 1)`. Linear only for lines being drawn.
  - Entrances are wipes or clip reveals, never fades. Deletions are hard cuts.
  - Exactly one element carries the signal colour per shot. That element is the subject.
  - Every position lands on a 12-column grid with 4% margins.
- **Palette**: Pitch Black `#000000`, Paper White `#FFFFFF`, Signal Accent (e.g. `#E63946` or Stark White).
- **Avoid**: Overshoot, springs, drop shadows, more than one typeface, centred-everything layouts.

## 2. Flat Vector Explainer
- **Summary**: Flat colour shapes and simple geometric characters with springy, confident movement.
- **Rules**:
  - Entrances overshoot with `cubic-bezier(0.34, 1.56, 0.64, 1)` and settle within 12 frames.
  - Stagger groups by 2 to 4 frames, never all at once.
  - Transitions are carried by an element: a shape grows to fill the frame and becomes the next background.
  - Four to five flat colours, no gradients, no outlines thinner than 3px at 1080p.
- **Avoid**: Stock-illustration people with tiny heads, gradients, crossfades between scenes.

## 3. Shape Morph & Liquid
- **Summary**: One shape keeps turning into the next. The story is told by transformation, not cuts.
- **Rules**:
  - There are no cuts. Every new idea grows out of the previous shape.
  - Each morph takes 18 to 30 frames and passes through a readable in-between shape.
  - Hold each finished shape at least 1 second so it reads.
  - Liquid joins use smooth-min blending, never a hard overlap.
- **Avoid**: Morphs that pass through a shapeless blob, constant motion with no holds.

## 4. Single Line & Live Drawing
- **Summary**: One ink line draws itself, never lifts, and becomes the next picture. The camera follows the pen.
- **Rules**:
  - The line draws at a steady speed, linear easing, about 800px per second at 1080p.
  - The camera pans to keep the pen tip in the middle third of the frame.
  - One fill moment: the closed line floods with colour on a downbeat.
  - Constant stroke width, round caps.
- **Avoid**: Many lines drawing at once, fades in, text typed letter by letter.

## 5. Data Story
- **Summary**: Real numbers drawn mark by mark, with one annotation that says why it matters.
- **Rules**:
  - One reading per screen. Never show two charts at once.
  - Bars grow from the baseline in 20 frames with ease-out; counters roll to the exact value and stop.
  - Every number on screen comes from the data you were given.
  - Axis labels at least 28px at 1080p so they read on a phone.
- **Avoid**: 3D charts, rainbow palettes, decorative gridlines, numbers that are not in the source.

## 6. Isometric Miniature World
- **Summary**: A tidy isometric diorama that builds itself, block by block, and opens up to show how things work.
- **Rules**:
  - True isometric angles (30 degrees). The camera slides, it never rotates in perspective.
  - Objects drop in from 40px above with a small bounce, staggered by 3 frames.
  - Three tones per material: top light, left mid, right dark.
  - Things open to reveal their insides instead of cutting to a new scene.
- **Avoid**: Perspective cameras, realistic textures, labels floating without leader lines.

## 7. Dark Tech Keynote
- **Summary**: Near-black stage, hairline grid, one accent, light sweeping across a product, one giant number.
- **Rules**:
  - Slow, long-tail easing: `cubic-bezier(.16, 1, .3, 1)`, 30 to 45 frames per move.
  - One giant number per piece, 30% of frame height, counted up to its exact value.
  - Reveals come from light: a soft sweep passes and leaves the object lit.
  - The accent colour appears on one thing only.
- **Avoid**: Lens flares, neon glow, particle bursts, more than one accent colour.

## 8. Living UI Screencast
- **Summary**: Looks like a real screen recording, but every pixel is rebuilt in code, so the camera can zoom and the UI can act.
- **Rules**:
  - Rebuild the real UI with real copy and colours. Never use static screenshots.
  - The cursor moves on eased curves, 20 to 30 frames per move, and pauses 8 frames before each click.
  - Zoom to 1.6x on the detail that matters, then pull back.
  - One action every 3 to 4 seconds so the viewer can follow.
- **Avoid**: Fake features, cursor teleporting, lorem ipsum, zooming on nothing.

## 9. HUD & Terminal
- **Summary**: Wireframes, lock-on brackets, rolling numbers and monospace glyph grids.
- **Rules**:
  - All text is monospace and sits on a character grid.
  - Numbers roll through random glyphs for 6 to 10 frames before settling on the real value.
  - Brackets lock onto a target in 3 steps: wide, tighter, locked with a tick.
  - Two colours max on the dark field, plus dim grid lines.
- **Avoid**: Heavy glow and bloom, glitch tearing, unreadable tiny text.

## 10. Watercolour & Ink
- **Summary**: Brush strokes paint themselves on textured paper. Washes bleed past the lines.
- **Rules**:
  - Everything is painted with strokes. No plain vector shapes.
  - Washes reveal over 15 to 25 frames and bleed 4 to 8px past the ink line.
  - Paper texture shows through everything.
- **Avoid**: Uniform digital airbrush, shapes that pop in fully opaque.

## 11. Editorial Print Layout & Collage
- **Summary**: High-fashion print layouts, strong editorial typography, and disciplined white space.
- **Rules**:
  - Strict typographic scale (Headline 96pt, Body 24pt, Caption 12pt).
  - Clean rectangular clipping boundaries.

## 12. Retro 8-Bit Pixel Art
- **Summary**: Authentic retro low-res pixel matrices with strict color palettes (PICO-8, GameBoy).
- **Rules**:
  - Pixel-perfect integer nearest-neighbor scaling.
  - Stepped frame rate (10-12 FPS) for character animation.

## 13. 3D Geometric Clay & Orthographic Solids
- **Summary**: Tactile matte solids, soft directional shadows, studio lighting, zero specular glare.
- **Rules**:
  - Diffuse PBR shading, zero harsh gloss.

## 14. 3D Split-Flap Perspective Flip
- **Summary**: Mechanical card flips along the X-axis simulating an airport departure board or physical flipper.
- **Rules**:
  - $\text{scale\_y} = \sin(p \cdot \frac{\pi}{2})$ from $0 \to 1$.
  - FreeType vector typography rendered onto sub-canvas and squashed vertically.
  - Snaps into place with HUD lock-on brackets on completion.

## 15. Minimalist Monochrome Brand Film
- **Summary**: Stark high-contrast `#000000` and `#FFFFFF` storytelling.
- **Rules**:
  - Vector FreeType dynamic font scaling (`font_size = int(base_size * zoom)`).
  - Zero bitmap interpolation blur.

## 16. Concentric Sonar & Verification Radar
- **Summary**: Circular sonar waves rippling outward and snapping onto verification targets with crosshairs.
- **Rules**:
  - Expanding concentric rings with smooth cosine falloff.
  - Reticle crosshair with coordinate readouts.

## 17. Broadcast Director Harness
- **Summary**: Full Python-to-FFmpeg RGB24 raw pipe with audio synchronization and speech ducking.
- **Rules**:
  - 128 BPM grid (1 beat = 0.46875s, 1 bar = 1.875s).
  - Guaranteed speech cushion $\ge 0.85$s.
  - Ducking music by $-6.5$dB during dialogue.
