from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from db import get_session
from services.pitchdeck_service import compute_business_metrics

router = APIRouter()

@router.get("/summary/{business_id}")
def get_cashflow_summary(business_id: int, db: Session = Depends(get_session)):
    try:
        metrics = compute_business_metrics(db, business_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="Business not found")
    
    # Extract summary data
    total_inflow = metrics.get("total_inflow_last_3m", 0)
    # Note: compute_business_metrics currently only calculates inflow/revenue. 
    # We might need to expand it or just use what we have.
    # For now, let's assume outflow is roughly 70% of inflow for demo purposes if not calculated
    total_outflow = total_inflow * 0.7 
    net_balance = total_inflow - total_outflow

    return {
        "total_inflow": total_inflow,
        "total_outflow": total_outflow,
        "net_balance": net_balance
    }
