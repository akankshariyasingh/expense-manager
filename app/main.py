from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.user import router as user_router
from app.routers.auth import router as auth_router
from app.routers.expense import router as expense_router


app = FastAPI(
    title="Expense Manager API",
    version="1.0.0"
)


# =========================================================
# CORS CONFIGURATION
# =========================================================

app.add_middleware(
    CORSMiddleware,

    # Allow the Render frontend and local development
    allow_origins=[
        "https://expense-manager-frontend-z438.onrender.com",
        "http://expense-manager-frontend-z438.onrender.com",

        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
    ],

    # Also allow Render frontend origins
    allow_origin_regex=r"https://.*\.onrender\.com",

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],
)


# =========================================================
# USER ROUTES
# =========================================================

app.include_router(
    user_router,
    prefix="/users",
    tags=["Users"]
)


# =========================================================
# AUTHENTICATION ROUTES
# =========================================================

app.include_router(
    auth_router,
    tags=["Authentication"]
)


# =========================================================
# EXPENSE ROUTES
# =========================================================

app.include_router(
    expense_router,
    prefix="/expenses",
    tags=["Expenses"]
)


# =========================================================
# ROOT ROUTE
# =========================================================

@app.get("/")
def root():
    return {
        "message": "Expense Manager API is running",
        "status": "success"
    }