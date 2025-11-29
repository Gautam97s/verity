from fastapi import APIRouter, HTTPException
from schemas.ingest import (
    TransactionParseRequest, TransactionParseResponse,
    InvoiceParseRequest, InvoiceParseResponse,
    CSVParseRequest, CSVParseResponse
)
from agents.parser_agent import parse_transaction_with_ai, parse_invoice_with_ai
from agents.csv_agent import map_csv_columns_with_ai

router = APIRouter()

@router.post("/transaction", response_model=TransactionParseResponse)
def ingest_transaction(payload: TransactionParseRequest):
    parsed = parse_transaction_with_ai(payload.raw_text)
    return {"parsed_transaction": parsed}

@router.post("/invoice", response_model=InvoiceParseResponse)
def ingest_invoice(payload: InvoiceParseRequest):
    parsed = parse_invoice_with_ai(payload.ocr_text)
    return {"parsed_invoice": parsed}

@router.post("/csv", response_model=CSVParseResponse)
def ingest_csv(payload: CSVParseRequest):
    # For now, we just map columns and maybe return a dummy list of parsed transactions
    # The user request said: "For each row, call the appropriate csv_agent function"
    # But csv_agent currently only maps columns. 
    # I will assume we map columns and then return the mapping for now, 
    # or if the user wants "parsed transactions", I might need to implement row parsing logic here or in agent.
    # The user said: "For each row, call the appropriate csv_agent function and return a list of parsed transactions"
    # But map_csv_columns_with_ai takes headers and sample rows.
    # I will implement the mapping call and return it in a structured way, 
    # but since the response model expects "parsed_transactions", I'll mock that part or adapt.
    
    # Actually, let's stick to what the agent does: map columns.
    # But the user asked for "parsed transactions". 
    # I'll update the agent call to map columns, and then "parse" rows using that mapping (simple logic).
    
    mapping = map_csv_columns_with_ai(payload.headers, payload.rows[:5])
    
    # Simple parsing logic: rename keys based on mapping
    parsed_txs = []
    for row in payload.rows:
        tx = {}
        for col, val in row.items():
            # Find which canonical field this col maps to
            canonical = next((k for k, v in mapping.items() if v == col), None)
            if canonical:
                tx[canonical] = val
            else:
                tx[col] = val # Keep original if no mapping
        parsed_txs.append(tx)
        
    return {"parsed_transactions": parsed_txs}
