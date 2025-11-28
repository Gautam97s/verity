import json
from typing import Dict
from config import settings

try:
    from google import genai
    client = genai.Client(api_key=settings.GEMINI_API_KEY) if settings.GEMINI_API_KEY else None
except ImportError:
    client = None

REMINDER_PROMPT = """
You are a helpful assistant for a small business owner.
Input:
{
  "business_name": "string",
  "customer_name": "string",
  "invoice_number": "string",
  "due_date": "YYYY-MM-DD",
  "amount_due": float,
  "days_overdue": int,
  "preferred_tone": "friendly" | "firm" | "urgent",
  "preferred_language": "English" | "Hinglish" | "Hindi"
}

Output: STRICT JSON schema:
{
  "message": "string"
}

Responsibilities:
- Generate a WhatsApp-style reminder message.
- Adapt tone and language as requested.
- Include key details (amount, invoice #, due date).
- Return ONLY JSON.
"""

def _call_gemini(prompt: str, content: str) -> dict:
    if client is None or not settings.GEMINI_API_KEY:
        return {"message": "Reminder generation unavailable (offline)."}
    
    full_prompt = f"{prompt}\n\nINPUT_DATA:\n{content}"
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash-exp",
            contents=full_prompt,
        )
        text = response.text.strip()
        if text.startswith("```"):
            text = text.strip("`")
            if text.startswith("json"):
                text = text[4:]
        return json.loads(text)
    except Exception as e:
        print(f"Gemini Error: {e}")
        return {"message": "", "error": str(e)}

def generate_payment_reminder(context: Dict) -> Dict:
    """
    Generates a payment reminder message.
    """
    content = json.dumps(context, indent=2)
    return _call_gemini(REMINDER_PROMPT, content)
