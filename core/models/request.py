from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

if TYPE_CHECKING:
    from .user import User
    from .item import Item
from .base import Base


class Request(Base):
    condition: Mapped[str] = mapped_column(server_default='На рассмотрении')
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    user: Mapped['User'] = relationship('User', back_populates='requests')

    item_id: Mapped[int] = mapped_column(ForeignKey('item.id'), nullable=False)
    item: Mapped['Item'] = relationship('Item', back_populates='requests')
