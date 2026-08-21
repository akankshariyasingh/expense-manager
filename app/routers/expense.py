from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.models.expense import Expense
from app.schemas.expenses import ExpenseRequestDto
from app.core.jwt_helper import get_current_user


router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_expense(
    expense_data: ExpenseRequestDto,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    expense = Expense(
        title=expense_data.title,
        amount=expense_data.amount,
        description=expense_data.description,
        show=expense_data.show,
        user_id=current_user.id
    )

    db.add(expense)
    db.commit()
    db.refresh(expense)

    return {
        "status": "success",
        "message": "Expense created successfully",
        "data": {
            "expense": {
                "id": expense.id,
                "user_id": expense.user_id,
                "title": expense.title,
                "amount": expense.amount,
                "description": expense.description,
                "show": expense.show,
                "created_at": expense.created_at
            }
        }
    }


@router.get("/")
def get_all_expenses(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    expenses = (
        db.query(Expense)
        .filter(Expense.user_id == current_user.id)
        .all()
    )

    return {
        "status": "success",
        "message": "Expenses retrieved successfully",
        "data": {
            "expenses": expenses
        }
    }


@router.get("/search/")
def search_expenses(
    keyword: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    expenses = (
        db.query(Expense)
        .filter(
            Expense.user_id == current_user.id,
            Expense.title.ilike(f"%{keyword}%")
        )
        .all()
    )

    return {
        "status": "success",
        "message": "Expenses searched successfully",
        "data": {
            "expenses": expenses
        }
    }


@router.get("/{expense_id}")
def get_expense_by_id(
    expense_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    expense = (
        db.query(Expense)
        .filter(
            Expense.id == expense_id,
            Expense.user_id == current_user.id
        )
        .first()
    )

    if not expense:
        raise HTTPException(
            status_code=404,
            detail="Expense not found"
        )

    return {
        "status": "success",
        "message": "Expense retrieved successfully",
        "data": {
            "expense": expense
        }
    }


@router.put("/{expense_id}")
def update_expense(
    expense_id: int,
    expense_data: ExpenseRequestDto,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    expense = (
        db.query(Expense)
        .filter(
            Expense.id == expense_id,
            Expense.user_id == current_user.id
        )
        .first()
    )

    if not expense:
        raise HTTPException(
            status_code=404,
            detail="Expense not found"
        )

    expense.title = expense_data.title
    expense.amount = expense_data.amount
    expense.description = expense_data.description
    expense.show = expense_data.show

    db.commit()
    db.refresh(expense)

    return {
        "status": "success",
        "message": "Expense updated successfully",
        "data": {
            "expense": expense
        }
    }


@router.delete("/{expense_id}")
def delete_expense(
    expense_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    expense = (
        db.query(Expense)
        .filter(
            Expense.id == expense_id,
            Expense.user_id == current_user.id
        )
        .first()
    )

    if not expense:
        raise HTTPException(
            status_code=404,
            detail="Expense not found"
        )

    db.delete(expense)
    db.commit()

    return {
        "status": "success",
        "message": "Expense deleted successfully",
        "data": {}
    }