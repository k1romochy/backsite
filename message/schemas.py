from pydantic import BaseModel, ConfigDict


class MessageModel(BaseModel):
    message: str


class MessageModelId(MessageModel):
    id: int
    user_id: int
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)


class MessageUpdateCond(BaseModel):
    condition: str