from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.db import Base, engine

# Import models so SQLAlchemy knows about the tables
import app.models.user
import app.models.expense

# Import routers
from app.routers.auth import auth_router
from app.routers.user import user_router
from app.routers.expense import expense_router


# =========================================================
# CREATE DATABASE TABLES
# =========================================================

Base.metadata.create_all(bind=engine)


# =========================================================
# CREATE FASTAPI APP
# =========================================================

app = FastAPI(
    title="Expense Manager API",
    description="Backend API for Expense Manager",
    version="1.0.0"
)


# =========================================================
# CORS
# =========================================================

app.add_middleware(
    CORSMiddleware,

    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
        "http://127.0.0.1:8000",
        "http://localhost:8000"
    ],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],
)


# =========================================================
# REGISTER ROUTERS
# =========================================================

app.include_router(auth_router)

app.include_router(user_router)

app.include_router(expense_router)


# =========================================================
# ROOT
# =========================================================

@app.get("/")
def root():

    return {
        "message": "Expense Manager API is running"
    }