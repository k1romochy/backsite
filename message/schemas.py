import datetime

from pydantic import BaseModel, ConfigDict


class MessageModel(BaseModel):
    message: str | None
    item_id: int | None


class MessageModelId(MessageModel):
    id: int
    user_id: int
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)


class MessageUpdateMess(BaseModel):
    message: str


class MessageItem(MessageModelId):
    username: str
    item_name: str | None
    created_at: datetime
