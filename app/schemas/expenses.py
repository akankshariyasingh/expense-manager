from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class ExpenseRequestDto(BaseModel):

    title: str = Field(
        ...,
        description="The title of the expense",
        min_length=1,
        max_length=50
    )

    amount: float = Field(
        ...,
        description="The amount of the expense"
    )

    description: Optional[str] = Field(
        None,
        description="The description of the expense"
    )

    category: str = Field(
        ...,
        description="Category of the expense"
    )

    show: bool = Field(
        default=True,
        description="Whether the expense should be shown"
    )


class ExpenseresponseDto(BaseModel):

    id: int

    user_id: int

    title: str

    amount: float

    description: Optional[str]

    category: str

    show: bool

    created_at: datetime

    model_config = {
        "from_attributes": True
    }