from typing import Optional

from pydantic import BaseModel, ConfigDict


class RequestBase(BaseModel):
    condition: str = 'На рассмотрении'
    item_id: int


class RequestModelId(RequestBase):
    id: int
    user_id: int
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)


class RequestDep(RequestModelId):
    username: str
    item_name: str | None


class RequestUpdateCond(BaseModel):
    condition: Optional[str] = 'На рассмотрении'
