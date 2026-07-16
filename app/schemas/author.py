from pydantic import BaseModel
from datetime import date
from typing import Optional

class AuthorBase(BaseModel):
    name: str
    birth_date: Optional[date] = None

class AuthorCreate(AuthorBase):
    pass

class AuthorResponse(AuthorBase):
    id: int

class AuthorUpdate(BaseModel):
    name: Optional[str] = None
    birth_date: Optional[date] = None

class Config:
    from_attributes = True
