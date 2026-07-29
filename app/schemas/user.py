from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str
    role: str = "user"

class UserResponse(BaseModel):
    id: int
    username: str
    role: str
    is_active: bool
    

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
    