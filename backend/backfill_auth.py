from sqlmodel import Session, select
from db import engine
from models.business import Business
from utils.auth import get_password_hash
import random
import string

def backfill_auth():
    with Session(engine) as session:
        businesses = session.exec(select(Business).where(
            (Business.username == None) | (Business.hashed_password == None)
        )).all()
        
        print(f"Found {len(businesses)} businesses to backfill.")
        
        for b in businesses:
            if not b.username:
                # Generate a safe unique username
                base_name = b.name.lower().replace(" ", "")[:10]
                random_suffix = ''.join(random.choices(string.digits, k=4))
                b.username = f"{base_name}{random_suffix}"
                print(f"Generated username for ID {b.id}: {b.username}")
            
            if not b.hashed_password:
                # Set a default password that must be reset
                default_pw = "Temporary@123"
                b.hashed_password = get_password_hash(default_pw)
                print(f"Set default password for ID {b.id}")
            
            session.add(b)
        
        session.commit()
        print("Backfill complete.")

if __name__ == "__main__":
    backfill_auth()
