from pydantic import BaseModel, EmailStr
from typing import Literal

class UserBase(BaseModel):
    name: str
    email: EmailStr
    profile: str
    
class UserCreate(UserBase):
    password: str
    profile: Literal['admin', 'startup']
    startupName: str | None = None

class UserUpdate(BaseModel):
    name: str | None = None
    email: str | None = None
    password: str | None = None
    profile: Literal['admin', 'startup'] | None = None
    startupName: str | None = None

class User(UserBase):
    id: int
