from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.modassembly.authentication.core.create_access_token import (
    create_access_token,
)
from app.modassembly.database.get_session import get_session
from app.models.User import User


router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


ACCESS_TOKEN_EXPIRE_MINUTES = 30


class Token(BaseModel):
    access_token: str
    token_type: str


@router.post("/token")
def login_api(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: Session = Depends(get_session),
) -> Token:
    print(form_data)
    user = session.query(User).filter(User.email == form_data.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User not found for email :: {form_data.username}",
        )
    if not pwd_context.verify(form_data.password, str(user.password)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid password for email :: {form_data.username}",
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        email=str(user.email), expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")
