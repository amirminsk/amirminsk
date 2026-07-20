---
name: MAISON
colors:
  primary: "#c9a84c"
  secondary: "#e8c97a"
  tertiary: "#7a7874"
  neutral: "#f0ede8"
  surface: "#070604"
  deep: "#0c0b09"
typography:
  headline-display:
    fontFamily: Bebas Neue
    fontSize: 9rem
    letterSpacing: 0.12em
  headline-lg:
    fontFamily: Cormorant Garamond
    fontSize: 3.4rem
    fontWeight: 300
  headline-md:
    fontFamily: Cormorant Garamond
    fontSize: 1.8rem
    fontWeight: 300
  body-md:
    fontFamily: Courier Prime
    fontSize: 0.8rem
    lineHeight: 1.6
  body-sm:
    fontFamily: Courier Prime
    fontSize: 0.72rem
    lineHeight: 1.5
  label-lg:
    fontFamily: Courier Prime
    fontSize: 0.6rem
    letterSpacing: 0.28em
  label-sm:
    fontFamily: Courier Prime
    fontSize: 0.55rem
    letterSpacing: 0.3em
spacing:
  xs: 0.75rem
  sm: 1.6rem
  md: 2.5rem
  lg: 4rem
rounded:
  none: 0px
  sm: 3px
  full: 999px
---

## Overview

MAISON is a haute-horlogerie brand site built around a dark, low-contrast
canvas that lets gold accents and full-bleed product photography carry the
weight. The palette is intentionally narrow — near-black backgrounds, warm
off-white text, and a single metallic gold used sparingly for emphasis (CTAs,
active states, hairline borders) — so the watches themselves read as the
brightest thing on the page.

Type pairs a classic serif (Cormorant Garamond) for headlines with a
monospace (Courier Prime) for everything functional: labels, navigation,
body copy, form fields. The monospace choice reads as "specification sheet"
rather than "marketing copy," reinforcing the horlogerie/engineering theme.
A single display face (Bebas Neue) is reserved for the loading-screen
wordmark and should not be reused elsewhere.

This file documents the system as expressed on the primary landing
experience (`index.html`). `product.html` and `collection.html` currently
run a lighter, cream-toned variant of the same layout patterns — see
Do's and Don'ts.

## Colors

- **primary** (`#c9a84c`, gold) — the brand's single accent color. Used for
  calls to action, active nav/link states, focus borders, and dividers.
  Never used as a large fill; always foreground/accent.
- **secondary** (`#e8c97a`, light gold) — hover/highlight state for
  `primary`, and gradient partner when a richer metallic effect is needed.
- **tertiary** (`#7a7874`, warm gray) — muted/secondary text: nav links at
  rest, footer copy, timestamps, helper text.
- **neutral** (`#f0ede8`, off-white) — primary text color on dark surfaces.
- **surface** (`#070604`, near-black) — the page background.
- **deep** (`#0c0b09`) — a slightly lighter panel background used to
  separate cards/sections from the base `surface` without introducing a
  second hue.

## Typography

- **headline-display** — Bebas Neue, 9rem, 0.12em tracking. Reserved for the
  loading-screen wordmark only.
- **headline-lg** — Cormorant Garamond, 3.4rem, weight 300. Section/story
  titles (e.g. scroll-driven "stop" titles).
- **headline-md** — Cormorant Garamond, 1.8rem, weight 300. Sub-section and
  footer headings.
- **body-md** — Courier Prime, 0.8rem, 1.6 line-height. Default paragraph
  copy.
- **body-sm** — Courier Prime, 0.72rem, 1.5 line-height. Secondary copy:
  footer text, form fields.
- **label-lg** — Courier Prime, 0.6rem, 0.28em tracking, uppercase.
  Navigation links and primary labels.
- **label-sm** — Courier Prime, 0.55rem, 0.3em tracking, uppercase.
  Utility buttons (sound toggle, skip button) and fine print.

All uppercase label styles rely on heavy letter-spacing rather than bold
weight to read as "engraved" rather than "loud."

## Layout

Base spacing scale used for padding/gaps across nav, sections, and cards:

- **xs** (0.75rem) — tight gaps between an icon/label pair.
- **sm** (1.6rem) — nav padding, small stacks.
- **md** (2.5rem) — standard section/card horizontal padding.
- **lg** (4rem) — section vertical rhythm, footer column gaps.

## Elevation & Depth

- **card**: `0 16px 48px rgba(0,0,0,0.55), 0 0 0 1px rgba(201,168,76,0.12)`
  — resting elevation for product/media cards: a soft black drop shadow plus
  a hairline gold rule instead of a hard border.
- **glow**: `0 8px 28px rgba(201,168,76,0.2)` — hover/active state, a gold
  ambient glow used in place of a second shadow color.

## Shapes

- **none** (0px) — default for panels, sections, and most surfaces; the
  system favors hard edges.
- **sm** (3px) — small interactive chrome (e.g. form inputs) where a hint of
  softness is needed.
- **full** (999px) — icon buttons and dot/indicator elements only; a
  large-radius value that yields a full circle/pill on square or
  single-line elements (the tokens here are limited to px/rem/em, so this
  stands in for CSS's `border-radius: 50%` on those shapes).

## Components

```yaml
components:
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.surface}"
    typography: label-lg
    rounded: "{rounded.none}"
    padding: 1.1rem
  button-secondary:
    backgroundColor: transparent
    textColor: "{colors.neutral}"
    typography: label-lg
    rounded: "{rounded.none}"
    padding: 1rem
  icon-button:
    backgroundColor: transparent
    textColor: "{colors.tertiary}"
    typography: label-sm
    rounded: "{rounded.full}"
    padding: 0.45rem
  card:
    backgroundColor: "{colors.deep}"
    textColor: "{colors.neutral}"
    typography: body-md
    rounded: "{rounded.none}"
    padding: 2.5rem
```

## Do's and Don'ts

- **Do** keep gold (`{colors.primary}`/`{colors.secondary}`) as an accent
  only — borders, text, small fills. Don't use it as a large background
  fill; it reads as gaudy at scale instead of precious.
- **Do** pair every uppercase label with wide `letterSpacing` (0.25em+)
  rather than bold weight for emphasis.
- **Do** reserve `headline-display` (Bebas Neue) for the loading-screen
  wordmark. Don't introduce it into body content or other headings.
- **Don't** introduce new accent hues; the system is deliberately
  monochrome-plus-gold.
- **Known drift:** `product.html` and `collection.html` currently use a
  separate cream/light palette (`--bg: #f4f0e8`, `--ink: #111010`) and
  additional fonts (Barlow Semi Condensed, Space Mono) not captured in this
  file. Treat that as technical debt to reconcile toward this system, not as
  a second supported theme.
