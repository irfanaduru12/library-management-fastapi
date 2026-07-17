from pydantic import BaseModel, ConfigDict
from datetime import date
from typing import Optional

class AuthorBase(BaseModel):
    name: str
    birth_date: Optional[date] = None

class AuthorCreate(AuthorBase):
    pass

class AuthorResponse(AuthorBase):
    id: int
    
    model_config = ConfigDict(from_attributes=True)

class AuthorUpdate(BaseModel):
    name: Optional[str] = None
    birth_date: Optional[date] = None


