from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional


class UserModel(BaseModel):
    name: str
    email: EmailStr
    role: Optional[str] = "User"


class User(UserModel):
    id: int

    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)


class UserCreate(UserModel):
    pass
