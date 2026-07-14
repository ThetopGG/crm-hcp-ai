"""Authentication business logic."""
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.crud.user import get_user_by_email, create_user
from app.core.security import verify_password, create_access_token
from app.schemas.auth import UserCreate, UserLogin


def register_user(db: Session, user_in: UserCreate):
    existing = get_user_by_email(db, user_in.email)
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    user = create_user(db, user_in)
    token = create_access_token(data={"sub": str(user.id)})
    return token, user


def authenticate_user(db: Session, credentials: UserLogin):
    user = get_user_by_email(db, credentials.email)
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
    token = create_access_token(data={"sub": str(user.id)})
    return token, user
