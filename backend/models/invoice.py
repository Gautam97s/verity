from typing import Optional
from datetime import date
from sqlmodel import SQLModel, Field

class Invoice(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    business_id: int = Field(foreign_key="business.id")
    contact_id: Optional[int] = Field(default=None, foreign_key="contact.id")
    amount: float
    type: str # "receivable" | "payable"
    status: str = "pending"
    due_date: Optional[date] = None
    description: Optional[str] = None
