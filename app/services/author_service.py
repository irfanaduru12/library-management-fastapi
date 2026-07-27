from sqlalchemy.orm import Session
from fastapi import HTTPException, status 
from app.crud import crud_author
from app.schemas.author import AuthorUpdate

def update_author(db: Session, author_id: int, author_data: AuthorUpdate):
    author = crud_author.get_author(db, author_id=author_id)

    if not author:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Author with id {author_id} cannot be found")
    
    return crud_author.update_author(db=db, db_author=author, author_update=author_data)

def search_authors(db: Session, name: str):
    authors = crud_author.search_author(name=name,db=db)

    if not authors:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Authors cannot be found")
    
    return authors