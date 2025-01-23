from pydantic import BaseModel, EmailStr
from typing import Optional


class UserModel(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: Optional[str] = "User"

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    role: Optional[str] = "User"
