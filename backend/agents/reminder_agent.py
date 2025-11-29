import json
from typing import Dict
from utils.llm import generate_content

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
"""


def _fallback_template(context: Dict) -> Dict:
    """Local template when LLM is unavailable / fails."""
    customer = context.get("customer_name", "Customer")
    business = context.get("business_name", "your business")
    invoice = context.get("invoice_number", "the invoice")
    amount = context.get("amount_due", 0)
    due_date = context.get("due_date", "")
    days_overdue = context.get("days_overdue")

    extra = ""
    if days_overdue is not None and days_overdue > 0:
        extra = f" It is overdue by {days_overdue} days."

    msg = (
        f"Hi {customer}, this is a gentle reminder from {business} "
        f"for the pending payment of ₹{amount} for invoice {invoice}"
    )
    if due_date:
        msg += f" (due on {due_date})."
    else:
        msg += "."
    msg += extra + " Please ignore this message if you have already paid. Thank you!"

    return {"message": msg}


def generate_payment_reminder(context: Dict) -> Dict:
    """
    Generates a payment reminder message.
    Tries Grok (via utils.llm) first, then falls back to a local template.
    """
    content = json.dumps(context, indent=2)

    # 1. Try Grok
    result = generate_content(REMINDER_PROMPT, content)

    # 2. If Grok failed / empty message → fallback template
    if not result or not result.get("message") or "error" in result:
        print(f"[REMINDER] Grok failed or returned error, using fallback. Result: {result}")
        return _fallback_template(context)

    return result
