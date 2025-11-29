# backend/utils/whatsapp.py
import os
from twilio.rest import Client
from .logger import get_logger  # if you have one, else just use print

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_FROM = os.getenv("TWILIO_WHATSAPP_FROM", "whatsapp:+14155238886")

logger = get_logger(__name__) if "get_logger" in dir() else None

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN) if TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN else None


def send_whatsapp_message(to_phone_e164: str, message: str):
    """
    to_phone_e164: phone number in E.164 with 'whatsapp:' prefix, e.g. 'whatsapp:+919876543210'
    message: text body
    """
    if client is None:
        # For dev/demo when keys are missing
        print(f"[MOCK WHATSAPP] To: {to_phone_e164} | Message: {message}")
        return {"status": "mock", "to": to_phone_e164, "body": message}

    try:
        msg = client.messages.create(
            from_=TWILIO_WHATSAPP_FROM,
            to=f"whatsapp:{to_phone_e164}" if not to_phone_e164.startswith("whatsapp:") else to_phone_e164,
            body=message,
        )
        if logger:
            logger.info(f"Sent WhatsApp message SID={msg.sid} to {msg.to}")
        return {"status": "sent", "sid": msg.sid, "to": msg.to}
    except Exception as e:
        if logger:
            logger.error(f"Error sending WhatsApp message: {e}")
        else:
            print("Error sending WhatsApp:", e)
        return {"status": "error", "error": str(e)}
