from typing import Optional
from sqlmodel import SQLModel, Field

class Contact(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    business_id: int
    name: str
    type: str = Field(default="customer") # "customer" | "supplier"
    phone: Optional[str] = None
