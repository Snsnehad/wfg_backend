from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = (
    "postgresql://postgres.mlsdyymldckhomhcbjug:Sneha%402002@aws-1-ap-southeast-2.pooler.supabase.com:5432/postgres"
)

engine = create_engine(
    DATABASE_URL,
    pool_size=20,
    max_overflow=0,
    pool_pre_ping=False,  # OFF - removes latency
    pool_recycle=300,
    echo=False,
    execution_options={
        "isolation_level": "READ COMMITTED"
    },
    connect_args={
        "connect_timeout": 3,
        "keepalives": 1,
        "keepalives_idle": 5,
        "keepalives_interval": 2,
        "keepalives_count": 2,
    }
)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
