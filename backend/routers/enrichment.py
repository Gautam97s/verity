from fastapi import APIRouter
from schemas.enrichment import LedgerMatchRequest, LedgerMatchResponse
from agents.enrichment_agent import match_ledger_entry

router = APIRouter()

@router.post("/match", response_model=LedgerMatchResponse)
def match_ledger(payload: LedgerMatchRequest):
    result = match_ledger_entry(payload.transaction, payload.ledger_context)
    return {"match_result": result}
