# UNC Skate Club site — Roadmap

## v0 — Above-the-fold landing prototype (in progress, currently v7)

- [x] Drop logo + flyer examples into `assets/`
- [x] `frontend-designer` + `skate-stylist` pass to lock visual language
- [x] Scaffold index.html + global.css + textures
- [x] Replace synthesized assets with real photos (bulletin board, griptape, torn paper)
- [x] Animated handrail divider from Claude Design bundle
- [x] Transparent logo swap (no-lettering version)
- [x] Move griptape from hero band to nav row
- [x] Texture paper surface so it reads as fibrous paper, not solid cream
- [ ] **OPEN**: fix side torn edges (CSS-rotation geometry bug — see `design/current-state.md` for the three paths forward)
- [ ] Below-the-fold content (flyers wall, photo block, etc.)

## Map architecture — 2026-06-01 pivot to a backend

The map moved off the static-site plan onto a **FastAPI + Postgres/PostGIS** backend with a **Celery/RabbitMQ image worker** and **Cloudflare R2** photo storage. Full rationale + the durability/cost constraints are in `design/current-state.md` → "Map architecture (backend)". Hard rules driving everything:
- Free, and **must not break after the founder graduates** (orphaned accounts, lapsed free tiers).
- Photos live on R2 (never in the DB) so storage can't fill up and take the site down.
- The **public map survives the backend dying**: backend writes a static `public-spots.json` snapshot; the map falls back to it when the API is down.
- Pre-graduation: migrate all infra to **club-owned** accounts.

The static-map references in `spots/data/schema.md` and `admin/data/README.md` are superseded; their field definitions still describe the data shape (now a DB model + the snapshot format).

## v1 — Public map, backend-backed (read-only)

- [x] Postgres + PostGIS schema / SQLAlchemy models + Alembic migration (spot fields per `schema.md`) — built, not yet run
- [x] FastAPI read-only endpoint(s) — `/api/spots` (+ viewport/bounds query support via PostGIS)
- [x] Backend **seed script** — reads editable `backend/seed_data.json`; idempotent (4 placeholder spots so far)
- [x] Map page (Leaflet + OSM) reads the API; **static-snapshot fallback** when API is down
- [x] Snapshot job — `backend/app/snapshot.py` writes `spots/data/public-spots.json`
- [x] Custom marker design derived from club assets — OEC-capsule markers; **two bust styles shipped for a spike (`?markers=color|state`), user to pick**
- [x] Filter UI — type + bust; chip label is **`transition`** (not "tranny")
- [x] Spot detail popup — cream torn-paper bottom sheet; user strings escaped, photo URLs allowlisted
- [x] **Anticipate video in the data model**: `videos` table created (model + migration only; nothing serves it)
- [x] `security` pass — backend + frontend reviewed; no blockers; gaps fixed (CORS prod note, bbox range guard, marker `type`/`bust` whitelist)
- [ ] **User picks the marker style** (`color` vs `state`), then delete the loser
- [x] **Stand up + verify the backend** — uv installed, PostGIS up (port 5433), migrate → seed → snapshot → endpoints all verified; `uv.lock` committed; pytest suite (7 tests) passing; fixed a missing `shapely` dep that broke `/api/spots` + snapshot on clean install
- [ ] Replace placeholder seed spots with real Chapel Hill / Carrboro spots
- [ ] Decide free hosting (Fly.io / Koyeb) + Neon DB; deploy (set `API_BASE` to https before deploy)

## Interim — Google Form intake (before the real form exists)

- [ ] **Google Form** the founder shares with skater friends → responses land in a Google Sheet. Exec reviews each, then it's hand-added to `backend/seed_data.json` (re-seed + re-snapshot). This is the *validation gate for now*: human exec review + the JSON schema (`schema.json`) + the snapshot↔schema pytest test. Form fields map to the schema; **`bust` is optional**. Lets us collect real spots fast without building the v2 form yet.

