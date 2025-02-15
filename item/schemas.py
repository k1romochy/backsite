from pydantic import BaseModel, EmailStr, Field, ConfigDict

from typing import Annotated, List
from annotated_types import MaxLen, MinLen

from user.schemas import User


class ItemModel(BaseModel):
    name: str
    quantity: int
    condition: str


class Item(ItemModel):
    id: int
    user_id: int

    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)


class ItemCreate(ItemModel):
    pass


class ItemUpdateRequest(BaseModel):
    quantity: int
    condition: str


class ItemUsersRequests(Item):
    users: list[User]
