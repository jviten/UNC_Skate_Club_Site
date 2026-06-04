from datetime import date

from geoalchemy2.shape import to_shape
from pydantic import BaseModel

from app.models import Spot


class SpotOut(BaseModel):
    id: str
    name: str
    lat: float
    lng: float
    type: str
    area: str | None = None
    bust: str | None = None
    surface: str | None = None
    size: str | None = None
    notes: str | None = None
    photos: list[str] = []
    verified: date | None = None
    added: date | None = None
    submitted_by: str | None = None

    @classmethod
    def from_spot(cls, spot: Spot) -> "SpotOut":
        point = to_shape(spot.geom)  # shapely Point (x=lng, y=lat)
        return cls(
            id=spot.id,
            name=spot.name,
            lat=point.y,
            lng=point.x,
            type=spot.type,
            area=spot.area,
            bust=spot.bust,
            surface=spot.surface,
            size=spot.size,
            notes=spot.notes,
            photos=spot.photos or [],
            verified=spot.verified,
            added=spot.added,
            submitted_by=spot.submitted_by,
        )
