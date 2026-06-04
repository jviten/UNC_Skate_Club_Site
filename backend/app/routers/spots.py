from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.db import SessionLocal
from app.models import Spot
from app.schemas import SpotOut

router = APIRouter(prefix="/api", tags=["spots"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/spots", response_model=list[SpotOut])
def list_spots(
    bbox: str | None = Query(
        None, description="Viewport bounds as 'west,south,east,north' (lng/lat degrees)."
    ),
    db: Session = Depends(get_db),
):
    stmt = select(Spot).where(Spot.is_public.is_(True))
    if bbox is not None:
        try:
            west, south, east, north = (float(v) for v in bbox.split(","))
        except ValueError:
            raise HTTPException(
                status_code=400, detail="bbox must be 'west,south,east,north' floats"
            )
        # Reject out-of-range, NaN, and infinite coords (the range comparison
        # also rejects nan/inf, which never satisfy it) before they hit PostGIS.
        if not (
            -180 <= west <= 180
            and -180 <= east <= 180
            and -90 <= south <= 90
            and -90 <= north <= 90
        ):
            raise HTTPException(status_code=400, detail="bbox coords out of range")
        envelope = func.ST_MakeEnvelope(west, south, east, north, 4326)
        stmt = stmt.where(func.ST_Intersects(Spot.geom, envelope))
    spots = db.execute(stmt).scalars().all()
    return [SpotOut.from_spot(s) for s in spots]


@router.get("/spots/{spot_id}", response_model=SpotOut)
def get_spot(spot_id: str, db: Session = Depends(get_db)):
    stmt = select(Spot).where(Spot.id == spot_id, Spot.is_public.is_(True))
    spot = db.execute(stmt).scalar_one_or_none()
    if spot is None:
        raise HTTPException(status_code=404, detail="spot not found")
    return SpotOut.from_spot(spot)
