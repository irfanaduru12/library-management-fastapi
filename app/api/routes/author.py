from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.schemas.author import AuthorCreate, AuthorResponse, AuthorUpdate
from app.dependencies import pagination_params
from app.services import author_service

from app.dependencies import get_current_user, get_current_admin_user
from app.db import models

router = APIRouter(
    prefix="/authors",
    tags=["Authors"]
)

@router.post("/", response_model=AuthorResponse, status_code=status.HTTP_201_CREATED)
def create_author(author: AuthorCreate, db: Session = Depends(get_db), current_user : models.User = Depends(get_current_admin_user)):
    return author_service.create_author(db=db, author=author)

@router.get("/", response_model=List[AuthorResponse])
def get_authors(pagination: dict = Depends(pagination_params), db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    skip_value = pagination["skip"]
    limit_value = pagination["limit"]

    return author_service.get_authors(db=db, offset=skip_value, limit=limit_value)

@router.put("/{author_id}", response_model=AuthorResponse)
def author_update(author_id: int, author_update: AuthorUpdate, db: Session = Depends(get_db), current_user : models.User = Depends(get_current_admin_user)):
    return author_service.update_author(db=db, author_id=author_id, author_data=author_update)

@router.get("/search/", response_model=List[AuthorResponse])
def search_author(name: str, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return author_service.search_authors(db=db, name=name)

@router.delete("/{author_id}")
def delete_author(author_id : int, db: Session = Depends(get_db), current_user = Depends(get_current_admin_user)):
    return author_service.delete_author(db=db, author_id=author_id)