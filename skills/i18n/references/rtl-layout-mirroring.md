# RTL Layout Mirroring, CSS Logical Properties & Bilingual Routing

> **Objective**: Support bidirectional locales (`ar`, `he`, `fa`, `ur`) and bilingual URL architectures without physical CSS overrides or layout clipping.

---

## 1. CSS Logical Properties Matrix

Never hardcode physical horizontal sides (`left`/`right`) in shared layout stylesheets:

| Physical CSS / Tailwind (Avoid) | Logical Equivalent (Mandatory) |
| :--- | :--- |
| `margin-left` / `margin-right` | `margin-inline-start` / `margin-inline-end` (`ms-*` / `me-*`) |
| `padding-left` / `padding-right` | `padding-inline-start` / `padding-inline-end` (`ps-*` / `pe-*`) |
| `left: 0` / `right: 0` | `inset-inline-start: 0` / `inset-inline-end: 0` (`start-0` / `end-0`) |
| `border-left` / `border-top-left-radius` | `border-inline-start` / `border-start-start-radius` (`rounded-ss-*`) |
| `text-align: left` / `text-align: right` | `text-align: start` / `text-align: end` |

---

## 2. Directional Icons, Controls & Typography

- **Mirror Directional Glyphs**: Back/forward arrows, chevrons, drawer toggles, and progress tracks flip via `[dir="rtl"] .dir-flip { transform: scaleX(-1); }`.
- **Never Mirror Universal Semantics**: Play/pause/media timelines, analog clocks, checkmarks, code blocks (`dir="ltr"`), phone numbers, and brand wordmarks stay unflipped.
- **Line-Height & Font Stack**: Arabic/Persian scripts need taller vertical clearance (`line-height: 1.65–1.85`) and zero negative letter-spacing (`letter-spacing: 0`) so diacritics and connected ligatures never break.

---

## 3. Bilingual App Router Architecture (`bettersanfernando` Pattern)

When serving a primary default locale alongside secondary localized routes:
- Keep the default locale **unprefixed** (`/`, `/services`) via internal middleware/rewrite to `/[locale]/...` and issue `308` permanent redirects from `/en/...` to unprefixed canonical URLs (zero duplicate SEO indexing).
- Prefix secondary locales cleanly (`/fil/services`, `/ar/services`), preserving query params and generating full `<link rel="alternate" hreflang="...">` tags.
- **Pseudo-Localization QA**: Run builds with a `1.4x`-expanded pseudo-locale (`[!! Téxt !!]`) to catch fixed-width button truncation before real translations arrive.
