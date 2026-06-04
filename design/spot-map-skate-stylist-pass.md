# Spot Map — skate-stylist design direction

*Pass for `spots/index.html`. Design direction only — no map code here. The map frontend is greenfield (no `map.js`/`map.css` yet). This is the brief the builder implements after `frontend-designer` corroborates and the user signs off.*

Read alongside: `design/current-state.md` (locked palette/type/aesthetic + the 2026-06-04 "Map frontend UX direction"), `CLAUDE.md` (voice/values), `spots/data/schema.json` (the fields below come straight from here).

---

## The one-sentence read

The landing page is a flyer taped to a bulletin board. The spot map is **the back of that flyer** — the part where someone drew a map to the spot in marker, and the crew added pins and notes over time. Full-bleed map, club chrome floating over it like stickers and tape on glass. Not a flyer wrapped around a tiny map.

There's a direct ancestor in the assets: `skate-spot-oec-griptape.png` is literally a Carolina-blue capsule that says "SKATE SPOT @ THE OEC" sitting on griptape. That flyer is *about a spot*. The map page is the same energy, just interactive. Lean on it.

---

## Hard constraints (carried from current-state, restated so the builder can't miss them)

- **Full-bleed map.** Leaflet fills the viewport. No cream paper frame around a shrunken map. The chrome (title, filters, popups, markers) sits *over* the map.
- **Mobile-first.** Phone is the primary device — a skater standing at a curb checking the next spot. Thumb-reachable controls, popups readable at arm's length in sunlight.
- **Snappy, lightweight.** No heavy decorative PNGs layered over a live map. Markers and chrome are mostly CSS + small SVG. Nothing that fights pan/zoom performance.

---

## 1. Marker design

### The pin shape — derived from the ram skull, not a generic teardrop

Do **not** use Leaflet's default blue teardrop. That's the single biggest AI/generic tell on this page. Also do **not** stamp the full ram-skull PNG at every coordinate — at 30px the skull turns to mud, it's heavy to repaint on every pan, and it clutters fast when spots cluster.

Instead, build the marker as a **small CSS/SVG "spot tag"** that borrows the skull's *construction*, not its silhouette:

- **Heavy dark-blue outline** (`--carolina-deep #1d3a5f`), ~2px, flat fill inside. That thick confident outline is the single most recognizable thing about the logo — every marker reading like it was drawn with the same pen is what ties the map to the brand.
- Shape: a **rounded-rectangle "capsule" tag** echoing the OEC flyer capsule — not a teardrop, not a circle. A short stub/notch at the bottom center points to the exact coordinate (the anchor). Think a hand-cut sticker with a pointer.
- Inside the capsule: a **single glyph for the spot type** (see below) in ink on the fill color. One glyph, no text label on the marker itself — labels live in the popup.
- **The ram skull earns one job, not every job:** the club's *own* home/HQ marker (or a "you are here"-style anchor, if we ever add it) can be the full skull. Regular spots are the capsule tags. This keeps the skull special instead of wallpaper — same discipline as "graffiti bubble letters reserved for special moments."

### Encoding `bust` — color is the loudest channel, so bust owns color

Bust factor is the thing a skater needs to read *before* they ride over. Make it the marker's fill color. Three values, and the color language has to be legible to a skater instantly:

| `bust` | meaning (from schema) | fill | why |
|---|---|---|---|
| `chill` | no one cares | **Carolina blue** `#4B9CD3` | the brand's resting/safe color. Blue = go. |
| `caution` | depends on time/day | **bone/warm-white** `#ebe4d2` (or a muted gold-tan) | neutral, "read the notes first." Reads as paper, on-brand, not a stoplight yellow. |
| `hot` | expect to get kicked | **ink black** `#14171a` fill, with the dark-blue outline | blacked-out = heat. Not red. **Avoid red** — red on a map is a generic "error/danger" UI cliché and it'd be the first thing frontend-designer flags. Black is more skate (think a redacted/blacked-out spot) and stays in palette. |

Rationale for *not* using a red/yellow/green stoplight: it's the most generic possible choices, it would clash with cream+Carolina+ink, and it screams "Google My Maps." We stay in the locked 3-color resting palette (Carolina + bone + ink) and let bust ride entirely on it. **This is a deliberate brand choice — flag for frontend-designer to confirm legibility holds, especially `hot` black markers on dark OSM areas (mitigated by the dark-blue outline + a thin bone halo, see below).**

Add a **thin bone/off-white halo (1–2px) around every marker** so all three fills separate cleanly from any base-tile color — black on a dark park polygon, blue on blue water, etc. Cheap, CSS, solves contrast in one move.

