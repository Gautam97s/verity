import json
from typing import List, Dict, Any
from config import settings

try:
    from google import genai
    client = genai.Client(api_key=settings.GEMINI_API_KEY) if settings.GEMINI_API_KEY else None
except ImportError:
    client = None

LEDGER_MAPPING_PROMPT = """
You are an expert accounting assistant.
Input:
1. Parsed transaction JSON.
2. Existing DB snapshot (contacts, invoices).

Output: STRICT JSON schema:
{
  "contact_match": {
    "match_type": "exact" | "fuzzy" | "new",
    "contact_id": int | null,
    "contact_name": "string"
  },
  "invoice_match": {
    "matched": boolean,
    "invoice_id": int | null,
    "remaining_due": float | null
  },
  "transaction_record": {
    "direction": "inflow" | "outflow",
    "amount": float,
    "category": "string",
    "link_to_invoice_id": int | null
  }
}

Responsibilities:
- Match counterparty name to existing contacts (fuzzy string match).
- Match payments to open invoices (by invoice number and/or amount + counterparty).
- Suggest new contact creation if no good match.
- Suggest whether this payment fully or partially settles an invoice.
- Return ONLY JSON.
"""

CATEGORISATION_PROMPT = """
You are an expert bookkeeper.
Input: Transaction description + basic metadata.
Output: STRICT JSON schema:
{
  "category": "string",
  "subcategory": "string",
  "is_recurring": boolean,
  "confidence": float // 0.0 to 1.0
}

Responsibilities:
- Assign category/subcategory (e.g., inventory/food, rent, salary, utilities).
- Flag recurring expenses.
- Provide confidence score.
- Return ONLY JSON.
"""

def _call_gemini(prompt: str, content: str) -> dict:
    if client is None or not settings.GEMINI_API_KEY:
        return {}
    
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
        return {}

def match_ledger_entry(transaction_data: Dict, db_snapshot: Dict) -> Dict:
    """
    Matches a parsed transaction to existing contacts and invoices.
    db_snapshot should contain lists of contacts and open invoices.
    """
    content = json.dumps({
        "transaction": transaction_data,
        "snapshot": db_snapshot
    }, indent=2)
    return _call_gemini(LEDGER_MAPPING_PROMPT, content)

def categorize_transaction(description: str, metadata: Dict) -> Dict:
    """
    Categorizes a transaction based on description and metadata (amount, date, etc.).
    """
    content = json.dumps({
        "description": description,
        "metadata": metadata
    }, indent=2)
    return _call_gemini(CATEGORISATION_PROMPT, content)
