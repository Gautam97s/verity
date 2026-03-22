from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field

class Business(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    username: Optional[str] = Field(default=None, unique=True, index=True)
    hashed_password: Optional[str] = Field(default=None)
    owner_name: Optional[str] = None
    industry: Optional[str] = None
    location: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