### Encoding `type` — a glyph inside the capsule

Six types in the schema. Use a **simple line/sketch glyph** per type, drawn in the same heavy-outline hand as the skull so they feel hand-cut, not icon-font generic:

| `type` | glyph (sketch, single weight) |
|---|---|
| `ledge` | a low horizontal bar / curb in profile |
| `stairs` | a 3-step staircase profile |
| `rail` | a diagonal handrail line with two posts |
| `transition` | a quarterpipe curve (the "tranny" arc) |
| `flat` | a flat dash / open ground (a single horizontal line) |
| `DIY` | a small trowel/brick mark, or a wet-concrete "fresh pour" squiggle — the scrappiest glyph, on purpose |

Keep them **monoline and recognizable at 16–18px**. If a glyph isn't legible at marker size, it's wrong — kick it back. These can be one tiny SVG sprite shared across all markers (performance: one fetch, reused).

So: **shape is constant (capsule tag), color = bust, glyph = type.** Two channels, no clutter, readable at a glance — which is the whole point of a spot map.

### Clustering

When spots overlap at low zoom, cluster into a **single capsule with a count number** (ink on bone), same outline. Don't let default Leaflet cluster bubbles (those soft green/yellow/red circles) ship — that's a hard generic tell. Restyle the cluster to match the marker capsule or it doesn't go live.

---

## 2. Filter UI

Two filters: **type** (6 values) and **bust** (3 values). Optionally **area** (Chapel Hill / Carrboro / other) later — keep it out of v1 unless the user asks; two filters is already plenty over a full-bleed map.

### Mobile (primary): a bottom sheet with chip rows

- A **thumb-reachable bar pinned to the bottom** of the screen — a short strip that reads like a strip of masking tape across the bottom of the glass, with a label like **"filter spots"** in Permanent Marker, ink. Tapping it raises a **bottom sheet** (slides up from the bottom edge — short, abrupt, no bouncy spring; click → open, click → closed). Bottom placement = thumb reach; this is the whole mobile-first point.
- Inside the sheet: two rows of **chips**.
  - Row 1 — **what** (type): `ledges · stairs · rails · tranny · flat · DIY`
  - Row 2 — **how hot** (bust): `chill · caution · hot`
- Chips are small capsule tags styled like the markers — selected = filled (Carolina for the type row; for the bust row, fill each chip its own bust color so the legend and the filter are the same object). Unselected = outline only on bone. **Selected state is a hard flip, no transition fade.**
- A **"reset / show all"** chip, plain ink outline.

### Desktop: chips float top-left over the map

Same chips, laid out as a small cluster floating over the top-left of the map (clear of Leaflet's zoom control, which we move or restyle). On a strip of "tape" so it reads as stuck-on chrome, not a browser toolbar.

### The legend is the filter — don't build two things

The bust-color chips double as the legend. No separate "key" box. One fewer thing on screen, and it teaches the color language by being interactive.

### Copy / labels (club voice — a skater talking to a friend)

- Sheet trigger: **"filter spots"** (lowercase, Permanent Marker)
- Type row header: **"what"** — chips: `ledges` `stairs` `rails` `tranny` `flat` `DIY`
  - Use **"tranny"** for transition — it's what skaters say, and this audience reads it as the trick word, not anything else. (Flag for the user: if they'd rather play it safe publicly, `transition` is the fallback. My call as the skater in the room: `tranny` is correct and natural here, but it's the user's club and their name on it.)
- Bust row header: **"how hot"** — chips: `chill` `caution` `hot`
- Reset: **"show all"**

Avoid: "Filter by obstacle type," "Difficulty," dropdown `<select>` menus. Dropdowns over a map are a dead-giveaway generic admin-panel look.

---

## 3. Spot popup / detail card

This is where most of the schema surfaces. On a phone it has to be readable at arm's length, one-handed.

### Mobile: tapping a marker raises a bottom card (not a Leaflet balloon)

Default Leaflet popups (white rounded balloon with a little tail and an X) are a generic tell and they're cramped on phones. Replace with a **bottom detail card** that slides up over the lower third of the screen when a marker is tapped — same sheet mechanic as the filter, so there's one interaction language. Map stays visible above it. Tap the map or swipe down to dismiss. Abrupt, no spring.

### Card layout, top to bottom

