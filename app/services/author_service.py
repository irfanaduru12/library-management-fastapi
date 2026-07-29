from sqlalchemy.orm import Session
from fastapi import HTTPException, status 
from app.db import models
from app.schemas.author import AuthorUpdate, AuthorCreate

def create_author(db: Session, author: AuthorCreate):
    db_author = models.Author(
        name = author.name,
        birth_date = author.birth_date
    )

    db.add(db_author)
    db.commit()
    db.refresh(db_author)

    return db_author

def get_authors(db: Session, offset: int = 0, limit: int = 10):
    return db.query(models.Author).offset(offset).limit(limit).all()

def get_author(db: Session, author_id: int):
    return db.query(models.Author).filter(models.Author.id == author_id).first()

def update_author(db: Session, author_id: int, author_data: AuthorUpdate):
    author = get_author(db, author_id=author_id)

    if not author:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Author with id {author_id} cannot be found")
    
    update_data = author_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(author, key, value)

    db.commit()
    db.refresh(author)

    return author

def search_authors(db: Session, name: str):
    authors = db.query(models.Author).filter(models.Author.name.ilike(f"%{name}%")).all()

    if not authors:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Authors cannot be found")
    
    return authors

def delete_author(db: Session, author_id: int):
    author = get_author(db=db, author_id=author_id)

    if not author:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Author cannot be found")

    db.delete(author)
    db.commit()

    return {"message": "Author succesfully deleted"}
