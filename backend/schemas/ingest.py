from typing import List, Optional, Dict, Any
from pydantic import BaseModel

class TransactionParseRequest(BaseModel):
    business_id: int
    raw_text: str

class TransactionParseResponse(BaseModel):
    parsed_transaction: Dict[str, Any]

class InvoiceParseRequest(BaseModel):
    ocr_text: str

class InvoiceParseResponse(BaseModel):
    parsed_invoice: Dict[str, Any]

class CSVParseRequest(BaseModel):
    headers: List[str]
    rows: List[Dict[str, Any]]

class CSVParseResponse(BaseModel):
    parsed_transactions: List[Dict[str, Any]]
