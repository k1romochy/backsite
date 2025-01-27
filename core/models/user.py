from typing import TYPE_CHECKING

from sqlalchemy.orm import mapped_column, Mapped, relationship

from .base import Base

if TYPE_CHECKING:
    from .item import Item


class User(Base):
    username: Mapped[str] = mapped_column(nullable=False)
    password: Mapped[bytes] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(unique=True)
    role: Mapped[str] = mapped_column(nullable=False, server_default='User')

    items: Mapped[list['Item']] = relationship('Item', back_populates='user')
