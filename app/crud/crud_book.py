from sqlalchemy.orm import Session
from app.db import models
from app.schemas import book as schemas
from typing import Optional

def get_book(db: Session, book_id: int):
    return db.query(models.Book).filter(models.Book.id == book_id).first()

def get_all_books(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Book).offset(skip).limit(limit).all()

def create_book(db: Session, book: schemas.BookCreate):
    db_book = models.Book(
        title = book.title,
        author_id = book.author_id,
        isbn = book.isbn,
        page_number = book.page_number
    )

    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

def update_book(db: Session, db_book: models.Book, book_update: schemas.BookUpdate):
    update_data = book_update.model_dump(exclude_unset=True) # model_dump turns JSON into dict, exclude_unset only updates not None values

    for key, value in update_data.items():
        setattr(db_book, key, value)

    db.commit()
    db.refresh(db_book)
    return db_book

def delete_book(db: Session, db_book: models.Book):
    db.delete(db_book)
    db.commit()
    return db_book

def search_books(db: Session, title: Optional[str] = None, author_name: Optional[str] = None):
    query = db.query(models.Book)

    if title:
        query = query.filter(models.Book.title.ilike(f"%{title}%"))

    if author_name:
        query = query.join(models.Author).filter(models.Author.name.ilike(f"%{author_name}%"))

    return query.all()