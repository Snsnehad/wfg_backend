# 🔗 WFG – Transaction Webhook Service (Backend)

## Overview

This service receives transaction webhooks from external payment processors, acknowledges them immediately, and processes transactions reliably in the background with idempotency guarantees.

The system is designed to be fast, reliable, and production-ready while keeping the implementation simple and easy to reason about.

---

## ✨ Features

- ⚡ **Fast webhook acknowledgment** (< 500ms, returns 202 Accepted)
- 🔄 **Background transaction processing** with 30-second delay
- 🔒 **Idempotent handling** of duplicate webhooks
- 💾 **Persistent storage** of transaction status and timestamps
- ☁️ **Cloud-deployed** public API endpoint

---

## 🛠️ Tech Stack

- **FastAPI** – high-performance Python web framework
- **PostgreSQL (Cloud – Supabase)** – persistent data storage
- **SQLAlchemy** – ORM for database interaction
- **Uvicorn** – ASGI server
- **Render** – cloud hosting platform

---

## 📡 API Endpoints

### 1️⃣ Health Check

**GET** `/`

**Response**
```json
{
  "status": "HEALTHY",
  "current_time": "2024-01-15T10:30:00Z"
}
```

---

### 2️⃣ Transaction Webhook

**POST** `/v1/webhooks/transactions`

**Request Body**
```json
{
  "transaction_id": "txn_abc123def456",
  "source_account": "acc_user_789",
  "destination_account": "acc_merchant_456",
  "amount": 150.50,
  "currency": "USD"
}
```

**Response**

`202 Accepted`

Response body is intentionally empty.  
Processing happens asynchronously in the background.

---

### 3️⃣ Get Transaction Status (For Testing)

**GET** `/v1/transactions/{transaction_id}`

**Response**
```json
[
  {
    "transaction_id": "txn_abc123def456",
    "source_account": "acc_user_789",
    "destination_account": "acc_merchant_456",
    "amount": 150.5,
    "currency": "USD",
    "status": "PROCESSED",
    "created_at": "2024-01-15T10:30:00Z",
    "processed_at": "2024-01-15T10:30:30Z"
  }
]
```

---

## 🔄 Background Processing

1. Webhook requests are acknowledged **immediately**
2. Each transaction is processed **asynchronously**
3. A **30-second delay** simulates external API or payment gateway processing
4. Final transaction status and timestamps are stored in the database

---

## 🔒 Idempotency Handling

- `transaction_id` is used as a **primary key**
- Duplicate webhook calls with the same `transaction_id`:
  - Return `202 Accepted`
  - Do not create duplicate records
  - Do not trigger duplicate background processing
- This mirrors real-world payment gateway behavior (e.g., Razorpay, Stripe)

---

## 💾 Data Storage

**Stored transaction fields include:**

- `transaction_id`
- `source_account`
- `destination_account`
- `amount`
- `currency`
- `status` (PROCESSING → PROCESSED)
- `created_at`
- `processed_at`

---

## 🚀 Running Locally

### Prerequisites

- Python 3.9+
- Virtual environment (recommended)

### Steps
```bash
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

**API will be available at:**  
`http://127.0.0.1:8000`

---

## ☁️ Deployment

- Backend is deployed on **Render**
- Database is hosted on **Supabase (PostgreSQL)**
- Environment variables are used for secure configuration

### Environment Variable
```
DATABASE_URL=postgresql://<user>:<password>@<pooler-host>:6543/postgres?sslmode=require
```

---

## 🌍 Live API

**Public Endpoint**

`https://wfg-backend.onrender.com`

---

## 🎯 Design Choices

- **FastAPI** chosen for performance and simplicity
- **BackgroundTasks** used to ensure fast webhook responses
- **PostgreSQL** used for reliable persistence
- **Idempotency** via primary key ensures safe webhook retries
- **Minimal dependencies** for clarity and maintainability

---

## ✅ Assessment Checklist

- ✅ 202 Accepted response
- ✅ < 500ms webhook response
- ✅ Background processing with delay
- ✅ Idempotency support
- ✅ Persistent storage
- ✅ Cloud deployment with public API

---

## 👤 Author

**Sneha Dwivedi**  
Full Stack Developer