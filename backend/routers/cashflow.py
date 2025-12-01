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
    total_outflow = metrics.get("total_outflow_last_3m", 0)
    net_balance = total_inflow - total_outflow

    return {
        "total_inflow": total_inflow,
        "total_outflow": total_outflow,
        "net_balance": net_balance
    }

@router.get("/history/{business_id}")
def get_cashflow_history(business_id: int, db: Session = Depends(get_session)):
    try:
        metrics = compute_business_metrics(db, business_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="Business not found")
    
    monthly_revenue = metrics.get("monthly_revenue", {})
    monthly_outflow = metrics.get("monthly_outflow", {})
    
    # Combine keys and sort
    all_keys = sorted(set(monthly_revenue.keys()) | set(monthly_outflow.keys()))
    
    history = []
    for key in all_keys:
        history.append({
            "month": key,
            "inflow": monthly_revenue.get(key, 0.0),
            "outflow": monthly_outflow.get(key, 0.0)
        })
        
    return history
