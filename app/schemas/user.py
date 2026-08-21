from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class UserRequestDto(BaseModel):

    username: str = Field(
        ...,
        description="The username of the user",
        min_length=3
    )

    email: EmailStr = Field(
        ...,
        description="The email address of the user"
    )

    password: str = Field(
        ...,
        description="The password for the user",
        min_length=6
    )


class UserUpdateDto(BaseModel):

    username: Optional[str] = Field(
        None,
        description="The updated username",
        min_length=3
    )

    email: Optional[EmailStr] = Field(
        None,
        description="The updated email address"
    )

    password: Optional[str] = Field(
        None,
        description="The updated password",
        min_length=6
    )


class UserresponseDto(BaseModel):

    id: int

    username: str

    email: str

    created_at: datetime

    model_config = {
        "from_attributes": True
    }


class LoginRequest(BaseModel):

    email: str

    password: str


class LoginResponse(BaseModel):

    access_token: str

    user: UserresponseDto