from typing import TYPE_CHECKING

from sqlalchemy.orm import mapped_column, Mapped, relationship

from .base import Base


class User(Base):
    name: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(unique=True)
    role: Mapped[str] = mapped_column(server_default='User')
