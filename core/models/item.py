from typing import TYPE_CHECKING

from sqlalchemy.orm import mapped_column, Mapped, relationship

from . import User
from .base import Base


class Item(Base):
    name: Mapped[str] = mapped_column(nullable=False)
    count: Mapped[int] = mapped_column(nullable=False)
    user: Mapped[User] = mapped_column(relationship(back_populates='user'))
