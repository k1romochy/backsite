from pydantic import BaseModel, EmailStr, Field, ConfigDict

from typing import Annotated
from annotated_types import MaxLen, MinLen


class ItemModel(BaseModel):
    id: int
    name: str
    quantity: int

    model_config = ConfigDict(from_attributes=True)


class ItemCreate(ItemModel):
    pass
