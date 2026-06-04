# UNC Skate Club site — current state

*Snapshot as of 2026-06-01. Single source of truth for "where is the build right now and what's the next decision." Read this first if you're picking up the project with cleared context.*

> **2026-06-01 architecture pivot — read this before the map sections below.** The spot map is moving from the original *static-site + Formspree + client-merged JSON* plan to a **real backend** (FastAPI + Postgres/PostGIS + a Celery/RabbitMQ image worker). This was a deliberate decision: the map is photo- and data-heavy, needs genuine auth/privacy for private spots, and the static workarounds (co-locating `private.json` under `/admin/` and hoping nobody guesses the URL, honor-system email checks) were the most fragile parts of the design. See **"Map architecture (backend)"** below. The brand / visual / landing-page language is **untouched** — this pivot is purely the data + serving layer. The static-map references in `CLAUDE.md`, `TODO.md` (now updated), `spots/data/schema.md`, and `admin/data/README.md` are **superseded** for the map; the schema field definitions still describe the data shape (now a DB model + snapshot format).

## What exists

- **Repo**: `C:\Users\julia\Tempo\uncskate-site\` (sibling to the trick generator at `..\todaytodo\`).
- **Build state**: above-the-fold landing prototype, v7. No other pages, no JS, no below-the-fold content.
- **Entry point**: `index.html` (open directly in a browser; static site, no build step).
- **CSS**: `styles/global.css`.
- **Agents**: `planner`, `builder`, `reviewer` (standard); `skate-stylist`, `frontend-designer`, `security` (uncskate-specific, in `.claude/agents/`).

## What's locked (do not propose changing without explicit user reopening)

### Brand & copy
- **Site title / banner**: "SKATE CLUB / AT UNC" (two lines, Anton, line-height 0.9). NOT "UNC Skate Club" — that's the registered club name (still on the logo and IG handle).
- **Rejected naming**: "Thrill Hill" (IG profile display name; user dislikes).
- **Inclusivity copy line**: "any board. any wheels. first time on one is fine." Permanent Marker, ink. Beginners + women + all wheels (rollerbladers) are core values, woven through copy without becoming a marketing hook.

### Palette
- `--carolina: #4B9CD3` (logo skull; brand primary)
- `--carolina-deep: #1d3a5f` (logo outline; deep accent)
- `--paper: #f0ebe1` (cream — **confirmed**, no longer provisional)
- `--paper-fallback: #ebe4d2` (bone — pre-staged but currently unused)
- `--ink: #14171a` (near-black, warm)
- `--wall: #111` (used inside inner tear where wall shows through; the actual page wall is the bulletin board image)
- `--magenta: #E5197F` (video / Women in Skate contexts only)
- `--purple: #6E3AA8` (event-flyer contexts only)
- **Cohesion rule**: 3-color resting state (Carolina + cream + ink). Accents are contextual, never both magenta and purple on the same page.

### Typefaces (all Google Fonts)
- **Anton** — display / banner. Sole display face. No Druk, no Bowlby.
- **Permanent Marker** — hand-drawn body, meeting info, captions, accent lines.
- **Cabin Sketch** — nav row links and sub-headlines. **LOCKED — never propose changing.**
- **Special Elite** — typewriter, meta / short blocks. Currently loaded but used sparingly.
- **VT323** and **Newsreader** — defined in spec for future use (video pixel face / long-form body) but not loaded for v7 yet.
- **Hard NO**: Inter, Poppins, Roboto, Montserrat, Work Sans, `system-ui`.

