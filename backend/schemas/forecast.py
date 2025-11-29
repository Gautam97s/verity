from typing import Dict, Any, List
from pydantic import BaseModel

class ForecastExplainRequest(BaseModel):
    forecast_data: Dict[str, Any]

class ForecastExplainResponse(BaseModel):
    summary: str
    recommendations: List[str]
