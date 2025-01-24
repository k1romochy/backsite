from pydantic import BaseModel, EmailStr, Field, ConfigDict

from typing import Annotated
from annotated_types import MaxLen, MinLen


class ItemModel(BaseModel):
    name: str
    quantity: int


class Item(ItemModel):
    id: int

    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)


class ItemCreate(ItemModel):
    pass
