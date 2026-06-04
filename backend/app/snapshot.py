"""Write a static snapshot of all public spots to the repo, for the map's
backend-down fallback. Output validates against spots/data/schema.json.

Run:  uv run python -m app.snapshot
"""
import json
from pathlib import Path

from sqlalchemy import select

from app.db import SessionLocal
from app.models import Spot
from app.schemas import SpotOut

# backend/app/snapshot.py -> repo root is three parents up.
REPO_ROOT = Path(__file__).resolve().parents[2]
OUT_FILE = REPO_ROOT / "spots" / "data" / "public-spots.json"

# Optional fields are omitted when empty so the snapshot matches the hand-edited
# schema.json shape (which drops absent recommended fields).
OPTIONAL = ("area", "bust", "surface", "size", "notes", "verified", "added", "submitted_by")


def _to_entry(spot: Spot) -> dict:
    out = SpotOut.from_spot(spot)
    entry = {
        "id": out.id,
        "name": out.name,
        "lat": round(out.lat, 6),
        "lng": round(out.lng, 6),
        "type": out.type,
    }
    for field in OPTIONAL:
        value = getattr(out, field)
        if value is not None:
            entry[field] = value.isoformat() if hasattr(value, "isoformat") else value
    if out.photos:
        entry["photos"] = out.photos
    return entry


def run() -> None:
    db = SessionLocal()
    try:
        spots = (
            db.execute(select(Spot).where(Spot.is_public.is_(True)).order_by(Spot.id))
            .scalars()
            .all()
        )
        entries = [_to_entry(s) for s in spots]
    finally:
        db.close()

    OUT_FILE.write_text(json.dumps(entries, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {len(entries)} public spots to {OUT_FILE}")


if __name__ == "__main__":
    run()
