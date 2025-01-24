from typing import TYPE_CHECKING

from sqlalchemy import Enum
from enum import Enum as PyEnum
from sqlalchemy.orm import mapped_column, Mapped, relationship

from .base import Base

if TYPE_CHECKING:
    from .item import Item


class Role(PyEnum):
    USER = 'User'
    ADMIN = 'Admin'


class User(Base):
    name: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(unique=True)
    role: Mapped[str] = mapped_column(Enum(Role), nullable=False, server_default='User')

    items: Mapped[list['Item']] = relationship('Item', back_populates='user')
