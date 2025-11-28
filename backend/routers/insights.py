from fastapi import APIRouter
from schemas.insights import InsightGenerateRequest, InsightGenerateResponse
from agents.insight_agent import generate_insights

router = APIRouter()

@router.post("/generate", response_model=InsightGenerateResponse)
def generate_insights_endpoint(payload: InsightGenerateRequest):
    result = generate_insights(payload.metrics)
    return {"insights": result.get("insights", [])}
