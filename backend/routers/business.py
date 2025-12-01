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

from utils.auth import get_current_user
@router.get("/me", response_model=Business, response_model_exclude={"hashed_password"})
def get_current_business(username: str = Depends(get_current_user), session: Session = Depends(get_session)):
    business = session.exec(select(Business).where(Business.username == username)).first()
    return business
