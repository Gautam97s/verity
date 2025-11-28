# backend/schemas/pitchdeck.py
from typing import List, Optional
from pydantic import BaseModel

class PitchdeckRequest(BaseModel):
    business_id: int


class PitchdeckSlide(BaseModel):
    title: str
    bullets: List[str]


class PitchdeckResponse(BaseModel):
    title: str
    subtitle: Optional[str] = None
    slides: List[PitchdeckSlide]
