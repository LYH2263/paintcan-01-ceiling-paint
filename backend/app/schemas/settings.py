from pydantic import BaseModel
class SettingsRequest(BaseModel):
    coverage: float | None = None
    coats: int | None = None
    ceiling_coverage: float | None = None
    ceiling_coats: int | None = None
