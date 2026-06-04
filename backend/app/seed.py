"""Seed spots from seed_data.json. Idempotent upsert by id.

Run:  uv run python -m app.seed
Edit seed_data.json to add/change spots, then re-run.
"""
import json
from datetime import date
from pathlib import Path

from sqlalchemy import func

from app.db import SessionLocal
from app.models import Spot

SEED_FILE = Path(__file__).resolve().parent.parent / "seed_data.json"


def _parse_date(value: str | None) -> date | None:
    return date.fromisoformat(value) if value else None


def run() -> None:
    rows = json.loads(SEED_FILE.read_text(encoding="utf-8"))
    db = SessionLocal()
    try:
        for row in rows:
            point = func.ST_SetSRID(
                func.ST_MakePoint(row["lng"], row["lat"]), 4326
            )
            spot = db.get(Spot, row["id"])
            if spot is None:
                spot = Spot(id=row["id"])
                db.add(spot)
            spot.name = row["name"]
            spot.geom = point
            spot.type = row["type"]
            spot.area = row.get("area")
            spot.bust = row.get("bust")
            spot.surface = row.get("surface")
            spot.size = row.get("size")
            spot.notes = row.get("notes")
            spot.photos = row.get("photos", [])
            spot.verified = _parse_date(row.get("verified"))
            spot.added = _parse_date(row.get("added"))
            spot.submitted_by = row.get("submitted_by")
            # is_public left at its default (true) for seeded spots.
        db.commit()
        print(f"seeded {len(rows)} spots from {SEED_FILE.name}")
    finally:
        db.close()


if __name__ == "__main__":
    run()
