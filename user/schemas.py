from pydantic import BaseModel, EmailStr, Field, ConfigDict

from typing import Annotated
from annotated_types import MaxLen, MinLen


class UserBase(BaseModel):
    username: str
    email: str


class User(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
