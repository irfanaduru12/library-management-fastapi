from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.user import UserResponse, UserCreate, Token
from app.services import user_service
from app.db.database import get_db
from fastapi.security import OAuth2PasswordRequestForm

from app.dependencies import get_current_user
from app.db import models

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    return user_service.register_user(db=db, user_data=user)

@router.delete("/delete/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return user_service.delete_user(db=db, user_id=user_id)

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return user_service.login_user(db=db, username=form_data.username, password=form_data.password)

