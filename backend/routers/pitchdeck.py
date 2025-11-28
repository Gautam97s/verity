# backend/routers/pitchdeck.py
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from db import get_session
from schemas.pitchdeck import PitchdeckRequest, PitchdeckResponse, PitchdeckSlide
from services.pitchdeck_service import create_pitchdeck

router = APIRouter()


@router.post("/generate", response_model=PitchdeckResponse)
def generate_pitchdeck(payload: PitchdeckRequest, session: Session = Depends(get_session)):
    try:
        deck_data = create_pitchdeck(session, payload.business_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    # shape into Pydantic model
    slides = [
        PitchdeckSlide(title=s["title"], bullets=s.get("bullets", []))
        for s in deck_data.get("slides", [])
    ]
    response = PitchdeckResponse(
        title=deck_data.get("title", "Business Pitchdeck"),
        subtitle=deck_data.get("subtitle"),
        slides=slides,
    )
    return response
