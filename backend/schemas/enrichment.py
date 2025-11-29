from typing import Dict, Any
from pydantic import BaseModel

class LedgerMatchRequest(BaseModel):
    transaction: Dict[str, Any]
    ledger_context: Dict[str, Any]

class LedgerMatchResponse(BaseModel):
    match_result: Dict[str, Any]
