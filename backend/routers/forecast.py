from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from db import get_session
from schemas.forecast import ForecastExplainRequest, ForecastExplainResponse
from agents.forecast_agent import explain_forecast
from services.pitchdeck_service import compute_business_metrics

router = APIRouter()

@router.post("/explain", response_model=ForecastExplainResponse)
def explain_forecast_endpoint(payload: ForecastExplainRequest):
    result = explain_forecast(payload.forecast_data)
    return result

@router.get("/{business_id}")
def get_business_forecast(business_id: int, db: Session = Depends(get_session)):
    try:
        metrics = compute_business_metrics(db, business_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="Business not found")
    
    # Construct forecast data from metrics for the agent
    forecast_data = {
        "cashflow_summary": metrics.get("monthly_revenue", {}),
        "total_inflow": metrics.get("total_inflow_last_3m", 0),
        "growth": metrics.get("revenue_growth_percent", 0)
    }
    
    result = explain_forecast(forecast_data)
    return result
