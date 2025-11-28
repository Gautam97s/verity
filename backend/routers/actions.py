from fastapi import APIRouter
from schemas.actions import ReminderRequest, ReminderResponse
from agents.reminder_agent import generate_payment_reminder

router = APIRouter()

@router.post("/reminder", response_model=ReminderResponse)
def generate_reminder(payload: ReminderRequest):
    result = generate_payment_reminder(payload.context)
    return {"message": result.get("message", "")}
