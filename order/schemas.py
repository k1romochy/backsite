import datetime
from typing import List

from pydantic import BaseModel, ConfigDict

from item.schemas import ItemModel


class OrderModel(BaseModel):
    name: str
    cost: int
    items: List[int]


class OrderModelId(OrderModel):
    id: int
    user_id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)