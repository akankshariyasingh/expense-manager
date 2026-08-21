import os

from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


# Load environment variables
load_dotenv()


# Get database URL
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./expense.db"
)


print("DATABASE URL:", DATABASE_URL)


# SQLite requires this setting
connect_args = {}

if DATABASE_URL.startswith("sqlite"):
    connect_args = {
        "check_same_thread": False
    }


# Create database engine
engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args
)


# Create session
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


# Base model
Base = declarative_base()


# Database dependency
def get_db():

    db = SessionLocal()

    try:

        yield db

    finally:

        db.close()