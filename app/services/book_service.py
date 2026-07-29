from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.schemas.book import BookUpdate, BookCreate
from typing import Optional
from app.db import models

def create_book(db: Session, book: BookCreate):
    db_book = models.Book(title = book.title,
                          author_id = book.author_id,
                          isbn = book.isbn,
                          page_number = book.page_number)

    db.add(db_book)
    db.commit()
    db.refresh(db_book)

    return db_book

def search_books(db: Session, title: Optional[str] = None, author_name: Optional[str] = None):
    if not title and not author_name:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Enter a book title or author name")

    query = db.query(models.Book)

    if title:
        query = query.filter(models.Book.title.ilike(f"%{title}%"))

    if author_name:
        query = query.join(models.Author).filter(models.Author.name.ilike(f"%{author_name}%"))

    books = query.all()

    if not books:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="There is no book or author found")

    return books

def get_all_books(db: Session, offset: int = 0, limit: int = 10):
    return db.query(models.Book).offset(offset).limit(limit).all()

def get_book(db: Session, book_id: int):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()

    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The book with id {book_id} cannot be found")
    
    return book

def update_book(db: Session, book_id: int, book_data: BookUpdate):
    book = get_book(db=db, book_id=book_id)

    update_data = book_data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(book, key, value)

    db.commit()
    db.refresh(book)
    
    return book

def delete_book(db: Session, book_id: int):
    book = get_book(db=db, book_id=book_id)

    db.delete(book)
    db.commit()
    return {"message": f"The book with id {book_id} is deleted"}