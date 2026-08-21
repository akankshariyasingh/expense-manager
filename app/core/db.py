from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


DATABASE_URL = "sqlite:///./expense.db"
import os

print("DATABASE URL:", DATABASE_URL)
print("CURRENT WORKING DIRECTORY:", os.getcwd())
print(
    "DATABASE FILE:",
    os.path.abspath("expense.db")
)


engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)


LocalSession = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


def get_db():

    db = LocalSession()

    try:
        yield db

    finally:
        db.close()


Base = declarative_base()