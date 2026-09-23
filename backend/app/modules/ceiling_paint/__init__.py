"""ceiling_paint: ceiling area and paint liters with its own coverage/coats."""


def ceiling_area(length: float, width: float) -> float:
    return round(float(length) * float(width), 2)


def ceiling_liters(area_m2: float, coverage_m2_per_l: float, coats: int) -> dict:
    if coverage_m2_per_l <= 0 or coats <= 0:
        raise ValueError("ceiling coverage and coats must be positive")
    need = float(area_m2) * int(coats) / float(coverage_m2_per_l)
    return {
        "ceiling_m2": round(float(area_m2), 2),
        "ceiling_liters": round(need, 2),
        "ceiling_coats": int(coats),
        "ceiling_coverage": float(coverage_m2_per_l),
    }
