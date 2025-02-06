from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy import Table, Column, ForeignKey
from core.models.base import Base

ItemUser = Table(
    "item_user_association",
    Base.metadata,
    Column("user_id", ForeignKey("user.id"), primary_key=True),
    Column("item_id", ForeignKey("item.id"), primary_key=True)
)
