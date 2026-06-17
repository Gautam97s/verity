# backend/services/pitchdeck_service.py
from typing import Dict
from datetime import datetime
from sqlmodel import Session, select
from models.business import Business
from models.transaction import Transaction
from models.invoice import Invoice
from agents.pitchdeck_agent import generate_pitchdeck_outline


def compute_business_metrics(session: Session, business_id: int) -> Dict:
    # Basic business info
    business = session.get(Business, business_id)
    if not business:
        raise ValueError("Business not found")

    now = datetime.utcnow()
    # last 3 full months metrics (simple)
    month = now.month
    year = now.year

    def month_key(y, m):
        return f"{y}-{m:02d}"

    monthly_revenue = {}
    total_inflow_last_3m = 0.0
    total_outflow_last_3m = 0.0

    # grab all tx for last ~100 days
    stmt = select(Transaction).where(Transaction.business_id == business_id)
    txs = session.exec(stmt).all()

    for t in txs:
        key = month_key(t.date.year, t.date.month)
        if t.direction == "inflow":
            monthly_revenue[key] = monthly_revenue.get(key, 0.0) + t.amount
        elif t.direction == "outflow":
            # For simplicity, we just aggregate the outflow without storing monthly breakdown in metrics
            # Or we can just calculate total outflow last 3 months by adding to total directly
            if key in last_keys or len(monthly_revenue) == 0:
                pass # Need to check if it's in the last 3 months

    # A better way to calculate total inflow/outflow last 3 months
    last_keys = sorted(list(set(month_key(t.date.year, t.date.month) for t in txs)))[-3:]
    for t in txs:
        if month_key(t.date.year, t.date.month) in last_keys:
            if t.direction == "inflow":
                total_inflow_last_3m += t.amount
            elif t.direction == "outflow":
                total_outflow_last_3m += t.amount

    # very rough growth calculation: last month vs previous month
    revenue_growth_percent = None
    if len(last_keys) >= 2:
        last = monthly_revenue[last_keys[-1]]
        prev = monthly_revenue[last_keys[-2]]
        if prev > 0:
            revenue_growth_percent = (last - prev) / prev * 100

    # overdue invoices
    stmt_inv = select(Invoice).where(
        Invoice.business_id == business_id,
        Invoice.status == "overdue",
    )
    overdue_invoices = session.exec(stmt_inv).all()
    overdue_amount = sum(i.amount for i in overdue_invoices)

    metrics = {
        "business_id": business.id,
        "business_name": business.name,
        "industry": getattr(business, "industry", None),
        "location": getattr(business, "location", None),
        "monthly_revenue": monthly_revenue,
        "total_inflow_last_3m": total_inflow_last_3m,
        "total_outflow_last_3m": total_outflow_last_3m,
        "revenue_growth_percent": revenue_growth_percent,
        "overdue_amount": overdue_amount,
        # Extend later with: top customers, margins, etc.
    }
    return metrics


def create_pitchdeck(session: Session, business_id: int) -> Dict:
    metrics = compute_business_metrics(session, business_id)
    deck = generate_pitchdeck_outline(metrics)
    return deck
