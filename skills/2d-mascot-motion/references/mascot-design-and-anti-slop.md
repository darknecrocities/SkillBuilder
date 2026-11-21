# 2D Mascot Design & Anti-Slop Craftsmanship Manual

> **Objective**: Build memorable, expressive 2D characters that survive `32px` avatar crops and `512px` hero stages without looking like AI-generated plastic blobs or generic clip art.

---

## 1. The 5 Anti-Slop Mascot Failure Modes

1. **The Shiny Purple 3D-Fake Blob**: Muddy multi-stop radial gradients, soft airbrush shadows, and generic glowing eyes. Fails completely in monochrome, dark mode, and small sizes.
2. **Anatomical Hallucinations**: Extra limbs, asymmetrical mismatched eyes without intent, melting outlines, or 500-node auto-traced vector spaghetti.
3. **Emoji Substitution**: Dropping `🤖` or `👾` inside a `rounded-full` purple gradient circle and calling it a mascot.
4. **Corporate Memphis / Alegria Cloning**: Tiny pin-heads, rubber-hose purple arms, and lifeless flat smiles copied from generic SaaS templates.
5. **Motion Overload**: Constant fast bouncing (`translateY(-12px)` every `1s` infinite) that distracts from reading and violates `prefers-reduced-motion`.

---

## 2. Geometric Shape Language & Silhouette Discipline

Every durable mascot starts with **3–5 primary geometric primitives** before adding facial expression or secondary trim:

| Archetype | Primary Silhouette | Visual Character Trait | Ideal Product Fit |
| :--- | :--- | :--- | :--- |
| **Orbital / Companion** | Circle + chamfered visor | Friendly, approachable, focused | Onboarding guides, AI assistants, learning apps |
| **Architect / Toolbot** | Rounded squircle (`rx=22%`) + dual optics | Dependable, engineered, precise | DevTools, CLI dashboards, analytics portals |
| **Sentinel / Shield** | Hexagon / chamfered crest + crisp eyes | Protective, calm, authoritative | Security tools, local-first vaults, privacy apps |
| **Kinetic Spark** | Rounded diamond / capsule + antenna | Nimble, alert, responsive | Real-time automation, search, media converters |

### Mandatory Silhouette & Scale Tests
- **100% Solid Black Test**: Fill the entire mascot silhouette `#000000`. Is the character posture, head/ear/antenna profile, and personality still unmistakable?
- **32px Avatar Test**: Shrink to `32x32px`. Eyes and primary silhouette must stay distinct without thin `0.5px` eyelashes or micro-highlights vanishing into grey mud.

---

## 3. Color Value Separation (The 3-Value Cel Rule)

Avoid muddy 10-stop gradients. Build depth cleanly with **3 calibrated values** (compatible with both light and dark canvases):
1. **Base Fill (60%)**: Calibrated matte body hue (e.g. slate `#1e293b` or warm bone `#f4f4f5`).
2. **Structural Shadow Plane (25%)**: Single crisp vector clip plane `12–18%` darker in OKLCH lightness (never pure black `#000` at 50% opacity).
3. **Single-Zenith Rim Highlight (15%)**: Clean `1.5px–2px` top specular edge or visor reflection (`rgba(255,255,255,0.22)`), giving tactile materiality without plastic gloss.

---

## 4. Optical Eye & Visor Rigging Rules
- **Eye Spacing**: Keep `1.2x` to `1.8x` eye-width separation so expressions read clearly at `48px`.
- **Pupil Track Clamping**: Clamp `lookX` / `lookY` travel to `<= 28%` of the eye socket radius so pupils never clip outside the sclera or cross unnaturally.
- **Blinking Cadence**: Natural double-or-single blink every `3.5s–5.5s` (`110ms` close, `90ms` open), never metronomic `2.00s` loops.
- **Squash & Stretch**: Preserve volume (`scaleX * scaleY ≈ 1.0`): e.g. `scaleY: 0.92, scaleX: 1.08` on anticipation, then `scaleY: 1.06, scaleX: 0.94` on pop.