### Layout decisions (in `index.html` as of v7)
- **Wall** = `body` background, `assets/textures/wall-bulletin-board.jpg` (renamed from `Bulletin board, option one. .jpg`), tiled at 600px.
- **Paper** = `<main>.paper`, ~95% viewport, cream background with `::before` overlay tiling `white-ripped-paper-png.webp` interior + `paper-texture.svg` noise, `mix-blend-mode: multiply`, opacity `0.55`.
- **Four torn edges** at the paper boundary (top, bottom, left, right) — each using `white-ripped-paper-png.webp` rotated per side with different `background-position`. **Side edges have a known geometry bug — see "Open issues" below.**
- **Four corner tape pieces**, asymmetric: TL scotch-yellow `+12°`, TR white-masking `-7°`, BL blue-painter's `+4°`, BR black-duct `-9°`. Different lengths (95–140px).
- **Hero band collapsed with banner** (one section): big ram skull `assets/logo/unc-skate-logo-no-lettering.png` left of Anton "SKATE CLUB / AT UNC" wordmark in ink. Horns hard-crop through the torn top edge. Hero background is plain cream (griptape moved off here).
- **Carolina-blue capsule** on the right of the hero with "spring 26 / chapel hill" in Permanent Marker.
- **Nav row** (`SPOTS · MEETINGS · ABOUT · IG`) in Cabin Sketch, cream-colored text, with `assets/textures/skateboard-grip-tape.jpg` as background-image (`cover`). Full inner-paper width.
- **Handrail divider** between nav and meeting info: inline SVG from `design/claude-design-import/project/Skate Handrail.svg` with animation CSS lifted from `Skate Handrail.html`. Config: black rail (`#1a1a1a`), cap hat, sparks on, skater scale 0.7, animation speed 12.5s.
- **Meeting info** on cream paper, Permanent Marker, ink.
- **One inner tear** (asymmetric placement) between hero/meeting block and the bottom of the page, showing ~6px of `--wall` color through.
- **Mobile** under 600px: drop left+right torn edges, drop TR+BL tape pieces (keep TL scotch + BR duct diagonal), tape shrinks, Anton banner drops to ~80px, Permanent Marker bumps to ~24px so it isn't swallowed.

### Visual hierarchy (z-index)
- `.paper`: container
- `.paper::before` (paper texture overlay): z 1
- `.paper__inner` (content): z 2
- `.edge--*` (torn edges): z 3
- `.tape--*`: z 5
- `.hero__skull` (logo): z 6

## What's working

- Wall + paper + corner tape composition reads as intended ("flyer taped to bulletin board")
- Top and bottom torn edges
- Tape asymmetry
- Banner: ram + Anton wordmark, horns cropping through torn top edge
- Carolina-blue capsule on cream
- Nav-row griptape with cream Cabin Sketch links
- Animated handrail divider (skater grinding back and forth, 12.5s loop)
- Meeting info block on cream paper
- Inner tear

## Open issues

### 1. Side torn edges — geometry bug (high priority)

Builder diagnosed during v7: the current `.edge--left/--right` implementation creates a tall-narrow `<div>` then applies `transform: rotate(-90deg)` (or 90°) for the right side. CSS transform rotates around the box's center, which compresses the rotated box into a short wide stripe **centered on the paper's edge midpoint** — not a tall vertical strip running the full height of the paper. That's why v5/v6/v7 only show "a really little strip" on the sides regardless of width/bleed tuning.

**Three paths forward** (user has not picked yet — this is the active decision):

- **A. Rewrite edge geometry (no new assets needed)**. Rebuild `.edge--left/--right` as wide-short boxes (e.g. `width: 100vh; height: 110px`), then `rotate(-90deg)`. Yields an actual full-height vertical strip. Pure CSS work, ~one builder pass.
- **B. Generate a dedicated asset in Claude Design**. Either a vertical-tear strip for the sides (drop-in replacement), or a full-page torn-cream-paper image that replaces the whole `.paper` element. The latter cleans up architecture significantly.
- **C. Pivot to original mockup architecture**. The user's Claude Design mockup at `design/claude-design-import/project/Skate Club Site.html` has **cork as the page background everywhere**, hero as dark griptape rectangle, nav directly on cork, handrail directly on cork, and cream only as a small torn-paper accent in the corner of the hero. We've drifted from that. Pivoting would eliminate the side-edge problem entirely but means a larger restructure of what's already built.

Claude's recommendation when last asked: **B with a vertical-tear strip** — quickest path to actually-torn sides while keeping the v7 build mostly intact. The user opted to clear context before deciding.

### 2. Griptape on nav row may read as zoomed-in

Builder flagged in v4: `skateboard-grip-tape.jpg` was sized for the original tall hero band. Now at nav-row height with `background-size: cover` the texture displays at significant zoom. User said "we can kind of get away with a worse texture" so it stayed. If it ever reads as blurry, one-line fix: swap to `background-size: auto` (native pixels, tiled).

### 3. Logo over griptape (resolved in v3/v4)

With the no-lettering transparent PNG and the griptape moved off the hero, the logo no longer overlaps any dark texture. `mix-blend-mode: multiply` is gone. Z-index 6 keeps it above everything in its layer.

## Iteration history (v1 → v7)

