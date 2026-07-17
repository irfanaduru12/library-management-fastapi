from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.db.database import get_db
from app.schemas import book as schemas
from app.crud import crud_book as crud
from app.api.routes.dependencies.dependencies import pagination_params

router = APIRouter()

@router.post("/", response_model=schemas.BookResponse, status_code=status.HTTP_201_CREATED)
def add_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    return crud.create_book(db=db, book=book)

@router.get("/search/", response_model=List[schemas.BookResponse])
def search_books(title: Optional[str] = None, author_name: Optional[str] = None, db: Session = Depends(get_db)):
    books = crud.search_books(db=db, title=title, author_name=author_name)
    if not books:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book cannot be found")

    return books 

@router.get("/", response_model=List[schemas.BookResponse])
def get_all_books(pagination = Depends(pagination_params), db: Session = Depends(get_db)):
    skip_value = pagination["skip"]
    limit_value = pagination["limit"]
    return crud.get_all_books(db=db, skip=skip_value, limit=limit_value)

@router.get("/{book_id}", response_model=schemas.BookResponse)
def get_book(book_id: int, db: Session = Depends(get_db)):
    db_book = crud.get_book(db=db, book_id=book_id)
    if db_book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The book with id {book_id} cannot be found")
    
    return db_book

@router.put("/{book_id}", response_model=schemas.BookResponse)
def update_book(book_id : int, book_update: schemas.BookUpdate, db: Session = Depends(get_db)):
    db_book = crud.get_book(db=db, book_id=book_id)
    if db_book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The book with id {book_id} cannot be found")
    
    return crud.update_book(db=db, db_book=db_book, book_update=book_update)

@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    db_book = crud.get_book(db=db, book_id=book_id)
    if db_book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The book with id {book_id} cannot be found")
    
    return crud.delete_book(db=db, db_book=db_book)