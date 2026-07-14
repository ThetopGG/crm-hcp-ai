"""Authentication endpoints: register and login."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.auth import UserCreate, UserLogin, Token
from app.services.auth_service import register_user, authenticate_user

router = APIRouter(prefix="/api/auth", tags=["Auth"])


@router.post("/register", response_model=Token)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    token, user = register_user(db, user_in)
    return Token(access_token=token, user=user)


@router.post("/login", response_model=Token)
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    token, user = authenticate_user(db, credentials)
    return Token(access_token=token, user=user)
