from typing import List
from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from db import get_session
from models.business import Business

router = APIRouter()

@router.post("/create", response_model=Business)
def create_business(business: Business, session: Session = Depends(get_session)):
    session.add(business)
    session.commit()
    session.refresh(business)
    return business

@router.get("/list", response_model=List[Business])
def list_businesses(session: Session = Depends(get_session)):
    businesses = session.exec(select(Business)).all()
    return businesses
