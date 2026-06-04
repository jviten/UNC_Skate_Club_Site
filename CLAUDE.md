# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

The UNC Skate Club's public-facing website. Static HTML/CSS/JS, hosted on GitHub Pages, eventually at `uncskate.club`. Sibling project to the trick generator at `C:\Users\julia\Tempo\todaytodo` (live at `tricks.uncskate.club`).

First real feature: a Chapel Hill + Carrboro skate spot map. Leaflet + OSM, tiered visibility (public spots open to everyone, private spots gated behind Cloudflare Access for execs), user submissions via Formspree with manual exec review.

## Where to start

If you're picking up this project with no prior context, read **`design/current-state.md`** first. It's the single source of truth for what's built, what's locked, and what decisions are open. It supersedes any contradiction with `design/locked-spec.md` (which captures the v2 baseline; later iterations are tracked in current-state).

## Running it

Open `index.html` directly in a browser. No build, no install, no package manager.

## Architecture (target)

```
uncskate-site/
├── index.html             # landing
├── about.html             # club / meetings
├── styles/global.css      # site-wide visual system
├── assets/                # logo + flyer references (source of truth for design)
├── spots/
│   ├── index.html
│   ├── map.js             # Leaflet wiring
│   ├── map.css
│   ├── submit.html        # Formspree submission form
│   └── data/
│       ├── public.json    # public spots, served to everyone
│       └── private.json   # gated, served only at /admin/
└── admin/                 # behind Cloudflare Access (exec emails)
    ├── index.html
    └── queue.js
```

## Agents

Use them in order. Don't skip steps.

- **`planner`** — designs each feature before code. Read-only plan (goal, approach, files, steps, open questions).
- **`builder`** — implements an approved plan literally. No invented scope.
- **`reviewer`** — punch list after code is written (blockers / should-fix / nits).
- **`skate-stylist`** — design, copy, trick-list decisions. Skate-cultural authenticity (Polar / Quasi / Thrasher / FA).
- **`frontend-designer`** — anti-AI tells. Grounds visual choices in `assets/`. Pairs with skate-stylist on visuals.
- **`security`** — read-only security review before merging anything to `main`. Critical job: prevent `private.json` leakage into anything served to non-execs.

For any visual or copy change: run **both** `skate-stylist` *and* `frontend-designer`. They overlap on purpose.
For any push to `main`: run `security` first.

## Stack notes

- Pure HTML/CSS/JS. No build, no bundler, no framework unless we have a real reason.
- Leaflet + OSM tiles for the map (CDN-loaded with SRI + pinned version).
- Formspree for the submission form.
- Cloudflare Access in front of `/admin/` and any request that returns `private.json`.

## Styling note

Visual language is set by the assets in `assets/` (club logo + flyer references), not by `skate-stylist` or `frontend-designer` opinions in a vacuum. Before any visual work, confirm `assets/` is populated. Both agents push back hard on AI tells (gradients, soft shadows, glassmorphism, Inter, generic hero patterns) and on hype-skater clichés (neon-on-black, drip, Supreme cosplay).

## Voice & values

- **Inclusive by default.** Beginners welcome, women explicitly welcomed (Women in Skate is one of the club's biggest events), all wheels are welcome — rollerbladers included.
- **Don't make "all wheels" a title element on every page** and don't make inclusivity a marketing hook. Weave it through: one light mention in the about copy, one on the landing, photography that reflects it.
- **Copy voice**: a skater talking to a friend. No corporate DEI-speak. No "we welcome skaters of all backgrounds and abilities" boilerplate.
- **Photography**: the club has a photographer with hundreds of real photos. Allocate photo space throughout the site (landing, about, spots, member moments) — not a single gallery page. Real photos beat stock or AI imagery every time.
