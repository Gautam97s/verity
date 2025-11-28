from pydantic import BaseModel

class WhatsAppIn(BaseModel):
    business_id: int
    raw_text: str
