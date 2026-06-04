"""Smoke + invariant tests for the spot-map API.

The #1 invariant under test: private spots (is_public=False) must NEVER appear
in any response or in the public snapshot.
"""
import json
from pathlib import Path

import jsonschema
import sqlalchemy as sa

from conftest import make_point

REPO_ROOT = Path(__file__).resolve().parents[2]
SCHEMA = json.loads((REPO_ROOT / "spots" / "data" / "schema.json").read_text("utf-8"))


def _insert_spot(session, *, id, name, lng, lat, type="ledge", is_public=True):
    from app.models import Spot

    spot = Spot(
        id=id, name=name, type=type, photos=[], is_public=is_public,
        geom=make_point(lng, lat),
    )
    session.add(spot)
    session.commit()


def test_health(client):
    r = client.get("/api/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_list_returns_public_only(db_session, client):
    _insert_spot(db_session, id="pub", name="Public", lng=-79.05, lat=35.91)
    _insert_spot(db_session, id="priv", name="Private", lng=-79.05, lat=35.91,
                 is_public=False)

    r = client.get("/api/spots")
    assert r.status_code == 200
    ids = [s["id"] for s in r.json()]
    assert ids == ["pub"]


def test_bbox_filter(db_session, client):
    # Inside the Chapel Hill box.
    _insert_spot(db_session, id="inside", name="Inside", lng=-79.055, lat=35.912)
    # Far away (Los Angeles) — outside.
    _insert_spot(db_session, id="outside", name="Outside", lng=-118.24, lat=34.05)

    r = client.get("/api/spots", params={"bbox": "-79.10,35.90,-79.04,35.92"})
    assert r.status_code == 200
    ids = [s["id"] for s in r.json()]
    assert ids == ["inside"]


def test_bbox_bad_input(client):
    # Malformed (non-numeric) -> 400.
    assert client.get("/api/spots", params={"bbox": "abc"}).status_code == 400
    # Out-of-range coords -> 400.
    assert client.get(
        "/api/spots", params={"bbox": "999,999,999,999"}
    ).status_code == 400


def test_get_spot(db_session, client):
    _insert_spot(db_session, id="known", name="Known", lng=-79.05, lat=35.91)
    _insert_spot(db_session, id="secret", name="Secret", lng=-79.05, lat=35.91,
                 is_public=False)

    r = client.get("/api/spots/known")
    assert r.status_code == 200
    body = r.json()
    assert body["id"] == "known"
    assert body["name"] == "Known"
    assert body["lat"] == 35.91 and body["lng"] == -79.05

    # Unknown id -> 404.
    assert client.get("/api/spots/does-not-exist").status_code == 404
    # Private id -> 404 (must not leak existence).
    assert client.get("/api/spots/secret").status_code == 404


def test_seed_idempotent(db_session):
    from app import seed

    seed.run()
    count1 = db_session.execute(sa.text("SELECT count(*) FROM spots")).scalar()
    seed.run()
    count2 = db_session.execute(sa.text("SELECT count(*) FROM spots")).scalar()
    assert count1 == count2
    assert count1 > 0


def test_snapshot_conforms_to_schema(db_session, tmp_path, monkeypatch):
    from app import snapshot

    _insert_spot(db_session, id="pub-snap", name="Public Snap",
                 lng=-79.05, lat=35.91)
    _insert_spot(db_session, id="priv-snap", name="Private Snap",
                 lng=-79.05, lat=35.91, is_public=False)

    # Redirect output so we never clobber the authoritative repo snapshot.
    out = tmp_path / "public-spots.json"
    monkeypatch.setattr(snapshot, "OUT_FILE", out)
    snapshot.run()

    entries = json.loads(out.read_text("utf-8"))
    jsonschema.validate(entries, SCHEMA)

    ids = [e["id"] for e in entries]
    assert "pub-snap" in ids
    assert "priv-snap" not in ids
