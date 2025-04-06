from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# PostgreSQL connection URL format: postgresql://username:password@host:port/database
POSTGRESQL_DATABASE_URL = "postgresql://postgres:password@db:5432/iot_data"

engine = create_engine(
    POSTGRESQL_DATABASE_URL,
    pool_size=20,
    max_overflow=10,
    pool_pre_ping=True,
    pool_recycle=3600
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()