from fastapi import APIRouter
from schemas.reports import FinancialReportRequest, FinancialReportResponse
from agents.report_agent import generate_financial_report

router = APIRouter()

@router.post("/financial", response_model=FinancialReportResponse)
def generate_report(payload: FinancialReportRequest):
    result = generate_financial_report(payload.metrics)
    return {"report": result}