1. **Spot name** — Anton, ink, tight. This is the headline. (`name`)
2. **Type + bust line** — two capsule tags inline, the *same* tags as the marker/legend (e.g. a blue `ledge` capsule + a bone `caution` capsule). Instantly ties the card back to the pin you tapped. Under it in Permanent Marker, the bust meaning in plain words: chill → "nobody cares," caution → "depends on the day," hot → "you'll get kicked." (`type`, `bust`)
3. **Photo** — if `photos[0]` exists, a single lead photo, full card width, with a **thin ink border and a slight rotation (±1–2°)** like a snapshot taped into the card. Real club photos only — the photographer's point-and-shoot stuff is the whole texture. No photo placeholder graphic; if no photo, the card just skips it (see empty states). Lazy-load; never block the card on the image. (`photos`)
4. **The facts line** — small, Special Elite (typewriter), ink: `surface` · `size` · `area`. e.g. `concrete · knee-high ledge · Carrboro`. Typewriter face = "field notes," reads as data without a clinical table. Skip any field that's empty rather than printing "n/a."
5. **Notes** — Permanent Marker or a clean readable body, ink. This is the crew's voice — the schema says plain text, escape it. (`notes`)
6. **Clips (later)** — when video lands: a small "watch it" row of one or two embed thumbnails (YouTube/Vimeo, per the locked embed-only architecture). Out of scope for v1 — leave a clean spot in the layout for it so it doesn't get bolted on ugly later.
7. **Last verified** — smallest line, Special Elite, muted ink. Phrasing below.

### "Last verified" phrasing (`verified`)

Don't print a raw ISO date as a label-value pair ("Verified: 2026-04-12") — that's admin-panel voice. Say it like a skater:

- Recent: **"checked this spring"** / **"last skated Apr '26"**
- Older: **"last we checked, Apr '26 — might've changed"**
- If `verified` is missing: **"nobody's checked lately — roll up and see"**

Pick one format and compute it from the date; the "might've changed / roll up and see" hedge after a few months is honest and on-voice (spots get capped, this club knows it). Tie a small visual to staleness if easy — e.g. fresh = ink, stale = faded ink — but copy alone is enough for v1.

### Desktop popup

Same content, as a card anchored near the marker (still **not** the default Leaflet balloon styling — restyle the container: square-ish corners, ink border, no glossy white bubble, no default close-X — use a plain ink "×" or "back"). Keep it tight.

---

## 4. Page chrome

### Title / nav over the full-bleed map

- **Top-left: a small stuck-on title block** — a strip of "tape" (reuse a tape SVG from `assets/textures/`) or a torn-paper corner with **"SPOTS"** in Anton, ink, and one line under it in Permanent Marker: **"chapel hill + carrboro"**. Small. It's a label on the glass, not a banner. The map is the page.
- **Back to the site:** the **ram skull (no-lettering PNG)**, small, top-left as the home button — tap it to go back to `index.html`. This is the skull's *other* earned job on this page (home anchor), distinct from a HQ marker. One skull, top-left, clickable. That's it.
- **Don't rebuild the full landing nav** over the map. A skater opened the map to find a spot — give them the map, a way home (skull), and the filters. Anything else is clutter over a tool.
- **Submit button:** small capsule, bottom-right or in the filter sheet — **"know a spot?"** (Permanent Marker). Goes to the submission flow (or sits dark/disabled in v1 read-only with **"submissions soon"**). Per the backend phases, v1 is read-only — so this is a styled-but-dark affordance in v1, live in v2.

### Base tile styling — tint, don't fight

Raw OSM tiles are loud: bright green parks, blue water, red POI pins, orange roads, dense colored labels. Dropped under cream+Carolina+ink markers, it looks like two unrelated apps. Two acceptable paths, in order of preference:

- **Preferred — a muted/desaturated base** so the club chrome pops. Either (a) a low-saturation raster style (CARTO Positron-style "light, muted" tiles — clean, pale, lets ink+Carolina markers dominate), or (b) a light CSS filter on the OSM raster layer: `filter: saturate(0.55) sepia(0.08) contrast(0.95);` to knock OSM's candy colors toward a warm paper-ish neutral that sits with cream. The CSS-filter route is the cheapest and keeps us on plain OSM with no extra provider — **start there**, measure, escalate to a real muted tile provider only if OSM-under-filter still reads junky. *(Mind OSM/CARTO tile attribution + usage policy — note for the builder/security, not a design issue.)*
- **Do NOT** attempt a fully custom cream-and-Carolina vector basemap for v1. It's a big lift, it fights the "snappy/lightweight" constraint, and it's where a project goes to die. A filtered raster gets 90% of the cohesion for ~5 minutes of CSS.
- Whatever we pick, **the markers must out-contrast the base**, hence the bone halo in §1.

### Leaflet's own UI

