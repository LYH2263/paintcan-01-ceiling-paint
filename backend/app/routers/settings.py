from fastapi import APIRouter, HTTPException
from app.schemas.settings import SettingsRequest
from app.services.paint_service import PaintService
router = APIRouter()
@router.get("/settings")
def settings():
    with PaintService() as s: return s.settings()
@router.post("/settings")
def update_settings(body: SettingsRequest):
    with PaintService() as s:
        try:
            return s.update_settings(
                coverage=body.coverage, coats=body.coats,
                ceiling_coverage=body.ceiling_coverage, ceiling_coats=body.ceiling_coats)
        except ValueError as e:
            raise HTTPException(400, str(e))
