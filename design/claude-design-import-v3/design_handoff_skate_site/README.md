# Handoff: Skate Club at UNC — Landing Page

## Overview
A single-page site for the UNC Skate Club, styled as a **DIY punk-zine flyer pinned to a
cork bulletin board**. It carries the club's identity (ram skull mark + "Skate Club at UNC"
wordmark), the essentials (meeting time/place, inclusivity note, embedded skate video, socials),
and a "photo wall" of printed, pinned snapshots at the bottom. The whole page lives on a tiled
cork-board background; the main content is a torn-edge cream flyer held down with masking tape.

## About the Design Files
The files in this bundle are **design references created in HTML/CSS** — a working prototype of
the intended look and behavior, **not production code to ship directly**. The task is to
**recreate this design in your existing repo** using its established framework, component
patterns, and styling conventions (React/Vue/Astro/etc.). Pull exact values (colors, fonts,
spacing, copy) from this README and the HTML, but structure the implementation the way your
codebase already does things.

## Fidelity
**High-fidelity.** Final colors, typography, copy, layout, and interactions are all here and
intended to be matched closely. The texture/grunge treatment is core to the brand — don't
flatten it into a clean material-design page. A few CSS techniques (SVG displacement filters for
torn paper, turbulence noise overlays) are doing real visual work; replicate the *effect* even if
you implement it differently.

## Design Tokens

### Colors (CSS custom properties from `:root`)
- `--paper: #f0ebe1` — flyer cream (main paper)
- `--paper-edge: #d6cdb4` — darker backside revealed at torn edges
- `--ink: #14171a` — primary near-black text
- `--ink-soft: #2a2722` — softer brown-black (captions, secondary)
- `--carolina: #4B9CD3` — Carolina blue (accent swatch, links/hover, pins)
- `--carolina-deep: #1d3a5f` — deep blue
- `--magenta: #E5197F` — hot magenta (nav hover, pins)
- `--masking: #e8d8a4` / `--masking-edge: #c9b87a` / `--masking-warm: #ddc676` — masking-tape tones
- `--duct: #161616` — duct/griptape black
- Page background behind cork: `#4a3422` (brown); cork tile base `#5e4326`

### Typography (Google Fonts)
Imported: `Anton`, `Permanent Marker`, `Cabin Sketch` (400/700), `Special Elite`, `VT323`.
- **Body / meta:** `"Special Elite", "Courier New", monospace`
- **Hero wordmark:** `"Anton", Impact, sans-serif`, uppercase, line-height 0.84,
  `font-size: clamp(80px, 13vw, 220px)`, letter-spacing -0.01em
- **Nav links:** `"Cabin Sketch", cursive`, 700, `clamp(18px, 1.9vw, 28px)`, uppercase
- **Handwritten captions / gallery headings:** `"Permanent Marker", cursive`
- **Issue / date accents:** `"VT323", monospace`

### Spacing / structure
- Flyer max-width: `1380px`, centered. Stage padding: `80px 5vw 0`.
- Flyer content padding: `110px 9% 130px`.
- Gallery max-width: `1380px`, padding `10px 4vw 110px`.

### Effects
- **Torn paper edges:** SVG `feDisplacementMap` filter (`#paper-rip`) applied to the flyer
  paper layer + a slightly larger `--paper-edge` layer behind it to reveal the ragged backing.
- **Paper/griptape grain:** inline `feTurbulence` noise SVGs as background layers with
  `multiply` / `overlay` blend modes.
- **Drop shadows:** flyer uses layered `drop-shadow(0 5px 0 …)` + `drop-shadow(0 18px 24px …)`
  for a printed-paper lift.
- **Pins / tape:** pushpins are a reusable SVG `<symbol id="pin-glyph">` with bulb color set per
  instance via `--bulb-fill: url(#pinBulbMag | #pinBulbBlue)`. Tape strips are `.tape` divs with
  masking-tape gradient fills, rotated a few degrees.

## Screens / Views
Single page, top to bottom:

### 1. Cork wall background
Fixed, full-viewport tiled `assets/cork.jpg` (720px tile) on `#5e4326`, with a radial vignette
overlay darkening the edges. Sits behind everything (`z-index: 0`).

### 2. Flyer (the main card)
Torn-edge cream paper, taped to the cork with masking-tape strips at corners and straddling the
edges. Contains, in order:
- **Meta strip:** `ISSUE 026 // SPRING 26` · `CHAPEL HILL` · boxed `FREE / DIY` (rotated -2deg),
  underlined by a 2px ink rule.
- **Hero:** ram-skull logo (`assets/unc-skate-logo-no-lettering.png`, ~380px, pulled up with
  negative margin so it overhangs) on the left; right-aligned Anton wordmark "Skate Club / at
  UNC", where the **"at UNC" line sits on a Carolina-blue swatch** (`skewX(-4deg)`, cream text).
- **Nav band:** black griptape-textured strip (`assets/griptape.jpg` + turbulence overlay) with
  links *Spots · Meetings · About · GroupMe · IG* (Cabin Sketch, cream, dashed dividers,
  magenta on hover). An **animated SVG skater** grinds along a chrome rail across the top edge of
  this band (see Interactions).