Restyle or relocate the default `+ / −` zoom control and the attribution. Default Leaflet controls are a recognizable generic look. Square them off, ink them, or move zoom to a thumb-reachable bottom-right on mobile (away from the bottom filter bar). Attribution stays (required) but can be small/muted.

---

## 5. Copy (collected, club voice)

- **Page title strip:** `SPOTS` / `chapel hill + carrboro`
- **Filter trigger (mobile):** `filter spots`
- **Type chips:** `ledges` `stairs` `rails` `tranny` `flat` `DIY`
- **Bust header:** `how hot`  **Bust chips:** `chill` `caution` `hot`
- **Bust meanings (in card):** chill → `nobody cares` · caution → `depends on the day` · hot → `you'll get kicked`
- **Reset:** `show all`
- **Verified:** `checked this spring` / `last skated Apr '26` / `last we checked, Apr '26 — might've changed` / `nobody's checked lately — roll up and see`
- **Submit:** `know a spot?` (live in v2) / `submissions soon` (v1 dark state)
- **Home button:** ram skull, no text.

### Empty states (don't leave a blank map / blank card)

- **No spots match the filters:** `nothing matches — loosen it up` with a `show all` chip right under it. (Not "No results found.")
- **Map can't load / backend down (snapshot fallback active):** the map still shows last-known public spots silently (that's the whole point of the snapshot). If even that fails: `map's down right now — hit us on IG` with the IG link. Honest, not a spinner-of-doom or a corporate error page.
- **Spot has no photo:** card just omits the photo block. No "image coming soon" placeholder, no gray box with a broken-image glyph — that's the genericest possible move.
- **Loading:** brief, ink. If we want flavor, `finding spots…` in Permanent Marker — but if the snapshot loads instantly (it should), the user never sees it. No spinner gif.

---

## AI / generic-look tells to avoid (flagging for frontend-designer to corroborate)

These are the things that would make this map read as a Mapbox/Google template instead of UNC Skate Club. Frontend-designer should pressure-test each:

1. **Default Leaflet teardrop markers** — the #1 tell. Must be the capsule tags.
2. **Stoplight red/yellow/green for bust** — generic *and* off-palette. We use Carolina / bone / ink. (Confirm `hot` black-marker legibility — that's the one risk in this choice.)
3. **Default Leaflet popup balloon** (glossy white, rounded, tail, X) — replace with the bottom card / restyled container.
4. **Default Leaflet cluster bubbles** (soft colored circles) — restyle to the capsule.
5. **Raw OSM candy-color tiles** under the chrome — must be muted/filtered.
6. **A cream paper frame around a shrunk map** — violates full-bleed; the whole reason this is its own direction.
7. **`<select>` dropdown filters / a "Filter by…" admin bar** — use chips.
8. **Icon-font glyphs (Font Awesome map-pin, etc.)** — the type glyphs must be drawn in the skull's heavy-outline hand, or they'll read generic.
9. **Bouncy/spring sheet animations, parallax, scroll-fade** — sheets snap open/closed. Click → state → done. Skating is abrupt.
10. **Stock/placeholder map imagery** — only the club photographer's real photos in cards. No image placeholders ever.

## Open calls for the user (don't let the builder decide these silently)

- **`tranny` vs `transition`** as the public chip label — my call is `tranny`, but it's your club's public surface (§2).
- **`hot` = black marker** — deliberate anti-stoplight choice; confirm you're good with blacked-out = heat, and that legibility holds in field testing (§1).
- **Bottom sheet for both filter and detail** — one interaction language; confirm that's the feel you want before the builder commits to it (§2/§3).

---

## Buildable summary (the short version for the builder)

- Full-bleed Leaflet. Muted/filtered OSM raster (start with the CSS filter).
- **Marker** = CSS/SVG capsule tag, heavy `--carolina-deep` outline, bone halo. **Fill = bust** (Carolina/bone/ink). **Glyph = type** (6 monoline sketch glyphs in one SVG sprite). Bottom notch = anchor. Ram skull reserved for home button + (maybe) HQ.
- **Filters** = bottom sheet (mobile) / floating chips (desktop). Two rows: type, bust. Chips = same capsule tags = double as legend. Hard-flip selected state.
- **Detail** = bottom card (mobile) / restyled container (desktop): Anton name → type+bust tags + plain-words bust → taped photo → Special Elite facts line → notes → (clips later) → "last verified" in skater phrasing.
- **Chrome** = small taped `SPOTS / chapel hill + carrboro` title top-left, clickable ram skull = home, `know a spot?` submit (dark in v1).
- Copy + empty states per §5. No spinners, no placeholders, no default Leaflet anything.
