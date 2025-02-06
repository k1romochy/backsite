from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Enum
from enum import Enum as PyEnum
from sqlalchemy.orm import mapped_column, Mapped, relationship

from .item_user_assoc import ItemUser
from .user import User
from .base import Base

if TYPE_CHECKING:
    from .user import User


class Item(Base):
    name: Mapped[str] = mapped_column(nullable=False)
    quantity: Mapped[int] = mapped_column(nullable=False)
    condition: Mapped[str] = mapped_column(nullable=False)

    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    users: Mapped[list['User']] = relationship('User', secondary='item_user_association', back_populates='items')