- **v1** (builder): scaffolded `index.html` + `global.css` + hand-drafted SVG textures (paper, torn edges, tape, inner tear, griptape).
- **v2** (builder): swap to real assets — bulletin board wall, `Skateboard grip tape.jpg`, `white-ripped-paper-png.webp` for torn edges. Collapsed banner + hero into one section. Applied `mix-blend-mode: multiply` to logo (used `_With_Letters.png` by mistake).
- **v3** (builder): added animated handrail divider from Claude Design bundle. Tried to swap to transparent logo but the no-lettering version didn't exist yet — accidentally used `_With_Letters.png`.
- **v4** (builder): logo swap to no-lettering (renamed `unc-skate-logo-no-lettering.png`). Griptape moved from hero band to nav row. Hero reverted to plain cream. Anton wordmark + scribble switched to ink (now on cream). Nav links switched to cream (on griptape).
- **v5** (builder): tried `mix-blend-mode: multiply` on side torn edges to color-match white texture to cream paper. Over-corrected — sides became invisible.
- **v6** (builder): replaced multiply with `filter: sepia(0.35) brightness(0.94) saturate(0.55)` on sides. Visible but still thin. Builder honest: source asset is horizontal-tear; rotation doesn't yield true vertical fringe.
- **v7** (builder): added paper-surface texturing across whole `.paper` (tiled webp + svg noise, multiply blend, 0.55 opacity). Pushed side edges to 110px wide with -70px bleed. Builder diagnosed the rotation-geometry issue and named the three paths forward.

Per-iteration agent reports are saved in `design/`:
- `frontend-designer-pass-1.md`, `pass-2.md`, `pass-3.md`
- `skate-stylist-pass-1.md`, `pass-2.md`, `pass-3.md`
- `v2-changes.md`
- `locked-spec.md` (the v2-baseline spec; deltas in v3–v7 not folded back in)

## Where assets live

- **Logo**: `assets/logo/unc-skate-logo-no-lettering.png` (transparent, no lettering — the one in use). Also `UNC SKATE LOGO.png` (original, with white bg) and `UNC_SKATE_LOGO_transparent_With_Letters.png` (transparent, with letters — unused).
- **Wall**: `assets/textures/wall-bulletin-board.jpg` (renamed from `Bulletin board, option one. .jpg`). Other options also present: `Bulletin Board 2.jpg`, `blackchalkboardoption1.jpg`, `blackchalkboardoption2.png`.
- **Griptape**: `assets/textures/skateboard-grip-tape.jpg` (renamed from `Skateboard grip tape.jpg`).
- **Torn paper texture**: `assets/textures/white-ripped-paper-png.webp` (real-scanned, horizontal-tear). Rejected: `brown-ripped-paper-background-with-place-for-your-text-vector.jpg` (Canva-vector tell per skate-stylist).
- **Tape SVGs**: `assets/textures/tape-{scotch,masking,painter,duct}.svg` (hand-drafted, in use).
- **Inner tear SVG**: `assets/textures/inner-tear.svg`.
- **Paper-texture SVG**: `assets/textures/paper-texture.svg` (SVG turbulence noise).
- **Original handrail SVG**: `design/claude-design-import/project/Skate Handrail.svg` (currently inlined into `index.html`).
- **Flyer references** (visual language source of truth): `assets/flyers/*.png` (6 files — `pluto-premiere-flyer.png`, `women-in-skate-flyer.png`, `skate-spot-oec-griptape.png`, `ig-grid-recent.png`, `ig-grid-ram-skull-tees.png`, `ig-grid-exec-portraits.png`).

## Claude Design bundle

