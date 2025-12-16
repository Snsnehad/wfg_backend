import time
from .database import SessionLocal
from .crud import mark_processed

def process_transaction(transaction_id: str):
    time.sleep(30)

    db = SessionLocal()
    try:
        mark_processed(db, transaction_id)
    except Exception as e:
        print(f"Error processing {transaction_id}: {e}")
    finally:
        db.close()
