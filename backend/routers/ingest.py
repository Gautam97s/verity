from fastapi import APIRouter, Depends
from sqlmodel import Session
from schemas.ingest import WhatsAppIn
from db import get_session
from services.parser_services import parse_and_save_transaction

router = APIRouter()

@router.post("/whatsapp")
def ingest_whatsapp(payload: WhatsAppIn, session: Session = Depends(get_session)):
    tx = parse_and_save_transaction(session, payload.business_id, payload.raw_text, source="whatsapp")
    return {"message": "Ingested", "transaction_id": tx.id}
