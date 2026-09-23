import json
from app.db import connect
from app.engines.estimate import estimate_room
from app.repositories import openings, rooms, runs, settings

class PaintService:
    def __init__(self): self._c = connect()
    def close(self): self._c.close()
    def __enter__(self): return self
    def __exit__(self, *a): self.close()
    def list_rooms(self): return rooms.list_all(self._c)
    def room_detail(self, rid):
        r = rooms.get(self._c, rid)
        if not r: return None
        return {"room": r, "openings": openings.for_room(self._c, rid)}
    def settings(self): return settings.get_map(self._c)
    def update_settings(self, **vals):
        for k, v in vals.items():
            if v is None: continue
            if v <= 0: raise ValueError(f"{k} must be positive")
            settings.upsert(self._c, k, v)
        return settings.get_map(self._c)
    def history(self, limit=50): return runs.list_recent(self._c, limit)
    def run_detail(self, run_id):
        row = runs.get(self._c, run_id)
        if not row: return None
        inp = json.loads(row["input_json"] or "{}")
        res = json.loads(row["result_json"] or "{}")
        enabled = bool(res.get("ceiling_enabled", inp.get("ceiling_enabled", False)))
        return {
            "id": row["id"], "kind": row["kind"], "room_id": row["room_id"],
            "created_at": row["created_at"], "input": inp, "result": res,
            "wall_liters": res.get("liters"),
            "ceiling_liters": res.get("ceiling_liters", 0.0),
            "ceiling_enabled": enabled,
        }
    def estimate(self, room_id, persist, coats=None, coverage=None,
                 ceiling_enabled=False, ceiling_coats=None, ceiling_coverage=None):
        detail = self.room_detail(room_id)
        if not detail: return None
        r = detail["room"]
        cov, ct = settings.coverage_coats(self._c)
        cov = float(coverage if coverage is not None else cov)
        ct = int(coats if coats is not None else ct)
        if cov <= 0 or ct <= 0:
            raise ValueError("coverage and coats must be positive")
        ceil_cov = ceil_ct = None
        if ceiling_enabled:
            ccov, cct = settings.ceiling_coverage_coats(self._c)
            ceil_cov = float(ceiling_coverage if ceiling_coverage is not None else ccov)
            ceil_ct = int(ceiling_coats if ceiling_coats is not None else cct)
            if ceil_cov <= 0 or ceil_ct <= 0:
                raise ValueError("ceiling coverage and coats must be positive")
        ops = [{"w": o["w"], "h": o["h"]} for o in detail["openings"]]
        result = estimate_room(r["length"], r["width"], r["height"], ops, cov, ct,
                               ceiling_enabled, ceil_cov, ceil_ct)
        payload = {"room_id": room_id, "coats": ct, "coverage": cov,
                   "ceiling_enabled": bool(ceiling_enabled)}
        if ceiling_enabled:
            payload.update({"ceiling_coats": ceil_ct, "ceiling_coverage": ceil_cov})
        rid = None
        if persist:
            # Pin the liters/enablement as of this run so later setting changes
            # cannot mutate history.
            pinned = {**result, "ceiling_enabled": bool(ceiling_enabled),
                      "ceiling_liters": result.get("ceiling_liters", 0.0)}
            rid = runs.insert(self._c, "estimate", payload, pinned, room_id)
        return {"run_id": rid, "room_id": room_id, **result}
    def dashboard(self):
        rs = rooms.list_all(self._c)
        return {"room_count": len(rs), "clean": len([x for x in rs if "种子" not in x["name"] and "多种" not in x["name"]]), "dirty": len([x for x in rs if "多种" in x["name"]])}
