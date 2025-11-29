from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from db import get_session
from schemas.insights import InsightGenerateRequest, InsightGenerateResponse
from agents.insight_agent import generate_insights
from services.pitchdeck_service import compute_business_metrics # Reusing metrics logic

router = APIRouter()

@router.post("/generate", response_model=InsightGenerateResponse)
def generate_insights_endpoint(payload: InsightGenerateRequest):
    result = generate_insights(payload.metrics)
    return {"insights": result.get("insights", [])}

@router.get("/{business_id}")
def get_business_insights(business_id: int, db: Session = Depends(get_session)):
    # 1. Compute metrics
    try:
        metrics = compute_business_metrics(db, business_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="Business not found")
    
    # 2. Generate insights on the fly (or fetch from DB if we were storing them)
    # For now, we generate fresh insights
    result = generate_insights(metrics)
    return {"insights": result.get("insights", [])}
