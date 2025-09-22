from fastapi import APIRouter, Query, Depends
from sqlalchemy.orm import Session
from backend.schemas import GravitasStop
from backend.services.gravitas_service import GravitasService
from backend.database.database import get_session
from typing import List

router = APIRouter()
#service = GravitasService()

@router.get("/route", response_model=List[GravitasStop], summary="Get a Gravitas Food Route")
def get_gravitas_route(
    location: str = Query(..., example="Wellington"),
    cultures: str = Query(..., example="Middle Eastern, African"),
    db: Session = Depends(get_session)
):
    service = GravitasService()
    return service.generate_route(location, cultures, db)