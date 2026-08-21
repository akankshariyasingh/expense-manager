from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    username: str = Field(
        ...,
        min_length=3,
        max_length=50,
        description="Username of the user"
    )

    email: EmailStr = Field(
        ...,
        description="Email address of the user"
    )

    password: str = Field(
        ...,
        min_length=6,
        max_length=100,
        description="Password of the user"
    )


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        from_attributes = True
        