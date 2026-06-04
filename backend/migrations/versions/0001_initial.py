"""initial schema: spots + videos + postgis

Revision ID: 0001_initial
Revises:
Create Date: 2026-06-04
"""
from alembic import op
import sqlalchemy as sa
from geoalchemy2 import Geography

revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None

SPOT_TYPE = ("ledge", "stairs", "rail", "transition", "flat", "DIY")
SPOT_AREA = ("Chapel Hill", "Carrboro", "other")
SPOT_BUST = ("chill", "caution", "hot")
SPOT_SURFACE = ("concrete", "asphalt", "marble", "brick", "wood", "metal", "other")
VIDEO_PROVIDER = ("youtube", "vimeo")


def _enum(name, values):
    # native_enum=False => emitted as a CHECK constraint, no Postgres ENUM type
    # to create/drop separately.
    return sa.Enum(*values, name=name, native_enum=False)


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS postgis")

    op.create_table(
        "spots",
        sa.Column("id", sa.String(length=60), primary_key=True),
        sa.Column("name", sa.String(length=80), nullable=False),
        sa.Column(
            "geom",
            Geography(geometry_type="POINT", srid=4326, spatial_index=False),
            nullable=False,
        ),
        sa.Column("type", _enum("spot_type", SPOT_TYPE), nullable=False),
        sa.Column("area", _enum("spot_area", SPOT_AREA), nullable=True),
        sa.Column("bust", _enum("spot_bust", SPOT_BUST), nullable=True),
        sa.Column("surface", _enum("spot_surface", SPOT_SURFACE), nullable=True),
        sa.Column("size", sa.String(length=80), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("photos", sa.dialects.postgresql.JSONB(), nullable=False),
        sa.Column("verified", sa.Date(), nullable=True),
        sa.Column("added", sa.Date(), nullable=True),
        sa.Column("submitted_by", sa.String(length=60), nullable=True),
        sa.Column(
            "is_public",
            sa.Boolean(),
            nullable=False,
            server_default=sa.true(),
        ),
    )
    # GiST index for fast viewport/bbox queries. GeoAlchemy2 normally autocreates
    # a spatial index; we create it explicitly here so the migration is the
    # single source of truth.
    op.create_index(
        "ix_spots_geom",
        "spots",
        ["geom"],
        postgresql_using="gist",
    )

    op.create_table(
        "videos",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column(
            "provider", _enum("video_provider", VIDEO_PROVIDER), nullable=False
        ),
        sa.Column("video_id", sa.String(length=64), nullable=False),
        sa.Column("caption", sa.String(length=200), nullable=True),
        sa.Column(
            "spot_id",
            sa.String(length=60),
            sa.ForeignKey("spots.id", ondelete="CASCADE"),
            nullable=False,
        ),
    )


def downgrade() -> None:
    op.drop_table("videos")
    op.drop_index("ix_spots_geom", table_name="spots")
    op.drop_table("spots")
    # postgis extension intentionally left installed.
