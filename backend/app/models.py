from datetime import date

from geoalchemy2 import Geography
from sqlalchemy import Boolean, Date, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import ENUM, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base

# Enums mirror spots/data/schema.json exactly. native_enum=False keeps them as
# DB CHECK constraints (simpler to evolve than a Postgres ENUM type).
spot_type = ENUM(
    "ledge", "stairs", "rail", "transition", "flat", "DIY", "skatepark",
    name="spot_type", create_type=False, native_enum=False,
)
spot_area = ENUM(
    "Chapel Hill", "Carrboro", "other",
    name="spot_area", create_type=False, native_enum=False,
)
spot_bust = ENUM(
    "chill", "caution", "hot",
    name="spot_bust", create_type=False, native_enum=False,
)
spot_surface = ENUM(
    "concrete", "asphalt", "marble", "brick", "wood", "metal", "other",
    name="spot_surface", create_type=False, native_enum=False,
)
video_provider = ENUM(
    "youtube", "vimeo",
    name="video_provider", create_type=False, native_enum=False,
)


class Spot(Base):
    __tablename__ = "spots"

    # id is a kebab-case slug (schema.json pattern ^[a-z0-9][a-z0-9-]*$).
    id: Mapped[str] = mapped_column(String(60), primary_key=True)
    name: Mapped[str] = mapped_column(String(80), nullable=False)
    # geom is the source of truth for location; lat/lng are derived from it.
    geom: Mapped[object] = mapped_column(
        Geography(geometry_type="POINT", srid=4326), nullable=False
    )
    type: Mapped[str] = mapped_column(spot_type, nullable=False)
    area: Mapped[str | None] = mapped_column(spot_area)
    bust: Mapped[str | None] = mapped_column(spot_bust)
    surface: Mapped[str | None] = mapped_column(spot_surface)
    size: Mapped[str | None] = mapped_column(String(80))
    notes: Mapped[str | None] = mapped_column(Text)
    photos: Mapped[list[str]] = mapped_column(JSONB, nullable=False, default=list)
    verified: Mapped[date | None] = mapped_column(Date)
    added: Mapped[date | None] = mapped_column(Date)
    submitted_by: Mapped[str | None] = mapped_column(String(60))
    # Forward-compat for v2/v3 private spots. Default true = public.
    is_public: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    videos: Mapped[list["Video"]] = relationship(
        back_populates="spot", cascade="all, delete-orphan"
    )


class Video(Base):
    # Model + migration only. NOTHING reads/renders/serves this in v1.
    __tablename__ = "videos"

    id: Mapped[int] = mapped_column(primary_key=True)
    provider: Mapped[str] = mapped_column(video_provider, nullable=False)
    video_id: Mapped[str] = mapped_column(String(64), nullable=False)
    caption: Mapped[str | None] = mapped_column(String(200))
    spot_id: Mapped[str] = mapped_column(
        ForeignKey("spots.id", ondelete="CASCADE"), nullable=False
    )

    spot: Mapped["Spot"] = relationship(back_populates="videos")
