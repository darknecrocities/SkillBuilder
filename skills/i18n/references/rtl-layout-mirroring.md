# RTL Layout Mirroring & CSS Logical Properties

Arabic, Hebrew, Persian, and Urdu require right-to-left (RTL) reading and interaction flows.

---

## 1. CSS Logical Properties Matrix

Physical Property (Avoid) | Logical Equivalent (Required)
:--- | :---
`margin-left` / `margin-right` | `margin-inline-start` / `margin-inline-end` (`ms-*` / `me-*` in Tailwind)
`padding-left` / `padding-right` | `padding-inline-start` / `padding-inline-end` (`ps-*` / `pe-*` in Tailwind)
`left: 0` / `right: 0` | `inset-inline-start: 0` / `inset-inline-end: 0`
`text-align: left` | `text-align: start`

---

## 2. Directional Icons & Controls

- **Flip**: Back buttons, next arrows, progress bars (`transform: scaleX(-1)` when `dir="rtl"`).
- **Do Not Flip**: Media playback controls (play, pause, fast forward), clocks, non-directional brand logos.
