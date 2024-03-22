from typing import Annotated
from fastapi import Depends, HTTPException,status
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session, select
from db.mock_db import SessionTestDep
from core.security import ALGORITHM, verify_password
from jose import JWTError, jwt
from db.modals import TokenPayload, Users
from config import API_V1_STR, SECRET_KEY
from db.db_connection import  get_db
from pydantic import ValidationError


reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{API_V1_STR}/access-token"
)

SessionDep = Annotated[Session, Depends(get_db)]
TokenDep = Annotated[str, Depends(reusable_oauth2)]

def get_current_user(session: SessionDep, token: TokenDep) -> Users:
    try:
        payload = jwt.decode(
            token, str(SECRET_KEY), algorithms=[ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = session.get(Users, token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

CurrentUser = Annotated[Users, Depends(get_current_user)]

def get_user_by_email(*, session: Session, email: str) -> Users | None:
    statement = select(Users).where(Users.email == email)
    session_user = session.exec(statement).first()
    return session_user

def authenticate(*, session: Session, email: str, password: str) -> Users | None:
    db_user = get_user_by_email(session=session, email=email)
    if not db_user:
        return None
    if not verify_password(password, db_user.password):
        return None
    return db_user

def get_current_test_user(session: SessionTestDep, token: TokenDep) -> Users:
    try:
        payload = jwt.decode(
            token, str(SECRET_KEY), algorithms=[ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = session.get(Users, token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
CurrentTestUser = Annotated[Users, Depends(get_current_test_user)]