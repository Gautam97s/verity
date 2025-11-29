import json
from typing import Dict, Any
from utils.llm import generate_content

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

def parse_transaction_with_ai(raw_text: str) -> Dict[str, Any]:
    """
    Parses raw text into a structured transaction using LLM.
    """
    result = generate_content(TRANSACTION_PARSER_PROMPT, raw_text)
    
    # Fallback if empty or error
    if not result or "error" in result:
        return {
            "direction": "inflow", # Default safe assumption
            "amount": 0.0,
            "currency": "INR",
            "method": "other",
            "counterparty_name": "Unknown",
            "category": "other",
            "invoice": {"has_invoice": False},
            "notes": "Offline mode - AI not active",
            "parsing_error": result.get("error", "Unknown error")
        }
    return result

def parse_invoice_with_ai(ocr_text: str) -> Dict[str, Any]:
    """
    Parses OCR text into structured invoice data using LLM.
    """
    result = generate_content(INVOICE_PARSER_PROMPT, ocr_text)
    if not result or "error" in result:
        return {"error": result.get("error", "Failed to parse invoice")}
    return result
