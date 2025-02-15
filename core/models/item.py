from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from .user import User
from .base import Base

if TYPE_CHECKING:
    from .order import Order
    from .user import User
    from .message import Message
    from .request import Request


class Item(Base):
    name: Mapped[str] = mapped_column(nullable=False)
    quantity: Mapped[int] = mapped_column(nullable=False)
    condition: Mapped[str] = mapped_column(nullable=False)

    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    users: Mapped[list['User']] = relationship('User', secondary='item_user_association', back_populates='items')

    messages: Mapped[list['Message']] = relationship('Message', back_populates='item')
    requests: Mapped[list['Request']] = relationship('Request', back_populates='item')
    orders: Mapped[list['Order']] = relationship('Order', secondary='item_order_association', back_populates='items')
