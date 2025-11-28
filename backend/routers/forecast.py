from fastapi import APIRouter
from schemas.forecast import ForecastExplainRequest, ForecastExplainResponse
from agents.forecast_agent import explain_forecast

router = APIRouter()

@router.post("/explain", response_model=ForecastExplainResponse)
def explain_forecast_endpoint(payload: ForecastExplainRequest):
    result = explain_forecast(payload.forecast_data)
    return result
