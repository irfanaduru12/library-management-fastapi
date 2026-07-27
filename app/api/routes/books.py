from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.db.database import get_db
from app.schemas import book as schemas
from app.crud import crud_book as crud
from app.api.routes.dependencies.dependencies import pagination_params
from app.services import book_service

from app.dependencies import get_current_user
from app.db import models

router = APIRouter(prefix="/api/routes/books", 
tags=["Books"])

@router.post("/", response_model=schemas.BookResponse, status_code=status.HTTP_201_CREATED)
def add_book(book: schemas.BookCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return crud.create_book(db=db, book=book)

@router.get("/search/", response_model=List[schemas.BookResponse])
def search_books(title: Optional[str] = None, author_name: Optional[str] = None, db: Session = Depends(get_db)):
    return book_service.search_books(db=db, title=title, author_name=author_name) 

@router.get("/", response_model=List[schemas.BookResponse])
def get_all_books(pagination = Depends(pagination_params), db: Session = Depends(get_db)):
    skip_value = pagination["skip"]
    limit_value = pagination["limit"]
    return crud.get_all_books(db=db, skip=skip_value, limit=limit_value)

@router.get("/{book_id}", response_model=schemas.BookResponse)
def get_book(book_id: int, db: Session = Depends(get_db)):
    return book_service.get_book(db=db, book_id=book_id)
    
@router.put("/{book_id}", response_model=schemas.BookResponse)
def update_book(book_id : int, book_update: schemas.BookUpdate, db: Session = Depends(get_db), current_user : models.User = Depends(get_current_user)):
    return book_service.update_book(db=db, book_id=book_id, book_data=book_update)

@router.delete("/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db), current_user : models.User = Depends(get_current_user)):
    return book_service.delete_book(db=db, book_id=book_id)