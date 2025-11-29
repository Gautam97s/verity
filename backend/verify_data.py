from sqlmodel import Session, select
from db import engine
from models.transaction import Transaction
from models.business import Business
from datetime import datetime

from config import settings

def verify():
    print(f"DB URL: {settings.DATABASE_URL}")
    with Session(engine) as session:
        businesses = session.exec(select(Business)).all()
        if not businesses:
            print("No businesses found!")
            return

        for business in businesses:
            print(f"Business: {business.name} (ID: {business.id})")
            txs = session.exec(select(Transaction).where(Transaction.business_id == business.id)).all()
            print(f"  Total Transactions: {len(txs)}")

if __name__ == "__main__":
    verify()
