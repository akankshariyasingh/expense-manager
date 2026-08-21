from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.core.secure import get_current_user

from app.models.expense import Expense
from app.models.user import User

from app.schemas.api_response import Apiresponse
from app.schemas.expenses import (
    ExpenseRequestDto,
    ExpenseresponseDto
)


expense_router = APIRouter(
    prefix="/expenses",
    tags=["Expenses"]
)


# =========================================================
# CREATE EXPENSE
# =========================================================

@expense_router.post(
    "/",
    response_model=Apiresponse,
    status_code=status.HTTP_201_CREATED
)
def create_expense(
    expense_request_dto: ExpenseRequestDto,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):

    new_expense = Expense(
        user_id=user.id,
        title=expense_request_dto.title,
        description=expense_request_dto.description,
        amount=expense_request_dto.amount,
        show=expense_request_dto.show
    )

    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)

    return Apiresponse(
        status="success",
        message="Expense created successfully",
        data={
            "expense": ExpenseresponseDto.model_validate(
                new_expense
            )
        }
    )


# =========================================================
# SEARCH EXPENSE
# IMPORTANT: THIS MUST COME BEFORE /{expense_id}
# =========================================================

@expense_router.get(
    "/search/",
    response_model=Apiresponse
)
def search_expenses(
    title: str,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):

    expenses = (
        db.query(Expense)
        .filter(
            Expense.user_id == user.id,
            Expense.title.ilike(f"%{title}%")
        )
        .all()
    )

    return Apiresponse(
        status="success",
        message="Expenses retrieved successfully",
        data={
            "expenses": [
                ExpenseresponseDto.model_validate(
                    expense
                )
                for expense in expenses
            ]
        }
    )


# =========================================================
# GET ALL EXPENSES
# =========================================================

@expense_router.get(
    "/",
    response_model=Apiresponse
)
def get_all_expenses(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):

    expenses = (
        db.query(Expense)
        .filter(
            Expense.user_id == user.id
        )
        .all()
    )

    return Apiresponse(
        status="success",
        message="Expenses retrieved successfully",
        data={
            "expenses": [
                ExpenseresponseDto.model_validate(
                    expense
                )
                for expense in expenses
            ]
        }
    )


# =========================================================
# GET EXPENSE BY ID
# =========================================================

@expense_router.get(
    "/{expense_id}",
    response_model=Apiresponse
)
def get_expense_by_id(
    expense_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):

    expense = (
        db.query(Expense)
        .filter(
            Expense.id == expense_id,
            Expense.user_id == user.id
        )
        .first()
    )

    if not expense:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense not found"
        )

    return Apiresponse(
        status="success",
        message="Expense retrieved successfully",
        data={
            "expense": ExpenseresponseDto.model_validate(
                expense
            )
        }
    )


# =========================================================
# UPDATE EXPENSE
# =========================================================

@expense_router.put(
    "/{expense_id}",
    response_model=Apiresponse
)
def update_expense(
    expense_id: int,
    expense_request_dto: ExpenseRequestDto,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):

    expense = (
        db.query(Expense)
        .filter(
            Expense.id == expense_id,
            Expense.user_id == user.id
        )
        .first()
    )

    if not expense:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense not found"
        )

    expense.title = expense_request_dto.title

    expense.description = (
        expense_request_dto.description
    )

    expense.amount = (
        expense_request_dto.amount
    )

    expense.show = (
        expense_request_dto.show
    )

    db.commit()
    db.refresh(expense)

    return Apiresponse(
        status="success",
        message="Expense updated successfully",
        data={
            "expense": ExpenseresponseDto.model_validate(
                expense
            )
        }
    )


# =========================================================
# DELETE EXPENSE
# =========================================================

@expense_router.delete(
    "/{expense_id}",
    response_model=Apiresponse
)
def delete_expense(
    expense_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):

    expense = (
        db.query(Expense)
        .filter(
            Expense.id == expense_id,
            Expense.user_id == user.id
        )
        .first()
    )

    if not expense:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense not found"
        )

    db.delete(expense)
    db.commit()

    return Apiresponse(
        status="success",
        message="Expense deleted successfully"
    )