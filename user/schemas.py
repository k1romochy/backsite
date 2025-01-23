from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional


class UserModel(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: Optional[str] = "User"

    model_config = ConfigDict(from_attributes=True)


class UserCreate(BaseModel):
    pass
