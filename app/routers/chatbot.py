from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.core.jwt_helper import get_current_user
from app.models.expense import Expense
from app.schemas.chatbot import ChatRequest, ChatResponse
from app.services.gemini_service import ask_gemini


router = APIRouter()


def get_time_of_day(hour):
    if 5 <= hour < 12:
        return "Morning"
    elif 12 <= hour < 17:
        return "Afternoon"
    elif 17 <= hour < 21:
        return "Evening"
    else:
        return "Night"


@router.post("/chat", response_model=ChatResponse)
def chat(
    request: ChatRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """
    Expense Assistant.

    Simple expense questions are answered directly
    from the user's database.

    Gemini is used only for questions that require
    general AI-style analysis or advice.
    """

    message = request.message.lower().strip()

    expenses = (
        db.query(Expense)
        .filter(
            Expense.user_id == current_user.id
        )
        .order_by(
            Expense.created_at.desc()
        )
        .all()
    )

    # ========================================================
    # GREETING
    # ========================================================

    if message in [
        "hello",
        "hi",
        "hey",
        "hello there",
        "hi there",
        "hey there"
    ]:
        return ChatResponse(
            reply=(
                f"Hi {current_user.username}! 👋 "
                "Ask me anything about your spending."
            )
        )

    # ========================================================
    # NO EXPENSES
    # ========================================================

    if not expenses:
        return ChatResponse(
            reply=(
                "No expenses recorded yet. "
                "Add an expense to start analyzing your spending."
            )
        )

    # ========================================================
    # TOTAL
    # ========================================================

    total = sum(
        float(expense.amount)
        for expense in expenses
    )

    # ========================================================
    # CATEGORY TOTALS
    # ========================================================

    category_totals = {}

    for expense in expenses:

        category = expense.category or "Other"

        category_totals[category] = (
            category_totals.get(category, 0)
            + float(expense.amount)
        )

    # ========================================================
    # CATEGORY QUESTIONS
    # ========================================================

    category_names = [
        "food",
        "travel",
        "shopping",
        "bills",
        "entertainment",
        "health",
        "education",
        "other"
    ]

    requested_category = None

    for category in category_names:

        if category in message:

            requested_category = category.title()

            break

    if requested_category:

        category_expenses = [
            expense
            for expense in expenses
            if (expense.category or "Other").lower()
            == requested_category.lower()
        ]

        if not category_expenses:

            return ChatResponse(
                reply=(
                    f"You don't have any "
                    f"{requested_category.lower()} expenses yet."
                )
            )

        category_total = sum(
            float(expense.amount)
            for expense in category_expenses
        )

        return ChatResponse(
            reply=(
                f"You've spent ₹{category_total:,.2f} "
                f"on {requested_category.lower()} "
                f"across {len(category_expenses)} "
                f"expense"
                f"{'s' if len(category_expenses) != 1 else ''}."
            )
        )

    # ========================================================
    # CATEGORY BREAKDOWN
    # ========================================================

    if any(
        keyword in message
        for keyword in [
            "by category",
            "per category",
            "each category",
            "categories",
            "category breakdown",
            "category wise",
            "category-wise",
            "breakdown"
        ]
    ):

        sorted_categories = sorted(
            category_totals.items(),
            key=lambda item: item[1],
            reverse=True
        )

        lines = [
            f"• {category}: ₹{amount:,.2f}"
            for category, amount
            in sorted_categories
        ]

        return ChatResponse(
            reply="\n".join(lines)
        )

    # ========================================================
    # TOP CATEGORY
    # ========================================================

    if any(
        phrase in message
        for phrase in [
            "top category",
            "highest category",
            "largest category",
            "most spending",
            "spending the most",
            "spend the most",
            "where am i spending the most",
            "where do i spend the most",
            "which category"
        ]
    ):

        top_category = max(
            category_totals,
            key=category_totals.get
        )

        top_amount = category_totals[top_category]

        percentage = (
            (top_amount / total) * 100
            if total > 0
            else 0
        )

        return ChatResponse(
            reply=(
                f"Your top spending category is "
                f"{top_category} with "
                f"₹{top_amount:,.2f}, which is "
                f"{percentage:.1f}% of your total spending."
            )
        )

    # ========================================================
    # TOTAL SPENDING
    # ========================================================

    if any(
        phrase in message
        for phrase in [
            "how much have i spent",
            "how much did i spend",
            "how much have i spend",
            "how much i spent",
            "how much i have spent",
            "total spent",
            "total spending",
            "total expense",
            "total expenses",
            "total amount",
            "my total spending",
            "my total expenses",
            "how much money have i spent",
            "how much money did i spend"
        ]
    ):

        return ChatResponse(
            reply=(
                f"You've spent ₹{total:,.2f} "
                f"across {len(expenses)} expenses."
            )
        )

    # ========================================================
    # BIGGEST EXPENSE
    # ========================================================

    if any(
        keyword in message
        for keyword in [
            "biggest expense",
            "largest expense",
            "highest expense",
            "most expensive expense",
            "maximum expense",
            "most expensive"
        ]
    ):

        biggest = max(
            expenses,
            key=lambda expense: expense.amount
        )

        return ChatResponse(
            reply=(
                f"Your biggest expense is "
                f"{biggest.title} — "
                f"₹{float(biggest.amount):,.2f} "
                f"({biggest.category or 'Other'})."
            )
        )

    # ========================================================
    # RECENT EXPENSES
    # ========================================================

    if any(
        keyword in message
        for keyword in [
            "recent expenses",
            "latest expenses",
            "last expenses",
            "recent spending",
            "latest spending"
        ]
    ):

        recent = expenses[:5]

        lines = [
            (
                f"• {expense.title}: "
                f"₹{float(expense.amount):,.2f} "
                f"({expense.category or 'Other'})"
            )
            for expense in recent
        ]

        return ChatResponse(
            reply="\n".join(lines)
        )

    # ========================================================
    # LIST EXPENSES
    # ========================================================

    if any(
        keyword in message
        for keyword in [
            "show expenses",
            "list expenses",
            "my expenses",
            "all expenses",
            "show my expenses",
            "what are my expenses"
        ]
    ):

        lines = [
            (
                f"• {expense.title}: "
                f"₹{float(expense.amount):,.2f} "
                f"({expense.category or 'Other'})"
            )
            for expense in expenses[:10]
        ]

        return ChatResponse(
            reply="\n".join(lines)
        )

    # ========================================================
    # TIME OF DAY ANALYSIS
    # ========================================================

    if any(
        keyword in message
        for keyword in [
            "what time",
            "which time",
            "time do i spend",
            "time i spend",
            "time spending",
            "time of day",
            "when do i spend",
            "when i spend"
        ]
    ):

        time_totals = {
            "Morning": 0,
            "Afternoon": 0,
            "Evening": 0,
            "Night": 0
        }

        for expense in expenses:

            period = get_time_of_day(
                expense.created_at.hour
            )

            time_totals[period] += float(
                expense.amount
            )

        highest_period = max(
            time_totals,
            key=time_totals.get
        )

        highest_amount = time_totals[
            highest_period
        ]

        if highest_amount == 0:

            return ChatResponse(
                reply=(
                    "I don't have enough data "
                    "to determine that yet."
                )
            )

        return ChatResponse(
            reply=(
                f"You spend the most in the "
                f"{highest_period.lower()} "
                f"— ₹{highest_amount:,.2f}."
            )
        )

    # ========================================================
    # GEMINI FALLBACK
    # ========================================================

    expense_summary = "\n".join(
        [
            (
                f"- {expense.title}: "
                f"₹{float(expense.amount):,.2f} "
                f"| Category: "
                f"{expense.category or 'Other'} "
                f"| Date/time: "
                f"{expense.created_at.strftime('%d/%m/%Y %H:%M:%S')} "
                f"| Time of day: "
                f"{get_time_of_day(expense.created_at.hour)}"
            )
            for expense in expenses
        ]
    )

    prompt = f"""
You are a friendly Expense Manager Assistant.

Answer the user's question using ONLY the expense data below.

User question:
{request.message}

Expense data:
{expense_summary}

RESPONSE STYLE:
- Be natural, friendly, and conversational.
- Answer directly.
- Keep the answer to 1-2 short sentences.
- Use simple everyday language.
- Do not sound like a report.
- Do not start with "Based on your expense data".
- Do not repeat the question.
- Do not give unnecessary explanations.
- Do not give advice unless the user asks for it.
- Use ₹ for amounts.

DATA RULES:
- Do not invent expenses, amounts, dates, times, or categories.
- You may calculate totals, percentages, averages, and comparisons.
- Use the provided Category values.
- Use the provided Time of day values.
- If there is not enough data, say:
  "I don't have enough data to determine that yet."
"""

    try:

        ai_reply = ask_gemini(prompt)

        return ChatResponse(
            reply=ai_reply.strip()
        )

    except Exception:

        # Gemini quota/error fallback.
        # The application itself continues working.

        return ChatResponse(
            reply=(
                "I can answer questions about your "
                "expenses, totals, categories, and "
                "recent spending right now. "
                "Try asking one of those."
            )
        )