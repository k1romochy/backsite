from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Enum
from enum import Enum as PyEnum
from sqlalchemy.orm import mapped_column, Mapped, relationship

from .user import User
from .base import Base

if TYPE_CHECKING:
    from .user import User


class Role(PyEnum):
    USER = 'User'
    ADMIN = 'Admin'


class Item(Base):
    name: Mapped[str] = mapped_column(nullable=False)
    quantity: Mapped[int] = mapped_column(nullable=False)
    condition: Mapped[str] = mapped_column(nullable=False)

    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    user: Mapped['User'] = relationship('User', back_populates='items')
