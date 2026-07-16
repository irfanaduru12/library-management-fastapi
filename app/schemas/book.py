from pydantic import BaseModel, ConfigDict
from typing import Optional
from app.schemas.author import AuthorResponse

class BookBase(BaseModel):
    title: str
    author_id: Optional[int] = None
    isbn: str

class BookCreate(BookBase):
    pass

class BookUpdate(BaseModel):
    title: Optional[str] = None
    author_id: Optional[int] = None
    isbn: Optional[str] = None
    is_borrowed: Optional[bool] = None

class BookResponse(BookBase):
    id: int
    is_borrowed: bool
    author: Optional[AuthorResponse]

    model_config = ConfigDict(from_attributes=True) # turns sqlalchemy objects to JSON

