from sqlmodel import SQLModel, create_engine, Session
from config import settings

engine = create_engine(settings.DATABASE_URL, echo=False)

def init_db():
    from models import business, contact, invoice, transaction, raw_event
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
