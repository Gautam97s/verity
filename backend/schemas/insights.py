from typing import Dict, Any
from pydantic import BaseModel

class InsightGenerateRequest(BaseModel):
    metrics: Dict[str, Any]

class InsightGenerateResponse(BaseModel):
    insights: Dict[str, Any]
