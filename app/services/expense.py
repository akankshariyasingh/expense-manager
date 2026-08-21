from datetime import datetime

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
        description="The amount of the expense",
        gt=0
    )

    description: str = Field(
        ...,
        description="The description of the expense",
        max_length=500
    )

    show: bool = Field(
        default=True,
        description="Whether the expense should be shown"
    )


class ExpenseresponseDto(BaseModel):

    id: int = Field(
        ...,
        description="The ID of the expense"
    )

    user_id: int = Field(
        ...,
        description="The ID of the user who owns the expense"
    )

    title: str = Field(
        ...,
        description="The title of the expense"
    )

    amount: float = Field(
        ...,
        description="The amount of the expense"
    )

    description: str = Field(
        ...,
        description="The description of the expense"
    )

    show: bool = Field(
        ...,
        description="Whether the expense should be shown"
    )

    created_at: datetime = Field(
        ...,
        description="The creation date of the expense"
    )

    model_config = {
        "from_attributes": True
    }