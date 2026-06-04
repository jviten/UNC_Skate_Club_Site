# UNC Skate Club site — locked visual-language spec

*Synthesized from pass-1 + pass-2 of `frontend-designer` and `skate-stylist`, with all user decisions baked in. This is the single source of truth for `builder` — read this, not the individual pass docs.*

## 1. Palette (CSS custom properties)

```css
:root {
  --carolina:       #4B9CD3;  /* logo skull body, mark, strokes */
  --carolina-deep:  #1d3a5f;  /* ram skull outline; deep accents */
  --paper:          #f0ebe1;  /* cream — confirmed, with bone fallback pre-staged */
  --paper-fallback: #ebe4d2;  /* swap target if cream drifts in prototype */
  --ink:            #14171a;  /* near-black, slight warmth — never pure #000 */
  --wall:           #111111;  /* the dark behind the flyer; viewport background */

  /* contextual accents — never both on the same page */
  --magenta:        #E5197F;  /* video / Women in Skate references only */
  --purple:         #6E3AA8;  /* event-flyer-style contexts only */
}
```

Cohesion: resting state = `--carolina + --paper + --ink`. Accents earn appearance by being tied to a specific reference (Pluto, Women in Skate, Skate X Croquis). Never both magenta and purple on the same page.

## 2. Type stack (all Google Fonts / open-source)

| Role | Face | Notes |
|---|---|---|
| Display / banner | **Anton** | All-caps, tight kerning, line-height 0.9. Sole display face — no Druk, no Bowlby. |
| Hand / scratchy | **Permanent Marker** | Headlines that are "written on the flyer" — meeting info, captions, pull quotes |
| Hand / structural | **Cabin Sketch** | Secondary hand voice for nav labels, sub-headlines, marks-near-the-logo |
| Body / meta | **Special Elite** | Typewriter, for short blocks and meta (dates, addresses, captions) |
| Long-form body | **Newsreader** | About-page reading copy. Warm enough to live on cream without going corporate |
| Pixel / arcade | **VT323** | Reserved for video / Pluto / premiere contexts only. Don't sprinkle elsewhere. |

Hard no: Inter, Poppins, Roboto, Montserrat, Work Sans, `system-ui`. Graffiti bubble lettering (the OEC capsule style) is art only — never set as live HTML.

## 3. Frame architecture — "site as a taped flyer"

The site is structured as a flyer taped to a wall.

1. **Wall** (`<body>` background): `var(--wall)` ink black `#111`. No texture for v1. The wall is visible past the torn edges of the paper and through any inner tears.
2. **Paper** (`<main>`): `var(--paper)` cream, fills ~95% of viewport. All four edges masked by torn-paper PNGs (asymmetric, one unique edge per side). Edges bleed 12–20px into the wall so the paper reads as overlaid, not flush.
3. **Inner tears** (~1–2 per page max): small tears in the middle of the paper where the wall shows through. These replace the pass-1 section divider concept. Use as section breaks — `~6px` of wall visible per inner tear. Not on every section — sparingly, like real battle damage.
4. **Tape** — four corner pieces, asymmetric, mixed types. "Messed up" energy:
   - Top-left: scotch-tape yellow `#e8d96d`, slight translucency, `~+12°` rotation
   - Top-right: white masking tape `#ece6d2`, `~-7°` rotation
   - Bottom-left: blue painter's tape `#5b9bd5`, `~+4°` rotation
   - Bottom-right: black duct tape `#1d1d1d`, `~-9°` rotation
   - Each piece overhangs onto the wall slightly. Each is a different length (90–140px). No piece exactly matches another.

### Mobile degradation (under 600px viewport)

- Drop side torn edges; keep top + bottom only. Paper goes edge-to-edge horizontally.
- Drop two of the four tape pieces (keep top-left scotch + bottom-right duct for the diagonal). Tape shrinks to ~80px.
- Inner tears stay but reduce to max 1 per page.
- Never auto-rotate. Layout reflows from narrow to wide; tape rotations stay constant.

### Production notes — synthesized assets for v1

User declined to scan real paper/tape for now. v1 ships with synthesized assets:

- **Paper texture**: a CC0 cream paper texture overlaid with subtle CSS noise (`background-image` with a fine grain PNG, ~5% opacity).
- **Torn edges**: hand-drafted SVG with intentional irregularity (no uniform sine waves). Saved as PNG. Four unique variants — top, bottom, left, right.
- **Tape**: hand-drafted SVG per tape type, with grain overlay for masking tape, slight gloss for scotch, matte for duct, semi-translucent for painter's. Each saved as PNG.
- **Swap-in plan**: when real scans become available later, drop in `assets/textures/paper.png`, `assets/textures/edge-{top,bottom,left,right}.png`, `assets/textures/tape-{scotch,masking,painter,duct}.png` — same filenames, no other code changes needed.

## 4. Layout idioms

