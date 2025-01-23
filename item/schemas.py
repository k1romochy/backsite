from pydantic import BaseModel, EmailStr, Field, ConfigDict

from typing import Annotated
from annotated_types import MaxLen, MinLen


class ItemBase(BaseModel):
    name: str
    quantity: int


class Item(ItemBase):
    model_config = ConfigDict(from_attributes=True)

    id: int