## v2 — Submissions + uploader + image worker

- [ ] Public *request* form → DB moderation queue (rows with status, not an email inbox)
- [ ] Photo upload → Cloudflare R2; Celery/RabbitMQ worker: thumbnails, web-format transcode, **EXIF GPS stripping**
- [ ] Honeypot / rate-limit / validation on submissions (server-side now)
- [ ] Exec **moderation UI** (hand-built — FastAPI, no Django admin) to approve/reject → publish to map + refresh snapshot
- [ ] "Last verified" stamp updates on exec review
- [ ] **Clips attached to spots** — submission accepts a YouTube/Vimeo link; backend whitelists provider + extracts video ID (reject raw iframe/arbitrary URLs); frontend embeds via `youtube-nocookie.com/embed/<id>`; exec reviews each clip. Spot detail shows photo + clips. (Standalone trick-challenge feed = maybe-later, out of scope.)

## v3 — Auth + private spots

- [ ] Real auth (sessions/roles); exec role gating
- [ ] Private spots — never leave the server unless the requester is authorized (no client-side gating)
- [ ] Private-spot photos gated in R2 (signed URLs / private bucket)
- [ ] `security` pass: confirm zero private-spot leakage from public routes/endpoints

## v4 — UNC-verified contributor fast-track

- [ ] UNC-email verification (OTP or OAuth, `@unc.edu` / `@email.unc.edu`)
- [ ] Verified UNC users → pre-trusted fast-track lane on the uploader; non-UNC → standard request queue

## v5 — Community signal (votes + comments) — planned, details TBD

*Requested 2026-06-04. Add to plan now, design later.*

- [ ] Upvote / downvote on spots (is it good? still there? worth the trip?)
- [ ] Comments on spots
- [ ] Open design questions for later: anonymous vs identified voting (abuse/ballot-stuffing prevention — likely needs the v3 auth or at least rate-limiting); comment moderation (execs review, or post-and-flag); schema (votes + comments tables, spot FK); how votes surface on the map/popup; whether votes feed a "last confirmed skateable" signal.

## Landing page

- [ ] Build only after visual language is locked from assets
- [ ] Landing + about + meeting info (when, where, who)
- [ ] Embed / link to trick generator at `tricks.uncskate.club`
- [ ] Two light mentions of beginner-friendly + all-wheels (rollerbladers welcome) — not a headline, woven through
- [ ] Photography woven throughout, not siloed in one gallery — request batch from club photographer once frontend-designer locks layout zones

## Video gallery

The club has multiple skate videos. At minimum the **Pluto premiere** needs a home.

- [ ] Video row / gallery section (landing or dedicated `/videos/` page — decide once layout lands)
- [ ] Link Pluto premiere ("Skate Club's First Video Premiere ft. Jinx") prominently
- [ ] Treatment for video thumbnails should pull from the Pluto flyer aesthetic (Y2K chrome / starfield) per [[uncskate-visual-language]]
- [ ] Confirm where videos live (YouTube / Vimeo / self-hosted) before wiring embeds

## Domain / DNS

- [ ] Buy `uncskate.club` (Cloudflare or Porkbun)
- [ ] DNS → GitHub Pages
- [ ] Confirm HTTPS on apex + www
- [ ] Wire Cloudflare Access (free tier) to `/admin/`

## Open questions

- ~~Which existing spot finder did jviten reference?~~ **Resolved**: not usable — it has no Chapel Hill spots, which is the whole gap this project fills. Reference only, nothing to reuse.
- ~~Photo hosting: in-repo vs R2 vs external.~~ **Resolved**: Cloudflare R2 (10 GB free, zero egress), photos out of the DB. Reached via the backend pivot.
- Free hosting for the FastAPI app + worker + broker — Fly.io vs Koyeb, RabbitMQ (CloudAMQP) vs serverless Redis (Upstash) broker. Decide near deploy.
- Instagram as a data source — see open conversation thread.
