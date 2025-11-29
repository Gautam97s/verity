from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field

class RawEvent(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    business_id: int
    source: str
    raw_text: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
