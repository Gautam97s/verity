from typing import Dict, Any
from pydantic import BaseModel

class ReminderRequest(BaseModel):
    context: Dict[str, Any]

class ReminderResponse(BaseModel):
    message: str
