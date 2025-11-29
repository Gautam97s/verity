from sqlmodel import Session
from models.transaction import Transaction
from models.invoice import Invoice
from models.contact import Contact
from services.invoice_services import recompute_invoice_status
from agents.parser_agent import parse_transaction_with_ai

def parse_and_save_transaction(session: Session, business_id: int, raw_text: str, source: str):
    parsed = parse_transaction_with_ai(raw_text)

    # Contact
    name = parsed.get("counterparty_name")
    contact = None
    if name:
        contact = session.exec(
            Contact.select().where(Contact.business_id == business_id, Contact.name == name)
        ).first()
        if not contact:
            contact = Contact(business_id=business_id, name=name)
            session.add(contact)
            session.commit()
            session.refresh(contact)

    # Invoice if present
    invoice_obj = None
    inv = parsed.get("invoice", {})
    if inv.get("has_invoice"):
        invoice_obj = Invoice(
            business_id=business_id,
            contact_id=contact.id if contact else None,
            amount=parsed["amount"],
            type="receivable" if parsed["direction"] == "inflow" else "payable",
            due_date=inv.get("due_date"),
        )
        recompute_invoice_status(invoice_obj)
        session.add(invoice_obj)
        session.commit()
        session.refresh(invoice_obj)

    # Transaction
    tx = Transaction(
        business_id=business_id,
        invoice_id=invoice_obj.id if invoice_obj else None,
        direction=parsed["direction"],
        amount=parsed["amount"],
        method=parsed.get("method", "other"),
        category=parsed.get("category", "other"),
        raw_text=raw_text,
        source=source,
    )
    session.add(tx)
    session.commit()
    session.refresh(tx)
    return tx
