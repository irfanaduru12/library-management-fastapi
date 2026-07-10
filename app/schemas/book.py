from pydantic import BaseModel, ConfigDict
from typing import Optional

class BookBase(BaseModel):
    title: str
    author: str
    isbn: str

class BookCreate(BookBase):
    pass

class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    isbn: Optional[str] = None
    is_borrowed: Optional[bool] = None

class BookResponse(BookBase):
    id: int
    is_borrowed: bool

    model_config = ConfigDict(from_attributes=True) # turns sqlalchemy objects to JSON

