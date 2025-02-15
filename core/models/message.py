from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from .user import User
from .base import Base

if TYPE_CHECKING:
    from .user import User


class Message(Base):
    message: Mapped[str] = mapped_column(nullable=False)
    condition: Mapped[str] = mapped_column(server_default='На рассмотрении')

    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    user: Mapped['User'] = relationship('User', back_populates='messages')
