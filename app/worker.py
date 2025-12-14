import time
from .database import SessionLocal
from .crud import mark_processed

def process_transaction(transaction_id: str):
    # Simulate external API / processing delay
    time.sleep(30)

    db = SessionLocal()
    try:
        mark_processed(db, transaction_id)
    finally:
        db.close()