- **Info grid (2 columns):**
  - *Meetings:* "meetings at **6:30 pm** / in the pit / every thursday" + handwritten
    "no dues. show up."
  - *For anyone:* list — "any wheels." (sharpie underline), "beginners welcome.", "extra boards
    available." — followed by the **video snapshot** (see below).
- **The crew strip:** full-width horizontal `image-slot` placeholder for a long crew photo, with
  caption "// THE CREW … SPRING 26".

### 3. Video snapshot (inside "For anyone")
A small taped, rotated (-2.2deg) printed-photo frame containing an embedded YouTube player
(`youtube-nocookie.com/embed/FUS0ikotKhY`, "Pluto — UNC Skate Club"), masking-tape strip on top,
caption `"pluto" our video ↗`. Frame max-width ~440px, 16:9 iframe, hover lifts/scales slightly.

### 4. Footer strip (on cork)
A single inline line directly on the cork below the flyer:
`@unc.skate.club · every thursday · the pit · skate club @ UNC · 📍chapel hill` (the location has
a small magenta pushpin). IG handle links to `instagram.com/unc.skate.club`.

### 5. Photo wall / gallery ("// the wall")
Printed photos pinned to the cork, each `<figure class="photo">` with a pushpin SVG, an
`image-slot` (or filled `<img>`), a Permanent-Marker caption, and a small random rotation so they
look hand-tacked. Frame variants:
- base `.photo` — square (`aspect-ratio: 1/1`), `width: clamp(300px, 32vw, 396px)`
- `.photo--wide` — 3:2, `width: clamp(360px, 42vw, 520px)`
- `.photo--tall` — 4:5
- `.photo--double` — one wide print holding two 3:2 photos side by side (`.photo__pair`, flex),
  `width: clamp(420px, 78vw, 920px)`
- Photos 1 + 2 are wrapped in a `.gallery__duo` (flex) so they **stay side by side** and only
  stack below 520px.

Current contents (caption → asset):
- "women in skate" → `women-in-skate.jpg` (wide)
- "skate jam" → `skate-jam.png` (tall)
- "skate club got breaded up" → `breaded-trunk.jpg` + `breaded-checkout.jpg` (double)
- "who think elias landed ts?" → `elias-rail.jpg` (wide)
- "fully sent" → empty placeholder (square)

Every frame caps to `max-width: 92vw` so nothing overflows on small phones.

## Interactions & Behavior
- **Skater animation:** an SVG skater ollies onto a chrome rail, grinds across the nav band, and
  pops off, looping every 5s. Driven by the Web Animations API (`element.animate(routine, …)`)
  with a keyframe `routine` array of `{offset, transform, easing}` steps (translate + rotate);
  spark particles flash during the grind. See the inline `<script>` at the bottom of the HTML for
  the exact keyframes. Respect `prefers-reduced-motion` when you port it.
- **Nav links:** in-page anchors (`#spots`, `#meetings`, etc.); magenta on hover.
- **Video frame:** plays inline via the embedded iframe; hover transforms (rotate toward 0 +
  slight scale, shadow grows).
- **Photo frames:** static, individually rotated; no click behavior by default.
- **image-slot:** a custom element (`image-slot.js`) that renders a drag-and-drop image
  placeholder the user fills in; filled ones persist via localStorage in the prototype. In your
  app, **replace `image-slot` with real `<img>` tags / your image component** — it's only a
  prototype affordance for swapping photos. Slots with a `src` attribute already point at a real
  asset.

## Responsive behavior
- Wordmark, nav, and frames use `clamp()` so they scale with viewport.
- Info grid is 2-col on desktop; collapse to 1 column on narrow screens (check the
  `@media` rules in the HTML).
- `.gallery__duo` keeps photos 1+2 paired until `max-width: 520px`, then wraps.
- All gallery frames cap to `92vw`.

## State Management
Essentially none for production — this is a static marketing page. The only stateful piece is the
prototype's `image-slot` (localStorage-backed image swapping), which you should drop in favor of
static assets / a CMS field. The YouTube embed manages its own player state.

## Assets
All in `assets/` (copied into this bundle):
- `cork.jpg` — tiled cork-board background
- `griptape.jpg` — nav band texture
- `unc-skate-logo-no-lettering.png` — ram skull hero mark
- `women-in-skate.jpg`, `skate-jam.png`, `breaded-trunk.jpg`, `breaded-checkout.jpg`,
  `elias-rail.jpg` — photo-wall images (club's own photos)
- `white-ripped-paper.webp` — (available; torn-paper texture)
- **Video:** YouTube ID `FUS0ikotKhY` (embedded via youtube-nocookie)
- **Fonts:** Google Fonts — Anton, Permanent Marker, Cabin Sketch, Special Elite, VT323

## Files
- `UNC Skate Site v3.html` — the complete design (this is the current/canonical version)
- `image-slot.js` — custom element used for the drag-drop photo placeholders (prototype only;
  replace with your image component)
- `assets/` — all images referenced above

Note: the torn-paper / pushpin / tape SVG filters and `<symbol>` definitions live inline near the
top of the HTML body (look for `id="paper-rip"`, `id="pin-glyph"`, `id="pinBulbMag"`,
`id="pinBulbBlue"`). Port these along with the markup that uses them.
