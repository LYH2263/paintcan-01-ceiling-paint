import pytest
from app.db import DB_PATH  # noqa: F401  (ensures app package importable)
import app.db as db
from app import seed
from app.engines.estimate import estimate_room
from app.services.paint_service import PaintService

OPS = [{"w": 0.9, "h": 2.1}, {"w": 1.5, "h": 1.4}]


@pytest.fixture()
def svc(tmp_path, monkeypatch):
    monkeypatch.setattr(db, "DB_PATH", tmp_path / "test.db")
    seed.init_db()
    with PaintService() as s:
        yield s


def _run_count(s):
    return s._c.execute("SELECT COUNT(*) c FROM calc_runs").fetchone()["c"]


def test_disabled_response_matches_base():
    e = estimate_room(5, 4, 2.8, OPS, 8, 2, ceiling_enabled=False)
    assert e == {"gross_m2": 50.4, "openings_m2": 3.99, "net_m2": 46.41,
                 "liters": 11.6, "coats": 2, "coverage": 8.0}
    assert "ceiling_enabled" not in e


def test_ceiling_area_and_independent_liters():
    e = estimate_room(5, 4, 2.8, OPS, 8, 2,
                      ceiling_enabled=True, ceiling_coverage=8, ceiling_coats=1)
    assert e["ceiling_m2"] == 20.0
    assert e["ceiling_liters"] == 2.5
    assert e["ceiling_coats"] == 1
    # wall side untouched
    assert e["liters"] == 11.6


def test_ceiling_own_coats():
    e = estimate_room(5, 4, 2.8, OPS, 8, 2,
                      ceiling_enabled=True, ceiling_coverage=10, ceiling_coats=2)
    assert e["ceiling_liters"] == 4.0  # 20 * 2 / 10


def test_bad_ceiling_inputs_rejected(svc):
    before = _run_count(svc)
    with pytest.raises(ValueError):
        svc.estimate(1, True, ceiling_enabled=True, ceiling_coverage=0, ceiling_coats=1)
    with pytest.raises(ValueError):
        svc.estimate(1, True, ceiling_enabled=True, ceiling_coverage=8, ceiling_coats=-2)
    # whole order refused: nothing written
    assert _run_count(svc) == before


def test_bad_wall_override_rejected(svc):
    before = _run_count(svc)
    with pytest.raises(ValueError):
        svc.estimate(1, True, coverage=-1)
    assert _run_count(svc) == before


def test_persist_false_writes_nothing(svc):
    before = _run_count(svc)
    r = svc.estimate(1, False, ceiling_enabled=True)
    assert r["run_id"] is None
    assert _run_count(svc) == before


def test_pinned_history_survives_stricter_default(svc):
    r = svc.estimate(1, True, ceiling_enabled=True)  # 20m2 @ 8 m2/L, 1 coat = 2.5L
    rid = r["run_id"]
    assert r["ceiling_liters"] == 2.5
    svc.update_settings(ceiling_coverage=4)  # stricter coverage rule
    d = svc.run_detail(rid)
    assert d["ceiling_enabled"] is True
    assert d["ceiling_liters"] == 2.5
    assert d["wall_liters"] == 11.6


def test_history_disabled_run(svc):
    r = svc.estimate(1, True)
    d = svc.run_detail(r["run_id"])
    assert d["ceiling_enabled"] is False
    assert d["wall_liters"] == 11.6
