from fastapi import APIRouter
from schemas.risk import RiskAnalysisRequest, RiskAnalysisResponse
from agents.risk_agent import analyze_risk_and_demand

router = APIRouter()

@router.post("/analyze", response_model=RiskAnalysisResponse)
def analyze_risk(payload: RiskAnalysisRequest):
    result = analyze_risk_and_demand(payload.history, payload.context)
    return {"risk_analysis": result}
