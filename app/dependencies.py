from fastapi import Depends, status, HTTPException, Query
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.core.security import SECRET_KEY, ALGORITHM
from app.db import models
from app.services import user_service

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail="Token cannot be verified or expired",
                                          headers= {"WWW-Authenticate": "Bearer"},)

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str | None = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = user_service.get_user_by_username(db, username=username)
    if user is None:
        raise credentials_exception

    return user

def get_current_admin_user(current_user: models.User = Depends(get_current_user)):
    if current_user.role != "admin": #type: ignore
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not authorized for this action")

    return current_user

def pagination_params(skip: int = Query(0, ge=0, description="Records to be skipped"),
               limit: int = Query(10, ge=1, description="Max records to be shown")):
    safe_limit = min(limit, 100)

    return {"skip": skip, "limit": safe_limit}
