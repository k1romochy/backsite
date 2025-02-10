from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import mapped_column, Mapped, relationship

if TYPE_CHECKING:
    from .user import User
    from .item import Item
from .base import Base


class Message(Base):
    message: Mapped[str] = mapped_column(nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    user: Mapped['User'] = relationship('User', back_populates='messages')

    item_id: Mapped[int] = mapped_column(ForeignKey('item.id'), nullable=False)
    item: Mapped['Item'] = relationship('Item', back_populates='messages')

    created_at: Mapped[datetime] = mapped_column(
        nullable=False, server_default=func.now()
    )
