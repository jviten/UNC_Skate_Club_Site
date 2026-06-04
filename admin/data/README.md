# `admin/data/`

Private spot data lives here so it inherits the Cloudflare Access gate on `/admin/*`.

`private.json` follows the same schema as `spots/data/public.json` — see `spots/data/schema.md` and `spots/data/schema.json`.

## Do not

- Do not `fetch('admin/data/private.json')` from any page outside `/admin/`. Even a request that 401s leaks the URL's existence.
- Do not copy entries into `public.json` to "merge" the map for the admin view. Load both files at runtime in `admin/queue.js` and merge client-side.
- Do not commit photos for private spots into `assets/` if the photo itself reveals the location to anyone who finds the image. Host private-spot photos under `admin/photos/` so they share the same gate.

## Before any push to `main`

Run the `security` agent. Its single most important job is catching `private.json` leakage into anything served publicly.
