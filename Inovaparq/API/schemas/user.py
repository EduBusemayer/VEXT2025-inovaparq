from pydantic import BaseModel, EmailStr
from typing import Literal

class UserBase(BaseModel):
    name: str
    email: EmailStr
    profile: Literal['admin', 'startup']

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    name: str | None = None
    email: str | None = None
    password: str | None = None
    profile: Literal['admin', 'startup'] | None = None

class User(UserBase):
    id: int
    profile: str



