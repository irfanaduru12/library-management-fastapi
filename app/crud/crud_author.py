from sqlalchemy.orm import Session
from app.db import models
from app.schemas.author import AuthorCreate, AuthorUpdate

def create_author(db: Session, author: AuthorCreate):
    db_author = models.Author(
        name = author.name,
        birth_date = author.birth_date
    )
    db.add(db_author)
    db.commit()
    db.refresh(db_author)

    return db_author

def get_authors(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Author).offset(skip).limit(limit).all()

def update_author(db: Session, db_author: models.Author, author_update: AuthorUpdate):
    update_data = author_update.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_author,key, value)

    db.commit()
    db.refresh(db_author)
    return db_author

def get_author(db: Session, author_id: int):
    return db.query(models.Author).filter(models.Author.id == author_id).first()

def search_author(name: str, db: Session):
    return db.query(models.Author).filter(models.Author.name.ilike(f"%{name}%")).all()