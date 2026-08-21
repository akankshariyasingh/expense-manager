from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.user import router


app = FastAPI(
    title="Expense Manager API",
    description="Backend API for Expense Manager",
    version="1.0.0",
)


# -------------------------
# CORS Configuration
# -------------------------

origins = [
    "https://expense-manager-frontend-z438.onrender.com",
    "http://localhost:3000",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -------------------------
# Routers
# -------------------------

app.include_router(router)


# -------------------------
# Root Endpoint
# -------------------------

@app.get("/")
def root():
    return {
        "message": "Expense Manager API is running"
    }