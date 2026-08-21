from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.core.security import hash_password
from app.models.user import User
from app.schemas.api_response import Apiresponse
from app.schemas.user import (
    UserRequestDto,
    UserUpdateDto,
    UserresponseDto
)


user_router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@user_router.post(
    "/",
    response_model=Apiresponse,
    status_code=status.HTTP_201_CREATED
)
def create_user(
    user_request: UserRequestDto,
    db: Session = Depends(get_db)
):

    existing_username = (
        db.query(User)
        .filter(
            User.username == user_request.username
        )
        .first()
    )

    if existing_username:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )


    existing_email = (
        db.query(User)
        .filter(
            User.email == user_request.email
        )
        .first()
    )

    if existing_email:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )


    hashed_password = hash_password(
        user_request.password
    )


    new_user = User(
        username=user_request.username,
        email=user_request.email,
        password=hashed_password
    )


    db.add(new_user)

    db.commit()

    db.refresh(new_user)


    return Apiresponse(
        status="success",
        message="User created successfully",
        data={
            "user": UserresponseDto.model_validate(
                new_user
            )
        }
    )

# Create User
@user_router.post(
    "/",
    response_model=Apiresponse,
    status_code=status.HTTP_201_CREATED
)
def create_user(
    user_request: UserRequestDto,
    db: Session = Depends(get_db)
):
    # Check if username already exists
    existing_username = (
        db.query(User)
        .filter(User.username == user_request.username)
        .first()
    )

    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )

    # Check if email already exists
    existing_email = (
        db.query(User)
        .filter(User.email == user_request.email)
        .first()
    )

    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Hash the password
    hashed_pwd = hash_password(user_request.password)

    # Create new user
    new_user = User(
        username=user_request.username,
        email=user_request.email,
        password=hashed_pwd
    )

    # Save user to database
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return Apiresponse(
        status="success",
        message="User created successfully",
        data={
            "user": UserresponseDto.model_validate(new_user)
        }
    )