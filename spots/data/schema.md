# Spot data schema

The spot map is fed by two JSON files. Both share the same schema (`schema.json`) — the file path is what determines whether a spot is public or private.

| File | Served to | Edit workflow |
|---|---|---|
| `spots/data/public.json` | Everyone | Exec edits directly, commits to `main` |
| `admin/data/private.json` | Execs only (Cloudflare Access on `/admin/*`) | Same, but stays gated |

## Why `private.json` lives under `admin/`, not `spots/data/`

GitHub Pages serves every file in the repo at its path with no access control. Cloudflare Access only gates URL paths it's configured for — in our case, `/admin/*`. If `private.json` lived at `/spots/data/private.json`, anyone who guessed the URL could fetch it directly, regardless of what HTML page tried to load it.

Co-locating private data with the admin app under `/admin/data/private.json` means it actually inherits the Access gate. The `spots/index.html` map page never loads `private.json`. The `admin/index.html` map page loads both `public.json` and `private.json` and merges them in the browser.

This is a deviation from the path written in `CLAUDE.md` and `TODO.md`. Treat this file as the canonical location — those references should be updated when v3 admin work starts.

## Fields

See `schema.json` for the formal definition. Quick reference:

**Required**
- `id` — kebab-case slug, unique across both files. Stable across edits.
- `name` — human-readable.
- `lat`, `lng` — decimal degrees.
- `type` — one of `ledge`, `stairs`, `rail`, `transition`, `flat`, `DIY`.

**Recommended**
- `area` — `Chapel Hill` | `Carrboro` | `other`.
- `bust` — `chill` | `caution` | `hot`. Filter dimension per TODO.md.
- `surface` — `concrete` | `asphalt` | `marble` | `brick` | `wood` | `metal` | `other`.
- `size` — free-form, e.g. `"3-stair"`, `"knee-high ledge"`.
- `notes` — plain text, ≤500 chars. **Must be escaped in popups** — see security.
- `photos` — array of relative repo paths (`assets/spots/...`) or `https://` URLs.
- `verified` — ISO date, last exec confirmation.
- `added` — ISO date, first entry.
- `submitted_by` — optional contributor credit.

## Example entry

```json
{
  "id": "oec-griptape",
  "name": "OEC griptape ledge",
  "lat": 35.9132,
  "lng": -79.0558,
  "type": "ledge",
  "area": "Chapel Hill",
  "bust": "chill",
  "surface": "concrete",
  "size": "knee-high, ~12 ft run",
  "notes": "Concrete ledge wrapped in skate-spot griptape, club-installed. Free skating, weekends are best.",
  "photos": ["assets/flyers/skate-spot-oec-griptape.png"],
  "verified": "2026-05-20",
  "added": "2026-05-20"
}
```

*(Coordinates above are placeholder — replace with a real GPS pin before publishing.)*

## Security notes (relevant to map.js / submit.html implementers)

1. **Popup HTML.** Leaflet's `.bindPopup()` takes HTML and does not escape. `notes`, `name`, `size`, and `submitted_by` are strings that originate from human input (exec-edited, or Formspree submissions reviewed by exec). Pass them through `textContent` or an escape helper before injecting. Never `innerHTML` raw strings.
2. **Photo URLs.** `photos[i]` is either a relative path under `assets/` or an `https://` URL. Reject `javascript:`, `data:`, and protocol-relative URLs at render time even though the form will pre-filter.
3. **`private.json` must never be referenced from `spots/index.html` or any page outside `/admin/`.** Even a `fetch()` call that 401s is a leak (the URL existence confirms private data). The `security` agent runs before any push to `main` specifically to catch this.
4. **No PII in `public.json`.** `submitted_by` is opt-in and exec-reviewed. Don't store emails, full names, or location-revealing metadata.

## Adding a spot (v1 workflow, exec-only)

1. Open `spots/data/public.json`.
2. Append an object matching the schema.
3. `id` must be kebab-case and unique. Convention: short, descriptive — `franklin-st-banks`, `weaver-st-flat`, etc.
4. Validate with `python -m json.tool spots/data/public.json` (or any JSON linter) — the array must stay parseable.
5. Commit. GitHub Pages picks it up on next deploy.

Submission form workflow (v2) and admin moderation queue (v3) come later — see `TODO.md`.
