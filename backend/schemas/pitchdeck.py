from typing import List, Optional, Dict, Any
from pydantic import BaseModel

class PitchdeckRequest(BaseModel):
    metrics: Optional[Dict[str, Any]] = None
    business_id: Optional[int] = None

class PitchdeckSlide(BaseModel):
    title: str
    bullets: List[str]

class PitchdeckResponse(BaseModel):
    title: str
    subtitle: Optional[str] = None
    slides: List[PitchdeckSlide]

