from fastapi import FastAPI, BackgroundTasks, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timezone
import time
from fastapi import Request
from .database import Base, engine, get_db
from .schemas import TransactionCreate, TransactionResponse
from .crud import get_transaction, create_transaction
from .worker import process_transaction
from .models import Transaction
import logging
Base.metadata.create_all(bind=engine)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
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
    try:
        start = time.time()

        # ✅ Idempotency check
        existing_txn = db.query(Transaction).filter(
            Transaction.transaction_id == payload.transaction_id
        ).first()

        if existing_txn:
            logger.info(
                f"Duplicate webhook received for {payload.transaction_id}"
            )
            return  # ✅ silently accept duplicate

        txn = Transaction(**payload.dict())
        db.add(txn)
        db.commit()

        db_time_ms = (time.time() - start) * 1000
        logger.info(f"DB time: {db_time_ms:.2f} ms")

        background_tasks.add_task(
            process_transaction,
            payload.transaction_id
        )

    except Exception as e:
        db.rollback()
        logger.exception("Webhook processing failed")
        raise HTTPException(status_code=500, detail="Internal Server Error")

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
    # Single optimized query
    txn = db.query(Transaction).filter(
        Transaction.transaction_id == transaction_id
    ).first()
    
    if not txn:
        raise HTTPException(status_code=404, detail="Transaction not found")
    
    return [txn]

@app.middleware("http")
async def latency_middleware(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    latency_ms = (time.perf_counter() - start) * 1000
    response.headers["X-Latency-ms"] = f"{latency_ms:.2f}"
    return response