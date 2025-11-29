from typing import List, Dict, Any
from pydantic import BaseModel

class RiskAnalysisRequest(BaseModel):
    history: List[Dict[str, Any]]
    context: Dict[str, Any]

class RiskAnalysisResponse(BaseModel):
    risk_analysis: Dict[str, Any]
