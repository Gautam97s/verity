from typing import Dict, Any
from pydantic import BaseModel

class FinancialReportRequest(BaseModel):
    metrics: Dict[str, Any]

class FinancialReportResponse(BaseModel):
    report: Dict[str, Any]
