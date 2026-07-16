from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.schemas.author import AuthorCreate, AuthorResponse, AuthorUpdate
from app.crud import crud_author

router = APIRouter(
    prefix="/authors",
    tags=["Authors"]
)

@router.post("/", response_model=AuthorResponse, status_code=status.HTTP_201_CREATED)
def create_author(author: AuthorCreate, db: Session = Depends(get_db)):
    return crud_author.create_author(db=db, author=author)

@router.get("/", response_model=List[AuthorResponse])
def get_authors(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud_author.get_authors(db=db, skip=skip, limit=limit)

@router.put("/{author_id}", response_model=AuthorResponse)
def author_update(author_id: int, author_update: AuthorUpdate, db: Session = Depends(get_db)):
    db_author = crud_author.get_author(db, author_id=author_id)

    if db_author is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="There is no writer with id : {author_id}")
    
    return crud_author.update_author(db=db, db_author=db_author, author_update=author_update)