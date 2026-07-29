from fastapi import APIRouter, Depends
from app.schemas.user import UserResponse
from app.db import models
from app.dependencies import get_current_user
from app.services import user_service

router = APIRouter(prefix="/user", tags=["user"])

@router.get("/me", response_model=UserResponse)
def read_user_me(current_user: models.User = Depends(get_current_user)):
    return user_service.get_user_profile(current_user=current_user)