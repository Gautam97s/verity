from sqlmodel import Session, select, delete
from db import engine, init_db
from models.business import Business
from models.contact import Contact
from models.invoice import Invoice
from models.transaction import Transaction
from datetime import datetime, timedelta
import random

def seed_data():
    init_db()
    with Session(engine) as session:
        # Check if business exists
        existing_business = session.exec(select(Business).where(Business.id == 1)).first()
        if existing_business:
            print("Business exists. Clearing old data...")
            session.exec(delete(Transaction).where(Transaction.business_id == 1))
            session.exec(delete(Invoice).where(Invoice.business_id == 1))
            session.exec(delete(Contact).where(Contact.business_id == 1))
            session.delete(existing_business)
            session.commit()
            print("Old data cleared.")

        # 1. Create Business
        business = Business(
            id=1,
            name="TechFlow Solutions",
            owner_name="Gautam",
            industry="Technology",
            location="Bangalore",
            created_at=datetime.utcnow() - timedelta(days=365)
        )
        session.add(business)
        session.commit()
        session.refresh(business)
        print(f"Created Business: {business.name}")

        # 2. Create Contacts
        contacts = [
            Contact(business_id=business.id, name="Alpha Corp", type="customer", phone="+919876543210"),
            Contact(business_id=business.id, name="Beta Inc", type="customer", phone="+919876543211"),
            Contact(business_id=business.id, name="Gamma Ltd", type="supplier", phone="+919876543212"),
            Contact(business_id=business.id, name="Delta Services", type="supplier", phone="+919876543213"),
        ]
        for c in contacts:
            session.add(c)
        session.commit()
        print("Created Contacts")

        # 3. Create Transactions (Last 6 months)
        # Pattern: Growing revenue, some expenses
        start_date = datetime.utcnow() - timedelta(days=180)
        transactions = []
        
        for i in range(180):
            current_date = start_date + timedelta(days=i)
            
            # Inflow (Sales) - Random but generally increasing
            if random.random() < 0.3: # 30% chance of sale per day
                amount = random.randint(5000, 50000)
                transactions.append(Transaction(
                    business_id=business.id,
                    direction="inflow",
                    amount=amount,
                    date=current_date,
                    category="Sales",
                    method="bank_transfer",
                    raw_text=f"Payment received from {random.choice(['Alpha Corp', 'Beta Inc'])}"
                ))

            # Outflow (Expenses)
            if random.random() < 0.2: # 20% chance of expense
                amount = random.randint(2000, 15000)
                transactions.append(Transaction(
                    business_id=business.id,
                    direction="outflow",
                    amount=amount,
                    date=current_date,
                    category=random.choice(["Rent", "Utilities", "Software", "Salaries"]),
                    method="upi",
                    raw_text=f"Payment to {random.choice(['Gamma Ltd', 'Delta Services'])}"
                ))

        for t in transactions:
            session.add(t)
        session.commit()
        print(f"Created {len(transactions)} Transactions")

        # 4. Create Invoices (Some overdue)
        invoices = [
            Invoice(
                business_id=business.id,
                contact_id=1, # Alpha Corp
                amount=25000,
                type="receivable",
                status="overdue",
                due_date=(datetime.utcnow() - timedelta(days=10)).date(),
                description="Web Development Services"
            ),
            Invoice(
                business_id=business.id,
                contact_id=2, # Beta Inc
                amount=15000,
                type="receivable",
                status="pending",
                due_date=(datetime.utcnow() + timedelta(days=5)).date(),
                description="Maintenance Contract"
            ),
             Invoice(
                business_id=business.id,
                contact_id=3, # Gamma Ltd
                amount=8000,
                type="payable",
                status="pending",
                due_date=(datetime.utcnow() + timedelta(days=2)).date(),
                description="Server Hosting"
            )
        ]
        for inv in invoices:
            session.add(inv)
        session.commit()
        print("Created Invoices")

if __name__ == "__main__":
    seed_data()
