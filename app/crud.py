from sqlalchemy.orm import Session
from datetime import datetime
from .models import Transaction
from .schemas import TransactionCreate

def get_transaction(db: Session, transaction_id: str):
    return db.query(Transaction).filter_by(transaction_id=transaction_id).first()

def create_transaction(db: Session, data: TransactionCreate):
    txn = Transaction(**data.dict())
    db.add(txn)
    db.commit()
    return txn

def mark_processed(db: Session, transaction_id: str):
    db.query(Transaction).filter(
        Transaction.transaction_id == transaction_id
    ).update({
        "status": "PROCESSED",
        "processed_at": datetime.utcnow()
    }, synchronize_session=False) 
    db.commit()
