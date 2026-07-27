from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.crud import crud_book
from app.schemas.book import BookUpdate

def search_books(db: Session, title: str | None = None, author_name: str | None = None):
    if not title and not author_name:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Enter a book title or author name")
    
    books = crud_book.search_books(db=db, title=title, author_name=author_name)

    if not books:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="There is no book or author found")

    return books

def get_book(db: Session, book_id: int):
    book = crud_book.get_book(db=db, book_id=book_id)

    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The book with id {book_id} cannot be found")
    
    return book

def update_book(db: Session, book_id: int, book_data: BookUpdate):
    book = crud_book.get_book(db=db, book_id=book_id)

    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The book with id {book_id} cannot be found")
    
    return crud_book.update_book(db=db, db_book=book, book_update=book_data)

def delete_book(db: Session, book_id: int):
    book = crud_book.get_book(db=db, book_id=book_id)

    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The book with id {book_id} cannot be found")
    
    crud_book.delete_book(db=db, db_book=book)

    return {"message": f"The book with id{book_id} is deleted"}