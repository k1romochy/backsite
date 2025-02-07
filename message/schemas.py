from pydantic import BaseModel


class MessageModel(BaseModel):
    message: str
    user_id: int