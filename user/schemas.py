from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional

from message.schemas import MessageModelId


class UserModel(BaseModel):
    username: str
    email: EmailStr
    role: Optional[str] = "User"


class User(UserModel):
    id: int

    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)


class UserCreate(UserModel):
    password: str


class UserModelMess(UserModel):
    messages: list[MessageModelId]
