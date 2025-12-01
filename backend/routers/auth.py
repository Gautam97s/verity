from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select
from db import get_session
from models.business import Business
from utils.auth import get_password_hash, verify_password, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from pydantic import BaseModel
from datetime import timedelta

router = APIRouter()

class BusinessCreate(BaseModel):
    name: str
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

from sqlalchemy.exc import IntegrityError

@router.post("/signup", response_model=Token)
def signup(business: BusinessCreate, session: Session = Depends(get_session)):
    # Create new business
    hashed_password = get_password_hash(business.password)
    db_business = Business(
        name=business.name,
        username=business.username,
        hashed_password=hashed_password
    )
    try:
        session.add(db_business)
        session.commit()
        session.refresh(db_business)
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": db_business.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# Dummy hash for timing attack prevention
DUMMY_HASH = "$argon2id$v=19$m=65536,t=3,p=4$s9Z6b02Jca7VGkOGXU3iIgA$wNLNiuG5LBTQHE7ZarixiGfZkEM1Ub3qQjorgG"

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    # Find user
    business = session.exec(select(Business).where(Business.username == form_data.username)).first()
    
    # Determine which hash to use (real or dummy)
    if business:
        hashed_password = business.hashed_password
    else:
        hashed_password = DUMMY_HASH
    
    # Verify password (always performed to prevent timing attacks)
    is_valid = verify_password(form_data.password, hashed_password)
    
    # If user not found OR password invalid, raise error
    if not business or not is_valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": business.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
