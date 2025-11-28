import json
from config import settings

try:
    from google import genai
    client = genai.Client(api_key=settings.GEMINI_API_KEY) if settings.GEMINI_API_KEY else None
except ImportError:
    client = None

TRANSACTION_PARSER_PROMPT = """
You are an expert financial data parser for Indian MSMEs.
Input: raw text message (UPI, WhatsApp, POS slip text, SMS, free-text).
Output: STRICT JSON schema:
{
  "direction": "inflow" | "outflow",
  "amount": float,
  "currency": "INR",
  "method": "upi" | "pos" | "cash" | "bank" | "other",
  "counterparty_name": "string" | null,
  "category": "sales" | "inventory" | "rent" | "salary" | "other",
  "invoice": {
    "has_invoice": boolean,
    "invoice_number": "string" | null,
    "due_date": "YYYY-MM-DD" | null
  },
  "notes": "string" // optional
}
Extract amount, direction, payment method. Identify customer/supplier name. Detect invoice reference & due date if present. Map to business meaningful category.
Return ONLY JSON.
"""

INVOICE_PARSER_PROMPT = """
You are an expert invoice OCR parser.
Input: OCR text from an invoice.
Output: STRICT JSON schema:
{
  "invoice_number": "string" | null,
  "seller": "string" | null,
  "buyer": "string" | null,
  "total_amount": float,
  "due_date": "YYYY-MM-DD" | null,
  "issue_date": "YYYY-MM-DD" | null,
  "items": [
    {"name": "string", "amount": float}
  ]
}
Robustly extract invoice header fields. Extract line items when possible. Handle partially missing fields gracefully.
Return ONLY JSON.
"""

def _call_gemini(prompt: str, content: str) -> dict:
    if client is None or not settings.GEMINI_API_KEY:
        # Mock response for dev/offline
        return {"error": "Gemini API key not set or library missing"}
    
    full_prompt = f"{prompt}\n\nINPUT_TEXT:\n{content}"
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
        return {}

def parse_transaction_with_ai(raw_text: str) -> dict:
    # Fallback/Mock if offline (matches previous stub behavior roughly but better structure)
    if client is None or not settings.GEMINI_API_KEY:
        return {
            "direction": "inflow",
            "amount": 0.0,
            "currency": "INR",
            "method": "other",
            "counterparty_name": "Unknown",
            "category": "other",
            "invoice": {"has_invoice": False},
            "notes": "Offline mode - AI not active"
        }
    return _call_gemini(TRANSACTION_PARSER_PROMPT, raw_text)

def parse_invoice_with_ai(ocr_text: str) -> dict:
    if client is None or not settings.GEMINI_API_KEY:
        return {
            "invoice_number": None,
            "total_amount": 0.0,
            "items": []
        }
    return _call_gemini(INVOICE_PARSER_PROMPT, ocr_text)