A full design bundle from `claude.ai/design` is at `design/claude-design-import/`. Contents:
- `README.md` (Claude Design's own handoff readme — read first if implementing more from the bundle)
- `chats/chat1.md` (the full design conversation that produced the handrail)
- `project/Skate Handrail.html` — React preview prototype for the handrail
- `project/Skate Handrail.svg` — standalone SVG asset (currently inlined into the site)
- `project/Skate Club Site.html` — **the full original site mockup, the reference for Path C above**
- `project/tweaks-panel.jsx` — Claude Design's tweaks-panel component (not relevant to implementation)
- `project/uploads/pasted-1779246053831-0.png` — screenshot the user pasted into Claude Design

## Map architecture (backend) — supersedes the static-map plan

*Decided 2026-06-01. The landing page stays static (GitHub Pages / Claude Design). Only the map + submissions + admin become backend-backed. Frontend stays Leaflet — it fetches from an API instead of a flat JSON file.*

### Stack (locked)
- **API**: FastAPI + SQLAlchemy + Alembic (migrations).
- **DB**: Postgres + **PostGIS** (geospatial queries — viewport bounds, nearest, radius — instead of shipping the whole dataset to the browser). Leaning **Neon** free tier (persistent, scales to zero, PostGIS-capable, does *not* auto-delete like Render's free Postgres).
- **Image pipeline**: **Cloudflare R2** for photo storage (10 GB free, zero egress) + a **Celery worker on RabbitMQ** (or serverless Redis broker — Upstash/CloudAMQP free tiers) for thumbnails, web-format transcode, and **EXIF GPS stripping** (privacy: a private-spot photo must not leak coordinates in metadata).
- **Hosting**: scale-to-zero PaaS (Fly.io / Koyeb) — finalized closer to deploy; the architecture holds regardless.

### Video / clips (decided 2026-06-03)
Video is **embed-only — we never host video ourselves.** Self-hosting video would blow every cost/durability constraint (a single clip is 50–200 MB → R2's 10 GB free tier fills in ~50 clips and "breaks the site"; streaming egress is 10–100× photos; transcoding chokes a free scale-to-zero worker). So:
- **YouTube + Vimeo only.** The skater uploads to one of those (theirs or the club channel — the Pluto premiere already lives on YouTube); we store only a **provider + video ID** in Postgres. The frontend renders an embed.
- **Clips are attached to a spot**, not a standalone feed (for now). Spot detail = a photo in the main description + a set of clips of that spot to watch. Exact UI deferred. A standalone "trick-challenge" feed (tie-in with the trick generator at `tricks.uncskate.club`) is a *maybe-later*, explicitly out of scope for now.
- **Free + survives backend death**: a video ID is a few bytes in the DB; embeds are plain `<iframe>`s that keep working on the static-snapshot fallback even if the backend is gone.
- **Security guardrail**: never accept raw iframe HTML or arbitrary URLs. The backend whitelists provider (YouTube/Vimeo only), parses out just the video ID, and *we* construct the embed URL ourselves — use the privacy-enhanced `youtube-nocookie.com/embed/<id>`. Exec reviews every clip before it goes live (content moderation).
- **Stack impact: none.** It's a `videos` table (provider, video_id, caption, spot FK) + a frontend embed component. The Celery/RabbitMQ worker stays photo-only.

### Map frontend UX direction (decided 2026-06-04)
- **Full-bleed map.** If the map is on the page, it's *the* page — a real full-screen map, not a small framed-like-a-flyer panel. The zine/club visual language lives in the chrome *over* the map (filter chips, popups, marker design), not in a frame around a shrunken map.
- **Mobile-first.** Most visitors will be on phones (skaters checking spots out in the field). Design and build for small touch screens first, then scale up — touch-friendly controls, thumb-reachable filters, readable popups on a small screen.
- **Must not feel clunky.** Snappy and responsive is a hard requirement: fast load, smooth pan/zoom, no janky interactions, no heavy assets. This reinforces the snapshot-first approach (serve a static file fast, hydrate from the API) and keeps the marker/popup implementation lightweight.

### Governing principle: the public site must survive the backend dying
Free tiers change terms, billing lapses, accounts get orphaned after exec turnover / graduation. So we design for graceful degradation: **the backend periodically writes a static snapshot of approved public spots** (`public-spots.json` on R2 or committed to the Pages repo). The public map reads the live API when up and **falls back to the last snapshot when it's down.** Worst case after the backend dies = the map shows the last-known public spots and the submit button is dark. Nothing *breaks*. This also keeps the public map fast/cheap (served mostly as a static file; API only for fresh data).

### Cost / durability constraints (user's hard requirements)
- **Free**, and must **not unexpectedly break after the founder graduates.**
- **Storage can't fill up and take down the site** → photos live on R2, never in the DB; DB holds metadata + R2 URLs only, so it stays tiny.
- **Pre-graduation checklist** (don't forget): migrate all accounts (PaaS, Neon, R2/Cloudflare, domain, broker) to **club-owned shared billing/logins** before handoff so nothing gets orphaned.

### Who can add spots, by phase
- **v1**: founder only, via a **backend seed script** (direct DB insert). No uploader, no auth, no worker. Public sees a read-only map.
- **v2**: public *request* form → DB moderation queue → founder/exec **moderation UI** (built by hand — no Django admin since we chose FastAPI). Uploader + R2 + image worker arrive here.
- **v3**: real auth, exec roles, private spots that never leave the server unless authorized.
- **v4**: UNC-email-verified users get a fast-track contributor lane on the same uploader.

### v1 build status (2026-06-04)

**Backend foundation — built AND verified end-to-end (2026-06-04).** `backend/` holds FastAPI + SQLAlchemy + Alembic, PostGIS models (`spots` + the v2-anticipating `videos` table), read-only `/api/spots` (bbox) + `/api/spots/{id}`, an editable `seed_data.json` + idempotent seed script (4 placeholder Chapel Hill/Carrboro spots), and `snapshot.py`. `security` pass: no blockers; fixed CORS prod-warning + bbox range guard. **Stood up end-to-end** with `uv` (0.11.x): Docker PostGIS up, migration applied (tables + extension + GiST index verified), seed idempotent (4 spots), snapshot regenerated, all endpoints verified (health, spots, bbox include/exclude, 400 guards, 404), migration round-trip clean. **`uv.lock` now committed** (resolves the security flag). **pytest suite** (`backend/tests/`, 7 tests, all pass): health, public-only invariant, bbox filter, bad-bbox 400s, 404, seed idempotency, snapshot↔schema validation — run against a dedicated `uncskate_test` DB.

Two fixes the standup surfaced: (1) **missing `shapely` dep** — `geoalchemy2.shape.to_shape` needs it, and without it the snapshot writer *and every `/api/spots` call* break on a clean install; fixed via `geoalchemy2[shapely]`. (2) Local DB host port **5432 → 5433** (5432 was taken by another project's container). Run commands: `cd backend; docker compose up -d; uv run uvicorn app.main:app --port 8000`; tests: `uv run pytest`. Frontend static preview still: `python -m http.server 5500` at repo root.

**Map frontend — built.** `spots/index.html` + `map.js` + `map.css`. Full-bleed muted-OSM street map, mobile-first, capsule `divIcon` markers (OEC-flyer language) with hand-drawn type glyphs, thumb-zone filter chips that double as legend, cream torn-paper detail bottom sheet, ram-skull home/loading, snapshot-first paint with guarded API hydrate + masking-tape stale banner. Renders from `spots/data/public-spots.json` (hand-generated from seed data; `snapshot.py` regenerates it authoritatively once the DB runs). `security` pass: no blockers; fixed the one gap (unescaped `type`/`bust` in marker HTML → now whitelist-validated). `esc()` + `safePhoto()` verified solid.

**Decisions locked 2026-06-04:**
- Filter chip label is **`transition`** (not "tranny") — matches the beginner-welcoming voice.
- Base map = **muted OSM street tiles** (not satellite); the spot photo in the popup covers "see the actual spot."
- Detail sheet uses **cream `--paper`** (fall back to bone `#ebe4d2` only if it reads muddy over tiles).
- **Markers = one Carolina-blue capsule; glyph = type is the only differentiator.** (Resolved: the color-vs-state bust spike + toggle were removed — read as confusing without a legend. Bust lives in the filter chips + popup only.)
- **`skatepark` added as a 7th spot type** (schema + frontend + backend migration). For the Chapel Hill/Carrboro skatepark(s).
- **Initial map zoom = 14** (was 13 — read as too wide). **Hard pan boundary added** (`maxBounds` ~`[[35.79,-79.20],[36.03,-78.91]]`, `maxBoundsViscosity: 1.0`, `minZoom: 12`) — campus + ~15-min-drive ring; can't wander to Durham/Raleigh. Tune the box if it feels off.
- **`bust` stays optional** (already optional in the schema; confirmed — submission form/intake won't require it).
- **Spot intake (interim) = a Google Form** the founder shares → Sheet → exec review → hand-add to `seed_data.json`. Validation gate = human review + `schema.json` + the snapshot↔schema test. The real v2 form/queue comes later.
- **Votes + comments** requested → added to the roadmap as **v5** (design deferred).

**Design direction docs:** `design/spot-map-skate-stylist-pass.md`, `design/spot-map-frontend-designer-pass.md`.

**Carried to v2 (security):** set `API_BASE` to an **https** origin before the backend deploys (http is dead/blocked on Pages); add a `/spots/` CSP (`img-src https: 'self'`, script-src Leaflet CDN only); ensure `submitted_by` goes through `esc()` when the v2 sheet renders it.

## Next steps (planned, not yet started)

- **Finish v1**: user picks the marker style; stand up + verify the backend (uv/PostGIS); then real seed spots replace placeholders.
- v2 submissions + uploader + image worker (R2, EXIF stripping, moderation UI).
- v3 auth + private spots.
- v4 UNC-verified contributor fast-track.
- Landing-page side-edge CSS bug (unrelated to map; being redesigned in Claude Design separately — not active here).
- Domain purchase (`uncskate.club`).
- Photo placement strategy (club photographer has hundreds of real photos — weave throughout, not one gallery).
- Video gallery / link to Pluto premiere (on YouTube).
