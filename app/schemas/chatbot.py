from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str = Field(
        ...,
        min_length=1,
        max_length=1000,
        description="Message sent to the Expense Assistant"
    )


class ChatResponse(BaseModel):
    reply: str