from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.schemas.user import UserCreate
from app.core.security import get_password_hash, verify_password, create_access_token
from app.db import models

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def register_user(db: Session, user_data: UserCreate):
    user = get_user_by_username(db=db, username=user_data.username)

    if user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"User with username {user_data.username} already exists")

    hashed_pw = get_password_hash(user_data.password)

    db_user = models.User(username = user_data.username, hashed_password = hashed_pw, role = user_data.role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user

def delete_user(db: Session, user_id: int):
    user = get_user_by_id(db=db, user_id=user_id)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The user with id {user_id} cannot be found")

    if type(user).__name__ == 'Row':
        user = user[0]

    db.delete(user)
    db.commit()

    return {"message": "User deleted succesfully"}

def login_user(db: Session, username: str, password: str):
    user = db.query(models.User).filter(models.User.username == username).first()

    if not user or not verify_password(password, str(user.hashed_password)):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Username or password is false",
                            headers={"WWW-Authenticate": "Bearer"},)

    access_token = create_access_token(data={"sub": user.username})

    return {"access_token": access_token, "token_type": "bearer"}

def get_user_profile(current_user: models.User):
    try:
        return current_user
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Server Problem")
    