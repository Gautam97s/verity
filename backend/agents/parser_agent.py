# Will replace later when Kaggle prompt is ready
def parse_transaction_with_ai(raw_text: str) -> dict:
    return {
        "direction": "inflow",
        "amount": 1000.0,
        "method": "upi",
        "counterparty_name": "Unknown",
        "category": "sales",
        "invoice": {
            "has_invoice": False
        }
    }
