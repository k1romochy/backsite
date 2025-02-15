from typing import TYPE_CHECKING

from sqlalchemy.orm import mapped_column, Mapped, relationship

from .base import Base

if TYPE_CHECKING:
    from .item import Item
    from .cookie import SessionModel
    from .message import Message
    from .request import Request
    from .order import Order


class User(Base):
    username: Mapped[str] = mapped_column(nullable=False)
    password: Mapped[bytes] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(unique=True)
    role: Mapped[str] = mapped_column(nullable=False, server_default='User')

    items: Mapped[list['Item']] = relationship('Item', secondary='item_user_association', back_populates='users')
    session: Mapped['SessionModel'] = relationship('SessionModel', back_populates='user',
                                                    cascade="all, delete-orphan")
    messages: Mapped[list['Message']] = relationship('Message', back_populates='user')
    requests: Mapped[list['Request']] = relationship('Request', back_populates='user')
    orders: Mapped[list['Order']] = relationship('Order', back_populates='user')
