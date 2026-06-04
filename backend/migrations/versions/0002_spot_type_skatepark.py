"""add 'skatepark' to spot_type

Revision ID: 0002_spot_type_skatepark
Revises: 0001_initial
Create Date: 2026-06-04

Background: spot_type is declared native_enum=False (app/models.py). Under
SQLAlchemy 2.0 that maps to a plain VARCHAR with create_constraint=False, so
0001 emitted NO CHECK constraint — spots.type is an unconstrained VARCHAR(10).
This migration adds the value-set CHECK the schema intends, now including the
7th value 'skatepark'. upgrade() creates the constraint (7 values); downgrade()
drops it, restoring the true pre-0002 state (no constraint).
"""
from alembic import op

revision = "0002_spot_type_skatepark"
down_revision = "0001_initial"
branch_labels = None
depends_on = None

CONSTRAINT = "ck_spots_type"
SPOT_TYPE_7 = ("ledge", "stairs", "rail", "transition", "flat", "DIY", "skatepark")


def _in_list(values) -> str:
    return ", ".join(f"'{v}'" for v in values)


def upgrade() -> None:
    op.create_check_constraint(
        CONSTRAINT, "spots", f"type IN ({_in_list(SPOT_TYPE_7)})"
    )


def downgrade() -> None:
    op.drop_constraint(CONSTRAINT, "spots", type_="check")