- **Ram skull** (`assets/logo/UNC SKATE LOGO.png`) — three sizes:
  - **Header mark**: ~60–96px, top-left of the flyer, hard-cropped against the torn top edge so horns appear torn through with the paper.
  - **Hero centerpiece**: ~280–480px, left third of hero band, slightly cropped off the left edge.
  - **Watermark / dingbat**: ~24–32px, ~30% opacity overlapping photo corners; or full-color at end-of-section as a magazine-style mark.
- **Griptape** — demoted from pass-1 full-bleed band. Now a contained image inside the flyer (a "printed-on-paper" band behind the hero headline), bleeding left/right to the torn edges but capped top/bottom. Carolina-blue OEC-style capsule (per `assets/flyers/skate-spot-oec-griptape.png`) floats on it for hero text.
- **Photos** — pasted, not floated. Three treatments:
  1. Polaroid-tape look for portraits.
  2. Full-bleed B&W with magenta Permanent Marker caption for Women-in-Skate / video lead-ins.
  3. Untouched color, slight rotation (`-2°` to `+2°`, never the same), hard 4px `--ink` border, no shadow, no radius. Allowed to overlap headlines.
- **Section dividers inside the paper** — primary mechanism is the inner tear (showing wall through). Secondary mechanism: a thin `--ink` hairline rule (1px) where a tear would be overkill. No torn-paper strips inside the flyer — the frame is already torn paper; doubling up dilutes it.
- **Buttons / links** — square corners, 2px `--ink` outline on `--paper`, hover inverts to ink fill + cream text, ≤100ms transitions, no easing curves.
- **Pluto video block** — YouTube `<iframe>` housed inside a hand-drawn Permanent Marker frame, sitting on a magenta torn-paper scrap that's duct-taped to the cream. Lazy-load. VT323 + magenta accent active only inside this block.

## 5. Above-the-fold wireframe (landing)

```
[wall — ink black, viewport background]

[paper — cream, fills ~95% of viewport, four torn edges, 12-20px bleed into wall]

  [tape, four corners: scotch+12° TL, masking-7° TR, painter's+4° BL, duct-9° BR]

  [banner — top of paper interior, full inner width]
    Left:  UNC SKATE LOGO.png, ~60–96px, hard-cropped against torn top edge
    Right: Anton, all-caps, ink, ~140px desktop / ~80px mobile, line-height 0.9:
      "SKATE CLUB"
      "AT UNC"

  [nav row — directly below banner]
    Cabin Sketch (or Special Elite) caps, ~14–16px:
      "SPOTS · MEETINGS · ABOUT · IG"
    thin ink hairline under

  [meeting info — directly below nav, ink on cream]
    Permanent Marker, ink, ~28px:
      "thursdays · 6:30 · the pit"
    Permanent Marker, ink, ~16px on next line:
      "any board. any wheels. first time on one is fine."

  [hero band — griptape image, contained inside the flyer,
   ~45vh, bleeds to torn edges left/right but capped top/bottom]
    Ram skull, large, left third, cropped slightly
    Carolina-blue OEC-style capsule on the right, with a brief hand-drawn line
    in cream Permanent Marker (e.g. "spring 26 / chapel hill")

  [maybe one inner tear here, ~6px wall showing through, as a section break]

  [second block — flyers wall / latest photo from photographer]
    See section 4 photo treatments. Out of fold but signals "more below."
```

No "EST." line. No primary/secondary CTA pair. No centered hero.

## 6. Open production questions

- **Per-page tape variants**: do tape colors/positions stay constant site-wide, or vary per page so the site feels like multiple flyers taped over each other across visits? **Default: constant for v1**, vary in v2.
- **Inner-tear placement**: hard-code per page, or randomize at build time so each visit feels slightly different? **Default: hard-code for v1**, no randomization (predictability helps testing).
- **Hierarchy at small banner sizes**: 80px Anton may dominate 20px Permanent Marker meeting info — bump meeting info to 24–28px on mobile if needed during prototype.
- **Real-scan upgrade**: when ready, swap PNGs at the filenames above and the layout doesn't change.

## 7. What does NOT belong on this site

- Inter, Poppins, Roboto, any generic web sans
- Gradients (`linear-gradient`, `radial-gradient`) anywhere
- Soft drop shadows, `box-shadow` larger than `1px 1px 0` ink
- Border-radius above 0px (square corners only)
- Glassmorphism, backdrop-blur, frosted anything
- Stock photography, AI-generated imagery
- Emoji as iconography
- Friendly geometric icons (Lucide, Heroicons, Feather)
- Scroll-triggered fade-up, springs, parallax
- Centered hero + headline + subhead + CTA pair
- "Thrill Hill" branding — the site title is "Skate Club at UNC"
- Corporate inclusivity copy ("we welcome skaters of all backgrounds...") — the inclusivity message is carried by photography + light copy lines, never as a marketing hook
