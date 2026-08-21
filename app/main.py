from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.user import router as user_router
from app.routers.auth import router as auth_router
from app.routers.expense import router as expense_router


app = FastAPI(
    title="Expense Manager API",
    version="1.0.0",
)


# =========================================================
# CORS
# =========================================================

app.add_middleware(
    CORSMiddleware,

    # Production frontend
    allow_origins=[
        "https://expense-manager-frontend-z438.onrender.com",

        # Local development
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
    ],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],
)


# =========================================================
# ROUTERS
# =========================================================

# User registration
# POST /users/
app.include_router(
    user_router,
    prefix="/users",
    tags=["Users"],
)


# Authentication / Login
# POST /token
app.include_router(
    auth_router,
    tags=["Authentication"],
)


# Expenses
# POST   /expenses/
# GET    /expenses/
# GET    /expenses/{expense_id}
# PUT    /expenses/{expense_id}
# DELETE /expenses/{expense_id}
app.include_router(
    expense_router,
    prefix="/expenses",
    tags=["Expenses"],
)


# =========================================================
# ROOT
# =========================================================

@app.get("/")
def root():
    return {
        "message": "Expense Manager API is running"
    }