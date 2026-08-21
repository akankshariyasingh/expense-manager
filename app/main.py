from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.user import router as user_router
from app.routers.auth import router as auth_router
from app.routers.expense import router as expense_router


app = FastAPI(
    title="Expense Manager API",
    version="1.0.0"
)


# ============================================================
# CORS CONFIGURATION
# ============================================================

origins = [
    "https://expense-manager-frontend-z438.onrender.com",
    "http://localhost:5173",
    "http://localhost:3000",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# ROUTERS
# ============================================================

app.include_router(user_router)
app.include_router(auth_router)
app.include_router(expense_router)


# ============================================================
# ROOT
# ============================================================

@app.get("/")
def root():
    return {
        "message": "Expense Manager API is running"
    }