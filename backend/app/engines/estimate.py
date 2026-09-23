from app.engines.paint_volume import paint_liters
from app.engines.wall_area import wall_area
from app.modules.ceiling_paint import ceiling_area, ceiling_liters

def estimate_room(length, width, height, openings, coverage, coats,
                  ceiling_enabled=False, ceiling_coverage=None, ceiling_coats=None):
    area = wall_area(length, width, height, openings)
    vol = paint_liters(area["net_m2"], coverage, coats)
    result = {**area, **vol}
    if ceiling_enabled:
        result.update({"ceiling_enabled": True,
                       **ceiling_liters(ceiling_area(length, width), ceiling_coverage, ceiling_coats)})
    return result
