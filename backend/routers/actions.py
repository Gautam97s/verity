# backend/routers/actions.py
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlmodel import Session
from db import get_session
from agents import reminder_agent
from utils.whatsapp import send_whatsapp_message

router = APIRouter()

class SendReminderRequest(BaseModel):
    business_id: int
    customer_name: str
    customer_phone: str   # in E.164, e.g. +9198xxxxxxx
    invoice_number: str
    amount_due: float
    due_date: str         # ISO date string "2025-01-15"
    days_overdue: int | None = None
    preferred_tone: str = "friendly"
    preferred_language: str = "English/Hinglish"


class SendReminderResponse(BaseModel):
    message: str
    delivery: dict


@router.post("/send_whatsapp_reminder", response_model=SendReminderResponse)
def send_whatsapp_reminder(payload: SendReminderRequest, session: Session = Depends(get_session)):
    # 1. Build context for agent
    context = {
        "business_name": "Demo Business",  # in real code, fetch from DB using business_id
        "customer_name": payload.customer_name,
        "invoice_number": payload.invoice_number,
        "amount_due": payload.amount_due,
        "due_date": payload.due_date,
        "days_overdue": payload.days_overdue,
        "preferred_tone": payload.preferred_tone,
        "preferred_language": payload.preferred_language,
    }

    # 2. Call AI agent to generate message text
    print(f"[DEBUG] Calling reminder_agent for {payload.customer_name}")
    try:
        agent_result = reminder_agent.generate_payment_reminder(context)
        print(f"[DEBUG] reminder_agent returned: {agent_result}")
        message = agent_result.get("message")
        if not message:
            raise ValueError("Agent did not return 'message'")
    except Exception as e:
        print(f"[DEBUG] Error in reminder_agent: {e}")
        raise HTTPException(status_code=500, detail=f"Error generating reminder: {e}")

    # 3. Send via WhatsApp
    print(f"[DEBUG] Sending WhatsApp to {payload.customer_phone}")
    delivery = send_whatsapp_message(payload.customer_phone, message)
    print(f"[DEBUG] WhatsApp delivery result: {delivery}")

    return SendReminderResponse(message=message, delivery=delivery)
