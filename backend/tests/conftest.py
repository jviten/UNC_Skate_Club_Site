"""Test harness: a dedicated `uncskate_test` DB on the same Docker Postgres.

The app builds its engine from settings at import time, so DATABASE_URL must be
set BEFORE any `app.*` import. We create the test DB if absent, run the real
alembic migration against it (PostGIS ext + GiST index + tables), and hand out a
TestClient. The DB is dropped on teardown.
"""
import os
from pathlib import Path

import pytest
import sqlalchemy as sa

BACKEND_DIR = Path(__file__).resolve().parent.parent

# Mirror the dev URL but target a separate database. Set BEFORE importing the app.
ADMIN_URL = "postgresql+psycopg://uncskate:uncskate@localhost:5433/uncskate"
TEST_DB = "uncskate_test"
TEST_URL = f"postgresql+psycopg://uncskate:uncskate@localhost:5433/{TEST_DB}"
os.environ["DATABASE_URL"] = TEST_URL


def _drop_and_create_test_db() -> None:
    admin = sa.create_engine(ADMIN_URL, isolation_level="AUTOCOMMIT")
    with admin.connect() as conn:
        conn.execute(
            sa.text(
                "SELECT pg_terminate_backend(pid) FROM pg_stat_activity "
                "WHERE datname = :db AND pid <> pg_backend_pid()"
            ),
            {"db": TEST_DB},
        )
        conn.execute(sa.text(f'DROP DATABASE IF EXISTS "{TEST_DB}"'))
        conn.execute(sa.text(f'CREATE DATABASE "{TEST_DB}"'))
    admin.dispose()


def _alembic_upgrade_head() -> None:
    from alembic import command
    from alembic.config import Config

    cfg = Config(str(BACKEND_DIR / "alembic.ini"))
    cfg.set_main_option("script_location", str(BACKEND_DIR / "migrations"))
    # env.py reads settings.database_url, which now points at the test DB.
    command.upgrade(cfg, "head")


@pytest.fixture(scope="session", autouse=True)
def _test_database():
    _drop_and_create_test_db()
    _alembic_upgrade_head()
    yield
    # Teardown: drop the whole test DB.
    from app.db import engine

    engine.dispose()
    admin = sa.create_engine(ADMIN_URL, isolation_level="AUTOCOMMIT")
    with admin.connect() as conn:
        conn.execute(
            sa.text(
                "SELECT pg_terminate_backend(pid) FROM pg_stat_activity "
                "WHERE datname = :db AND pid <> pg_backend_pid()"
            ),
            {"db": TEST_DB},
        )
        conn.execute(sa.text(f'DROP DATABASE IF EXISTS "{TEST_DB}"'))
    admin.dispose()


@pytest.fixture
def db_session(_test_database):
    """A clean spots table per test, plus a session to populate it."""
    from app.db import SessionLocal

    session = SessionLocal()
    session.execute(sa.text("TRUNCATE spots RESTART IDENTITY CASCADE"))
    session.commit()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def client(_test_database):
    from fastapi.testclient import TestClient

    from app.main import app

    return TestClient(app)


def make_point(lng: float, lat: float):
    """A geography POINT expression, matching how seed.py builds geom."""
    return sa.func.ST_SetSRID(sa.func.ST_MakePoint(lng, lat), 4326)
