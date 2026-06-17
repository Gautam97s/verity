from typing import List, Dict, Any
from pydantic import BaseModel

class InsightGenerateRequest(BaseModel):
    metrics: Dict[str, Any]

class InsightGenerateResponse(BaseModel):
    insights: List[Dict[str, Any]]
