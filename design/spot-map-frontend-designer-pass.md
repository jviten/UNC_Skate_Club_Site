# Spot map — frontend-designer pass (anti-AI-tell visual direction)

*Direction only. No map code. Pairs with skate-stylist (parallel pass). My lane: ground every choice in `assets/`, kill generic/AI-generated tells. Their lane: skate-cultural correctness.*

*Grounded in: `assets/logo/unc-skate-logo-no-lettering.png` (blue ram skull, cream curled horns, ink outline, single eye socket), `assets/flyers/skate-spot-oec-griptape.png` (Carolina capsule + cream graffiti on griptape — literally a "skate spot" flyer, the closest existing asset to this page's job), `assets/flyers/women-in-skate-flyer.png` (torn-paper stamp + ink), `assets/textures/griptape.svg`, `assets/textures/tape-masking.svg`. Palette + type locked in `design/current-state.md`.*

---

## The governing idea

The landing page is "flyer taped to a bulletin board." The map page is **not** that — it's full-bleed by hard constraint, and a flyer-frame around a shrunk map is explicitly banned. So the metaphor shifts:

**The map is the wall. The chrome is what's stuck to it.** Markers, filter chips, and the popup are physical objects — capsules, tape, torn paper — laid *on top of* a live map, the same way the club staples flyers to a campus pole (see the Women in Skate IG shot: flyer pasted on a pole next to a protest flyer). The OEC flyer is the proof of concept: a Carolina-blue capsule with cream graffiti is already the club's visual for "skate spot." We reuse that exact object as the map's vocabulary.

Resting palette: Carolina + cream + ink. **No accent on this page by default.** Magenta/purple stay off the map — they belong to video and event contexts. The one allowed exception is video: a spot with clips gets a magenta tick (see Detail card), because magenta = video in this system. That's it.

---

## 1. Marker design — the ram-skull-derived pin

### What it is
A **divIcon** (HTML/CSS), not an image PNG, not a Leaflet default teardrop. Reasons: divIcon is the lightweight, snappy path (no per-marker image request, styled in CSS, recolored by class), and it lets us encode `type` + `bust` with CSS instead of generating 18 PNG variants (6 types × 3 busts). The default Leaflet blue-teardrop marker is itself a screaming generic tell — every untouched Leaflet demo on the internet uses it. We never ship it.

### Construction
Two-layer divIcon, ~28px tap target on mobile (Apple/Google min is 44px for touch — we hit that with an invisible padding hitbox around a 28px visible glyph):

- **Base shape**: the OEC capsule, miniaturized. A Carolina-blue (`--carolina #4B9CD3`) rounded "stadium"/lozenge with a **2px ink (`--ink`) outline** — the same heavy hand-drawn ink line that outlines the ram skull and the OEC capsule. The ink outline is doing the work here: it's what makes the marker read as *drawn*, not as a Material Design pin. Drop a tiny ink "tail"/notch at the bottom-center so it points at the coordinate (a 6px ink triangle, off-center-left by 1px so it's not robotically symmetric).
- **Glyph inside**: the `type`, drawn as a **single-weight ink line icon, hand-built**, not Lucide/Feather/Heroicons (those are an instant tell and they'd clash with the hand-drawn brand). Six marks, each one a crude side-profile of the obstacle, the way a skater sketches a spot in a notebook:
  - `ledge` — a short flat-topped block (rectangle, one edge thick)
  - `stairs` — a 3-step zigzag line
  - `rail` — a single diagonal line with two short legs (a handrail in profile)
  - `transition` — a quarter-pipe curve (one quarter-circle arc rising to a coping tick)
  - `flat` — a single horizontal line with a small dot (open ground)
  - `DIY` — an X of two strips of "tape" (nods to the masking-tape texture + the literal DIY ethos), or a wet-concrete trowel mark
  - These get drawn once as inline SVG `<symbol>`s and `<use>`-referenced — tiny, sharp at any DPR, recolorable.

### Encoding `bust` without clutter
`bust` is **the outline + fill state of the same capsule**, never a second badge, never a color-coded dot that fights the Carolina base:
- `chill` — solid Carolina fill, ink outline. The "default good" marker.
- `caution` — Carolina fill with the ink outline drawn as a **dashed/broken line** (4px dash). Reads as "the edge isn't clean here" — caution, without inventing a yellow that isn't in the palette.
- `hot` — **inverted**: cream (`--paper`) fill, ink outline, the Carolina pushed to just the glyph. A hot spot visually "cools off" / goes quiet — it stops shouting Carolina blue. Optionally a single ink hatch-slash across it (one diagonal stroke, like crossing something out). No red. No flame emoji. Red and a flame icon would be the two laziest AI choices here; we encode bust through the brand's own ink-line language instead.

So: **shape = always the capsule. Glyph = type. Fill/outline treatment = bust.** Three readable states, zero extra chips, all in 3 brand colors.

### At small size on a phone
- Test target: legible at 28px with the glyph filling ~16px. The type glyphs are deliberately crude/chunky (single thick stroke) so they survive at thumbnail scale — fine multi-stroke icons would mush. If a glyph doesn't read at 16px in testing, **drop the glyph and keep the capsule**; color/shape alone still carries type+bust via a legend. Better a clean blue capsule than mud.
- **Cluster** at low zoom (skater opens the map zoomed to all of Chapel Hill + Carrboro — that's a lot of pins). The cluster bubble is **not** the default Leaflet.markercluster green/yellow/red circles (another generic tell). It's a **bigger ink-outlined Carolina capsule with the count in Anton** (the display face), e.g. a chunky "12". Anton on a Carolina capsule instantly reads as "ours."
- **No bounce/drop animation** on marker add. Markers appear, done. Leaflet's default `markercluster` spiderfy spring + AI-favorite drop-in animations are exactly the springy motion the brand bans. Pan/zoom is the only motion.

---

## 2. Filter controls — chips, not a floating card

### The AI tell to kill
The default: a white rounded-corner card, `shadow-md`, maybe `backdrop-blur`, floating top-right with a column of toggle switches and Lucide icons. That's the Tailwind-starter map-app look and it's a fingerprint. Also bad on a phone: it eats a corner, the blur tanks scroll/pan perf, and it covers map.

### What we build instead
**A single horizontal strip of tape-and-capsule filter chips, bottom-anchored, thumb-reachable.** Phones first: filters go at the **bottom** of the viewport (thumb zone), not the top (where you'd reach across the screen). They sit *on* the map as physical chips, no containing card.

- **Chip = miniature OEC capsule.** Each `type` filter is a small Carolina capsule with ink outline + the same hand-drawn glyph + a Cabin Sketch label ("ledge", "rail"...). Inactive chips are **cream fill / ink outline** (turned off = paper); active chips **fill Carolina** (turned on = lit up). That on/off is the *inverse* of the bust encoding, which is fine — context disambiguates (chips are in a row at the bottom; markers are on the map). The toggle is **abrupt**: tap → fills Carolina → markers update. No fade, no slide, no spring. Click, state changes, done.
- **The strip itself**: horizontally scrollable on small screens (chips overflow off the right edge — and they *should* slightly bleed off the viewport edge, not sit politely centered; the brand breaks symmetry on purpose). Behind the strip, a **thin band of the griptape texture** (`assets/textures/griptape.svg`, the signature texture the user loves) so the chips read as stuck to a strip of grip, echoing the nav row on the landing page. Keep the griptape band short (chip height + small padding) so it doesn't cover map or cost perf.
- **`bust` filter** is a separate, smaller control — three tiny chips (chill / caution / hot) shown as the three marker *states* themselves (solid / dashed / inverted capsule) with no text, or a one-line Permanent Marker label "bust:" before them. This teaches the legend by reusing the exact marker visuals. Put it as a second, shorter row or tucked at the strip's left end.
- **Desktop**: the same strip, but it can move to a corner and stack into a short column if we want — the chip vocabulary doesn't change, only placement. Don't redesign for desktop; just let the strip breathe.

### Why this isn't clunky
Chips are cheap DOM. No blur, no big shadow (the ink outline is the "edge," not a soft shadow — soft drop shadows are both a tell *and* a phone-perf cost). The whole control is HTML/CSS over the map, no extra map layers.

---

## 3. Popup / detail card — torn paper, not the Leaflet bubble

### The AI tell to kill
Leaflet's default `.leaflet-popup` is a white rounded bubble with a soft shadow and a little CSS triangle tail — instantly recognizable as "untouched Leaflet," which on this brand reads as "nobody designed this." We override it completely.

### Mobile (primary): a bottom sheet, not a floating bubble
On a phone, a popup anchored to a marker near the top of the screen is unreadable and gets clipped. So on mobile, tapping a marker raises a **bottom sheet** — a panel that slides up from the bottom edge (abrupt, ~120ms, no spring/overshoot; it appears, it doesn't bounce). The sheet is:

- **Cream paper (`--paper`)** with a **torn top edge** — reuse the torn-paper language from the landing (`white-ripped-paper-png.webp` as the top fringe), so the sheet looks like a piece of flyer paper pulled up over the map. This is the asset-grounded replacement for the generic rounded sheet. Keep it to ONE torn edge (the top) for perf and restraint — the landing's four-edge treatment is too heavy for a control that opens/closes constantly.
- A small **strip of tape** (`assets/textures/tape-masking.svg`, the off-white masking tape) holding the sheet's top-left corner "down" onto the map — the same postering gesture as the landing's corner tape. One piece, slight rotation (~ -4°), not centered.
- **Content hierarchy, drastically mixed sizes** (the brand mixes huge/tiny, never all-medium):
  - **Spot name** in **Anton**, big, ink, hard left, allowed to run near the torn edge. This is the only display-face moment in the sheet.
  - **type · area · surface · size** as a single Special Elite (typewriter) meta line, small, like a flyer's fine print.
  - **bust** rendered as the marker glyph itself + a Permanent Marker word ("chill" / "watch it" / "hot — expect the boot") — copy is skate-stylist's call, but the *form* is: hand-drawn, not a colored pill badge.
  - **notes** in Permanent Marker or Special Elite, plain text (schema says no HTML — escape it).
  - **photo(s)**: the schema allows up to 8. Show **one** big photo in the sheet (the club has real photos — use them, never stock/AI) with the rest behind a "more" tap. The ram skull logo can sit as a small **ink/Carolina watermark** bottom-right of the photo, exactly how the club overlays it on portraits — that's an established club gesture, not invented chrome.
  - **clips** (video): if a spot has clips, show a single **magenta** tick / "▸ clips (3)" in the pixel/VT323 face — this is the *one* sanctioned accent on this page, because magenta = video across the whole brand (Pluto, Women in Skate). Tapping opens the clips (embed UI deferred per current-state). A spot with no clips shows nothing — no empty "no videos yet" slot.
  - **submitted_by / verified / added** dates: tiny Special Elite footer, like a stamp ("verified 5.20.26"). Use the torn-paper "stamp" energy from the Women in Skate flyer — a small ink date, not a UI timestamp row.
- **Close**: an ink **hand-drawn X** top-right (a real scratchy X mark, two crossing strokes — not a thin geometric Lucide `×`). Tap or swipe-down to dismiss.

### Desktop
Same panel, but anchored as a side panel (left or right, deliberately *not* a centered modal) rather than a bottom sheet. Still torn-paper + tape, still no Leaflet bubble. The map stays full-bleed behind it.

### Perf guardrail
The sheet is one element, built once and reused (swap content per marker), not re-created per tap. Torn edge = one background-image, no blur, no multiply-stack like the landing's `.paper::before` (that's fine for one static hero, too expensive for a panel that animates). One tape SVG. Keep it light.

---

## 4. Base map tiles — restyle OSM or it screams "demo"

### The AI tell to kill
**Default OSM "standard" tiles are the single biggest generic tell on this whole page.** Beige roads, that specific OSM green/yellow, the Mapnik look — every tutorial map on earth uses it. Drop our hand-drawn Carolina markers onto raw Mapnik and the markers look pasted onto someone else's map. The base has to recede and sit *under* the cream/Carolina/ink palette.

### Recommendation (in priority order)
1. **Preferred: a muted, low-chroma raster base that matches paper/ink.** Use **CARTO Positron** (light, near-grayscale, free, well-attributed) or **Stamen/Stadia "Toner Lite"** as the base tiles instead of standard OSM. Toner especially is **black-line-on-near-white** — which is *exactly* the ink-line-on-paper language of the whole brand. Toner Lite under cream chrome with ink-outlined Carolina markers would look intentional and cohesive, not like a demo. This is the strongest cohesion move and costs us nothing (still OSM data, just a designed tile style).
   - Check current Stadia/Stamen + CARTO free-tier terms and attribution requirements at build time; both are free for low volume but require correct attribution (keep the attribution control, restyle it small — see §5).
2. **If we must use raw OSM tiles** (licensing simplicity, full control): tone them down in-browser with a **CSS filter on the tile layer** — `filter: grayscale(0.7) sepia(0.15) brightness(1.04) contrast(0.92)`. This warms the grays toward the cream paper and kills the saturated OSM green/yellow so the only saturated thing on screen is the Carolina markers. Cheap (one filter on the tile pane), reversible, no extra requests. Downside: filters can cost a little on low-end phones during pan — test; if it janks, fall back to option 1's pre-styled tiles (zero runtime cost).
3. **Do NOT** build a fully custom griptape/dark base map. Tempting (griptape is the signature texture) but: dark base + Carolina markers + cream popups would fight, a dark map of a college town reads as a nightlife app, and a tiled texture base is a perf and legibility problem at every zoom. **Griptape stays as chrome accent (the filter strip), not the map surface.** The map surface is quiet paper-toned cartography so the club's blue pops.

Net: **light, desaturated, warm-leaning base (Toner Lite or Positron, or filtered OSM) — never raw Mapnik.**

---

## 5. Type / loading / empty states — on-brand, lightweight

### Type roles on this page
- **Anton** — spot names in the sheet, cluster counts. Sparingly; it's the loud face.
- **Cabin Sketch** — filter chip labels, any nav back to the rest of the site (locked face for nav/sub-heads).
- **Permanent Marker** — bust words, notes, short hand-written guidance.
- **Special Elite** — meta lines, dates/stamps, attribution.
- **VT323 / pixel** — *only* the clips/video tick (magenta), nowhere else. Pixel face is video-context only (Pluto). Don't let it leak into general map UI.
- **Never** Inter/Poppins/system-ui — including in the Leaflet attribution and any control text, which default to system sans. Override `.leaflet-container` font to Special Elite or Cabin Sketch so even the fine print is ours. (This is a common miss — untouched Leaflet text in system-sans is a quiet tell.)

### Loading state
- **No spinner.** A centered spinning ring is the universal AI/loading-default tell. Instead: a brief **ink stamp on cream** — the ram skull logo at small size with a Permanent Marker line under it ("rolling up the spots…" — copy is skate-stylist's). It holds for the fetch, then snaps away when tiles+markers are ready. No fade-out; remove it.
- Since the architecture serves a **static snapshot first then hydrates from the API** (current-state), design the load as: snapshot markers appear basically instantly (feels snappy — the hard requirement), and a tiny Special Elite line ("updated just now" / "showing last saved spots") tells the truth about freshness. **No skeleton shimmer** (another tell) — the snapshot makes skeletons unnecessary.

### Backend-down / stale state
current-state mandates graceful degradation. When on the snapshot fallback: a small **masking-tape banner** (one `tape-masking.svg` piece) along the top edge with a Special Elite line — "showing saved spots — submit's closed rn" (skate-stylist words it). Honest, on-brand, not an alarming red toast. The submit button goes **dark/disabled = inverted to cream-on-ink**, visibly "off," matching the marker logic where cream-fill = quiet/off.

### Empty state (filters return nothing)
- When a filter combo yields zero markers: a single torn-paper note pinned center-ish (off-center, with tape) — Permanent Marker, "nothing matches that combo — loosen it up." Plus the active chips stay lit so it's obvious *why* it's empty. **No generic "No results found" + magnifying-glass illustration** (textbook AI empty state).
- First-load-ever / genuinely no spots (early v1 with few seeds): don't fake a populated map. Show the few real seed spots and a Permanent Marker line "more spots dropping soon — got one? hit submit." Honest copy, not aspirational filler.

### Attribution / Leaflet controls
- Keep OSM/tile attribution (license requirement) but restyle: small, Special Elite, ink-on-cream, bottom corner, no default white box with link-blue underlines.
- **Zoom control**: the default Leaflet `+ / −` buttons are white rounded squares with soft borders — restyle to **ink-outlined cream squares with Anton `+` / `−`**, or hide them entirely on mobile and rely on pinch (phones don't need buttons; one fewer thing covering the map). Keep on desktop, styled.
- Geolocate ("where am I") is high-value for skaters in the field — if added, make it an **ink-outlined Carolina capsule** matching the marker language, not a generic crosshair button.

---

## AI tells to avoid on THIS page — quick reference

| AI tell | Asset-grounded replacement |
|---|---|
| Default Leaflet teardrop marker | OEC-capsule divIcon: Carolina lozenge, ink outline, hand-drawn type glyph |
| Red/flame for "hot" bust | Inverted cream capsule (Carolina "cools off"); ink hatch-slash; no red, no emoji |
| Lucide/Feather/Heroicons for type | Hand-drawn single-stroke obstacle marks (ledge/stairs/rail/etc.), built as inline SVG symbols |
| Floating white card + shadow + backdrop-blur filter panel | Tape-and-capsule chip strip on a short griptape band, bottom/thumb zone, no card |
| Default Leaflet popup bubble + tail + soft shadow | Cream torn-paper bottom sheet (mobile) / side panel (desktop), one masking-tape corner, ink hand-drawn X close |
| Raw OSM Mapnik tiles (saturated, "demo" look) | Toner Lite / Positron, or `grayscale+sepia` CSS filter on the tile pane — paper-toned, lets Carolina pop |
| Leaflet default markercluster colored circles + spiderfy spring | Bigger ink-outlined Carolina capsule, count in Anton; no spring/bounce |
| Spinner / skeleton shimmer loading | Ram-skull ink stamp on cream + Permanent Marker line; snapshot makes load near-instant |
| "No results found" + magnifying-glass illustration | Torn-paper taped note, Permanent Marker, "loosen it up"; active chips stay lit |
| Springy button presses, fade-ups, parallax | Abrupt state changes only — tap → fills → markers update; sheet appears in ~120ms, no overshoot |
| System-sans in Leaflet controls/attribution | Override `.leaflet-container` font; Special Elite fine print, Cabin Sketch labels |
| Magenta + purple scattered for decoration | No accent at rest (Carolina + cream + ink). Magenta only on the clips/video tick. Purple stays off this page. |

## Cohesion / palette flags for sign-off

- **Cream over a live map** is unproven. On the landing, cream is the paper everything sits on. Here it's a sheet/chip color floating over a paper-toned *map*. Risk: cream sheet on a near-white Toner base could be low-contrast / muddy. **Proposing, not committing** (per current-state's note that cream isn't fully sold). If it reads soft over the tiles, the ink outline + torn edge should rescue contrast; if not, fall back to **bone `--paper-fallback #ebe4d2`** for the sheet only, to separate it from the lighter map. Flagging before any CSS.
- **One accent rule holds**: magenta appears *only* on the video tick. If we ever feel the urge to color busts magenta/purple or tint the filter strip with an accent, stop — that's the palette fragmenting, which the user explicitly flagged.

## Disagreement / open question for the user (vs. skate-stylist likely position)
- **Griptape as base map**: I'm against it (§4 option 3) on perf + legibility + "this is a nightlife app" grounds, even though griptape is the user's favorite texture. skate-stylist may push for griptape as the map ground for authenticity. My counter: griptape stays as the *filter-strip* chrome where it's already proven (landing nav row), and the map surface stays quiet. **User picks** if we disagree.
- **Marker glyphs at 16px**: real risk they don't read on a phone. I'd rather ship clean capsules + a legend than mushy glyphs. Worth a quick build spike before committing to all six glyphs.
