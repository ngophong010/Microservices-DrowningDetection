from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import Any

from app.crud import crud_user
from app.schemas import user as user_schema

from app.core import security

router = APIRouter()

@router.post("/register", response_model=user_schema.UserInDB, status_code=status.HTTP_201_CREATED)
async def register_new_user(user_in: user_schema.UserCreate):
    user = await crud_user.get_by_email(email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
        )
    user = await crud_user.create(user_in)
    return user

@router.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await crud_user.get_by_email(email=form_data.username)
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = security.create_access_token(subject=user.id)
    return {"access_token": access_token, "token_type": "bearer"}
