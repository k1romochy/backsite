from typing import TYPE_CHECKING

from sqlalchemy.orm import mapped_column, Mapped, relationship

from .user import User
from .base import Base


class Item(Base):
    name: Mapped[str] = mapped_column(nullable=False)
    quantity: Mapped[int] = mapped_column(nullable=False)

    user_id: Mapped[int] = mapped_column(nullable=False)
    user: Mapped[User] = relationship('User', back_populates='items')