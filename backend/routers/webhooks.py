# backend/routers/webhooks.py
from fastapi import APIRouter, Form, Request

router = APIRouter()

@router.post("/whatsapp")
async def whatsapp_webhook(
    request: Request,
    From: str = Form(...),
    Body: str = Form(...)
):
    # Twilio posts form-encoded data
    print(f"[INCOMING WHATSAPP] From={From} Body={Body}")
    # Optional: run AI to categorize reply or update DB
    return "OK"
