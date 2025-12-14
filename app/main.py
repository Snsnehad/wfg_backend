from fastapi import FastAPI, BackgroundTasks, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timezone

from .database import Base, engine, get_db
from .schemas import TransactionCreate, TransactionResponse
from .crud import get_transaction, create_transaction
from .worker import process_transaction

Base.metadata.create_all(bind=engine)

app = FastAPI(title="WFG Transaction Webhook Service")

# Health Check
@app.get("/")
def health_check():
    return {
        "status": "HEALTHY",
        "current_time": datetime.now(timezone.utc).isoformat()
    }

# Webhook Endpoint
@app.post("/v1/webhooks/transactions", status_code=202)
def receive_webhook(
    payload: TransactionCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    # Idempotency check
    if get_transaction(db, payload.transaction_id):
        return

    create_transaction(db, payload)
    background_tasks.add_task(process_transaction, payload.transaction_id)
    return

# Get Transaction Status (LIST response as required)
@app.get(
    "/v1/transactions/{transaction_id}",
    response_model=list[TransactionResponse]
)
def get_transaction_status(
    transaction_id: str,
    db: Session = Depends(get_db)
):
    txn = get_transaction(db, transaction_id)
    if not txn:
        raise HTTPException(status_code=404, detail="Transaction not found")

    return [txn]
