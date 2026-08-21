from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.user import router as user_router
from app.routers.auth import router as auth_router
from app.routers.expense import router as expense_router


app = FastAPI(
    title="Expense Manager API",
    version="1.0.0",
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://expense-manager-frontend-z438.onrender.com",
        "http://localhost:3000",
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# ROOT / HEALTH
# ============================================================

@app.get("/")
def root():
    return {
        "message": "Expense Manager API is running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


# ============================================================
# USER ROUTES
# ============================================================

app.include_router(
    user_router,
    prefix="/users",
    tags=["Users"],
)


# ============================================================
# AUTH ROUTES
# ============================================================

app.include_router(
    auth_router,
    tags=["Authentication"],
)


# ============================================================
# EXPENSE ROUTES
# ============================================================

app.include_router(
    expense_router,
    prefix="/expenses",
    tags=["Expenses"],
)