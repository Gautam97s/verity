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
import json
from typing import List, Dict, Any
from utils.llm import generate_content

LEDGER_MAPPING_PROMPT = """
You are an expert accounting assistant.
Input:
- Transaction: {description, amount, counterparty}
- DB Snapshot: List of existing contacts/invoices.
Output: STRICT JSON:
{
  "contact_match": {"contact_id": int | null, "match_type": "exact"|"fuzzy"|"new", "confidence": float},
  "invoice_match": {"invoice_id": int | null, "match_type": "exact"|"fuzzy"|"none"}
}
Match transaction to existing entities.
Return ONLY JSON.
"""

CATEGORISATION_PROMPT = """
You are an expert accountant.
Input: Transaction description & metadata.
Output: STRICT JSON:
{
  "category": "string",
  "sub_category": "string",
  "tax_code": "string" | null
}
Categorize expense/income accurately.
Return ONLY JSON.
"""

def match_ledger_entry(transaction_data: Dict, db_snapshot: Dict) -> Dict:
    """
    Matches a parsed transaction to existing contacts and invoices.
    """
    content = json.dumps({
        "transaction": transaction_data,
        "snapshot": db_snapshot
    }, indent=2)
    return generate_content(LEDGER_MAPPING_PROMPT, content)

def categorize_transaction(description: str, metadata: Dict) -> Dict:
    """
    Categorizes a transaction based on description.
    """
    content = json.dumps({
        "description": description,
        "metadata": metadata
    }, indent=2)
    return generate_content(CATEGORISATION_PROMPT, content)
