from pydantic import BaseModel
class EstimateRequest(BaseModel):
    room_id: int
    coats: int | None = None
    coverage: float | None = None
    persist: bool = True
    ceiling_enabled: bool = False
    ceiling_coats: int | None = None
    ceiling_coverage: float | None = None
