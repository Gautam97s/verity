from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session
from db import get_session
from schemas.pitchdeck import PitchdeckRequest, PitchdeckResponse, PitchdeckSlide
from agents.pitchdeck_agent import generate_pitchdeck_outline
from services.pitchdeck_service import create_pitchdeck

router = APIRouter()

@router.post("/generate", response_model=PitchdeckResponse)
def generate_pitchdeck_endpoint(payload: PitchdeckRequest, db: Session = Depends(get_session)):
    if payload.metrics:
        deck_data = generate_pitchdeck_outline(payload.metrics)
    elif payload.business_id:
        deck_data = create_pitchdeck(db, payload.business_id)
    else:
        raise HTTPException(status_code=400, detail="Either metrics or business_id is required")

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
