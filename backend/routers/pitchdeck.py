from fastapi import APIRouter, HTTPException
from schemas.pitchdeck import PitchdeckRequest, PitchdeckResponse, PitchdeckSlide
from agents.pitchdeck_agent import generate_pitchdeck_outline

router = APIRouter()

@router.post("/generate", response_model=PitchdeckResponse)
def generate_pitchdeck(payload: PitchdeckRequest):
    # If metrics are provided directly, use them. 
    # If business_id is provided, we might need to fetch metrics (logic from previous implementation).
    # For now, user said "pass metrics".
    
    if not payload.metrics:
         raise HTTPException(status_code=400, detail="Metrics are required")

    deck_data = generate_pitchdeck_outline(payload.metrics)

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
