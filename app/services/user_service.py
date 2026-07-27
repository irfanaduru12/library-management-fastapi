from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.crud import crud_user
from app.schemas.user import UserCreate
from app.core.security import get_password_hash, verify_password, create_access_token


def register_user(db: Session, user_data: UserCreate):
    user = crud_user.get_user_by_username(db, username=user_data.username)

    if user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"User with username {user_data.username} already exists")

    hashed_pw = get_password_hash(user_data.password)

    return crud_user.create_user(db=db, user=user_data, hashed_password=hashed_pw)

def delete_user(db: Session, user_id: int):
    user = crud_user.get_user_by_id(db, user_id=user_id)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The user with id {user_id} cannot be found")

    crud_user.delete_user(db=db, db_user=user)

    return {"message": "User deleted succesfully"}

def login_user(db: Session, username: str, password: str):
    user = crud_user.get_user_by_username(db, username=username)

    if not user or not verify_password(password, str(user.hashed_password)):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Username or password is false",
                            headers={"WWW-Authenticate": "Bearer"},)

    access_token = create_access_token(data={"sub": user.username})

    return {"access_token": access_token, "token_type": "bearer"}