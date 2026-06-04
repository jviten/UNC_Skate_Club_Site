# UNC Skate Club — spot map backend

FastAPI + Postgres/PostGIS read-only API for the public spot map, plus a seed
script (founder's v1 "add a spot" path) and a static snapshot writer (the
backend-down fallback the public map reads).

This lives in `backend/` so Python source stays out of the GitHub-Pages-served
tree. The static site (`index.html`, `spots/`, `assets/`, …) is untouched.

## Prerequisites (Windows / PowerShell)

- [uv](https://docs.astral.sh/uv/) — `winget install astral-sh.uv` (or see uv docs)
- Docker Desktop (for the local PostGIS container)

## First-time setup

```powershell
# from backend\
Copy-Item .env.example .env      # defaults match docker-compose; edit if needed
uv sync                          # installs deps into .venv from pyproject + uv.lock
docker compose up -d             # starts postgis/postgis:16-3.4 on localhost:5432
uv run alembic upgrade head      # creates postgis ext, spots + videos, GiST index
uv run python -m app.seed        # loads seed_data.json (idempotent upsert by id)
uv run python -m app.snapshot    # writes ../spots/data/public-spots.json
```

## Run the API

```powershell
uv run uvicorn app.main:app --reload --port 8000
```

Then:
- Health: http://localhost:8000/api/health  → `{"status":"ok"}`
- All public spots: http://localhost:8000/api/spots
- Viewport query: http://localhost:8000/api/spots?bbox=-79.10,35.90,-79.04,35.92
- One spot: http://localhost:8000/api/spots/oec-griptape
- Docs: http://localhost:8000/docs

## Adding / editing spots (v1 founder workflow)

1. Edit `seed_data.json` — append an object. `id` is a kebab-case slug, unique
   and stable. `lat`/`lng` are decimal degrees (Chapel Hill / Carrboro ≈ 35.91,
   -79.05). `type` is one of: ledge, stairs, rail, transition, flat, DIY.
   Photos are in-repo relative paths under `assets/` (e.g.
   `assets/flyers/skate-spot-oec-griptape.png`).
2. `uv run python -m app.seed` — upserts by `id` (safe to re-run).
3. `uv run python -m app.snapshot` — regenerates `../spots/data/public-spots.json`.
4. Commit the updated `public-spots.json` (and `seed_data.json`).

> The current `seed_data.json` coords are **placeholders** (~35.91, -79.05).
> Replace them with real GPS pins before publishing.

## Migrations

```powershell
uv run alembic upgrade head      # apply
uv run alembic downgrade base    # roll back (round-trips; leaves postgis ext)
```

## Tests

```powershell
uv run pytest                    # runs tests/ against a dedicated uncskate_test DB
```

The suite uses its own `uncskate_test` database on the same Docker Postgres
(created/migrated/dropped per session by `tests/conftest.py`), so it never
touches dev data or the committed `public-spots.json`. Requires the Docker DB to
be up (`docker compose up -d`). Covers the health check, the public-only list
invariant, bbox filtering + range guard, single-spot 404s (including private
spots returning 404), seed idempotency, and snapshot/schema conformance.

## Notes

- `geom` (PostGIS `geography(Point,4326)`) is the source of truth for location.
  The API and snapshot derive `lat`/`lng` from it.
- `is_public` (default true) is forward-compat for v2/v3 private spots. The API
  and snapshot only ever return `is_public = true` rows.
- The `videos` table exists (model + migration) but nothing reads or serves it
  in v1.
- CORS is GET-only, scoped to `CORS_ORIGINS` in `.env`. The `https://uncskate.club`
  entry is a placeholder until the domain/Pages origin is finalized.
