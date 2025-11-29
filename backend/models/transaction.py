from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field

class Transaction(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    business_id: int
    invoice_id: Optional[int] = None
    direction: str # "inflow" | "outflow"
    amount: float
    method: str = "other"
    category: str = "other"
    date: datetime = Field(default_factory=datetime.utcnow)
    raw_text: Optional[str] = None
    source: str = "manual"
